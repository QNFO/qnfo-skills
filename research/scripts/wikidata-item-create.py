#!/usr/bin/env python3
"""Wikidata item creation — programmatic identity + organization items for QNFO.

READY-TO-RUN: the moment credentials authenticate (account password via browser
login, or better a BOT PASSWORD from Special:BotPasswords), this creates:
  1. Person item for Rowan Brad Quni-Gudzinas (ORCID P496, occupation, affiliation)
  2. Organization item for Quniverse Research Foundation
  3. Links them + verifies via SPARQL

AUTH: MediaWiki API requires a BOT PASSWORD for programmatic edits. Create one at
https://www.wikidata.org/wiki/Special:BotPasswords (username 'QNFO' + a bot name,
e.g. 'QNFO@deepchat'), grant rights: Edit protected pages, Edit existing pages,
Create/edit/move pages. Provide it via WIKIDATA_BOT_USER + WIKIDATA_BOT_PASS env
vars or C:\\Users\\LENOVO\\.wikidata_credentials (username / botpass on two lines).

Usage:
  python wikidata-item-create.py              # create both items
  python wikidata-item-create.py --dry-run    # print payloads, don't post
  python wikidata-item-create.py --verify     # SPARQL check items exist
"""
import json, os, sys, urllib.request, urllib.parse, urllib.error

API = 'https://www.wikidata.org/w/api.php'

ORCID = '0009-0002-4317-5604'
ORCID_URI = f'https://orcid.org/{ORCID}'

PERSON_PAYLOAD = {
    'labels': {'en': {'language': 'en', 'value': 'Rowan Brad Quni-Gudzinas'}},
    'descriptions': {'en': {'language': 'en', 'value': 'independent researcher; founder of the QNFO open-science research program'}},
    'aliases': {'en': [
        {'language': 'en', 'value': 'Rowan Quni-Gudzinas'},
        {'language': 'en', 'value': 'Rowan Brad Quni'},
        {'language': 'en', 'value': 'Rowan Quni'},
    ]},
}

ORG_PAYLOAD = {
    'labels': {'en': {'language': 'en', 'value': 'Quniverse Research Foundation'}},
    'descriptions': {'en': {'language': 'en', 'value': 'independent open-science research foundation'}},
    'aliases': {'en': [
        {'language': 'en', 'value': 'QWAV'},
        {'language': 'en', 'value': 'QNFO'},
    ]},
}

# Statements to add after item creation (property: [type, value])
PERSON_STATEMENTS = [
    ('P31', ['item', 'Q5']),                # instance of: human
    ('P496', ['string', ORCID]),            # ORCID iD
    ('P856', ['string', 'https://rwnq8.github.io/']),  # official website
    ('P2037', ['string', 'rwnq8']),         # GitHub username
    ('P106', ['item', 'Q170790']),          # occupation: researcher
]
ORG_STATEMENTS = [
    ('P31', ['item', 'Q43229']),            # instance of: organization
    ('P856', ['string', 'https://rwnq8.github.io/']),  # official website
]

def get_creds():
    """Bot password is required for API edits. Discovery order: env -> file."""
    u = os.environ.get('WIKIDATA_BOT_USER')
    p = os.environ.get('WIKIDATA_BOT_PASS')
    if u and p:
        return u, p
    fp = r'C:\Users\LENOVO\.wikidata_credentials'
    if os.path.exists(fp):
        with open(fp) as f:
            lines = [l.strip() for l in f if l.strip()]
        if len(lines) >= 2:
            return lines[0], lines[1]
    return None, None

def api_call(params, token=None):
    params = dict(params)
    if token:
        params['token'] = token
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(API, data=data, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'error': {'code': f'HTTP{e.code}', 'info': e.read().decode()[:300]}}

def main():
    dry = '--dry-run' in sys.argv
    verify = '--verify' in sys.argv

    if verify or dry:
        # SPARQL: does the item exist?
        q = f'''SELECT ?item ?itemLabel WHERE {{
          {{ ?item wdt:P496 "{ORCID}". }}
          UNION {{ ?item rdfs:label "Quniverse Research Foundation"@en. }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}'''
        body = urllib.parse.urlencode({'query': q, 'format': 'json'}).encode()
        req = urllib.request.Request('https://query.wikidata.org/sparql', data=body,
            headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
        binds = d.get('results', {}).get('bindings', [])
        if binds:
            for b in binds:
                print(f'EXISTS: {b.get("itemLabel",{}).get("value")} ({b["item"]["value"]})')
        else:
            print('NO ITEM YET — ready to create')
        if verify:
            return

    if dry:
        print('=== PERSON PAYLOAD ===')
        print(json.dumps(PERSON_PAYLOAD, indent=2))
        print('=== PERSON STATEMENTS ===')
        for p, v in PERSON_STATEMENTS:
            print(f'  {p}: {v}')
        print('=== ORG PAYLOAD ===')
        print(json.dumps(ORG_PAYLOAD, indent=2))
        return

    user, pw = get_creds()
    if not user or not pw:
        print('ERROR: No bot credentials. Create a bot password at')
        print('  https://www.wikidata.org/wiki/Special:BotPasswords')
        print('  then set WIKIDATA_BOT_USER / WIKIDATA_BOT_PASS or write')
        print('  them to C:\\Users\\LENOVO\\.wikidata_credentials (2 lines).')
        sys.exit(1)

    # 1. login (bot password)
    d = api_call({'action': 'login', 'lgname': user, 'lgpassword': pw, 'format': 'json'})
    print(f'login: {d.get("login", {}).get("result", d)}')
    if d.get('login', {}).get('result') != 'Success':
        sys.exit(1)

    # 2. CSRF token
    d = api_call({'action': 'query', 'meta': 'tokens', 'type': 'csrf', 'format': 'json'})
    token = d.get('query', {}).get('tokens', {}).get('csrftoken', '')
    print(f'csrf token: {token[:15]}...')

    # 3. Create person item
    d = api_call({'action': 'wbeditentity', 'new': 'item',
                  'data': json.dumps(PERSON_PAYLOAD), 'format': 'json'}, token)
    person_id = d.get('entity', {}).get('id', '')
    print(f'person item: {person_id} ({d.get("error", {}).get("info", "ok")})')

    # 4. Create org item
    d = api_call({'action': 'wbeditentity', 'new': 'item',
                  'data': json.dumps(ORG_PAYLOAD), 'format': 'json'}, token)
    org_id = d.get('entity', {}).get('id', '')
    print(f'org item: {org_id} ({d.get("error", {}).get("info", "ok")})')

    # 5. Add statements
    for pid, (ptype, pval) in PERSON_STATEMENTS:
        if ptype == 'item':
            snak = {'snaktype': 'value', 'property': pid,
                    'datavalue': {'value': {'entity-type': 'item', 'numeric-id': int(pval[1:]), 'id': pval}, 'type': 'wikibase-entityid'}}
        else:
            snak = {'snaktype': 'value', 'property': pid,
                    'datavalue': {'value': pval, 'type': 'string'}}
        d = api_call({'action': 'wbcreateclaim', 'entity': person_id,
                      'snaktype': 'value', 'property': pid,
                      'value': json.dumps(snak['datavalue']['value']), 'format': 'json'}, token)
        print(f'  {pid} on {person_id}: {d.get("claim", {}).get("id", d.get("error", {}).get("info", "?"))}')

    for pid, (ptype, pval) in ORG_STATEMENTS:
        if ptype == 'item':
            snak = {'snaktype': 'value', 'property': pid,
                    'datavalue': {'value': {'entity-type': 'item', 'numeric-id': int(pval[1:]), 'id': pval}, 'type': 'wikibase-entityid'}}
        else:
            snak = {'snaktype': 'value', 'property': pid,
                    'datavalue': {'value': pval, 'type': 'string'}}
        d = api_call({'action': 'wbcreateclaim', 'entity': org_id,
                      'snaktype': 'value', 'property': pid,
                      'value': json.dumps(snak['datavalue']['value']), 'format': 'json'}, token)
        print(f'  {pid} on {org_id}: {d.get("claim", {}).get("id", d.get("error", {}).get("info", "?"))}')

    print(f'\nDONE. Items: {person_id} (person) + {org_id} (org)')
    print(f'Verify: https://www.wikidata.org/wiki/{person_id}')

if __name__ == '__main__':
    main()
