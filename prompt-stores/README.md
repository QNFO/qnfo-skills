# DeepChat Custom Prompt Store — Canonical Copy

Version-controlled canonical export of the DeepChat custom prompt store
(`customPrompts` in `app_settings`, 4 template stores). Owned by the
`deepchat-settings` skill; restored via `deepchat-settings/scripts/restore-custom-prompts.py`.

## Why this file exists (2026-08-17 disaster-recovery lesson)

On 2026-08-17 custom prompts broke ("NOT LOADING", then "STILL CORRUPTED/NOT LOADING" after
restart). Root causes, in order:

1. Store entries were `{name, template, parameters}` — the app's fill tool reads
   `prompt.content` (`getTemplateDefinition` in app.asar) → every fill was EMPTY.
2. The UI route `config.listCustomPrompts` validates `z.array(PromptSchema)` with
   `id: z.string().min(1)` REQUIRED — id-less entries fail the WHOLE list in the UI while
   the MCP tool (no validation) keeps working.
3. Every local backup from 2026-08-11..2026-08-16 was template-only/id-less — **no local
   backup was loadable by the current app**. The one loadable artifact
   (`custom_prompts.json`, 17 commands with the full app model) lived in a legacy file the
   current app does NOT read for the UI (SyncService backup/import only).

Permanent fix: this file is the single canonical, schema-valid, git-tracked copy. Restore
any corruption in one command.

## App PromptSchema (verified in app.asar, 2026-08-17)

```
z.looseObject({
  id: z.string().min(1),            // REQUIRED — UI list validation fails without it
  name: z.string(),
  description: z.string(),
  content: z.string().optional(),   // REQUIRED in practice — fill tool reads prompt.content
  parameters: [{ name: z.string(), description: z.string().optional(),
                 required: z.boolean() }],   // required is MANDATORY
  files: [FileItemSchema], messages: [PromptMessageSchema],
  enabled: z.boolean().optional(),
  source: z.enum(["local", "imported", "builtin"]).optional(),
  createdAt/updatedAt: z.number().int().optional()
})
```

`template` key is tolerated (looseObject) and kept == `content` for the settingsWatcher
JSON shape. The MCP fill tool reads `content`; the UI validates `id`.

## Restore / verify recipe

```
python deepchat-settings/scripts/restore-custom-prompts.py verify     # validate 4 stores
python deepchat-settings/scripts/restore-custom-prompts.py inventory  # scan all sources
python deepchat-settings/scripts/restore-custom-prompts.py restore    # restore (default)
python deepchat-settings/scripts/restore-custom-prompts.py export     # re-export this file
```

Restore source precedence: this file → current ROAM_DB (if schema-valid) → newest
schema-valid local backup → legacy palette. Always restarts DeepChat afterwards
(runtime cache is populated at startup — TEMPLATE-STORES-1).

## Export discipline

Run `restore-custom-prompts.py export` after ANY prompt change (CMD SKILLS UPDATE cycles,
UI edits) and commit this file. If this file is newer than the stores, restore from it.

Current state (2026-08-17): **26 entries** — 9 CMD templates (cmd-continue … cmd-deploy)
+ 17 user commands (cmd-menu … init-session), all schema-valid, byte-identical across the
4 stores (Roaming app-settings.json / .deepchat mirror / app_db agent.db / legacy
.deepchat agent.db). System prompt v3.36 (sha16 b7f060a2eb1e5594) untouched by restores.
