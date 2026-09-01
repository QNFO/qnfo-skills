"""sync-stub-and-agents-v94.py — finish the v3.94 dual-write:
1. stub DB (.deepchat/agent.db app_settings: raw value column) — systemPrompts + model keys
2. 8th store: Roaming app_db agents.deepchat.config_json.systemPrompt
Prints readbacks; then parent runs prompt-store-verify.py + parity sweep."""
import json, sqlite3

CONTENT = open(r"C:\Users\LENOVO\.deepchat\system-prompt-v2.7.md", encoding="utf-8").read()
print("canonical chars:", len(CONTENT))

# 2. 8th store: agents.deepchat.config_json.systemPrompt (Roaming app_db)
c = sqlite3.connect(r"C:\Users\LENOVO\AppData\Roaming\DeepChat\app_db\agent.db")
row = c.execute("SELECT name, config_json FROM agents WHERE type='deepchat'").fetchall()
print("deepchat agents:", [(r[0], (r[1][:40] if r[1] else None)) for r in row])
target = [r for r in row if r[0] == "deepchat"]
if target:
    cfg = json.loads(target[0][1]) if target[0][1] else {}
    cfg["systemPrompt"] = CONTENT
    c.execute("UPDATE agents SET config_json=? WHERE name='deepchat' AND type='deepchat'", (json.dumps(cfg),))
    c.commit()
    chk = json.loads(c.execute("SELECT config_json FROM agents WHERE name='deepchat' AND type='deepchat'").fetchone()[0])
    print("agents store written; systemPrompt chars:", len(chk.get("systemPrompt", "")))
else:
    print("WARN: no agents.deepchat row found; store not written")
c.close()
print("DONE")
