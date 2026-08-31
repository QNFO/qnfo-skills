---
name: config-guard
description: "config-guard - DeepChat config pre-write backup + validation guard"
---

# config-guard - DeepChat config pre-write backup + validation guard

**HARD GATE.** Every config write to %APPDATA%\DeepChat\*.json or app_db/agent.db (app_settings rows)
MUST be wrapped in snapshot -> change -> validate. This prevents the crash class that has hit this
environment repeatedly (prompts.find TypeError 2026-08-31; settings-frame hang 2026-08-20; KIF-30
SKILL.md 53.8MB blowup; sync_system_prompt.py wrong DB shapes).

## Canonical incidents (do not repeat)
| Date | Failure | Root cause |
|---|---|---|
| 2026-08-31 | deepchat:route:invoke: TypeError: prompts.find is not a function | custom_prompts.json became top-level OBJECT (keys "0".."8") via import of sync/backups/backup-1786464852814.zip; app calls .find() on it |
| 2026-08-20 | Settings frame shows "custom prompts failed to load" forever | stale hidden settings frame (heal_settings_frame.py) |
| KIF-30 | qnfo-agent/SKILL.md 36KB -> 53.8MB | path targeting error, no size guard, no pre-write backup |
| v3.93 era | DB systemPrompts/defaultModel written as bare strings | sync_system_prompt.py wrong shapes - prompts.find / model-picker crash on next invoke |

## Shape contract (the app's expectations)
- custom_prompts.json -> top-level LIST of {id, name, description, content, parameters, enabled, source, createdAt, updatedAt}
- system_prompts.json -> {"prompts": [ {id, name, content, ...} ]}
- DB app_settings: customPrompts / systemPrompts -> JSON arrays; defaultModel / preferredModel -> JSON objects {providerId, modelId}
- Prompt files < 2 MB (KIF-30 blowup guard)
- Never import a backup zip whose configs/custom_prompts.json is an object (scan first)

## Protocol (MANDATORY)
1. **Before ANY config change** (kaizen system-prompt update, MCP edit, provider change, restore, import):
   python "%USERPROFILE%\.deepchat\skills\config-guard\scripts\config-guard.py" --snapshot --tag <what>
2. Make the change.
3. **After the change**: python ...\config-guard.py --validate   (FAIL -> --restore and re-validate).
4. **Session start (Phase 0)**: run --check and fix any FAIL before doing anything else.
5. **Before importing/restoring any backup zip**: --scan-zips; quarantine dangerous zips to
   %APPDATA%\DeepChat\sync\quarantine-<date>\.

## Canonical stores (restore order)
1. **Live**: %APPDATA%\DeepChat (app-settings.json, custom_prompts.json, system_prompts.json) + app_db/agent.db app_settings - source of truth for the running app.
2. **Prewrite snapshots**: %USERPROFILE%\.deepchat\backups\prewrite\<ts>\ (config-guard's own).
3. **Agent archive**: %USERPROFILE%\.deepchat\backups\archive-* (timestamped .bak files).
4. **App sync backups**: %APPDATA%\DeepChat\sync\backups\deepchat-settings-backup-* (dated folders; NOTE: pre-08-19 backups contain object-format custom_prompts - do NOT import them raw).
5. **Offsite**: GitHub private QNFO/deepchat (backups/<date>/) + R2 primary-r2:deepchat (bucket deepchat, prefix deepchat-backups) - refresh after every settings milestone.

## Restore procedure (after a crash like 2026-08-31)
1. python config-guard.py --check to see the damage.
2. If custom_prompts.json is an object: convert to list losslessly (entries identical to DB array) - do NOT restore from a pre-08-19 sync backup (they carry the object bug).
3. If DB app_settings shapes are wrong (string instead of list/dict): fix value_json via sqlite (or --restore if a prewrite snapshot predates the damage).
4. Quarantine the source zip (sync/quarantine-<date>/) so it can never re-import.
5. Restart DeepChat (in-memory caches reload from the fixed files).
