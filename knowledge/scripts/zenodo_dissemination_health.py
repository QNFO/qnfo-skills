#!/usr/bin/env python3
"""
zenodo_dissemination_health.py — Zenodo Dissemination Playbook levers D4-D5
(2026-08-14, QNFO.OUTREACH.2026-08-14-CONTINUE).

Implements:
  D4: Semantic Scholar gap monitoring — probes S2 for QNFO DOIs and reports
      INDEXED vs MISSING (playbook finding 2026-08-14: 5/5 sampled QNFO records
      were 404; upgraded to ENGINE-WIDE — S2 returns 404 for the whole
      10.5281/zenodo.* prefix, incl. highly-cited pycm/coverage.py).
  D5: OpenCitations COCI citation watch — weekly poll of citing-DOI counts
      (playbook baseline 2026-08-14: QUNTUF = 0 citations) + doi.org
      citation_title/citation_abstract meta-tag verification (post-publish
      verification layer).

DESIGNED FOR CRON: --json emits a single-line JSON report; exit 0 = healthy
(no NEW citations, DOI meta OK), exit 1 = new citations found (triggers
follow-up), exit 2 = verification failure (broken URL/meta missing),
exit 3 = both (bitmask; new citations are NEVER masked by a meta failure).

State: keeps last-seen citation counts at
C:\\Users\\LENOVO\\.deepchat\\skills\\knowledge\\scripts\\zenodo_dissemination_state.json
(new citations = count > last-seen; first run seeds the baseline and reports 0).

USAGE:
  python zenodo_dissemination_health.py --doi 10.5281/zenodo.21208346
  python zenodo_dissemination_health.py --doi ... --doi ... --json
  python zenodo_dissemination_health.py --doi ... --no-state   # always report counts

Requires: no tokens (all public APIs). S2 rate limit ~1 req/sec handled
internally (2s sleep).
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "zenodo_dissemination_state.json")
UA = {"User-Agent": "QNFO-Dissemination-Health/1.0 (rowan.quni@outlook.com)"}


def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return -1, str(e)


def load_state():
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def coci_citations(doi):
    """OpenCitations COCI — count citing DOIs."""
    st, body = get(f"https://opencitations.net/index/coci/api/v1/citations/{doi}")
    if st == 404:
        return 0
    if st != 200:
        return None
    try:
        return len(json.loads(body))
    except Exception:
        return None


def s2_status(doi):
    """Semantic Scholar graph API — INDEXED or MISSING (playbook D4)."""
    st, _ = get(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=title")
    return "INDEXED" if st == 200 else ("MISSING" if st == 404 else f"ERROR-{st}")


def doi_meta_ok(doi):
    """doi.org resolution + citation_title/citation_abstract meta tags (D5)."""
    st, body = get(f"https://doi.org/{doi}")
    if st != 200:
        return False, f"doi.org status {st}"
    has_title = re.search(r'<meta[^>]+name=["\']citation_title["\']', body, re.I)
    has_abs = re.search(r'<meta[^>]+name=["\']citation_abstract["\']', body, re.I)
    if not has_title:
        return False, "citation_title meta missing"
    return True, ("ok" + ("" if has_abs else " (citation_abstract missing)"))


def main():
    args = sys.argv[1:]
    dois = []
    for i, a in enumerate(args):
        if a == "--doi":
            dois.append(args[i + 1])
    if not dois:
        sys.exit(__doc__)
    as_json = "--json" in args
    no_state = "--no-state" in args

    state = {} if no_state else load_state()
    report = {"checked": [], "new_citations": []}
    exit_code = 0

    for doi in dois:
        coci = coci_citations(doi)
        time.sleep(0.5)
        s2 = s2_status(doi)
        time.sleep(2)  # S2 rate limit etiquette
        meta_ok, meta_msg = doi_meta_ok(doi)

        prev = state.get(doi, {}).get("coci_last")
        new = (prev is not None and coci is not None and coci > prev)
        state[doi] = {"coci_last": coci, "s2": s2, "checked": time.strftime("%Y-%m-%dT%H:%M:%SZ")}
        if new:
            report["new_citations"].append({"doi": doi, "count": coci, "previous": prev})
            exit_code |= 1
        if not meta_ok:
            exit_code |= 2

        entry = {"doi": doi, "coci_citations": coci, "s2": s2,
                 "doi_meta": meta_msg, "new_citation": new}
        report["checked"].append(entry)
        print(f"{doi}: COCI={coci} | S2={s2} | meta={meta_msg}" +
              (" | *** NEW CITATION ***" if new else ""))

    if not no_state:
        save_state(state)
    if as_json:
        print(json.dumps(report))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
