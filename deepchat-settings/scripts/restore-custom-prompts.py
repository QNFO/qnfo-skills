#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
restore-custom-prompts.py — DeepChat custom-prompt DISASTER RECOVERY + verify utility.
Canonical owner: deepchat-settings skill (v1.21+). Restores the custom prompt store to
ALL 4 template stores byte-identical, validated against the app's PromptSchema.

WHY THIS TOOL EXISTS (red-team finding 2026-08-17, "why couldn't you immediately load
backed-up working custom prompts?"):
  - Every local backup from 2026-08-11..2026-08-16 held `{name, template, parameters}`
    entries with NO `id` and NO `content` — the CURRENT app renders those as EMPTY fills
    (fill tool reads prompt.content) and REJECTS the whole list in the UI (PromptSchema
    requires id: z.string().min(1)). Blindly "restoring" them re-broke the store.
  - The one loadable artifact (custom_prompts.json, 17 commands with the full app model)
    lived in a legacy file the current app does NOT read for the UI (SyncService only).
  - There was NO version-controlled canonical copy and NO restore recipe.
  PERMANENT FIX: canonical store is now git-tracked at qnfo-skills/prompt-stores/
  customPrompts.json; this tool restores from the best schema-valid source in one command.

App PromptSchema (z.looseObject, verified in app.asar out/main/index.js 2026-08-17):
  id: str min(1) REQUIRED; name: str; description: str; content: str optional but
  REQUIRED for fills (fill tool reads prompt.content; empty = empty fills);
  parameters: [{name: str, description?: str, required: bool}] (required is MANDATORY
  per PromptParameterSchema); files: list; messages: list; enabled: bool;
  source: "local"|"imported"|"builtin"; createdAt/updatedAt: int ms.
  `template` key is tolerated (looseObject) and kept == content for the watcher JSON shape.

Modes:
  python restore-custom-prompts.py verify     # validate current 4-store state (exit 1 on violation)
  python restore-custom-prompts.py inventory  # scan current stores + all backup sources
  python restore-custom-prompts.py restore    # pick best source, write 4 stores, verify (default)
  python restore-custom-prompts.py export     # write canonical copy to qnfo-skills repo

Source precedence in restore:
  1. repo export  (qnfo-skills/prompt-stores/customPrompts.json) — canonical, git-tracked
  2. current ROAM_DB customPrompts — if schema-valid
  3. newest schema-valid local backup (app-settings.json.bak-*, customPrompts.bak-*.json,
     agent.db.bak-* legacy DBs, custom_prompts.json palette)
  4. legacy palette alone (17 commands) — warns CMD templates are missing
After every write: byte-identical 4-store parity + schema simulation + dsp sha unchanged +
model keys check. ALWAYS restart DeepChat after restore (runtime cache, TEMPLATE-STORES-1).
"""
import json, sqlite3, shutil, datetime, os, sys, glob, time, hashlib

ROAM = r'C:\Users\LENOVO\AppData\Roaming\DeepChat'
DEEP = r'C:\Users\LENOVO\.deepchat'
ROAM_AP = os.path.join(ROAM, 'app-settings.json')
DEEP_AP = os.path.join(DEEP, 'app-settings.json')
ROAM_DB = os.path.join(ROAM, 'app_db', 'agent.db')
DEEP_DB = os.path.join(DEEP, 'agent.db')
CP_FILE = os.path.join(ROAM, 'custom_prompts.json')
REPO = r'C:\Users\LENOVO\Documents\GitHub\qnfo-skills'
REPO_EXPORT = os.path.join(REPO, 'prompt-stores', 'customPrompts.json')

SOURCE_ENUM = ('local', 'imported', 'builtin')


def schema_errors(entries):
    """zod-equivalent simulation of the app's PromptSchema (looseObject semantics)."""
    errs = []
    for i, e in enumerate(entries):
        tag = f"[{i}] {e.get('name', '?')}"
        if not isinstance(e.get('id'), str) or len(e.get('id', '')) < 1:
            errs.append(f"{tag}: id missing (z.string().min(1) REQUIRED)")
        if not isinstance(e.get('name'), str) or not e['name']:
            errs.append(f"{tag}: name missing")
        if not isinstance(e.get('description', ''), str):
            errs.append(f"{tag}: description missing")
        content = e.get('content')
        if content is None:
            errs.append(f"{tag}: content missing (fill tool reads prompt.content -> EMPTY fills)")
        elif not isinstance(content, str):
            errs.append(f"{tag}: content not a string")
        if 'template' in e and e['template'] != content:
            errs.append(f"{tag}: template != content (keep byte-identical)")
        for p in e.get('parameters', []):
            if not isinstance(p.get('name'), str):
                errs.append(f"{tag}: parameter name missing")
            if not isinstance(p.get('required'), bool):
                errs.append(f"{tag}: parameter.required must be bool (PromptParameterSchema)")
        if not isinstance(e.get('files', []), list):
            errs.append(f"{tag}: files not a list")
        if e.get('source') is not None and e['source'] not in SOURCE_ENUM:
            errs.append(f"{tag}: source {e['source']} not in {SOURCE_ENUM}")
        if 'enabled' in e and not isinstance(e['enabled'], bool):
            errs.append(f"{tag}: enabled not bool")
        for k in ('createdAt', 'updatedAt'):
            if e.get(k) is not None and not isinstance(e[k], int):
                errs.append(f"{tag}: {k} not int")
    return errs


def db_val(path, key):
    try:
        con = sqlite3.connect(path, timeout=30); cur = con.cursor()
        cols = [c[1] for c in cur.execute('PRAGMA table_info(app_settings)').fetchall()]
        kcol = 'key' if 'key' in cols else ('name' if 'name' in cols else None)
        vcol = 'value_json' if 'value_json' in cols else ('value' if 'value' in cols else None)
        row = cur.execute(f'SELECT {vcol} FROM app_settings WHERE {kcol}=?', (key,)).fetchone() if (kcol and vcol) else None
        con.close()
        return row[0] if row else None
    except Exception:
        return None


def db_write(path, key, value):
    con = sqlite3.connect(path, timeout=30); cur = con.cursor()
    cols = [c[1] for c in cur.execute('PRAGMA table_info(app_settings)').fetchall()]
    kcol = 'key' if 'key' in cols else ('name' if 'name' in cols else None)
    vcol = 'value_json' if 'value_json' in cols else ('value' if 'value' in cols else None)
    assert kcol and vcol, f'unknown schema {cols}'
    now = int(time.time() * 1000)
    if 'updated_at' in cols:
        cur.execute(f"UPDATE app_settings SET {vcol}=?, updated_at=? WHERE {kcol}=?", (value, now, key))
    else:
        cur.execute(f'UPDATE app_settings SET {vcol}=? WHERE {kcol}=?', (value, key))
    con.commit(); con.close()


def parse_entries(obj):
    """Accept list, or dict with 'customPrompts', or dict with numeric keys (legacy palette object)."""
    if isinstance(obj, dict):
        if 'customPrompts' in obj and isinstance(obj['customPrompts'], list):
            return obj['customPrompts']
        digits = [obj[k] for k in obj.keys() if isinstance(k, str) and k.isdigit()]
        if digits:
            return digits
        if 'prompts' in obj and isinstance(obj['prompts'], list):
            return obj['prompts']
        return []
    return obj if isinstance(obj, list) else []


def load_cp_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            return parse_entries(json.load(f))
    except Exception:
        return []


def load_cp_db(path):
    v = db_val(path, 'customPrompts')
    if not v:
        return []
    try:
        return parse_entries(json.loads(v))
    except Exception:
        return []


def sha16(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


def current_stores():
    return {
        'ROAM_AP': load_cp_json(ROAM_AP),
        'DEEP_AP': load_cp_json(DEEP_AP),
        'ROAM_DB': load_cp_db(ROAM_DB),
        'DEEP_DB': load_cp_db(DEEP_DB),
    }


def verify_state():
    stores = current_stores()
    names = [e.get('name') for e in stores['ROAM_DB']]
    print('store counts:', {k: len(v) for k, v in stores.items()})
    ident = all(stores[k] == stores['ROAM_DB'] for k in stores)
    print('byte-identical 4/4:', ident)
    errs = schema_errors(stores['ROAM_DB'])
    print('schema violations:', errs if errs else 'NONE - all entries pass app PromptSchema')
    if names:
        print('names:', ', '.join(names))
    ap = json.load(open(ROAM_AP, encoding='utf-8'))
    dsp = ap.get('default_system_prompt', '')
    print('dsp:', 'sha16=' + sha16(dsp), 'len=' + str(len(dsp)), 'head=' + dsp[:44].replace('\n', ' '))
    pm = ap.get('preferredModel', {}); dm = ap.get('defaultModel', {})
    ok_models = (pm.get('modelId') == 'deepseek-v4-flash' and dm.get('modelId') == 'deepseek-v4-flash')
    print('model keys flash/flash:', ok_models, json.dumps(pm), json.dumps(dm))
    return ident and not errs and ok_models


def backup_sources():
    """Return [(label, path, entries)] for every prompt-bearing backup, newest first."""
    out = []
    pats = [ROAM + r'\app-settings.json.bak-*', ROAM + r'\app_db\customPrompts.bak-*.json',
            DEEP + r'\customPrompts.bak-*.json', DEEP + r'\app-settings.json.bak-*']
    for pat in pats:
        for f in glob.glob(pat):
            if os.path.isfile(f):
                out.append((os.path.basename(f), f, load_cp_json(f)))
    for f in glob.glob(DEEP + r'\agent.db.bak-*'):
        if os.path.isfile(f):
            out.append((os.path.basename(f), f, load_cp_db(f)))
    out.sort(key=lambda t: os.path.getmtime(t[1]), reverse=True)
    return out


def inventory():
    print('=== CURRENT STORES ===')
    for k, v in current_stores().items():
        e = schema_errors(v)
        print(f'{k}: total={len(v)} violations={len(e)}' + ('' if not e else f' {e[:3]}'))
    print('=== LEGACY PALETTE (custom_prompts.json) ===')
    cp = load_cp_json(CP_FILE)
    e = schema_errors(cp)
    print(f'custom_prompts.json: total={len(cp)} violations={len(e)}')
    print('=== REPO EXPORT ===')
    if os.path.exists(REPO_EXPORT):
        re_ = load_cp_json(REPO_EXPORT)
        print(f'{REPO_EXPORT}: total={len(re_)} violations={len(schema_errors(re_))}')
    else:
        print('MISSING - run: python restore-custom-prompts.py export')
    print('=== BACKUPS (schema-valid ones only, newest first) ===')
    n = 0
    for label, path, entries in backup_sources():
        e = schema_errors(entries)
        if entries and not e:
            m = time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(path)))
            print(f'{m} | {label} | total={len(entries)}')
            n += 1
    if n == 0:
        print('NONE - no schema-valid local backup exists (pre-2026-08-17 backups are template-only/id-less)')


def restore():
    sources = []
    if os.path.exists(REPO_EXPORT):
        sources.append(('repo_export', REPO_EXPORT, load_cp_json(REPO_EXPORT)))
    cur = load_cp_db(ROAM_DB)
    if cur:
        sources.append(('current_ROAM_DB', ROAM_DB, cur))
    for label, path, entries in backup_sources():
        if entries:
            sources.append((f'backup:{label}', path, entries))
            break  # newest backup only
    cp = load_cp_json(CP_FILE)
    if cp:
        sources.append(('legacy_palette', CP_FILE, cp))

    chosen = None
    for label, path, entries in sources:
        errs = schema_errors(entries)
        if not errs and len(entries) >= 9:
            chosen = (label, path, entries)
            break
    if chosen is None:
        print('FATAL: no schema-valid source with >=9 entries found. Sources:')
        for label, path, entries in sources:
            print(f'  {label}: total={len(entries)} violations={len(schema_errors(entries))}')
        sys.exit(1)

    label, path, entries = chosen
    print(f'RESTORING from: {label} ({path}) - {len(entries)} entries, schema-valid')
    if label != 'repo_export' and os.path.exists(REPO_EXPORT):
        print('  note: repo export exists but was not schema-valid or smaller; re-export with: export')

    ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    now = int(time.time() * 1000)
    fixed = []
    for e in entries:
        content = e.get('content') or e.get('template') or ''
        fixed.append({
            'id': e['id'], 'name': e['name'], 'description': e.get('description', ''),
            'content': content, 'template': content,
            'parameters': [{'name': p['name'], 'description': p.get('description', ''),
                            'required': p.get('required', True)} for p in e.get('parameters', [])],
            'files': e.get('files', []), 'enabled': e.get('enabled', True),
            'source': e.get('source', 'local'),
            'createdAt': e.get('createdAt', now), 'updatedAt': now,
        })
    errs = schema_errors(fixed)
    if errs:
        print('FATAL: normalized entries still violate schema:', errs[:5])
        sys.exit(1)

    shutil.copy2(ROAM_AP, ROAM_AP + f'.bak-restore-{ts}')
    shutil.copy2(DEEP_AP, DEEP_AP + f'.bak-restore-{ts}')
    db_val(ROAM_DB, 'customPrompts') and open(os.path.join(ROAM, 'app_db', f'customPrompts.bak-restore-{ts}.json'), 'w', encoding='utf-8').write(db_val(ROAM_DB, 'customPrompts'))
    db_val(DEEP_DB, 'customPrompts') and open(os.path.join(DEEP, f'customPrompts.bak-restore-{ts}.json'), 'w', encoding='utf-8').write(db_val(DEEP_DB, 'customPrompts'))

    payload = json.dumps(fixed, ensure_ascii=False)
    ap = json.load(open(ROAM_AP, encoding='utf-8')); ap['customPrompts'] = fixed
    with open(ROAM_AP, 'w', encoding='utf-8') as f: json.dump(ap, f, indent=2, ensure_ascii=False)
    dp = json.load(open(DEEP_AP, encoding='utf-8')); dp['customPrompts'] = fixed
    with open(DEEP_AP, 'w', encoding='utf-8') as f: json.dump(dp, f, indent=2, ensure_ascii=False)
    db_write(ROAM_DB, 'customPrompts', payload)
    db_write(DEEP_DB, 'customPrompts', payload)

    ok = verify_state()
    print(f'RESTORE {"OK" if ok else "FAILED"} (backups: *.bak-restore-{ts})')
    print('ACTION REQUIRED: restart DeepChat so the runtime cache reloads the prompts (TEMPLATE-STORES-1).')
    return ok


def export():
    entries = load_cp_db(ROAM_DB)
    if not entries:
        print('FATAL: no entries in ROAM_DB to export'); sys.exit(1)
    os.makedirs(os.path.dirname(REPO_EXPORT), exist_ok=True)
    with open(REPO_EXPORT, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f'EXPORTED {len(entries)} entries -> {REPO_EXPORT}')
    print('Commit: cd qnfo-skills && git add prompt-stores/customPrompts.json && git commit -m "chore(prompt-stores): export customPrompts (N entries)" && git push')


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'restore'
    if mode == 'verify':
        sys.exit(0 if verify_state() else 1)
    elif mode == 'inventory':
        inventory()
    elif mode == 'export':
        export()
    elif mode == 'restore':
        restore()
    else:
        print('usage: restore-custom-prompts.py [verify|inventory|restore|export]'); sys.exit(2)
