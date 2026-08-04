---
name: research
version: 2.60
description: >
  End-to-end research and publication pipeline. KIF-29 Cross-Domain Consilience
  Gate upgraded from SOFT to HARD (always runs, scope-scaled, with Silo-Failure
  Detection Protocol). Canonical case: Compton-BT synthesis — five disciplines,
  one structure, 100-year missed connection. Dynamic domain selection replaces
  fixed 6-domain template. Minimum-viable-finding requirement. Gate calibration
  register added. De-bloated: 2,022 → 504 lines. Core pipeline preserved.
triggers:
  - research
  - publication
  - paper
  - literature search
  - due diligence
  - deep dive
  - paradigm forecast
  - consilience
  - cross-domain
  - silo
  - missed connection
  - isomorphism
  - Zenodo
  - PDF
  - forecast
---

# RESEARCH — v2.60

> **v2.54 UPDATE (2026-08-04, kaizen — D1 zenodo_url ownership incident):**
> Red-team: user challenge caught a blanket `zenodo_url = 'https://doi.org/'||doi`
> backfill (`WHERE doi LIKE '%zenodo%'`) creating 1,245+ rows of fake linkage when
> only ~500 QNFO-owned DOIs exist. Session dXXJ3TxRQ1VHzGdAyp-lo.
> HARD: 3. SOFT: 1. DESIGN: 1. Changes:
> (1) [HARD] **P5.OWNERSHIP gate added (BLOCKING)** — zenodo_url/zenodo_doi may ONLY
>     be written for DOIs verified QNFO-owned against the LIVE API (creator search
>     `metadata.creators.person_or_org.name:QNFO` + person-name variant
>     "Rowan Brad Quni-Gudzinas" for mis-attributed records). Never blanket-derive
>     from `doi LIKE '%zenodo%'` — it matches external citations (other researchers'
>     records in papers/paper_ids), URL-prefixed doi values (double-prefix garbage),
>     and the `PENDING-ZENODO` placeholder.
> (2) [HARD] **3 anti-pattern rows added**: ZENODO-LINK-OWNERSHIP-1 (blanket LIKE
>     backfill), ZENODO-LINK-OWNERSHIP-2 (papers/paper_ids tables contain external
>     citations — `doi LIKE '%zenodo%'` ≠ owned), NULL-ID-UPDATE-1 (keyed UPDATEs
>     skip NULL identifiers — use keyless bulk match on (doi,url)).
> (3) [HARD] **Metadata-only edit protocol CONFIRMED in-place**: edit→PUT→publish
>     keeps the SAME DOI (verified on 254 records + 18 duplicates + 50 notes-fix,
>     2026-08-04). Use it for metadata-only changes; newversion only for file changes.
> (4) [SOFT] **`scripts/zenodo-ownership-check.py` added** — D1 ↔ API ownership audit
>     (reports any zenodo_url/zenodo_doi pointing at non-QNFO DOIs).
> Cross-reference: kaizen v1.13, session dXXJ3TxRQ1VHzGdAyp-lo.

> **v2.55 UPDATE (2026-08-04, kaizen — ENFORCED BACKFILL PROTOCOL for D1 zenodo_url writes):**
> Red-team: rollback execution audit in session dXXJ3TxRQ1VHzGdAyp-lo.
> HARD: 2. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **P5.OWNERSHIP gate extended with ENFORCED BACKFILL PROTOCOL** — any bulk
>     D1 write deriving `zenodo_url`/`zenodo_doi` MUST follow: (1) PREVIEW (read-only
>     classification: owned/external/garbage counts from the live API, printed before
>     writing); (2) GATE (0 garbage AND 0 external-derived targets, else BLOCK);
>     (3) EXECUTE (keyless bulk `UPDATE ... WHERE lower(zenodo_url) IN (SELECT
>     lower('https://doi.org/'||doi) ...) AND lower(doi) NOT IN (<owned list>)`);
>     (4) VERIFY (COUNT(*) before/after equals the target; 0 rows whose zenodo_url
>     points at a non-owned DOI). D1 per-call "ok" ≠ rows changed — trust
>     `changes`/`rows_written` + COUNT(*) only.
> (2) [HARD] **2 anti-pattern rows added**: BACKFILL-PREVIEW-1 (bulk derived-value
>     UPDATE without read-only preview), D1-UPDATE-SUCCESS-NE-ROWS-CHANGED (per-call
>     "ok" treated as rows changed; NULL-key WHERE clauses no-op silently).
> (3) [SOFT] **Ownership-set completeness note**: creator search + person-name variant
>     can still miss QNFO records whose creator structure differs (e.g., 21722389/93/95
>     Counterfactual Physics / QWAV Decade / Ultrametric Consilience Atlas); augment
>     with project `.zenodo_versions.json` and paper YAML DOIs.
> Cross-reference: kaizen v1.14, session dXXJ3TxRQ1VHzGdAyp-lo.

> **v2.57 UPDATE (2026-08-04, kaizen — WBS standardization + concurrent-closeout merge):**
> Red-team: ecosystem-wide skills audit for consistent taxonomy/nomenclature
> (session dXXJ3TxRQ1VHzGdAyp-lo). HARD: 2. SOFT: 1. DESIGN: 1. This banner MERGES
> two concurrent v2.56 change-sets (this session's WBS work + session ktmz7cqk's
> closeout: BACKGROUND-TIMEOUT-1, TEMP-VOLATILITY-2, CONCURRENT-SKILL-WRITE-1,
> BUCKET-LOCKED-RESOLVE-1, DRAFT-PUBLISH-FLOW-1, SUBAGENT-DEADLINE-CROSSREF-1 —
> all anti-pattern rows present in the table below).
> Changes:
> (1) [HARD] **execute_plan rewritten with canonical WBS code prefixes** — every
>     step now starts `[{WBS}.P{N}]` per qnfo-core N-1/N-4 + WBS-AGENT-PROTOCOL.md
>     §2 (ADR-2026-007). Phases map 1:1 to WBS.TAXONOMY.md §2 (P0→P8). Previously
>     plain `Phase N:` steps violated the WBS mandate and made qnfo-core's
>     cross-ref ("research carries WBS codes in execute_plan") false.
> (2) [HARD] **WBS INTEGRATION note added to execute_plan section** — canonical
>     docs (`QNFO/wbs-6-synthesis:docs/WBS.TAXONOMY.md`, `WBS-AGENT-PROTOCOL.md`),
>     D1 program_registry resolution rule, phase-number mapping.
> (3) [SOFT] **Anti-pattern rows added** — WBS-STD-1 (plan steps without WBS code
>     prefix) + WBS-STD-2 (cross-ref claiming WBS usage that doesn't exist).
> (4) [DESIGN] **Nomenclature standardization**: version header delimiter
>     normalized to `# RESEARCH — vX.Y` (em-dash); mixed `--`/`—`/`(vN.M)`
>     delimiters across the ecosystem flagged for owning skills (cloudflare,
>     system, knowledge use `--`).
> Cross-reference: qnfo-core N-1/N-4/N-5, kaizen v1.14, WBS.TAXONOMY.md,
> WBS-AGENT-PROTOCOL.md, sessions dXXJ3TxRQ1VHzGdAyp-lo + ktmz7cqk.

> **v2.51 UPDATE (2026-08-03, kaizen — PDF quality enforcement):**
> Trigger: user permanent deprecation of xhtml2pdf + Page.printToPDF (session SHEfIEGiQvA2LI5xAPkon).
> Both papers published with Helvetica-only ReportLab PDFs (zero rendered math). User required
> LaTeX-quality typesetting, perfect math rendering, cross-format, cross-platform.
> Changes:
> (1) [HARD] **PDF Building section rewritten** — xhtml2pdf fallback code block permanently removed.
>     HARD gate: no Chromium binary = BLOCK publication. Never fall back to substandard renderers.
> (2) [HARD] **MathJax SVG mandate** — tex-svg-full.js required (CHTML PUA glyphs don't survive CDP).
> (3) [HARD] **Source delimiter mandate** — $...$ not \(...\) (pandoc strips escaped parens).
> (4) [HARD] **Anti-pattern rewritten** — "Extract cached Chromium zips first" replaces xhtml2pdf fallback.
> Cross-reference: session SHEfIEGiQvA2LI5xAPkon, odr-thesis v0.8-mathjax-svg.

> **v2.50 UPDATE (2026-08-03, kaizen — Zenodo API diagnostics + metadata fix):**
> Trigger: `ZENODO_TOKEN` diagnosed as "403 token scope problem" for 6+ hours while
> the real issue was the decommissioned `/api/deposit/depositions` endpoint (HTTP 404
> after InvenioRDM migration). Token confirmed WORKING via `GET /api/user` → 200.
> Session SHEfIEGiQvA2LI5xAPkon.
> Changes:
> (1) [HARD] **ZENODO-API-INVENIORDM table added** — maps all 6 decommissioned
>     `/api/deposit` endpoints to their InvenioRDM replacements (`/api/records`).
> (2) [HARD] **Credential Protocol rewritten** — `zenodo-token-check.py` is now
>     MANDATORY before diagnosing any auth failure; the protocol distinguishes token
>     validity (GET /api/user → 200), endpoint reachability (GET /api/records → 200),
>     and Content-Type requirements (415) before reaching any conclusion.
> (3) [HARD] **Common Error Signatures expanded** with InvenioRDM-specific entries:
>     POST 404 (decommissioned endpoint), POST 415 (missing Content-Type), DELETE 204
>     (zero-length body).
> (4) [HARD] **Anti-pattern row added** — "Diagnosing every Zenodo 403/404 as token
>     scope problem" — with the zenodo-token-check.py workflow.
> (5) [SOFT] **`scripts/zenodo-token-check.py` created** — the previously non-existent
>     script now exists at the referenced path. Validates token, endpoint, headers.
> Cross-reference: qnfo-core v1.7, kaizen v1.9, session SHEfIEGiQvA2LI5xAPkon.

> **v2.49 UPDATE (2026-08-03, kaizen — bibliographic fabrication prevention):**
> Red-team: direct parent-agent 5-adversary audit of odr-thesis Phases 0-3 (session SHEfIEGiQvA2LI5xAPkon).
> HARD: 9. SOFT: 10. DESIGN: 1. Trigger: standing directive — "hallucinated authors or fabricated
> data/information is an automatic red-team audit and kaizen update of affected skills."
> Incident: `references.bib` contained fabricated author lists (C4: 3 hallucinated authors;
> C5: wrong list) and wrong DOIs (S2, S3 pointed at unrelated papers).
> Changes:
> (1) [HARD] **P3.AUTHOR-GATE added to Phase 3** — every BibTeX entry verified against live
>     Crossref/OpenAlex before commit; DOI resolved title must match entry title;
>     HTML-redirect responses disqualify "auto-generated" claims; no unread tool-output claims.
> (2) [HARD] **5 anti-pattern rows** (CITING-1..5): unverified author lists, wrong-paper DOIs,
>     phantom auto-generation, phantom validation, silent merge duplicates.
> (3) [SOFT] Canonical incident documented in P3.AUTHOR-GATE for cross-skill discoverability.
> Cross-reference: qnfo-core v1.7 (§0.0 Proprietary Nomenclature Integrity), qnfo-core v1.5 (§0.0 Bibliographic Integrity), kaizen v1.8,
> session SHEfIEGiQvA2LI5xAPkon, odr-thesis tag v0.5-redteam-fix.

> **v2.48 UPDATE (2026-08-03, kaizen — ODR v3.0 publication forensics):**
> Red-team: direct parent-agent 5-adversary audit of session R8ZWb04K4BHAldwEqCX4b.
> HARD: 4. SOFT: 1. DESIGN: 0.
> Root incident: ODR v3.0 publication pipeline produced a duplicate Zenodo deposit (21761802)
> and the canonical record (21758752) embedded stale YAML (`doi: TBD`, `status: draft`).
> User challenge forced forensic diff: documents differ by 9 bytes (YAML-only).
> Changes:
> (1) [HARD] **R1 — 3 Zenodo error signatures added to Common Error Signatures**:
>     (a) **ZENODO-SEARCH-FN: search-API false negative** — `GET /api/records?q=<slug>`
>         OR-tokenizes unquoted queries and misses live records. ALWAYS follow search
>         with direct `GET /api/records/{id}` before concluding "record not found."
>     (b) **ZENODO-DUP-1: duplicate deposit created when YAML already has live DOI**
>         — paper YAML `doi:` field exists and resolves → use `actions/newversion`,
>         NEVER create a fresh deposit. P5.DUPCHECK gate added (BLOCKING).
>     (c) **ZENODO-PUB-1: published-record deletion attempted** — published Zenodo
>         records CANNOT be deleted via API. Use `isObsoletedBy` in related_identifiers
>         to mark superseded, or delete the duplicate via the Zenodo web UI.
> (2) [HARD] **R2 — Post-publish embedded-YAML freshness gate (P5.FRESH)**:
>     After Zenodo publish, download the deposit `.md` file and assert `doi:` ≠ TBD
>     AND `status:` = "published" in the YAML frontmatter. Case: 21758752 had stale
>     YAML while R2 held the corrected version — the deposit's OWN embedded markdown
>     was wrong. This gate catches it.
> (3) [HARD] **R3 — SCS-1 cross-reference**: competing D1 write scripts targeting same
>     row → race-dependent outcome. One D1 write target, one approach. After write,
>     re-read AND content-verify. Anti-pattern row added.
> (4) [SOFT] **R4 — Version sync note**: after publish, verify D1 `version` matches
>     Zenodo metadata `version` in `.zenodo_versions.json`.
> (5) [HARD] **R5 — Token retrieval note**: `ZENODO_TOKEN` always retrievable via
>     `wmic process call create` shortcut; never declare a token-blocker without
>     trying the wmic route.
> Cross-reference: kaizen v1.8, cloudflare v3.21, session R8ZWb04K4BHAldwEqCX4b,
> ODR v3.0 (DOI 10.5281/zenodo.21758752).

> **v2.47 UPDATE (2026-08-02, kaizen — PDF fallback + Zenodo hardening):**
> Red-team: direct parent-agent audit (no subagents, per HARD GATE). HARD: 0. SOFT: 3. DESIGN: 1.
> (1) [SOFT] PDF fallback pipeline documented (pandoc→HTML→xhtml2pdf) for when build-pdf-pro.py
>     times out on puppeteer bootstrap. Validated on 6 papers (ACRP-06,07,08,09, PERR, Consilient Synth v2.1).
> (2) [SOFT] Zenodo API error signatures expanded: DELETE 204, newversion draft-conflict,
>     metadata partial-update rejection. Fixes documented in Common Error Signatures table.
> (3) [SOFT] Pandoc canonical path documented: C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe
>     (not on PATH — reference full path in build scripts).
> (4) [DESIGN] Zenodo anti-patterns added to research skill from kaizen v1.6 for
>     cross-skill discoverability.
> 
> (6) [HARD] **PDF Building section rewritten (v2.55)** — complete Chrome for Testing
>     procurement via Python urllib (puppeteer install hangs). MathJax CDN unreachable from
>     Chrome headless — must download locally + inline via str.replace() (NOT re.sub).
>     5-step pipeline: procure Chrome → pandoc HTML → switch SVG → inline MathJax → CDP PDF.
> (7) [HARD] **ZENODO-API-INVENIORDM corrections** — `/actions/newversion` → HTTP 404
>     (decommissioned). Use `POST /api/records/{id}/draft` (HTTP 201). Token validation:
>     `/api/me` (HTTP 200), NOT `/api/user` (HTTP 404). Publish: `POST /draft/actions/publish`.
> (8) [SOFT] **10 new anti-patterns** — CHROME-PROCURE-1, MATHJAX-CDN-HEADLESS-1,
>     RE-SUB-ESCAPE-1, ZENODO-NEWVERSION-404, ZENODO-USER-404, ZENODO-BUCKET-LOCKED-1,
>     NODE-EVAL-CMD-1, PYTHON-C-AMPERSAND-1, PANDOC-PATH-CMD-QUOTES-1.
> (9) [SOFT] **Corrected credential endpoint** — `GET /api/me` replaces `GET /api/user`
>     throughout the InvenioRDM table and credential protocol.
> (10) [SOFT] **Render script pattern** included — complete puppeteer-core ESM `.mjs`
>     render script with MathJax diagnostics, error fallback, and size verification.

Cross-reference: kaizen v1.6, session 3bPo9XqsLFBBGRz0xT4HB.

> **v2.46 UPDATE (2026-08-02, kaizen — KIF-29 SOFT→HARD + Silo-Failure Detection):**
> Red-team: 5-adversary audit. HARD: 3 (KIF-29 upgrade, Silo-Failure Detection, dynamic domains).
> SOFT: 3 (minimum-viable-finding, gate calibration, execute_plan update). DESIGN: 2 (canonical case, silo-cost metric).
> Canonical case: Compton-BT — five disciplines discovered the same combinatorial-tree-with-cross-ratios
> structure over 100+ years and never connected. 66-110yr gaps per domain pair.
>
> This de-bloated version (v2.46) collapses 22 version banners into 1, removes references to 5 deleted
> scripts, merges 4 duplicate Anti-Phantom Gate sections into 1 umbrella, retires historical XeLaTeX
> pipeline descriptions, moves the Zenodo Data Dictionary to a reference file, and trims anti-patterns
> to the last 12 months. Legacy material → HISTORY.md. Full v2.45 archive: `deploy/history/research-v2.45-archive.md`.
>
> **Bloat removed:** 22 version banners (~400 lines), 5 deleted-script references, 3 duplicate mandates,
> historical pipelines, 37-field Zenodo dictionary → `references/zenodo-deposit-schema.json`.
> **Net:** 2,022 lines → ~900 lines (55% reduction). Core pipeline preserved. v2.46 changes preserved.

## execute_plan

**WBS INTEGRATION (v2.56, HARD):** Every `update_plan` step carries a canonical
WBS code prefix `[{WBS}.P{N}]` (per qnfo-core N-1/N-4 + WBS-AGENT-PROTOCOL.md §2,
ADR-2026-007). Resolve the project's WBS code from D1 `program_registry` (or the
WBS.TAXONOMY.md registry) BEFORE executing; never invent codes. Phase numbers map
1:1 to WBS.TAXONOMY.md §2 (P0 Init → P8 Core Distribution). Canonical docs:
`QNFO/wbs-6-synthesis:docs/WBS.TAXONOMY.md` + `docs/WBS-AGENT-PROTOCOL.md`.

update_plan([
  {"step": "[{WBS}.P0] Init: repo scaffold, WBS code resolution, README, PROJECT-PLAN.md, core claim lock", "status": "pending"},
  {"step": "[{WBS}.P0] Pre-Flight: run P1-P11 checklist — HARD gates must pass before Phase 1", "status": "pending"},
  {"step": "[{WBS}.P1] Due diligence: KG + D1 + Vectorize + external cross-ref", "status": "pending"},
  {"step": "[{WBS}.P1] Consilience gate (KIF-29 HARD): cross-domain lexicon + silo-cost table + synthesis", "status": "pending"},
  {"step": "[{WBS}.P2] Literature: 8 parallel sources, dedup, classify, Mandatory Symmetry Template (KIF-18)", "status": "pending"},
  {"step": "[{WBS}.P3] Citations: extract, verify BibTeX (P3.AUTHOR-GATE), auto-generate missing DOIs", "status": "pending"},
  {"step": "[{WBS}.P4] Research: Structured Forecast Protocol (11 stages) + red-team + calibration", "status": "pending"},
  {"step": "[{WBS}.P5] Publish: paper.md + PDF (build-pdf-pro.py) + BP-1→BP-10 gates + Zenodo DOI", "status": "pending"},
  {"step": "[{WBS}.P6] Deploy: D1 living-paper, papers-server Worker, MCP-driven verification", "status": "pending"},
  {"step": "[{WBS}.P7] Disseminate: SEO, Buffer social, papers.qnfo.org, Internet Archive", "status": "pending"},
  {"step": "[{WBS}.P8] Distribute: GitHub tag, Zenodo newversion, R2 archive, D1/KG records, BP-4/5 corrections", "status": "pending"},
])

**Note:** Phase 0 and Pre-Flight apply to net-new, long-lived projects. Single-paper updates skip to Phase 1.

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — UNIVERSAL, MANDATORY)

**No remote publication action — Zenodo deposit, GitHub push/tag/release, R2 upload, D1 insert, OSF
registration, Buffer post — may be reported as successful without an INDEPENDENT re-query of the live
state in the SAME turn.** An API's `201 Created` is the FIRST signal, not the LAST.

1. **Zenodo** — verify via `curl -sI https://doi.org/10.5281/zenodo.<id>` (HTTP 200), not the API response alone.
2. **Git push** — verify via `git ls-remote origin <branch>` or GitHub API, not local exit code.
3. **R2 upload** — download back and compare size/hash.
4. **D1/KG inserts** — re-run SELECT/neighbors query and show the row/edge present.
5. **Buffer** — confirm post ID in response; for queue state, verify counts after.
6. **If live re-verification cannot run in this turn**, response MUST read `[NOT-VERIFIED: reason]`.

**Cross-phase references:** All per-phase verification sections (Zenodo §5, D1 §6, Buffer §7, Core §8)
delegate to this umbrella mandate — the rule is the same, the tool is what changes.

---

## Cross-Skill Integration Checklist

| Skill | Load at Phase | Purpose |
|:------|:-------------|:--------|
| `git-github` | 0 (init), every closeout | Branch discipline, conventional commits, repo creation |
| `knowledge` | 0 (KG seed), 1 (DD), every closeout | KG queries, D1 cross-reference, project state logging |
| `cloudflare` | 6 (deployment), 8 (distribution) | R2 archive, D1 insert, Worker verification, MCP-driven check |
| `qnfo-core` | All phases | Research integrity, banned words, Ostrowski mandate, mojibake scan |
| `knowledge` | 0, every closeout | Durable memory logging |
| `documents` / `pdf` | 5 (publication) | PDF building, document formatting |
| `skill-creator` | 5 (publication) | For skill_file generation if needed |

---

## Phase 0: Project Initialization (BLOCKING GATE for new projects)

**HARD GATE:** Phase 1 MUST NOT begin until all Phase 0 deliverables committed.

### 0.1 Repository

**PROJECT BRANCH POLICY (HARD GATE):** NEVER create a new repository for a single paper or project. All QNFO research work lives as **branches** inside the consolidated program repos in `QNFO/`. Use the routing table from the git-github skill ($Project Branch Policy) to select the correct program repo for the project's domain.

**Workflow:**
1. Clone the appropriate program repo: `git clone https://github.com/QNFO/<program>.git`
2. Resolve WBS program code from qnfo-core §N-1 (canonical: `UMP`, `SLB`, `INM`, `CFE`, `RES`, `PLT`, `DEM` + existing `ADL`, `CON`, `SR`)
3. Create a branch using `{prog}/{type}/{canonical-slug}`: `git checkout -b ump/paper/<slug>`
4. Scaffold: `mkdir -p <slug>/docs <slug>/artifacts <slug>/notebooks <slug>/releases`
5. Create `PROJECT-PLAN.md` at `<slug>/PROJECT-PLAN.md` (not at repo root). First line MUST carry the WBS code: `# WBS: {PORTFOLIO}.{PROG}.{NNN}`

**Program repo routing with WBS codes (canonical):**

| WBS Code | Research Domain | Program Repo | Branch Prefix |
|:---------|:----------------|:-------------|:--------------|
| `UMP` | Ultrametric / p-adic / adelic physics | `QNFO/ultrametric-physics` | `ump/` |
| `SLB` | Laws of Form / Spencer-Brown | `QNFO/laws-of-form` | `slb/` |
| `INM` | Infomatics / information-as-fundamental | `QNFO/infomatics` | `inm/` |
| `CFE` | CFPE / paradigm forecasting | `QNFO/cfpe` | `cfe/` |
| `RES` | General QNFO research / audits | `QNFO/qnfo-research` | `res/` |

**REPO-TARGET GATE (HARD):** `git remote -v` before every tag/commit/release — confirm target is a QNFO program repo, NEVER `QNFO/qnfo-skills` (ADR-026).

### 0.2 Project Plan

`PROJECT-PLAN.md` with: Charter, Phases with WBS, Milestones with gate criteria, Deliverable Registry, Risk Register, Success Criteria.

### 0.3 Closeout

Phase Closeout Protocol: commit → credential-scan → tag → push → verify → log to memory. Tag: `v0.1-phase0`.

---

## Pre-Flight Checklist (P1-P11, HARD gates before Phase 1)

| ID | Check | Gate |
|:---|:------|:-----|
| P1 | Branch created in correct program repo; `{type}/{slug}` convention | HARD |
| P2 | GitHub remote configured and pushed | HARD |
| P3 | Directory structure: docs/ artifacts/ notebooks/ releases/ | HARD |
| P4 | PROJECT-PLAN.md with charter, WBS, milestones | HARD |
| P5 | README.md with overview | SOFT |
| P6 | Core claim reformulated and locked (§1.2) | HARD |
| P7 | .gitignore present | SOFT |
| P8 | Phase 0 committed, tagged, and pushed | HARD |
| P9 | Project logged to KG / memory | SOFT |
| P10 | Cross-skill integration checklist reviewed | SOFT |
| P11 | OSF project (MAJOR projects only) | SOFT-CONDITIONAL |

**If any HARD gate fails:** BLOCK. Fix and re-run.

---

## Phase 1: Due Diligence — Cross-Reference Discovery

### (a) QNFO Cross-Reference
- `query_graph({endpoint: "stats"})` for ecosystem overview
- `query_graph({endpoint: "nodes", params: {label: "Paper", search: "<topic>"}})` for existing papers
- `search_papers({query: "<topic>", limit: 10})` via Vectorize
- Report: "QNFO Cross-Reference: Found N related papers"

### (b) External Literature Search (MANDATORY)
Query 8 sources: OpenAlex (PRIMARY), Crossref, Zenodo records, Europe PMC, arXiv, web search, QNFO Vectorize, QNFO KG. Deduplicate. Save evidence to `artifacts/external-search/`.

**Rate-Limit Matrix:** OpenAlex/Croesref/Zenodo/Europe PMC all keyless, HTTP 200 verified. Semantic Scholar retired (429). Polite-pool with `mailto`, ~0.4s between queries. Exact-phrase searches for novelty claims — unquoted Zenodo `q=` OR-tokenizes.

**Evidence discipline:** Save every API response; cite file for every count/DOI. Never report a count without its evidence file.

### (c) Gap Analysis
Which aspects covered by QNFO? What prior work to build on? Is the proposed research genuinely novel?

**Vectorize Confirmation-Bias Disclosure:** If ALL hits are QNFO-internal, flag `[CONFIRMATION-BIAS-RISK]` — distinguish internal from external corroboration.

### Institutional Status Neutrality Gate (KIF-16, HARD)
Strip institutional metadata. Never use "fringe"/"pseudoscience" — use epistemic categories: `[UNFALSIFIABLE]`, `[CONTRADICTS ESTABLISHED EVIDENCE]`, `[UNTESTED]`, `[CONTESTED]`.

### AI Convergence Bias Disclosure (KIF-17, HARD when triggered)
If 2+ AI evaluations converge on dismissing a claim → flag `[AI-CONVERGENCE-WARNING]`. AI convergence reflects shared training-data priors, not independent validation.

---

## Phase 1b: Cross-Domain Consilience & Silo-Failure Detection Gate (KIF-29, HARD)

**Trigger: ALWAYS runs during Phase 1. Scope scales to project size.**

**GATE (HARD, MANDATORY):** Phase 1 MUST produce:

1. **Cross-Domain Lexicon** — dynamic domain selection from Phase 1 due diligence evidence (3-6 domains); fallback to Physics/CS/InfoTheory/Biology/Sociology template only if no evidence available. Explicitly state why each domain was chosen with evidence citations.

2. **Minimum-Viable-Finding** — at least one non-trivial structural isomorphism per domain checked, OR an explicit reasoned statement why none exists (with specific, verifiable reasoning — generic "not applicable" is REJECTED).

3. **Silo Cost Table** (see Silo-Failure Detection Protocol below).

4. **Synthesis Consilience** — one meta-principle (what is invariant across all translations) and one Frontier Question.

**Why this gate is HARD:** The Compton-BT synthesis (2026-08-02) is the canonical case. Five independent disciplines — mathematical physics, quantum foundations, number theory, computer science, information theory — each discovered the same combinatorial-tree-with-cross-ratios structure between 1916 and 1980, called it by five different names, and spent 78-110 years never connecting them. The prior SOFT trigger ("run when research spans 2+ domains") was circular: it only executed when the agent ALREADY knew the work was cross-domain, and silo blindness prevents that knowledge.

**Gate check:** If no consilience audit record exists in `artifacts/consilience-gate.md` with the Silo Cost table → Phase 1 is INCOMPLETE. HARD BLOCK on Phase 2.

### Silo-Failure Detection Protocol (mandatory sub-protocol)

For each domain identified in the consilience translation:
1. **Earliest Discovery:** What year? Cite key paper.
2. **Cross-Domain Connection:** What year was this connected to other domains?
3. **Silo Cost (years):** Earliest discovery − connection year.
4. **Silo Name:** What did THIS domain call the structure?

**Template:**

| Domain | Structure Name | Earliest | Connected | Silo Cost | Key Paper |
|:-------|:---------------|:---------|:----------|:----------|:----------|
| {domain} | {name} | {year} | {year/NEVER} | {gap} | {DOI} |

**Canonical Case — Compton-BT:**

| Domain | Structure Name | Earliest | Silo Cost | Key Paper |
|:-------|:---------------|:---------|:----------|:----------|
| Number Theory | Ostrowski completions | 1916 | **110 yr** | Ostrowski, Acta Math 1916 |
| Quantum Foundations | Zitterbewegung/Compton | 1928 | **98 yr** | Dirac, Proc. Roy. Soc. A 1928 |
| Information Theory | Dimensionless entropy | 1948 | **78 yr** | Shannon, BSTJ 1948 |
| Computer Science | Radix tree / trie | 1960 | **66 yr** | Fredkin, 1960 |
| Mathematical Physics | Bruhat–Tits tree | 1980s | **~40 yr** | Vladimirov–Volovich, 1994 |

If silo cost > 50yr: flag `[SILO-FAILURE: >50yr gap — this synthesis rectifies multi-generational knowledge fragmentation]`.

### Gate Calibration Register

```
[CHECK: 2027] All post-gate QNFO papers must have consilience audit records.
Strength: [WEAK] | Status: [PENDING]
---
[CHECK: 2028] Compton-BT must be the LAST "accidental" cross-domain discovery.
Strength: [STRONG] | Status: [PENDING]
---
[CHECK: 2030] ≥1 external citation of a QNFO consilience finding as bridging
two previously separate domains.
Strength: [WEAK] | Status: [PENDING]
```

### Integration with later phases

| Phase | Integration |
|:------|:------------|
| Phase 2 | Translated Lexicon terms → parallel search queries in each domain |
| Phase 4 | Synthesis Consilience → Stage 1 candidate; Frontier Question → Stage 5 calibration |
| Phase 5 | Cross-Domain Lexicon table is publication-ready |

---

## Phase 2: Literature Search & Triage

### Multi-Source Search (8 sources in parallel)

| Source | Method | Purpose |
|:-------|:-------|:--------|
| **OpenAlex** | `api.openalex.org/works?search=<q>&mailto=<email>` (NO KEY) | PRIMARY academic index |
| **Crossref** | `api.crossref.org/works?query=<q>&mailto=<email>` (NO KEY) | DOI registry |
| **Zenodo records** | `zenodo.org/api/records?q=<q>` (NO KEY) | Search ALL deposits |
| **Europe PMC** | `ebi.ac.uk/europepmc/webservices/rest/search?query=<q>` (NO KEY) | Life sciences |
| **arXiv** | `export.arxiv.org/api/query?search_query=<q>` | Preprint search |
| **Web** | Browser or curl | Broader discovery |
| **QNFO Vectorize** | `search_papers({query: "..."})` | Internal corpus |
| **QNFO KG** | `query_graph('nodes', {label: "Paper", search: "..."})` | Internal concepts |

**Evidence discipline:** Save every response to `artifacts/external-search/<api>_<query>.json`.

### Classification Matrix

| Class | Definition | Min | Max | Action |
|:------|:-----------|:----|:----|:-------|
| Core | Directly addresses RQ | 5 | 10 | Deep read, extract citations |
| Supporting | Adjacent work | 10 | 20 | Read abstract + methods |
| Background | Context, foundations | 5 | 15 | Skim, note for bibliography |
| Reject | Irrelevant, retracted | — | — | Archive with reason |

### Mandatory Symmetry Template (KIF-18, HARD)

Every literature review MUST include BOTH:
```markdown
## Where External Literature Supports [Claim]

[Enumerate specific papers with DOIs.]

## Where External Literature Constrains or Contradicts [Claim]

[MUST NOT be empty or contain only hedging language. Name specific
constraining evidence or explicitly state [NO CONSTRAINING EVIDENCE FOUND].]
```

**GATE:** Missing either section → BLOCKED.

---

## Phase 3: Citation Management

Extract citations from markdown (Pandoc `@key`, numeric `[1]`, LaTeX `\cite{key}`). Cross-reference against `.bib` file. Flag missing, unused, malformed entries. Auto-generate missing BibTeX from DOIs via `doi.org/<DOI>` (Accept: application/x-bibtex). Audit report.

### P3.AUTHOR-GATE (HARD — v2.49, bibliographic fabrication prevention)

**Every BibTeX entry's author list, title, journal, volume, year, and DOI MUST be verified
against live Crossref (`api.crossref.org/works/<doi>`) or OpenAlex metadata BEFORE the
entry is committed.** Hand-constructed entries without live verification are FABRICATION
RISK — author names and DOIs are the two most commonly hallucinated fields.

**Canonical incident (2026-08-03, odr-thesis red-team v1):** `references.bib` contained
fabricated author lists for C4 ("Gao, Ping; S.~Ning; Watanabe, Hikaru" — all hallucinated)
and C5 ("Bhattacharyya, Chen, Hung, Liu" — real: Hung, Li, Melby-Thompson), plus wrong
DOIs (S3 pointed at Guo & Lin "BGK Waves"; S2 pointed at Postma "electroweak baryogenesis").

1. **Verify EVERY author list** — never trust a recalled or LLM-suggested author list.
   `curl -s https://api.crossref.org/works/<url-encoded-doi>` → parse `message.author[].given/family`.
   Mismatch → BLOCKED.
2. **Verify every DOI resolves to the CORRECT paper** — HTTP 200 is not enough; the
   resolved title must MATCH the entry title. `doi.org/<DOI>` HEAD 200 ≠ correct DOI.
3. **Never claim "auto-generated from DOI" when the endpoint returned an HTML redirect** —
   `curl -H "Accept: application/x-bibtex" https://doi.org/<DOI>` frequently returns an
   HTML Handle Redirect page, not BibTeX. If the response starts with `<html`, the
   auto-generation FAILED — construct the entry manually from Crossref/OpenAlex metadata
   and VERIFY it per rules 1-2.
4. **Never claim validation tool output without reading it** — if `biber` / `bibtexparser`
   is not installed, say so. "0 errors, 0 warnings" must come from an actual run.
5. **After any `.bib` merge or append, re-run duplicate-key detection** — `copy /b file1+file2`
   can double entries silently (odr-thesis incident: 11 duplicate keys).
6. **Zero fabricated entries** per qnfo-core §0.0: a fabricated author or DOI is a
   research-integrity violation, not a citation error.

Output: `artifacts/citation-audit.md` — entry count, verification method per entry,
DOI-resolution evidence, duplicate check.

---

## Phase 4: Deep Research & Structured Forecast (MANDATORY for all projects)

**Scope scales to project size.** Single-result paper: assumptions enumerated, uncertainty ranges, sensitivity check, ≥1 calibration prediction. Paradigm forecast: full 11-stage protocol.

**PUBLICATION PRINCIPLE:** Do NOT name the methodology in research outputs. Bury the method in the prose — "Underlying this candidate are three critical assumptions" not "Stage 2 Assumption Audit found."

**METHODOLOGY NOTE:** This is a structured judgment exercise, NOT a Bayesian computation. Qualitative ranking with uncertainty ranges and reference-class anchors. No false-precision EV numbers.

### Stage -1: Likelihood Calibration Protocol (HARD GATE)

Every P(E|H) > 0.80 must trace to an empirical calibration pillar (Empirical Base Rate, Reference-Class Forecast, Calibrated Subjective, Inter-Rater Reliability, Known Prior). Unanchored likelihoods capped at 0.80 with `[CALIBRATION-CAP]`. Run calibration training (≥20-question quiz, Brier score). Reviewer subagent independently assigns every assumption. Output: `artifacts/likelihood-calibration.md`.

### Stages 0-8: Full Protocol (scope-scaled)

0. **Domain Assessment** — map field, active paradigms, key questions.
1. **Paradigm-Shift Candidates** — qualitative ranking, impact/timeline/testability/dependency.
2. **Assumption Audit** — enabling assumptions, blocking assumptions, dependency chain.
3. **Red-Team Challenge** — 5 adversary positions (Null-Hypothesis Defender, Methodology Skeptic, Better-Alternative Proposer, Scaling Pessimist, Resource Realist).
4. **Judgment Sensitivity** — pessimistic/optimistic/halved-priors ranking, ROBUST/CONDITIONAL/FRAGILE statement.
5. **Calibration Register** — dated, strength-weighted predictions `[CHECK: 2030]` with likelihood-anchor provenance.
6. **Research Effort Allocation** — qualitative-rank-based effort distribution, 10% hedge floor.
7. **Strategic Memo** — executive summary, key findings, risk assessment.
8. **Cross-Review** — same-model subagent consistency check, blind-spot identification.

### Stage 9: Practical Applications Extension (MANDATORY)

Map each forecast candidate onto 2-5 concrete application domains. Operational signature per candidate-domain pair. Domain-specific falsifiable claims. Additional calibration register entries.

### Stage 10: Counterfactual Backcasting (MANDATORY)

Systematic backcasting across target disciplines with tiered forks (Tier 1: ~20yr, Tier 2: ~60yr, Tier 3: ~120yr, Tier 4: alternate axioms). Counterfactual technology stack table. Backcast calibration register entries. Near-term fork recommendations → Future Work.

**Forecast Integration Map:** All Stage outputs feed into Phases 1-8. Forecasting is the analytical engine generating the paper's claims. See Forecast Integration Map in HISTORY.md for the full cross-reference table.

---

## Phase 5: Publication Pipeline

### Pre-Publication Requirements

**BP-1 Fit-Verify Gate (HARD):** Independent Python recomputation verifying every claimed numerical value. Discrepancy > 0.01% → BLOCKED. Output: `artifacts/fit-verify.txt`.

**BP-2 Terminology Audit Gate (HARD):** Every field-specific term → check standard definition. Mismatch → BLOCKED. Output: `artifacts/terminology-audit.md`.

**BP-3 Density Gate (HARD):** When claiming "set S approximates values V to ε%" and S is dense in ℝ⁺, null model with pre-registered tolerance required. p_global > 0.05 → `[CONSISTENT WITH LOOK-ELSEWHERE ARTIFACT]`.

**BP-4 Cross-Paper Numerical Consistency (HARD):** Same number in multiple QNFO papers must agree within rounding.

**BP-5 Overdetermined System Gate (HARD):** N fitted ratios from M<N independent quantities → closure error must be computed.

**BP-6 Derived-Quantity Recompute (HARD):** Every derived quantity recomputed from first principles.

**BP-7 Sigma/Error Propagation (HARD):** Every σ traces to specific uncertainty source with documented propagation.

**BP-8 Numerology Claim Classification (DESIGN):** 5-class typology (Dense-Approximant, Ratio-Factorization, Index-Selection, Transcendental, Pattern-in-Noise) with per-class required gates.

**BP-9 Audit-the-Auditor (SOFT):** Audit papers self-audit via BP-1 through BP-7 before publication.

**BP-10 Independent-Recompute (HARD):** Before citing any paper's numerical claim, recompute it independently.

### Numeracy Red Flags Checklist

Quick-scan: 0 🚩 → proceed. 1-2 🚩 → investigate. 3+ 🚩 → HARD BLOCK.

### YAML Frontmatter (MANDATORY)
```yaml
---
title: "Paper Title"
author: "Author Name"
date: "YYYY-MM-DD"
license: "QNFO Unified License Agreement (QNFO-ULA)"
doi: "10.5281/zenodo/XXXXXXXXX"
status: "draft" | "published"
---
```

### Publication Language Gate (BLOCKING)
Scan for: internal language, credential leaks, bare Unicode math, AI-generated filler phrases. Run `scan-mojibake.py` (qnfo-core §0.2). Run credential scan.

### Physics Writing Standards
All 18 points from qnfo-core §7. Minimum: certainty calibration, falsifiability conditions, banned-word enforcement.

### Professional Publication Standards (HARD GATE)
Structural: Title, Abstract (150-250 words), Keywords (4-6), Introduction, Body, Conclusion, Declarations (9 subsections), Bibliography. Tone: formal third-person, no hedging filler, no contractions, no rhetorical questions. Copyediting: zero spelling errors, consistent hyphenation, curly quotes, every acronym defined, every figure captioned, no orphaned headers.

### Ostrowski Dimensionless Mandate (HARD)
ALL physics formulas in dimensionless Planck units (ℏ=c=G=kB=1). Dimensional formulas must include dimensionless equivalent + Ostrowski rationale. Cross-reference: qnfo-core §0.7.

### Source File Encoding Integrity (HARD, KIF-28)
Zero BOM, zero U+FFFD, zero U+FFFF in all source files. All Python: `encoding='utf-8'` explicit. Pre-commit scan mandatory.

### PDF Building (v2.55, HARD GATE — NO FALLBACK TO SUBSTANDARD RENDERERS)

**CANONICAL PIPELINE:** pandoc (--mathjax) → MathJax SVG switch → MathJax local download + inline → puppeteer-core CDP PDF render. TeX Live uninstalled (2026-08-02). xhtml2pdf and Page.printToPDF permanently deprecated (2026-08-03). MathJax MUST use SVG output processor (`tex-svg-full.js`), NOT CHTML (`tex-chtml-full.js`) — CHTML uses Private Use Area glyphs that do not survive CDP capture.

**HARD GATE — NO CHROMIUM = NO PDF (BLOCK):** If no Chromium binary exists anywhere on the system: **BLOCK the publication.** Do not publish with any substandard PDF renderer. Report: `[BLOCKED: no Chromium binary available for CDP PDF pipeline]`. In practice, always procure Chrome for Testing (see below).

#### Step 1: Procure Chrome for Testing (MANDATORY when no system Chromium exists)

This machine has NO pre-installed Chromium. Chrome for Testing must be downloaded manually. **Do NOT use `npx puppeteer browsers install` or `@puppeteer/browsers` install() — both hang indefinitely on this machine.** Use Python urllib instead:

```python
# dl_chrome.py — write to %TEMP%, run with python
import urllib.request, zipfile, os

cache_dir = os.path.join(os.environ["USERPROFILE"], ".cache", "puppeteer", "chrome")
os.makedirs(cache_dir, exist_ok=True)

# Discover latest version from Google Chrome Labs API:
# https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
# Or use a known-good version:
version = "153.0.7989.0"
url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/win64/chrome-win64.zip"
zip_path = os.path.join(cache_dir, f"chrome-{version}.zip")

urllib.request.urlretrieve(url, zip_path)  # ~194 MB, 2-5 minutes

with zipfile.ZipFile(zip_path, 'r') as zf:
    zf.extractall(cache_dir)

# Result: %USERPROFILE%\.cache\puppeteer\chrome\chrome-win64\chrome.exe
```

Launch puppeteer-core with:
```js
const chromeExe = `${os.homedir()}/.cache/puppeteer/chrome/chrome-win64/chrome.exe`;
const browser = await puppeteer.launch({
    executablePath: chromeExe,
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
});
```

#### Step 2: Build HTML with pandoc

```bash
C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe --mathjax --standalone <slug>.md -o <slug>.html
```

**Source delimiters (2026-08-03):** source markdown MUST use `$...$` / `$$...$$` delimiters, NOT `\(...\)` / `\[...\]`. Pandoc's default reader treats `\(` as an escaped paren and STRIPS the LaTeX. If source has `\(`, convert first: `re.sub(r'\\\\((.*?)\\\)', r'$\1$', source)`.

#### Step 3: Switch MathJax from CHTML to SVG

pandoc `--mathjax` emits `tex-chtml-full.js`. CHTML uses Private Use Area glyphs that do not survive CDP capture. Switch to SVG:

```python
# switch_svg.py
html = open(html_path, 'r', encoding='utf-8').read()
html = html.replace('tex-chtml-full.js', 'tex-svg-full.js')
open(html_path, 'w', encoding='utf-8').write(html)
```

#### Step 4: Download MathJax locally and inline (CRITICAL — CDN UNREACHABLE)

The MathJax CDN (`cdn.jsdelivr.net`) is UNREACHABLE from Chrome headless on this machine. The HTML `page.goto()` with `networkidle0` will hang forever waiting for the CDN. **MathJax must be downloaded locally AND inlined into the HTML.**

```python
# fix_mathjax.py — download MathJax and inline into both HTMLs
import urllib.request, os, re

cdn_url = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg-full.js"
local_dir = os.path.join(os.environ["TEMP"], "mathjax")
os.makedirs(local_dir, exist_ok=True)
local_path = os.path.join(local_dir, "tex-svg-full.js")
urllib.request.urlretrieve(cdn_url, local_path)  # ~2.2 MB

# Read MathJax JS
with open(local_path, 'r', encoding='utf-8') as f:
    mathjax_js = f.read()

# Inline into each HTML
for html_name in ['paper1.html', 'paper2.html']:
    html_path = os.path.join(os.environ['TEMP'], html_name)
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find the MathJax script tag (split across lines in pandoc output)
    matches = list(re.finditer(r'<script[^>]*tex-svg[^>]*>[^<]*</script>', html))
    if not matches:
        raise RuntimeError(f"No MathJax script tag found in {html_name}")
    
    full_match = matches[0].group(0)
    inline_tag = f'<script>{mathjax_js}</script>'
    
    # IMPORTANT: use str.replace() NOT re.sub() — MathJax JS contains \u escape
    # sequences that crash Python's re.sub(). str.replace() handles these fine.
    html = html.replace(full_match, inline_tag)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Inlined MathJax into {html_name}: {len(html)} chars')
```

**CRITICAL:** Use `str.replace(full_match, inline_tag)`, NOT `re.sub()` — MathJax JS contains `\uXXXX` escape sequences that crash `re.sub()` with "bad escape \u at position N".

#### Step 5: Render PDF via puppeteer-core CDP

**Always write Node scripts to `.mjs` files — `node -e` fails in cmd.exe with "Unterminated string constant" when code contains quotes or line breaks.**

```js
// render_pdf.mjs — use with: node render_pdf.mjs
import { existsSync, statSync } from 'fs';
import { resolve } from 'path';
import os from 'os';
import puppeteer from 'puppeteer-core';

const chromeExe = `${os.homedir()}/.cache/puppeteer/chrome/chrome-win64/chrome.exe`;
const tmp = process.env.TEMP || os.tmpdir();

async function render(htmlName, pdfName) {
    const htmlFile = resolve(tmp, htmlName);
    const pdfFile = resolve(tmp, pdfName);
    
    if (!existsSync(htmlFile)) throw new Error(`HTML not found: ${htmlFile}`);
    
    const browser = await puppeteer.launch({
        executablePath: chromeExe,
        headless: true,
        args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
    });
    
    try {
        const page = await browser.newPage();
        const fileUrl = 'file:///' + htmlFile.replace(/\\/g, '/');
        
        await page.goto(fileUrl, { waitUntil: 'load', timeout: 120000 });
        
        // Wait for MathJax to render (inline JS, no CDN dependency)
        const mjStatus = await page.evaluate(() => {
            if (typeof window.MathJax === 'undefined') return 'MathJax undefined';
            if (window.MathJax.startup && window.MathJax.startup.promise)
                return 'MathJax has startup.promise';
            return 'MathJax exists but no startup';
        });
        console.log('MathJax status:', mjStatus);
        
        try {
            await page.evaluate(() => window.MathJax.startup.promise);
            console.log('MathJax rendered successfully');
        } catch (e) {
            console.log('MathJax render error:', e.message.substring(0, 200));
        }
        
        const mathCount = await page.evaluate(() =>
            document.querySelectorAll('mjx-container, .MathJax, mjx-assistive-mml').length
        );
        console.log('Rendered math elements:', mathCount);
        
        await new Promise(r => setTimeout(r, 3000));  // extra settle time
        
        await page.pdf({
            path: pdfFile,
            format: 'A4',
            printBackground: true,
            margin: { top: '2cm', bottom: '2cm', left: '2cm', right: '2cm' }
        });
        
        const size = statSync(pdfFile).size;
        console.log(`PDF: ${(size/1024).toFixed(1)} KB, math=${mathCount}`);
        return size >= 102400;  // HARD GATE: <100KB = substandard renderer
    } finally {
        await browser.close();
    }
}

// Render both papers
const results = [
    await render('paper1.html', 'paper1.pdf'),
    await render('paper2.html', 'paper2.pdf'),
];
console.log('PDF build complete:', results.every(r => r) ? 'ALL OK' : 'SOME FAILED');
```

**Mandatory verification:** Zero U+FFFD, PDF size > 100KB (xhtml2pdf output is typically < 40KB — this gate catches accidental fallback). **Math expressions MUST be visually verified** — if math is missing or rendered as bare text, the SVG switch, source delimiters, or inline MathJax need fixing.

**Canonical incident (2026-08-04, session ktmz7cqk):** Multiple PDF rendering failures traced to:
1. No Chromium on system — no Edge, no Chrome, no Brave installed
2. `npx @puppeteer/browsers install chrome` hung indefinitely (installed version but never returned)
3. MathJax CDN unreachable from Chrome headless — `page.goto` with `networkidle0` hung waiting for CDN fetch
4. `node -e` failed with "Unterminated string constant" in cmd.exe for multi-line render script
5. `re.sub()` crashed on MathJax JS containing `\u` escape sequences — must use `str.replace()`

All five failures would repeat for any agent on this machine. This section now documents the complete working pipeline end-to-end.


### Zenodo Upload

**Credential Protocol:** Never hardcode or retype tokens. Reference live environment variable. Run `scripts/zenodo-token-check.py` on ANY auth failure (403, 404, 415). The script validates (a) token existence, (b) token validity via `GET /api/me` (NOT `/api/user` — returns 404 in InvenioRDM), (c) InvenioRDM endpoint reachability via `GET /api/records`, and (d) Content-Type header requirements before diagnosing the root cause. Never diagnose "403 = token scope" without running the checker first — InvenioRDM migrates old endpoints to 404, which some clients report as 403. [HARD — v2.50, session SHEfIEGiQvA2LI5xAPkon: quasiparticle extension paper blocked 6+ hours because 403 was diagnosed as "token scope" when the real issue was decommissioned endpoint 404.]

**ZENODO-API-INVENIORDM (v2.50, HARD):** Zenodo migrated to InvenioRDM. The old `GET /api/deposit/depositions` endpoint returns HTTP 404 (decommissioned). Use:

| Old (decommissioned) | New (InvenioRDM) | Verified |
|:---------------------|:-----------------|:---------|
| `POST /api/deposit/depositions` | `POST /api/records` | ✅ |
| `GET /api/deposit/depositions?q=<query>` | `GET /api/records?q=<query>` | ✅ |
| `PUT /api/deposit/depositions/{id}` | `PUT /api/records/{id}/draft` | ✅ |
| `POST /api/deposit/depositions/{id}/actions/publish` | `POST /api/records/{id}/draft/actions/publish` | ✅ |
| `POST /api/deposit/depositions/{id}/actions/newversion` | `POST /api/records/{id}/draft` | ✅ (v2.55 — HTTP 201 creates draft edit) |
| `PUT /api/files/{bucket}/{filename}` | `PUT /api/records/{id}/draft/files/{filename}` | ✅ |
| File upload Content-Type | `application/octet-stream` (mandatory) | ✅ |
| Token validation | `GET /api/me` (HTTP 200) — NOT `/api/user` (HTTP 404) | ✅ |
| Newversion (Obsolete) | `/actions/newversion` returns **HTTP 404** — decommissioned entirely. Use `POST /api/records/{id}/draft` instead. | ✅ |

**PRE-CHECK:** Before publishing, search for existing records: `GET /api/records?q=<title>`. If a draft exists: `GET /api/user/records?q=<title>&status=draft`. Deduplicate per P5.DUPCHECK.

**Upload order (PREVIEW-FIRST):** `<slug>.pdf` → `README.md` → `<slug>.md` → `PROVENANCE-BUNDLE.zip` → remaining files. BUCKET URL RULE: upload to `{links.bucket}/{filename}`, never construct URL manually.

**Metadata:** Data dictionary → `references/zenodo-deposit-schema.json`. Templates: Variant A (fresh), Variant B (newversion). Checklist before PUT: title matches YAML, upload_type set, keywords is JSON array, related_identifiers include isNewVersionOf+isSupplementedBy.

**REQUESTS MANDATE (v2.53, HARD — urllib drops DELETE/PUT, use requests instead):** ALL Zenodo API calls that use non-GET methods (DELETE, PUT) MUST use the `requests` library, NOT `urllib.request`. Python's `urllib.request.Request(method="DELETE")` silently drops the method and sends GET — confirmed in session zESRNRQLF76EBvTbldEev (2026-08-04) where every Zenodo 403 was caused by DELETE being sent as GET hitting read-protected draft file endpoints. The `requests` library handles all methods correctly:
- `requests.delete(url, headers=h)` — correct DELETE
- `requests.put(url, headers=h, data=binary)` — correct PUT
- `requests.post(url, headers=h, json=data)` — correct POST
- `requests.get(url, headers=h)` — correct GET
Never use `urllib.request.Request(method="DELETE")` for any Zenodo operation.
**Protocol (APT-1):** When ANY Zenodo API call returns 403/404/401 unexpectedly, run the API-Failure Self-Diagnosis Protocol from windows-command-patterns S-1.0.6 (STOP -> VERIFY -> COMPARE -> FIX -> THEN-diagnose). Do NOT blame token scope, rate limits, or WAF — verify your code's HTTP method first. Cross-ref: kaizen BLAME-EXTERNAL-1.

**ZENODO-EDIT-DRAFT PROTOCOL (v2.53, HARD - updating a PUBLISHED record):** Zenodo does NOT
allow in-place file replacement on a published record's edit draft ("Bucket is locked for
modifications"). To update a published paper:
1. **PREFERRED: newversion** - `POST /api/records/{id}/versions` creates a fresh deposit
   with an UNLOCKED bucket. Upload files (create -> put content -> commit), then publish.
   The parent DOI automatically resolves to the newversion. VERIFIED 2026-08-04 on
   frequency-valuation-theory (21778603 -> 21782835), ODR thesis, consilient-gap-synthesis.
2. **NOT PREFERRED: edit draft** - `POST /api/records/{id}/draft` succeeds (201) but the
   inherited bucket stays LOCKED, so DELETE/upload return 403 "Bucket is locked for
   modifications". Only metadata-only edits (no file changes) work this way.
Use the `requests` library for all calls (see REQUESTS MANDATE above). Never urllib.
Cross-ref: windows-command-patterns S-1.0.5/S-1.0.6, kaizen BLAME-EXTERNAL-1.


**CREATOR FORMAT (v2.52, HARD — corrected 2026-08-03):**
- **Personal creator:** `{"person_or_org": {"family_name": "LastName", "given_name": "FirstName", "type": "personal"}}`
- **Organizational creator:** `{"person_or_org": {"name": "OrgName", "type": "organizational"}}` — DO NOT use `family_name`/`given_name` for organizational creators. The `name` field is the ONLY valid identifier for organizations. Using `family_name` for an organization produces "Name cannot be blank" on publish.
- **ALL metadata fields are required on PUT** — InvenioRDM validates the FULL metadata object, not just changed fields. A partial PUT (e.g., only `creators`) clears `title`, `publication_date`, and `resource_type` — causing multi-field validation failures on publish. Always include the complete metadata object: `title`, `publication_date`, `resource_type`, and `creators` at minimum.

**Publish → Verify:** `curl -sI https://doi.org/10.5281/zenodo/{id}` → HTTP 200. `.zenodo_versions.json` tracking.

**P5.FRESH — Post-publish embedded-YAML freshness gate (v2.48, HARD):**
After Zenodo publish, download the deposit's `.md` file and verify its YAML frontmatter:
1. `curl -s https://zenodo.org/api/records/{id}/files/<slug>.md/content` → read YAML
2. Assert `doi:` field ≠ `TBD` / `null` / placeholder
3. Assert `status:` field = `"published"` (not `"draft"`)
4. If verification fails: re-upload corrected `.md` + re-publish (or newversion)
**Case:** ODR v3.0 canonical record 21758752 had `doi: TBD` and `status: draft` in its embedded `.md` while R2 held the corrected version — the deposit's OWN embedded markdown was stale. This gate catches that before closeout.

**Versioning:** Use `actions/newversion` for same-concept updates. Never create disconnected new deposit for same project.

**HARD GATES:**
- **P5.OWNERSHIP (v2.54, BLOCKING):** Before writing `zenodo_url`/`zenodo_doi` to D1
  (`papers` or `paper_ids`), verify the target DOI is QNFO-owned against the LIVE API.
  Build the owned-DOI set from BOTH `metadata.creators.person_or_org.name:QNFO` AND the
  person-name variant `"Rowan Brad Quni-Gudzinas"` (mis-attributed records are invisible
  to the QNFO creator search — Adelic Shannon chain 21698550/21698976/21710934).
  NEVER blanket-derive `zenodo_url = 'https://doi.org/'||doi WHERE doi LIKE '%zenodo%'`
  — `papers`/`paper_ids` contain EXTERNAL citations (other researchers' Zenodo records),
  URL-prefixed doi values (→ double-prefix garbage), and the `PENDING-ZENODO` placeholder.
  After any backfill, re-verify: 0 rows whose zenodo_url points at a non-owned DOI.
  **Canonical incident (2026-08-04):** blanket backfill created 1,245+ fake links
  (225 papers + 219 paper_ids external citations; 8 double-prefix/PENDING garbage).
  Rollback: papers 503→277, paper_ids 468→248. See ZENODO-LINK-OWNERSHIP-1/2,
  NULL-ID-UPDATE-1 anti-patterns.
  **ENFORCED BACKFILL PROTOCOL (v2.55):** any bulk D1 write that DERIVES
  `zenodo_url`/`zenodo_doi` MUST follow:
  (1) **PREVIEW** — read-only classification pass building the owned-DOI set from
      the live API (creator search + person-name variant + project
      `.zenodo_versions.json` / paper YAML DOIs) and printing owned/external/garbage
      counts + sample rows BEFORE any write;
  (2) **GATE** — 0 garbage AND 0 external-derived targets, else BLOCK the write;
  (3) **EXECUTE** — keyless bulk
      `UPDATE ... WHERE lower(zenodo_url) IN (SELECT lower('https://doi.org/'||doi)
      FROM <t> WHERE doi IS NOT NULL) AND lower(COALESCE(doi,'')) NOT IN (<owned list>)`;
  (4) **VERIFY** — COUNT(*) before/after equals the target; 0 rows whose zenodo_url
      points at a non-owned DOI; inspect response meta `changes`/`rows_written`.
  D1 per-call "ok" ≠ rows changed (NULL-key WHERE clauses no-op silently) — trust
  `changes`/`rows_written` + COUNT(*) only. Cross-ref: kaizen BACKFILL-PREVIEW-1,
  D1-UPDATE-SUCCESS-NE-ROWS-CHANGED.
- **P5.DUPCHECK (v2.48):** Before ANY Zenodo deposit, check paper YAML frontmatter for a `doi:` field. If present AND resolves to HTTP 200 → paper already has a canonical Zenodo record. Use `actions/newversion` on the existing deposit; NEVER create a fresh deposit. Also check `GET /api/records?q=<title>` for unsubmitted drafts before newversion. If YAML `doi:` is non-null and resolves → fresh-deposit is BLOCKED.
- **P5.PDF (KIF-30):** Every deposit must include individual PDFs. Markdown-only = INCOMPLETE.
- **P5.IDENTITY (KIF-58):** Title + DOI + GitHub repo identity verified before upload.
- **P5.CLEAN (v2.45):** After newversion, DELETE all stale files before uploading fresh ones.

### Common Error Signatures

| Error | Root Cause | Fix |
|:------|:-----------|:----|
| `resource_type: Missing data` | upload_type not set | Set upload_type top-level |
| `resource_type: Not a valid string` | Nested object on newversion | Use string fields |
| `keywords` 400 | Comma-joined, not array | Wrap in `[...]` |
| `newversion` 400 `files.enabled` | Draft already exists | Follow `links.latest_draft` |
| Upload 415 | Missing Content-Type | `Content-Type: application/octet-stream` |
| DELETE returns 204 No Content | Zenodo DELETE file returns zero-length body | Check `len(response) == 0` before `json.loads()`; return `{}` for empty bodies |
| `newversion` 400 `files.enabled` (stale draft) | Existing draft from prior failed publish has stale files | Search drafts via `GET /deposit/depositions?q=<title>&status=draft`, find match, DELETE files, re-upload, PUBLISH |
| Metadata PUT 400 `resource_type`/`creators` | Metadata PUT is FULL replacement, not merge | Always include minimum: `upload_type`, `publication_type`, `creators` |
| **POST /api/records 404 (v2.50)** | Decommissioned endpoint — old `/api/deposit` prefix is GONE in InvenioRDM | Use `POST /api/records` with `Content-Type: application/json`; verify via `GET /api/user` (200 = token works, 404 = endpoint decommissioned) |
| **POST /api/records 415 (v2.50)** | Missing `Content-Type: application/json` | Add `Content-Type: application/json` header — InvenioRDM requires it explicitly for JSON payloads |
| **DELETE file 204 (v2.47)** | Zenodo returns zero-length body on file DELETE | Check `len(response) == 0` before `json.loads()`; return `{}` for empty bodies |

---

## Phase 6: Cloudflare Deployment

### D1 Access
Canonical: `cloudflare/scripts/d1-query.py`. CHECK-THEN-WRITE pattern (never combined upsert on FTS5 tables). Column is `body_md`. Verify via independent re-query.

### Papers-Server Verification
`curl -sI https://papers.qnfo.org/papers/<slug>/` → HTTP 200.

### R2 Archive
Upload `<slug>.md`, `<slug>.pdf` to `qnfo-releases/releases/<YYYY>/<MM>/<slug>/`.

### MCP-Driven Deployment Verification (HARD)
Cross-MCP chain: cloudflare-builds → cloudflare-observability → cloudflare-bindings → cloudflare-auditlogs. All must pass before declaring deployment complete.

---

## Phase 7: Dissemination

### SEO Audit
robots.txt, sitemap.xml, llms.txt, meta tags, Schema.org ScholarlyArticle, Open Graph.

### Buffer Social Media
Canonical: `api.buffer.com/graphql`, `createPost` mutation. ALWAYS discover channel IDs live. 401 diagnostic protocol before "stale token" diagnosis. Inline fragments on PostActionPayload work. `LimitReachedError` = account queue cap, not agent bug.

### IPFS/DNSLink (OPTIONAL)
Cloudflare R2 (durable store) + locally-computed CIDv1 + Cloudflare DNS DNSLink. NO third-party pinning services.

### Internet Archive
`https://web.archive.org/save/https://papers.qnfo.org/papers/<slug>`

---

## Phase 8: Core Distribution Stack (MANDATORY)

All 4 layers verified before status → "published":

| Layer | Implementation | Verification |
|:------|:--------------|:-------------|
| GitHub | Public repo, tags, releases | `git tag -l`, `gh release view` |
| Zenodo | DOI with versioned deposits | `curl -sI https://doi.org/<doi>` |
| R2 | Canonical file archive | `npx wrangler r2 object get ... --remote` |
| D1/KG | Living-paper DB + KG node | `get_paper_context`, `query_graph('neighbors')` |

**BP-4 Correction-on-Discovery:** GitHub ERRATA.md → Zenodo newversion + `obsoletes` → KG CORRECTS/SUPERSEDES edge.

---

## Verification Gates

| Gate | Check | Evidence |
|:-----|:------|:---------|
| Due Diligence | KG + D1 + 2+ external sources | Query outputs |
| Consilience (HARD) | artifacts/consilience-gate.md with Silo Cost table | File present |
| Classification | All papers classified | Table |
| Citation | BibTeX verified | Audit output |
| Publication Language | Zero internal language, zero banned words | Scan: 0 hits |
| PDF | Renders without errors | build-pdf-pro.py exit 0 |
| DOI | Zenodo resolves, preview is PDF | curl HTTP 200 |
| Deployment | papers-server 200, D1 entry exists | curl + d1-query |
| SEO | robots.txt, sitemap, meta tags | Verify each URL |
| Social | Buffer posts confirmed | Post ID in response |
| Core Distribution | All 4 layers verified | All pass |
| Practical Applications | artifacts/practical-applications-extension.md | File present |
| Counterfactual Backcasting | artifacts/counterfactual-backcasting.md | File present |

---

## Anti-Patterns (trimmed to 2025-2026)

| Anti-Pattern | Fix |
|:-------------|:----|
| Searching only one source | Query all 8 in parallel |
| Inventing citations | All citations → real papers with DOIs |
| Skipping dedup | Run dedup, report counts |
| No falsifiability | Every speculative claim: "disconfirmed if..." |
| Hardcoding API tokens | Store path, read live |
| python -c "..." inline on Windows | write .py → exec → delete |
| PowerShell curl alias (Invoke-WebRequest) | Use curl.exe explicitly. PowerShell is DELETED. |
| Obsidian/external paths silently skipped | Document, ask user to copy in |
| Generic paper.md naming | Use <slug>.md |
| Temp directory assumed to identify project | Read YAML title: + doi: first |
| Zenodo without retry | 3x exponential backoff; recover drafts |
| **Classifying research "single-domain" without Consilience Gate** | Gate IS the check — always run Quick Scan |
| **Cargo-cult [NOT-APPLICABLE] without specific reasoning** | ≥1 isomorphism or explicit reasoned denial |
| **Fixed 6-domain template on every project** | Dynamic domain selection from Phase 1 evidence |
| **Skipping Silo Cost for multi-domain synthesis** | Compute temporal gap. >50yr → [SILO-FAILURE] |
| **No calibration register for the gate** | Add dated predictions [2027/2028/2030] |
| `actions/newversion` assumes clean draft | DELETE all files first (GATE P5.CLEAN) |
| Zenodo unsubmitted draft check skipped | Pre-check API before every publish |
| D1 slug drift after rename | Verify slug matches after BP-2 corrections |
| Cross-paper numerical inconsistency | BP-4: reconcile before publish |
| Unreproducible headline sigma | BP-7: trace every σ to specific source |
| Derived quantity not recomputed | BP-6: recompute from first principles |
| Density gate for one claim but not identical sibling | BP-8: classify all claims uniformly |
| **Assuming `pandoc` is on PATH — binary at `C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe`** | Reference full path or prepend to PATH in all build scripts |
| **Assuming `build-pdf-pro.py` always works — puppeteer bootstrap times out** | DO NOT fall back to xhtml2pdf or Page.printToPDF. Extract cached Chromium zips first (they're pre-downloaded in `~/.cache/puppeteer/chrome/`), or use system Chromium (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`). Only if no Chromium binary exists anywhere: BLOCK the publication — DO NOT publish with substandard renderers. |
| **Zenodo DELETE — assuming JSON response body** | Handle HTTP 204: check `len(content) == 0` before `json.loads()` |
| **Zenodo `actions/newversion` — assuming clean draft** | Search for existing drafts first; delete stale files; then upload |
| **Zenodo metadata PUT — partial update** | Always include `upload_type`, `publication_type`, `creators` in metadata PUT |
| **ZENODO-SEARCH-FN: Search API false negative — `GET /api/records?q=<slug>` misses live records (2026-08-03)** | Zenodo `q=` OR-tokenizes unquoted queries. `GET /api/records?q=odr-v3` → `hits=0` while `GET /api/records/21758752` → 200. ALWAYS follow a negative search with direct record-ID GET before concluding "not found." Case: session R8ZWb04K, search missed canonical record 21758752 → pipeline created duplicate 21761802. |
| **ZENODO-DUP-1: Duplicate deposit created when paper YAML already has live DOI (2026-08-03)** | Before ANY deposit, check paper YAML `doi:` field. If present AND resolves → use `actions/newversion`, NEVER create fresh deposit. P5.DUPCHECK gate (HARD). Case: ODR v3.0 YAML had `doi: 10.5281/zenodo.21758752` (live) but pipeline created fresh 21761802. |
| **ZENODO-PUB-1: Attempting to delete published Zenodo record via API (2026-08-03)** | Published records CANNOT be deleted via REST API. Mitigation: add `isObsoletedBy` → canonical DOI, mark title `[SUPERSEDED]`, queue UI deletion. Never waste API calls on published-record deletion. |
| **SCS-1: Competing D1 write scripts targeting same row — race-dependent outcome (2026-08-03)** | One D1 write target, one approach. If a backup script fails, DELETE it immediately. Never leave competing scripts alive. After any D1 write: re-read AND content-verify the row contains the INTENDED content, not just "update succeeded." Cross-reference: kaizen v1.2.5. Case: session R8ZWb04K, two D1 write scripts ran concurrently — truncated version won because full version hit wrong DB UUID. |
| **Version drift between D1 and Zenodo metadata after publish** | After publish, verify D1 `version` column matches Zenodo metadata version in `.zenodo_versions.json`. Publish ≠ D1 is automatically current. Case: ODR v3.0 D1 had v1.8 but Zenodo metadata said v1.0. |
| **Declaring ZENODO_TOKEN unreachable without trying wmic** | `ZENODO_TOKEN` is always retrievable via `wmic process call create` shortcut in a Python subprocess. Never declare a token-blocker without attempting the wmic route first. |
| **Diagnosing every Zenodo 403/404 as "token scope problem" (2026-08-03)** | IMPORTANT: Run `scripts/zenodo-token-check.py` FIRST before diagnosing. Confirm (a) `GET /api/user` → 200 = token works; (b) `GET /api/records` → 200 = InvenioRDM reachable. If token works and endpoint works, the issue is Content-Type (415) or endpoint URL (404 on decommissioned paths). Case: odr-quasiparticle-extension blocked 6+ hours in session SHEfIEGiQvA2LI5xAPkon — 403 diagnosed as scope, real issue was `/api/deposit/depositions` 404 (decommissioned in InvenioRDM migration). ZENODO-API-INVENIORDM table (v2.50) maps all old → new endpoints. |
| **CITING-1: Hand-writing BibTeX author lists without live verification (2026-08-03)** | Author lists are hallucination-prone. Verify EVERY entry against `api.crossref.org/works/<doi>` before commit (P3.AUTHOR-GATE, HARD). Case: odr-thesis C4 had 3 fabricated authors ("Gao, Ping; S.~Ning; Watanabe, Hikaru"); C5 had wrong list (real: Hung, Li, Melby-Thompson). |
| **CITING-2: DOI points to WRONG paper — 200 OK ≠ correct DOI (2026-08-03)** | `doi.org/<DOI>` HEAD 200 only proves the DOI exists. Verify the resolved title MATCHES the entry title. Case: odr-thesis S3 used 10.1007/s00220-017-2873-2 (Guo & Lin "BGK Waves") for Gubser's p-Adic AdS/CFT (correct: 10.1007/s00220-016-2813-6); S2 used 10.1007/jhep09(2021)055 (Postma "baryogenesis") for Bending-the-BT-tree (correct: 10.1007/jhep09(2021)097). |
| **CITING-3: Claiming "auto-generated BibTeX from DOI" when endpoint returned HTML (2026-08-03)** | `curl -H "Accept: application/x-bibtex" doi.org/<DOI>` returns an HTML Handle Redirect page, not BibTeX, unless redirects are followed. If response starts with `<html`, auto-generation FAILED — construct manually from Crossref/OpenAlex and verify per P3.AUTHOR-GATE. Never claim auto-generation that did not occur. |
| **CITING-4: Claiming validation results from a tool that is not installed (2026-08-03)** | "biber: 0 errors, 0 warnings" was claimed while `biber` is not installed. Report actual tool output; say "not installed — skipped" when the tool is absent. |
| **CITING-5: Silent duplicate BibTeX keys after file merge (2026-08-03)** | `copy /b references.bib + part2.bib` appended entries that already existed → 11 duplicate keys broke the bibliography. After ANY .bib merge/append, run duplicate-key detection (regex `@\w+\{([^,]+),` + Counter). |
| **ACRONYM-1: Expanding a proper name or project slug into a fabricated acronym (2026-08-03 — ODR → "Ontological Distribution of Reality" same class as QNFO → "Quantum Number Field Ontology")** | **HARD GATE (qnfo-core §0.0 Proprietary Nomenclature Integrity v1.7):** QNFO ecosystem names (QNFO, ODR, QWAV) are proper names, NOT acronyms. Never expand them. Any expansion without explicit user confirmation is a fabrication — identical in kind to hallucinated authors or fabricated DOIs. Case: ODR thesis 90-message pipeline (session SHEfIEGiQvA2LI5xAPkon) — the Zenodo records were clean but the agent's internal language fabricated the expansion. |
| **ZENODO-LINK-OWNERSHIP-1: Blanket-deriving `zenodo_url` from `doi LIKE '%zenodo%'` (2026-08-04)** | **HARD GATE (P5.OWNERSHIP):** `zenodo_url = 'https://doi.org/'||doi WHERE doi LIKE '%zenodo%'` mints fake QNFO linkage for EXTERNAL citations, URL-prefixed doi values, and placeholders. Only ~500 QNFO-owned DOIs exist; the blanket backfill claimed 1,245+ rows. Fix: build the owned-DOI set from the live API (creator search + person-name variant) and write links ONLY for owned DOIs; re-verify 0 non-owned links after any backfill. Case: session dXXJ3TxRQ1VHzGdAyp-lo — 225 papers + 219 paper_ids fake links, rollback 503→277 / 468→248. |
| **ZENODO-LINK-OWNERSHIP-2: Assuming `doi LIKE '%zenodo%'` means "QNFO-owned record" (2026-08-04)** | D1 `papers` and `paper_ids` tables contain EXTERNAL literature citations (other researchers' Zenodo records ingested from external-search) alongside QNFO publications. A zenodo-pattern DOI ≠ QNFO-owned. Always confirm ownership per-DOI via the live API before treating a row as QNFO-published. |
| **NULL-ID-UPDATE-1: Keyed UPDATEs skip rows with NULL identifiers — under-clearing data (2026-08-04)** | `UPDATE ... WHERE identifier = ?1` never matches rows where identifier IS NULL. Rollback passes 1-2 skipped 58 papers rows this way. Fix: use keyless bulk `UPDATE ... WHERE lower(zenodo_url) IN (SELECT lower('https://doi.org/'||doi) ...) AND lower(doi) NOT IN (<owned list>)`, or handle NULL keys explicitly via a fallback column (`id`). Verify final counts match the target, not just "N ok" from keyed loops. |
| **BACKFILL-PREVIEW-1: Executing a bulk derived-value D1 UPDATE without a read-only classification preview (2026-08-04)** | Any bulk write that DERIVES values (e.g., `zenodo_url = 'https://doi.org/'||doi`) MUST first run a read-only classification pass (owned/external/garbage counts from the live API, printed BEFORE any write) and gate the write on it (0 garbage, 0 external). The 2026-08-04 backfill went straight to UPDATE → 1,245+ fake links (225 papers + 219 paper_ids external citations, 8 double-prefix/PENDING garbage). Rollback papers 503→277, paper_ids 468→248 succeeded because it previewed first. See P5.OWNERSHIP ENFORCED BACKFILL PROTOCOL. |
| **D1-UPDATE-SUCCESS-NE-ROWS-CHANGED: Treating per-call UPDATE "ok" as rows actually changed (2026-08-04)** | D1 returns success for UPDATE calls that matched 0 rows (NULL-key WHERE no-op). Rollback reported "385 ok, 0 failed" while papers only dropped 503→341 (162/226 targets changed). Fix: after any bulk D1 write verify COUNT(*) before/after against the exact target AND inspect response meta `changes`/`rows_written`; use keyless bulk matching on (doi,url) instead of keyed passes. |
| **WBS-STD-1: update_plan steps without a canonical WBS code prefix (2026-08-04)** | Every plan step MUST start with `[{WBS}.P{N}]` (qnfo-core N-1/N-4, WBS-AGENT-PROTOCOL.md §2, ADR-2026-007). Plain `Phase N:` steps break cross-session continuity, dependency tracking, and auditability. Fix: resolve the WBS code from D1 `program_registry` (or WBS.TAXONOMY.md) and prefix every step. Case: research v2.55 execute_plan had no WBS codes despite qnfo-core claiming it did. |
| **WBS-STD-2: Cross-reference claims WBS usage that does not exist (2026-08-04)** | A skill's cross-ref "research (phases carry WBS codes in execute_plan)" was FALSE — research had plain Phase steps. Cross-refs to a standard must be verified against the target skill's actual content (read the file) before being written; phantom compliance claims are the same class as phantom validation claims. Fix: verify target content before writing the cross-ref; kaizen Watchtower should audit WBS cross-refs. |
| **PHASE0-EMPTY-REPO: `git subtree add` on a new program repo without a bootstrap commit — v2.59, 2026-08-04** | A brand-new program repo created via `gh repo create <name> --public` has NO commits and NO HEAD. `git subtree add` requires an existing commit to merge into → all subtree adds fail silently. **Fix:** Clone with `gh repo create --add-readme` (creates a bootstrap commit on main) OR clone → write README → commit → rename branch to main → push BEFORE any subtree operations. Canonical case: session PMH0kzte — consolidate.py v1 subtree-added 12 repos into a new-empty ultrametric-physics repo; all 12 failed silently because HEAD didn't exist. See git-github skill SUBTREE-NO-HEAD anti-pattern.

| **BACKGROUND-TIMEOUT-1: Foreground exec of long-running command (Chrome download, MathJax CDP render, pandas HTML) times out at 600s max (2026-08-04)** | `exec` has a 600s (10min) maximum timeout including `background: true` tasks that auto-cancel. Chrome download (~194 MB) takes 2-5 min; CDP PDF render with MathJax takes 30-90s. Always use `background: true` for downloads > 30s. Use `process poll` to check status; do NOT assume `exec` returning a sessionId means the task completed. Kill hung processes early (2 polls with no progress = stuck) and retry with a different approach. Canonical case: session ktmz7cqk — 3 hung background Chrome installs, 2 hung CDP renders. |
| **TEMP-VOLATILITY-2: Published paper files in %TEMP% evicted between authoring and PDF build phases (2026-08-04)** | Files written to `%TEMP%` during the authoring phase (step N) are GONE by the PDF-build phase (step N+1). Windows cleans temp directories between long-running agent turns. **Re-clone repos from GitHub after every phase transition.** Never assume a `%TEMP%` file written in an earlier phase is still there. Canonical case: session ktmz7cqk — both `_26216024446.md` (136KB) and `_26216024519.md` (10KB) evicted; odr-thesis-v2.md and quasipaper-v2.md also evicted. Git is the persistence layer, not temp. Cross-reference: git-github TEMP Volatility HARD GATE. |
| **CONCURRENT-SKILL-WRITE-1: Two processes (agent + automated system) writing the same SKILL.md simultaneously (2026-08-04)** | A skill file can be modified by an automated pipeline (e.g., kaizen Watchtower, scheduled backfill) while the current session is also editing it. Symptom: version string changed to unexpected content between writes. Fix: (A) read→edit→write in a SINGLE atomic Python script (not read tool + edit tool + write tool); (B) after every write, immediately re-read the skill file to verify YOUR content landed; (C) if content was overwritten, re-read the current state and re-apply. Canonical case: research SKILL.md v2.54→v2.55 — version string overwritten by backfill protocol update between write and verification. |
| **BUCKET-LOCKED-RESOLVE-1: Zenodo draft bucket returns 403 "Bucket is locked" on DELETE after POST /draft (2026-08-04)** | Deletion of old files from a newly-drafted record may be denied. Two-tier resolution: (A) upload new files with the SAME key — `PUT /api/records/{id}/draft/files/{filename}` overwrites existing files atomically, no DELETE needed; (B) if overwrite also returns 403, wait 30-60 seconds for the post-draft lock to clear, then retry. Never attempt DELETE→wait→DELETE loops — use overwrite instead. |
| **DRAFT-PUBLISH-FLOW-1: InvenioRDM draft→publish flow differs from research skill v2.50 documentation (2026-08-04)** | The complete InvenioRDM flow: (1) `POST /api/records/{id}/draft` (HTTP 201, creates draft edit of published record, same ID); (2) `PUT /api/records/{id}/draft` (HTTP 200, update metadata); (3) overwrite files via `PUT /api/records/{id}/draft/files/{filename}` with Content-Type: application/octet-stream; (4) `POST /api/records/{id}/draft/actions/publish` (HTTP 202). Record retains same DOI under concept DOI. No new record ID is created — the draft IS the published record in edit mode. Verify: `GET /api/records/{id}` → status = published, files = updated. |
| **SUBAGENT-DEADLINE-CROSSREF-1: Subagent runTimeoutMs of 300000 (5 min) insufficient for API-heavy audits (2026-08-04)** | Cross-reference: kaizen skill v1.13 SUBAGENT-DEADLINE-1. For fetch-heavy subagent tasks (Zenodo paginated search, D1 scans), set `runTimeoutMs: 900000` or run directly in parent. This research skill's publication pipeline (Phase 5-8) often triggers subagent audits — if a Phase 5 subagent audit times out, fall back to parent-agent direct verification. |


| **CHROME-PROCURE-1: Attempting `npx @puppeteer/browsers install chrome` hangs (2026-08-04)** | The `@puppeteer/browsers` install() method hangs indefinitely on this machine after downloading the zip. Use Python `urllib.request.urlretrieve(url, zip_path)` + `zipfile.extractall()` instead. Download is ~194 MB, takes 2-5 minutes. Cache at `%USERPROFILE%\.cache\puppeteer\chrome\`. |
| **MATHJAX-CDN-HEADLESS-1: Chrome headless cannot reach MathJax CDN (2026-08-04)** | `page.goto(htmlFile, {waitUntil: 'networkidle0'})` with CDN-referenced MathJax hangs forever on `networkidle0`. Download `tex-svg-full.js` (~2.2 MB) via Python urllib and INLINE it into the HTML before CDP capture. Use `str.replace(script_tag, inline_script_tag)` — NOT `re.sub()` which crashes on MathJax JS `\u` escape sequences. |
| **RE-SUB-ESCAPE-1: Using re.sub() on MathJax JS crashes with "bad escape \u" (2026-08-04)** | MathJax `tex-svg-full.js` contains `\uXXXX` Unicode escape sequences. Python's `re.sub(replacement)` interprets `\u` as a regex escape and crashes. Use `str.replace(exact_match, replacement)` instead — it treats the replacement as a literal string. |
| **ZENODO-NEWVERSION-404: POST /api/records/{id}/actions/newversion → HTTP 404 in InvenioRDM (2026-08-04)** | The `/actions/newversion` endpoint is DECOMMISSIONED. It returns HTTP 404 for all records. Use `POST /api/records/{id}/draft` — creates a draft edit of the published record (HTTP 201) with the same ID. Publish via `POST /api/records/{id}/draft/actions/publish` (HTTP 202). |
| **ZENODO-USER-404: GET /api/user → HTTP 404 in InvenioRDM (2026-08-04)** | Token validation endpoint is `/api/me` (HTTP 200 returns user email), NOT `/api/user` (HTTP 404). A token returning 404 on `/api/user` and 200 on `/api/me` is VALID — do not diagnose "expired token" from a `/api/user` 404. |
| **ZENODO-BUCKET-LOCKED-1: DELETE file from draft → 403 "Bucket is locked" (2026-08-04)** | After `POST /api/records/{id}/draft`, deleting old files may return 403. Instead, upload new files with the SAME key to overwrite: `PUT /api/records/{id}/draft/files/{filename}` with `Content-Type: application/octet-stream`. If bucket remains locked, wait 30 seconds and retry. |
| **NODE-EVAL-CMD-1: node -e fails with "Unterminated string constant" in cmd.exe (2026-08-04)** | `node -e` in Windows cmd.exe cannot handle multi-line code or code with quotes. Always write Node scripts to `.mjs` files and run `node <file>`. Same rule as windows-command-patterns S0.0 for Python `-c`. |
| **PYTHON-C-AMPERSAND-1: python -c fails when command contains & (2026-08-04)** | cmd.exe interprets `&` as command separator. Always write Python scripts to `.py` files and run `python <file>`. Cross-reference: windows-command-patterns S0.0. |
| **PANDOC-PATH-CMD-QUOTES-1: cmd.exe quoting fails for pandoc with PATH prepend (2026-08-04)** | `cmd /c "set PATH=... && pandoc ..."` with outer quotes is not valid cmd.exe syntax. Use the canonical pandoc path directly: `C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe`. Never prepend to PATH via cmd /c set. |

> **Full anti-pattern archive (pre-2025 incidents, 50+ resolved rows) → HISTORY.md**

---

## HISTORY.md (cross-reference)

The full research skill archive is maintained at `deploy/history/research-v2.45-archive.md` and includes:
- 22 version banners (v2.19–v2.45) with complete incident records
- Resolved anti-patterns (pre-2025, 50+ rows)
- Historical PDF pipelines (XeLaTeX, build-paper.py, unicode-latex-preprocess.py)
- Zenodo Data Dictionary (37-field table, full templates)
- Professional Publication Standards copyediting checklist (expanded)
- Phase Closeout Protocol (complete 6-step)
- Version Tagging Protocol table
- OSF Registration workflow (retired)
- Forecast Integration Map (complete cross-reference)
- All retired script references (build-paper.py, _check_pdf.py, unicode-latex-preprocess.py, _fffd_scan.py)

This de-bloated v2.46 retains the complete core pipeline, the v2.46 KIF-29 upgrade, and the last 12 months of anti-patterns. For version history beyond v2.46, audit the archive file.

## Version

Current: **v2.60** (research — WBS taxonomy integration: Phase 0.1 routing table includes WBS codes (UMP/SLB/INM/CFE/RES) with canonical repo URLs + branch prefixes; `{prog}/{type}/{slug}` branch naming; PROJECT-PLAN.md first-line WBS code mandate; execute_plan uses real WBS program codes; cross-ref git-github v2.10, qnfo-core v1.10; 2026-08-04) (research — v2.59: PHASE0-EMPTY-REPO; v2.60: WBS taxonomy; 2026-08-04)
