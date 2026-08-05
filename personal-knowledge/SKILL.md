---
name: personal-knowledge
description: Query the PERSONAL semantic layer (personal-life Vectorize/D1/Workers) from DeepChat. Use when the user asks about their own files, documents, life admin, Obsidian vault, personal archives, or anything NOT QNFO/QWAV research. Bridges personal-search endpoint + durable memories + conversation history + Obsidian vault. STRICTLY personal domain — never mixes with qnfo-* (user mandate 2026-08-04).
version: 1.0
kif_tags: [PERSONAL]
---

# PERSONAL KNOWLEDGE — v1.3 (2026-08-05)

> **PURPOSE:** The user uses DeepChat as the single interface for ALL information
> needs. This skill is the integration path for their PERSONAL files — everything
> that is NOT QNFO/QWAV research (which stays in `search_papers` / `query_graph` /
> `qnfo-projects`). Do NOT cross-contaminate.

>
> **v1.1 UPDATE (2026-08-05, kaizen — GitHub profile deployment runbook + session retrospective):**
> Red-team: direct parent-agent audit of session IfYDah5TSY5gNMY0S4OT5 (rwnq8 profile README
> build + deploy, QNFO/resume -> rwnq8/resume transfer). HARD: 0. SOFT: 3. DESIGN: 1. Changes:
> (1) [SOFT] **GitHub Profile & Personal Repo Deployment section added** — autonomous runbook:
>     deploy pipeline, repo transfer pattern, key facts table (rwnq8/rwnq8 + rwnq8/resume),
>     100% factual badge rule.
> (2) [SOFT] **3 new anti-patterns** — PROFILE-README-DEPLOY-1, GITHUB-CDN-PROPAGATION-1,
>     PROFILE-README-FABRICATE-1 (cross-ref kaizen v1.38 for canonical definitions).
> (3) [SOFT] **Version bumped v1.0 -> v1.1** + banner added.
> (4) [DESIGN] Personal resume repo is now rwnq8/resume (NOT QNFO/resume) — personal content
>     stays in the personal account, per user directive.
> Cross-reference: kaizen v1.38, git-github v2.16, session IfYDah5TSY5gNMY0S4OT5.

> **v1.2 UPDATE (2026-08-05, kaizen — CRITICAL FIX: "Share to Profile" discovery):**
> Red-team: direct parent-agent forensic audit of session IfYDah5TSY5gNMY0S4OT5
> (profile README not appearing on github.com/rwnq8 for 40+ min despite correct
> repo config: name match, public, README.md on main, non-fork).
> HARD: 1. SOFT: 0. DESIGN: 1. Changes:
> (1) [HARD] **GITHUB-CDN-PROPAGATION-1 anti-pattern REVISED** — the 5-30 min "CDN wait"
>     theory was WRONG. Root cause: CLI/API-created profile repos (gh repo create) are
>     NOT auto-promoted. The fix is clicking **"Share to Profile"** on the repo page —
>     profile README appears IMMEDIATELY after. Verified via raw HTML (profile-readme
>     container present server-side).
> (2) [DESIGN] **Deploy runbook updated** — step 4 is now a HARD GATE: click
>     "Share to Profile" after first push. Verification: `curl -s github.com/rwnq8
>     | grep profile-readme`.
> Cross-reference: kaizen v1.38 GITHUB-CDN-PROPAGATION-1 (cross-refs point here),
> git-github v2.16, session IfYDah5TSY5gNMY0S4OT5.

> **v1.3 UPDATE (2026-08-05, kaizen — THIN-CLIENT CANONICAL ASSET: deploy script):**
> Red-team: direct parent-agent audit of session IfYDah5TSY5gNMY0S4OT5 closeout
> (thin-client mandate enforcement — reusable scripts MUST NOT live on local disk).
> HARD: 1. SOFT: 0. DESIGN: 1. Changes:
> (1) [HARD] **Canonical deploy script created** — `scripts/deploy-profile-readme.py`,
>     committed to QNFO/qnfo-skills (PRIMARY canonical) + mirrored to R2 deepchat
>     via skill-sync.js (SECONDARY durable). Live-dir copy is runtime view only.
>     Script performs the full pipeline in ONE turn (clone -> copy -> commit -F ->
>     push -> ls-remote -> curl profile verify -> rmdir) and auto-prints
>     SHARE-TO-PROFILE-REQUIRED when the profile page is not yet serving.
> (2) [DESIGN] **Runbook updated** — deploy pipeline now references the canonical
>     script instead of an inline code pattern.
> Cross-reference: git-github v2.17 THIN-CLIENT CANONICAL ASSET PROTOCOL, kaizen
> v1.39, session IfYDah5TSY5gNMY0S4OT5.



## Separation Mandate (HARD — user directive 2026-08-04)

- Personal layer: `d-drive` bucket, `personal-life` Vectorize, `personal-life` D1,
  `personal-life-indexer` + `personal-life-search` Workers
- QNFO layer: `qnfo-*` buckets/indexes/Workers, `search_papers`, `query_graph`
- **These NEVER mix.** Personal files in qnfo-projects = BUCKET-COMMINGLE-1 (HARD).

## Architecture

```
D:\Archive, D:\Obsidian, D:\Downloads, D:\Google⁠ Download Your Data ...
   │  rclone sync (detached, resumable)
   ▼
d-drive bucket (R2)
   │  personal-life-indexer Worker (cron 0 */12 + /index?cursor=)
   ▼
personal-life Vectorize (768d cosine)  +  personal-life D1 (files registry)
   │
   ▼
personal-life-search Worker:  GET /search?q=<query>&topK=N
   ▼
DeepChat UI (the user's interface)
```

## Query Endpoints

| Endpoint | Method | Purpose |
|:---------|:-------|:--------|
| `https://personal-life-search.q08.workers.dev/search?q=<query>&topK=20` | GET/POST | Semantic search over personal files |
| `https://personal-life-search.q08.workers.dev/stats` | GET | Count of indexed files |
| `https://personal-life-indexer.q08.workers.dev/index?limit=N&scanCap=N&prefix=...&cursor=...` | GET/POST | Trigger/resume indexing |
| `https://personal-life-indexer.q08.workers.dev/files?prefix=...&limit=N` | GET | List indexed file registry |

## DeepChat Integration Path (when user asks about personal content)

```
1. personal-life-search  →  /search?q=<user question>     (semantic hits on their files)
2. search_memories       →  durable memories (preferences, facts, outcomes)
3. search_conversations  →  past DeepChat conversations about this topic
4. Synthesize ONE answer across all three sources (user hates checking multiple places)
```

**Cross-reference rule:** personal results are surfaced with their R2 path
(e.g., `obsidian/notes/v1/2025/07/02/_25183003234.md`) so the user can open them
via the mounted drive or rclone cat.

## Handling Different File Types

The indexer covers text formats automatically (md, txt, csv, json, html, tex, bib,
yaml, log, ini, ...). **PDFs and .docx are NOT auto-indexed** — they need the
extraction helper:

```python
# extract_pdf_text.py — run manually, upload result to d-drive/_extracted/
# Requires: pip install pypdf python-docx (or PyMuPDF)
import os, sys, glob
from pathlib import Path

def extract_pdf(p):
    try:
        from pypdf import PdfReader
        return "\n".join((pg.extract_text() or "") for pg in PdfReader(p).pages)
    except Exception:
        try:
            import fitz  # PyMuPDF
            return "".join(pg.get_text() for pg in fitz.open(p))
        except Exception as e:
            return f"[extract failed: {e}]"

def extract_docx(p):
    from docx import Document
    return "\n".join(par.text for par in Document(p).paragraphs)

# For each PDF/DOCX in a folder, write <name>.txt into D:\_extracted\, then:
# rclone copy D:\_extracted primary-r2:d-drive/_extracted --transfers 8
# (indexer TEXT_EXTS includes 'txt' — next cron/slice picks them up)
```

## Indexer Operations (for the agent)

```bash
# Resume interrupted indexing from saved cursor
python C:\Users\LENOVO\AppData\Local\Temp\per_driver.py   # or replicate the loop:
#   GET /index?limit=300&scanCap=400&prefix=obsidian/&cursor=<last cursor>
#   save returned cursor; repeat until "done": true

# Full re-index of a prefix (registry sig skips unchanged files)
#   GET /index?limit=200&scanCap=400&prefix=downloads/

# Clean a bad file (40023 vector): delete its D1 row + vectorize vectors, re-run
```


## GitHub Profile & Personal Repo Deployment (autonomous runbook)

The user's personal GitHub presence: **github.com/rwnq8**. Profile README lives in
the special repo `rwnq8/rwnq8` (repo name MUST match username exactly — that is what
makes GitHub render it as the profile landing page; there is NO settings toggle).
The personal resume/portfolio repo is **rwnq8/resume** (transferred from QNFO/resume
2026-08-05 — it is personal content, NOT organizational).

### Deploy pipeline (fully agent-executable, zero manual steps)

```bash
# 1. Source file: C:\Users\LENOVO\AppData\Local\Temp\resume-build\rwnq8-README.md
#    (or wherever the latest README draft lives)
# 2. CANONICAL DEPLOY SCRIPT (thin-client asset — lives in git + R2, NEVER on local disk):
python "C:\Users\LENOVO\.deepchat\skills\personal-knowledge\scripts\deploy-profile-readme.py" --src <path-to-README.md>
#    Canonical location: QNFO/qnfo-skills:personal-knowledge/scripts/deploy-profile-readme.py
#    (primary) + R2 deepchat bucket via skill-sync.js (secondary durable mirror).
#    The script performs the full pipeline: clone -> overwrite README.md -> commit -F
#    -> push -> ls-remote verify -> curl profile-page verify -> rmdir cleanup, all in ONE turn.
```

Use the SAME deploy script shape as `git-github` SAME-TURN-COMMIT: clone to %TEMP%,
copy the new README, commit with `-F` (NEVER `-m` — GIT-COMMIT-M-QUOTE-1), push,
verify with `git ls-remote`, then `rmdir /s /q` the temp clone. All in ONE turn —
temp is volatile.

### Updating the README content

1. Edit the local draft (or generate fresh from resume/portfolio material)
2. **100% FACTUAL badge rule (PROFILE-README-FABRICATE-1):** every tool/skill badge
   MUST be attested in the actual resume/portfolio — grep the source files first.
   Never add MATLAB/Docker/Qiskit/etc. badges from training memory.
3. Run the deploy script. Commit message format:
   `ACTION:EDIT FILE: README.md RATIONALE: <what changed>`
4. **CRITICAL — CLICK "Share to Profile" (HARD GATE, verified 2026-08-05):**
   After the push, navigate to `https://github.com/rwnq8/rwnq8` in the logged-in
   browser and click the **"Share to Profile"** button. Without this, the README
   renders on the repo page but NEVER appears on the profile page — no amount of
   waiting, force-pushing, or visibility toggling helps. This is the documented
   manual-promotion path for repos created via CLI/API (gh repo create). Verify
   after clicking: `curl -s https://github.com/rwnq8 | grep profile-readme` must
   return a match.

### Key facts (2026-08-05)

| Item | Value |
|:-----|:------|
| Profile repo | `rwnq8/rwnq8` (public, main branch, README.md in root) |
| Resume/portfolio repo | `rwnq8/resume` (public; transferred from QNFO 2026-08-05) |
| Social links in README | LinkedIn, ResearchGate, ORCID, Zenodo, Resume DOI (10.5281/zenodo.21737024) |
| Profile promotion | **MUST click "Share to Profile"** on the repo page after first push (CLI-created repos are not auto-promoted). Verified: appears immediately after click, server-side rendered (GITHUB-CDN-PROPAGATION-1 revised). The deploy script auto-detects this and prints SHARE-TO-PROFILE-REQUIRED when the profile page is not yet serving the README. |
| Canonical deploy script | `personal-knowledge/scripts/deploy-profile-readme.py` — PRIMARY: QNFO/qnfo-skills git; SECONDARY: R2 deepchat via skill-sync.js; runtime: live skill dir. Full pipeline: clone -> copy -> commit -F -> push -> ls-remote -> curl verify -> rmdir. |

### Repo transfer pattern (if user asks to move a repo)

```bash
gh api repos/{owner}/{repo}/transfer -X POST -f new_owner={target} -H "Accept: application/vnd.github+json"
# Then verify: gh api repos/{target}/{repo} --jq .html_url  -> should resolve to target
# Update any READMEs that reference the old {owner}/{repo} path.
```


## Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| **PERSONAL-QNFO-MIX-1:** answering a personal question from search_papers (QNFO corpus) or answering a research question from personal-life | Route by domain: personal → /search?q= (this skill); research → search_papers/query_graph (research skill). Verify the source layer in the answer. |
| **PERSONAL-STATS-ONLY-1:** reporting "filesIndexed: N" without actually searching | The user wants ANSWERS, not index stats. Always run /search?q= for their actual question. |
| **PDF-SKIP-1:** telling the user "PDFs aren't indexed" instead of extracting them | Run the extraction helper + rclone to _extracted/ so the indexer picks them up. |
| **SINGLE-SOURCE-1:** answering from only the search endpoint | Bridge memories + conversations too — DeepChat is the single interface; the answer should be too. |
| **PROFILE-README-DEPLOY-1:** treating the GitHub profile README as a manual user task | Fully agent-executable: run the canonical script `personal-knowledge/scripts/deploy-profile-readme.py` (git primary / R2 secondary). The user has explicitly mandated ZERO manual steps (MANUAL-DELEGATE-1). |
| **GITHUB-CDN-PROPAGATION-1 (cross-ref, REVISED 2026-08-05):** profile README does NOT auto-appear for CLI/API-created profile repos | **THE REAL FIX is the "Share to Profile" button** on the repo page (github.com/{username}/{username} -> "Share to Profile"). The repo page renders the README but the PROFILE page stays empty until this button is clicked — it is NOT a 5-30min CDN wait. Verified 2026-08-05: rwnq8/rwnq8 rendered on repo page for 40+ min with zero profile-page markdown; clicking "Share to Profile" made it appear on github.com/rwnq8 IMMEDIATELY (server-side rendered, confirmed via curl). Repos created via `gh repo create` need this manual promotion; the editor banner ("is a special repository") confirms recognition but does NOT promote it. |
| **PROFILE-README-FABRICATE-1 (cross-ref):** badge/tool claims without resume attestation | HARD GATE. Grep the actual resume/portfolio for every tool badge before adding it. |

## Related
- cloudflare v3.32 §Vectorize Indexing Gotchas (indexer anti-patterns)
- knowledge skill (QNFO memory/KG — different layer, never merged)
- system v2.13 (skill-sync, desktop boundary)
