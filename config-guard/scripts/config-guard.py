#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
config-guard.py v1.0 - DeepChat config pre-write backup + post-write validation guard (2026-08-31).

WHY: config corruption has crashed DeepChat multiple times:
  - 2026-08-31: custom_prompts.json became a top-level OBJECT (imported from a backup zip)
    -> "deepchat:route:invoke: TypeError: prompts.find is not a function" (every prompts route)
  - 2026-08-20: stale hidden settings frame (heal_settings_frame.py)
  - KIF-30: SKILL.md grew 36KB -> 53.8MB (no size guard, no pre-write backup)
  - sync_system_prompt.py: wrote systemPrompts/defaultModel as bare strings into agent.db
    (wrong shapes) -> prompts.find / model-picker crashes on next route invoke

MANDATORY PROTOCOL (HARD GATE) before ANY write to
  %APPDATA%\DeepChat\*.json  or  %APPDATA%\DeepChat\app_db\agent.db (app_settings):
  1. python config-guard.py --snapshot
  2. make the change
  3. python config-guard.py --validate     (if FAIL -> python config-guard.py --restore)
Session start (Phase 0): python config-guard.py --check
Before importing any backup zip: python config-guard.py --scan-zips

Stdlib only. Fast (<2s). --check/--validate/--scan-zips always exit 0 with PASS/FAIL lines.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import shutil
import sqlite3
import sys
import zipfile

APP = os.path.join(os.environ.get("APPDATA", ""), "DeepChat")
USER = os.environ.get("USERPROFILE", "")
BACKUP_ROOT = os.path.join(USER, ".deepchat", "backups", "prewrite")
DB = os.path.join(APP, "app_db", "agent.db")
MAX_PROMPT_FILE_BYTES = 2_000_000  # KIF-30 blowup guard

CONFIG_FILES = [
    "app-settings.json", "custom_prompts.json", "system_prompts.json",
    "mcp-settings.json", "model-config.json", "acp_agents.json",
    "plugin-settings.json", "plugin-tool-policies.json", "database-security.json",
    "knowledge-configs.json", "settings-window-state.json", "window-state.json",
]

LIST_KEYS = ("customPrompts", "systemPrompts")     # must be JSON arrays
DICT_KEYS = ("defaultModel", "preferredModel")     # must be JSON objects


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_file(fn):
    p = os.path.join(APP, fn)
    problems = []
    if not os.path.exists(p):
        return problems
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        return ["JSON-PARSE " + fn + ": " + str(e)]
    if fn == "custom_prompts.json":
        if not isinstance(d, list):
            problems.append("SHAPE " + fn + ": top-level " + type(d).__name__ + ", expected LIST (object form breaks prompts.find -> route crash)")
        elif not all(isinstance(e, dict) and e.get("id") and e.get("name") and "content" in e for e in d):
            problems.append("SHAPE " + fn + ": some entry missing id/name/content")
    if fn == "system_prompts.json":
        if not isinstance(d, dict) or not isinstance(d.get("prompts"), list):
            problems.append("SHAPE " + fn + ": expected {prompts: [...]}, got " + type(d).__name__)
        elif not all(e.get("content") for e in d["prompts"]):
            problems.append("SHAPE " + fn + ": prompt entry missing content")
    if fn in ("custom_prompts.json", "system_prompts.json"):
        sz = os.path.getsize(p)
        if sz > MAX_PROMPT_FILE_BYTES:
            problems.append("SIZE " + fn + ": " + str(sz) + " bytes > " + str(MAX_PROMPT_FILE_BYTES) + " (KIF-30 blowup guard)")
    return problems


def validate_db():
    problems = []
    if not os.path.exists(DB):
        return problems
    try:
        c = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
        for key in LIST_KEYS + DICT_KEYS:
            row = c.execute("SELECT value_json FROM app_settings WHERE key=?", (key,)).fetchone()
            if not row:
                continue
            try:
                v = json.loads(row[0])
            except Exception as e:
                problems.append("DB-JSON " + key + ": " + str(e))
                continue
            if key in LIST_KEYS and not isinstance(v, list):
                problems.append("DB-SHAPE " + key + ": " + type(v).__name__ + ", expected LIST")
            if key in DICT_KEYS and not isinstance(v, dict):
                problems.append("DB-SHAPE " + key + ": " + type(v).__name__ + ", expected DICT")
        c.close()
    except Exception as e:
        problems.append("DB-OPEN: " + str(e))
    return problems


def validate():
    problems = []
    for fn in CONFIG_FILES:
        problems.extend(validate_file(fn))
    problems.extend(validate_db())
    return problems


def snapshot(tag=None):
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    if tag:
        ts += "-" + tag
    dest = os.path.join(BACKUP_ROOT, ts)
    os.makedirs(dest, exist_ok=True)
    manifest = {"created": datetime.datetime.now().isoformat(), "files": {}, "db": {}}
    for fn in CONFIG_FILES:
        p = os.path.join(APP, fn)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(dest, fn))
            manifest["files"][fn] = sha256(p)
    if os.path.exists(DB):
        try:
            c = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
            rows = c.execute("SELECT key, value_json FROM app_settings").fetchall()
            with open(os.path.join(dest, "app_settings.json"), "w", encoding="utf-8") as f:
                json.dump({k: json.loads(v) for k, v in rows}, f, indent=2)
            manifest["db"] = {"app_settings_keys": sorted(r[0] for r in rows)}
            c.close()
        except Exception as e:
            manifest["db_error"] = str(e)
    with open(os.path.join(dest, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("SNAPSHOT:", dest)
    print("  files:", len(manifest["files"]), "db keys:", len(manifest["db"].get("app_settings_keys", [])))
    return dest


def restore(ts=None):
    snaps = sorted(glob.glob(os.path.join(BACKUP_ROOT, "*")))
    if not snaps:
        print("RESTORE: no snapshots found under", BACKUP_ROOT)
        return 1
    src = snaps[-1] if ts is None else os.path.join(BACKUP_ROOT, ts)
    if not os.path.isdir(src):
        print("RESTORE: snapshot not found:", src)
        return 1
    restored = 0
    for fn in CONFIG_FILES:
        p = os.path.join(src, fn)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(APP, fn))
            restored += 1
            print("RESTORED:", fn)
    print("RESTORE: done from", os.path.basename(src), "(", restored, "files )")
    return 0


def scan_zips():
    hits = []
    roots = [os.path.join(APP, "sync", "backups")]
    for root in roots:
        if not os.path.isdir(root):
            continue
        for zp in sorted(glob.glob(os.path.join(root, "*.zip"))):
            try:
                with zipfile.ZipFile(zp) as z:
                    member = next((n for n in z.namelist() if n.endswith("custom_prompts.json")), None)
                    if not member:
                        continue
                    d = json.loads(z.read(member).decode("utf-8"))
                    if not isinstance(d, list):
                        hits.append((zp, type(d).__name__, len(d)))
            except Exception as e:
                hits.append((zp, "ERR", str(e)[:80]))
    if hits:
        print("ZIP-SCAN: DANGEROUS zips (object-format custom_prompts.json - do NOT import):")
        for zp, t, extra in hits:
            print("  ", zp, "->", t, extra)
    else:
        print("ZIP-SCAN: clean (no object-format custom_prompts.json in any backup zip)")
    return 0


def redact_value(v):
    if isinstance(v, dict):
        out = {}
        for k, val in v.items():
            lk = k.lower()
            if isinstance(val, str) and any(s in lk for s in ("key", "token", "secret", "password", "authorization", "cookie")) and len(val) > 8:
                out[k] = val[:6] + "...(redacted)"
            else:
                out[k] = redact_value(val)
        return out
    if isinstance(v, list):
        return [redact_value(x) for x in v]
    return v


def main():
    ap = argparse.ArgumentParser(description="DeepChat config guard")
    ap.add_argument("--check", action="store_true", help="validate everything (session start)")
    ap.add_argument("--validate", action="store_true", help="validate after a write")
    ap.add_argument("--snapshot", action="store_true", help="pre-write backup of configs + DB app_settings")
    ap.add_argument("--tag", default=None, help="snapshot tag suffix")
    ap.add_argument("--restore", nargs="?", const="latest", default=None, help="restore files from snapshot (default latest)")
    ap.add_argument("--scan-zips", action="store_true", help="scan backup zips for object-format prompts")
    ap.add_argument("--redact-snapshot", action="store_true", help="snapshot with secrets redacted (for R2 offsite)")
    args = ap.parse_args()

    if args.restore is not None:
        return restore(None if args.restore == "latest" else args.restore)

    if args.snapshot or args.redact_snapshot:
        dest = snapshot(args.tag)
        if args.redact_snapshot:
            for fn in ("app-settings.json", "mcp-settings.json"):
                p = os.path.join(dest, fn)
                if os.path.exists(p):
                    with open(p, encoding="utf-8") as f:
                        d = json.load(f)
                    with open(p, "w", encoding="utf-8") as f:
                        json.dump(redact_value(d), f, indent=2, ensure_ascii=False)
                    print("REDACT:", fn, "secrets masked (redacted snapshot for offsite only)")
        return 0

    if args.scan_zips:
        return scan_zips()

    problems = validate()
    if problems:
        print("CONFIG-GUARD: FAIL")
        for p in problems:
            print("  -", p)
        print("RECOVERY: python config-guard.py --restore   (restores latest prewrite snapshot)")
        return 0 if args.check else 1
    print("CONFIG-GUARD: PASS (all configs valid, all prompts shapes are arrays/lists)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
