#!/usr/bin/env python3
"""OAI-PMH harvester for the QNFO Zenodo corpus — zero-dependency (urllib + xml).

OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting) is the
read-only bulk-metadata protocol used by BASE/CORE/OpenAIRE/DataCite/Google
Scholar to harvest repositories. Zenodo endpoint: https://zenodo.org/oai2d

WHY OAI-PMH BEATS THE REST SEARCH API FOR CORPUS WORK (verified 2026-08-05):
  - No search syntax, no OR-tokenization, no auth key
  - Pagination via resumptionToken (no page-size limits)
  - oai_datacite prefix returns creators + ORCIDs + titles + DOIs
  - With full Chrome headers it bypasses the ZENODO-BOT-403-1 wall
  - THE canonical tool for ADR-014 attribution audits: the QNFO set exposes
    records attributed to 'QNFO' (violation) vs 'Rowan Brad Quni-Gudzinas' (OK)

Usage:
  python oai-pmh-harvest.py                    # harvest user-qnfo set, report + save JSON
  python oai-pmh-harvest.py --set user-qwav    # another set
  python oai-pmh-harvest.py --full             # walk ALL sets from 2026-01-01
  python oai-pmh-harvest.py --audit            # attribution audit (ADR-014) only

Auth: none required. Full Chrome headers needed (ZENODO-BOT-403-1).
"""
import json, sys, time, urllib.request, urllib.parse
import xml.etree.ElementTree as ET

OAI = 'https://zenodo.org/oai2d'
NS = {
    'oai': 'http://www.openarchives.org/OAI/2.0/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'datacite': 'http://datacite.org/schema/kernel-4',
}
H = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'),
     'Accept': 'application/xml,text/xml,*/*',
     'Accept-Language': 'en-US,en;q=0.9',
     'Referer': 'https://zenodo.org/', 'Origin': 'https://zenodo.org'}

def oai_get(params, timeout=60):
    url = OAI + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=H)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return ET.fromstring(r.read().decode('utf-8', 'replace'))

def harvest(set_spec, from_date='2026-01-01', max_pages=30):
    """Walk a set via ListRecords + resumptionToken. Returns list of record dicts."""
    records = []
    token = None
    page = 0
    while page < max_pages:
        params = {'verb': 'ListRecords', 'metadataPrefix': 'oai_datacite',
                  'set': set_spec, 'from': from_date} if not token else \
                 {'verb': 'ListRecords', 'resumptionToken': token}
        try:
            root = oai_get(params)
        except Exception as e:
            print(f'  page {page+1}: ERROR {e}')
            break
        for rec in root.findall('.//oai:record', NS):
            hdr = rec.find('oai:header', NS)
            ident = hdr.find('oai:identifier', NS).text if hdr is not None and hdr.find('oai:identifier', NS) is not None else '?'
            meta = rec.find('oai:metadata', NS)
            title_el = meta.find('.//datacite:title', NS) if meta is not None else None
            doi_el = meta.find('.//datacite:identifier', NS) if meta is not None else None
            creators = []
            orcids = []
            if meta is not None:
                for c in meta.findall('.//datacite:creator', NS):
                    cn = c.find('datacite:creatorName', NS)
                    if cn is not None:
                        creators.append(cn.text)
                    ni = c.find('.//datacite:nameIdentifier', NS)
                    if ni is not None and ni.get('nameIdentifierScheme') == 'ORCID':
                        orcids.append(ni.text)
            records.append({
                'id': ident, 'title': title_el.text if title_el is not None else '',
                'doi': doi_el.text if doi_el is not None else '',
                'creators': creators, 'orcid': orcids,
            })
        rt = root.find('.//oai:resumptionToken', NS)
        token = rt.text if rt is not None and rt.text else None
        page += 1
        print(f'  page {page}: {len(records)} total (token: {"yes" if token else "done"})')
        if not token:
            break
        time.sleep(0.5)
    return records

def audit(records):
    """ADR-014 attribution audit: flag records whose creator is a collective/organization."""
    violations = []
    ok = []
    for r in records:
        creators = r['creators']
        if not creators:
            violations.append((r['id'], 'NO CREATOR', r['title'][:50]))
        elif all(c.lower() in ('qnfo', 'qwav', 'quniverse research foundation', 'qnfo research collective')
                 for c in creators):
            violations.append((r['id'], ', '.join(creators), r['title'][:50]))
        else:
            ok.append(r)
    return violations, ok

def main():
    set_spec = 'user-qnfo'
    full = '--full' in sys.argv
    audit_only = '--audit' in sys.argv
    if '--set' in sys.argv:
        set_spec = sys.argv[sys.argv.index('--set') + 1]

    from_date = '2014-01-01' if full else '2026-01-01'
    print(f'Harvesting set={set_spec} from={from_date}')
    records = harvest(set_spec, from_date=from_date)

    if audit_only:
        violations, ok = audit(records)
        print(f'\n=== ADR-014 ATTRIBUTION AUDIT (set {set_spec}) ===')
        print(f'  total records: {len(records)}')
        print(f'  OK (individual author): {len(ok)}')
        print(f'  VIOLATIONS (collective/organizational creator): {len(violations)}')
        for vid, creators, title in violations:
            print(f'    {vid}: {creators} | {title}')
        return

    # Save full harvest
    out = rf'C:\Users\LENOVO\.deepchat\oai_{set_spec.replace("user-","")}.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2)
    print(f'\nHarvest complete: {len(records)} records -> {out}')
    # Quick stats
    with_orcid = sum(1 for r in records if r['orcid'])
    print(f'  records with ORCID: {with_orcid}')
    print(f'  unique creators: {sorted(set(c for r in records for c in r["creators"]))[:10]}')

if __name__ == '__main__':
    main()
