"""prompt-store-verify.py — permanent DeepChat customPrompts integrity gate.

Read-only. Mirrors the app's exact zod schemas (PromptSchema / PromptParameterSchema /
FileItemSchema / PromptMessageSchema from app.asar /out/main/index.js) and checks:
  1. schema validity of every entry in every store (one bad field fails the WHOLE
     config.listCustomPrompts UI route — the 2026-08-20 'not loading' root cause)
  2. cross-store parity (repo canonical == script canonical == 4 live stores)
  3. template==content on every entry (PROMPT-KEY-SCHEMA-ASYMMETRY-1)

Usage:
  python prompt-store-verify.py           # full verify, exit 0 = healthy
  python prompt-store-verify.py inventory # table of stores + entry counts
Exit codes: 0 healthy | 1 violations found | 2 store unreadable

Scheduled guard: Daily Ops cronjob (216e1d12) check #6 runs this daily; notify-on-failure.
"""
import json, sqlite3, sys, os

DEFAULT_PATHS = {
    "repo": r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills\prompt-stores\customPrompts.json",
    "script": r"C:\Users\LENOVO\.deepchat\scripts\customPrompts-canonical.json",
    "dotdeep_json": r"C:\Users\LENOVO\.deepchat\app-settings.json",
    "roaming_json": r"C:\Users\LENOVO\AppData\Roaming\DeepChat\app-settings.json",
    "roaming_db": r"C:\Users\LENOVO\AppData\Roaming\DeepChat\app_db\agent.db",
    "stub_db": r"C:\Users\LENOVO\.deepchat\agent.db",
}
SRC_ENUM = {"local", "imported", "builtin"}
EXPECTED_IDS = ["cmd-closeout", "cmd-continue", "cmd-execute", "cmd-publish", "cmd-red-team",
                "cmd-research", "cmd-skills-update", "audit-infrastructure",
                "find-papers-on-topic", "validate-citations"]


def validate_prompt(p):
    """Exact mirror of the app's zod schemas. Returns list of violation strings."""
    errs = []
    if not isinstance(p, dict):
        return ["NOT A DICT"]
    # PromptSchema required fields
    if not isinstance(p.get("id"), str) or not p.get("id").strip():
        errs.append("id: non-empty string required")
    if not isinstance(p.get("name"), str):
        errs.append("name: string required")
    if not isinstance(p.get("description"), str):
        errs.append(f"description: string required, got {type(p.get('description')).__name__}")
    if p.get("content") is not None and not isinstance(p.get("content"), str):
        errs.append("content: must be string when present")
    # PromptParameterSchema: name AND required are REQUIRED (not optional)
    params = p.get("parameters")
    if params is not None:
        if not isinstance(params, list):
            errs.append("parameters: array required")
        else:
            for i, pa in enumerate(params):
                if not isinstance(pa, dict):
                    errs.append(f"parameters[{i}]: object required"); continue
                if not isinstance(pa.get("name"), str):
                    errs.append(f"parameters[{i}].name: REQUIRED string, got {pa.get('name')!r}")
                if not isinstance(pa.get("required"), bool):
                    errs.append(f"parameters[{i}].required: REQUIRED bool, got {pa.get('required')!r}")
                if "description" in pa and not isinstance(pa["description"], str):
                    errs.append(f"parameters[{i}].description: string when present")
    # FileItemSchema: id/name/type/path required strings
    files = p.get("files")
    if files is not None:
        if not isinstance(files, list):
            errs.append("files: array required")
        else:
            for i, fi in enumerate(files):
                if not isinstance(fi, dict):
                    errs.append(f"files[{i}]: object required"); continue
                for k in ("id", "name", "type", "path"):
                    if not isinstance(fi.get(k), str):
                        errs.append(f"files[{i}].{k}: REQUIRED string, got {fi.get(k)!r}")
    # PromptMessageSchema: role + content.text required strings
    messages = p.get("messages")
    if messages is not None:
        if not isinstance(messages, list):
            errs.append("messages: array required")
        else:
            for i, ms in enumerate(messages):
                if not isinstance(ms, dict):
                    errs.append(f"messages[{i}]: object required"); continue
                if not isinstance(ms.get("role"), str):
                    errs.append(f"messages[{i}].role: REQUIRED string")
                c = ms.get("content")
                if not isinstance(c, dict) or not isinstance(c.get("text"), str):
                    errs.append(f"messages[{i}].content.text: REQUIRED string")
    if p.get("enabled") is not None and not isinstance(p.get("enabled"), bool):
        errs.append(f"enabled: bool when present, got {p.get('enabled')!r}")
    if p.get("source") is not None and p.get("source") not in SRC_ENUM:
        errs.append(f"source: INVALID {p.get('source')!r} (enum local|imported|builtin)")
    # 2026-08-20 root cause: string timestamps fail z.number().int()
    for k in ("createdAt", "updatedAt"):
        v = p.get(k)
        if v is not None and not isinstance(v, int):
            errs.append(f"{k}: INT REQUIRED, got {type(v).__name__} {v!r}")
    # PROMPT-KEY-SCHEMA-ASYMMETRY-1: fill tool reads content; keep template in sync
    t = p.get("template")
    if isinstance(t, str) and t != p.get("content"):
        errs.append("template != content")
    return errs


def read_store(name, path):
    """Return (entries_or_None, error_string_or_None)."""
    try:
        if name.endswith("_db"):
            c = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=60)
            cols = [r[1] for r in c.execute("PRAGMA table_info(app_settings)").fetchall()]
            if "key" not in cols:
                return None, "app_settings table missing key column"
            valcol = "value_json" if "value_json" in cols else "value"
            row = c.execute(f"SELECT {valcol} FROM app_settings WHERE key='customPrompts'").fetchone()
            c.close()
            if not row:
                return None, "no customPrompts row"
            cp = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        else:
            d = json.load(open(path, encoding="utf-8"))
            cp = d.get("customPrompts") if isinstance(d, dict) and "customPrompts" in d else d
        if not isinstance(cp, list):
            return None, f"not a list ({type(cp).__name__})"
        return cp, None
    except sqlite3.DatabaseError as e:
        # JSON files opened by mistake fall through to json path
        try:
            d = json.load(open(path, encoding="utf-8"))
            cp = d.get("customPrompts") if isinstance(d, dict) and "customPrompts" in d else d
            return (cp, None) if isinstance(cp, list) else (None, f"not a list ({type(cp).__name__})")
        except Exception as e2:
            return None, f"unreadable: {e} / {e2}"
    except Exception as e:
        return None, str(e)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "inventory":
        print(f"{'store':16s} {'entries':>7s} {'violations':>10s}  status")
        for name, path in DEFAULT_PATHS.items():
            cp, err = read_store(name, path)
            if err:
                print(f"{name:16s} {'-':>7s} {'-':>10s}  ERROR {err}")
                continue
            v = sum(len(validate_prompt(p)) for p in cp)
            print(f"{name:16s} {len(cp):7d} {v:10d}  {'OK' if v == 0 else 'INVALID'}")
        return 0

    rc = 0
    results = {}
    for name, path in DEFAULT_PATHS.items():
        cp, err = read_store(name, path)
        if err:
            print(f"[STORE-ERROR] {name}: {err}")
            results[name] = None
            rc = max(rc, 2)
            continue
        results[name] = cp
        v = sum(len(validate_prompt(p)) for p in cp)
        ids = [p.get("id") for p in cp if isinstance(p, dict)]
        missing = [e for e in EXPECTED_IDS if e not in ids]
        if v:
            print(f"[SCHEMA-VIOLATION] {name}: {v} violation(s) — UI list route (config.listCustomPrompts) will fail")
            for p in cp:
                perr = validate_prompt(p)
                if perr:
                    print(f"   id={p.get('id')!r}: {perr}")
            rc = max(rc, 1)
        if missing:
            print(f"[MISSING-IDS] {name}: {missing}")
            rc = max(rc, 1)

    # parity against repo canonical
    repo = results.get("repo")
    if repo is not None:
        for name, cp in results.items():
            if name == "repo" or cp is None:
                continue
            if cp != repo:
                print(f"[DRIFT] {name} differs from repo canonical")
                rc = max(rc, 1)

    rc = max(rc, 1 if check_system_prompt_parity() else 0)

    if rc == 0:
        print("PROMPT-STORE-VERIFY: PASS (schema + parity + system-prompt parity)")
    return rc




# === SYSTEM-PROMPT PARITY (AGENT-PROMPT-PARITY-1, 2026-08-29 remediation) ===
# Checks the system-prompt stores, INCLUDING the agents table row
# (agents.deepchat.config_json.systemPrompt), which was frozen at v3.74
# (2026-08-25) while the canonical stores moved (v3.93).
SYSPROMPT_STORES = {
    "canonical_md":   r"C:\Users\LENOVO\.deepchat\system-prompt-v2.7.md",
    "roaming_json":   r"C:\Users\LENOVO\AppData\Roaming\DeepChat\app-settings.json",
    "dotdeep_json":   r"C:\Users\LENOVO\.deepchat\app-settings.json",
    "app_db_list":    r"C:\Users\LENOVO\AppData\Roaming\DeepChat\app_db\agent.db",
    "stub_db_raw":    r"C:\Users\LENOVO\.deepchat\agent.db",
    "repo_copy_md":    r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills\system-prompt-v2.7.md",
    "agents_row":     r"C:\Users\LENOVO\AppData\Roaming\DeepChat\app_db\agent.db",
}

def read_system_prompt(name, path):
    try:
        if name in ("canonical_md", "repo_copy_md"):
            return open(path, encoding="utf-8").read(), None
        if name in ("roaming_json", "dotdeep_json"):
            return json.load(open(path, encoding="utf-8")).get("default_system_prompt"), None
        if name == "app_db_list":
            c = sqlite3.connect("file:%s?mode=ro" % path, uri=True, timeout=60)
            v = c.execute("SELECT value_json FROM app_settings WHERE key='systemPrompts'").fetchone()
            c.close()
            if not v:
                return None, "no systemPrompts row"
            j = json.loads(v[0])
            if isinstance(j, list) and j:
                return j[0].get("content"), None
            if isinstance(j, str):
                return j, None
            return None, "unexpected shape %s" % type(j).__name__
        if name == "stub_db_raw":
            c = sqlite3.connect("file:%s?mode=ro" % path, uri=True, timeout=60)
            cols = [r[1] for r in c.execute("PRAGMA table_info(app_settings)").fetchall()]
            vc = "value_json" if "value_json" in cols else "value"
            v = c.execute("SELECT %s FROM app_settings WHERE key='systemPrompts'" % vc).fetchone()
            c.close()
            if not v:
                return None, "no systemPrompts row"
            j = v[0]
            if isinstance(j, str) and j.startswith('"'):
                j = json.loads(j)
            return j, None
        if name == "agents_row":
            c = sqlite3.connect("file:%s?mode=ro" % path, uri=True, timeout=60)
            v = c.execute("SELECT config_json FROM agents WHERE id='deepchat'").fetchone()
            c.close()
            if not v:
                return None, "no deepchat agent row"
            return json.loads(v[0]).get("systemPrompt"), None
        return None, "unknown store"
    except Exception as e:
        return None, str(e)

def check_system_prompt_parity():
    vals, errs = {}, 0
    for name, path in SYSPROMPT_STORES.items():
        v, err = read_system_prompt(name, path)
        if err:
            print("[SYSPROMPT-STORE-ERROR] %s: %s" % (name, err))
            errs += 1
            continue
        vals[name] = (v or "").strip()
    ref = vals.get("canonical_md")
    if ref:
        for name, v in vals.items():
            if v != ref:
                print("[SYSPROMPT-DRIFT] %s != canonical_md (len %d vs %d)" % (name, len(v), len(ref)))
                errs += 1
    if errs == 0:
        print("SYSTEM-PROMPT-PARITY: PASS (%d stores identical)" % len(vals))
    return errs


if __name__ == "__main__":
    sys.exit(main())
