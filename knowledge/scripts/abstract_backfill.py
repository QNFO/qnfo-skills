"""Abstract backfill: for Zenodo records flagged !desc<200(no-auto-backfill),
find the REAL abstract in D1 living-paper (by zenodo_doi / doi / title match)
and push it to Zenodo via edit->set description->PUT->publish.

NEVER fabricates — only writes when a real abstract (>= 200 chars) is found
in the D1 body_md (YAML abstract: / ## Abstract / first substantial paragraph).
"""
import json
import os
import re
import time
import urllib.request
import urllib.error

WORK = r"C:\Users\LENOVO\AppData\Local\Temp\deepchat_work"
OUT = os.path.join(WORK, "abstract_backfill.txt")
lines = []

def log(s):
    lines.append(str(s))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

with open(r"C:\Users\LENOVO\tokens\cloudflare", "r", encoding="utf-8") as f:
    CT = f.read().strip()
with open(r"C:\Users\LENOVO\tokens\zenodo", "r", encoding="utf-8") as f:
    ZT = f.read().strip()

ACCOUNT = "edb167b78c9fb901ea5bca3ce58ccc4b"
LIVING_PAPER_DB = "70a58cb3-b2cd-498d-877f-ecca86859a22"
ZAUTH = {"Authorization": f"Bearer {ZT}", "Content-Type": "application/json", "User-Agent": "QNFO/1.0"}

def dq(sql, params=None):
    body = {"sql": sql}
    if params:
        body["params"] = params
    data = json.dumps(body).encode("utf-8")
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/d1/database/{LIVING_PAPER_DB}/query"
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {CT}", "Content-Type": "application/json",
        "User-Agent": "QNFO-Backfill/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def rows(d):
    if d.get("result") and d["result"][0].get("results"):
        return d["result"][0]["results"]
    return []

def zh(url, method="GET", data=None):
    req = urllib.request.Request(url, headers=ZAUTH, method=method,
                                 data=data if data is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            return (resp.status, json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        return (e.code, {})
    except Exception as e:
        return (-1, {"error": str(e)})


def extract_abstract(body_md):
    """Extract a real abstract from paper body_md. Returns (abstract, source)."""
    if not body_md:
        return None, "no body"
    b = body_md
    # 1. YAML frontmatter abstract:
    m = re.search(r"^abstract:\s*(.+)$", b, re.M)
    if m:
        a = m.group(1).strip().strip('"\'')
        if len(a) >= 200:
            return a, "yaml"
    # 2. ## Abstract / **Abstract** section
    m = re.search(r"(?:##+\s*Abstract|#+\s*Abstract|\*\*Abstract\*\*|Abstract:)\s*\n+([^\n#]+(?:\n[^\n#]+)*)", b)
    if m:
        a = re.sub(r"\s+", " ", m.group(1)).strip()
        if len(a) >= 200:
            return a, "section"
    # 3. First substantial paragraph after the title (skip headings/refs)
    # take the longest paragraph >= 200 chars that isn't a TOC/ref
    paras = re.split(r"\n\s*\n", b)
    best = None
    for p in paras:
        p = re.sub(r"\s+", " ", p).strip()
        if len(p) >= 200 and not p.startswith(("#", "[", "http", "Table of", "Contents")):
            if best is None or len(p) > len(best):
                best = p
    if best:
        return best, "paragraph"
    return None, "none-found"


def main():
    log("=== ABSTRACT BACKFILL (real sources from D1, never fabricated) ===")

    # 1. Flagged records: from v5 stdout lines containing !desc<200
    flagged = []
    stdout = os.path.join(WORK, "corpus_opt5_stdout.txt")
    if os.path.exists(stdout):
        with open(stdout, "r", encoding="utf-8") as f:
            for l in f:
                if "!desc<200(no-auto-backfill)" in l:
                    # extract zenodo DOI from result file instead (stdout has title only)
                    flagged.append(l.strip()[:110])
    log(f"flagged lines in v5 stdout: {len(flagged)}")

    # 2. Build D1 lookup: zenodo_doi -> body_md (via reconciliation, 412 DOIs now linked)
    log("\n[1] Loading D1 living-paper bodies for zenodo-linked papers...")
    r = dq("SELECT zenodo_doi, body_md FROM papers WHERE zenodo_doi IS NOT NULL AND zenodo_doi != ''")
    d1_map = {}
    for row in rows(r):
        doi = row.get("zenodo_doi", "")
        body = row.get("body_md") or ""
        if doi and doi not in d1_map:
            d1_map[doi] = body
    log(f"  D1 zenodo-linked bodies loaded: {len(d1_map)}")

    # 3. Match flagged Zenodo records (by DOI from the result file)
    # The v5 result file lists fixed DOIs; the !desc ones are flagged but fixed
    # for other fields. We re-list deposits to find records with short desc.
    log("\n[2] Listing Zenodo deposits with short descriptions...")
    deposits = []
    page = 1
    while True:
        st, data = zh(f"https://zenodo.org/api/deposit/depositions?size=100&page={page}&sort=mostrecent")
        if st != 200 or not isinstance(data, list):
            break
        deposits.extend(data)
        if len(data) < 100:
            break
        page += 1
        time.sleep(0.4)
    log(f"  deposits: {len(deposits)}")

    short = []
    for dep in deposits:
        m = dep.get("metadata", {})
        title = m.get("title") or ""
        desc = m.get("description") or ""
        doi = m.get("doi", "")
        if title and title != "?" and len(desc) < 200 and doi:
            short.append({"id": dep.get("id"), "doi": doi, "title": title, "desc_len": len(desc)})
    log(f"  records with description < 200 chars: {len(short)}")

    # 4. Backfill loop
    log("\n[3] Backfilling abstracts from D1 bodies...")
    fixed = 0
    skipped = 0
    for rec in short:
        # find body by DOI (exact or suffix match)
        body = d1_map.get(rec["doi"])
        if not body:
            suffix = rec["doi"].split("/")[-1]
            for k, v in d1_map.items():
                if k.split("/")[-1] == suffix:
                    body = v
                    break
        if not body:
            log(f"  - {rec['doi']} ({rec['title'][:40]}): no D1 body — skip")
            skipped += 1
            continue
        abstract, source = extract_abstract(body)
        if not abstract:
            log(f"  - {rec['doi']} ({rec['title'][:40]}): no abstract extractable ({source}) — skip")
            skipped += 1
            continue
        # push to Zenodo
        st, ed = zh(f"https://zenodo.org/api/deposit/depositions/{rec['id']}/actions/edit", method="POST")
        if st != 201:
            log(f"  x {rec['doi']} ({rec['title'][:40]}): edit {st} — skip")
            skipped += 1
            continue
        m = ed.get("metadata", {})
        m["description"] = abstract
        payload = json.dumps({"metadata": m}).encode("utf-8")
        st, pu = zh(ed["links"]["self"], method="PUT", data=payload)
        if st != 200:
            log(f"  x {rec['doi']} ({rec['title'][:40]}): PUT {st} — skip")
            skipped += 1
            continue
        st, fi = zh(pu["links"]["publish"], method="POST")
        if st == 202:
            log(f"  + {rec['doi']} ({rec['title'][:40]}): abstract from {source} ({len(abstract)} chars)")
            fixed += 1
        else:
            log(f"  x {rec['doi']} ({rec['title'][:40]}): publish {st} — skip")
            skipped += 1
        time.sleep(0.4)

    log(f"\nRESULT: fixed={fixed} skipped={skipped} (of {len(short)} short-desc records)")
    log("DONE")


if __name__ == "__main__":
    main()
