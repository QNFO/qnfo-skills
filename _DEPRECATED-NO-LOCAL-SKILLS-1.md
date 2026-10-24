# DEPRECATED — NO LOCAL SKILLS (NO-LOCAL-SKILLS-1, 2026-09-28)

The client loads **NO skills** (`enableSkills: false` in Roaming app-settings.json).
MANDATE-4 SKILL ENFORCEMENT is REMOVED. All domain capability is SERVER-SIDE
(qnfo-ops tools + system-prompt gates + the D1 registry).

This `skills/` directory is retained ONLY because it also hosts two prompt-store
locations the verifier reads (`system-prompt-v2.7.md`, `prompt-stores/customPrompts-canonical.json`)
and as rollback evidence. It is NEVER consulted for capability.

- Do NOT call skill_list() / skill_view().
- Do NOT pull, enumerate, or add skills.
- Rollback: set enableSkills=true and restore from `*.bak-noskills-*`.
