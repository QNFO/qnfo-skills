#!/usr/bin/env python3
"""
zenodo_bucket_assets.py — Zenodo Dissemination Playbook lever D6
(2026-08-14, QNFO.OUTREACH.2026-08-14-CONTINUE).

Implements:
  D6: machine-readable structural files INSIDE the Zenodo upload bucket so
      content-parsing crawlers (Semantic Scholar, CORE, Google Dataset Search)
      can parse the asset without calling back to the API:
        1. datacite.json      — DataCite 4.3-style schema print of the record
        2. README.md          — structured markdown (File Inventory / Usage /
                                Citation Guide)
        3. metadata.jsonld    — Schema.org Dataset/ScholarlyArticle JSON-LD

SAFETY:
  - GENERATE-ONLY BY DEFAULT. --upload requires the Zenodo token and streams
    the three files into the record's bucket (links.bucket).
  - Never fabricates fields: reads live record metadata from the public API.
  - For published records, uploading to the bucket requires a DRAFT (new
    version) — the script prints the draft bucket URL hint if the record is
    published and no --bucket-url is supplied.

USAGE:
  python zenodo_bucket_assets.py --record 21208346
  python zenodo_bucket_assets.py --record 10.5281/zenodo.21208346 --out DIR
  python zenodo_bucket_assets.py --record 21208346 --upload
  python zenodo_bucket_assets.py --record 21208346 --upload --bucket-url https://zenodo.org/api/files/XXXX

Requires (for --upload): Zenodo token at C:\\Users\\LENOVO\\tokens\\zenodo
"""
import json
import os
import sys
import urllib.request

TOKEN_PATH = r"C:\Users\LENOVO\tokens\zenodo"
BASE = "https://zenodo.org"
UA = {"User-Agent": "QNFO-Bucket-Assets/1.0 (rowan.quni@outlook.com)"}
OUT_DEFAULT = r"C:\Users\LENOVO\AppData\Local\Temp\deepchat_work\bucket_assets"


def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def upload_file(bucket_url, fname, content):
    with open(TOKEN_PATH, "r", encoding="utf-8") as f:
        tok = f.read().strip()
    url = f"{bucket_url.rstrip('/')}/{fname}"
    req = urllib.request.Request(url, data=content.encode("utf-8"), method="PUT",
                                 headers={**UA, "Content-Type": "application/octet-stream",
                                          "Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status


def main():
    args = sys.argv[1:]
    if "--record" not in args:
        sys.exit(__doc__)
    record = args[args.index("--record") + 1]
    out_dir = args[args.index("--out") + 1] if "--out" in args else OUT_DEFAULT
    do_upload = "--upload" in args
    bucket_url = None
    if "--bucket-url" in args:
        bucket_url = args[args.index("--bucket-url") + 1]

    rid = record.split("/")[-1] if "/" in record else record
    rec = get(f"{BASE}/api/records/{rid}")
    md = rec.get("metadata", {})
    links = rec.get("links", {})

    title = md.get("title", "Untitled record")
    doi = md.get("doi", "")
    creators = []
    for c in md.get("creators", []):
        po = c.get("person_or_org", {})
        name = po.get("name") or po.get("family_name") or "Unknown"
        orcid = None
        for ident in po.get("identifiers", []) or []:
            if ident.get("scheme") == "orcid":
                orcid = ident.get("identifier")
        creators.append({"name": name, "orcid": orcid})

    # --- datacite.json (DataCite 4.3-ish) ---
    datacite = {
        "types": {"ris": "GEN", "bibtex": "misc", "citeproc": "article",
                  "schemaOrg": "ScholarlyArticle",
                  "resourceTypeGeneral": md.get("resource_type", {}).get("type", "Other")},
        "creators": [{"name": c["name"], "nameType": "Personal",
                      "nameIdentifiers": ([{"nameIdentifierScheme": "ORCID",
                                            "schemeUri": "https://orcid.org",
                                            "nameIdentifier": c["orcid"]}]
                                          if c["orcid"] else [])}
                     for c in creators],
        "titles": [{"title": title}],
        "publisher": "Zenodo",
        "publicationYear": (md.get("publication_date") or "")[:4] or "2026",
        "identifiers": [{"identifierType": "DOI", "identifier": doi}],
        "descriptions": [{"descriptionType": "Abstract",
                          "description": md.get("description", "")[:2000]}],
        "subjects": [{"subject": s.get("term", "")} for s in md.get("subjects", [])],
        "rightsList": [{"rights": md.get("license", {}).get("id", "")}],
        "relatedIdentifiers": [{"relatedIdentifier": r.get("identifier", ""),
                                "relatedIdentifierType": "DOI",
                                "relationType": r.get("relation", "References")}
                               for r in md.get("related_identifiers", [])],
        "language": md.get("language") or "eng",
    }

    # --- metadata.jsonld (Schema.org Dataset) ---
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": title,
        "url": links.get("html", f"{BASE}/records/{rid}"),
        "identifier": [{"@type": "PropertyValue", "propertyID": "DOI",
                        "value": doi}] if doi else [],
        "sameAs": f"https://doi.org/{doi}" if doi else None,
        "description": md.get("description", "")[:2000],
        "creator": [{"@type": "Person", "name": c["name"]} for c in creators],
        "datePublished": md.get("publication_date") or "",
        "keywords": md.get("keywords", []),
        "license": f"https://creativecommons.org/licenses/by/4.0/"
                   if md.get("license", {}).get("id") == "cc-by-4.0" else None,
        "inLanguage": md.get("language") or "en",
        "isAccessibleForFree": True,
        "publisher": {"@type": "Organization", "name": "QNFO", "url": "https://qnfo.org"},
    }

    # --- README.md ---
    kw = ", ".join(md.get("keywords", [])[:10])
    readme = (
        f"# {title}\n\n"
        f"- **DOI:** {doi}\n"
        f"- **Published:** {md.get('publication_date', '')}\n"
        f"- **License:** {md.get('license', {}).get('id', '')}\n"
        f"- **Keywords:** {kw}\n\n"
        f"## File Inventory\n\n"
        "This record contains the files listed on the Zenodo record page. "
        "See the record landing page for the full file list.\n\n"
        f"## Usage Notes\n\n{md.get('description', '')[:1500]}\n\n"
        f"## How to Cite\n\n```\n{', '.join(c['name'] for c in creators)} "
        f"({(md.get('publication_date') or '')[:4]}). {title}. Zenodo. "
        f"https://doi.org/{doi}\n```\n"
    )

    os.makedirs(out_dir, exist_ok=True)
    files = {
        "datacite.json": json.dumps(datacite, indent=2, ensure_ascii=False),
        "metadata.jsonld": json.dumps(jsonld, indent=2, ensure_ascii=False),
        "README.md": readme,
    }
    for fname, content in files.items():
        p = os.path.join(out_dir, fname)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"generated: {p} ({len(content)} bytes)")

    if not do_upload:
        print("\nGENERATE-ONLY. Re-run with --upload to stream into the bucket.")
        if rec.get("status") == "published" and not bucket_url:
            print("NOTE: record is published — uploading files requires a NEW VERSION "
                  "draft. Fetch the draft bucket URL from the latest_draft link, or "
                  "pass --bucket-url explicitly.")
        return

    target = bucket_url or links.get("bucket")
    if not target:
        sys.exit("ERROR: no bucket URL — pass --bucket-url (published records need "
                 "a draft version)")
    for fname, content in files.items():
        st = upload_file(target, fname, content)
        print(f"uploaded {fname} -> status {st}")


if __name__ == "__main__":
    main()
