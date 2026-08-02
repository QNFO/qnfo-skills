---
name: memory-management
version: "1.0"
description: Guide the agent to recall, remember, and route durable learning into Memory, Skills, Scheduled Tasks, or Tape.
---


> **v1.1 UPDATE (2026-08-02, kaizen — restart after prune):**
> [HARD] agent.db pruning / VACUUM changes the skill index. Schedule a restart
> after any prune so DeepChat re-reads the DB: `python "<system>\scripts\restart-deepchat.py" --reason "agent.db pruned"`.
> `--vacuum` specifically requires DeepChat CLOSED — the helper handles the
> close/relaunch sequence. Cross-reference: system v2.6, bloat-cleanup v2.8.


# Memory Management

> **STALE AGENT.DB CACHE (2026-08-02):** When DeepChat skills fail to load after
> restart despite valid YAML/frontmatter, suspect a stale agent.db cache rather
> than file errors. A process restart alone may not clear the indexer cache —
> use the deferred restart: `python "%USERPROFILE%\.deepchat\skills\system\scripts\schedule-restart.py"`.
> See system skill §Auto-Restart Protocol.


Use this skill when a task may produce durable learning or when the user asks you to recall, remember, continue earlier work, preserve an exact statement, capture a reusable procedure, or handle a recurring need.

## Recall

Rely on automatic memory injection for ordinary context. Use `memory_recall` when the user refers to previous work with cues such as again, last time, before, continue, same project, remember, or asks what you already know.

Use `tape_search` and then `tape_context` when the user needs source evidence, exact wording, logs, command output, file snippets, or why a prior decision was made. Memory is a durable conclusion layer, not the raw transcript.

## Remember

Use `memory_remember` only for durable conclusions that should change future behavior. Choose the most specific category:

- `user_preference`: stable user preferences, constraints, communication style, environment choices.
- `project_fact`: durable project conventions, architecture entry points, commands, dependencies, paths, or operational constraints.
- `task_outcome`: completed, blocked, or deliberately deferred task results. Include status, outcome, and blocker in prose when relevant.
- `heuristic`: reusable troubleshooting strategy, workflow, decision rule, or engineering lesson.
- `anti_pattern`: repeated mistake, unsafe approach, brittle pattern, stale assumption, or thing to avoid.

Do not remember raw tool results, bash output, grep output, file contents, transient mechanics, one-off failures, secrets, credentials, hidden reasoning, or anything only useful for the current turn.

## Verbatim Scope

Store exact wording only when the user explicitly asks you to remember a sentence or phrase verbatim. In that case, keep the requested text intact and make the surrounding content minimal.

Automatic extraction is different: it should normalize durable facts into concise memory content, deduplicate related entries, and avoid preserving raw transcript text.

## Procedures -> Skill

When the useful learning is a reusable multi-step procedure, prefer drafting a skill with `skill_manage` instead of stuffing the full procedure into Memory. Memory may keep a short pointer or heuristic, but the repeatable workflow belongs in a Skill.

Use `skill_manage` for draft skills only. Do not modify installed skills unless the user explicitly asks through the supported review flow.

## Recurring -> Scheduled Task

When the user asks for a periodic, low-frequency, or future recurring action, suggest creating a Scheduled Task in settings. Memory does not wake the agent, schedule future work, or create automation side effects.

## End-of-task Learning Check

Before finishing a non-trivial task, check whether there is one durable lesson to save:

1. Did the user reveal a stable preference or constraint?
2. Did you learn a durable project fact?
3. Is there a task outcome, blocker, or explicit deferral worth preserving?
4. Did a reusable heuristic work?
5. Did an anti-pattern or stale assumption become clear?
6. Is this actually a reusable procedure for `skill_manage` or a recurring need for Scheduled Tasks rather than Memory?

Remember only the smallest durable conclusion. Leave raw process in Tape.

> **UPDATE (2026-08-02): MCP-OFFLOAD-1 — QNFO MCP tools (search_papers, query_graph,
> resolve_paper_id, search_memories, recall_facts, memory_recall) often return "OK"
> with results offloaded to unreadable files.** Do NOT treat "OK" as evidence of
> retrieved content. For verification-critical lookups, prefer direct probes
> (Python urllib + browser UA against live endpoints) or cross-check via the
> cloudflare skill's agent tool map. Also: DeepChat memories are EPHEMERAL —
> critical rules belong in SKILL.md; memory is for session outcomes, not authority.
> Cross-reference: cloudflare v3.18, kaizen v1.4.1.

