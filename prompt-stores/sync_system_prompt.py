"""sync_system_prompt.py — v3.93 cycle: 7-store system-prompt dual-write + model-key DB-root fix.

Reads canonical .deepchat/system-prompt-v2.7.md and writes:
  - Roaming app-settings.json default_system_prompt
  - .deepchat/app-settings.json default_system_prompt
  - Roaming app_db/agent.db app_settings.systemPrompts (value_json = JSON string)
  - .deepchat/agent.db app_settings.systemPrompts (if table exists)
Model keys (MODEL-KEY-DB-ROOT-SOURCE-1): DB rows defaultModel/preferredModel -> "deepseek/deepseek-v4-flash"
BEFORE JSON, then JSON dicts {'providerId':'deepseek','modelId':'deepseek-v4-flash'} for both keys.
Readback prints lengths + values for verification.
"""
import json, sqlite3, os

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
    c = sqlite3.connect(dbp)
    tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    if "app_settings" not in tables:
        print("skip (no app_settings):", dbp)
        c.close()
        continue
    c.execute("UPDATE app_settings SET value_json=? WHERE key=?", (json.dumps(content), "systemPrompts"))
    c.execute("UPDATE app_settings SET value_json=? WHERE key=?", (json.dumps(FLASH), "defaultModel"))
    c.execute("UPDATE app_settings SET value_json=? WHERE key=?", (json.dumps(FLASH), "preferredModel"))
    c.commit()
    c.close()
    print("db written:", dbp)

# 3. Readback
print("=== READBACK ===")
d = json.load(open(ROAMING_JSON, encoding="utf-8"))
print("roaming promptlen:", len(d.get("default_system_prompt", "")))
print("roaming defaultModel:", d.get("defaultModel"), "preferredModel:", d.get("preferredModel"))
l = json.load(open(DOTDEEP_JSON, encoding="utf-8"))
print("legacy promptlen:", len(l.get("default_system_prompt", "")), "preferredModel:", l.get("preferredModel"))
c = sqlite3.connect(ROAMING_DB)
for r in c.execute("SELECT key, length(value_json) FROM app_settings WHERE key IN ('systemPrompts','defaultModel','preferredModel')"):
    print("db row:", r)
c.close()
