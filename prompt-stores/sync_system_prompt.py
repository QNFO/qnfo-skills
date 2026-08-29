"""sync_system_prompt.py — v3.93.1 remediation (2026-08-29): 8-store dual-write + shape fix.

AGENT-PROMPT-PARITY-1 (2026-08-29, audit remediation): the deepchat agent row
(agents.deepchat.config_json.systemPrompt) was frozen at v3.74 since 2026-08-25
while the 7 canonical stores moved (v3.74 -> v3.93). This script now ALSO writes
the agents table (8th store). SHAPE FIX: app_db.app_settings.systemPrompts MUST
be the LIST shape ([{id,name,content}]) the app schema expects — the v3.93 cycle
wrote a bare string, which breaks list readers (prompts.find is not a function).
Stub DB column is 'value' (not 'value_json') — handle both.

Reads canonical .deepchat/system-prompt-v2.7.md and writes:
  - Roaming app-settings.json default_system_prompt
  - .deepchat/app-settings.json default_system_prompt
  - Roaming app_db/agent.db app_settings.systemPrompts (LIST shape)
  - .deepchat/agent.db app_settings.systemPrompts (if table exists; value col)
  - Roaming app_db/agent.db agents.deepchat.config_json.systemPrompt (8th store)
Model keys (MODEL-KEY-DB-ROOT-SOURCE-1): DB rows defaultModel/preferredModel -> "deepseek/deepseek-v4-flash"
BEFORE JSON, then JSON dicts {'providerId':'deepseek','modelId':'deepseek-v4-flash'} for both keys.
Readback prints lengths + values for verification.
"""
import json, sqlite3, datetime

CANON = r"C:\Users\LENOVO\.deepchat\system-prompt-v2.7.md"
ROAMING_JSON = r"C:\Users\LENOVO\AppData\Roaming\DeepChat\app-settings.json"
DOTDEEP_JSON = r"C:\Users\LENOVO\.deepchat\app-settings.json"
ROAMING_DB = r"C:\Users\LENOVO\AppData\Roaming\DeepChat\app_db\agent.db"
STUB_DB = r"C:\Users\LENOVO\.deepchat\agent.db"
FLASH = "deepseek/deepseek-v4-flash"
MODEL_DICT = {"providerId": "deepseek", "modelId": "deepseek-v4-flash"}

with open(CANON, "r", encoding="utf-8") as f:
    content = f.read()
print("canonical chars:", len(content))

# 1. JSON files
for p in (ROAMING_JSON, DOTDEEP_JSON):
    d = json.load(open(p, encoding="utf-8"))
    d["default_system_prompt"] = content
    d["defaultModel"] = MODEL_DICT
    d["preferredModel"] = MODEL_DICT
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("json written:", p, "promptlen", len(d["default_system_prompt"]))

# 2. Databases (DB-first per MODEL-KEY-DB-ROOT-SOURCE-1)
for dbp in (ROAMING_DB, STUB_DB):
    c = sqlite3.connect(dbp, timeout=60)
    c.execute("PRAGMA busy_timeout=15000")
    tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    if "app_settings" not in tables:
        print("skip (no app_settings):", dbp)
        c.close()
        continue
    cols = [r[1] for r in c.execute("PRAGMA table_info(app_settings)").fetchall()]
    vc = "value_json" if "value_json" in cols else "value"
    # SHAPE FIX: main DB systemPrompts row = LIST [{id,name,content}]
    if dbp == ROAMING_DB:
        c.execute("UPDATE app_settings SET value_json=? WHERE key=?",
                  (json.dumps([{"id": "default", "name": "DeepChat", "content": content}], ensure_ascii=False), "systemPrompts"))
    else:
        c.execute("UPDATE app_settings SET %s=? WHERE key=?" % vc,
                  (json.dumps(content), "systemPrompts"))
    c.execute("UPDATE app_settings SET %s=? WHERE key=?" % vc, (json.dumps(FLASH), "defaultModel"))
    c.execute("UPDATE app_settings SET %s=? WHERE key=?" % vc, (json.dumps(FLASH), "preferredModel"))
    c.commit()
    c.close()
    print("db written:", dbp)

# 3. AGENTS TABLE — 8th store (AGENT-PROMPT-PARITY-1)
c = sqlite3.connect(ROAMING_DB, timeout=60)
c.execute("PRAGMA busy_timeout=15000")
cfg = json.loads(c.execute("SELECT config_json FROM agents WHERE id='deepchat'").fetchone()[0])
cfg["systemPrompt"] = content
c.execute("UPDATE agents SET config_json=?, updated_at=? WHERE id='deepchat'",
          (json.dumps(cfg, ensure_ascii=False), int(datetime.datetime.now().timestamp()*1000)))
c.commit()
c.close()
print("agents.deepchat.config_json.systemPrompt written")

# 4. Readback
print("=== READBACK ===")
d = json.load(open(ROAMING_JSON, encoding="utf-8"))
print("roaming promptlen:", len(d.get("default_system_prompt", "")))
print("roaming defaultModel:", d.get("defaultModel"), "preferredModel:", d.get("preferredModel"))
l = json.load(open(DOTDEEP_JSON, encoding="utf-8"))
print("legacy promptlen:", len(l.get("default_system_prompt", "")), "preferredModel:", l.get("preferredModel"))
c = sqlite3.connect(ROAMING_DB, timeout=60)
for r in c.execute("SELECT key, length(value_json) FROM app_settings WHERE key IN ('systemPrompts','defaultModel','preferredModel')"):
    print("db row:", r)
v = c.execute("SELECT value_json FROM app_settings WHERE key='systemPrompts'").fetchone()[0]
j = json.loads(v)
print("app_db systemPrompts shape:", type(j).__name__, "| content len:", len(j[0]['content']) if isinstance(j, list) else len(j))
cfg2 = json.loads(c.execute("SELECT config_json FROM agents WHERE id='deepchat'").fetchone()[0])
print("agents row systemPrompt len:", len(cfg2.get('systemPrompt', '')), "header:", cfg2.get('systemPrompt','')[:50].replace(chr(10),' '))
c.close()
