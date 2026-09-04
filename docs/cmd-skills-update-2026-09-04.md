# CMD SKILLS UPDATE 2026-09-04 (canonical v4.08 block)

Cycle executed 2026-09-04 (system-prompt v4.07 -> v4.08 / kaizen v2.130 -> v2.131).

## Red-team skills audit (2026-09-04) — PASS at the v4.07 state
- prompt-store-verify.py exit 0: SYSTEM-PROMPT-PARITY PASS (5 stores identical), SKILL-ANCHOR-PARITY PASS (17 versioned skills), PROMPT-STORE-VERIFY PASS (schema + parity), MCP-AUTOAPPROVE file intact 9/9.
- Audited v4.07-state 5-store sha 306741bbc693d2888843f5aba68a148d039f61f8a6e68c6a6782580fb0372a87 / 121815 bytes; header==footer==title v4.07.
- Skill anchors: kaizen 2.130 / research 2.149 / cloudflare 3.74 / qnfo-core 1.43 / execution-mandate 2.14; live==repo hashes for 10 core skills; qnfo-skills repo clean at 5b9ade8.
- scheduler-guard.py exit 0 (5 canonical rows, 0 disabled residue).
- model_guard.py exit 0 state=clean (all four model keys flash); QNFO-ModelKey-Guard Windows task verified at every-30-min repeat (last run 2026-09-04 03:55, result 0).

## Findings
- HARD: 1 — RESTORE-CP-FILE-GAP-1: restore_custom_prompts.py restore() omitted ROAMING_CP_FILE (Roaming/DeepChat/custom_prompts.json). Docstring claimed all 4 live stores; restore only wrote Roaming DB + Roaming app-settings.json + script canonical backup, leaving the standalone CP file stale and prompt-store-verify exit 1 until manual sync. Fix: v2.1 adds the ROAMING_CP_FILE full-list rewrite; proven by re-running restore ("Roaming custom_prompts.json: OK") + prompt-store-verify exit 0.
- SOFT: 1 — AUDIT-ANCHOR-SNAPSHOT-1: audit-record anchor lists inside top gates describe the PRE-BUMP audited state (v4.07 record lists kaizen 2.129; the 2.130 bump shipped the same record). Header kaizen version = post-bump truth.
- DESIGN: 0.

## Dual-write v4.07 -> v4.08
- Canonical system prompt (123743 chars, sha 51c2778b2064b381 after RESTORE-gate amend) synced to all 5 system-prompt stores: .deepchat md / qnfo-skills repo md / Roaming app-settings.json default_system_prompt / Roaming agent.db systemPrompts / Roaming agent.db agents.deepchat systemPrompt.
- 11/11 CMD templates re-synced to all template stores (repo canonical, script canonical, Roaming app-settings customPrompts, Roaming custom_prompts.json, Roaming DB customPrompts, .deepchat skills mirror) with 2026-09-04 additions on CMD SKILLS UPDATE + CMD RED TEAM (cadence parity).
- DEEPCHAT-DEFAULT-MODEL-1: all four model keys deepseek/deepseek-v4-flash.
- Commits: 4298906 (dual-write) + 7316878 (cycle-log sha correction). master at 7316878 on origin.
