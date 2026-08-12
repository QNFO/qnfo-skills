> **v1.12 UPDATE (2026-08-12, kaizen — CMD SKILLS UPDATE: system prompt v3.3 + AI-stack cost-management prompt integration):**
> Red-team: direct parent-agent 5-adversary audit (this session — user directive: all Cloudflare AI services
> discoverable + cost-managed). Prompt stores verified byte-identical pre-edit (v3.2, sha16 cd420a28588a7f1f).
> HARD: 0 (settings-side). SOFT: 1. DESIGN: 1. Changes:
> (1) [SOFT] **System prompt v3.2 → v3.3** — Cloudflare Leverage Mandate extended with the AI-Stack Cost Gate
>     (all AI traffic through AI Gateway, spend limit $10/30d, free-tier-first model selection). Dual-written to
>     all 4 stores (agent.db systemPrompts / app-settings.json default_system_prompt / system-prompt-v2.7.md in
>     .deepchat root + qnfo-skills repo).
> (2) [DESIGN] **CMD DEPLOY template updated** — appended AI-stack cost check (AI calls via AI Gateway,
>     spend-limited). Both stores.
> Cross-reference: cloudflare v3.48, kaizen v2.22, session this.

> **v1.11 UPDATE (2026-08-12, kaizen — CMD SKILLS UPDATE: system prompt v3.2 + CMD DEPLOY Cloudflare-leverage; Cloudflare Docs & Tools Leverage Mandate):**
> Red-team: direct parent-agent 5-adversary audit + UIA Q1-8 (this session — user directive "NOT
> LEVERAGING CLOUDFLARE DOCUMENTATION AND TOOLS ENOUGH (MCP SERVERS AND SKILLS)"). Prompt stores
> verified byte-identical pre-edit (v3.1, sha16 d9f6a397901beb8a). HARD: 0 (settings-side). SOFT: 2.
> DESIGN: 1. Changes:
> (1) [SOFT] **System prompt v3.1 → v3.2 dual-written to ALL 4 stores** — agent.db systemPrompts,
>     app-settings.json default_system_prompt, .deepchat/system-prompt-v2.7.md, qnfo-skills/
>     system-prompt-v2.7.md — byte-identical after write (sha16 recorded in session tape). v3.2 adds
>     the Cloudflare Docs & Tools Leverage Mandate (search_cloudflare_documentation / cloudflare-docs
>     MCP / workers_list / query_worker_observability FIRST; wrangler/REST fallback only).
> (2) [SOFT] **CMD DEPLOY template updated (both stores)** — wrangler-first → MCP/docs-first:
>     "CMD DEPLOY: skill_view cloudflare -> CLOUDFLARE MCP+DOCS FIRST (search_cloudflare_documentation
>     / workers_list / query_worker_observability) -> wrangler deploy -> verify ..." (200 → ~300 chars).
> (3) [DESIGN] **Cloudflare Leverage Mandate referenced from the settings skill** — any prompt-template
>     update that touches Cloudflare operations should carry the MCP/docs-first trigger per
>     Skills-Updates-Must-Include-Prompt-Stores mandate. Cross-ref: cloudflare v3.47, kaizen v2.21.
> Cross-reference: cloudflare v3.47, kaizen v2.21, system-prompt-v2.7.md (content v3.2),
> CMD DEPLOY template, session this.

---
name: deepchat-settings
version: 1.12
description: DeepChat app settings modification (DeepChat 设置/偏好) skill. Covers both UI-level settings (theme, language, font size) AND back-end programmatic modification (custom prompts, system prompt via agent.db + app-settings.json). Activate ONLY for DeepChat settings. Do NOT activate for OS/system settings, editor settings, or other apps.
allowedTools:
  - deepchat_settings_toggle
  - deepchat_settings_set_language
  - deepchat_settings_set_theme
  - deepchat_settings_set_font_size
  - deepchat_settings_open
---

# DeepChat Settings — v1.12
> **v1.10 UPDATE (2026-08-11, kaizen — USER MANDATE: skills updates MUST/SHALL also update system prompt + custom templates):**
> Red-team: direct parent-agent 5-adversary audit (session i3NHS7gJBTyozMCNeaZm- — CMD SKILLS UPDATE with
> the new standing mandate). Watchtower: 19/19 QNFO skills N-2 CLEAN pre/post (kaizen 2.17 + dsp 1.9 bumped
> concurrently). HARD: 1 (mandate). Changes:
> (1) [HARD] **Skills-Updates-Must-Include-Prompt-Stores protocol added** — every kaizen/skills-update cycle
>     MUST/SHALL also update (a) the DeepChat system prompt in ALL THREE stores (`agent.db` → `app_settings`
>     → `systemPrompts` content key, `app-settings.json` → `default_system_prompt`, canonical
>     `system-prompt-v2.7.md` in BOTH .deepchat root and qnfo-skills git repo) and (b) the custom CMD prompt
>     templates (`agent.db` customPrompts content key + `app-settings.json` customPrompts template key).
>     System prompt bumped v3.0 → v3.1 (56,137 chars, "Last updated 2026-08-11"); CMD SKILLS UPDATE template
>     now carries the mandate text (317 → 426 chars) in both stores.
> (2) [SOFT] **Footer description normalized** — the v1.9 concurrent bump reused the v1.8 footer description
>     ("stdio registration note + mcp-guard row"); footer now describes this v1.10 change.
> Cross-reference: kaizen v2.17, system-prompt-v2.7.md (content v3.1), MCP-REGISTRATION-ONE-STORE-1,
> session i3NHS7gJBTyozMCNeaZm-.

> **v1.8 UPDATE (2026-08-11, kaizen — red-team fix cycle: stdio registration note + mcp-guard row; CMD EXECUTE):**
> Red-team: direct parent-agent 5-adversary audit (session i3NHS7gJBTyozMCNeaZm- — post-restart audit of
> v1.7 + qwav-platform registration). HARD: 0. SOFT: 3. DESIGN: 2. This cycle applies the writable fixes:
> (1) [SOFT] **stdio-type server note added** to MCP Server Registration — the v1.7 section documented
>     HTTP-type (baseUrl) only; stdio servers (npx-based: LinkedIn, buffer, cloudflare, cua-driver) use
>     `command`/`args` in mcp-settings.json and get serverId/bindingHash in agent.db at startup persistence.
> (2) [DESIGN] **mcp-guard.json row added** to File Locations — config dir carries mcp-guard.json (a
>     file-hygiene/mojibake guard: version/enabled/rules/known_mojibake_signatures/target_files), NOT an
>     MCP allowlist; no registration entry needed. Row added to complete the map (UIA Q2 residual).
> (3) [SOFT] v1.7 banner cross-ref "kaizen v2.10" is now stale (kaizen v2.11/v2.12 concurrent bumps) —
>     banner-history text, EXEMPT per N-2-SCAN-FALSE-POSITIVE-1; left as written.
> Cross-reference: kaizen v2.12, MCP-REGISTRATION-ONE-STORE-1, MCPMARKET-CATALOG-NE-SERVER-1,
> session i3NHS7gJBTyozMCNeaZm-.

> **v1.7 UPDATE (2026-08-11, kaizen — MCP server registration mechanics documented; CMD SKILLS UPDATE):**
> Red-team: direct parent-agent 5-adversary audit + UIA Q1-8 (session i3NHS7gJBTyozMCNeaZm- — qwav-platform
> MCP registration cycle). Watchtower: 19/19 QNFO skills N-2 CLEAN pre-edit. HARD: 0. SOFT: 2. DESIGN: 1.
> (1) [SOFT] **MCP Server Registration section added** — dual-store pattern: `mcp-settings.json` → `mcpServers`
>     (settingsWatcher live reload) + `agent.db` → `mcp_servers` (config_json with serverId/bindingHash;
>     startup persistence) + `mcp_settings` (mcpEnabled/removedBuiltInServers) + `agent_mcp_selections`.
>     bindingHash semantics: identical baseUrl → identical bindingHash → ALIAS entry (no new tool surface;
>     tools keyed by name via input_enabledMcpTools). Backup-before-edit + rollback documented.
> (2) [SOFT] **Anti-pattern rows added** — MCP-REGISTRATION-ONE-STORE-1 (single-store registration silently
>     lost at restart or invisible to live reload; MUST dual-write) + MCPMARKET-CATALOG-NE-SERVER-1
>     (marketplace catalog listing ≠ runnable MCP server; verify endpoint with MCP initialize POST —
>     GET /mcp 404 is normal for streamable-HTTP — before registering).
> (3) [DESIGN] **File Locations table completed** — added `mcp-settings.json` row (the map omitted the
>     territory per UIA Q2).
> Cross-reference: kaizen v2.10, MCP-REGISTRATION-ONE-STORE-1, MCPMARKET-CATALOG-NE-SERVER-1,
> qwav-platform registration (session i3NHS7gJBTyozMCNeaZm-), session this.

> **v1.6 UPDATE (2026-08-10, kaizen — system prompt v2.9 sync + BLAME-EXTERNAL-1 live; CMD RED TEAM follow-up):**
> Red-team: direct parent-agent 5-adversary audit (session JyHYI9Q9pS2zs7fL_mJbS). Finding: the v2.9 update had reached ONLY the canonical .md file — both runtime stores still held v2.8 (49,419 chars, no BLAME-EXTERNAL-1). The running system prompt was therefore still v2.8; the principle was inert. HARD: 2. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **System prompt v2.9 dual-written to runtime stores** — `app-settings.json` → `default_system_prompt` AND `agent.db` → `app_settings` → `systemPrompts` (backups: `.bak_20260810_174603`). All 3 stores now IDENTICAL: 50,518 chars, v2.9 header, BLAME-EXTERNAL-1 present. settingsWatcher picks up app-settings.json dynamically; agent.db loads at startup.
> (2) [HARD] **Wrong-path misdiagnosis corrected** — earlier "agent.db locked by running app" was FALSE: the probe used `C:\Users\LENOVO\.deepchat\agent.db` (wrong path); the real path `%APPDATA%\DeepChat\app_db\agent.db` opens read-only AND writable with zero lock issues. Same fault class as BLAME-EXTERNAL-1 (blamed environment, fault was my own reference).
> (3) [SOFT] **Reference updated** — "49,419 chars as of v2.8" -> v2.9 (50,518 chars, "Last updated 2026-08-10"). 9 CMD templates re-verified present in BOTH stores (content key in agent.db, template key in app-settings.json).
> (4) [DESIGN] **Stale memory corrected** — the "system prompt must be applied manually via Settings UI" memory was WRONG (programmatic dual-write is the documented, executed path) and has been archived.
> Cross-reference: kaizen v1.99, system-prompt-v2.7.md (content v2.9), BLAME-EXTERNAL-1, session this.


# DeepChat Settings — v1.5

> **v1.5 UPDATE (2026-08-07, kaizen — CMD template architecture + system prompt v2.8 sync):**
> Red-team: direct parent-agent audit (session 5gsgy_E4umEpfGejRgDD4 — CMD CONTINUE).
> HARD: 0. SOFT: 2. DESIGN: 0. Changes:
> (1) [SOFT] **Canonical template architecture updated** — the prompt inventory is now NINE
>     CMD-prefixed templates (CMD CONTINUE, CMD EXECUTE, CMD RED TEAM, CMD RED TEAM SUB,
>     CMD RESEARCH, CMD SKILLS UPDATE, CMD PUBLISH, CMD DEPLOY, CMD CLOSEOUT), replacing the
>     former two-template set (SKILLS UPDATE + CONTINUE). All share the `CMD ` prefix so they
>     group together in the / slash-command dropdown. Sync example updated accordingly.
> (2) [SOFT] **System prompt v2.8 reference updated** — "48,598 chars as of v2.7" -> v2.8
>     (49,419 chars, "Last updated 2026-08-07"). v2.8 adds the auto-search mandate (Phase 0
>     now includes search_conversations / search_messages / tape_search / memory_recall) and
>     fixes the LANGUAGE CONTRADICTION. All 3 stores verified IDENTICAL.
> Cross-reference: kaizen v1.86, system-prompt-v2.7.md (content v2.8), CMD-LEGACY-1,
> session 5gsgy_E4umEpfGejRgDD4.

> **v1.4 UPDATE (2026-08-06, kaizen — PROMPT-KEY-SCHEMA-ASYMMETRY-1 + v2.7 system prompt sync):**
> Red-team: direct parent-agent audit (session gpgLR3KXSZxQQkEG_G2HW SKILLS UPDATE).
> HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **PROMPT-KEY-SCHEMA-ASYMMETRY-1 anti-pattern added** — agent.db customPrompts use `content`
>     key; app-settings.json customPrompts use `template` key. Always read BOTH keys when verifying prompt
>     content. A single-key read produces a false "empty prompt" flag.
> (2) [SOFT] **System prompt v2.7 reference updated** — "44156 chars as of v2.6" -> v2.7 (48,598 chars,
>     "Last updated 2026-08-05"). v2.7 is current in all 3 stores (agent.db systemPrompts /
>     app-settings.json default_system_prompt / system-prompt-v2.7.md), verified IDENTICAL.
> Cross-reference: kaizen v1.61, PROMPT-REDISCOVERY-1, system-prompt-v2.7.md,
> session gpgLR3KXSZxQQkEG_G2HW.


# DeepChat Settings Modification Skill

Use this skill to safely change DeepChat *application* settings during a conversation.

## Core rules

- Only change settings when the user is asking to change **DeepChat** settings.
- Use the dedicated settings tools; never attempt arbitrary key/value writes.
- These tools are intended to be available only when this skill is active.
- Viewing the main `deepchat-settings` `SKILL.md` activates this skill for the current conversation and exposes the `deepchat_settings_*` tools in the next tool loop iteration.
- Viewing linked files under this skill does **not** activate the skill.
- If the request is ambiguous, ask a clarifying question before applying.
- **Custom prompts and system prompt** CAN be modified programmatically via the back-end storage (see §Backend Storage Layout). Use the documented SQLite + JSON patterns — no Settings UI required.

## Supported settings (initial allowlist)

Toggles:

- `soundEnabled`: enable/disable sound effects.
- `copyWithCotEnabled`: enable/disable copying COT details.
- `loggingEnabled`: enable/disable execution logging and trace (main log + per-session bgexec logs). May require app restart.

Enums:

- `language`: DeepChat locale, including `system`, `zh-CN`, `en-US`, `zh-TW`, `zh-HK`, `ko-KR`, `ru-RU`, `ja-JP`, `fr-FR`, `fa-IR`, `pt-BR`, `da-DK`, `he-IL`.
- `theme`: `dark | light | system`.
- `fontSizeLevel`: integer level within supported range.

Settings navigation (open-only):

- Use `deepchat_settings_open` only when the request cannot be fulfilled by the settings tools, and avoid calling it if the change is already applied.
- `section` hints: `common`, `display`, `provider`, `mcp`, `prompt`, `acp`, `skills`, `knowledge-base`, `database`, `shortcut`, `about`.

## Workflow

1. Confirm the user is requesting a DeepChat settings change.
2. If the settings tools are not yet present, inspect the main `deepchat-settings` skill document first so the skill becomes active for this conversation.
3. Determine the target setting and the intended value.
4. If the setting is supported, call the matching tool:
   - toggles: `deepchat_settings_toggle`
   - language: `deepchat_settings_set_language`
   - theme: `deepchat_settings_set_theme`
   - font size: `deepchat_settings_set_font_size`
5. Confirm back to the user what changed (include the final value).
6. If the setting is unsupported, call `deepchat_settings_open` (with `section`) and provide a short pointer to the correct Settings section. Do not call it if the requested change has already been applied.

## Backend Storage Layout (PROGRAMMATIC MODIFICATION)

DeepChat stores configuration in TWO locations. Understanding both prevents
the ~15 tool-call rediscovery this session burned (PROMPT-REDISCOVERY-1).

### File Locations

| What | Path | Format |
|:-----|:-----|:-------|
| **Agent database** | `%APPDATA%\DeepChat\app_db\agent.db` | SQLite3, `app_settings` table |
| **App settings** | `%APPDATA%\DeepChat\app-settings.json` | JSON, top-level keys |
| **MCP servers** | `%APPDATA%\DeepChat\mcp-settings.json` | JSON, `mcpServers` map |
| **MCP guard** | `%APPDATA%\DeepChat\mcp-guard.json` | JSON, file-hygiene/mojibake guard (not an MCP allowlist) |
| **Provider registry** | `%APPDATA%\DeepChat\app_db\agent.db` → `providers`, `provider_models`, `model_status`, `model_configs` + `app-settings.json` → `preferredModel`/`defaultModel` | Custom provider config (api_key, base_url, enabled models, default model) — dual-write per §Provider Registration |
| **History DB** | `%APPDATA%\DeepChat\rtk\history.db` | SQLite3 (10824 commands) |
| **Skills** | `%USERPROFILE%\.deepchat\skills\` | Markdown files (no .git) |
| **Git-tracked skills** | `%USERPROFILE%\Documents\GitHub\qnfo-skills\` | Git repo (canonical) |

### agent.db Structure

The `app_settings` table uses a **key-value_json** pattern:

```sql
SELECT key, value_json FROM app_settings;
-- customPrompts       -> '[{"id":"...","name":"SKILLS UPDATE","content":"...","parameters":[...]}, ...]'
-- systemPrompts       -> '[{"id":"default","name":"DeepChat","content":"..."}]'
-- loggingEnabled      -> 'true'
-- skills.managementState -> '{...}'
```

**CRITICAL**: `value_json` is stored as a JSON STRING, not parsed. Use `json.loads()`/`json.dumps()`.

### Custom Prompt Templates (Programmatic)

```python
import sqlite3, json

adb = r'C:\Users\LENOVO\AppData\Roaming\DeepChat\app_db\agent.db'
conn = sqlite3.connect(adb, timeout=10)
cur = conn.cursor()

# READ
cur.execute("SELECT value_json FROM app_settings WHERE key = 'customPrompts'")
prompts = json.loads(cur.fetchone()[0])

# MODIFY
for p in prompts:
    if p['name'] == 'OLD_NAME':
        p['name'] = 'NEW_NAME'
        p['content'] = 'NEW_TEMPLATE_TEXT'

# WRITE
cur.execute("UPDATE app_settings SET value_json = ?, updated_at = ? WHERE key = 'customPrompts'",
            (json.dumps(prompts, ensure_ascii=False), int(datetime.now().timestamp() * 1000)))
conn.commit()
conn.close()
```

**Schema**: Each prompt object has `id`, `name`, `description`, `content`, `parameters`.

**SettingsWatcher**: DeepChat's `settingsWatcher.ts` watches `app-settings.json` and
dynamically reloads `shell`, `modelConfig`, and `customPrompts` without restart.
However, template **names** are cached at startup — adding/renaming a template
requires an app restart for the name to appear in the UI. Content changes are
picked up dynamically if synced to `app-settings.json`.

### Syncing Prompts to app-settings.json

For settingsWatcher to detect changes, ALSO write to `app-settings.json`:

```python
import json
ap = r'C:\Users\LENOVO\AppData\Roaming\DeepChat\app-settings.json'
with open(ap, encoding='utf-8') as f:
    d = json.load(f)
d['customPrompts'] = [
    {"name": "CMD CONTINUE",      "template": "CMD CONTINUE: update_plan -> execute -> verify -> iterate. Complete autonomously. `update_plan` `exec`", "parameters": []},
    {"name": "CMD EXECUTE",       "template": "CMD EXECUTE: PLAN/EXECUTE/RED-TEAM/VERIFY/ITERATE with WBS codes...", "parameters": []},
    {"name": "CMD RED TEAM",      "template": "CMD RED TEAM: 5-adversary direct audit... READ-ONLY", "parameters": []},
    {"name": "CMD RED TEAM SUB",  "template": "CMD RED TEAM SUB: subagent_orchestrator(run, parallel)...", "parameters": []},
    {"name": "CMD RESEARCH",      "template": "CMD RESEARCH: skill_view research -> Phase 1 (Due Diligence)...", "parameters": []},
    {"name": "CMD SKILLS UPDATE", "template": "CMD SKILLS UPDATE: EXECUTE RED TEAM SKILLS AUDIT...", "parameters": []},
    {"name": "CMD PUBLISH",       "template": "CMD PUBLISH: skill_view research -> Phase 5 pipeline...", "parameters": []},
    {"name": "CMD DEPLOY",        "template": "CMD DEPLOY: skill_view cloudflare -> wrangler deploy...", "parameters": []},
    {"name": "CMD CLOSEOUT",      "template": "CMD CLOSEOUT: verify git clean -> audit deferred tasks...", "parameters": []},
]
# Canonical 9-template CMD architecture (2026-08-07): ALL templates share the CMD prefix so they
# group alphabetically in the / slash-command dropdown. Full content synced live to both stores.
with open(ap, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
```

**Always update BOTH** agent.db and app-settings.json for prompt changes.

### System Prompt (Programmatic)

The system prompt is stored in TWO locations that MUST stay in sync:

| Location | Key | Notes |
|:---------|:----|:------|
| `agent.db` → `app_settings` | `systemPrompts` | JSON array, `[{"id":"default","name":"DeepChat","content":"..."}]` |
| `app-settings.json` | `default_system_prompt` | Raw string (v3.3 as of 2026-08-12, Cloudflare Leverage Mandate + AI-Stack Cost Gate present; 4 stores byte-identical) |

To update the system prompt:
1. Modify `app-settings.json` → `default_system_prompt` (settingsWatcher detects this)
2. Modify `agent.db` → `app_settings` → `systemPrompts` (app reads this at startup)
3. App restart may be required

### MCP Server Registration (Programmatic — added 2026-08-11)

MCP servers are stored in TWO locations that MUST be dual-written (canonical case:
qwav-platform registration, session i3NHS7gJBTyozMCNeaZm- — ~15 tool calls were
burned rediscovering this before it was documented):

| Location | Key / Table | Role |
|:---------|:------------|:-----|
| `%APPDATA%\DeepChat\mcp-settings.json` | `mcpServers` (map keyed by server name) | Live MCP list; settingsWatcher watches this file |
| `%APPDATA%\DeepChat\app_db\agent.db` | `mcp_servers` (name, config_json, sort_order, created_at, updated_at) | Startup persistence — survives restarts |
| `agent.db` | `mcp_settings` (key/value_json) | `mcpEnabled`, `autoDetectNpmRegistry`, `removedBuiltInServers`, `npmRegistryCache` |
| `agent.db` | `agent_mcp_selections` (agent_id, is_builtin, mcp_id, sort_order) | Per-agent server selection |

**Entry shape (http type):** `type=http`, `baseUrl`, `enabled=true`, `command=""`,
`args=[]`, `env={}`, `customHeaders={}`, `customNpmRegistry=""`. DB config_json adds
`serverId` (uuid), `configGeneration`, `bindingHash`.
**stdio-type servers (npx-based):** servers like LinkedIn, buffer, cloudflare, cua-driver use
`command` + `args` instead of `baseUrl` (e.g. `command: "npx"`, `args: ["-y", "package@latest"]`).
They are configured in `mcp-settings.json` `mcpServers`; agent.db `mcp_servers` stores their
config_json (serverId/bindingHash) when the app binds them. Same discipline applies: backup the
JSON, verify with a real handshake, roll back by removing from both stores.


**bindingHash semantics (CRITICAL):** the binding hash is derived from the connection
parameters (baseUrl/command/type). Two entries with the SAME baseUrl get the SAME
bindingHash — the second is an **ALIAS of the first binding**, not a new server. It
adds naming fidelity but ZERO new tool surface: DeepChat keys tool enablement by
NAME via `input_enabledMcpTools` in app-settings.json, so both names resolve to the
same tools. Document aliases as aliases in the description.

**Registration procedure:**
1. BACKUP: copy `mcp-settings.json` → `mcp-settings.json.bak-YYYYMMDD-suffix`.
2. `mcp-settings.json`: add the entry under `mcpServers` (settingsWatcher reloads live).
3. `agent.db`: `INSERT INTO mcp_servers (name, config_json, sort_order, ...)` with
   sort_order = `MAX(sort_order)+1` (verify no collision).
4. VERIFY: re-read both stores + confirm the endpoint is live with an MCP
   `initialize` POST (NOT a bare GET — GET /mcp → 404 is normal for streamable-HTTP).

**Rollback:** remove the key from `mcpServers` + `DELETE FROM mcp_servers WHERE name='...'`.

**Marketplace listings (mcpmarket.com etc.) are CATALOG CARDS — not servers.** They
rarely contain an endpoint/install command; the linked repo may have NO MCP server
component. Verify a real endpoint (MCP initialize POST; bare-Python UA may get CF
403/1010 — use browser-grade headers) before registering. See MCPMARKET-CATALOG-NE-SERVER-1.

### Provider Registration (Programmatic — added 2026-08-11)

Custom providers (like the qnfo-ai "Cloudflare AI Router") are stored in agent.db tables
AND mirrored in app-settings.json. This session (qnfo-ai ensemble setup) discovered the
full schema — previously undocumented. THE KEY ROW MUST MATCH THE UPSTREAM SECRET:
a stale `api_key` in `providers` silently 401s every chat request (PROVIDER-KEY-SYNC-1).

**agent.db tables:**

| Table | Key columns | Purpose |
|:------|:------------|:--------|
| `providers` | id, name, api_type, api_key, base_url, enabled, custom, sort_order, provider_json | The provider registry. `custom=1` = user-added. `provider_json.apiKey` MUST match `api_key` |
| `provider_models` | provider_id, model_id, source, name, group_name, sort_order, model_json | Model catalog per provider (source=`provider` or `user`) |
| `model_status` | status_key, provider_id, model_id, enabled, updated_at | Which models are ENABLED (the model picker gate) |
| `model_configs` | cache_key, provider_id, model_id, source, config_json | Per-model user config (maxTokens, contextLength, temperature, apiEndpoint) |
| `app_settings` | key=`preferredModel` / `defaultModel`, value_json | The active default model (dual-write with app-settings.json) |

**provider_json shape (custom OpenAI-compatible):**
`{"id":"<provider-id>","name":"...","apiType":"openai","apiKey":"<KEY>","baseUrl":"https://.../v1","enable":true,"custom":true}`

**Registration procedure (programmatic, zero UI):**
1. BACKUP both stores: copy `app-settings.json` and `agent.db`.
2. INSERT into `providers` (id, name, api_type='openai', api_key, base_url, enabled=1, custom=1,
   sort_order=MAX+1, provider_json) — or UPDATE existing row if the provider already exists.
3. INSERT provider_models rows for each discoverable model (from GET {base}/models).
4. INSERT model_status rows (enabled=1) for the models you want selectable.
5. INSERT model_configs rows for user-tuned models.
6. Set `preferredModel` + `defaultModel` in BOTH app-settings.json AND agent.db app_settings.
7. VERIFY: re-read the provider row (api_key matches upstream), GET {base}/models returns
   200, and a live chat completion with the stored key returns 200.
8. NOTE: agent.db provider config is loaded at app STARTUP — a restart is needed for the
   running instance to pick up key changes (app-settings.json modelConfig applies live).

**Canonical case (2026-08-11):** Cloudflare AI Router provider (id `-_X6Z7YffrNPktrj3Vhjo`)
was fully registered (16 models, enabled) but held the PRE-ROTATION api_key — the Worker's
`ROUTER_AUTH_KEY` secret had been rotated, so every chat request returned 401. Fix: updated
`providers.api_key` + `provider_json.apiKey` to the rotated key, cleaned stale key from
agent_memory, set defaultModel to ensemble, verified 6/6 E2E.

### TEMP-VOLATILITY (Critical Peril)

**Windows `%TEMP%` is volatile across agent tool calls.** A file written by the
`write` tool to `C:\Users\LENOVO\AppData\Local\Temp\` may NOT exist when the
`exec` tool tries to read it. This is TEMP-VOLATILITY-3 (kaizen v1.31).

**Fix**: Write executable scripts to a non-temp stable path:
- `C:\Users\LENOVO\.deepchat\_script.py` (preferred — survives turns)
- NEVER write to `C:\Program Files\DeepChat\` (SKILL-WRITE-EPERM: EPERM)
- Always use `encoding='utf-8'` with `open()`

Pattern: `write` tool → stable path → `exec python <stable-path>` → verify → `del <stable-path>`.

### SettingsWatcher Behavior

| Change | Auto-detected? | Restart needed? |
|:-------|:--------------|:----------------|
| `app-settings.json` → `customPrompts` | ✅ Yes (dynamic reload) | No (for content), **Yes** for template names |
| `agent.db` → `customPrompts` | ❌ Not watched | **Yes** — agent.db is loaded at startup |
| `app-settings.json` → `default_system_prompt` | ✅ Yes | Maybe (test after change) |
| `app-settings.json` → `shell` | ✅ Yes | No |
| `app-settings.json` → `modelConfig` | ✅ Yes | No |

**Rule**: Update BOTH locations. The `app-settings.json` write triggers
settingsWatcher's dynamic reload; the `agent.db` write ensures the change
persists across restarts.

## Skill Registry Truth-Source (added 2026-08-05)

**Forensic finding (session IZbk2G9P2aA0JH0f0yQjj):** `execution-mandate` v2.8 was
on disk, valid frontmatter, `.kaizen_history` updated 2026-08-04 — yet the app
NEVER loaded it, and kaizen v1.24 declared it `[NOT-INSTALLED]`. That was a false
"removal" — a file written directly to the skills dir was never registered with
the app's loader. Three sources of truth disagreed; sessions trusted different ones.

### The Three Sources of Truth (ranked)

| # | Source | What It Is | Trust? |
|:-:|:-------|:-----------|:-------|
| 1 | **`skill_list` tool** | The app's LIVE loader — the ONLY authority on "is this skill active" | ✅ **PRIMARY** |
| 2 | **On-disk dir** (`%USERPROFILE%\.deepchat\skills\<name>\SKILL.md`) | File presence ≠ installed. Valid frontmatter ≠ loaded | ⚠️ Secondary |
| 3 | **`skills.managementState`** (`agent.db` → `app_settings`) | 84-entry bookkeeping with 58 GHOST entries adopted 2026-07-10 from `.claude`/`.agents` whose files never existed | ❌ Do NOT trust |

### The Rules (permanent — prevents skill churn)

1. **`skill_list` is the ONLY truth.** A skill that is not in `skill_list` is
   not loaded — regardless of on-disk presence, frontmatter validity, or
   `.kaizen_history` activity.
2. **A file on disk is NOT an installed skill.** Writing `SKILL.md` to the
   skills dir (via `skill_manage` draft, `write` tool, or file copy) does NOT
   register it with the app's loader. Proper install = the app's install flow
   (Settings → Skills, or the app's skill-install API).
3. **Before declaring a skill "removed"/"dead":** (a) check `skill_list` FIRST;
   (b) check `.kaizen_history` — a fresh entry means it was ACTIVELY maintained,
   not removed; (c) distinguish "never loaded" from "was loaded then removed."
4. **`AGENT-DB-STALE-1` memory is WRONG** — the skill registry is NOT in
   `agent_settings.acp.skills` (that table has 2 rows). Trust `skill_list`.
5. **When a skill is missing from `skill_list` but present on disk and actively
   maintained:** flag it as "on-disk but not loaded by the app" — do NOT infer
   removal. Reconcile via the app's skill management, not by rewriting skill files.

## Examples (activate this skill)

- "把主题改成深色"
- "Turn off sound effects"
- "语言改成英文"
- "复制时不要带 COT"
- "Enable logging for debugging"
- "Turn on execution trace"
- "Open the MCP settings page"
- "Edit my prompts"

## Anti-Patterns

| Anti-Pattern | Correct |
|:-------------|:--------|

| **PROMPT-KEY-SCHEMA-ASYMMETRY-1: Reading customPrompts with the wrong key (2026-08-06)** | agent.db `customPrompts` entries: `{"name":..., "content":"..."}`. app-settings.json `customPrompts` entries: `{"name":..., "template":"..."}`. The prompt TEXT lives under DIFFERENT keys in the two stores. Always read `content` (agent.db) AND `template` (app-settings.json); both must be non-empty. Canonical case: session gpgLR3KXSZxQQkEG_G2HW — a `content`-key read of app-settings.json falsely reported empty templates. |
| **PROMPT-REDISCOVERY-1: Searching for prompt storage locations with 15+ tool calls when the answer is documented here (2026-08-05)** | Custom prompts live in `agent.db` → `app_settings` → `key='customPrompts'` (value_json JSON string). The system prompt is in `agent.db` → `key='systemPrompts'` AND `app-settings.json` → `default_system_prompt`. Read this skill first — do not grep JSON files or walk directory trees. |
| **DB-SCHEMA-GUESS-1: Guessing database table names instead of querying sqlite_master (2026-08-05)** | Before querying any DeepChat database, run `SELECT name FROM sqlite_master WHERE type='table'` to discover the actual schema. The `app_settings` table uses key-value_json, not typed columns. The `history.db` uses `commands` and `parse_failures` tables, not `prompts`. |
| **MCP-REGISTRATION-ONE-STORE-1: Registering an MCP server in only ONE of the two stores (2026-08-11)** | Dual-write BOTH: `mcp-settings.json` → `mcpServers` (settingsWatcher live reload) AND `agent.db` → `mcp_servers` (startup persistence). A one-store registration silently vanishes at restart (agent.db missed) or never appears in the live list (mcp-settings.json missed). Canonical case: qwav-platform registration 2026-08-11 — verified both stores needed (28-entry mcp-settings.json + 18-row mcp_servers). Cross-ref: MCP Server Registration section. |
| **PROVIDER-KEY-SYNC-1: Provider api_key in agent.db goes stale when the upstream Worker secret is rotated (2026-08-11)** | **HARD.** After ANY rotation of a Worker secret that backs a custom provider (e.g. qnfo-ai `ROUTER_AUTH_KEY`), update `providers.api_key` + `provider_json.apiKey` in agent.db in the SAME session — otherwise every chat request 401s silently. Also clean the stale key from `agent_memory` (it leaks secrets in recall). Canonical case: 2026-08-11 Cloudflare AI Router — pre-rotation key `w18b7smc...` persisted in providers row after ROUTER_AUTH_KEY rotation; all requests 401'd until fixed; backups app-settings.json.bak-20260811_180232 / agent.db.bak-20260811_180232. Cross-ref: deepchat-settings §Provider Registration, kaizen mirror, TOKEN-VERIFY-SCOPE-1 (same class: scope mismatch on verify). |
| **MCPMARKET-CATALOG-NE-SERVER-1: Treating an MCP marketplace listing (mcpmarket.com) as a runnable MCP server (2026-08-11)** | Marketplace listings are CATALOG CARDS: no endpoint, no install command, no tool list; the linked repo may contain NO MCP server component. Before registering in DeepChat, verify a REAL endpoint with an MCP `initialize` POST (bare GET /mcp → 404 is normal for streamable-HTTP; bare-Python UA may get CF 403/1010 — use browser-grade headers). Canonical case: qwav-platform — listing pointed at QNFO/qwav-platform repo (624 files, 0 with 'mcp' in name); the live endpoint was the pre-existing qnfo-memory-mcp worker. Cross-ref: MCP Server Registration section. |


| **SKILL-FILE-NE-INSTALLED-1: Writing a SKILL.md file to the skills dir and assuming it is an installed skill (2026-08-05)** | File presence and valid frontmatter do NOT register a skill with the app loader. `skill_list` is the only truth. Canonical case: execution-mandate v2.6→v2.8 was written to disk and kaizened for 2 days while the app never loaded it — then kaizen v1.24 inferred "removed" and declared `[NOT-INSTALLED]` (SKILL-DEATH-FALSE-POSITIVE-1). When creating/updating a skill: verify via `skill_list` after writing, and if absent, run the app's install flow (not file writes). |


## Examples (do NOT activate this skill)

- "把 Windows 的系统代理改成..."
- "帮我改 VS Code 的字体"
- "把电脑的声音关掉"

## Version

Current: **v1.12** (deepchat-settings — CMD SKILLS UPDATE: system prompt v3.3 + AI-stack cost-management integration; 2026-08-12)
