"""Corpus-wide Zenodo metadata gap audit (read-only).
Pulls all deposits once, computes the gap matrix across every
discoverability-relevant field. Evidence for the optimization plan.
"""
import json
import os
import re
import time
import urllib.request

WORK = r"C:\Users\LENOVO\AppData\Local\Temp\deepchat_work"
OUT = os.path.join(WORK, "corpus_gap_audit.txt")
lines = []

def log(s):
    lines.append(str(s))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

with open(r"C:\Users\LENOVO\tokens\zenodo", "r", encoding="utf-8") as f:
    TOKEN = f.read().strip()

AUTH = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "QNFO/Corpus-Audit/1.0",
}

def http_json(url, headers, timeout=60):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        return (resp.status, json.loads(body) if body else {})

# ---- fetch all deposits ----
deposits = []
page = 1
while True:
    url = f"https://zenodo.org/api/deposit/depositions?size=100&page={page}&sort=mostrecent"
    st, data = http_json(url, AUTH)
    if st != 200 or not isinstance(data, list):
        log(f"page {page}: HTTP {st} — stop")
        break
    deposits.extend(data)
    if len(data) < 100:
        break
    page += 1
    time.sleep(0.4)
log(f"TOTAL deposits fetched: {len(deposits)}")

# ---- gap matrix ----
stats = {
    "total": len(deposits),
    "has_desc_200": 0,        # description >= 200 chars (PhilPapers trigger tier)
    "has_desc_50": 0,         # any meaningful description > 50
    "no_desc": 0,             # no description at all
    "has_kw": 0,              # any keywords
    "has_phil_kw": 0,         # philosophy-domain keywords
    "has_orcid": 0,           # person creator with ORCID
    "has_affiliation": 0,     # any creator with affiliation
    "has_subjects": 0,        # subjects field populated
    "has_license": 0,         # license set
    "has_language": 0,        # language set
    "has_related": 0,         # related_identifiers present
    "has_community": 0,       # community membership
    "has_title": 0,
}
licenses = {}
langs = {}
types = {}
author_variants = {}
titleless = []
for dep in deposits:
    m = dep.get("metadata", {})
    title = m.get("title") or ""
    desc = m.get("description") or ""
    kw = m.get("keywords") or []
    creators = m.get("creators") or []
    subj = m.get("subjects") or []
    lic = m.get("license") or {}
    lic_val = lic.get("id") if isinstance(lic, dict) else str(lic)
    lang = m.get("language")
    related = m.get("related_identifiers") or []
    comms = m.get("communities") or []
    ut = m.get("upload_type") or m.get("resource_type", {}).get("subtype") or "?"
    pt = m.get("publication_type") or "?"
    rt = f"{ut}/{pt}"

    if title:
        stats["has_title"] += 1
    else:
        titleless.append(dep.get("id"))
    if len(desc) >= 200:
        stats["has_desc_200"] += 1
    if len(desc) > 50:
        stats["has_desc_50"] += 1
    if not desc:
        stats["no_desc"] += 1
    if kw:
        stats["has_kw"] += 1
    if any(any(p in k.lower() for p in ("philosoph", "epistemolog", "metaphysic", "ontolog")) for k in kw):
        stats["has_phil_kw"] += 1
    # author analysis
    person_orcid = False
    has_affil = False
    for c in creators:
        nm = c.get("name", "")
        if c.get("orcid"):
            person_orcid = True
        if c.get("affiliations") or c.get("affiliation"):
            has_affil = True
        # track name variants (Quni-authored)
        if any(k in nm for k in ("Quni", "Gudzinas", "Rowan")):
            variant = nm
            author_variants[variant] = author_variants.get(variant, 0) + 1
    if person_orcid:
        stats["has_orcid"] += 1
    if has_affil:
        stats["has_affiliation"] += 1
    if subj:
        stats["has_subjects"] += 1
    if lic_val:
        stats["has_license"] += 1
        licenses[lic_val] = licenses.get(lic_val, 0) + 1
    if lang:
        stats["has_language"] += 1
        langs[lang] = langs.get(lang, 0) + 1
    if related:
        stats["has_related"] += 1
    if comms:
        stats["has_community"] += 1
    types[rt] = types.get(rt, 0) + 1

log("")
log("=== GAP MATRIX ===")
log(f"total: {stats['total']}")
log(f"  title:            {stats['has_title']} ({stats['has_title']/stats['total']*100:.0f}%)  [titleless: {len(titleless)}]")
log(f"  desc >=200 chars: {stats['has_desc_200']} ({stats['has_desc_200']/stats['total']*100:.0f}%)  <- PhilPapers trigger tier")
log(f"  desc >50 chars:   {stats['has_desc_50']} ({stats['has_desc_50']/stats['total']*100:.0f}%)")
log(f"  NO desc:          {stats['no_desc']} ({stats['no_desc']/stats['total']*100:.0f}%)  <- ABSTRACT GAP")
log(f"  keywords:         {stats['has_kw']} ({stats['has_kw']/stats['total']*100:.0f}%)")
log(f"  phil keywords:    {stats['has_phil_kw']} ({stats['has_phil_kw']/stats['total']*100:.0f}%)")
log(f"  ORCID (person):   {stats['has_orcid']} ({stats['has_orcid']/stats['total']*100:.0f}%)")
log(f"  affiliation:      {stats['has_affiliation']} ({stats['has_affiliation']/stats['total']*100:.0f}%)")
log(f"  subjects:         {stats['has_subjects']} ({stats['has_subjects']/stats['total']*100:.0f}%)  <- arXiv categories gap")
log(f"  license:          {stats['has_license']} ({stats['has_license']/stats['total']*100:.0f}%)")
log(f"  language:         {stats['has_language']} ({stats['has_language']/stats['total']*100:.0f}%)")
log(f"  related_ident:    {stats['has_related']} ({stats['has_related']/stats['total']*100:.0f}%)  <- citation graph gap")
log(f"  community:        {stats['has_community']} ({stats['has_community']/stats['total']*100:.0f}%)")

log("")
log("=== LICENSE DISTRIBUTION ===")
for k, v in sorted(licenses.items(), key=lambda x: -x[1]):
    log(f"  {k or '(none)'}: {v}")

log("")
log("=== LANGUAGE DISTRIBUTION ===")
for k, v in sorted(langs.items(), key=lambda x: -x[1]):
    log(f"  {k or '(none)'}: {v}")

log("")
log("=== RESOURCE TYPE DISTRIBUTION ===")
for k, v in sorted(types.items(), key=lambda x: -x[1])[:15]:
    log(f"  {k}: {v}")

log("")
log("=== AUTHOR NAME VARIANTS (Quni-authored) ===")
for k, v in sorted(author_variants.items(), key=lambda x: -x[1]):
    log(f"  {v:4d}  {k}")

log("")
log("DONE")
