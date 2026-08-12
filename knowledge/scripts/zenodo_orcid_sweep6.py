#!/usr/bin/env python3
"""Zenodo ORCID Coverage Sweep v6 — canonical (git-tracked).

Ensures ORCID 0009-0002-4317-5604 is present on EVERY Rowan-authored Zenodo
deposit/version owned by this account. Supersedes zenodo_fix4.py / sweep v5.

Verified facts (2026-08-12):
- The deposit API (legacy + new RDM) strips any creator field other than
  name/affiliation/orcid — ISNI cannot be stored on Zenodo creators.
  Cross-link path: ORCID profile external identifier (manual web-UI step,
  API write scopes rejected for this client).
- edit -> PUT -> publish in-place metadata cycle preserves the DOI
  (ZENODO-INPLACE-EDIT-1).
- Deposits left in state=inprogress (from prior failed runs) can be
  recovered with PUT(self) -> publish on the pending draft.
- THIRD-PARTY RECORDS MUST NOT GET ROWAN'S ORCID. Only add the person creator
  to deposits whose existing creators are all QNFO-related or empty.
  (2026-08-12 incident: Petina/IFARA records 18143391/18263334/18370178/
  18385504 were wrongly touched; reverted via discard + creator removal.)
- Junk empty drafts (unsubmitted, no title, no creators) are deleted.

Usage:
  python zenodo_orcid_sweep6.py --dry-run   # audit only (truly read-only)
  python zenodo_orcid_sweep6.py             # audit + fix
"""
import json
import sys
import time
import urllib.request
import urllib.error

TOKEN = "BkLOVH2EDBccmqRMEYz0KRjmx9gqnEGKdxSz4RAkwCLgr0yvJUZMJoqjw72g"
ORCID = "0009-0002-4317-5604"
PERSON = {"name": "Quni-Gudzinas, Rowan Brad", "affiliation": "QNFO", "orcid": ORCID}
AUTH = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json",
        "User-Agent": "QNFO/ORCID-Sweep-v6/1.0"}
QNFO_HINTS = ("qnfo", "qwav", "quni", "rowan", "gudzinas", "quniverse", "autaxys", "aiq8")

RESULT = r"C:\Users\LENOVO\AppData\Local\Temp\deepchat_work\orcid_sweep6_result.jsonl"


def http_json(url, headers=None, method="GET", data=None, timeout=40):
    req = urllib.request.Request(url, headers=headers or AUTH, method=method,
                                 data=data if data is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return (resp.status, json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return (e.code, json.loads(body))
        except Exception:
            return (e.code, {"raw": body[:300]})
    except Exception as e:
        return (None, {"raw": str(e)[:150]})


def list_all_deposits():
    deposits = []
    page = 1
    while True:
        url = f"https://zenodo.org/api/deposit/depositions?size=100&page={page}&sort=mostrecent"
        for attempt in range(4):
            st, data = http_json(url)
            if st == 200 and isinstance(data, list):
                deposits.extend(data)
                print(f"  page {page}: +{len(data)} (cumulative {len(deposits)})", flush=True)
                if len(data) < 100:
                    return deposits
                page += 1
                break
            print(f"  page {page} attempt {attempt+1}: HTTP {st} — retrying", flush=True)
            time.sleep(2 + attempt * 2)
        else:
            return deposits
    return deposits


def is_qnfo_related(name):
    n = (name or "").lower()
    return any(h in n for h in QNFO_HINTS)


def rowan_creators(creators):
    return [c for c in (creators or []) if any(h in (c.get("name") or "") for h in ("Quni", "Rowan", "Gudzinas"))]


def org_affiliation(org_name):
    n = org_name or ""
    nl = n.lower()
    if "collective" in nl:
        return "QNFO Research Collective"
    if "qwav" in nl and "qnfo" in nl:
        return "QWAV / QNFO"
    if "qwav" in nl:
        return "QWAV"
    if "foundation" in nl:
        return "Quniverse Research Foundation"
    return "QNFO"


def process_deposit(dep, dry):
    """Classify + (if not dry) fix one deposit. Returns status dict."""
    dep_id = dep.get("id")
    meta = dep.get("metadata", {}) or {}
    title = (meta.get("title") or "?")[:80]
    doi = meta.get("doi", "")
    state = dep.get("state", "")
    creators = meta.get("creators", []) or []

    # empty junk draft
    if state == "unsubmitted" and not (meta.get("title") or "").strip() and not creators:
        if dry:
            return {"status": "junk_draft_would_delete", "dep_id": dep_id}
        st, _ = http_json(f"https://zenodo.org/api/deposit/depositions/{dep_id}", method="DELETE")
        return {"status": "deleted_junk_draft", "dep_id": dep_id, "http": st}

    rowan = rowan_creators(creators)
    if rowan:
        if any(c.get("orcid") == ORCID for c in rowan):
            return {"status": "skip", "dep_id": dep_id, "doi": doi, "title": title}
        # person present, ORCID missing -> add ORCID
        if dry:
            return {"status": "would_fix_orcid", "dep_id": dep_id, "doi": doi, "title": title}
        return fix_orcid(dep, dep_id, doi, title)

    # no Rowan person creator
    if not creators:
        return {"status": "no_creators_skipped", "dep_id": dep_id, "doi": doi, "title": title}
    # THIRD-PARTY GUARD: only add Rowan if EVERY existing creator is QNFO-related
    if not all(is_qnfo_related(c.get("name")) for c in creators):
        return {"status": "third_party_skipped", "dep_id": dep_id, "doi": doi,
                "title": title, "creators": [c.get("name") for c in creators]}
    # org-only QNFO record -> add Rowan person creator alongside
    if dry:
        return {"status": "would_add_person", "dep_id": dep_id, "doi": doi, "title": title}
    return add_person_creator(dep, dep_id, doi, title)


def fix_orcid(dep, dep_id, doi, title):
    """edit -> PUT(creators[].orcid) -> publish; recover inprogress."""
    try:
        if dep.get("state") == "inprogress":
            return _put_publish(dep, dep_id, doi, title, meta=dep.get("metadata", {}),
                                mutate=lambda m: _set_orcid(m))
        st, ed = http_json(f"https://zenodo.org/api/deposit/depositions/{dep_id}/actions/edit",
                           method="POST")
        if st != 201:
            return {"status": "error", "dep_id": dep_id, "doi": doi, "title": title,
                    "error": f"edit HTTP {st} {json.dumps(ed)[:150]}"}
        m = ed.get("metadata", {})
        _set_orcid(m)
        st2, pu = http_json(ed["links"]["self"], method="PUT",
                            data=json.dumps({"metadata": m}).encode("utf-8"))
        if st2 != 200:
            return {"status": "error", "dep_id": dep_id, "doi": doi, "title": title,
                    "error": f"PUT HTTP {st2}"}
        st3, fi = http_json(pu["links"]["publish"], method="POST")
        if st3 != 202:
            return {"status": "error", "dep_id": dep_id, "doi": doi, "title": title,
                    "error": f"publish HTTP {st3}"}
        return {"status": "fixed_orcid", "dep_id": dep_id, "doi": doi, "title": title}
    except Exception as e:
        return {"status": "error", "dep_id": dep_id, "doi": doi, "title": title,
                "error": str(e)[:140]}


def add_person_creator(dep, dep_id, doi, title):
    try:
        org_name = next((c.get("name") for c in (dep.get("metadata", {}).get("creators", []) or [])),
                        "")
        person = dict(PERSON)
        person["affiliation"] = org_affiliation(org_name)
        if dep.get("state") == "unsubmitted":
            m = dict(dep.get("metadata", {}))
            m["creators"] = list(m.get("creators", [])) + [person]
            st, pu = http_json(dep["links"]["self"], method="PUT",
                               data=json.dumps({"metadata": m}).encode("utf-8"))
            return {"status": "draft_creator_added", "dep_id": dep_id, "doi": doi,
                    "title": title, "http": st}
        if dep.get("state") == "inprogress":
            return _put_publish(dep, dep_id, doi, title, meta=dep.get("metadata", {}),
                                mutate=lambda m: m.get("creators", []).append(person))
        st, ed = http_json(f"https://zenodo.org/api/deposit/depositions/{dep_id}/actions/edit",
                           method="POST")
        if st != 201:
            return {"status": "error", "dep_id": dep_id, "doi": doi, "title": title,
                    "error": f"edit HTTP {st} {json.dumps(ed)[:150]}"}
        m = ed.get("metadata", {})
        m["creators"] = list(m.get("creators", [])) + [person]
        st2, pu = http_json(ed["links"]["self"], method="PUT",
                            data=json.dumps({"metadata": m}).encode("utf-8"))
        if st2 != 200:
            return {"status": "error", "dep_id": dep_id, "doi": doi, "title": title,
                    "error": f"PUT HTTP {st2}"}
        st3, fi = http_json(pu["links"]["publish"], method="POST")
        if st3 != 202:
            return {"status": "error", "dep_id": dep_id, "doi": doi, "title": title,
                    "error": f"publish HTTP {st3}"}
        return {"status": "fixed_org_added_person", "dep_id": dep_id, "doi": doi, "title": title}
    except Exception as e:
        return {"status": "error", "dep_id": dep_id, "doi": doi, "title": title,
                "error": str(e)[:140]}


def _set_orcid(m):
    for c in m.get("creators", []):
        if any(h in (c.get("name") or "") for h in ("Quni", "Rowan", "Gudzinas")):
            c["orcid"] = ORCID
            break


def _put_publish(dep, dep_id, doi, title, meta, mutate):
    """Recover a pending inprogress draft: apply mutation, PUT self, publish."""
    m = dict(meta)
    mutate(m)
    st, pu = http_json(dep["links"]["self"], method="PUT",
                       data=json.dumps({"metadata": m}).encode("utf-8"))
    if st != 200:
        return {"status": "error", "dep_id": dep_id, "doi": doi, "title": title,
                "error": f"PUT(draft) HTTP {st}"}
    st2, fi = http_json(pu["links"]["publish"], method="POST")
    if st2 != 202:
        return {"status": "error", "dep_id": dep_id, "doi": doi, "title": title,
                "error": f"publish(draft) HTTP {st2}"}
    return {"status": "fixed_recovered", "dep_id": dep_id, "doi": doi, "title": title}


def main():
    dry = "--dry-run" in sys.argv
    mode = "DRY-RUN" if dry else "FIX"
    print(f"=== ZENODO ORCID SWEEP v6 [{mode}] ===", flush=True)
    print("\n[1] Listing all deposits (all versions)...", flush=True)
    deposits = list_all_deposits()
    print(f"  Total: {len(deposits)}", flush=True)

    print("\n[2] Auditing...", flush=True)
    stats = {"total": len(deposits)}
    lines = []
    for i, dep in enumerate(deposits):
        r = process_deposit(dep, dry)
        stats[r["status"]] = stats.get(r["status"], 0) + 1
        if r["status"] in ("skip",):
            pass
        else:
            print(f"  {r['status']:28s} [{i+1}/{len(deposits)}] {r.get('title','')[:52]} {r.get('error','')}", flush=True)
        lines.append(json.dumps(r, ensure_ascii=False))
        if not dry and r["status"] not in ("skip", "no_creators_skipped", "third_party_skipped"):
            time.sleep(0.4)
        else:
            time.sleep(0.12)

    print(f"\n=== SUMMARY [{mode}] ===", flush=True)
    print(json.dumps(stats, indent=2), flush=True)
    with open(RESULT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Result:", RESULT, flush=True)


if __name__ == "__main__":
    main()
