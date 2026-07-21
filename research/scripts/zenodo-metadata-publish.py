#!/usr/bin/env python3
"""
Zenodo Metadata + Publish (Step 3-4 of the publish pipeline)

CRITICAL CREDENTIAL RULE: see zenodo-create-upload.py header. Always read
ZENODO_TOKEN from the environment directly -- never hardcode or retype it.

Reads _zenodo_pending_deposit.json (written by zenodo-create-upload.py).

Usage:
    python zenodo-metadata-publish.py --metadata-file metadata.json [--dry-run]

metadata.json format (Zenodo REST API "metadata" object):
    {
      "title": "...",
      "description": "...",
      "creators": [{"name": "..."}],
      "upload_type": "dataset",
      "access_right": "open",
      "license": "cc-by-4.0",
      "publication_date": "YYYY-MM-DD",
      "version": "v2.0",
      "keywords": ["...", "..."],
      "related_identifiers": [
        {"identifier": "10.5281/zenodo.XXXXXXX", "relation": "isNewVersionOf", "resource_type": "dataset"}
      ]
    }

NOTE the REQUIRED "upload_type" (or equivalently "resource_type") field --
publish fails with HTTP 400 "Missing data for required field" on
metadata.resource_type if this is omitted. Common values: "publication",
"dataset", "software", "poster", "presentation".

--dry-run sets metadata but does NOT call actions/publish, leaving the
deposit as an editable draft. Use this to review on zenodo.org before
committing to an immutable publish.
"""
import requests
import json
import os
import sys
import argparse


def get_token() -> str:
    token = os.environ.get('ZENODO_TOKEN')
    if not token:
        print('ERROR: ZENODO_TOKEN not set in environment.')
        sys.exit(1)
    return token


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata-file', required=True, help='Path to metadata JSON')
    parser.add_argument('--pending-file', default='_zenodo_pending_deposit.json')
    parser.add_argument('--dry-run', action='store_true',
                         help='Set metadata only, skip actions/publish')
    args = parser.parse_args()

    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}

    with open(args.pending_file) as f:
        pending = json.load(f)
    deposit_id = pending['deposit_id']

    with open(args.metadata_file) as f:
        metadata_body = json.load(f)

    if 'upload_type' not in metadata_body and 'resource_type' not in metadata_body:
        print('WARNING: metadata has no upload_type/resource_type -- '
              'publish will fail with HTTP 400. Add "upload_type": "dataset" '
              '(or "publication", "software", etc.)')

    print(f'=== Set metadata (deposit {deposit_id}) ===')
    r = requests.put(
        f'https://zenodo.org/api/deposit/depositions/{deposit_id}',
        headers=headers,
        json={'metadata': metadata_body},
    )
    print(f'Status: {r.status_code}')
    if r.status_code != 200:
        print(f'FAILED: {r.text}')
        sys.exit(1)
    print(f'Title: {r.json()["metadata"].get("title")}')

    if args.dry_run:
        print(f'\nDRY RUN -- deposit left as editable draft: '
              f'https://zenodo.org/deposit/{deposit_id}')
        return

    print('\n=== Publish ===')
    r = requests.post(
        f'https://zenodo.org/api/deposit/depositions/{deposit_id}/actions/publish',
        headers=headers,
    )
    print(f'Status: {r.status_code}')
    if r.status_code != 202:
        print(f'FAILED: {r.text}')
        sys.exit(1)
    data = r.json()
    doi = data['doi']

    print(f'\n===== PUBLISHED =====')
    print(f'DOI: {doi}')
    print(f'URL: https://doi.org/{doi}')
    print(f'Concept DOI: {data["conceptdoi"]}')

    result = {
        'deposit_id': deposit_id,
        'doi': doi,
        'concept_doi': data['conceptdoi'],
        'url': f'https://doi.org/{doi}',
    }
    with open('_zenodo_publish_result.json', 'w') as f:
        json.dump(result, f, indent=2)
    print('\nSaved to _zenodo_publish_result.json -- '
          'copy these values into your project\'s .zenodo_versions.json')

    # Verification (mandatory per research skill Verification Gates table --
    # "trust actual server-side state, not tool return values")
    print('\n=== Verifying live ===')
    v = requests.head(f'https://doi.org/{doi}', allow_redirects=False)
    print(f'doi.org redirect check: HTTP {v.status_code} '
          f'(expect 302)')
    rec = requests.get(f'https://zenodo.org/api/records/{deposit_id}')
    if rec.status_code == 200:
        files = [f['key'] for f in rec.json().get('files', [])]
        print(f'Record files confirmed live: {files}')
    else:
        print(f'WARNING: could not verify record via API: {rec.status_code}')


if __name__ == '__main__':
    main()
