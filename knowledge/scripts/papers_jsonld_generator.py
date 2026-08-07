#!/usr/bin/env python3
"""
papers_jsonld_generator.py — Schema.org ScholarlyArticle JSON-LD generator
for papers.qnfo.org.

Reads the D1 living-paper database (the canonical paper store) and emits:
  1. papers-jsonld.json        — array of ALL ScholarlyArticle blocks
  2. paper-jsonld/<slug>.json  — one file per paper (for Worker injection)
  3. inject.js                 — Worker-side snippet to embed JSON-LD into
                                 the api-router HTML response per paper route
  4. papers-jsonld.html        — <script type="application/ld+json"> blocks
                                 ready to paste into each paper page

WHY: papers.qnfo.org is the user's OWN, indexable property (no noindex,
has sitemap.xml). Adding ScholarlyArticle markup lets Google understand each
paper (title/author/abstract/DOI) and rank it for title/keyword queries —
the Zenodo pages themselves carry noindex and cannot be fixed per-record.

USAGE:
  python papers_jsonld_generator.py [--out DIR]

Requires: Cloudflare API token at C:\\Users\\LENOVO\\tokens\\cloudflare
D1: living-paper (account edb167b78c9fb901ea5bca3ce58ccc4b,
                 db 70a58cb3-b2cd-498d-877f-ecca86859a22)
"""
import json
import os
import sys
import urllib.request
from datetime import datetime

OUT_ROOT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else \
    r"C:\Users\LENOVO\AppData\Local\Temp\deepchat_work\jsonld_out"

ACCOUNT = "edb167b78c9fb901ea5bca3ce58ccc4b"
DB = "70a58cb3-b2cd-498d-877f-ecca86859a22"
TOKEN_PATH = r"C:\Users\LENOVO\tokens\cloudflare"
SITE = "https://papers.qnfo.org"

def dq(sql, params=None):
    with open(TOKEN_PATH, "r", encoding="utf-8") as f:
        tok = f.read().strip()
    body = {"sql": sql}
    if params:
        body["params"] = params
    data = json.dumps(body).encode("utf-8")
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/d1/database/{DB}/query"
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {tok}",
        "Content-Type": "application/json",
        "User-Agent": "QNFO-JSONLD/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

def rows(d):
    if d.get("result") and d["result"][0].get("results"):
        return d["result"][0]["results"]
    return []

def parse_authors(authors_field):
    """authors stored as JSON array or comma string."""
    if not authors_field:
        return []
    a = authors_field
    if isinstance(a, str):
        a = a.strip()
        if a.startswith("["):
            try:
                return json.loads(a)
            except Exception:
                pass
        # comma-separated; handle "Family, Given" awkwardness minimally
        parts = [p.strip() for p in a.split(",")]
        # heuristic: if parts look like names, join alternating
        out = []
        i = 0
        while i < len(parts):
            if i + 1 < len(parts) and parts[i + 1] and not parts[i + 1].endswith("."):
                out.append(f"{parts[i].strip()}, {parts[i+1].strip()}")
                i += 2
            else:
                out.append(parts[i])
                i += 1
        return out
    return a

def build_scholarly_article(row):
    slug = row.get("slug") or ""
    title = row.get("title") or ""
    doi = row.get("doi") or row.get("zenodo_doi") or ""
    abstract = (row.get("abstract") or "")[:3000]
    published = (row.get("published") or "")[:10]
    keywords = row.get("keywords") or ""
    license_v = row.get("license") or "https://creativecommons.org/licenses/by/4.0/"
    authors = parse_authors(row.get("authors"))
    pdf_url = row.get("pdf_url") or (f"{SITE}/papers/{slug}" if slug else "")
    html_url = row.get("html_url") or (f"{SITE}/papers/{slug}" if slug else "")

    if not slug and not doi:
        return None

    author_objs = []
    for name in authors:
        if isinstance(name, dict):
            author_objs.append({"@type": "Person", "name": name.get("name", "")})
        else:
            author_objs.append({"@type": "Person", "name": str(name)})

    kw_list = []
    if keywords:
        if isinstance(keywords, str):
            kw_list = [k.strip() for k in keywords.split(",") if k.strip()][:10]
        elif isinstance(keywords, list):
            kw_list = keywords[:10]

    return {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": title,
        "name": title,
        "url": html_url,
        "identifier": [
            {"@type": "PropertyValue", "propertyID": "DOI", "value": doi}
        ] if doi else [],
        "sameAs": f"https://doi.org/{doi}" if doi else None,
        "author": author_objs,
        "abstract": abstract,
        "datePublished": published,
        "keywords": kw_list,
        "inLanguage": (row.get("language") or "en")[:5],
        "license": license_v,
        "publisher": {
            "@type": "Organization",
            "name": "QNFO",
            "url": "https://qnfo.org",
        },
        "isAccessibleForFree": True,
        "encoding": [
            {
                "@type": "MediaObject",
                "encodingFormat": "application/pdf",
                "contentUrl": pdf_url,
            }
        ] if pdf_url else [],
    }

def main():
    os.makedirs(os.path.join(OUT_ROOT, "paper-jsonld"), exist_ok=True)

    # 1. Fetch papers from D1
    r = dq("SELECT slug, title, doi, zenodo_doi, abstract, published, authors, "
           "keywords, license, language, pdf_url, html_url FROM papers "
           "WHERE status != 'draft' ORDER BY published DESC")
    papers = rows(r)
    print(f"papers from D1: {len(papers)}")

    all_blocks = []
    per_paper = {}
    for row in papers:
        block = build_scholarly_article(row)
        if block:
            all_blocks.append(block)
            slug = row.get("slug")
            if slug:
                per_paper[slug] = block

    # 2. Aggregate file
    with open(os.path.join(OUT_ROOT, "papers-jsonld.json"), "w", encoding="utf-8") as f:
        json.dump(all_blocks, f, indent=2, ensure_ascii=False)
    print(f"aggregate blocks: {len(all_blocks)} -> papers-jsonld.json")

    # 3. Per-paper files
    for slug, block in per_paper.items():
        with open(os.path.join(OUT_ROOT, "paper-jsonld", f"{slug}.json"),
                  "w", encoding="utf-8") as f:
            json.dump(block, f, indent=2, ensure_ascii=False)
    print(f"per-paper files: {len(per_paper)}")

    # 4. HTML <script> blocks for direct paste
    with open(os.path.join(OUT_ROOT, "papers-jsonld.html"), "w", encoding="utf-8") as f:
        f.write("<!-- ScholarlyArticle JSON-LD blocks for papers.qnfo.org -->\n")
        for slug, block in per_paper.items():
            f.write(f"<!-- {slug} -->\n")
            f.write('<script type="application/ld+json">\n')
            f.write(json.dumps(block, indent=2, ensure_ascii=False))
            f.write("\n</script>\n\n")
    print(f"html blocks: {len(per_paper)} -> papers-jsonld.html")

    # 5. Worker injection snippet
    inject = '''// inject.js — api-router Worker snippet: embed paper JSON-LD into HTML.
// Place after the HTML response is constructed, before returning:
//   import jsonldMap from './paper-jsonld/index.js';  // {slug: block}
//   const m = url.pathname.match(/^\\/papers\\/([a-z0-9\\-]+)\\/?$/);
//   if (m && jsonldMap[m[1]]) {
//     body = body.replace('</head>',
//       '<script type="application/ld+json">' +
//       JSON.stringify(jsonldMap[m[1]]) + '</script></head>');
//   }
'''
    with open(os.path.join(OUT_ROOT, "inject.js"), "w", encoding="utf-8") as f:
        f.write(inject)
    print("inject.js written")

    # 6. Manifest for the Worker build step
    manifest = {
        "site": SITE,
        "generated": datetime.utcnow().isoformat() + "Z",
        "paper_count": len(per_paper),
        "papers": [{"slug": s, "doi": b.get("identifier", [{}])[0].get("value") if b.get("identifier") else None}
                   for s, b in per_paper.items()],
    }
    with open(os.path.join(OUT_ROOT, "papers-jsonld-manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("manifest written")

    print(f"\nDONE — output in {OUT_ROOT}")

if __name__ == "__main__":
    main()
