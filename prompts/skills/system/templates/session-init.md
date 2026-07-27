# DeepChat Session Initialization Protocol

## Purpose
This template ensures critical skills are loaded at session start, fixing the "weak link" where the 24-Skill Trigger Table (inside qnfo-agent) is unavailable until explicitly loaded.

## Session Start Commands

### Option 1: Full Initialization (Recommended)
```
/init
```
Executes: `skill_view("qnfo-agent")` + `skill_view("system")` + skill-hygiene.js

### Option 2: Minimal Initialization
```
/skills
```
Executes: `skill_list()` to see available skills

### Option 3: Task-Specific Initialization
When starting a specific task, load the relevant skill:
- Research/papers: `skill_view("research")`
- Cloudflare/infra: `skill_view("cloudflare")`
- Code review: `skill_view("code-review")`
- Documents: `skill_view("documents")`

## Automatic Skill Discovery

The qnfo-agent skill contains the **Full 24-Skill Trigger Table**. When loaded, it enables autonomous skill discovery based on task keywords:

| Task Domain | Primary Skill | Also Load |
|:------------|:--------------|:----------|
| deploy, Workers, R2, D1 | cloudflare | qnfo-agent |
| research, paper, Zenodo | research | knowledge, cloudflare |
| UI, design, frontend | frontend-design | cloudflare |
| code review, security | code-review | code |
| git, GitHub, commit | git-github | — |
| documents, docx, xlsx | documents | research |

## Why This Matters

1. **DeepChat shows only 8 skills** in the system prompt (by design)
2. **qnfo-agent contains the full 24-skill trigger table** for autonomous discovery
3. **Without loading qnfo-agent first**, the LLM cannot discover which skill to use
4. **This template ensures** qnfo-agent is always loaded at session start

## Implementation

The `/init` command should be added to DeepChat's custom prompts to auto-execute:
1. `skill_view("qnfo-agent")` — loads the safety-net core with trigger table
2. `skill_view("system")` — loads skill management and config
3. `skill_run("system", "scripts/skill-hygiene.js")` — verifies skill locations

---
*session-init.md v1.0 — DeepChat session initialization protocol*
