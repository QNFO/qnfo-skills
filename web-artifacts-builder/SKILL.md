---
name: web-artifacts-builder
version: 0.3
description: Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.
license: Complete terms in LICENSE.txt
---

> **v0.3 UPDATE (2026-08-04, kaizen — GitHub Pages deployment patterns + QWAV artifact pipeline):**
> Red-team: direct parent-agent audit of session C8CxG7CWs3AOR9w37Q5c8 (A1/A2/A3 QWAV artifact
> deployment to GitHub Pages). HARD: 3. SOFT: 2. DESIGN: 0.
> Changes:
> (1) [HARD] **PAGES-DEPLOY-OWNER-1**: `POST /user/repos` creates the repo under the PERSONAL
>     account (rwnq8), not the QNFO org. Use `POST /orgs/QNFO/repos` explicitly (CONSOLIDATION-
>     OWNER-RESOLVE-1, kaizen v1.16). Canonical case: a1_create_repo.py created under rwnq8 first.
> (2) [HARD] **PAGES-IDENTITY-1**: a fresh `git clone` has NO git identity — `git commit` fails
>     with "unable to auto-detect email address". Run `git config user.email/user.name` before
>     committing in every fresh clone.
> (3) [HARD] **REPO-ARCHIVED-403**: writing to an ARCHIVED GitHub repo returns 403 "Repository was
>     archived so is read-only". Unarchive via `PATCH /repos/{owner}/{repo}` `{"archived": false}`
>     (requires admin). Canonical case: QNFO/QWAV strategy 3.0 rows frozen until unarchived.
> (4) [SOFT] **PAGES-BUILD-LATENCY-1**: GitHub Pages first build takes 1-5 minutes. Verification
>     MUST poll (up to 3 min), not fail on the first 404. Verify content markers + mojibake scan.
> (5) [SOFT] **TOKEN-DISCOVERY-1**: GitHub token discovery order: env `GH_TOKEN`/`GITHUB_TOKEN`
>     → `~/.github_token` → `~/keys.json` (keys: GH_TOKEN/GITHUB_TOKEN/github_token). Not
>     consistently in env across exec sessions — always check files as fallback.
> Cross-reference: git-github v2.12 (CONSOLIDATION-OWNER-RESOLVE-1, ARCHIVE-REDIRECT-1),
> kaizen v1.18, qnfo-core N-2.

> **v0.2 UPDATE (2026-08-03, kaizen — Cloudflare discovery):**
> Red-team: parent-agent ecosystem audit. HARD: 0. SOFT: 1. DESIGN: 0.
> Added §Cloudflare Deployment (Pages + R2) with canonical tool names (`workers_list`,
> `search_cloudflare_documentation`, `migrate_pages_to_workers_guide`, `search_papers`,
> `query_graph`) + Anti-Phantom Gate verification. Closes cloudflare v3.18 map gap:
> skill previously had ZERO Cloudflare references despite the map claiming Pages deploys.

> **v0.1 UPDATE (2026-08-03, kaizen — skill merge):**
> Merged `frontend-design` skill (43 lines) into this skill.
> Red-team: direct parent-agent ecosystem audit. HARD: 0. SOFT: 0. DESIGN: 1.
> Content appended as 

---

## GitHub Pages Deployment (QWAV artifact pipeline — MANDATORY)

Artifacts/websites built with this skill can be deployed to GitHub Pages under the
**QNFO GitHub org** (canonical home; no separate QWAV org exists; agent has admin
rights on QNFO). Verified 2026-08-04 on QWAV Artifacts A1/A2/A3.

### Deployment Protocol (verified end-to-end)

```python
# 1. CREATE repo under QNFO org EXPLICITLY (NOT /user/repos — PAGES-DEPLOY-OWNER-1)
body = json.dumps({
    "name": "<repo-name>",
    "description": "<desc>",
    "homepage": "https://qnfo.github.io/<repo-name>/",
    "private": False, "has_pages": True, "auto_init": True
}).encode()
POST https://api.github.com/orgs/QNFO/repos   # NOT /user/repos

# 2. Clone with token URL
git clone https://x-access-token:{GH_TOKEN}@github.com/QNFO/<repo-name>.git .

# 3. SET GIT IDENTITY in fresh clone (PAGES-IDENTITY-1 — commit fails without it)
git config user.email "agent@qnfo.org"
git config user.name "QNFO Agent"

# 4. Copy index.html + README.md, commit with -F msgfile (cmd.exe quoting)
git add index.html README.md
git commit -F <msgfile>     # NEVER git commit -m "multi word" on cmd.exe

# 5. Push
git push origin main

# 6. Enable Pages (idempotent POST)
POST https://api.github.com/repos/QNFO/<repo-name>/pages
  {"source": {"branch": "main", "path": "/"}}

# 7. VERIFY — poll for up to 3 min (PAGES-BUILD-LATENCY-1)
#    200 OK + content markers (title, canvas ids, footer) + zero mojibake
```

### Strategy status tracking (QNFO/QWAV)

Strategy 3.0 (`QNFO/QWAV/strategy/3.0.md`) carries the artifact status table
(A1-A5, K1-K5). Update rows via Contents API after deployment:
- If the repo is ARCHIVED: `PATCH /repos/QNFO/QWAV {"archived": false}` first
  (REPO-ARCHIVED-403) — requires admin.
- Then GET contents → base64 decode → replace `📋 PLANNED` → `✅ DONE` + LIVE URL → PUT.

### Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| **PAGES-DEPLOY-OWNER-1**: `POST /user/repos` creates under personal account (2026-08-04) | Always `POST /orgs/QNFO/repos` for QNFO-hosted artifacts. Check `html_url` owner in the response. |
| **PAGES-IDENTITY-1**: fresh clone commit fails "unable to auto-detect email" (2026-08-04) | `git config user.email` + `user.name` in EVERY fresh clone before committing. |
| **REPO-ARCHIVED-403**: writing to archived repo → 403 (2026-08-04) | `PATCH /repos/{owner}/{repo} {"archived": false}` (admin) before writing. |
| **PAGES-BUILD-LATENCY-1**: first Pages build 404s (2026-08-04) | Poll up to 3 min (20s intervals) before declaring failure. Verify content markers, not just HTTP 200. |
| **TOKEN-DISCOVERY-1**: GH token missing from env in some exec sessions (2026-08-04) | Discovery order: env `GH_TOKEN`/`GITHUB_TOKEN` → `~/.github_token` → `~/keys.json` (keys GH_TOKEN/GITHUB_TOKEN/github_token). |

---

## Frontend Design Principles (merged from frontend-design skill, 2026-08-03).

# Web Artifacts Builder — v0.3

To build powerful frontend claude.ai artifacts, follow these steps:
1. Initialize the frontend repo using `scripts/init-artifact.sh`
2. Develop your artifact by editing the generated code
3. Bundle all code into a single HTML file using `scripts/bundle-artifact.sh`
4. Display artifact to user
5. (Optional) Test the artifact

**Stack**: React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui

## Design & Style Guidelines

VERY IMPORTANT: To avoid what is often referred to as "AI slop", avoid using excessive centered layouts, purple gradients, uniform rounded corners, and Inter font.

## Quick Start

### Step 1: Initialize Project

Run the initialization script to create a new React project:
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

This creates a fully configured project with:
- ✅ React + TypeScript (via Vite)
- ✅ Tailwind CSS 3.4.1 with shadcn/ui theming system
- ✅ Path aliases (`@/`) configured
- ✅ 40+ shadcn/ui components pre-installed
- ✅ All Radix UI dependencies included
- ✅ Parcel configured for bundling (via .parcelrc)
- ✅ Node 18+ compatibility (auto-detects and pins Vite version)

### Step 2: Develop Your Artifact

To build the artifact, edit the generated files. See **Common Development Tasks** below for guidance.

### Step 3: Bundle to Single HTML File

To bundle the React app into a single HTML artifact:
```bash
bash scripts/bundle-artifact.sh
```

This creates `bundle.html` - a self-contained artifact with all JavaScript, CSS, and dependencies inlined. This file can be directly shared in Claude conversations as an artifact.

**Requirements**: Your project must have an `index.html` in the root directory.

**What the script does**:
- Installs bundling dependencies (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- Creates `.parcelrc` config with path alias support
- Builds with Parcel (no source maps)
- Inlines all assets into single HTML using html-inline

### Step 4: Share Artifact with User

Finally, share the bundled HTML file in conversation with the user so they can view it as an artifact.

### Step 5: Testing/Visualizing the Artifact (Optional)

Note: This is a completely optional step. Only perform if necessary or requested.

To test/visualize the artifact, use available tools (including other Skills or built-in tools like Playwright or Puppeteer). In general, avoid testing the artifact upfront as it adds latency between the request and when the finished artifact can be seen. Test later, after presenting the artifact, if requested or if issues arise.

## Reference

- **shadcn/ui components**: https://ui.shadcn.com/docs/components

---

## Cloudflare Deployment (Pages + R2) — MANDATORY discoverability

Artifacts/websites built with this skill can be deployed to Cloudflare Pages (static
hosting) with assets archived to R2. **Never deploy without verifying.**

**Canonical agent tools for Cloudflare discovery & verification (use by name):**
- `workers_list` — enumerate deployed Workers/Pages state before trusting any "deployed" claim
- `search_cloudflare_documentation` — Cloudflare limits, Pages config, R2 API reference
- `migrate_pages_to_workers_guide` — when migrating Pages projects to Workers
- `search_papers` / `get_paper_context` / `query_graph` — QNFO publication state cross-refs
- `skill_view("cloudflare")` — the canonical Cloudflare skill (full-stack mandate, EXECUTION GATE,
  anti-patterns KIF-50/51/52, LoS audit scripts). ALWAYS load before any deploy.

**Deployment paths (per cloudflare skill decision ladder — MCP tools → wrangler → REST):**
1. Pages project: `npx wrangler pages project list` → confirm project exists
2. Deploy: `npx wrangler pages deploy <dist-dir> --project-name <project>` (or REST API)
3. R2 archive (canonical asset store): `npx wrangler r2 object put <bucket>/<key> --file <local> --remote`
4. **Verify (Anti-Phantom Gate — mandatory):** probe the deployed URL live (HTTP 200) and
   re-GET the R2 object comparing size/hash. Never claim "deployed" from exit code alone.

**Cross-refs:** cloudflare skill v3.38 (§MCP-Driven Operations, §KIF-50/51/52), research v2.97
(Phase 6 deployment + Phase 8 core distribution), qnfo-core v1.24 (integrity gates).

---



---

## GitHub Pages Deployment (QWAV artifact pipeline — MANDATORY)

Artifacts/websites built with this skill can be deployed to GitHub Pages under the
**QNFO GitHub org** (canonical home; no separate QWAV org exists; agent has admin
rights on QNFO). Verified 2026-08-04 on QWAV Artifacts A1/A2/A3.

### Deployment Protocol (verified end-to-end)

```python
# 1. CREATE repo under QNFO org EXPLICITLY (NOT /user/repos — PAGES-DEPLOY-OWNER-1)
body = json.dumps({
    "name": "<repo-name>",
    "description": "<desc>",
    "homepage": "https://qnfo.github.io/<repo-name>/",
    "private": False, "has_pages": True, "auto_init": True
}).encode()
POST https://api.github.com/orgs/QNFO/repos   # NOT /user/repos

# 2. Clone with token URL
git clone https://x-access-token:{GH_TOKEN}@github.com/QNFO/<repo-name>.git .

# 3. SET GIT IDENTITY in fresh clone (PAGES-IDENTITY-1 — commit fails without it)
git config user.email "agent@qnfo.org"
git config user.name "QNFO Agent"

# 4. Copy index.html + README.md, commit with -F msgfile (cmd.exe quoting)
git add index.html README.md
git commit -F <msgfile>     # NEVER git commit -m "multi word" on cmd.exe

# 5. Push
git push origin main

# 6. Enable Pages (idempotent POST)
POST https://api.github.com/repos/QNFO/<repo-name>/pages
  {"source": {"branch": "main", "path": "/"}}

# 7. VERIFY — poll for up to 3 min (PAGES-BUILD-LATENCY-1)
#    200 OK + content markers (title, canvas ids, footer) + zero mojibake
```

### Strategy status tracking (QNFO/QWAV)

Strategy 3.0 (`QNFO/QWAV/strategy/3.0.md`) carries the artifact status table
(A1-A5, K1-K5). Update rows via Contents API after deployment:
- If the repo is ARCHIVED: `PATCH /repos/QNFO/QWAV {"archived": false}` first
  (REPO-ARCHIVED-403) — requires admin.
- Then GET contents → base64 decode → replace `📋 PLANNED` → `✅ DONE` + LIVE URL → PUT.

### Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| **PAGES-DEPLOY-OWNER-1**: `POST /user/repos` creates under personal account (2026-08-04) | Always `POST /orgs/QNFO/repos` for QNFO-hosted artifacts. Check `html_url` owner in the response. |
| **PAGES-IDENTITY-1**: fresh clone commit fails "unable to auto-detect email" (2026-08-04) | `git config user.email` + `user.name` in EVERY fresh clone before committing. |
| **REPO-ARCHIVED-403**: writing to archived repo → 403 (2026-08-04) | `PATCH /repos/{owner}/{repo} {"archived": false}` (admin) before writing. |
| **PAGES-BUILD-LATENCY-1**: first Pages build 404s (2026-08-04) | Poll up to 3 min (20s intervals) before declaring failure. Verify content markers, not just HTTP 200. |
| **TOKEN-DISCOVERY-1**: GH token missing from env in some exec sessions (2026-08-04) | Discovery order: env `GH_TOKEN`/`GITHUB_TOKEN` → `~/.github_token` → `~/keys.json` (keys GH_TOKEN/GITHUB_TOKEN/github_token). |

---

## Frontend Design Principles (merged from frontend-design skill, 2026-08-03)

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

---

## Version

Current: **v0.3** (kaizen — GitHub Pages deployment patterns: PAGES-DEPLOY-OWNER-1,
PAGES-IDENTITY-1, REPO-ARCHIVED-403, PAGES-BUILD-LATENCY-1, TOKEN-DISCOVERY-1;
QWAV A1/A2/A3 artifact pipeline verified; 2026-08-04)
