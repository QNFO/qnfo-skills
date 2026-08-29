"""update_templates_v94.py — v3.94 cycle: append the six newversion-publish gates to
cmd-publish + cmd-skills-update in BOTH repo canonicals, content==template."""
import json

REPO = r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills\prompt-stores"
PUBLISH_ADD = ("\n\n2026-08-29 v3.94 additions (system-prompt v3.94 / kaizen v2.114): "
               "NEWVERSION-DRAFT-FILE-KEY-1 (newversion draft file entries may use filename "
               "not key — read f.get('key') or f.get('filename')); "
               "ZENODO-BUCKET-PUT-CANONICAL-1 (POST /files 400 on newversion drafts after "
               "carried-file deletion — upload via bucket PUT {bucket}/{name}?access_token=..., "
               "Content-Type application/octet-stream); "
               "ZENODO-NEWVERSION-STRAY-PURGE-1 (purge stray carried files not in the expected "
               "set via per-file links.self, then assert count == expected before publish); "
               "ZENODO-CONCEPTRECID-COERCE-1 (compare conceptrecid after str() coercion); "
               "BUILD-PDF-BIB-FILENAME-1 (build-pdf.py must locate refs.bib OR references.bib; "
               "verify 0 raw [@ citation keys in the built HTML/PDF before publish); "
               "CITE-AUDIT-LIVE-API-1 (validate sibling DOIs/titles against the LIVE Zenodo "
               "records API, not lagging registry rows). Canonical: RES.032 v0.2 newversion "
               "10.5281/zenodo.22160404.")
SKILLS_ADD = ("\n\n2026-08-29 v3.94 additions: cycle at system-prompt v3.94 / kaizen v2.114 / "
              "research v2.146 / cloudflare v3.69 / qnfo-core v1.39 / execution-mandate v2.13 — "
              "newversion publish gates NEWVERSION-DRAFT-FILE-KEY-1, ZENODO-BUCKET-PUT-CANONICAL-1, "
              "ZENODO-NEWVERSION-STRAY-PURGE-1, ZENODO-CONCEPTRECID-COERCE-1, "
              "BUILD-PDF-BIB-FILENAME-1, CITE-AUDIT-LIVE-API-1 (canonical RES.032 v0.2); "
              "run prompt-store-verify.py exit 0 after any dual-write.")

for name in ("customPrompts.json", "customPrompts-canonical.json"):
    p = REPO + "\\" + name
    d = json.load(open(p, encoding="utf-8"))
    hits = 0
    for e in d:
        if e.get("id") == "cmd-publish":
            e["content"] = (e.get("content") or "") + PUBLISH_ADD
            if "template" in e:
                e["template"] = e["content"]
            hits += 1
        elif e.get("id") == "cmd-skills-update":
            e["content"] = (e.get("content") or "") + SKILLS_ADD
            if "template" in e:
                e["template"] = e["content"]
            hits += 1
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("wrote", name, "entries", len(d), "updated", hits)
