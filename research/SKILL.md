---
name: research
version: 2.46
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

# RESEARCH — v2.46 De-Bloated (KIF-29 HARD Upgrade + Silo-Failure Detection Protocol)

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

update_plan([
  {"step": "Phase 0: Project Initialization — repo, scaffold, WBS, core claim lock", "status": "pending"},
  {"step": "Pre-Flight: Run P1-P11 checklist — HARD gates must pass before Phase 1", "status": "pending"},
  {"step": "Phase 1: Due Diligence — query KG + D1 + Vectorize + external sources", "status": "pending"},
  {"step": "Phase 1b: Cross-Domain Consilience & Silo-Failure Detection (HARD — always runs, scope-scaled)", "status": "pending"},
  {"step": "Phase 2: Literature Search — 8 parallel sources, dedup, classify, Mandatory Symmetry Template (KIF-18)", "status": "pending"},
  {"step": "Phase 3: Citation Management — extract, verify BibTeX, auto-generate missing DOIs", "status": "pending"},
  {"step": "Phase 4: Deep Research — Structured Forecast Protocol (mandatory, scope-scaled; 11 stages, produces forecast artifacts)", "status": "pending"},
  {"step": "Phase 5: Publication — format paper, build PDF (build-pdf-pro.py), BP-1→BP-10 gates, Zenodo upload with DOI", "status": "pending"},
  {"step": "Phase 6: Deploy — D1 living-paper insert, papers-server Worker verification, MCP-driven deployment check", "status": "pending"},
  {"step": "Phase 7: Disseminate — SEO audit, Buffer social media, papers.qnfo.org verification, Internet Archive", "status": "pending"},
  {"step": "Phase 8: Core Distribution — GitHub push + tag, Zenodo new-version, R2 archive sync, D1/KG records, BP-4/BP-5 correction protocol", "status": "pending"},
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
| `memory-management` | 0, every closeout | Durable memory logging |
| `documents` / `pdf` | 5 (publication) | PDF building, document formatting |
| `skill-creator` | 5 (publication) | For skill_file generation if needed |

---

## Phase 0: Project Initialization (BLOCKING GATE for new projects)

**HARD GATE:** Phase 1 MUST NOT begin until all Phase 0 deliverables committed.

### 0.1 Repository

Standard scaffold: `<project-slug>/` with `README.md`, `PROJECT-PLAN.md`, `.gitignore`, `docs/`, `artifacts/`, `notebooks/`, `releases/`. Git init on feature branch (NEVER main/master).

**REPO-TARGET GATE (HARD):** `git remote -v` before every tag/commit/release — confirm target is the PROJECT's repo, NEVER `QNFO/qnfo-skills` (ADR-026).

### 0.2 Project Plan

`PROJECT-PLAN.md` with: Charter, Phases with WBS, Milestones with gate criteria, Deliverable Registry, Risk Register, Success Criteria.

### 0.3 Closeout

Phase Closeout Protocol: commit → credential-scan → tag → push → verify → log to memory. Tag: `v0.1-phase0`.

---

## Pre-Flight Checklist (P1-P11, HARD gates before Phase 1)

| ID | Check | Gate |
|:---|:------|:-----|
| P1 | Git repo initialized on feature branch | HARD |
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

### PDF Building

**CANONICAL PIPELINE:** `build-pdf-pro.py` (MathJax-SVG → puppeteer CDP → PyMuPDF verify). TeX Live uninstalled (2026-08-02). Legacy XeLaTeX/build-paper.py pipelines retired → HISTORY.md.

```bash
python build-pdf-pro.py <slug>.md <slug>.pdf --title "<Title>"
```

Slug-based naming: `<slug>.md`, `<slug>.pdf` — NEVER generic `paper.md`.

**Mandatory verification:** `build-pdf-pro.py` exit code 0 = ZERO U+FFFD, ZERO PUA, ZERO icon-fonts, ZERO Times fallback. Exit code 1 → MUST NOT publish.

### Zenodo Upload

**Credential Protocol:** Never hardcode or retype tokens. Reference live environment variable. Run `scripts/zenodo-token-check.py` on any 403. Required scopes: `deposit:write`, `deposit:actions`, `user:email`.

**PRE-CHECK:** Before `actions/newversion`, check for unsubmitted drafts via `GET /api/deposit/depositions?q=<title>`.

**Upload order (PREVIEW-FIRST):** `<slug>.pdf` → `README.md` → `<slug>.md` → `PROVENANCE-BUNDLE.zip` → remaining files. BUCKET URL RULE: upload to `{links.bucket}/{filename}`, never construct URL manually.

**Metadata:** Data dictionary → `references/zenodo-deposit-schema.json`. Templates: Variant A (fresh), Variant B (newversion). Checklist before PUT: title matches YAML, upload_type set, creators format "Family, Given", keywords is JSON array, related_identifiers include isNewVersionOf+isSupplementedBy.

**Publish → Verify:** `curl -sI https://doi.org/10.5281/zenodo/{id}` → HTTP 200. `.zenodo_versions.json` tracking.

**Versioning:** Use `actions/newversion` for same-concept updates. Never create disconnected new deposit for same project.

**HARD GATES:**
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
| curl on PS (alias to Invoke-WebRequest) | Use curl.exe explicitly |
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
