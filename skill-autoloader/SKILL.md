---
name: skill-autoloader
description: AUTOMATICALLY loads relevant QNFO skills based on task detection. User NEVER manually loads skills. Cross-references all skills. Handles fallback when skill_view() fails.
pinned: true
---

# SKILL AUTO-LOADER — v1.0

> **PRIORITY 0 — pinned, always active. User NEVER manually loads skills.**

## Purpose

The LLM system automatically detects what skills are needed for any task and loads them without user prompting. The user should NEVER say "load the cloudflare-deployer skill" — the LLM detects the task and loads it.

## Core Rules

### Rule 1: Auto-Detect by Task Pattern

When the user's message or the LLM's planned task matches a pattern, auto-load the relevant skill:

| Task Pattern | Auto-Load |
|-------------|-----------|
| deploy, upload, wrangler, Pages, Workers, R2, D1, DNS, KV, Vectorize, Queues, Cloudflare | `cloudflare-deployer` |
| publish, Zenodo, DOI, PDF, paper, manuscript, LaTeX | `publication-publisher` |
| close out, terminate, done, session end, HANDOFF, handoff | `closeout-manager` |
| git error, detached HEAD, merge conflict, rebase | `git-hygiene` |
| email, send, Outlook, compose | `email-composer` |
| PDF build, convert markdown, LaTeX compile | `pdf-builder` (via cloudflare-deployer) |
| knowledge graph, KG, graph-api, dependencies, impact, neighbors, nodes, edges | `knowledge-graph` |
| audit, infrastructure, health check, orphan, stale, lifecycle | `infrastructure-audit` |
| UI, design, frontend, page, styling, BLING, visual | `bling-usability-audit` |
| research, paper search, literature, arXiv, Semantic Scholar | `literature-search` |
| SEO, sitemap, robots.txt, discoverability, llms.txt | `seo-discoverability` |
| Kaizen, improve, update system, deploy prompts | `kaizen-autonomous-update` |
| skill sync, backup skills, restore skills | `skill-sync` |
| cite, citation, BibTeX, bibliography | `citation-manager` |
| social media, tweet, post, Buffer, LinkedIn, Bluesky | `buffer-integration` |
| template, fill_prompt_template | `template-catalog` |
| migrate, local to R2, cleanup, thin client | `local-to-r2-migration` |
| prompt audit, self-audit, skill audit | `prompt-audit` |
| user story, "as a researcher", "I need to" | `user-story-separation` |

### Rule 2: Fallback When skill_view() Fails

If `skill_view('name')` returns an error, try these fallbacks in order:
1. `read('%APPDATA%\.deepchat\skills\<name>\SKILL.md')`
2. `npx wrangler r2 object get qnfo/prompts/skills/<name>/SKILL.md --remote --file=_skill.md` then read
3. Report `[SKILL-UNAVAILABLE: <name>]` and continue with best-effort knowledge

NEVER ask the user to manually load a skill. NEVER silently continue without the skill's critical instructions.

### Rule 3: Cross-Link Skills

Every QNFO skill MUST reference related skills in its header:
```
> **Related:** execution-guard, closeout-manager, cloudflare-deployer
```

When loading skill A, auto-load any skills it cross-references that are relevant to the current task.

### Rule 4: Pre-Task Skill Check

Before executing any task, check:
1. What skills does this task require?
2. Have they been loaded this session?
3. If not: load them now (auto-detect + fallback)

### Rule 5: Load Once, Use Many

Once a skill is loaded, cache its content for the session. Don't re-load the same skill multiple times.

## Skill Inventory (34 skills)

| Skill | Trigger Pattern | Related Skills |
|-------|----------------|---------------|
| `skill-autoloader` | (always active) | all |
| `execution-guard` | (always active) | closeout-manager, qnfo-agent |
| `user-story-separation` | user stories | qnfo-agent, execution-guard |
| `qnfo-agent` | (always active) | all |
| `cloudflare-deployer` | deploy, upload, wrangler, Pages, Workers, R2, D1, DNS, KV | infrastructure-audit, closeout-manager |
| `closeout-manager` | close, terminate, handoff, done | execution-guard, cloudflare-deployer, knowledge-graph |
| `publication-publisher` | publish, Zenodo, DOI, PDF, paper | cloudflare-deployer, citation-manager |
| `knowledge-graph` | KG, graph-api, dependencies, neighbors | qnfo-agent, infrastructure-audit |
| `infrastructure-audit` | audit, health check, orphan, stale | cloudflare-deployer, knowledge-graph |
| `literature-search` | research, arXiv, Semantic Scholar | publication-publisher, citation-manager |
| `git-hygiene` | git error, detached HEAD, merge | closeout-manager |
| `email-composer` | email, send, Outlook | — |
| `template-catalog` | template, fill_prompt_template | all |
| `citation-manager` | cite, BibTeX, bibliography | publication-publisher, literature-search |
| `bling-usability-audit` | UI, design, frontend, styling | cloudflare-deployer |
| `seo-discoverability` | SEO, sitemap, robots.txt | cloudflare-deployer |
| `buffer-integration` | social media, tweet, post | publication-publisher |
| `kaizen-autonomous-update` | Kaizen, improve, update | closeout-manager, skill-sync |
| `skill-sync` | sync skills, backup | kaizen-autonomous-update |
| `prompt-audit` | prompt audit, self-audit | skill-sync |
| `local-to-r2-migration` | migrate, cleanup, thin client | cloudflare-deployer |
| `handoff-protocol` | handoff, QACP | closeout-manager |
| `ultrametric-engine` | ultrametric, p-adic, tree | knowledge-graph |

## Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| User says "load the cloudflare-deployer skill" | Should never happen — auto-detected |
| LLM says "I don't know how to deploy — which skill?" | Load cloudflare-deployer automatically |
| skill_view() fails, LLM silently continues | Run fallback chain: read() → R2 → report |
| Skill loaded but not used | Only load skills relevant to current task |
| Skills loaded multiple times | Cache: load once per session |

---

*skill-autoloader v1.0 — Priority 0. Auto-detects task patterns and loads skills. User never manually manages skills. Fallback recovery for load failures.*
