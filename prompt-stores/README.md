# DeepChat Custom Prompt Store — Canonical Copy

Version-controlled canonical export of the DeepChat custom prompt store
(`customPrompts` in `app_settings`, 4 template stores). Owned by the
`deepchat-settings` skill; tools live HERE (repo canonical):
`prompt-stores/restore_custom_prompts.py` + `prompt-stores/prompt-store-verify.py`
(local working copies in `.deepchat/scripts/`).

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

## Why it broke AGAIN on 2026-08-20 (string-timestamp lesson)

On 2026-08-20 the UI prompt list died again — this time with the ON-DISK stores passing
all previously-known checks. New root cause: a cycle wrote `updatedAt` as a JSON **string**
(`'1787166894113'`) on 2 entries. `updatedAt: z.number().int().optional()` — two mistyped
fields fail the zod validation of the **whole** `config.listCustomPrompts` array → UI shows
nothing while the unvalidated MCP path keeps listing names. Signature: agent tools work,
UI list empty.

Secondary finding: the live stores had **diverged from this repo canonical** on 3 entries
(live cmd-publish silently dropped the v3.42 prose-gate tail; repo cmd-research/
cmd-skills-update were stale prefixes). Writes must source ONLY from this file, never from
memory; merges take the complete side per entry (prefix analysis).

Fixed: merged canonical + int coercion across all 6 sources (repo, script canonical,
4 live stores), byte-identical + schema-valid. Safeguards:
- `prompt-store-verify.py` — read-only exact-schema + 6-source parity check (exit 0/1/2);
  run after EVERY write, at every CMD SKILLS UPDATE closeout, and daily via Daily Ops
  cronjob (216e1d12) check #6 (report-only, notify-on-failure).
- `restore_custom_prompts.py` v2 — schema-GATED restore: candidates that fail the exact
  schema are REFUSED; timestamps coerced to int; source precedence repo → backup file →
  live Roaming JSON → Roaming DB.

## App PromptSchema (verified in app.asar, 2026-08-20)

```
z.looseObject({
  id: z.string().min(1),            // REQUIRED — UI list validation fails without it
  name: z.string(),                 // REQUIRED
  description: z.string(),          // REQUIRED
  content: z.string().optional(),   // REQUIRED in practice — fill tool reads prompt.content
  parameters: [{ name: z.string(), description: z.string().optional(),
                 required: z.boolean() }],   // name AND required are MANDATORY
  files: [z.looseObject({ id: z.string().min(1), name: z.string(), type: z.string(),
                          path: z.string(), ... })],
  messages: [{ role: z.string(), content: { text: z.string() } }],
  enabled: z.boolean().optional(),
  source: z.enum(["local", "imported", "builtin"]).optional(),
  createdAt/updatedAt: z.number().int().optional()   // STRING timestamps kill the UI list
})
```

`template` key is tolerated (looseObject) and kept == `content` for the settingsWatcher
JSON shape. The MCP fill tool reads `content`; the UI validates the whole array.

## Restore / verify recipe (v2 tools, repo canonical)

```
python .deepchat/scripts/prompt-store-verify.py            # exact schema + 6-source parity
python .deepchat/scripts/restore_custom_prompts.py verify  # same, with per-store logging
python .deepchat/scripts/restore_custom_prompts.py inventory
python .deepchat/scripts/restore_custom_prompts.py restore # schema-gated restore
python .deepchat/scripts/restore_custom_prompts.py export  # re-export backup copy
```

Restore source precedence: this file → backup file → live Roaming JSON → Roaming DB
(all schema-gated). Always restart DeepChat afterwards (runtime cache is populated at
startup — TEMPLATE-STORES-1 / RUNTIME-CACHE-CONTRACT-1).

## Export discipline

Run `restore_custom_prompts.py export` after ANY prompt change (CMD SKILLS UPDATE cycles,
UI edits), commit this file AND run `prompt-store-verify.py` (exit 0) before closeout.
If this file is newer than the stores, restore from it. NEVER write templates from a
hardcoded in-memory list (CONCURRENT-REWRITE-1).

Current state (2026-08-20, merged canonical): **10 entries** — 7 CMD templates
(cmd-closeout, cmd-continue, cmd-execute, cmd-publish, cmd-red-team, cmd-research,
cmd-skills-update) + 3 quick commands (AUDIT INFRASTRUCTURE, FIND PAPERS ON TOPIC,
VALIDATE CITATIONS), all schema-valid (int timestamps), byte-identical across the 4 live
stores + 2 canonical copies. cmd-skills-update carries the PROMPT-STORE-SCHEMA-GATE
mandate so every future template cycle self-verifies. History: 26 → 18 → 10 consolidation
2026-08-17; v3.53/v3.54-era content merge + timestamp coercion 2026-08-20.
