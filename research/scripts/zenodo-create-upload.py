#!/usr/bin/env python3
"""
Zenodo Create + Upload (Step 1-2 of the publish pipeline)

CRITICAL CREDENTIAL RULE (see research/SKILL.md "Zenodo Credential Protocol"):
    ALWAYS read the token from the environment variable directly:
        TOKEN = os.environ.get('ZENODO_TOKEN')
    NEVER hardcode, retype, or manually reconstruct a token string from a
    truncated display (e.g. "prefix...suffix" shown by `Get-ChildItem env:`
    or similar). A single mistyped/dropped character produces a token that
    is subtly wrong -- Zenodo returns the SAME generic
    `{"status":403,"message":"Permission denied."}` for a wrong token as
    for a real-but-scopeless token, making the two failure modes
    indistinguishable by symptom alone. This caused a full session of
    false "token is dead / read-only scope" diagnosis on 2026-07-20 before
    the root cause (a 59-vs-60-character transcription error) was found.

    If you only have a truncated token fragment (e.g. from a prior tool
    output), DO NOT attempt to reconstruct it. Re-read the live
    environment variable instead: `os.environ.get('ZENODO_TOKEN')` in
    Python, or `$env:ZENODO_TOKEN` in PowerShell -- passed through
    directly, never printed-then-retyped.

Usage:
    python zenodo-create-upload.py <bundle-file> [--newversion <deposit_id>]

Behavior:
    --newversion <deposit_id>  : create a new version of an EXISTING
                                  concept (via actions/newversion) instead
                                  of a fresh deposit. Use this for every
                                  publish EXCEPT the very first one for a
                                  project (see .zenodo_versions.json
                                  convention in the research skill).
    (no --newversion)          : create a brand-new deposit/concept DOI.
                                  Only use this for a genuinely new,
                                  unrelated publication -- see the
                                  "Anti-Patterns" table in research
                                  SKILL.md ("Creating a disconnected new
                                  Zenodo deposit for each phase").

Writes _zenodo_pending_deposit.json (ephemeral, gitignored) with the
deposit_id and bucket_url for the next script (zenodo-metadata-publish.py).
"""
import requests
import json
import os
import sys
import argparse


def get_token() -> str:
    token = os.environ.get('ZENODO_TOKEN')
    if not token:
        print(
            'ERROR: ZENODO_TOKEN not set in environment.\n'
            'Set it with: $env:ZENODO_TOKEN = "<your token>"  (PowerShell, current session)\n'
            'or store it persistently via Windows Credential Manager / a .env file\n'
            'loaded at session start. NEVER hardcode it into a script file.'
        )
        sys.exit(1)
    return token


def create_deposit(headers: dict, newversion_of: str | None) -> tuple[int, str, str]:
    """Returns (deposit_id, bucket_url, concept_id)."""
    if newversion_of:
        # Verify the source deposit is reachable and in 'done' state first
        # (research skill C2 fix -- avoid HTTP 403 from a stale deposit id)
        r = requests.get(
            f'https://zenodo.org/api/deposit/depositions/{newversion_of}',
            headers=headers,
        )
        if r.status_code != 200:
            print(f'ERROR: cannot GET source deposit {newversion_of}: '
                  f'{r.status_code} {r.text}')
            sys.exit(1)
        src = r.json()
        if src.get('state') != 'done':
            print(f'ERROR: source deposit {newversion_of} state is '
                  f'"{src.get("state")}", expected "done"')
            sys.exit(1)

        r = requests.post(
            f'https://zenodo.org/api/deposit/depositions/{newversion_of}/actions/newversion',
            headers=headers,
        )
        if r.status_code != 201:
            print(f'ERROR: newversion failed: {r.status_code} {r.text}')
            sys.exit(1)
        data = r.json()
        # newversion returns the ORIGINAL record with a "latest_draft" link;
        # the new draft's own id is embedded in that link.
        latest_draft_url = data['links']['latest_draft']
        new_id = latest_draft_url.rstrip('/').split('/')[-1]
        r2 = requests.get(latest_draft_url, headers=headers)
        if r2.status_code != 200:
            print(f'ERROR: cannot GET new draft {new_id}: {r2.status_code} {r2.text}')
            sys.exit(1)
        draft = r2.json()
        return draft['id'], draft['links']['bucket'], draft['conceptrecid']

    r = requests.post(
        'https://zenodo.org/api/deposit/depositions',
        headers=headers,
        json={},
    )
    if r.status_code != 201:
        print(f'ERROR: create deposit failed: {r.status_code} {r.text}')
        sys.exit(1)
    data = r.json()
    return data['id'], data['links']['bucket'], data['conceptrecid']


def upload_file(headers: dict, bucket_url: str, path: str) -> None:
    name = os.path.basename(path)
    size = os.path.getsize(path)
    print(f'Uploading {name} ({size} bytes)...')
    with open(path, 'rb') as f:
        r = requests.put(f'{bucket_url}/{name}', headers=headers, data=f)
    if r.status_code not in (200, 201):
        print(f'ERROR: upload failed: {r.status_code} {r.text}')
        sys.exit(1)
    print(f'Uploaded: {r.json().get("key")}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bundle', help='Path to the file to upload (e.g. PROVENANCE-BUNDLE.zip)')
    parser.add_argument('--newversion', metavar='DEPOSIT_ID', default=None,
                         help='Create a new version of this existing deposit instead of a fresh one')
    args = parser.parse_args()

    token = get_token()
    print(f'Token length: {len(token)} chars (sanity check only -- lengths vary by token)')
    headers = {'Authorization': f'Bearer {token}'}

    deposit_id, bucket_url, concept_id = create_deposit(headers, args.newversion)
    print(f'Deposit ID: {deposit_id}')
    print(f'Concept ID: {concept_id}')

    upload_file(headers, bucket_url, args.bundle)

    pending = {'deposit_id': deposit_id, 'bucket_url': bucket_url, 'concept_id': concept_id}
    with open('_zenodo_pending_deposit.json', 'w') as f:
        json.dump(pending, f, indent=2)

    print(f'\nDeposit ready: https://zenodo.org/deposit/{deposit_id}')
    print('Next: python zenodo-metadata-publish.py --metadata-file <metadata.json>')


if __name__ == '__main__':
    main()
