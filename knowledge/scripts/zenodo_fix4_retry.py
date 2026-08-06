#!/usr/bin/env python3
"""zenodo_fix4 retry pass — clean up transient failures from the first run.

The v4 run had ~66 transient failures (50 DNS getaddrinfo, 11 timeouts,
3x502, 1x503, 1 connection-reset) plus 14 harmless titleless-draft 400s.
This pass re-scans all 900 deposits (idempotent: skips records already
carrying philosophy keywords + ORCID) with:
  - 60s timeouts (vs 30s)
  - up to 3 retries per record on transient errors (DNS/timeout/5xx/connection)
  - same targeted keyword sets + ORCID for person creators

USAGE: python zenodo_fix4_retry.py
"""
import json
import os
import sys
import time
import urllib.request

TOKEN = "BkLOVH2EDBccmqRMEYz0KRjmx9gqnEGKdxSz4RAkwCLgr0yvJUZMJoqjw72g"
ORCID = "0009-0002-4317-5604"
RESULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fix4_retry_result.txt")

AUTH = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "QNFO/PhilPapers-Opt/1.0",
}

PHIL_KW_SETS = {
    "physics": ["philosophy of physics", "foundations of quantum mechanics", "epistemology"],
    "math": ["philosophy of mathematics", "epistemology"],
    "science": ["philosophy of science", "epistemology", "consilience"],
    "default": ["epistemology", "philosophy of science", "consilience"],
}

PHYS_HINTS = ["ultrametric", "p-adic", "quantum", "physic", "zitterbewegung", "qec",
              "bruhat", "tensor network", "compton", "shadows", "quasiparticle", "lorentz"]
MATH_HINTS = ["number", " pi", "math", "valuation", "adelic", "geometry", "counting",
              "positional", "ratio", "frequency"]
SCI_HINTS = ["consilience", "framework", "synthesis", "falsifiability", "scientific",
             "research", "stratigraphy", "paradigm", "audit", "thesis", "foundation"]

TRANSIENT_MARKERS = [
    "getaddrinfo", "timed out", "502", "503", "Remote end closed",
    "Bad Gateway", "Service Unavailable", "timeout", "Connection",
    "IncompleteRead", "urlopen error",
]


def kw_set_for_title(title):
    t = title.lower()
    if any(h in t for h in PHYS_HINTS):
        return PHIL_KW_SETS["physics"]
    if any(h in t for h in MATH_HINTS):
        return PHIL_KW_SETS["math"]
    if any(h in t for h in SCI_HINTS):
        return PHIL_KW_SETS["science"]
    return PHIL_KW_SETS["default"]


def http_json(url, headers, method="GET", data=None, timeout=60):
    req = urllib.request.Request(url, headers=headers, method=method,
                                 data=data if data is not None else None)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        return (resp.status, json.loads(body) if body else {})


def http_json_retry(url, headers, method="GET", data=None, timeout=60, retries=4):
    """http_json with retry-on-transient-error (incl. IncompleteRead)."""
    last_err = None
    for attempt in range(retries):
        try:
            return http_json(url, headers, method=method, data=data, timeout=timeout)
        except Exception as e:
            last_err = str(e)[:140]
            txt = last_err
            transient = any(m in txt for m in TRANSIENT_MARKERS) or "IncompleteRead" in txt
            if transient:
                time.sleep(5 * (attempt + 1))  # backoff 5s, 10s, 15s
                continue
            raise
    raise RuntimeError(f"retries exhausted: {last_err}")


def is_transient(exc_text):
    return any(m in exc_text for m in TRANSIENT_MARKERS)


def list_all_deposits():
    deposits = []
    page = 1
    while True:
        url = f"https://zenodo.org/api/deposit/depositions?size=100&page={page}&sort=mostrecent"
        status, data = http_json_retry(url, AUTH)
        if status != 200 or not isinstance(data, list):
            print(f"  page {page}: HTTP {status} — stopping", flush=True)
            break
        deposits.extend(data)
        print(f"  page {page}: +{len(data)} (cumulative {len(deposits)})", flush=True)
        if len(data) < 100:
            break
        page += 1
        time.sleep(0.5)
    return deposits


def find_person_creator(creators):
    for c in creators or []:
        nm = c.get("name", "")
        if any(k in nm for k in ("Quni", "Rowan", "Gudzinas")):
            return c
    return None


def has_phil_kw(keywords):
    for k in keywords or []:
        kl = k.lower()
        if any(p in kl for p in ("philosoph", "epistemolog", "metaphysic", "ontolog")):
            return True
    return False


def fix_deposit(dep):
    meta = dep.get("metadata", {})
    title = meta.get("title", "?") or "?"
    doi = meta.get("doi", "")
    dep_id = dep.get("id")
    if not dep_id:
        return {"status": "skip", "title": title, "doi": doi, "why": "no id"}

    kw = meta.get("keywords", [])
    person = find_person_creator(meta.get("creators", []))
    has_phil = has_phil_kw(kw)
    has_orcid = bool(person and person.get("orcid"))

    if has_phil and has_orcid:
        return {"status": "skip", "title": title, "doi": doi, "why": "already optimized"}

    changes = []
    if not has_phil:
        add_kw = kw_set_for_title(title)
        existing = {k.lower() for k in kw}
        merged = list(kw)
        for k in add_kw:
            if k.lower() not in existing:
                merged.append(k)
        changes.append(f"+{len(merged) - len(kw)}kw")
    if not has_orcid and person:
        changes.append("orcid")

    last_err = None
    for attempt in range(3):
        try:
            st, ed = http_json(
                f"https://zenodo.org/api/deposit/depositions/{dep_id}/actions/edit",
                AUTH, method="POST")
            if st != 201:
                return {"status": "error", "title": title, "doi": doi,
                        "error": f"edit HTTP {st}"}

            m = ed.get("metadata", {})
            if not has_phil:
                existing = {k.lower() for k in m.get("keywords", [])}
                for k in kw_set_for_title(title):
                    if k.lower() not in existing:
                        m.setdefault("keywords", []).append(k)
            if not has_orcid:
                for c in m.get("creators", []):
                    nm = c.get("name", "")
                    if any(k in nm for k in ("Quni", "Rowan", "Gudzinas")):
                        c["orcid"] = ORCID
                        break

            payload = json.dumps({"metadata": m}).encode("utf-8")
            st, pu = http_json(ed["links"]["self"], AUTH, method="PUT", data=payload)
            if st != 200:
                return {"status": "error", "title": title, "doi": doi,
                        "error": f"PUT HTTP {st}"}

            st, fi = http_json(pu["links"]["publish"], AUTH, method="POST")
            if st != 202:
                return {"status": "error", "title": title, "doi": doi,
                        "error": f"publish HTTP {st}"}

            return {"status": "fixed", "title": title,
                    "doi": fi.get("metadata", {}).get("doi", doi), "changes": changes,
                    "attempts": attempt + 1}
        except Exception as e:
            last_err = str(e)[:140]
            if is_transient(last_err):
                time.sleep(3 * (attempt + 1))  # backoff 3s, 6s
                continue
            return {"status": "error", "title": title, "doi": doi, "error": last_err}

    return {"status": "error", "title": title, "doi": doi, "error": last_err}


def main():
    print("=== ZENODO->PHILPAPERS FIXER v4-RETRY ===", flush=True)

    print("\n[1] Listing deposits (paginated)...", flush=True)
    deposits = list_all_deposits()
    print(f"  Total deposits: {len(deposits)}", flush=True)

    print("\n[2] Re-scanning (idempotent) + fixing transient failures...", flush=True)
    stats = {"total": len(deposits), "skip": 0, "fixed": 0, "error": 0}
    lines = []
    for i, dep in enumerate(deposits):
        r = fix_deposit(dep)
        stats[r["status"]] = stats.get(r["status"], 0) + 1
        if r["status"] == "fixed":
            print(f"  ✓ [{i+1}/{len(deposits)}] {r['title'][:60]} → {r['changes']} (attempt {r.get('attempts',1)})", flush=True)
            lines.append(f"FIXED | {r['doi']} | {r['title'][:70]} | {r['changes']}")
        elif r["status"] == "skip":
            if i % 50 == 0:
                print(f"  ... {i+1}/{len(deposits)} scanned, skipping optimized records", flush=True)
        else:
            print(f"  ✗ [{i+1}/{len(deposits)}] {r['title'][:60]} → {r.get('error','')}", flush=True)
            lines.append(f"ERROR | {r['doi']} | {r['title'][:70]} | {r.get('error','')}")
        time.sleep(0.4)

    summary = f"\n=== SUMMARY [v4-RETRY] ===\n{json.dumps(stats, indent=2)}\n"
    print(summary, flush=True)
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write(summary + "\n".join(lines))
    print(f"Result file: {RESULT_FILE}", flush=True)


if __name__ == "__main__":
    main()
