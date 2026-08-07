---
name: deepchat-settings
version: 1.5
description: DeepChat app settings modification (DeepChat 设置/偏好) skill. Covers both UI-level settings (theme, language, font size) AND back-end programmatic modification (custom prompts, system prompt via agent.db + app-settings.json). Activate ONLY for DeepChat settings. Do NOT activate for OS/system settings, editor settings, or other apps.
allowedTools:
  - deepchat_settings_toggle
  - deepchat_settings_set_language
  - deepchat_settings_set_theme
  - deepchat_settings_set_font_size
  - deepchat_settings_open
---

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
| `app-settings.json` | `default_system_prompt` | Raw string (49,419 chars as of v2.8) |

To update the system prompt:
1. Modify `app-settings.json` → `default_system_prompt` (settingsWatcher detects this)
2. Modify `agent.db` → `app_settings` → `systemPrompts` (app reads this at startup)
3. App restart may be required

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


| **SKILL-FILE-NE-INSTALLED-1: Writing a SKILL.md file to the skills dir and assuming it is an installed skill (2026-08-05)** | File presence and valid frontmatter do NOT register a skill with the app loader. `skill_list` is the only truth. Canonical case: execution-mandate v2.6→v2.8 was written to disk and kaizened for 2 days while the app never loaded it — then kaizen v1.24 inferred "removed" and declared `[NOT-INSTALLED]` (SKILL-DEATH-FALSE-POSITIVE-1). When creating/updating a skill: verify via `skill_list` after writing, and if absent, run the app's install flow (not file writes). |


## Examples (do NOT activate this skill)

- "把 Windows 的系统代理改成..."
- "帮我改 VS Code 的字体"
- "把电脑的声音关掉"

## Version

Current: **v1.4** (deepchat-settings — PROMPT-KEY-SCHEMA-ASYMMETRY-1 + v2.7 system prompt sync; 2026-08-06)
