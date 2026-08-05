---
name: social-media-management
version: 1.3.0
description: Programmatic social media follow management for Bluesky and Mastodon with a curated QNFO account registry covering 45+ verified researchers, journals, and institutions across four platforms. Use when the user wants to follow/unfollow accounts, bulk-follow QNFO-aligned researchers, manage social media presence, or discover accounts in quantum foundations, mathematical physics, complex systems, AI+science, and related domains. Covers Bluesky AT Protocol API, Mastodon REST API, account registry, and integration with linkedin-mcp for LinkedIn connections.
---

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
> LinkedIn: connections via linkedin-mcp-tools (5/day cap).

# SOCIAL MEDIA MANAGEMENT — v1.3.0

Programmatic social media follow management for Bluesky and Mastodon, with
a curated QNFO account registry aligned to the QWAV/QNFO research program.

---

## Platform Support Matrix

| Platform  | Follow API? | Auth Model                  | Script                | Daily Limit     |
|:----------|:------------|:----------------------------|:----------------------|:----------------|
| Bluesky   | ✅ YES      | App password (AT Protocol)  | `bluesky_follow.py`   | ~100+           |
| Mastodon  | ✅ YES      | OAuth 2.0 (REST)            | `mastodon_follow.py`  | Instance limit  |
| X/Twitter | ❌ NO       | OAuth 1.0a/2.0 (removed)    | Manual only           | N/A             |
| LinkedIn  | ⚠️ PARTIAL  | Browser profile (stealth)   | `linkedin-mcp-tools`   | 5 conns/day     |

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

## Account Registry (`references/qnfo_accounts.json`)

The registry tracks **96 QNFO-aligned accounts** across four platforms (52
Bluesky / 7 Mastodon / 27 X / 10 LinkedIn). `domain` = canonical QNFO program
code; `domain_detail` = sub-topic. All 52 Bluesky handles carry live-verified DIDs.

### Canonical QNFO Program Codes (from qnfo_taxonomy.md)

| Code | Program | Registry Coverage (2026-08-05) |
|:-----|:--------|:-------------------------------|
| `ump` | Ultrametric Physics | 3 (AMS, LMS community; individuals rare) |
| `slb` | Laws of Form | **0 accounts — OPEN GAP** |
| `inm` | Infomatics | 11 (Active Inference Institute, Seth, Allen, Preskill, Wilde…) |
| `cfe` | CFPE / Paradigm Engineering | 8 (forecasters + quantum roadmaps) |
| `res` | QNFO Research (consilience/Ruliad) | 17 (Carroll, Coecke, Virgo, Hossenfelder, NIST…) |
| `plt` | QWAV Platform (4-D + agentic AI) | 6 (Protocol Labs, Filecoin, IPFS, LangChain, HF, CF Dev) |

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
| Using `li_at` cookies for LinkedIn auth | linkedin-mcp-tools v2.0.3 uses persistent browser profiles, not cookies |
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
│   ├── mastodon_follow.py              ← Mastodon REST API follow management
│   └── social_follow.py                ← Unified CLI (all platforms)
└── references/
    └── qnfo_accounts.json              ← Curated QNFO account registry
```

---

## .kaizen_history

| Date       | Version | Changes |
|:-----------|:--------|:--------|
| 2026-08-05 | v1.0.0  | Initial skill: Bluesky + Mastodon scripts, QNFO registry, unified CLI |

## Version

Current: **v1.3.0** (social-media-management — Bluesky/Mastodon/X/LinkedIn follow management, QNFO account registry; 2026-08-05)
