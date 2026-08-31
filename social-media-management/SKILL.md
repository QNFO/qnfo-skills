---
name: social-media-management
version: 1.10.0
description: Programmatic social media follow management for Bluesky and Mastodon
  with a curated QNFO account registry covering 96 QNFO-aligned accounts (52 Bluesky
  / 7 Mastodon / 27 X / 10 LinkedIn) across four platforms. Use when the user wants
  to follow/unfollow accounts, bulk-follow QNFO-aligned researchers, manage social
  media presence, or discover accounts in quantum foundations, ultrametric physics,
  laws of form, infomatics, CFPE forecasting, consilience, complex systems, AI+science,
  and related domains. Covers Bluesky AT Protocol API, Mastodon REST API, account
  registry, taxonomy-driven discovery (discover_accounts.py), and browser-automation
  path for LinkedIn profile updates.
---
> **v1.10.0 UPDATE (2026-08-28, kaizen — qnfo-social cloud posting pipeline):**
> qnfo-social Worker replaces local bluesky_post.py for Bluesky posting. Pipeline: /compose (deepseek-v4-flash via Workers AI drafts a 5-post thread from title+abstract -> status='draft'), /approve (draft->queued), cron "30 14 * * *" posts the oldest queued thread, /broadcast (409 guard), /queue (sanitized). D1 social_threads (status queued/posting/posted/failed/draft + retry_count + error). Secrets BSKY_HANDLE/BSKY_APP_PASS/SOCIAL_TOKEN. Draft-only compose preserves accuracy. DEEPSEEK-WORKERS-AI-CHAT-MODEL-1: deepseek-v4-flash is a CHAT model - use messages format + read choices[0].message.content, never prompt format / .response. workers.dev: 1010 (Bot Fight Mode, browser UA) + 1042 (subdomain propagation).

> **v1.9.0 UPDATE (2026-08-26, kaizen — BUFFER-TOKEN-ENV-1: Buffer token env-sourced + queue-clear resume):**
> Red-team: direct parent-agent (RES.024 P7 Buffer social 2026-08-26). HARD: 1. Changes:
> (1) [HARD] **BUFFER-TOKEN-ENV-1 added** — Buffer API token discovery: **env `BUFFER_TOKEN` is now the primary source** (TOKEN-DISCOVERY-1 order: env → tokens dir → keys.json → memory). The Buffer MCP was REMOVED 2026-08-17 (per v1.8.0); the canonical path is the **Buffer GraphQL API** `api.buffer.com/graphql` with `Authorization: Bearer $BUFFER_TOKEN` — discover org via `account { organizations { id name } }`, channels via top-level `channels(input:{organizationId})` (check `isDisconnected`), post via `createPost` with UNION fragments and REQUIRED `mode: addToQueue, needsApproval: false, schedulingType: "automatic"`. When the user clears the queue ("THERE ARE NO POSTS IN BUFFER QUEUE"), the earlier queue-full/expired-token block is lifted — re-check env for a fresh token and resume P7 posting. Canonical: RES.024 2026-08-26 — 3 scheduled posts (LinkedIn 6a8fc1aa, X 6a8fc1ab, Mastodon 6a8fc1ad), 266-char D7 copy, concept DOI 10.5281/zenodo.22114388.
> Cross-reference: research v2.141 (Buffer GraphQL dictionary), kaizen v2.101, system-prompt v3.78, session this.

> **v1.8.0 UPDATE (2026-08-18, kaizen — PERSONAL ALIGNMENT: Become-a-Node strategy):**
> Red-team: direct parent-agent (user directive "DEFINITELY UPDATE MY PERSONAL SKILL...AND OTHERS
> TO ALIGN WITH MY VISION, VALUES, AND MOTIVATIONS").
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **Become-a-Node Strategy section added** — the QNFO tribe is scattered across
>     boundaries; scattered tribes find members through nodes, not conferences: monthly presence
>     on one LoF-adjacent channel (math4wisdom / stream.syscoi.com), D1-D7 broadcast per event,
>     per-bet portfolio broadcasts with external-only traction, authoritative venue facts via
>     memory f94805ee (supersedes stale venue claims). FM version quoted per ecosystem convention.
> Cross-reference: qnfo-core v1.31 §0.8, portfolio memory 1e82547d, venue corrections f94805ee,
> session gtblUizh8IJisfcn-08HI.

> **v1.7.0 UPDATE (2026-08-14, kaizen — Zenodo Dissemination Playbook D7 broadcast):**
> Red-team: direct parent-agent audit (session waFvkOWgtaYZqNMLWOqdW continuation; reviewer stalled -> fallback).
> HARD: 0. SOFT: 0. DESIGN: 0 (post-fix).
> Changes:
> (1) [HARD] **`zenodo_broadcast.py` added to scripts/** — Zenodo Dissemination
>     Playbook lever D7: composes <280-char "impact copy" (contribution -> DOI ->
>     3 hashtags, no exclamation points) and dispatches to Mastodon + Bluesky ONLY
>     with an explicit `--post` flag. Compose-only default (TEST-SEND-EXTERNAL-1
>     compliance). Enforces BSKY-300-GRAPHEME-1 (290-char cap). Credential discovery
>     per TOKEN-DISCOVERY-1 (env -> keys.json -> ~/.mastodon_creds.json).
> (2) [SOFT] **D7 workflow documented** — after a Zenodo record goes live:
>     `python scripts\zenodo_broadcast.py --doi <doi> --title "<title>"` (compose),
>     then `--post` when confirmed live. Cross-links knowledge skill v2.11 playbook.
> Cross-reference: knowledge v2.11 (Zenodo Dissemination Playbook D1-D7),
> playbook note 2026-08-14, BSKY-300-GRAPHEME-1, TEST-SEND-EXTERNAL-1.


> **v1.6.0 UPDATE (2026-08-05, kaizen — Bluesky posting script + 300-grapheme limit):**
> Red-team: direct parent-agent audit of session 3i_KVLownViukLTZB_BJ1 (discoverability sprint).
> HARD: 1. SOFT: 0. DESIGN: 1. Changes:
> (1) [HARD] **BSKY-300-GRAPHEME-1 anti-pattern added** — 300-grapheme hard limit; post 1
>     (322 chars) rejected 3x before trim.
> (2) [DESIGN] **bluesky_post.py added to scripts/** — AT Protocol posting client with
>     credential auto-discovery (env → keys.json → .env → .bsky_credentials) and threaded
>     posting. Canonical thread: references/bluesky-thread.txt (5 posts, published live).
> Cross-reference: kaizen v1.51, research v2.79, session 3i_KVLownViukLTZB_BJ1.

> **v1.5.0 UPDATE (2026-08-05, kaizen — UNIFIED CROSS-PLATFORM SOCIAL HUB + linkedin-mcp DELETED):**
> Red-team: direct parent-agent audit of session yHXrIYDvUfwQ6twlIaWG5.
> HARD: 1. SOFT: 2. DESIGN: 1. Changes:
> (1) [HARD] **linkedin-mcp-tools v2.0.3 DEPRECATED** — never functional on this machine:
>     profile dir `C:\Users\LENOVO\.linkedin-mcp\profile` MISSING, credential stores
>     MISSING, auto-login script absent, `LINKEDIN_COOKIE` schema-only/inert (zero
>     addCookies in dist). User verified: "NON-FUNCTIONAL PIECE OF SHIT". This skill is
>     now the SINGLE hub for ALL social media: Bluesky, Mastodon, X (manual), LinkedIn
>     (browser-automation path), and Buffer (functional remote MCP with real token).
> (2) [SOFT] **LINKEDIN-MCP-NONFUNCTIONAL-1 anti-pattern added** — never build an
>     automation layer on a tool whose auth chain is unverified end-to-end; audit the
>     profile dir + credential stores + cookie-injection code BEFORE wiring it in.
> (3) [SOFT] **Buffer MCP section added** — mcp.buffer.com remote MCP is enabled=True with
>     a real Bearer token in mcp-settings.json; cross-platform posting path documented.
> (4) [DESIGN] **Platform Support Matrix updated** — LinkedIn row corrected to
>     browser-automation (autocomplete selectors); Buffer row added.
> Cross-reference: linkedin-mcp (DELETED 2026-08-05), kaizen v1.44 (ZENODO-RAW-UPLOAD-CT-1
> class — same verify-the-auth-chain discipline), session yHXrIYDvUfwQ6twlIaWG5.

> **v1.4.1 UPDATE (2026-08-05, kaizen — STALE-COUNT-1 live recurrence + phantom-entry removal):**
> - Phantom entry **@ivl@mathstodon.xyz (Ivo Velitchkov) REMOVED** — Mastodon API lookup
>   returned HTTP 404 (2026-08-05). It was added unverified during the LoF investigation;
>   per registry verification discipline, entries MUST be live-verified before addition.
> - STALE-COUNT-1 demonstrated live: the v1.4.0 closeout left prose claims (97/8) stale
>   after the registry changed (96/7). ALL prose counts now reconciled to actual data:
>   desc/section 96-52-7-27-10; table rows ump 3, slb 1, inm 13, cfe 11, res 24, plt 6, dem 1.
> - Registry enriched: slb_communities (syscoi.com, math4wisdom.com) + lof50_proceedings refs.
> - Cross-reference: kaizen v1.46 STALE-COUNT-1, DOTFILE-TRACK-GAP-1.

> **v1.4.0 UPDATE (2026-08-05, kaizen):** Red-team audit closeout.
> - Registry actual count reconciled: **97 accounts** (52 Bluesky / 8 Mastodon / 27 X / 10 LinkedIn).
> - Frontmatter description de-staled (was '45+' from v1.0; now reflects full scope).
> - Mastodon +1 since v1.3.0: Ivo Velitchkov (@ivl@mathstodon.xyz, SLB re-entry/systems, unverified).
> - `.kaizen_history` created (protocol compliance).
> - Audit verified: N-2 triple consistent, 5/5 scripts compile, 7/7 taxonomy sections,
>   registry canonical (0 bad domains, 0 missing DIDs), no non-installed skill refs.

> **v1.3.0 UPDATE (2026-08-05):** Ecosystem-tier completion.
> - Registry expanded 75 → **96 accounts** (Bluesky 52 / Mastodon 7 / X 27 / LinkedIn 10).
> - RES·Autaxys extension: quantum cognition (Hameroff proxy = Arizona Astrobiology Ctr), The Neurocritic.
> - DEM tier: John D. Cook (golden ratio/applied math, bridged from mathstodon).
> - INM: +Jens Eisert (quantum thermodynamics — Margolus-Levitin relevance).
> - CFE·Scenario/Econ: +80,000 Hours, Matt Clancy (Open Phil), Max Roser.
> - Mastodon +4: @simonmyerson (LoF-adjacent number theorist), @mc (category-cybernetics),
>   @paolop (applied category theory), @manlius (complexity networks).
> - X +7 / LinkedIn +3: Friston, Hossenfelder, Hameroff, Smolin, Koch, Lidar, Tononi.
> - NEW script `discover_accounts.py` — taxonomy-keyword-driven discovery (Bluesky + Mastodon).
> - Taxonomy reference completed: PLT + DEM sections added (all 7 programs present).

> **v1.2.0 UPDATE (2026-08-05):** Full-scope correction — taxonomy treated as
> the map of the ENTIRE research ecosystem, not a niche list.
> - Registry expanded 55 → **75 accounts** (Bluesky 25 → **45**, all live-verified).
> - +20 accounts across every program tier: INM (Active Inference Institute,
>   Anil Seth, Allen Institute), RES·Autaxys (Quantum Biology DAO, Aiello),
>   RES·Bridge (Hossenfelder, Krauss), RES·Stratigraphy (NIST), CFE·Domain
>   (Minev, Wootton), PLT·4-D (Protocol Labs, Filecoin, IPFS), PLT·Agentic
>   (LangChain, Hugging Face), PLT·Cloudflare (CF Dev), UMP·Community (AMS, LMS).
> - Domain taxonomy extended with `plt` (QWAV Platform) — 6 codes total.
> - Remaining gaps: SLB (0), UMP individuals (rare), CFE scenario/econ tiers.

> **v1.1.0 UPDATE (2026-08-05):** QNFO taxonomy integration.
> - All 25 Bluesky handles live-verified via unauth `resolveHandle` (DIDs recorded).
> - Registry remapped to canonical QNFO program codes (ump/slb/inm/cfe/res).
> - +6 CFE accounts (forecasting): Wildeford, Sempere, de Neufville, Unjournal, Bengio, Erdil.
> - +2 Mastodon: Nathaniel Virgo (@Nathaniel@mathstodon.xyz), Victor Buendia (@vbuendiar@fediscience.org).
> - New script `verify_bsky_handles.py` — unauthenticated live handle verification.
> - New reference `qnfo_taxonomy.md` — full QNFO keyword taxonomy for account discovery.

> **v1.0.0 INITIAL RELEASE (2026-08-05):**
> Zero-dependency Python automation for Bluesky and Mastodon follow management.
> 55 QNFO-aligned accounts across 4 platforms (25 Bluesky / 3 Mastodon / 20 X / 7 LinkedIn).
> X/Twitter: API follow removed from Basic/Pro — registry + manual only.
> LinkedIn: connections via browser-automation with authenticated Chrome profile.
# SOCIAL MEDIA MANAGEMENT — v1.10.0

UNIFIED cross-platform social media hub: follow management (Bluesky/Mastodon),
curated QNFO account registry (97 accounts), Buffer MCP cross-platform posting, and
LinkedIn browser-automation path (linkedin-mcp DELETED 2026-08-05).

---

## Platform Support Matrix

| Platform  | Follow API? | Auth Model                  | Script                | Daily Limit     |
|:----------|:------------|:----------------------------|:----------------------|:----------------|
| Bluesky   | ✅ YES      | App password (AT Protocol)  | `bluesky_follow.py`   | ~100+           |
| Mastodon  | ✅ YES      | OAuth 2.0 (REST)            | `mastodon_follow.py`  | Instance limit  |
| X/Twitter | ❌ NO       | OAuth 1.0a/2.0 (removed)    | Manual only           | N/A             |
| LinkedIn  | ❌ NO API   | Browser automation (autocomplete selectors) | Manual via browser | N/A — profile edit unbounded |
| Buffer    | ❌ NO (MCP removed 2026-08-17) | Buffer web UI / REST API | — | Cross-platform scheduler |

> **X/Twitter note:** The Follows and List Follows endpoints were removed from
> Basic and Pro tiers in August 2023. Only Enterprise tier ($42K+/year) retains
> them. X/Twitter accounts are tracked in the registry for manual reference.

---

## Quick Start

### 1. Bluesky Setup

```bash
# Create an app password at: https://bsky.app/settings/app-passwords
# (NOT your account password — app passwords are scoped and revocable)

# Set credentials (or create .env file)
set BSKY_HANDLE=you.bsky.social
set BSKY_APP_PASS=xxxx-xxxx-xxxx-xxxx

# Follow a single account
python scripts\bluesky_follow.py follow preskill.bsky.social

# Bulk follow ALL QNFO Bluesky accounts from the registry
python scripts\bluesky_follow.py bulk references\qnfo_accounts.json

# List who you're following
python scripts\bluesky_follow.py list-following
```

### 2. Mastodon Setup

```bash
# Interactive OAuth setup (opens browser, asks for auth code)
python scripts\mastodon_follow.py auth mastodon.social
# (Replace "mastodon.social" with your instance, e.g. mathstodon.xyz)

# Follow a single account
python scripts\mastodon_follow.py follow @johncarlosbaez@mathstodon.xyz

# Bulk follow ALL QNFO Mastodon accounts
python scripts\mastodon_follow.py bulk references\qnfo_accounts.json

# List following
python scripts\mastodon_follow.py list-following
```

### 3. Unified CLI

```bash
# Dry-run: preview all accounts by platform
python scripts\social_follow.py dry-run

# Follow ALL accounts on ALL configured platforms
python scripts\social_follow.py all

# Follow on Bluesky only
python scripts\social_follow.py all bluesky

# Follow on Mastodon only
python scripts\social_follow.py all mastodon
```

---

## Script Reference

### `bluesky_follow.py` — AT Protocol Client

Zero-dependency Python client for the Bluesky AT Protocol. Uses only `urllib`
(stdlib). No `pip install` required.

**Commands:**

| Command           | Description                                    |
|:------------------|:-----------------------------------------------|
| `follow @handle`  | Follow a single account by handle or DID       |
| `bulk file.json`  | Bulk follow from JSON registry or handle list  |
| `unfollow @handle`| Unfollow an account                            |
| `list-following`  | List all accounts you currently follow         |

**Auth flow:** Handle + app password → `com.atproto.server.createSession` →
bearer token for subsequent calls.

**Follow record:** `com.atproto.repo.createRecord` with collection
`app.bsky.graph.follow` and subject DID.

**Rate limiting:** Configurable via `BSKY_RATE_LIMIT_DELAY` (default 1.0s).
State file (`~/.bsky_follow_state.json`) prevents duplicate follow attempts.

### `mastodon_follow.py` — REST Client

Zero-dependency Python client for the Mastodon REST API.

**Commands:**

| Command           | Description                                  |
|:------------------|:---------------------------------------------|
| `auth [instance]` | Interactive OAuth 2.0 setup                  |
| `follow @handle`  | Follow a single account (resolves federation)|
| `bulk file.json`  | Bulk follow from JSON registry               |
| `unfollow @handle`| Unfollow an account                          |
| `list-following`  | List following with display names            |

**Auth flow:** Register OAuth app → user authorizes in browser → exchange
code for token → persist to `~/.mastodon_creds.json`. Scopes: `read write follow`.

**Federation:** Handles cross-instance follows via `/api/v2/search?resolve=true`.
Mastodon accounts are identified as `@user@instance.tld`.

---

## LinkedIn — Browser Automation Path (ONLY method)

**linkedin-mcp-tools MCP DELETED (2026-08-05)** — never functional. The ONLY
LinkedIn automation path is browser automation via puppeteer-core CDP with an
authenticated Chrome profile (`~/.linkedin-profile`, one manual sign-in required).

---

### What Works (EDITING existing sections only)

| Section | Method | Verified |
|:--------|:-------|:---------|
| **Headline** | Navigate `/in/{slug}/edit/intro` → `div[contenteditable="true"].ProseMirror` (TipTap editor) → `execCommand('selectAll')` + `execCommand('insertText')` → Save | ✅ 2026-08-05, live |
| **About** | Navigate profile page → click `a[aria-label="Edit about"]` (NOT a button!) → wait for TipTap editor → `execCommand('insertText')` → Save | ✅ 2026-08-05, live |

### What Does NOT Work (ADDING new sections — CDP CANNOT automate)

| Section | Blocker |
|:--------|:--------|
| **Experience** | Profile has no experience section. "Add a position or career break" button exists but produces NO form/modal via CDP. Requires "Add profile section" → Core → Add experience flow — the popup renders outside detectable DOM containers. LINKEDIN-EXP-NO-FORM-1. |
| **Skills** | Same blocker — not on main profile. Behind "Add profile section" → Core → Skills panel. |
| **Education** | Same blocker — not on main profile. |
| **Certifications** | Same blocker — not on main profile. |
| **Featured** | Same blocker. |
| **Any NEW section type** | Profiles WITHOUT a section type CANNOT have it added via CDP. Only existing sections can be EDITED. |

### Working Pipeline

**Script:** `scripts/linkedin-apply-profile.py` — puppeteer-core CDP browser automation.
**Data:** `scripts/linkedin-profile-update.json` — structured profile data from resume pipeline.

```cmd
python scripts/linkedin-apply-profile.py ^
  --package scripts/linkedin-profile-update.json ^
  --section about   # or headline
```

**Auth gate:** First run opens Chrome for manual sign-in. Persistent profile survives sessions.

### Verified Selectors (CDP/puppeteer-core)

| Target | Selector | Notes |
|:-------|:---------|:------|
| Login username | `input[autocomplete="username"]` | IDs are randomized |
| Login password | `input[autocomplete="password"]` | |
| Edit-intro URL | `https://www.linkedin.com/in/{slug}/edit/intro` | NOT /in/edit/intro |
| Headline editor | `div[contenteditable="true"].ProseMirror` | TipTap/ProseMirror |
| About edit trigger | `a[aria-label="Edit about"]` | **It is an `<a>`, NOT a `<button>`!** |
| Save button | `button` with innerText `"Save"` / `"Opslaan"` | |
| Content insertion | `execCommand('selectAll')` + `execCommand('insertText')` | ProseMirror-compatible. `el.innerText = x` is NOT. |
| Navigation | `waitUntil: 'domcontentloaded'` | LinkedIn NEVER reaches networkidle0 |

### Safety

Profile edits are unbounded (not gated by connection budget). But LinkedIn bot detection is
aggressive: pace edits, one section per session, human-in-the-loop for CAPTCHA/2FA. If
blocked (CLOUDFLARE_BLOCKED / AUTH_REQUIRED), stop and re-authenticate manually — **never
hammer retries. Retrying the same broken approach risks account lockout.**

### Profile Update Mapping (from resume pipeline)

| LinkedIn field | Source (resume repo) |
|:---------------|:---------------------|
| Headline | RESUME.md subtitle / Target Roles |
| About | RESUME.md Professional Summary |
| Experience | RESUME.md Professional Experience — **manual only** |
| Skills | SKILLS-TECHNOLOGY.md matrix — **manual only** |


---
---

## Buffer — Cross-Platform Posting (MCP REMOVED 2026-08-17)

Buffer MCP was **removed** in the MCP audit 2026-08-17 (unneeded for QNFO/Cloudflare;
plaintext Bearer token removed from `mcp-settings.json`). Buffer scheduling now uses the
Buffer web UI or REST API directly.

- **Channels:** publish the same QNFO content to all connected profiles from one queue
- **Workflow:** draft in markdown → post via Buffer web/API → verify in Buffer dashboard
- **Auth:** Buffer token no longer stored in `mcp-settings.json` (TOKEN-DISCOVERY-1 order: tokens dir → env → memory → user)
- **Integration:** pairs with `email-composer` for announcement sequences and with
  the registry for account targeting

---

## Account Registry (`references/qnfo_accounts.json`)

The registry tracks **96 QNFO-aligned accounts** across four platforms (52
Bluesky / 7 Mastodon / 27 X / 10 LinkedIn). `domain` = canonical QNFO program
code; `domain_detail` = sub-topic. All 52 Bluesky handles carry live-verified DIDs.

### Canonical QNFO Program Codes (from qnfo_taxonomy.md)

| Code | Program | Registry Coverage (2026-08-05) |
|:-----|:--------|:-------------------------------|
| `ump` | Ultrametric Physics | 3 (AMS, LMS, Janssen — Langlands community; individuals rare) |
| `slb` | Laws of Form | 1 (@simonmyerson — demarcation/Jaffe-Quinn; direct LoF theorists absent) |
| `inm` | Infomatics | 13 (Preskill, Wilde, Eisert, Seth, Allen, Active Inference…) |
| `cfe` | CFPE / Paradigm Engineering | 11 (forecasters + quantum roadmaps + scenario/econ) |
| `res` | QNFO Research (consilience/Ruliad) | 24 (18 BS + 6 MS: Carroll, Coecke, Virgo, Hossenfelder…) |
| `plt` | QWAV Platform (4-D + agentic AI) | 6 (Protocol Labs, Filecoin, IPFS, LangChain, HF, CF Dev) |
| `dem` | QWAV Demos | 1 (John D. Cook, golden-ratio applied math) |

**Known gaps:** `ump` (p-adic/ultrametric researchers maintain no public social
presences — use taxonomy keywords for recurrent discovery) and `slb` (Laws of
Form community is tiny; check second-order cybernetics circles).

### Discovery Protocol (see qnfo_taxonomy.md for full keyword sets)

0. **Automated**: run `scripts\discover_accounts.py --dry-run` to preview
   candidate checks per program; add `--add-verified` to append verified
   Bluesky finds directly into the registry. Mastodon verification requires
   `MASTODON_TOKEN` (from `mastodon_follow.py auth`).
1. **Bluesky**: `https://bsky.app/search?q=<keyword>` — centralized search.
2. **Mastodon**: `GET /api/v2/search?q=<keyword>&resolve=true` on
   `mathstodon.xyz`, `fediscience.org`, `qoto.org` — run per-instance.
3. **X/Twitter**: manual search (API follow removed); read via
   DataWhisker/x-mcp-server if installed.
4. **Verify before adding**: run
   `scripts\verify_bsky_handles.py` (unauthenticated AT Protocol resolveHandle)
   to confirm Bluesky handles live and record DIDs. Set `verified: true` only
   after live confirmation.

### Adding Accounts

Edit `references/qnfo_accounts.json` — the schema is:

```json
{
  "accounts": {
    "bluesky": [
      {"handle": "user.bsky.social", "name": "Display Name",
       "domain": "res", "domain_detail": "complex-systems", "verified": true}
    ]
  }
}
```

`domain` must be one of `ump`/`slb`/`inm`/`cfe`/`res`/`plt`. Then run
`verify_bsky_handles.py` to populate the live DID.

### Bluesky Starter Packs

The registry also tracks Bluesky starter packs — one-click bundles of related
accounts. Load these in the Bluesky app to bulk-follow entire communities:
[QuantumSky](https://bsky.app/starter-pack/quantumsky),
[Quantum Computing](https://bsky.app/starter-pack/quantum-computing),
[QEC Pack](https://bsky.app/starter-pack/qec),
[Forecasting & Prediction Markets](https://blueskystarterpack.com/forecasting-and-prediction-market).

---

### `bluesky_post.py` — AT Protocol Posting Client

Zero-dependency posting client with credential auto-discovery (env → keys.json →
.env → .bsky_credentials) and threaded posting. Canonical thread:
`references/bluesky-thread.txt` (5 posts, published live 2026-08-05).

| Command | Description |
|:--------|:------------|
| (see script docstring) | Post text / threads; enforces the 300-grapheme limit |

### `zenodo_broadcast.py` — Zenodo Publish Broadcast (Playbook D7, 2026-08-14)

Composes <280-char "impact copy" for a published Zenodo record and (only with an
explicit `--post` flag) dispatches to Mastodon + Bluesky:

```cmd
:: Compose only (default — no network writes)
python scripts\zenodo_broadcast.py --doi 10.5281/zenodo.21208346 --title "The Ultrametric Foundation: A Unified Thesis on Number, Time, Knowledge, and Computation"

:: Post to QNFO's OWN handles after the record is confirmed live
python scripts\zenodo_broadcast.py --doi 10.5281/zenodo.21208346 --title "..." --post
```

Rules enforced by the script (from the Zenodo Dissemination Playbook §5):
- Lead with the primary contribution; end with `https://doi.org/<doi>`.
- Exactly three hashtags; NO exclamation points / marketing jargon.
- Mastodon ≤280 chars; Bluesky ≤290 (BSKY-300-GRAPHEME-1 hard limit).
- Compose-only default = TEST-SEND-EXTERNAL-1 compliance (never test-post to
  external accounts; only QNFO-owned handles).

---

## Zenodo Publish Broadcast Workflow (D7, 2026-08-14)

Wire-in after any Zenodo record goes live (see knowledge skill v2.11 playbook D1-D7):

1. **Verify the record is live** — `zenodo_dissemination_health.py --doi <doi>`
   (knowledge skill) or a manual `https://doi.org/<doi>` check (citation_title meta present).
2. **Compose** — `python scripts\zenodo_broadcast.py --doi <doi> --title "<title>"`.
3. **Approve + post** — re-run with `--post` (QNFO-owned handles only; check the
   composed copy for length/hashtags first).
4. **Track** — thread posts must include replyTo root/parent refs
   (BSKY-300-GRAPHEME-1 case); keep broadcast ≤290 graphemes.

Cross-reference: knowledge skill v2.11 (Zenodo Dissemination Playbook),
playbook note `D:\Obsidian\notes\v1\2026\08\14\Zenodo-dissemination-playbook-2026-08-14.md`.

---

## Integration with DeepChat

### Ad-hoc Follow from a Conversation

When the agent discovers a QNFO-relevant account during research:

```python
# Bluesky
exec("python C:\\Users\\LENOVO\\.deepchat\\skills\\social-media-management\\scripts\\bluesky_follow.py follow new_researcher.bsky.social")

# Mastodon
exec("python C:\\Users\\LENOVO\\.deepchat\\skills\\social-media-management\\scripts\\mastodon_follow.py follow @new_researcher@fediscience.org")
```

### Bulk Follow All QNFO Accounts

```python
exec("python C:\\Users\\LENOVO\\.deepchat\\skills\\social-media-management\\scripts\\social_follow.py all")
```

### Dry-Run Before Following

```python
exec("python C:\\Users\\LENOVO\\.deepchat\\skills\\social-media-management\\scripts\\social_follow.py dry-run")
```

---

## Credential Management

Credentials are stored in environment variables or `.env` files. Never commit
credentials to git.

**Bluesky:**
- `BSKY_HANDLE` — your Bluesky handle
- `BSKY_APP_PASS` — app-specific password (create at bsky.app/settings/app-passwords)

**Mastodon:**
- `MASTODON_INSTANCE` — your home instance
- `MASTODON_TOKEN` — OAuth access token (set by `mastodon_follow.py auth`)
- `MASTODON_CLIENT_ID` / `MASTODON_CLIENT_SECRET` — OAuth app credentials
- Stored persistently at `~/.mastodon_creds.json`

---

## State & Idempotency

Both scripts maintain a state file to prevent duplicate follow attempts:

- Bluesky: `~/.bsky_follow_state.json`
- Mastodon: `~/.mastodon_follow_state.json`

The state file records:
- `followed`: `{handle: ISO-8601 timestamp}`
- `failed`: `{handle: error message}`

Re-running `bulk` skips already-followed accounts. Use `--reset` (not yet
implemented) or delete the state file to force re-follow.

---

## Anti-Patterns

| Anti-pattern | Correct |
|:-------------|:--------|
| Using your Bluesky account password instead of app password | Create an app password at bsky.app/settings/app-passwords |
| Running bulk without checking `dry-run` first | Always run `social_follow.py dry-run` before `all` |
| Following X/Twitter accounts via API | Not supported — removed from Basic/Pro. Manual only. |
| **LINKEDIN-MCP-NONFUNCTIONAL-1: building on linkedin-mcp-tools v2.0.3 — it NEVER worked; skill DELETED (2026-08-05)** | linkedin-mcp-tools v2.0.3 MCP server was never functional (profile dir missing, credentials absent, cookie schema inert). Skill directory DELETED from disk and git (5527b41). All surviving LinkedIn automation lives in this skill's browser-automation path. Never build an automation layer on a tool whose auth chain is unverified end-to-end. |
| **BSKY-300-GRAPHEME-1: Bluesky posts exceed the 300-grapheme hard limit (2026-08-05)** | Bluesky rejects posts over 300 graphemes with `Invalid app.bsky.feed.post record: grapheme too big (maximum 300, got N)`. This is a HARD server-side limit — the API does not truncate. Fix: keep thread posts under 300 graphemes (count characters including URLs and emoji); split long content across more thread posts. Also: thread posts MUST include the replyTo root/parent refs from post 1's uri/cid or the thread breaks. Canonical case: session 3i_KVLownViukLTZB_BJ1 — post 1 (322 chars) rejected 3x until trimmed; 5-post thread then published (DID did:plc:vad2yeqflg5uznmp557zge5c). Cross-ref: bluesky_post.py script in this skill. |
| **LINKEDIN-EXP-NO-FORM-1: LinkedIn's "Add a position or career break" button produces no modal/form via CDP (2026-08-05)** | Canonical case: session wG__dZyYtV1X4_9mgl4MW — puppeteer-core clicked `button[aria-label="Add a position or career break"]` on `/details/experience/` (confirmed via exact aria-label match). No dialog, modal, or form fields appeared — URL unchanged, `div[role="dialog"]`/`.artdeco-modal` empty. LinkedIn experience-adding requires pre-existing experience section. Profiles without a section type cannot have new sections added via CDP. Only EXISTING sections can be EDITED (About, Headline work fine). Never retry — hammering this risks account lockout. |

| Pasting `li_at` cookies expecting LinkedIn auth | linkedin-mcp-tools is DELETED. Use browser automation with an authenticated persistent Chrome profile (autocomplete selectors). |
| Hardcoding credentials in scripts | Use `.env` files or environment variables |
| Rate-limiting by guessing | Bluesky: 1.0s between follows (configurable). Mastodon: 1.5s. |
| Ignoring federated Mastodon handles | Always use full `@user@instance.tld` format for non-local accounts |
| Expecting Mastodon discovery parity with Bluesky | Mastodon discovery is instance-by-instance; Bluesky has centralized search. |

---

## Dependencies

**Zero external dependencies.** Both scripts use only Python 3.8+ stdlib:
`urllib`, `json`, `os`, `sys`, `time`, `pathlib`, `webbrowser`, `subprocess`,
`collections.defaultdict`.

No `pip install` required. Works on any Python 3.8+ installation.

---

## File Layout

```
social-media-management/
├── SKILL.md                            ← This file
├── scripts/
│   ├── bluesky_follow.py               ← Bluesky AT Protocol follow management
│   ├── bluesky_post.py                 ← Bluesky AT Protocol posting client
│   ├── discover_accounts.py            ← Taxonomy-driven account discovery
│   ├── linkedin-apply-profile.py       ← LinkedIn profile editing (CDP)
│   ├── mastodon_follow.py              ← Mastodon REST API follow management
│   ├── social_follow.py                ← Unified CLI (all platforms)
│   ├── verify_bsky_handles.py          ← Unauthenticated handle verification
│   └── zenodo_broadcast.py             ← Zenodo publish broadcast (D7, 2026-08-14)
└── references/
    ├── qnfo_accounts.json              ← Curated QNFO account registry
    ├── qnfo_taxonomy.md                ← QNFO keyword taxonomy
    ├── bluesky-thread.txt              ← Canonical Bluesky thread
    └── jpcub-thread.txt                ← JPCUB Bluesky thread
```

---

## .kaizen_history

| Date       | Version | Changes |
|:-----------|:--------|:--------|
| 2026-08-05 | v1.0.0  | Initial skill: Bluesky + Mastodon scripts, QNFO registry, unified CLI |
| 2026-08-14 | v1.7.0  | Zenodo broadcast (D7) — compose+post script, publish workflow |
| 2026-08-18 | v1.8.0  | Become-a-Node strategy + tribe map (personal alignment) |

## Become-a-Node Strategy (v1.8.0, HARD — 2026-08-18)

The QNFO tribe is scattered across boundaries (Laws of Form, cybernetics, information
science, heterodox quantum foundations). Scattered tribes find their members through
NODES, not conferences. Cadence over reach:

1. **Monthly presence** on one LoF-adjacent channel: math4wisdom seminar or
   stream.syscoi.com — the tribe assembles around regulars.
2. **D1-D7 broadcast per event** — every talk/appearance runs the Zenodo broadcast
   playbook (record -> post -> broadcast), converting one-day performances into
   permanent dissemination assets.
3. **Per-bet portfolio broadcasts** — each of the six PoC bets
   (D:\Obsidian\notes\v1\_portfolio-of-poc.md) gets zenodo_broadcast copy when a
   milestone publishes. Traction signals are EXTERNAL only — never self-referential
   engagement metrics (AI-QUALITY-GATE-1 class).
4. **Authoritative venue facts** (LoF28: 7-11 Aug 2028 Wolfson College Cambridge, no
   2027 edition; QIP27: 20-26 Feb 2027 Singapore, abstract deadline 2026-10-05;
   ASC 2027; IS4SI Summit 2027) — see durable memory f94805ee. Never re-derive venue
   claims from older memories.

Cross-reference: qnfo-core §0.8 v1.31 (tribe map), portfolio memory 1e82547d, venue
corrections f94805ee, session gtblUizh8IJisfcn-08HI.

## Version

Current: **v1.10.0** (social-media-management — UNIFIED cross-platform social hub: Bluesky/Mastodon/X/LinkedIn, Zenodo publish broadcast D7, linkedin-mcp DELETED, Buffer MCP REMOVED 2026-08-17, QNFO account registry, Become-a-Node strategy; 2026-08-18)
