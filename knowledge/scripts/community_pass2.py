"""Community membership pass (v2): add qnfo community via deposit-metadata
communities field (edit -> set -> PUT -> publish). Runs AFTER the v5 corpus
pass completes (edit-lock conflict avoidance). Skips records already in qnfo.
"""
import json
import os
import time
import urllib.request
import urllib.error

OUT = r"C:\Users\LENOVO\AppData\Local\Temp\deepchat_work\community_pass2.txt"
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
    "User-Agent": "QNFO/1.0",
}

def http_json(url, headers, method="GET", data=None, timeout=60):
    req = urllib.request.Request(url, headers=headers, method=method,
                                 data=data if data is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return (resp.status, json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode("utf-8", errors="ignore"))
        except Exception:
            err = {}
        return (e.code, err)
    except Exception as e:
        return (-1, {"error": str(e)})


def add_community(rid, title):
    """edit -> set communities -> PUT -> publish. Returns status."""
    try:
        st, ed = http_json(
            f"https://zenodo.org/api/deposit/depositions/{rid}/actions/edit",
            AUTH, method="POST")
        if st != 201:
            return f"edit {st}"
        m = ed.get("metadata", {})
        existing = [c.get("identifier") for c in m.get("communities", [])]
        if "qnfo" in existing:
            return "already"
        comms = m.get("communities", [])
        comms.append({"identifier": "qnfo"})
        m["communities"] = comms
        payload = json.dumps({"metadata": m}).encode("utf-8")
        st, pu = http_json(ed["links"]["self"], AUTH, method="PUT", data=payload)
        if st != 200:
            return f"PUT {st}"
        st, fi = http_json(pu["links"]["publish"], AUTH, method="POST")
        if st != 202:
            return f"pub {st}"
        return "added"
    except Exception as e:
        return f"ERR {str(e)[:80]}"


log("=== COMMUNITY PASS v2 (qnfo) ===")

# 1. List all deposits
deposits = []
page = 1
while True:
    st, data = http_json(f"https://zenodo.org/api/deposit/depositions?size=100&page={page}&sort=mostrecent", AUTH)
    if st != 200 or not isinstance(data, list):
        log(f"  page {page}: HTTP {st} — stop")
        break
    deposits.extend(data)
    if len(data) < 100:
        break
    page += 1
    time.sleep(0.4)
log(f"TOTAL: {len(deposits)}")

# 2. Add qnfo community to every titled record not already in it
added = 0
already = 0
errors = 0
for i, dep in enumerate(deposits):
    rid = dep.get("id")
    title = dep.get("metadata", {}).get("title")
    if not rid or not title or title == "?":
        continue
    res = add_community(rid, title)
    if res == "added":
        added += 1
    elif res == "already":
        already += 1
    else:
        errors += 1
        if errors <= 15:
            log(f"  ✗ [{i+1}/{len(deposits)}] {rid} ({title[:40]}): {res}")
    if i % 50 == 0:
        log(f"  ... {i+1}/{len(deposits)} (added={added} already={already} errors={errors})")
    time.sleep(0.3)

log(f"\nRESULT: added={added} already={already} errors={errors}")
log("DONE")
