---
name: cloudflare-deployer
description: Cloudflare platform deployment operations — Pages, R2, Workers, Vectorize, DNS, redirects, and Containers. Use when the agent needs to deploy, manage, or troubleshoot Cloudflare infrastructure.
version: "1.8"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# CLOUDFLARE DEPLOYER SKILL — v1.8

> **On-demand skill.** Load via `skill_view('cloudflare-deployer')` for all Cloudflare operations.
> Source: `templates/CLOUDFLARE-DEPLOYMENT.md` v2.1 + QWAV-DEFAULT.md §0.6.5-0.6.7

---

## execute_plan (MANDATORY — Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** — at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** — Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Verify wrangler auth", "status": "pending"},
  {"step": "Pull test suite from R2", "status": "pending"},
  {"step": "Pull build script from R2", "status": "pending"},
  {"step": "Build publication artifacts", "status": "pending"},
  {"step": "Deploy to Cloudflare Pages", "status": "pending"},
  {"step": "Run post-deploy red-team verification", "status": "pending"},
  {"step": "Verify MathJax config on deployed page", "status": "pending"},
  {"step": "Upload artifacts to R2", "status": "pending"},
  {"step": "Clean up ephemeral files", "status": "pending"},
])

---

## ⚠️ WRANGLER v4.95+ COMPATIBILITY

**`r2 object list` was REMOVED in wrangler v4.95+.** Only `get`, `put`, `delete` are available.
The `--remote` flag is deprecated (remote is default in v4+). For directory enumeration, deploy a list-objects Worker or use per-object `get` operations.

---

## Authentication

**PERSISTENT -- 2026-06-19:** The CLOUDFLARE_API_TOKEN is stored at User-level with ALL Cloudflare permissions. No manual loading needed. Token survives reboots.

**Token:** API Token with ALL PERMISSIONS (full account access)
- Account: quniverse (edb167b78c9fb901ea5bca3ce58ccc4b)
- Email: rwnquni@outlook.com
- Persistence: User env var (set via [Environment]::SetEnvironmentVariable)
- Token prefix: cfat_Imj... (53 chars)

**Scopes:** ALL Cloudflare policies: Pages (deploy), R2 (read+write+delete), Workers, Vectorize, D1, DNS (zone:edit), redirect rules, zones, AI, containers, queues, pipelines, secrets store.

**S3-compatible access:**
- Endpoint: https://edb167b78c9fb901ea5bca3ce58ccc4b.r2.cloudflarestorage.com
- Access Key ID: 2b87ede317499c6a6a2f8e5c42667c52
- Secret Access Key: stored in persistent env

For direct API calls, use the token via Bearer auth:
```bash
curl -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" https://api.cloudflare.com/client/v4/...
```


-
## Policy Access Matrix (v1.3 — Verified 2026-06-19)

All Cloudflare policies verified via both wrangler CLI and REST API direct calls. Actual enumerated resource counts from the quniverse account.

| Service | Access | Count | API Endpoint | Wrangler Command |
|:--------|:------:|:------|:-------------|:-----------------|
| **R2** | ✅ Read+Write+Delete | 1 bucket (qnfo) | `/accounts/:id/r2/buckets` | `wrangler r2 object {get,put,delete}` |
| **Pages** | ✅ Full | 10 projects (3 essential, 4 redirecting) | `/accounts/:id/pages/projects` | `wrangler pages project list` |
| **Workers** | ✅ Full | 30 scripts | `/accounts/:id/workers/scripts` | `wrangler deploy` |
| **D1** | ✅ Full | 5 databases | `/accounts/:id/d1/database` | `wrangler d1 list` |
| **KV** | ✅ Full | 2 namespaces | `/accounts/:id/storage/kv/namespaces` | `wrangler kv namespace list` |
| **Vectorize** | ✅ Full | 3 indexes (qwav-research-v2, qnfo-handoffs, qnfo-tasks) | `/accounts/:id/vectorize/indexes` | `wrangler vectorize list` |
| **Queues** | ✅ Full | 2 queues | `/accounts/:id/queues` | `wrangler queues list` |
| **AI (Workers AI)** | ✅ Full | Models available | `/accounts/:id/ai/models/search` | `wrangler ai models list` |
| **Pipelines** | ✅ Full | Configured | `/accounts/:id/pipelines` | `wrangler pipelines` |
| **Hyperdrive** | ✅ Full | Configured | `/accounts/:id/hyperdrive/configs` | `wrangler hyperdrive` |
| **Workflows** | ✅ Full | Configured | `/accounts/:id/workflows` | `wrangler workflows` |
| **DNS / Zones** | ✅ Granted | 0 zones | `/zones` | `wrangler dns` (zone context required) |
| **Secrets Store** | ✅ Granted | Configurable | `/accounts/:id/secrets-store` | `wrangler secrets-store` |
| **AI Search** | ✅ Granted | Configurable | `/accounts/:id/ai-search` | `wrangler ai-search` |
| **Browser Run** | ✅ Granted | Configurable | `/accounts/:id/browser` | `wrangler browser` |
| **Containers** | ✅ Granted | Configurable | `/accounts/:id/containers` | `wrangler containers` |
| **VPC** | ✅ Granted | Configurable | API | `wrangler vpc` |
| **Certificates (mTLS)** | ✅ Granted | Configurable | API | `wrangler cert` / `wrangler mtls-certificate` |
| **Email Routing** | ✅ Granted | Configurable | API | `wrangler email` |
| **Artifacts** | ✅ Granted | Configurable | API | `wrangler artifacts` |
| **Agent Memory** | ✅ Granted | Configurable | API | `wrangler agent-memory` |
| **Web Search** | ✅ Granted | Configurable | API | `wrangler websearch` |
| **Dispatch Namespaces** | ✅ Granted | Configurable | API | `wrangler dispatch-namespace` |
| **Tunnels** | ✅ Granted | Configurable | API | `wrangler tunnel` |

### Available Resources (Enumerated)

**R2 Buckets:** `qnfo` (primary) — audit trails, releases, deployments, tools, projects, discovery index

**D1 Databases (5):**
- `qnfo-cms` (0458a344) — CMS content management (34 entries, 5 types)
- `qnfo-graph` (a1954b92-d681-4d02-b1f6-f9a2eb4c265d) — Knowledge graph storage
- `qnfo-audit` (35e2e573-92f3-46ac-83c6-22f6429fc5e5) — Audit trail storage
- `living-paper` (70a58cb3-b2cd-498d-877f-ecca86859a22) — Living paper data (170 papers, 23 columns)
- `portfolio-state` (d80fdf2a-0a60-45a3-968b-2907ce806dcd) — Portfolio state

**KV Namespaces (1):**
- `equation-cache` (2fbbb9fa2d774a6e80d3a3d2547f8b5f) — Equation rendering cache
- ~~`git-on-cloudflare-routes`~~ — DEPRECATED (GitHub fully deprecated per ADR-001)

**Vectorize Indexes (3):**
- `qwav-research-v2` — 1024-dim cosine, active (bge-m3 compatible). Used by ask-qwav Worker.
- `qnfo-handoffs` — 768-dim cosine, handoffs semantic search
- `qnfo-tasks` — 768-dim cosine, tasks semantic search
- ~~`qwav-research` (768-dim)~~ — DELETED (replaced by v2)
- ~~`paper-similarity` (1024-dim)~~ — DELETED (empty, redundant)

**Queues (2):**
- `qnfo-lifecycle-queue` — Lifecycle pipeline (archival jobs, auto-transitions)
- `git-on-cloudflare-repo-maint` (296cceec) — Git repository maintenance (DEPRECATED — GitHub deprecated per ADR-001)

**Pages Projects (10):** qnfo-hub (hub.qnfo.org), qnfo-publications (papers.qnfo.org + 5 topics), qnfo-legal (legal.qnfo.org), quantum-laws-of-form (laws.qnfo.org → 301), qwav (deep.qwav.tech → 301), qnfo-archive (archive.qnfo.org → 301), adelic-qft (adelic.qnfo.org → 301), qlof-primer (primer.qwav.tech → 301), qnfo-ipfs-archive, qnfo-design-system

**Workers (26 scripts):** Deployed — key workers include `graph-api` (Knowledge Graph), `qnfo-lifecycle` (automated project lifecycle, cron: daily 06:00 UTC), `living-papers-api` (Living Papers with D1 + IPFS), `qnfo-archive-worker` (queue consumer for R2 archival migration), `qnfo-archive-verify` (archive verification), `umbrella-router` (traffic routing). Query via `wrangler deployments` with specific worker names.

-

## Prerequisites

1. **Cloudflare API Token** — auto-available via `$env:CLOUDFLARE_API_TOKEN` (User-level env var, survives reboots). Verify: `npx wrangler whoami` must show account `quniverse`.
2. **Node.js 18+ / npm** — required for `npx wrangler`. Verify: `node --version`.
3. **Python 3.8+** — required for build scripts and R2 utilities.
4. **Network access** — `api.cloudflare.com` must be reachable.
5. **Git workspace** — all operations must run from within a git-tracked project directory.

**Pre-flight check:**
```bash
npx wrangler whoami              # Must show quniverse account
node --version                    # Must be >= 18
python --version                  # Must be >= 3.8
```

---

## Cloudflare Pages

```bash
# List all Pages projects
npx wrangler pages project list

# Deploy
npx wrangler pages deploy <dir> --project-name <name> --branch main

# Custom domain
npx wrangler pages project set-domain <name> <domain>

# Deployment history
npx wrangler pages deployment list --project-name <name>

# Rollback
npx wrangler pages deployment rollback --project-name <name>
```

**Active Projects:** qwav (deep.qwav.tech), prompts-wiki, qnfo-archive (archive.qnfo.org),
quantum-laws-of-form (laws.qnfo.org), qlof-primer (primer.qwav.tech), +11 more.

### Post-Deploy Verification (MANDATORY for ALL deploys — v1.7)

**This is the deployment instance of the RED-TEAM → DoD → ITERATE → REFINE cycle.** See `skill_view('red-team-dod')` for the canonical framework.

After deploying ANY content to Cloudflare Pages or Workers, run the post-deploy red-team:

```bash
# Pull test suite from R2 (ephemeral)
npx wrangler r2 object get qnfo/tools/test_suite.py --remote --file=_test_suite.py

# Run deploy verification (Pages + CMS + KG)
python _test_suite.py --cms --pages --kg

# Content quality gate — MUST PASS
python _test_suite.py --content

# Discard
Remove-Item _test_suite.py
```

**GATE:** If ANY test marked `CRIT` fails → deployment is NOT complete. Fix before claiming [EXECUTED].
**GATE:** If ANY page shows `stub=True` → deployment is REJECTED. Content must be professional.
**GATE:** If ANY publication shows `EMPTY body` → content is NOT ready.

### Post-Deploy Redirect Verification (MANDATORY for Redirect Deployments)

After deploying redirects, verify they actually work:

```bash
python _dod_enforce.py --preflight-only && python _test_suite.py --redirects
```

**GATE:** `_dod_enforce.py` must return exit 0 AND `_test_suite.py --redirects` must show all redirects as PASS.

### Post-Deploy MathJax Verification (MANDATORY for Publication Pages)

After deploying ANY publication page to Cloudflare Pages, verify MathJax is correctly configured:

```bash
# Post-deploy MathJax verification — write check script, execute, discard
echo "import urllib.request, sys; url = sys.argv[1]; html = urllib.request.urlopen(url).read().decode('utf-8'); config_pos = html.find('window.MathJax'); script_pos = html.find('MathJax-script'); assert config_pos >= 0, f'MathJax config missing on {url}'; assert script_pos >= 0, f'MathJax script missing on {url}'; assert config_pos < script_pos, f'Config AFTER script on {url}'; print(f'[OK] MathJax correct: config@{config_pos}, script@{script_pos}')" > _verify_cf_mathjax.py
python _verify_cf_mathjax.py <deployed-url>
Remove-Item _verify_cf_mathjax.py
```

**CRITICAL:** The `window.MathJax` configuration MUST come BEFORE the `<script id="MathJax-script">` tag. If config is after the script, MathJax initializes without macros and math will NOT render. This is the #1 cause of "MathJax isn't rendering."

For the canonical MathJax configuration, see `templates/MATHJAX-CONFIG.md` and `templates/HTML-PUBLICATION-PAGE.md`.

---

## Cloudflare R2 (Object Storage)

```bash
# Get an object (v4.95+ compatible)
npx wrangler r2 object get qnfo/audit/state/<project>.json

# Put an object
npx wrangler r2 object put qnfo/audit/state/<project>.json --file=<local-file>

# Delete an object
npx wrangler r2 object delete qnfo/audit/state/<project>.json

# NOTE: r2 object list does NOT exist in v4.95+
# Use per-object get operations instead
```

**Primary bucket:** `qnfo`
**R2 paths:** `qnfo/audit/state/`, `qnfo/audit/backlog/`, `qnfo/audit/decisions/`,
`qnfo/releases/YYYY/MM/`, `qnfo/deployments/`

---

## Cloudflare Workers

```bash
# Deploy a worker
npx wrangler deploy --name <worker-name>

# Deployment history
npx wrangler deployments list
```

---

## Cloudflare Containers

```bash
# Create
npx wrangler containers create <name> --image ubuntu-22.04

# Execute
npx wrangler containers exec <name> -- "<command>"

# List
npx wrangler containers list

# Stop
npx wrangler containers stop <name>
```

---

## Vectorize (Semantic Search)

For paper vectorization, use:
```bash
# Pull from R2: npx wrangler r2 object get qnfo/tools/vectorize-papers.py --remote --file=_vectorize-papers.py
python _vectorize-papers.py
# Discard: Remove-Item _vectorize-papers.py
```

---

## Cost Gate

| Resource | Free Tier | Overage |
|:---------|:----------|:--------|
| Pages builds | 500/month | Builds queue |
| Pages bandwidth | Unlimited | N/A |
| Workers requests | 100k/day | $0.30/M |
| R2 storage | 10 GB | $0.015/GB/mo |
| R2 egress | **Free** | N/A |
| Containers | Free quota | $0.002/min |

---


---

## Skills Backup & Recovery (v1.3)

All 28 QNFO DeepChat skills are redundantly backed up. This skill itself is recoverable from:

| Source | Location | Recovery Command |
|:-------|:---------|:-----------------|
| **GitHub** | `rwnq8/qnfo-skills` | `git clone https://github.com/rwnq8/qnfo-skills.git %APPDATA%\.deepchat\skills` |
| **R2** | `qnfo/prompts/skills/cloudflare-deployer/SKILL.md` | `python bootstrap_skills.py --source r2` |
| **Discovery Index** | `qnfo/discovery/index.json` (skills_backup) | JSON lookup |

**Bootstrap tools on R2:**
- `qnfo/tools/bootstrap_skills.py` — One-command restore from GitHub or R2
- `qnfo/tools/skills-recovery-guide.md` — Full recovery documentation

**Keep synced after any skill change:**
```bash
python "%APPDATA%\.deepchat\skills\bootstrap_skills.py" --sync
```
This pushes to GitHub AND uploads to R2 in a single command.

## Common Patterns

### Deploy a Publication

> **Design System v2.0 (2026-06-30):** All pages must use the Silent Radix Light Theme.
> CSS: `https://qnfo.org/design-system/qnfo-light.css`
> PDF Builder: `qnfo/design-system/build_pdf.py` (v2.0)
> Template: `qnfo/design-system/publication-template.html`
> 🚫 **DARK THEMES FORBIDDEN.**
```bash
# 1. Build PDF
# Pull from R2: npx wrangler r2 object get qnfo/design-system/build_pdf.py --remote --file=_build_pdf.py
python _build_pdf.py
# Discard: Remove-Item _build_pdf.py --input <file>

# 2. Deploy to Pages
npx wrangler pages deploy <dir> --project-name qwav --branch main

# 3. Upload PDF to R2
npx wrangler r2 object put qnfo/releases/YYYY/MM/<file>.pdf --file=<path>

# 4. Generate SEO
# Pull from R2: npx wrangler r2 object get qnfo/tools/generate-seo.py --remote --file=_generate-seo.py
python _generate-seo.py
# Discard: Remove-Item _generate-seo.py
```

### Check Infrastructure Health
```bash
npx wrangler whoami
npx wrangler pages project list
npx wrangler r2 object get qnfo/audit/state/qwav.json
```

### Verify Design System
```bash
# Check if a page uses the light theme
python -c "import urllib.request;h=urllib.request.urlopen('https://papers.qnfo.org/').read().decode();print('DARK' if '#0a0a0f' in h or '#0d1117' in h else 'LIGHT')"
```

---


---

## QNFO Design System Compliance (v2.0 - 2026-06-30)

**ALL QNFO/QWAV publications, pages, PDFs, and web artifacts MUST use the Silent Radix Light Theme.**

| Resource | Location |
|:---------|:---------|
| Canonical CSS | `https://qnfo.org/design-system/qnfo-light.css` |
| PDF builder (v2.0) | `qnfo/design-system/build_pdf.py` |
| HTML template | `qnfo/design-system/publication-template.html` |
| Design doc | `qnfo/design-system/QNFO-DESIGN-SYSTEM.md` |

**DARK THEMES FORBIDDEN.** All output must use:
- White background (#FFFFFF), dark text (#363636)
- System font stack, max-width 800px centered layout
- Clean tables with border-collapse: collapse
- MathJax CHTML with left-aligned display equations

## Failure Handling

| Scenario | Response |
|:---------|:---------|
| `wrangler whoami` fails or shows wrong account | Token expired or wrong — run `npx wrangler login` or verify `$env:CLOUDFLARE_API_TOKEN` |
| R2 upload returns HTTP 401 | Token has insufficient permissions — token must have R2 read+write+delete |
| Pages deploy returns build error | Check build output directory exists and contains `index.html` |
| Worker deploy returns "duplicate script" | Use `--force` flag or delete old version first |
| `r2 object list` returns "command not found" | Feature removed in v4.95+ — use per-object `get` operations or REST API `_r2_list.py` |
| DNS/redirect changes not propagating | Cloudflare DNS TTL is 300s minimum — wait and retry |
| `skill_view('cloudflare-deployer')` returns error | Skill not indexed — run `bootstrap_skills.py --sync` and restart DeepChat |
| MathJax not rendering after deploy | Config is AFTER script tag — fix ordering before redeploying |
| Token not found in environment | Persist token: `[Environment]::SetEnvironmentVariable('CLOUDFLARE_API_TOKEN', '<token>', 'User')` |

**Recovery tools on R2:**
- `qnfo/tools/fast_r2_upload.py` — batch R2 upload (250x faster than wrangler)
- `qnfo/tools/r2_list.py` — R2 object listing
- `qnfo/tools/ps_run.py` — Safe Python execution bridge
- `qnfo/design-system/build_pdf.py` — Markdown to PDF
- `qnfo/tools/generate-seo.py` — SEO metadata generation
- `qnfo/tools/bootstrap_skills.py` — Skill sync and recovery



## Reference Files

- Full deployment template: `templates/CLOUDFLARE-DEPLOYMENT.md`
- Cloudflare audit: `qnfo/SESSION-HANDOFF-2026-05-28.md`
- SEO generator: `_generate-seo.py` (R2: `qnfo/tools/generate-seo.py`)
- Vectorize: `_vectorize-papers.py` (R2: `qnfo/tools/vectorize-papers.py`)

---


## Embedded Scripts

> **SELF-CONTAINED:** This skill depends on the scripts listed below. Before executing any script, verify it exists at its canonical path.

| Script | R2 Canonical | Execution Cache | Purpose |
|:-------|:-------------|:----------------|:--------|
| `vectorize-papers.py` | `qnfo/tools/\vectorize-papers.py` | Index papers in Cloudflare Vectorize for semantic search |
| `build_pdf.py` | `qnfo/tools/\build_pdf.py` | Markdown/HTML -> PDF (shared with publication-publisher) |

### Bootstrap Protocol

Before using any script, verify it exists:
```bash
# Pull from R2: npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py
# Verify: Test-Path _<script>.py
```

**If script is MISSING:** Scripts are version-controlled in the prompts repo.
1. `git log --oneline -- qnfo/tools/<script>.py`
2. The canonical source for all tools is R2 (`qnfo/tools/`). Pull from R2: `npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py`.

**Shared scripts:** `build_pdf.py` is primarily maintained in the `publication-publisher` skill.
If missing, check that skill's Embedded Scripts section for recovery guidance.

### Dependencies
- `vectorize-papers.py`: requires Cloudflare API token (auto-available via `$env:CLOUDFLARE_API_TOKEN`) and Workers AI access
- `build_pdf.py`: requires `reportlab` and optionally `markdown` packages


*cloudflare-deployer skill v1.6 — Load on-demand via skill_view(). RED-TEAM-DOD post-deploy verification. Compatible with wrangler v4.95+*

---

*cloudflare-deployer v1.5 — QNFO custom skill. Load via read('R2 `qnfo/prompts/skills/cloudflare-deployer\\SKILL.md'). Not accessible via skill_view().*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.\n**Skill-Specific Checks:**\n6. Pages Preview URL: Verify deploy accessible at *.pages.dev before custom domain\n7. R2 Sync: Verify qnfo-cms-client.js exists on R2 with correct version\n8. CDN Purge: Verify custom domain serves latest deploy after CDN propagation\n9. MathJax Config: For publication pages, verify MathJax config BEFORE script tag
Refer to RED-TEAM-PROTOCOL.md for full protocol.

