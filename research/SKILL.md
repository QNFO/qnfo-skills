---
name: research
description: End-to-end research and publication pipeline -- GitHub + Zenodo + R2 + D1/KG core distribution stack (v2.38, Buffer API v2.14, slug-based naming, mojibake gate). Project initialization, literature search, citation management, deep research, publication, deployment, and core distribution -- project initialization (Phase 0 scaffold, pre-flight checklist, WBS), literature search (OpenAlex, arXiv, Crossref, Zenodo records, Europe PMC, web, Vectorize, KG), paper triage and classification, citation management and BibTeX verification, deep paradigm forecasting (11-stage structured forecast protocol with calibration register, practical applications extension, and counterfactual backcasting), research planning and hypothesis generation, publication formatting and PDF building (Springer Nature LaTeX template `sn-jnl.cls` as the MANDATORY DEFAULT for LaTeX-native journal papers; Pandoc+XeLaTeX for Markdown-native publications), Professional Publication Standards (journal-grade content/tone/structure/copyediting bar), Zenodo DOI upload with robust retry and versioning, Cloudflare deployment (D1 + papers-server Worker), social media dissemination via Buffer (api.buffer.com graphql, createPost mutation, assets:[] required, inline fragments on PostActionPayload union members for error handling), SEO optimization, core distribution stack (GitHub + Zenodo + R2 + D1/KG), and phase closeout protocol with version tagging. Use for ANY research, publication, project lifecycle, or dissemination task.
triggers: ["research", "paper", "literature", "preprint", "arXiv", "Semantic Scholar", "OpenAlex", "Crossref", "Europe PMC", "Zenodo search", "rate limit", "429", "cite", "citation", "BibTeX", "bibliography", "deep dive", "paradigm forecast", "forecast", "publish", "Zenodo", "DOI", "manuscript", "LaTeX", "build PDF", "social media", "tweet", "post", "Buffer", "LinkedIn", "Bluesky", "SEO", "sitemap", "robots.txt", "discoverability", "llms.txt", "structured data", "meta tags", "IPFS", "filebase", "cid", "pinning", "Web3", "CAR", "DID", "Filecoin", "Arweave", "research plan", "methodology", "hypothesis", "publication", "dissemination", "write paper", "publish paper", "scientific", "academic", "LRAP", "QNFO publication", "QWAV publication"]
related: ["knowledge", "cloudflare", "git-github"]
version: "2.45"
priority: 1
platform: all
autonomous: true
self_sufficient: true
---

> **v2.26 UPDATE (2026-07-29, KIF-32 thin-client temp-volatility incident):**
> Companion update to git-github v2.3. A session editing Continuum Trilogy
> Paper III source files cloned to `$env:TEMP` lost work across 3 re-clones
> because Windows temp directories can be cleaned between turns. The Phase 5
> PDF build/edit cycle is especially vulnerable: the agent reads a local clone,
> edits the source to fix math-mode issues, tries to build, discovers more
> issues, edits again — often across 5-10 turns on the same clone. **Every
> edit to a temp clone MUST be followed by git commit + push in the SAME
> turn**, not batched for a "final commit" at the end. Added Phase 5 temp
> guard below and anti-pattern rows. Cross-reference: git-github v2.3
> §TEMP Volatility & Same-Turn Commit Mandate (HARD GATE).

> **v2.25 UPDATE (2026-07-29, Cloudflare MCP integration kaizen):**
> Red-team audit identified that this skill references Cloudflare infrastructure
> (D1, R2, Workers) but gives zero guidance on using the 17 Cloudflare MCP servers
> for deployment verification, observability, and dissemination. Added:
> 1. Phase 1 (Due Diligence): `cloudflare-browser-mcp-server` for headless browser
>  web research; `cloudflare-blog` for relevant Cloudflare announcements.
> 2. Phase 6 (Deployment): MCP-driven deployment verification chain (`cloudflare-builds`
>  + `cloudflare-observability` + `cloudflare-bindings` + `cloudflare-auditlogs`)
>  as a HARD GATE after every D1/R2/Worker deployment.
> 3. Phase 7 (Dissemination): `cloudflare-radar` for domain ranking insights;
>  `cloudflare-docs` for SEO best-practice verification; `dex-analysis` for
>  papers.qnfo.org latency monitoring.
> 4. Phase 8 (Core Distribution): Full 17-MCP verification chain as the mandatory
>  gate before setting status="published".
> 5. Cross-Skill Integration Checklist: added `cloudflare` skill load at Phase 6
>  (was already present) and reference to §MCP-Driven Operations decision matrix.
> See `cloudflare` skill v3.9 for the canonical MCP-Driven Operations decision
> matrix. Companion update: `cloudflare` v3.9, `code` v2.2, `knowledge` v2.2.

# RESEARCH -- v2.45 (Core Pipeline: GitHub + Zenodo + R2 + D1/KG + 17-MCP Verification + Forecast + Applications + Backcasting + Slug-Based Naming + Mojibake Gate + GATE P5.CLEAN)

> **v2.45 UPDATE (2026-08-02, kaizen — newversion file-inheritance + preview + D1 slug drift):**
> Reactive kaizen per user directive following D1/D2/D3 errata publishing session.
> Red-team: direct parent-agent 5-adversary audit per kaizen v1.2.5 HARD GATE (no subagents).
> HARD findings: 1. SOFT findings: 2.
> Changes:
> (1) [HARD] **GATE P5.CLEAN:** `actions/newversion` copies ALL files from the source deposit
>   into the new draft. If old files are not deleted before uploading, they persist and can
>   become the preview file — evidenced in this session where ACRP-04 v1.3's preview became
>   `ERRATA.md` (1KB) instead of the intended PDF (80KB), and ACRP-06 v1.1's preview was the
>   `.md` source file instead of the PDF. After every `actions/newversion`, MANDATORILY
>   enumerate and DELETE ALL files before uploading fresh files in preview-first order.
>   Updated Zenodo Versioning step 2 with explicit GET→DELETE→PUT workflow.
> (2) [SOFT] Anti-patterns: added "Assuming actions/newversion creates a clean draft" (GATE
>   P5.CLEAN, 2026-08-02) and "D1 living-paper slug drifted after terminology correction"
>   (2026-08-02 — ACRP-04 slug changed from `pythagorean-semigroup-audit` to
>   `acrp04-five-smooth-audit` after BP-2 correction; D1 query by old slug returned zero).
> (3) [SOFT] Session heuristic: PowerShell `python -c` with quotes/dicts/regex (kaizen B1)
>   recurred 4-6 times this session despite being a documented anti-pattern. Escalating
>   severity note — consider a HARD runtime gate that blocks `python -c` if the command
>   contains `"`, `{`, or `(` (deferred — requires DeepChat tool-level enforcement).
> Cross-reference: kaizen v1.4.1, ACRP-04 v1.3 (10.5281/zenodo.21754151), session KR56igk6tirRGs0kA4r8w.
> Reactive kaizen from the carry-forward session (ODR v2.1 + Cross-Domain v4.1 execution).
> Red-team: direct parent-agent 5-adversary audit per kaizen v1.2.5 HARD GATE (no subagents).
> HARD findings: 4. SOFT: 1.
> Changes:
> (1) [HARD] Common Error Signatures: added `actions/newversion` 400 `files.enabled:
>   Please remove all files first` — means a newversion draft ALREADY EXISTS; follow
>   `links.latest_draft` and complete it, never create a parallel newversion (ODR
>   incident: deposit 21751722, draft 21752136, 2026-08-02).
> (2) [HARD] Zenodo Versioning section: added mandatory PRE-CHECK — query
>   `/api/deposit/depositions?q=<title>` for `state=="unsubmitted"` drafts BEFORE any
>   newversion/publish; a recently-modified unsubmitted draft is a CONCURRENT session's
>   in-flight work — coordinate, do not collide.
> (3) [HARD] Anti-patterns: 4 new rows — "Treating a Zenodo record ID as proof of
>   paper identity" (record IDs are GLOBAL; a 404 ID can later be claimed by a
>   third party — 21748026; verify TITLE+CREATOR, not existence), "Calling
>   actions/newversion twice because a draft already exists", "Publishing without
>   checking for in-flight unsubmitted drafts", "Syncing D1 body_md from a stale
>   local copy after publish" (Cross-Domain: D1 47,134 chars old table vs published
>   49,515 corrected — re-download from the new record).
> (4) [SOFT] Frontmatter `version` reconciled 2.38 → 2.44 (had drifted from live
>   header v2.43 — Status Auditor).
> Cross-reference: kaizen v1.4, ODR v2.1 (10.5281/zenodo.21752136), Cross-Domain v4.1
> (10.5281/zenodo.21754016).

> **v2.43 UPDATE (2026-08-02, kaizen — Zenodo bucket-URL rule + upload endpoint fix):**
> Reactive kaizen following the ODR v1.5 Zenodo upload block (session 3YzGvuFkUK, 2026-08-02).
> Root cause: the SKILL.md "2. Upload Files" section documented the WRONG file-upload endpoint —
> `PUT /api/deposit/depositions/{id}/files/{file}` — which agents translated into ad-hoc
> constructed URLs (e.g. `/api/files/{deposit_id}`). Zenodo's storage backend returns HTTP 500
> for these paths because the deposit ID is NOT the bucket UUID. The canonical script
> `scripts/zenodo-create-upload.py` was already correct (`upload_file` uses `f'{bucket_url}/{name}'`
> with the bucket URL returned by `create_deposit` from `links.bucket`); only the prose guidance
> was wrong.
> Changes:
> (1) [HARD] Added **BUCKET URL RULE** to "2. Upload Files" — the upload endpoint MUST be
>   extracted from the deposit record's `links.bucket` field (UUID path); NEVER constructed
>   manually. Manual construction returns HTTP 500.
> (2) [HARD] Corrected the documented upload-path examples in "2. Upload Files" — the
>   deprecated wrong path is flagged and replaced with `PUT {links.bucket}/{filename}`.
> (3) [HARD] Added anti-pattern row: "Constructing the Zenodo file-upload URL manually instead
>   of extracting links.bucket" with the full incident root-cause and fix reference.
> (4) [SOFT] Cross-referenced `scripts/zenodo-create-upload.py` as the canonical upload
>   implementation to follow, not ad-hoc inline scripts.
> Red-team: direct parent-agent audit per kaizen v1.2.5 HARD GATE (no subagents).
> Cross-reference: kaizen v1.3.0, ODR v1.5 (DOI 10.5281/zenodo.21750975), zenodo-create-upload.py.

> **v2.42 UPDATE (2026-08-02, kaizen — numeracy gates + look-elsewhere expansion):**
> Reactive kaizen per user directive: "EXECUTE KAIZEN UPDATE TO AUDIT FOR AND REMEDIATE
> LOOK-ELSEWHERE AND NUMEROLOGY/DATA-FITTING ISSUES/VIOLATIONS WHEN CONDUCTING RESEARCH."
> Triggered by full-session red-team audit of ACRP-04 / Koide analysis that surfaced
> 7 findings including: 9,138σ unreproducible (best: 8,943σ), cross-paper numerical
> inconsistency (99.8% vs 99.85%), 0.050% overdetermined lepton closure error, Koide Q
> miscalculated (0.02% → 0.00289%), and §6 adelic factorization identified as untested
> Class 2 numerology.
> Changes:
> (1) [HARD] **BP-4 Cross-Paper Numerical Consistency Gate** — when multiple QNFO papers cite
>   the same number, values MUST agree within rounding. Blocks cross-paper drift.
> (2) [HARD] **BP-5 Overdetermined System Verification Gate** — when N ratios claimed from
>   M<N independent quantities, internal closure error must be computed and reported.
> (3) [HARD] **BP-6 Derived-Quantity Recompute Gate** — any quantity derived from claimed
>   primary results must be recomputed from first principles before being cited as evidence.
> (4) [HARD] **BP-7 Sigma/Error Propagation Audit Gate** — every σ must trace to a specific
>   cited uncertainty source; two conflicting uncertainty values in one paper = BLOCKED.
> (5) [DESIGN] **BP-8 Numerology Claim Classification** — 5-class typology (Dense-Approximant,
>   Ratio-Factorization, Index-Selection, Transcendental, Pattern-in-Noise) with per-class
>   required gates. Closes the §6/§7.2 selective-gate-application gap.
> (6) [SOFT] **BP-9 Audit-the-Auditor Gate** — audit papers critiquing numerical accuracy
>   must self-audit via BP-1 through BP-7 before publication.
> (7) [HARD] **BP-10 Independent-Recompute Gate** — before citing any paper's numerical
>   claim as evidence, recompute it in the current session with independent implementation.
> (8) [DESIGN] **Numeracy Red Flags Checklist** — 14-signal quick-scan (🚩) for pre-publication
>   numerical claim screening. 0 🚩→proceed; 1-2→investigate; 3+→HARD BLOCK.
> (9) [SOFT] **9 new anti-pattern rows** covering: unreproducible audit numbers, conflicting
>   uncertainty values, overdetermined closure, derived-quantity errors, cross-paper
>   inconsistency, selective gate application, untraceable sigma sources, skipped
>   recomputation, and post-hoc tolerance selection.
> Red-team: direct parent-agent 5-adversary audit (Accuracy/Completeness/Dependency/Novelty/
> Status). All findings integrated. Zero blocking issues remaining after remediation.
> Cross-reference: kaizen v1.2.5, ACRP-04 (DOI 10.5281/zenodo.21748008), session 747X9msNaKJP47-DGVSrn.

> **v2.41 UPDATE (2026-08-01, kaizen — Zenodo preview file designation):**
> Reactive kaizen per user directive: "UPDATE ZENODO SKILL TO DESIGNATE A PREVIEW
> FILE WHEN UPLOADING DEPOSITS/VERSIONS. GENERALLY THIS WILL BE EITHER MAIN PDF
> PUBLICATION/PAPER, README, OR PRIMARY MARKDOWN FILE (IN THAT PREFERRED ORDER)."
> Changes:
> (1) [DESIGN] Added **Preview File Designation Protocol** (new subsection after
>   the Zenodo Upload §2 step lists) — a mandatory priority-ordered upload rule:
>   the intended preview file MUST be uploaded FIRST. Zenodo uses the first file
>   uploaded as the deposit's landing-page preview/thumbnail. Priority: (a) main
>   PDF publication, (b) README.md, (c) primary markdown file `<slug>.md`.
> (2) [DESIGN] Updated Zenodo Upload §2 file upload order to reflect preview-first
>   priority: `<slug>.pdf` ALWAYS first; then README.md; then `<slug>.md`; then
>   PROVENANCE-BUNDLE.zip and remaining artifacts.
> (3) [DESIGN] Added preview-file verification to the GATE P5.PDF post-upload
>   check — after upload, confirm the first file in the deposit's file list is
>   the intended preview.
> (4) [DESIGN] Added "Preview file uploaded first" to the Template Usage Checklist.
> (5) [SOFT] Added anti-pattern row: "Uploading files to Zenodo in arbitrary order
>   without designating a preview file."
> Cross-reference: kaizen v1.2.5.

> **v2.40 UPDATE (2026-08-01, kaizen — Zenodo data dictionary + template):**
> Reactive kaizen per user directive: "ZENODO SKILL INSTRUCTIONS SHOULD CONTAIN
> TEMPLATE FOR UPLOADS WITH COMPLETE DATA DICTIONARY."
> Changes:
> (1) [DESIGN] Added complete **Zenodo Metadata Data Dictionary** — 37-field table
>     with JSON type, required/optional, constraints, allowed values, examples, and
>     gotchas for every Zenodo deposit metadata field (title through prereserve_doi).
> (2) [DESIGN] Added **Related Identifier Relations table** — 6 relations
>     (isNewVersionOf, isPreviousVersionOf, isVersionOf, isSupplementedBy, cites,
>     obsoletes) with meaning, scheme, and example for each.
> (3) [DESIGN] Added **two Ready-to-Fill JSON Templates** — Variant A (fresh deposit)
>     and Variant B (newversion draft) with placeholder fields and critical notes
>     about the upload_type/publication_type string-fallback for newversion drafts.
> (4) [DESIGN] Added **Template Usage Checklist** — 9 pre-PUT verification items
>     including P5.IDENTITY title match, keyword array format, and license defaults.
> (5) [DESIGN] Added **Common Error Signatures table** — 6 canonical error patterns
>     with root cause and fix (resource_type missing, invalid string, creators missing,
>     keywords 400, newversion 403, upload 415).
> Inserted between the Zenodo Credential Protocol and Zenodo Upload sections.
> Cross-reference: kaizen v1.2.5, `references/zenodo-deposit-schema.json` (already
> existed but agents rarely consulted it as a reference file).

> **v2.39 UPDATE (2026-08-01, kaizen — 5 new best practices from full-session red-team):** HARD: 0. SOFT: 1 — Pythagorean misnomer for 5-smooth numbers propagated through 4 papers. DESIGN: 5 — BP-1 fit-verify, BP-2 terminology audit, BP-3 density gate, BP-4 correction-on-discovery, BP-5 KG CORRECTS edge. Added 4 new anti-patterns. Bumped execute_plan Phase 5 + Phase 8 with new gates.
>
> Per user directive, all paper output files MUST use project-slug-based naming instead
> of generic `paper.md`/`paper.pdf`. Changed all 25+ references across the skill:
> `paper.md` → `<slug>.md`, `paper.pdf` → `<slug>.pdf`. Rationale: generic names cause
> confusion when multiple paper repos share a temp directory. Added anti-pattern row.
> Also added §0.2 UTF-8 Source Encoding Mandate cross-reference from qnfo-core v1.2 —
> `scan-mojibake.py` must pass BEFORE any publication (HARD GATE). See qnfo-core v1.2
> §0.2 for the full gate protocol and mojibake pattern reference table.
>
> **v2.37 UPDATE (2026-07-31, kaizen — KIF-58 cross-contamination incident):**
> Red-team: direct parent-agent 5-adversary audit (Accuracy, Completeness, Dependency,
> Novelty, Status) following JPCUB/Computing-Machines cross-contamination incident.
> HARD findings: 1. SOFT: 0. DESIGN: 0.
> Changes:
> (1) [HARD] Added **HARD GATE P5.IDENTITY (KIF-58)** — cross-project paper identity
>   verification before ANY Zenodo upload or GitHub cross-population: verify paper
>   title matches target Zenodo concept, DOI belongs to concept chain, GitHub repo
>   paper title matches, temp directory content validated, Zenodo bucket lock
>   awareness. This gate blocks the exact failure mode where "Computing After
>   Silicon" paper was uploaded to the JPCUB Zenodo concept and JPCUB content was
>   pushed to the computing-machines repo (Accuracy + Completeness Auditors,
>   parent-agent).
> (2) [SOFT] Added 4 new anti-pattern rows: "Assuming temp-directory name identifies
>   project," "Cross-populating Zenodo/GitHub without verifying paper identity,"
>   "Publishing Zenodo deposit without verifying uploaded file contents," and
>   "Cross-project paper confusion from handoff ambiguity" (Completeness +
>   Dependency Auditors, parent-agent).
> Cross-reference: kaizen v1.2.2, qnfo-core KIF-58, memory "Do not assume temporary
> directory names identify the project."

> **v2.36 UPDATE (2026-07-31, red-team kaizen):**
> Red-team review: 5 parallel subagents attempted, 0 completed with full output (all
> truncated); fell back to direct parent-agent 5-adversary audit (Accuracy, Completeness,
> Dependency, Novelty, Status) per kaizen §Subagent Failure Handling.
> HARD: 2. SOFT: 8. DESIGN: 4 (3 applied, 1 deferred).
> Changes:
> (1) [HARD] Appended v2.35/v2.36 entries to `.kaizen_history` — the v2.35 kaizen skipped
>   the mandatory history log (Dependency Auditor, parent-agent).
> (2) [HARD] Fixed dangling cross-ref "memory 'Semantic Scholar 429 — use hybrid fallback
>   strategy'" — two memory_recall probes found no such durable memory; created the
>   heuristic memory so the reference resolves (Dependency Auditor, parent-agent).
> (3) [SOFT] Corrected Rate-Limit Matrix query counts to match evidence files (4 per API):
>   OpenAlex ×6→×4, Crossref ×3→×4, Zenodo ×3→×4, Europe PMC ×3→×4 (Accuracy Auditor —
>   verified against `artifacts/external-search/`, 16 query files + 3 doc files).
> (4) [SOFT] Softened unverified Crossref "50 req/s recommended ceiling" → "documented
>   guidance, not session-measured" (Accuracy Auditor — docs fetch showed no rate-limit
>   statement).
> (5) [SOFT] Anti-pattern "Query all 5 sources in parallel" → "all 8 sources" (Completeness
>   Auditor — Phase 2 Multi-Source Search now lists 8 sources).
> (6) [SOFT] Frontmatter description "(v2.17, Buffer API v2.13)" → "(v2.36, Buffer API
>   v2.14)" (Status Auditor — stale metadata).
> (7) [SOFT] New anti-pattern: novelty claims from fuzzy/tokenized search alone (Novelty
>   Auditor — unquoted Zenodo q= OR-tokenizes: "JPCUB joules per computational unit"
>   returned 311,162 vs quoted "\"JPCUB\"" returning 2).
> (8) [DESIGN] Phase 2 Multi-Source Search: added evidence-saving instruction (save every
>   API response to `artifacts/external-search/<api>_<query>.json` and cite the file for
>   every count/DOI — KIF-55) (Novelty Auditor).
> (9) [DESIGN] Rate-Limit Matrix Rule: added polite-pool etiquette (mailto param for
>   OpenAlex/Crossref, ~0.4s sleep between queries) + exact-phrase vs tokenized search
>   semantics (Novelty Auditor).
> (10) [DESIGN] Added arXiv ~3s query-interval note (Completeness Auditor).
> Deferred: (D1) standalone `scripts/research-api-search.py` — the Multi-Source Search
> table already carries canonical URLs; deferred once per kaizen DESIGN policy, revisit
> if a second project needs a reusable probe.
> Cross-reference: kaizen v1.2.2 (calibration register research v2.34→v2.36),
> jpcub-validation commit (due-diligence status-table count corrections).

> **v2.35 UPDATE (2026-07-31, keyless research API replacement kaizen):**
> Per user directive, Semantic Scholar is REPLACED as the primary academic search
> source. A session's Phase 1 due diligence lost 4 queries to HTTP 429 (rate
> limited, key-gated) with zero data retrieved. Live verification this session
> (jpcub-validation, all outputs saved to `artifacts/external-search/`):
> **OpenAlex, Crossref, Zenodo records, and Europe PMC ALL returned HTTP 200
> back-to-back with zero 429s — no API keys required.** OpenAlex is now the
> PRIMARY academic index; Crossref (DOI registry), Zenodo records (search ALL
> users' deposits, not just uploads), and Europe PMC are mandatory supplementary
> sources. Added: (1) new Research API Rate-Limit Matrix section; (2) Zenodo
> records search wired into Phase 2 — Zenodo is BOTH an upload target AND a
> third-party deposit discovery source; (3) anti-pattern rows for Semantic
> Scholar-as-primary and for skipping Zenodo deposit search; (4) frontmatter
> triggers + description updated. Verified novelty example: exact term "JPCUB"
> returns 0 in OpenAlex title search, 0 Crossref, 0 Europe PMC, and 2 Zenodo
> hits that are BOTH the author's own deposits — a 5-source novelty confirmation
> (arXiv + these 4). Cross-reference: memory "Semantic Scholar 429 — use hybrid
> fallback strategy".

> **v2.34 UPDATE (2026-07-30, kaizen):**
> Red-team review: 5 parallel subagents attempted, all truncated; fell back to direct
> parent-agent audit (Subagent Failure Handling protocol invoked).
> Changes:
> (1) [SOFT] Removed stale `_verify_4d.py` reference in anti-patterns; replaced with
>   Core Distribution Gate description (Accuracy Auditor, parent-agent).
> (2) [SOFT] Clarified `_citation_audit.py` in Verification Gates as a reusable inline
>   pattern, not a standalone script (Accuracy Auditor, parent-agent).
> (3) [SOFT] Fixed v2.33 banner miscount: "9 HARD issues" → "9 issues (3 HARD, 6 SOFT)"
>   with per-fix severity tags (Status Auditor, parent-agent).
> (4) [SOFT] Fixed v2.33 banner item 6: "10-stage pipeline" → "11-stage pipeline
>   (Stages -1 through 10)" (Status Auditor, parent-agent).
> Deferred: (D1) cronjob integration for scheduled calibration register/literature checks,
> (D2) subagent_orchestrator for Phase 2 parallel literature searches, (D3) tape_handoff
> for phase-to-phase session continuity, (D4) cross-skill version reference live verification
> (cloudflare v3.9, code v2.2, etc.), (F3) remaining mojibake encoding cleanup in
> anti-patterns section. Cross-reference: kaizen v1.1 (self-kaizen protocol, subagent
> failure handling).

> **v2.33 UPDATE (2026-07-30, kaizen — practical applications + backcasting default):**
> Kaizen adding Stages 9 and 10 (Practical Applications Extension + Counterfactual
> Backcasting) to the Structured Forecast Protocol, making them MANDATORY for all
> research projects. Red-team review: 5 parallel subagents attempted, 4 truncated
> (workspace path mismatch), 1 partial; fell back to direct parent-agent audit.
> Changes:
> 1. **Stage 9: Practical Applications Extension** — maps each forecast candidate/era
>  onto concrete application domains (computation, AI, measurement, communication,
>  economics, etc.) with falsifiable claims and calibration register entries.
> 2. **Stage 10: Counterfactual Backcasting** — systematic backcasting across target
>  disciplines with tiered historical forks (Tier 1: ~20yr, Tier 2: ~60yr,
>  Tier 3: ~120yr, Tier 4: alternate axioms). Produces "counterfactual technology
>  stack" tables and calibration register entries.
> 3. **Forecast Integration Map** — new Stage 9 and 10 rows added.
> 4. **Verification Gates** — two new gates: Practical Applications Extension (SOFT)
>  and Counterfactual Backcasting (SOFT).
> 5. **Anti-Patterns** — 4 new rows for missing Stages 9 and 10.
> 6. **Design principle paragraph** — updated to reference the full 11-stage pipeline (Stages -1 through 10).
> 7. **Frontmatter description** — "9-stage" → "11-stage structured forecast protocol."
> Zero blocking issues. **Remediation red-team (2026-07-30):** Full 5-adversary re-run found 9 issues (3 HARD, 6 SOFT).
> Fixes applied: (F1) brave_web_search → Browser/exec+curl [HARD], (F2) _check_pdf.py phantom-fix → build-paper.py
> in Verification Gates table [HARD], (F3) .kaizen_history created [HARD], (S1) two 9-stage references → full protocol [SOFT],
> (S2) KIF-32 collision resolved → KIF-54 [SOFT], (S3) trailing-slash contradiction fixed [SOFT], (S4) v2.28 chronology
> note added [SOFT], (S5) v2.22 dedup verified [SOFT], (S6) v2.32 gap documented [SOFT].

> **v2.31 UPDATE (2026-07-30, kaizen clean + forecast integration audit):**
> Comprehensive kaizen audit and red-team review. Changes:
> 1. **execute_plan Phase 4:** "(if paradigm forecast triggered)" → "(mandatory, scope-scaled;
>  produces forecast artifacts)" — resolves v2.28 contradiction.
> 2. **Duplicate v2.22 banner REMOVED** — copy-paste artifact, two identical KIF-28 blocks.
> 3. **Verification Gates PDF entry:** `_check_pdf.py` → `build-paper.py` — the former was deleted
>  in v2.21 (KIF-27 consolidation).
> 4. **Triplicated OSF anti-patterns DEDUPED** — 6 anti-pattern rows appeared 2-3× each; one copy kept.
> 5. **Stale `createDraft` reference in anti-patterns:** `.createDraft` → `createPost` — `createDraft`
>  was deprecated in v2.11.
> 6. **Frontmatter description:** "no inline fragments on PostActionPayload" → "inline fragments
>  on PostActionPayload union members for error handling" — the v2.13 retracted claim was still
>  in the skill's primary triggering metadata.
> 7. **Forecast Integration Map ADDED** — explicit cross-reference table showing how every
>  Phase 4 Stage output feeds into Phases 1-8, making the "seamless weaving" of forecasting
>  into research explicit and auditable.
> 8. **Phase 5 PUBLICATION PRINCIPLE cross-reference ADDED** — methodology-invisibility principle
>  now explicitly referenced at Phase 5 entry point, preventing agents from producing
>  methodology-branded publication output.
> Red-team review: 3 parallel subagents (methodology-invisibility, consistency, structural overload)
> plus direct forensic audit. Zero blocking issues remaining.
> Cross-reference: skill-creator v1.0 (progressive disclosure, <500 line target).
>
> **v2.30 UPDATE (2026-07-30, genre cross-reference kaizen):** Added genre
> classification cross-reference to Phase 5 Pre-Publication Requirements.
> Certainty calibration and Professional Publication Standards apply to Genre A
> (Epistemic Content) only. For Genre B (Commercial/Marketing), the protocol is
> MODIFIED per qnfo-core 0.1: no inline [speculative] labels, use Forward-Looking
> Statements footer and dagger footnotes instead. Cross-reference: qnfo-core v1.1 0.1,
> frontend-design v2.2 (Landing Page Content Gate).
>
> **v2.29 UPDATE (2026-07-30, methodology-invisibility principle):**
> Research outputs (papers, PDFs, abstracts) must NOT brand methodology.
> The reader should see good analysis, not protocol signage. Added
> PUBLICATION PRINCIPLE to Phase 4 header: never write "Stage 2 Assumption
> Audit found..." — write "Underlying this candidate are three critical
> assumptions." The method should be invisible in the prose.

> **v2.28 UPDATE (2026-07-30, Phase 4 mandatory + trigger cleanup kaizen):**
> Per user directive, the structured forecast protocol is now MANDATORY for
> ALL research projects, not an optional add-on gated behind trigger keywords.
> Architectural changes:
> 9. Phase 4 is now **mandatory for all projects** — scope scales to project size
>  (a single-result paper runs a lighter version; a paradigm forecast runs
>  the full 9-stage protocol). Trigger-gating keywords (`"deep dive"`,
>  `"paradigm forecast"`, `"maximize EVs"`) are REMOVED from the Phase 4
>  header; Phase 4 now simply states "Runs for ALL projects."
> 10. Frontmatter triggers: `"Bayesian"` and `"EV ranking"` removed from the
>   trigger words array — these are dead keywords from v1 that should no
>   longer cause skill activation.
> 11. Frontmatter description: "9-stage Bayesian cascade" → "9-stage structured
>   forecast protocol."
> 12. Anti-patterns: the duplicate "Use Likelihood-Span Sensitivity (Stage 4,
>   KIF-31 upgrade)" row replaced with "Use Judgment Sensitivity Analysis
>   (Stage 4, v2.27)."
> 13. Version bumped: 2.26 → 2.28 (frontmatter `version` field + heading).
> **Note:** v2.27 was a retroactive kaizen applied AFTER v2.28, inserted between v2.26 and v2.28 in the banner chronology. The "2.26 → 2.28" bump reflects the version state at the time v2.28 was created.

> **v2.27 UPDATE (2026-07-30, Bayesian Cascade retirement kaizen):**
> Per user directive, the "9-Stage Bayesian Cascade" is RETIRED and replaced
> with a "Structured Forecast Protocol." Key changes:
> 1. Phase 4 renamed from "9-Stage Bayesian Cascade" to "Structured Forecast
>  Protocol" — with an explicit METHODOLOGY NOTE declaring that this is NOT
>  a Bayesian computation but a structured judgment exercise.
> 2. EV = P × I / √t formula RETIRED. Candidate ranking is now qualitative
>  with uncertainty ranges and explicit anchor reference classes. No
>  false-precision numbers (1.17, 0.71, 0.32) are produced.
> 3. Stage 1: "high-EV shifts" → "highest-impact paradigm-shift candidates"
>  with qualitative scoring.
> 4. Stage 4: "Likelihood-Span Sensitivity Analysis" → "Judgment Sensitivity
>  Analysis" — tests qualitative ranking robustness under perturbation,
>  does NOT compute numeric EVs.
> 5. Stage 6: "Optimal Portfolio Allocation / Kelly-like" → "Research Effort
>  Allocation" — effort heuristics based on qualitative ranking, not
>  pseudo-optimal bets.
> 6. Stage 8: "Adversarial Review" → "Cross-Review" — honest disclosure that
>  the reviewer is a same-model subagent, not independent inter-rater
>  reliability.
> 7. All remaining "Bayesian cascade" references scrubbed from execute_plan,
>  v2.23 banner, Stage -1 gate description, and anti-patterns table.
> 8. Existing calibration register (Stage 5) and calibration pillars (Stage -1)
>  are retained — these are genuinely useful and honest methodology.
> Cross-reference: Measurement Stratigraphy paper v2.0 which applies this
> protocol in its `structured-forecast-protocol-v2.md` artifact.

> **v2.24 UPDATE (2026-07-26, KIF-30 — mandatory PDF inclusion in Zenodo):**
> Added **HARD GATE P5.PDF (KIF-30)** to §5 Zenodo Upload — ALL PDFs MUST be
> rendered via `build-paper.py`, confirmed present locally, AND uploaded
> individually to every Zenodo deposit (both new and newversion). A
> markdown-only deposit is a publication protocol violation and MUST be
> remediated with a major version bump. The gate was red-teamed live against
> the ALP v1.0 deposit (DOI 10.5281/zenodo.21609539, 0 PDFs) and fixed in
> ALP v2.0 (DOI 10.5281/zenodo.21609889, 14 files including all 12 PDFs).
> Updated upload checklist, newversion PDF requirement, and Anti-Patterns
> table. See `qnfo-agent` v3.49 KIF-30 registry and `kaizen-skill-fixes`
> v1.5 §H for the full incident record and remediation protocol.

> **v2.23 UPDATE (2026-07-26, KIF-29 — cross-domain consilience gate):**
> Added **Cross-Domain Consilience Gate (KIF-29, SOFT)** to Phase 1 (Due Diligence),
> following the Universal Consilience Translator v2.0 prompt engineering and
> right-sizing session. The gate triggers when research spans 2+ domains or
> uses domain-specific terminology without external analogues. Output: a compact
> 6-domain structural translation (Physics, CS, CogSci, Information Theory,
> Biology, Sociology) with Core Dynamic, Cross-Domain Lexicon, Domain Translations
> (Lexicon/Instance/Ramification each), Synthesis Consilience, and Research
> Integration. Wired into Phase 2 (Lexicon terms → parallel literature search),
> Phase 4 (Synthesis → structured forecast protocol), and Phase 5 (Lexicon table in paper).
> Anti-patterns added for domain siloing, ad hoc analogies, single-domain
> literature search, and consilience claims without a unification principle.
> See `kaizen-skill-fixes` v1.4 §H for the fix design document. The full UCT-v2
> prompt is archived at `D:\Obsidian\notes\v1\2026\07\26\_26207185215.md`.
>
> **v2.22 UPDATE (2026-07-26, KIF-28 — comprehensive encoding kaizen):**
> Red-teamed KIF-28 closeout: Source File Encoding Integrity section and 7
> encoding anti-pattern rows were claimed as added but did not exist on disk.
> Added: (1) **Source File Encoding Integrity (HARD GATE)** — BOM, U+FFFD,
> U+FFFF, Python encoding declarations, and PowerShell encoding checks all
> mandatory before commit/publish; (2) 7 encoding anti-pattern rows; (3) BOM
> stripped from this file; (4) U+FFFD/U+FFFF characters removed from the
> verification code example (replaced with Python escape text). See `qnfo-agent`
> v3.48 for complementary anti-pattern updates and KIF-28 registry entry.
>
> **v2.21 UPDATE (2026-07-26, KIF-27 -- single build-paper.py consolidation):**
> DELETED `scripts/unicode-latex-preprocess.py`, `scripts/check-pdf.py`,
> and `scripts/build-pdf.py` -- three scripts patched incrementally across
> 4 kaizen passes, including one wrong detour. Replaced with ONE script:
> `scripts/build-paper.py` (preprocess + build + verify, UTF-8 forced on
> all file I/O to prevent mojibake -- see `qnfo-agent` §8.7). Usage:
> `python scripts/build-paper.py <slug>.md`. Independently re-verified
> against the original problem source (Zenodo 21595214): 0 U+FFFD, 0
> U+FFFF across 16 pages, checked with a separate verification script
> (never trust the build tool's own success claim).

> **v2.20 UPDATE (2026-07-26, KIF-26 v3 — comprehensive preprocessor fix):**
> The v2.19 "holistic unicode-math" approach was WRONG. `unicode-math` only
> applies to characters INSIDE `$...$`. Unicode math in prose uses the text
> font, which lacks glyphs. `unicode-latex-preprocess.py` v3.0 is the correct
> solution with: subscript/superscript GROUPING (10⁻¹²⁰ → `$^{-120}$`),
> adjacent digits, sqrt patterns, Mathematical Alphanumeric Symbols block,
> post-processing for subscript bracing. Verified: Zenodo 21597495 = ZERO
> errors. The `build-pdf.py` wrapper is DEPRECATED — use the preprocessor
> directly with standard pandoc.

> **v2.19 UPDATE (2026-07-26, holistic PDF Unicode solution — KIF-26 v2):**
> The v2.18 dictionary-based `unicode-latex-preprocess.py` was a band-aid.
> Dictionaries can never be comprehensive — there are thousands of Unicode
> math symbols. The CORRECT solution: configure XeLaTeX to use fonts that
> HAVE the glyphs. New pipeline:
> 1. `scripts/build-pdf.py` — uses `unicode-math` package + `STIX Two Math`
>  font, which has complete Unicode mathematical symbol coverage
> 2. `templates/qnfo-xelatex-unicode.yaml` — Pandoc defaults file
> 3. `scripts/check-pdf.py` — mandatory verification gate
> The old `unicode-latex-preprocess.py` is DEPRECATED. With the correct font
> configuration, Unicode symbols render directly without conversion.
> Verified: "Measure-Theoretic Artifacts" paper builds with ZERO errors.

> **v2.18 UPDATE (2026-07-26, PDF rendering HARD BLOCK gate — KIF-26):**
> Red-teamed a published Zenodo PDF (21595214) with 135 U+FFFD replacement
> characters. Root cause: `unicode-latex-preprocess.py` v1.0 only handled
> numeric subscripts (₀-₉) but physics papers use letter subscripts
> (ₐ ₑ ₒ ₓ ₕ ₖ ₗ ₘ ₙ ₚ ₛ ₜ) for ℚₚ, vₚ(x), etc. Also missing: ħ (h-bar),
> ℓ (script ell), 𝔸 (blackboard A for adeles), and superscript letters.
> Fix: `unicode-latex-preprocess.py` v2.0 adds ALL subscript/superscript
> letters + physics symbols; `check-pdf.py` v2.0 is now a MANDATORY
> PRE-PUBLICATION GATE (exit code 1 = MUST NOT PUBLISH). The PDF build
> pipeline is now: preprocess → pandoc → **check-pdf.py HARD GATE** → upload.
> A PDF that fails `check-pdf.py` MUST NOT be published to Zenodo or any
> public distribution channel.

> **v2.17 UPDATE (2026-07-25, default-template + professional-standard kaizen):**
> Established the **Springer Nature LaTeX Template (`sn-jnl.cls`, v3.1, Dec
> 2024)** as the MANDATORY DEFAULT TEMPLATE for all QNFO publications and
> publication-grade PDFs, replacing all prior references to the legacy,
> retired `svjour3`/`svjour.cls` package (CTAN `springer` package -- verified
> retired via live Springer Nature LaTeX Author Support page, 2026-07-25).
> Template files are embedded in this skill at
> `templates/springer-nature-latex/` (`sn-jnl.cls`, all 8 `.bst` styles,
> `sn-article.tex` reference example, `sn-bibliography.bib`,
> `user-manual.pdf`, and `qnfo-paper-template.tex` -- a QNFO-conventions
> overlay with the mandatory Declarations block pre-populated). See
> `templates/springer-nature-latex/README.md` for build instructions,
> class-option table, and the kaizen finding on `.bst` subdirectory
> placement (bibtex will not find `.bst` files in a `bst/` subfolder --
> copy the needed style file alongside `paper.tex`/`refs.bib` first).
> Also added the **Professional Publication Standards** section (new,
> below) specifying the journal-grade content, tone, structure, and
> copyediting bar every QNFO publication must clear -- this is the
> "would a peer reviewer at Foundations of Physics / PRA / NJP accept this
> without a desk rejection for presentation quality" bar, independent of
> and in addition to the Physics Writing Standards (`qnfo-agent` §7,
> content-integrity) and Publication Language Gate (internal-language
> scrubbing) that already existed. Validated end-to-end: rebuilt *The
> Macroscopic Boundary Problem in Quantum Reconstructions* on the new
> template (13 pages, zero undefined references, zero Unicode replacement
> characters, clean 4-pass build) as the reference case.

> **v2.16 UPDATE (2026-07-25, structured-schema kaizen):** Added
> **`references/zenodo-deposit-schema.json`** (canonical Zenodo REST API
> schema, including the `resource_type` persistence-failure incident from
> the adelic-cross-domain v3.2 newversion publish and the working
> `upload_type`/`publication_type` string-field fallback) and
> **`references/buffer-graphql-schema.json`** (canonical Buffer GraphQL
> schema consolidated from the scattered Phase 7 prose below). Added
> **`scripts/zenodo-resource-type-fix.py`** — tries known-working metadata
> shapes in order and verifies persistence via re-GET instead of guessing.
> Consult these reference files BEFORE constructing any Zenodo/Buffer API
> call. See `qnfo-agent` KIF-20.

> **v2.15 UPDATE (2026-07-24, PQS epistemic bias kaizen):** Added three new
> HARD gates from the PQS AI-Evaluation Audit session:
> - **Institutional Status Neutrality Gate (KIF-16):** Strip institutional
>  metadata before evaluating claims; use epistemic categories (`[UNFALSIFIABLE]`,
>  `[CONTRADICTS ESTABLISHED EVIDENCE]`, `[UNTESTED]`, `[CONTESTED]`) not
>  social categories ("fringe", "pseudoscience"); open science is real science.
> - **AI Convergence Bias Disclosure (KIF-17):** When 2+ AI systems converge
>  on dismissing a claim, flag explicitly — convergence may reflect shared
>  training-data bias, not independent validation.
> - **Mandatory Symmetry Template (KIF-18):** Every literature review MUST
>  include both "Supporting" AND "Constraining" sections; document structure
>  enforces epistemic balance.
> User statement archived: "OPEN SCIENCE IS CHANGING INSTITUTIONAL GATEKEEPERS,
> AND PUBLIC ACCESS ALWAYS WINS." Cross-references `qnfo-agent` v3.38 and
> `kaizen-skill-fixes` v1.3.

> **v2.14 UPDATE (2026-07-22, Buffer inline-fragment false-claim correction):**
> v2.13 wrongly claimed "`PostActionPayload` union type members are NOT
> directly accessible as fragment targets" and instructed querying only
> `__typename`. This was FALSE and is retracted. Live testing this session
> (The Two-Level Lie paper dissemination) proved inline fragments work
> correctly: `... on PostActionSuccess { post { id } }` returned a real post
> ID on success, and `... on LimitReachedError { message }` /
> `... on InvalidInputError { message }` returned the EXACT actionable error
> text (e.g. "You have 10 scheduled posts out of 10 allowed.") instead of a
> bare, undiagnostic `__typename`. The v2.13 `Unknown type "PostActionSuccess"`
> error that led to the false claim was caused by fragmenting on a
> **non-existent** type name (`Post`) in an earlier attempt, not by any
> actual GraphQL union restriction — a schema-shape mistake mis-generalized
> into a false rule. `scripts/buffer-post.py` bumped to v1.1 with the
> corrected mutation (requests `message` on every error variant, `post.id`
> on success) and tested live for both the success and
> failure(`LimitReachedError`) paths. Also added explicit guidance that
> `LimitReachedError` (an account-level queue cap, not a bug) must be
> disclosed as `[BLOCKED: account queue limit]` rather than retried or
> misreported.

> **v2.10 UPDATE (2026-07-21, credential/protocol kaizen after a session with
> repeated Buffer/D1/IPFS failures):** Root-caused and permanently fixed three
> classes of failure from a single session:
> 1. **Buffer token was stale in this very skill file.** The hardcoded
>  `1/7feabe69e3c8a6544ee3c20e8b21c2aa` value below was WRONG/EXPIRED and
>  caused ~10 failed Buffer API calls (401/404) before the user supplied a
>  screenshot of the actual valid key (Buffer Personal Access Token,
>  prefix `14Ky`, created 2026-06-21, 7 scopes). **Skills MUST NOT hardcode
>  live secret values that can silently go stale** -- see the corrected
>  Buffer section below, which now stores the token ONLY in
>  `%USERPROFILE%\buffer\token` and instructs verification via a live GET
>  before any POST, exactly like the Zenodo Credential Protocol already
>  mandates. Endpoint is `https://api.bufferapp.com/1.0/graphql.json`
>  (confirmed live) -- `createDraft` mutation works, but there is NO
>  `drafts` query on this schema (attempting one returns 404 "endpoint
>  not found" -- this is normal, not a fault; do not misdiagnose it as a
>  broken token).
> 2. **D1 REST API account ID was wrong.** Using an incorrect Cloudflare
>  account ID against `POST /accounts/{id}/d1/database/{uuid}/query`
>  produces a misleading 401/404 that looks like a scope problem but is
>  actually a wrong-account-ID problem. `npx wrangler whoami` prints the
>  correct account ID directly from the live `CLOUDFLARE_API_TOKEN` --
>  ALWAYS run this first, never hardcode or guess the account ID.
>  Additionally, `wrangler d1 execute <name> --remote` FAILS with
>  "Couldn't find a D1 DB with name/binding" unless that name is bound in
>  a local `wrangler.toml`/`wrangler.jsonc` -- for databases with no local
>  binding (common for shared infra DBs like `living-paper`), use the
>  Cloudflare REST API directly with the UUID from `wrangler d1 list`
>  (or `GET /accounts/{id}/d1/database`), not the `d1 execute` CLI.
> 3. **D1 `ON CONFLICT` upsert on the `living-paper.papers` table returned
>  HTTP 400.** The table has FTS5 shadow tables/triggers (`papers_fts`,
>  `papers_fts_data`, etc.) that can make `ON CONFLICT DO UPDATE` behave
>  unpredictably. Fix: `SELECT` to check existence first, then choose a
>  plain `INSERT` (no `ON CONFLICT`) or a plain `UPDATE` -- never a
>  combined upsert on this table. A single successful INSERT reports
>  `changes` > 1 because of FTS trigger fan-out; that is expected, not a
>  duplicate-row bug.
> 4. **All non-Cloudflare/non-native IPFS pinning services (Filebase,
>  Pinata, Lighthouse, web3.storage, w3up) are DEPRECATED as of this
>  version and MUST NOT be used or referenced as an action item.** Per
>  explicit product direction: IPFS distribution for QNFO publications
>  uses ONLY (a) Cloudflare R2 as the durable byte-store, (b) a locally
>  computed CIDv1 (sha2-256, raw codec, base32) for content-addressing
>  with no third-party pinning dependency, and (c) Cloudflare DNS
>  DNSLink TXT records (`_dnslink.<slug>.qnfo.org` -> `dnslink=/ipfs/<CID>`)
>  as the sole naming/distribution layer -- verified via
>  `nslookup -type=TXT _dnslink.<slug>.qnfo.org` and (once propagated)
>  `https://dweb.link/ipns/<slug>.qnfo.org` or `https://cloudflare-ipfs.com`.
>  Every prior "Filebase primary / Lighthouse secondary" instruction in
>  this skill is now VOID -- see the rewritten IPFS section below.
> 5. **PowerShell inline `python -c "..."` is now a HARD BLOCK, not just an
>  anti-pattern note.** This exact session lost >15 tool calls to
>  `SyntaxError: unterminated string literal` / `The '<' operator is
>  reserved` from inline quoting collisions between PowerShell's parser
>  and Python string literals containing `"`, `<`, `>`, or JSON braces.
>  The `write` -> `exec <file>.py` -> delete pattern (kaizen fix B1,
>  already documented below) is MANDATORY for any Python beyond a
>  zero-quote one-liner -- treat any `python -c` call containing a
>  quote character, an angle bracket, or a dict/JSON literal as
>  guaranteed to fail and write a file first without even attempting it.

> **v2.9 UPDATE (2026-07-21, Zenodo credential incident):** Added the
> **Zenodo Credential Protocol** section (in Phase 5, immediately before
> "Zenodo Upload") after a session diagnosed ~15 false "token dead /
> read-only scope" 403s that were actually caused by manually
> retyping/reconstructing a token from a truncated terminal display,
> introducing a one-character transcription error invisible by symptom.
> New scripts: `scripts/zenodo-token-check.py` (run FIRST on any Zenodo
> 403 -- distinguishes real scope problems from credential-transcription
> errors in one call), `scripts/zenodo-create-upload.py` and
> `scripts/zenodo-metadata-publish.py` (canonical create/upload/
> metadata/publish pipeline, replacing ad hoc inline scripts, with
> built-in live-DOI verification). Required token scopes documented:
> `deposit:write`, `deposit:actions`, `user:email`.

> **v2.7 UPDATE (2026-07-20, Pinata quota exceeded) -- SUPERSEDED BY v2.10:**
> Pinata IPFS pinning removed. The v2.7 replacement (Filebase primary,
> Lighthouse secondary) is ITSELF now deprecated as of v2.10 -- see the
> v2.10 banner above and the rewritten IPFS/DNSLink section below. ALL
> third-party IPFS pinning services (Pinata, Filebase, Lighthouse,
> web3.storage, w3up, etc.) are out of scope for QNFO publications. Use
> ONLY Cloudflare R2 + locally-computed CIDv1 + Cloudflare DNS DNSLink.

> **v2.6 UPDATE (2026-07-20, kaizen audit):** Added `scripts/unicode-latex-preprocess.py` (fixes XeLaTeX Unicode-glyph and `keywords:`-field build failures -- A1/A2), `scripts/check-pdf.py` (PyMuPDF preflight + file-lock-safe replace -- B4/B5), `scripts/credential-scan.py` (pre-commit + pre-publish token leak scanner -- A4/C1/D2) wired into the Phase Closeout Protocol STEP 0.5 and the Publication Language Gate, `templates/gitignore-research-project-template.txt` for new project repos, a PROVENANCE-BUNDLE.zip hard gate before Zenodo upload (A3), `.zenodo_versions.json` version-chain tracking convention (C2), a Vectorize confirmation-bias disclosure requirement (C3), a multi-pinner IPFS fallback order Pinata→Filebase→Lighthouse (C4), documented Windows/PowerShell anti-patterns for inline `python -c`, `&&` chaining, and `curl` aliasing (B1/B2/B3), a YAML `---` delimiter conflict check (D3), an auto-discover related_identifiers KG query step (D4), a tag-backfill check in Phase Closeout (D1), and an Obsidian/external-path source material limitation note (C5/D5).

> **v2.5 UPDATE (2026-07-19): Added OSF Project Registration (Phase 5.5) for major research with falsifiable predictions. Added P11 (OSF GATE-CONDITIONAL) to Pre-Flight checklist. OSF policy: all resources public by default, API-only automation, external links (Zenodo/GitHub/IPFS) replace file uploads NEVER require manual browser interaction.

> **v2.4 UPDATE's R2-Immediate-Write + Per-Turn Checkpoint Protocol (per-turn R2 sync, phase-end GitHub push + Zenodo version, session/project-conclusion IPFS pin + social promotion for FINAL deliverables only).

> **Merges 6:** research-pipeline + deep-research + publication-publisher + buffer-integration + seo-discoverability + ipfs-web3
> **v2.2 UPDATE (2026-07-18):** Merged in Phase 0 (Project Initialization), Pre-Flight Checklist (P1-P11), Cross-Skill Integration Checklist, Phase Closeout Protocol, Deliverable Registry / Risk Register templates, and Version Tagging Protocol (previously drafted as a separate, since-retired `research-v2` duplicate skill -- consolidated here as the single canonical research skill).
> **v2.3 UPDATE (2026-07-18):** Added mandatory REPO-TARGET GATE (`git remote -v` check) before every tag/commit/release in Phase 0 and the Phase Closeout Protocol, following ADR-026 Incident 3 (a prior session's Phase Closeout tags -- `v0.1-phase0`, `v1.0.0`, etc. -- plus a Zenodo-DOI GitHub Release were mistakenly created inside `qnfo-skills` instead of the project's own repo, requiring backup+delete remediation).
> **Related:** Always load `knowledge` for KG/D1 discovery. Load `cloudflare` for deployment to Pages/R2/D1/Workers. Load `git-github` for Phase 0 init and every phase closeout.
> **Cloudflare Full-Stack:** All publication artifacts live on R2 + D1 + Workers. Zenodo is external archival. Buffer is social dissemination.

## execute_plan

update_plan([
 {"step": "Phase 0: Project Initialization -- repo, scaffold, WBS, core claim lock", "status": "pending"},
 {"step": "Pre-Flight: Run P1-P11 checklist -- HARD gates must pass before Phase 1", "status": "pending"},
 {"step": "Phase 1: Due Diligence -- query KG + D1 + Vectorize + external sources", "status": "pending"},
 {"step": "Phase 2: Literature Search -- 5 parallel sources, dedup, classify core/supporting/background/reject", "status": "pending"},
 {"step": "Phase 3: Citation Management -- extract citations, verify BibTeX, auto-generate missing DOIs", "status": "pending"},
 {"step": "Phase 4: Deep Research -- structured forecast protocol (mandatory, scope-scaled; produces forecast artifacts)", "status": "pending"},
  {"step": "Phase 5: Publication — format paper, build PDF, BP-1 fit-verify, BP-2 terminology audit, BP-3 density gate, Zenodo upload with DOI", "status": "pending"},
 {"step": "Phase 6: Deploy -- D1 living-paper insert, papers-server Worker verification", "status": "pending"},
 {"step": "Phase 7: Disseminate -- SEO audit, Buffer social media, papers.qnfo.org verification", "status": "pending"},
  {"step": "Phase 8: Core Distribution — GitHub push + tag, Zenodo new-version, R2 archive sync, D1/KG records, BP-4/BP-5 correction protocol (if erratum)", "status": "pending"},
])

**Note:** Phase 0 and the Pre-Flight checklist apply to net-new, long-lived research projects (new repo, new WBS). For a single paper/update within an existing project, skip directly to Phase 1.

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — MANDATORY, 2026-07-21)

This skill already carries extensive per-phase verification gates (BibTeX
audit, PDF rendering check, DOI resolution, papers-server HTTP 200, etc.).
This section is the umbrella rule they all serve: **no remote publication
action — Zenodo deposit, GitHub push/tag/release, R2 upload, D1
living-paper insert, OSF registration, Buffer post — may be reported as
successful without an INDEPENDENT re-query of the live state in the SAME
turn.** An API's immediate `"success": true`/`201 Created` response is the
FIRST signal, not the LAST — it confirms the request was accepted, not
that the artifact is durably live and correct.

1. **Zenodo** — never report "published" from the create/publish API response alone. Wait for indexing, then verify via `curl -sI https://doi.org/10.5281/zenodo.<id>` returning HTTP 200 (not the Zenodo API's own state field).
2. **Git push** — verify via an independent GitHub API query (`GET /repos/{owner}/{repo}/commits/{sha}`) or `git ls-remote origin <branch>`, not the local push exit code alone.
3. **R2 upload** — download the file back (`wrangler r2 object get ... --remote`) and compare size/hash to the source.
4. **D1 living-paper / KG inserts** — re-run a `SELECT`/`/neighbors` query and show the row/edge actually present.
5. **OSF registrations** — confirm via `GET /v2/registrations/{id}/` showing the real `date_registered`/`pending_registration_approval` state, never assert "registered" from the POST response body alone.
6. **Any claim this session already reported success on** — if closing out or continuing a prior session's claim, re-verify live state before repeating the claim; a prior turn's phantom claim propagates if not re-checked (see memory: never trust a remote action as successful without confirming actual server-side state).
7. If live re-verification cannot be run in this turn, the response MUST read `[NOT-VERIFIED: reason]` instead of "published"/"deployed"/"live"/"confirmed".

---

## Phase 0: Project Initialization (BLOCKING GATE for new projects)

> **HARD GATE:** Phase 1 MUST NOT begin until all Phase 0 deliverables are committed.

### 0.1 Repository and Infrastructure

Standard directory scaffold:
```
<project-slug>/
├── README.md
├── PROJECT-PLAN.md
├── .gitignore
├── docs/      # Source documents, prior work
├── artifacts/    # Literature reviews, gate memos, test results
├── notebooks/    # Working notes, calculation notebooks
└── releases/    # Versioned Zenodo-ready bundles
```

Git init on feature branch (NEVER main/master). Create GitHub repo via `gh repo create`.

**`.gitignore` (kaizen fix A4):** copy `templates/gitignore-research-project-template.txt`
into the new project's `.gitignore`. It excludes `_*.py`/`_*.js` (ephemeral
scripts frequently contain hardcoded tokens during development), `.env`,
`*.token`, `keys.json`, and standard build/OS noise. A project repo is NOT
the qnfo-skills allowlist repo -- it needs its own permissive `.gitignore`,
not the skills repo's default-deny one.

**REPO-TARGET GATE (HARD, MANDATORY — check before `git init`/`git tag`/`gh repo create`):**
```
git remote -v  # or: git -C <target-dir> remote -v
```
Verify the remote/working directory is the project's OWN repo
(`QNFO/<project-name>` or `QNFO/qnfo-research`) — **NEVER `QNFO/qnfo-skills`.**
`qnfo-skills` is a skills-only repo (ADR-026) and its tags/releases are
reserved for skill versioning, never research project phases. This check
applies to every step in this skill that creates a git tag, commit, or
GitHub Release — not just Phase 0. Verify the repo target FRESH each time;
do not assume a prior verification still holds after switching directories,
subagent delegation, or a long session. **A single misdirected `git tag` or
`gh release create` inside qnfo-skills is a policy violation that requires
full remediation (backup + delete + audit) — see ADR-026 Incident 3.**

### 0.2 Project Plan and WBS

Write `PROJECT-PLAN.md` with: Charter, Phases with WBS, Milestones with gate criteria, Deliverable Registry (see `templates/deliverable-registry-template.md`), Risk Register (see `templates/risk-register-template.md`), Success Criteria, Version History.

### 0.3 Core Claim Lock

If project audits/evaluates a claim: restate in logically valid, falsifiable terms. Document original AND reformulation if original had errors. Lock in `PROJECT-PLAN.md §1.2`.

### 0.4 Knowledge Graph / Memory Seed

Query KG for existing related papers/projects. Log novel project to working memory.

### 0.5 Closeout

Execute Phase Closeout Protocol (below). Tag: `v0.1-phase0`.

**Source material path limitation (kaizen fix C5):** if source materials
(e.g. Obsidian vault notes) live outside the workspace/allowed directories
(e.g. `D:\Obsidian`), `glob`/`read` cannot access them directly. This is a
platform limitation, not a bug to work around silently -- document it and
ask the user to either (a) copy the specific files into the project
workspace, or (b) run an `exec` command with an explicit `cwd` pointing at
the external path if the environment permits Full Access mode. Do not
assume such files don't exist just because a glob search returns empty.

---

## Pre-Flight Checklist (BLOCKING -- runs before Phase 1)

**HARD GATE:** Every item marked HARD must pass before Phase 1 begins.

| ID | Check | Gate | How to Verify |
|---|---|---|---|
| **P1** | Git repo initialized on feature branch? | HARD | `git branch --show-current` != main/master |
| **P2** | GitHub remote configured and pushed? | HARD | `git remote -v` shows origin; `gh repo view` succeeds |
| **P3** | Directory structure created? (`docs/`, `artifacts/`, `notebooks/`, `releases/`) | HARD | Directory listing shows all 4 dirs |
| **P4** | `PROJECT-PLAN.md` written with charter, WBS, milestones, deliverables, risks? | HARD | All 6 sections populated; no placeholder text |
| **P5** | `README.md` written with project overview? | SOFT | File exists with name, status, quick start |
| **P6** | Core claim reformulated and locked (if applicable)? | HARD | `PROJECT-PLAN.md §1.2` contains locked, logically valid formulation |
| **P7** | `.gitignore` present? | SOFT | File exists covering IDE, OS, build artifacts |
| **P8** | Phase 0 committed, tagged, and pushed? | HARD | `git tag -l 'v0.1*'` returns tag; `git log -1 --oneline` shows Phase 0 commit |
| **P9** | Project logged to Knowledge Graph / working memory? | SOFT | Memory recall returns project entry |
| **P10** | Cross-skill integration checklist reviewed? | SOFT | All relevant skills loaded per integration table |
| **P11** | OSF project created for qualifying research? (MAJOR projects ONLY — skip for exploratory studies, single papers, or minor updates) | SOFT-CONDITIONAL | OSF API: project public, components linked to Zenodo/GitHub, registration drafts created. File upload via API NOT supported — use external links (Zenodo DOI, GitHub raw) instead. NEVER require manual browser interaction. ALL OSF resources must be public. |

**If any HARD gate fails:** BLOCK research launch. Fix the gap and re-run.

---

## Cross-Skill Integration Checklist

| Skill | Load at Phase | Purpose |
|---|---|---|
| `git-github` | **0** (init), every closeout | Branch discipline, conventional commits, repo creation |
| `knowledge` | **0** (KG seed), **1** (DD), every closeout | KG queries, D1 cross-reference, project state logging |
| `cloudflare` | **6** (deployment), **8** (distribution) | R2 archive, D1 insert, Worker verification, **MUST consult §MCP-Driven Operations decision matrix** for MCP-first verification (observability, builds, auditlogs, bindings, graphql, dns-analytics) |
| `research` | **All phases** | This skill -- the master pipeline |
| `memory-management` | **0**, every closeout | Durable memory logging |
| `documents` / `pdf` | **5** (publication) | PDF building, document formatting |
| `system` | **0** (if Desktop automation needed) | App configuration |
| `git-github` (OSF addendum) | **2-5** (qualifying projects only) | OSF project creation, components, registration drafts, external file links |

---


## Forecast Integration Map (MANDATORY reference)

The Structured Forecast Protocol (Phase 4) is NOT an isolated phase — its outputs feed
into every other phase of the research pipeline. This map makes the integration explicit
so agents never treat forecasting as a standalone deliverable to be "checked off."

| Forecast Output | Feeds Into | Integration Rule |
|:----------------|:-----------|:-----------------|
| **Stage 0: Domain Assessment** | Phase 1 (Due Diligence), Phase 2 (Literature) | Domain topology informs search queries and gap analysis |
| **Stage 1: Candidate Ranking** | Phase 5 (Publication §Introduction) | Qualitative ranking drives the paper's narrative arc — "we assess the candidates comparatively" |
| **Stage 2: Assumption Audit** | Phase 5 (Publication §Body) | Enabling/blocking assumptions become the paper's analytical backbone — "underlying this candidate are three critical assumptions" |
| **Stage 3: Red-Team Challenge** | Phase 5 (Publication §Discussion) | Adversary positions become the paper's limitations section — "we examined challenges from multiple adversarial perspectives" |
| **Stage 4: Judgment Sensitivity** | Phase 5 (Publication §Discussion) | Robustness statement informs the paper's confidence calibration — [ROBUST]/[CONDITIONAL]/[FRAGILE] |
| **Stage 5: Calibration Register** | Phase 5 (Publication), Phase 8 (Distribution) | Dated, strength-weighted predictions become the paper's falsifiable claims — [STRONG]/[WEAK] anchors |
| **Stage 6: Effort Allocation** | Phase 0 (Project Plan §Risk Register), Phase 5 (Publication §Future Work) | Informs resource prioritization and future-work recommendations |
| **Stage 7: Strategic Memo** | Phase 5 (Publication §Abstract + Conclusion) | Executive synthesis becomes the paper's thesis statement |
| **Stage 8: Cross-Review** | Phase 5 (Publication §Declarations) | Reviewer findings inform the "Use of Artificial Intelligence" declaration |
| **Consilience Gate (KIF-29)** | Phase 1 → Phase 4 (Stage 1), Phase 2, Phase 5 | Synthesis Consilience becomes an additional Stage 1 candidate; Lexicon terms expand Phase 2 search queries; Cross-Domain table becomes a Phase 5 section |
| **Stage 9: Practical Applications** | Phase 5 (Publication §Applications), Phase 8 (Distribution) | Maps each forecast candidate/era onto concrete application domains with falsifiable claims; generates additional calibration register entries |
| **Stage 10: Counterfactual Backcasting** | Phase 5 (Publication §Discussion/Backcast), Phase 8 (Distribution) | Systematic backcasting across target disciplines with tiered historical forks; produces counterfactual technology stack tables and calibration register entries |

**Design principle:** Forecasting is not a separate "module" bolted onto research — it is the
analytical engine that generates the paper's claims, structure, and falsifiable predictions.
The agent should think of Phase 4 not as "now we do forecasting" but as "now we generate the
substantive content that Phases 5-8 will publish." Stages 9 and 10 extend this: Stage 9 makes
the forecast actionable by grounding it in concrete domains; Stage 10 stress-tests it by
imagining alternative evolutionary paths. The PUBLICATION PRINCIPLE (Phase 4 header)
enforces this: the reader sees good analysis, not methodology signage.


## Phase Closeout Protocol (MANDATORY -- every phase, for net-new projects with a dedicated repo)

**STEP 0 (HARD GATE, run FIRST, every single time -- no exceptions):**
```
git remote -v
```
Confirm the remote URL is the PROJECT's own repo (`QNFO/<project-name>` or
`QNFO/qnfo-research`). If it shows `QNFO/qnfo-skills` -- STOP. Do not commit,
tag, or create a release. `cd` to the correct project directory first. This
single check prevents the exact failure mode documented in ADR-026 Incident 3
(research phase tags `v0.1-phase0`, `v1.0.0`, etc. and a Zenodo-DOI GitHub
Release were mistakenly created inside `qnfo-skills`, requiring a full
backup+delete remediation).

**STEP 0.5 (HARD GATE, kaizen fix A4/C1/D2 -- credential pre-commit scan):**
```bash
python <research-skill-path>/scripts/credential-scan.py --staged
```
Run this AFTER `git add` and BEFORE `git commit`. If it exits non-zero,
BLOCK the commit, remove the hardcoded secret (move to env var or a
`~/.{service}_token` file), re-stage, and re-scan. GitHub push protection
will otherwise reject the push after the fact -- catching it pre-commit
avoids a rewritten-history remediation.

```
1. COMMIT: git add <phase-artifacts> ; python <research-skill-path>/scripts/credential-scan.py --staged ; git commit -m "ACTION:CREATE FILE: <files> RATIONALE: Phase N complete"
2. TAG:   git tag v<major>.<minor>-<phase-slug> -m "Phase N: <description>"
3. PUSH:  git push origin <feature-branch> --tags
4. VERIFY: git log -1 --oneline && git branch --show-current && git status --short
5. LOG:   memory_remember(content="Phase N completed. Deliverables: <list>.")
6. TAG-BACKFILL-CHECK (kaizen fix D1): git tag -l 'v*' # confirm ALL prior
  phase tags exist -- a missing tag from an earlier phase (e.g. Phase 0's
  v0.1-phase0 never created) should be discovered and backfilled NOW, not
  discovered later during an audit.
```
*(Windows PowerShell note -- kaizen fix B2: use `;` to chain commands, not
`&&`. `cmd /c "cmd1 && cmd2"` also works but breaks on inner quoting; prefer
`;` or separate sequential tool calls.)*

### Version Tagging Protocol

| Phase | Tag Pattern | Example |
|---|---|---|
| 0 -- Init | `v0.1-phase0` | `v0.1-phase0` |
| 1 -- Due Diligence | `v0.2-phase1-dd` | `v0.2-phase1-dd` |
| 2 -- Literature | `v0.3-phase2-lit` | `v0.3-phase2-lit` |
| 3 -- Citations | `v0.4-phase3-cite` | `v0.4-phase3-cite` |
| 4 -- Deep Research | `v0.5-phase4-deep` | `v0.5-phase4-deep` |
| 5 -- Publication | `v1.0` | `v1.0` (major version bump) |
| 6 -- Deployment | `v1.1-deploy` | `v1.1-deploy` |
| 7 -- Dissemination | `v1.2-disseminate` | `v1.2-disseminate` |
| 8 -- Core Distribution | `v1.3-distribute` | `v1.3-distribute` |

---

## Phase 1: Due Diligence -- Cross-Reference Discovery

### MANDATORY BEFORE ANY RESEARCH PIPELINE LAUNCHES

**(a) QNFO Cross-Reference Discovery:**
- Query KG: `query_graph({endpoint: \"stats\"})` for ecosystem overview
- Query KG: `query_graph({endpoint: \"query\", params: {query: \"MATCH (n) WHERE n.name CONTAINS '<topic>' RETURN n\"}})` for existing papers/projects
- Query D1: `get_paper_context({slug: \"<topic>\"})` and `search_papers({query: \"<topic>\", limit: 10})` via Vectorize
- Report: "QNFO Cross-Reference: Found N related papers, M active projects"

**(b) External Literature Search (MANDATORY):**
- arXiv API, OpenAlex (PRIMARY academic index — keyless), Crossref (DOI registry — keyless),
 Zenodo records API (`zenodo.org/api/records?q=...` — search OTHER users' deposits, keyless),
 Europe PMC (keyless), web search
- Deduplicate against QNFO papers from step (a)
- Report: "External Literature: Found N papers (M core, K supporting, J background)"

**(c) Gap Analysis:**
- Which aspects already covered by QNFO?
- What prior QNFO work should this build upon?
- Is the proposed research genuinely novel?
- If already covered -> flag `[DUPLICATE-WARNING: topic covered by existing QNFO publications <DOIs>]`

**GATE:** If (a) and (b) NOT executed -> research pipeline launch BLOCKED.

**Vectorize Confirmation-Bias Disclosure (kaizen fix C3, HARD when triggered):**
QNFO's Vectorize index currently contains ONLY QNFO-internal papers. If a
`search_papers` call returns results and ALL of them are QNFO-authored, this
is NOT external corroboration -- it is the corpus searching itself. Any
report claiming "confirmed by literature search" MUST distinguish:
`[QNFO-INTERNAL: N hits, self-referential]` vs `[EXTERNAL: M hits from arXiv/
OpenAlex/Crossref/Zenodo/EuropePMC/web]`. If external search step (b) was skipped or returned
zero results while internal search (a) returned nonzero, explicitly flag
`[CONFIRMATION-BIAS-RISK: only internal corpus searched]` in the due
diligence report -- do not silently present internal-only hits as validation.

### Institutional Status Neutrality Gate (KIF-16, HARD)

**BEFORE evaluating any claim from a self-published or non-peer-reviewed source:**

1. **Strip institutional metadata.** Do not consider: publication venue, peer-review status, author's institutional affiliation, citation count, h-index, or whether the work appears on arXiv vs Nature. These are social signals, not truth signals.

2. **Evaluate substance directly.** Extract the claim. Identify what evidence would support it. Identify what evidence would falsify it. Search for both.

3. **Never use "fringe" or "pseudoscience" as a classification.** These are social categories, not epistemic ones. Use instead:
  - `[UNFALSIFIABLE]` — no conceivable observation would disconfirm this
  - `[CONTRADICTS ESTABLISHED EVIDENCE: <specific evidence>]` — name the evidence
  - `[UNTESTED]` — falsifiable but no relevant experiments exist
  - `[CONTESTED: <specific debate>]` — active scientific disagreement exists

4. **Open science is real science.** Zenodo, SSRN, ResearchGate, arXiv, and personal websites are legitimate publication channels. Many paradigm-shifting papers (Einstein 1905, Bell 1964, Aspect 1982) were initially self-published or preprinted. Lack of traditional peer review is NOT a heuristic for unreliability.

**GATE:** If any investigation document contains the words "fringe," "pseudoscience," "crank," or "crackpot" without an accompanying `[CONTRADICTS ESTABLISHED EVIDENCE: <specific>]` citation → BLOCKED. Revise to use epistemic categories, not social categories.

### AI Convergence Bias Disclosure (KIF-17, HARD when triggered)

**If the investigation references or incorporates evaluations from multiple AI systems:**

1. **Convergence is NOT validation.** If Claude, Gemini, GPT, and other AI systems all converge on the same evaluation of a claim, this does NOT constitute independent confirmation. All large language models share overlapping training data (web text, academic papers, Wikipedia) that encodes "mainstream consensus" as the default position.

2. **Flag convergence explicitly.** If 2+ AI evaluations agree on dismissing a claim, append:
  ```
  [AI-CONVERGENCE-WARNING: Multiple AI systems converged on this evaluation.
  This may reflect shared training-data priors rather than independent analysis.
  AI systems systematically underweight paradigm-challenging claims because
  "mainstream consensus" is overrepresented in training corpora.]
  ```

3. **Do not treat AI dismissal as authoritative.** An AI saying "this contradicts Bell's theorem" is a STARTING POINT for investigation, not a CONCLUSION. Verify: Does the claim actually contradict Bell's theorem, or does it invoke a known loophole (measurement independence, superdeterminism, retrocausality)? AI systems often oversimplify technical debates.

4. **The meta-lesson:** The PQS session (2026-07-24) failed because the agent uncritically replicated AI dismissals from source conversations instead of investigating the claims directly. The user had to explicitly intervene: "THE SCOPE IS NOT TO EVALUATE ALL 'FRINGE' CLAIMS... BUT TO INVESTIGATE IT SERIOUSLY AND WITHOUT EDITORIALIZING."

### Cross-Domain Consilience Gate (KIF-29, SOFT)

**Trigger (SOFT GATE):** Run this gate during Phase 1 if ANY of:
- The research question spans 2+ recognisable domains (physics + CS, cognition + biology, etc.)
- The core claim uses domain-specific terminology with no external analogues identified
- The project is explicitly tagged as "consilience," "cross-domain," or "interdisciplinary"

**Purpose:** Every concept carries structural isomorphisms across disciplines. What appears as "a valuation" in number theory is "a measurement" in physics, "a constraint check" in CS, "a threshold" in cognition, "a fitness function" in biology, and "a norm" in sociology. Without systematic cross-domain translation, research stays siloed — producing internally coherent papers that miss the consilience discovery. This gate ensures the agent does not merely search within the source domain but actively maps the core claim onto structurally analogous domains.

**Protocol:** Produce a compact 6-domain translation using this template. The output is stored in `artifacts/consilience-gate.md` for the project record.

```markdown
# Cross-Domain Consilience Audit: [Core Claim]

## Core Dynamic
[One jargon-free sentence: what does the claim *do* — classify, bind, transform, constrain, measure?]

## Cross-Domain Lexicon
| Source Term | Physics | CS | CogSci | InfoTheory | Biology | Sociology |
|:------------|:--------|:---|:-------|:-----------|:--------|:----------|
| [term 1]  | ... | ... | ... | ... | ... | ... |
| [term 2]  | ... | ... | ... | ... | ... | ... |
| [term 3]  | ... | ... | ... | ... | ... | ... |

## Domain Translations
### Physics
- **Lexicon:** [1-2 terms: energy, field, phase space, symmetry, gauge...]
- **Instance:** [1 concrete physical system/law that embodies the same dynamic]
- **Ramification:** [1 testable implication — what measurement or experiment follows?]

### Computer Science
- **Lexicon:** [1-2 terms: data structure, algorithm, type system, complexity class...]
- **Instance:** [1 concrete computing system, protocol, or architecture]
- **Ramification:** [1 testable implication — impact on computability, scaling, verification?]

### Cognitive Science
- **Lexicon:** [1-2 terms: perception, memory, learning, attention, mental model...]
- **Instance:** [1 concrete reasoning pattern, illusion, or neural behaviour]
- **Ramification:** [1 testable implication — effect on induction, category formation, bias?]

### Information Theory
- **Lexicon:** [1-2 terms: entropy, mutual information, channel capacity, coding...]
- **Instance:** [1 concrete coding scheme or noisy-channel phenomenon]
- **Ramification:** [1 testable implication — effect on signal integrity, rate-distortion?]

### Biology
- **Lexicon:** [1-2 terms: evolution, homeostasis, signalling, niche, plasticity...]
- **Instance:** [1 living system, evolutionary dynamic, or regulatory network]
- **Ramification:** [1 testable implication — what would be selected for/against?]

### Sociology
- **Lexicon:** [1-2 terms: norms, institutions, network dynamics, power, collective behaviour...]
- **Instance:** [1 concrete social phenomenon — diffusion, polarisation, isomorphism]
- **Ramification:** [1 testable implication — impact on resilience, inequality, coordination?]

## Synthesis Consilience
**Meta-Principle:** [One statement: what is invariant across all 6 translations?]
**Frontier Question:** [One question: what assumption, if relaxed, would unify two previously separate domains?]

## Research Integration
- **Scoping:** [How the Lexicon generates new hypotheses or reveals blind spots]
- **Deep Dive:** [How to design a model/simulation/experiment testing the cross-domain analogy]
- **Execution:** [How to build a prototype/intervention/policy based on the Synthesis]
```

**Gate check:** If a qualifying research project reaches Phase 2 without this audit existing in `artifacts/consilience-gate.md`, flag `[DOMAIN-SILOED: cross-domain consilience gate skipped on qualifying research]` in the due diligence report. This is a SOFT gate (does not block Phase 2), but its absence must be explicitly noted and justified ("single-domain research, no external analogues identified after explicit check" is a valid justification).

**Integration with later phases:**

| Phase | Integration |
|:------|:------------|
| **Phase 2 (Literature)** | Use each translated Lexicon term as an additional search query in the corresponding domain. Example: if the physics Instance is "phase transition," search biology for "phase transition in gene regulation" and sociology for "tipping points in collective behaviour." |
| **Phase 4 (Deep Research)** | Feed the Synthesis Consilience meta-principle into Stage 1 (Paradigm-Shift Candidate Identification) as an additional candidate. The Frontier Question becomes a Stage 5 Calibration Register entry. |
| **Phase 5 (Publication)** | The Cross-Domain Lexicon table is publication-ready. The Synthesis Consilience becomes the paper's unifying thesis or a dedicated "Cross-Domain Implications" section. |

**Anti-pattern:** Running this gate on research that genuinely operates within a single domain and forcing strained analogies. The gate is for *qualifying* cross-domain research — if the Lexicon produces only trivial or forced mappings (e.g., "this quantum operator is like... a social norm because both are rules"), mark `[CROSS-DOMAIN-NOT-APPLICABLE: no non-trivial structural isomorphisms found across domains]` and move on. The absence of a consilience finding is itself a valid result.

---

## Phase 2: Literature Search & Triage

### Multi-Source Search (query in parallel)

| Source | Method | Purpose |
|:-------|:-------|:--------|
| **OpenAlex API** | `https://api.openalex.org/works?search=<query>&per-page=N&mailto=<email>` — no key; add `mailto` for polite pool | PRIMARY academic index (~250M works, abstracts, DOIs, arXiv IDs, citation counts) |
| **Zenodo records API** | `https://zenodo.org/api/records?q=<query>&size=N` — no key | **Search OTHER users' deposits** (datasets, software, papers) — Zenodo is a discovery source, not just an upload target |
| **Crossref API** | `https://api.crossref.org/works?query=<query>&rows=N&mailto=<email>` — no key | DOI registry: verified metadata, journal articles, DOI-first dedup |
| **Europe PMC API** | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<query>&format=json&pageSize=N` — no key | Life-sciences/health literature (PubMed Central + preprint aggregation) |
| **arXiv API** | `http://export.arxiv.org/api/query?search_query=<query>` | Preprint search |
| **Web search** | Browser (`load_url`) or `exec` with `curl` | Broader discovery |
| **QNFO Vectorize** | `search_papers({query: \"...\", limit: 10})` | Existing QNFO corpus semantic search |
| **QNFO Knowledge Graph** | `query_graph('query', {query: 'MATCH (p:Paper) WHERE ...'})` | Related QNFO concepts |

### Research API Rate-Limit Matrix (v2.36 — VERIFIED 2026-07-31)

| API | API Key | Rate-Limit Profile | Verdict |
|:----|:--------|:-------------------|:--------|
| **Semantic Scholar** | Optional (higher limits with key) | HTTP 429 under sustained load WITHOUT a key; session-verified failure | **RETIRED as primary** — do not block Phase 1/2 on it |
| **OpenAlex** | **NONE** | Keyless; polite pool with `mailto` param; sustained back-to-back queries OK | **PRIMARY** — verified HTTP 200 ×4 back-to-back, 0 × 429 |
| **Crossref** | **NONE** | Keyless; polite pool with `mailto` param; documented ceiling ~50 req/s (guidance, not session-measured) | **MANDATORY SUPPLEMENT** — verified HTTP 200 ×4 |
| **Zenodo records** | **NONE** (search); token only for deposit writes | Keyless search, generous; 429 documented only as an error code, not observed | **MANDATORY SUPPLEMENT** — verified HTTP 200 ×4 |
| **Europe PMC** | **NONE** | Keyless; generous; no observed throttling | **SUPPLEMENT** — verified HTTP 200 ×4 |

**Rule (v2.36):** If a search source returns 429 twice in a row, do NOT retry
aggressively — switch to OpenAlex/Crossref/Zenodo/EuropePMC for that query and
flag `[RATE-LIMIT-OVERRIDE: <source> 429, substituted <replacement>]` in the
due diligence report. Semantic Scholar may be consulted opportunistically with
its free tier but MUST NOT gate the pipeline. (Cross-ref: durable heuristic
"Semantic Scholar 429 — use hybrid fallback strategy", created 2026-07-31.)

**Polite-pool etiquette (v2.36):** add `&mailto=<email>` to OpenAlex and
Crossref requests to enter the polite pool; keep ~0.4s between back-to-back
queries. arXiv: keep ~3s between requests (documented interval, not measured).
**Exact-phrase vs tokenized search (v2.36):** unquoted Zenodo `q=` queries
OR-tokenize — `q=JPCUB joules per computational unit` returned total=311,162
while quoted `q="JPCUB"` returned total=2 (the true novelty count). For
exact-novelty checks use quoted phrases on Zenodo and
`filter=title.search:TERM` on OpenAlex. (Evidence: `zenodo_jpcub.json` vs
`zenodo_exact.json` in jpcub-validation artifacts.)

**Evidence discipline (v2.36):** save every API response to
`artifacts/external-search/<api>_<query>.json` and cite the file for every
count/DOI claimed (KIF-55). Never report a count without its evidence file.

### Deduplication Protocol
1. Normalize DOIs (lowercase, strip `https://doi.org/` prefix)
2. Normalize titles (lowercase, strip punctuation, normalize whitespace)
3. Match by DOI exact, arXiv ID, or title similarity (>90% cosine)
4. Flag duplicates, keep canonical source (OpenAlex preferred; Crossref for DOI-first verification)
5. Report: "Found N raw papers, M unique after deduplication"

### Classification Matrix

| Class | Definition | Min | Max | Action |
|:------|:-----------|:----|:----|:-------|
| **Core** | Directly addresses research question with relevant methodology | 5 | 10 | Deep read, extract all citations |
| **Supporting** | Adjacent work, citations, related methods or domains | 10 | 20 | Read abstract + methods, extract key citations |
| **Background** | Context, related domains, foundational texts | 5 | 15 | Skim, note for bibliography |
| **Reject** | Irrelevant, retracted, predatory journal, or duplicate | -- | -- | Archive with reason |

### Reading Protocol
For each Core paper: read full text, extract 3-5 key claims, note methodology, identify assumptions, flag fabrication risk.
For each Supporting paper: read abstract + methods + conclusions, note relevance to RQ.

### Mandatory Symmetry Template (KIF-18, HARD)

Every literature review or investigation document MUST include BOTH of the following section headings, populated with actual content:

```markdown
## Where External Literature Supports [Claim/Framework]

[Enumerate specific papers, experiments, or theoretical results that are
consistent with or supportive of the claim being investigated. Include DOIs.]

## Where External Literature Constrains or Contradicts [Claim/Framework]

[Enumerate specific papers, experiments, or theoretical results that
constrain, limit, or contradict the claim being investigated. Include DOIs.
This section MUST NOT be empty or contain only hedging language.]
```

**GATE:** If a literature review contains a "Supporting" section but no "Constraining" section (or vice versa) → BLOCKED. Epistemic symmetry is structural, not optional.

**Anti-pattern:** "The literature is broadly supportive, with some minor caveats" is NOT a constraining section. Name specific constraining evidence or explicitly state `[NO CONSTRAINING EVIDENCE FOUND IN SEARCH: <search terms used>]`.

---

## Phase 3: Citation Management

### Citation Extraction
Extract citations from paper markdown using regex patterns:
- `[@author2022]` -- Pandoc-style citations
- `[1]`, `[2-5]` -- numeric citations
- `(Author, 2022)` -- APA inline citations
- `\\cite{key}` -- LaTeX citations

### BibTeX Verification
1. Parse `.bib` file, extract all entry keys and DOIs
2. Cross-reference citations extracted from paper against BibTeX entries
3. Flag: missing entries, missing DOIs, unused entries, malformed entries
4. Auto-generate missing BibTeX from DOIs via `https://doi.org/<DOI>` (Accept: application/x-bibtex)
5. Produce audit report: "Citations found: N, Matched: M, Missing: K, Unused: J"

### Script Pattern (ephemeral -- write, execute, delete)
```python
# _citation_audit.py
import re, sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
  paper = f.read()
with open(sys.argv[2], 'r', encoding='utf-8') as f:
  bib = f.read()

# Extract all citation keys from paper
paper_cites = set(re.findall(r'@(\w+)', paper))
bib_keys = set(re.findall(r'@\w+\{(\w+),', bib))

missing = paper_cites - bib_keys
unused = bib_keys - paper_cites
matched = paper_cites & bib_keys

print(f"Paper citations: {len(paper_cites)}")
print(f"BibTeX entries: {len(bib_keys)}")
print(f"Matched: {len(matched)}")
print(f"Missing from BibTeX: {len(missing)} -- {', '.join(sorted(missing))}")
print(f"Unused BibTeX entries: {len(unused)} -- {', '.join(sorted(unused))}")
```

---

## Phase 4: Deep Research & Structured Forecast (MANDATORY for all projects)

**Runs for ALL projects.** The scope scales: a single-result paper runs a lighter
version (assumptions enumerated, uncertainty ranges, sensitivity check, at least one
calibration prediction); a paradigm forecast runs the full protocol (all 11 stages).

**PUBLICATION PRINCIPLE (MANDATORY):** In research outputs — papers, PDFs,
abstracts, presentations — do NOT name the methodology. Do not write "We applied
a Structured Forecast Protocol" or "per Stage 4 sensitivity analysis." The reader
should see good analysis, not methodology signage. Bury the method in the prose:
- Instead of "Stage 2 Assumption Audit found..." write "Underlying this candidate are
 three critical assumptions: ..."
- Instead of "Qualitative Ranking from the forecast protocol" write "We assess the
 candidates comparatively: ..."
- Instead of "per the Calibration Register" write "We register the following
 dated, falsifiable predictions: ..."
- Instead of "red-teamed by five adversary positions" write "We examined challenges
 from multiple adversarial perspectives: ..."
The artifact file (`structured-forecast-protocol-v2.md`) documents the full analysis
method — cite it as a supplementary reference, not as a branded protocol.

**METHODOLOGY NOTE (v2.27):** This protocol is a structured judgment exercise — NOT a Bayesian computation. No formal Bayesian updating from data occurs. The probability numbers below are the analyst's structured judgments, loosely anchored to imperfect historical reference classes. They have wide uncertainty bands and must not be mistaken for empirically derived quantities. The protocol's primary value is in the **discipline it imposes**: making assumptions explicit, challenging each candidate, and registering dated, falsifiable predictions. The ranking output is qualitative with subjective probability ranges — not a computed expected value. The EV = P × I / √t formula used in prior versions is RETIRED; portfolio allocation is now based on qualitative ranking and judgment, not pseudo-optimal Kelly bets.

### Stage -1: Likelihood Calibration Protocol (HARD GATE, KIF-31)

**GATE:** Every P(E|H) or P(E|¬H) likelihood value > 0.80 assigned in Stage 2
MUST trace to at least one empirical calibration pillar BEFORE it enters the
structured forecast protocol. Likelihoods assigned without an anchor are "well-quantified
noise" — precise decimals communicating false quantitative precision for
what are fundamentally directionally informed human intuitions. 9 stages of
arithmetic on uncalibrated numbers produces rankings that reflect optimism
bias, not reality, and Stage 6's effort allocation then commits *real
resources* based on compounded intuitions.

**Calibration Pillars (at least one required per likelihood > 0.80):**

| Pillar | Operational Definition | Constraint |
|:-------|:----------------------|:-----------|
| **Empirical Base Rate** | Search literature for how often claims of the same type resolve to confirmed findings. Cite at least one meta-analysis or systematic review. | Value MUST fall within [baseRate × 0.5, baseRate × 2.0] |
| **Reference-Class Forecast** | Identify ≥3 closest historical scientific predictions of the same type, magnitude, and maturity as the target claim. Record their actual outcomes. | Likelihood MUST include justification drawn from the reference-class range |
| **Calibrated Subjective Confidence** | Before assigning any likelihood, complete a 15-minute calibration training run on ≥20 everyday-quantity questions (90% confidence intervals), measuring personal Brier score / overconfidence error. | If overconfidence > 0.15 Brier, adjust all likelihoods > 0.80 downward by factor (1.0 − overconfidence_error) |
| **Explicit Inter-Rater Reliability Anchor** | A REVIEWER subagent independently assigns the same likelihood without seeing the primary agent's value. Report the divergence. | If divergence > 0.15 and no consensus reached, use the MORE CONSERVATIVE value |
| **Unconditionally Known Prior** | A peer-reviewed empirical estimate exists (e.g., "discover 10 GeV supersymmetry" has a peer-reviewed prior from LHC null results). | Use directly. No pillar adjustment applied. |

**Protocol (run BEFORE Stage 2 assumption audit):**

1. For every assumption that will receive a P(E|H) > 0.80, identify which
  calibration pillar(s) apply. Document the anchor in
  `artifacts/likelihood-calibration.md` using the template below.
2. Run calibration training (≥20-question confidence interval quiz).
  Measure Brier score. If Brier > 0.15, apply the overconfidence adjustment
  factor to ALL likelihoods > 0.80 in this protocol.
3. Delegate the same assumptions to a REVIEWER subagent for independent
  assignment. If divergence > 0.15 on any assumption, use the more
  conservative value and flag the disagreement in the calibration report.
4. Any raw likelihood > 0.80 that CANNOT be anchored to an empirical pillar
  is **capped at 0.80** and labeled `[CALIBRATION-CAP: no empirical pillar
  for P > 0.80]`.
5. Calibration training is **mandatory** the first time any proposal passes
  through the full protocol. Subsequent proposals by the same agent
  may reuse the same calibration score if the training was completed within
  the same session or < 7 days prior.

**Required output: `artifacts/likelihood-calibration.md`**

```markdown
# Likelihood Calibration Audit: {project-slug}

## Assumption H1: {short statement}

| Parameter | Raw Estimate | Pillar | Anchor / Rationale | Calibrated |
|:----------|:-------------|:-------|:-------------------|:-----------|
| P(E1\|H1) | 0.90 | Empirical Base Rate | {citation}: X/Y claims of this type confirmed → base rate 0.72 | 0.75 |
| P(E1\|¬H1) | 0.20 | Reference Class | {3 historical cases with outcomes} | 0.15 |
| ... | ... | ... | ... | ... |

## Calibration Training Results
Brier score: {value} | Overconfidence error: {value} | Adjustment factor: {value}

## Inter-Rater Reliability
| Assumption | Agent Value | Reviewer Value | Divergence | Resolution |
|:-----------|:------------|:---------------|:-----------|:-----------|
| H1 E1   | 0.90 (raw) | 0.72      | 0.18    | Conservative (0.72) used |
```

**HARD GATE checks before Stage 2 may proceed:**
1. Every raw likelihood > 0.80 has a documented empirical pillar — or is
  capped at 0.80 with the `[CALIBRATION-CAP]` tag.
2. Calibration training Brier score recorded. If > 0.15, the adjustment
  factor has been applied to all > 0.80 likelihoods.
3. Inter-rater reliability report exists (REVIEWER subagent assigned every
  assumption independently).
4. `artifacts/likelihood-calibration.md` is committed before any Stage 2
  assumption table is populated.

**Integration with the protocol:** Calibrated likelihoods from Stage -1 are
the *only* values that enter Stage 2's Enabling Assumptions Table. Raw
(pre-calibration) values are recorded for transparency in the calibration
report but never flow into the protocol's judgment framework. Stage 4 sensitivity
analysis (see below) operates on the calibrated values and their documented
spans.

**Relationship to Stage 5 Calibration Register:** Stage -1 calibrates the
*inputs* to the protocol (the likelihood judgments). Stage 5 calibrates the *outputs*
of the protocol (the predictions). Both are required — calibrating inputs
without tracking outputs, or tracking outputs without calibrated inputs, is
each a half-measure that leaves the other half unverified.

### Stage 0: Domain Assessment
Map the field. Identify key research questions, active paradigms, methodological approaches. Produce domain topology map.

### Stage 1: Paradigm-Shift Candidate Identification
Identify highest-impact paradigm-shift candidates. Score candidates qualitatively on: probability (subjective, anchored to reference classes), impact (1-10 scale), timeline to mainstream, testability, and dependency chain. Produce a qualitatively ranked candidate list with uncertainty ranges and anchor reference classes explicitly stated. Do NOT compute an EV = P × I / √t — this formula is retired as of v2.27.

### Stage 2: Assumption Audit (MANDATORY -- 3 outputs)
1. **Enabling Assumptions Table:** For each candidate, enumerate all assumptions with confidence ratings. Use the assumption audit template.
2. **Blocking Assumptions:** What currently-true things must become false?
3. **Dependency Chain:** Which shifts must happen first? What enables what?

### Stage 3: Red-Team Adversarial Challenge
5 adversary roles challenge every assumption:
1. **Null-Hypothesis Defender:** "Nothing new here -- status quo explains everything"
2. **Methodology Skeptic:** "Your method is flawed -- here's why"
3. **Better-Alternative Proposer:** "X already does this better"
4. **Scaling Pessimist:** "Can't scale past N"
5. **Resource Realist:** "Would cost $Y and take Z years -- nobody will fund it"

### Stage 4: Judgment Sensitivity Analysis (v2.27 rewrite)

**Rationale:** The prior "Likelihood-Span Sensitivity Analysis" computed EVs from
subjective judgments and an arbitrary √t discount, producing false-precision numbers
(1.17, 0.71, 0.32) from armchair estimates. This replaces it with honest qualitative
robustness analysis — testing whether the QUALITATIVE ranking (A > B > C) survives
plausible perturbations of the analyst's judgments.

For each candidate:

1. **Judgment Span Perturbation:** Identify the judgment's documented uncertainty range
  (from Stage -1 calibration pillars). Test:
  - **Pessimistic scenario:** All judgments moved to their lower bounds
  - **Optimistic scenario:** All judgments moved to their upper bounds
  Does the qualitative ranking hold across both extremes? If the ranking reverses
  in EITHER extreme, flag the reversal explicitly — the ranking is NOT robust.

2. **Skeptical-priors stress test:** Halve all optimistic priors (retained from prior
  version — this tests whether the ranking survives if the analyst is systematically
  overconfident). If halving priors changes the ranking, the analyst is likely
  overconfident.

3. **Dependency correlation stress-test:** For candidates with shared prerequisites
  (e.g., B requires A; C requires A and B), test the correlated-failure scenario:
  if Candidate A fails, how severely do B and C degrade? Flag any cascade risk.

4. **Output:** Qualitative robustness statement:
  ```
  Ranking: A > B > C
  Robustness: [ROBUST] | [CONDITIONAL: <which perturbation flips it>] | [FRAGILE: <which perturbations flip it>]
  Pessimistic ranking: [A > B > C] or [reordered]
  Optimistic ranking: [A > B > C] or [reordered]
  Halved-priors ranking: [A > B > C] or [reordered]
  Key fragility: <the assumption whose perturbation most easily flips the ranking>
  ```

**IMPORTANT:** Do NOT compute numerical EVs (e.g., 1.17, 0.71, 0.32). The EV formula
(P × I / √t) is retired. If a prior cascade artifact still uses EV numbers, flag it
as `[V1-LEGACY: EV numbers are false-precision artifacts from v1 Bayesian Cascade —
replace with qualitative ranking per v2.27]`.

### Stage 5: Calibration Register (MANDATORY, KIF-54 strength-weighted)

For each non-obvious prediction, create a dated calibration entry with its
likelihood-anchor provenance visible — so post-hoc rationalizers cannot
later claim "we always knew this was a high-confidence prediction" when the
evidence pillar was a single agent's uncalibrated intuition:

```
[CHECK: 2030] By 2030, ______ should be observed if ______ is correct.
Likelihood-Anchor: {which Stage -1 pillar was used? Empirical Base Rate | Reference Class | Calibrated Subjective | Known Prior | NONE [CALIBRATION-CAP]}
Strength: [STRONG] | [WEAK]
Status: [PENDING]
Post-hoc risk: {what language a post-hoc rationalizer would use if this
        prediction fails}
```

**Strength tags:**
- **[STRONG]:** Likelihood anchored by Empirical Base Rate, Reference Class,
 or Known Prior — an external, verifiable, non-subjective pillar.
- **[WEAK]:** Likelihood anchored only by Calibrated Subjective Confidence
 or [CALIBRATION-CAP]'d — internal to the agent, even if calibration
 training reduced the bias.

This prevents post-hoc rationalization AND makes the prediction's epistemic
provenance visible to future readers — a prediction that failed despite a
STRONG likelihood anchor is a more interesting disconfirmation than one that
failed on a WEAK anchor.

### Stage 6: Research Effort Allocation

Resource allocation across candidates using qualitative ranking:
1. Rank all candidates by qualitative judgment (from Stage 1)
2. Allocate effort proportionally to ranking position, not to a computed EV
  (no EV formula exists as of v2.27)
3. Maintain a 10% hedge allocation for unknown candidates (anti-fragility floor)
4. **Output:** Research effort allocation table with qualitative justifications

**Important:** These percentages are research-effort heuristics, not Kelly-criterion
optimal bets. The domain is too uncertain for formal portfolio optimization. Do NOT
label them "Kelly-like" or compute them from EV ratios.

### Stage 7: Strategic Memo
Synthesize into a publication-ready strategic memo: executive summary, key findings, ranked recommendations, risk assessment, resource allocation.

### Stage 8: Cross-Review

A structured review by a REVIEWER subagent. **Important honesty note:** the reviewer
is a subagent of the SAME underlying model — this is a consistency and blind-spot
check, NOT independent inter-rater reliability in a statistical sense. The reviewer
challenges: Did the analysis miss a paradigm? Did it overfit to the current literature?
Are the judgment estimates consistent and well-reasoned? Are anchoring biases (e.g.,
hammer-sees-nail in the analyst's domain of expertise) identified and flagged?

---

### Stage 9: Practical Applications Extension (MANDATORY for all projects)

**Runs for ALL projects. Scope scales.** A single-result paper maps its forecast
onto 2-3 application domains; a paradigm forecast maps onto 5+ domains with
falsifiable claims per domain.

**Purpose:** The forecast protocol produces paradigm-shift candidates and
calibration predictions, but these are abstract — "sheaf-theoretic measurement
will be adopted by 2035." Stage 9 grounds every forecast candidate in concrete
operational domains, answering: "If this candidate is correct, what does it
enable that we cannot do today?" This prevents forecasts from remaining purely
theoretical and ensures every prediction has a practical face.

**Protocol:**

1. **Domain Mapping:** For each top-ranked forecast candidate (from Stage 1),
  identify 2-5 concrete application domains. The domains must be recognizable
  by practitioners — computation, AI/ML, measurement/metrology, communication,
  cryptography/security, energy, medicine, economics/finance, cognitive
  science, robotics, materials science, etc. If the candidate has no plausible
  practical application in any domain, flag it as `[PURELY THEORETICAL]` and
  note that its calibration timeline should be extended accordingly.

2. **Operational Signature:** For each candidate-domain pair, articulate the
  *operational signature* — the specific change in how practitioners work
  that the candidate enables. Example: "Era 10 (Contextual Enclosure) →
  quantum error correction: every error syndrome carries a context tag
  $(C, \Delta)$, making the cocycle condition a verifiable hardware check."

3. **Falsifiable Claims:** For each candidate-domain pair, produce at least
  one falsifiable claim that is testable in that domain.

4. **Calibration Register Entries:** Register at least one dated, strength-weighted
  prediction per domain cluster. These supplement Stage 5's general predictions
  with domain-specific falsifiable anchors.

5. **Cross-Domain Consilience:** If the Cross-Domain Consilience Gate (KIF-29)
  was triggered in Phase 1, cross-reference the Stage 9 domain mapping against
  the consilience audit's 6-domain translations. Flag any domain where the
  forecast's practical application contradicts or enriches the consilience.

**Output:** A "Practical Applications Extension" document (stored in
`artifacts/`) with: domain mapping table, operational signatures, domain-specific
falsifiable claims, additional calibration register entries, and cross-domain
consilience cross-references.

**Integration with publication (Phase 5):** The domain mapping becomes a
"Practical Applications" section in the paper. Falsifiable claims become part
of the paper's calibration register. The operational signatures drive the
paper's evidence-of-impact argument.

### Stage 10: Counterfactual Backcasting (MANDATORY for all projects)

**Runs for ALL projects. Scope scales.** A single-result paper backcasts across
2-3 target disciplines at 1-2 fork tiers; a paradigm forecast backcasts across
4+ disciplines at 3-4 fork tiers.

**Purpose:** Stage 9 maps the forecast forward into applications. Stage 10
maps backward: given a hypothetically advanced state of the target disciplines
(Stratigraphy, Metrology, Number Theory, Valuation Theory — or whatever
disciplines the research operates within), what technology stacks would be
available today, and what historical forks could have produced them?

This is a counterfactual exercise that serves three functions:
(a) It stress-tests the forecast by asking "what would have to be true for
  this to already exist?" — revealing hidden timeline assumptions.
(b) It identifies *actionable near-term forks* — Tier 1 forks that could
  have been achieved with a ~20-year research reprioritization.
(c) It generates *calibration register entries* for the backcast claims,
  providing a second independent set of falsifiable predictions.

**Protocol:**

1. **Target Discipline Identification:** Identify the core disciplines the
  research depends on. State the current state and the "target state."

2. **Tiered Fork Classification:**

  | Tier | Description | Temporal Distance |
  |:-----|:------------|:------------------|
  | **Tier 1** | Single research program reprioritized ~20 years ago | 2000s fork → impacts by 2020s |
  | **Tier 2** | Coordinated advancement across 2-3 disciplines | 1960s fork → impacts by 2000s |
  | **Tier 3** | Incompatible mathematical foundations required | 1900s fork → impacts by 1980s |
  | **Tier 4** | The axioms themselves differ | Indefinite |

3. **Counterfactual Technology Stack:** For each discipline × tier, describe
  the counterfactual technology. Be specific: name, capability, enabling fork.

4. **Summary Table:** Map every Discipline × Tier → Counterfactual Technology.

5. **Calibration Register Entries:** Register at least one dated prediction
  per backcast tier — reverse predictions: "If Tier N fork had occurred, we
  would observe X by now."

6. **Near-Term Fork Recommendations:** Tier 1 forks become actionable
  recommendations for the paper's Future Work section.

**Output:** A "Counterfactual Backcasting" document (stored in `artifacts/`)
with: target discipline assessment, tiered fork classification, counterfactual
technology stack table, backcast calibration register entries, and near-term
fork recommendations.

**Integration with publication (Phase 5):** The backcast becomes a
"Counterfactual Technology Stacks" section. The tiered fork table is
publication-ready. Near-term fork recommendations become Future Work.

**Generalization:** The protocol template uses Stratigraphy, Metrology, Number
Theory, and Valuation Theory as placeholders. The agent MUST replace these
with the actual core disciplines of the research project. Every research
project has core disciplines — identify them from Phase 1 due diligence.

---

## Phase 5: Publication Pipeline

> **PUBLICATION PRINCIPLE (cross-ref Phase 4):** The methodology-invisibility rule from
> Phase 4 applies to ALL Phase 5 outputs — papers, PDFs, and abstracts must present
> analysis without methodology branding. See Phase 4 §PUBLICATION PRINCIPLE for the
> canonical replacement table ("Stage 2 Assumption Audit found..." → "Underlying this
> candidate are three critical assumptions..."). The Forecast Integration Map (above)
> shows how every Stage output maps to a specific paper section.


### Pre-Publication Requirements


#### BP-1 Fit-Verify Gate (Numerical Claim Verification Before Zenodo) `[HARD — v2.39]`

**MANDATORY before any Zenodo upload involving a numerical table, triple, or fit.**

1. Write an independent Python recomputation script that computes every claimed value directly from the stated formula/triple.
2. The script MUST: (a) compute every claimed value; (b) report the EXACT computed vs paper's claimed value; (c) flag any discrepancy > 0.01%.
3. Output → `artifacts/fit-verify.txt`. Exit 0 = all claims match → proceed. Exit 1 = BLOCKED — fix the table.
4. For search-based fits: confirm the claimed triple IS optimal under stated bounds (non-optimal = gate failure).
5. **Why this gate:** Cross-Domain v3.2 §7.2 had 2 arithmetic errors (m_τ/m_μ = 0.2624 not 16.80; m_h/m_e = 239.15 not 244,888 — and 244,888 not 3-smooth) + 5 non-optimal triples. Published "verified." A 30-second recomputation would have caught all errors pre-publication.

#### BP-2 Terminology Audit Gate (Field-Specific Term Verification) `[HARD — v2.39]`

**MANDATORY for ALL publications.** Every field-specific term → check standard definition (Wikipedia/MathWorld/nLab).

1. Identify every field-specific term that is NOT a standard common noun.
2. For each: check the closest standard definition.
3. If no match: NEW coinage → explicitly define in §1.
4. If matches BUT paper uses differently → BLOCKED. Rename to correct term.
5. If matches with SAME definition: PASS.
6. Output: `artifacts/terminology-audit.md` with per-term verdicts.
7. **Why this gate:** "Pythagorean semigroup" for {2^a·3^b·5^c} = misnomer. These are 5-smooth (Hamming) numbers. Pythagorean numbers satisfy a²+b²=c². Every integer ≥3 is a leg of some Pythagorean triple, so "Pythagorean number" is not a distinguishing property. The misnomer originated in Cross-Domain v3.2 §7.2 and propagated into 4 published papers. A 60-second Wikipedia check would have prevented this.

#### BP-3 Density Gate (Approximating Claims Must Pass Null Model) `[HARD — v2.39]`

**MANDATORY when a paper claims "set S approximates values V to within ε%" and S is dense in ℝ⁺ (rationals, 5-smooth numbers, Diophantine approximants, etc.).**

1. Construct null model: draw N random targets from realistic prior (log-uniform over observed range).
2. Perform the SAME fit procedure as the claim (search space, exponent bounds, algorithm).
3. Report: median null error, P(null best-fit ≤ observed max), P(all-n-values simultaneously fit).
4. Look-elsewhere correction: global p-value with trials factor × search space.
5. **GATE:** p_global > 0.05 → MUST report `[CONSISTENT WITH LOOK-ELSEWHERE ARTIFACT]`. Passing is a BOUNDED NUMEROLOGICAL RISK, not a discovery.
6. If p_global ≤ 0.05 → claim carries `[LOOK-ELSEWHERE GATE: PASSED]` with exact p-value.
7. **Reference:** ACRP-04 (DOI 10.5281/zenodo.21727479) is the canonical execution.
8. Output: `artifacts/density-gate.md`. Absent on qualifying claim → REJECTED.

#### BP-4 Cross-Paper Numerical Consistency Gate `[HARD — v2.42]`

**MANDATORY when multiple QNFO publications cite the same numerical result.** Before publishing ANY paper that cites a number also appearing in another QNFO paper, reconcile the values.

1. Identify the shared number (e.g., P(all-9-fit) = 99.8% in ACRP-04, "99.85%" in Adelic v4.0).
2. Recompute the number independently in the current session.
3. If the values disagree beyond trivial rounding (±0.1pp for percentages, ±1 for small σ values), BLOCK until resolved.
4. Output: `artifacts/cross-paper-consistency.md` with per-number reconciliation.
5. **Why this gate:** ACRP-04 reports P(all-9-fit) = 0.998 (99.8%); Adelic v4.0 §7.2 disclosure reports "99.85%." Both reference the same Monte Carlo (seed 20260731). A shared null-model result MUST be consistent across all papers that cite it.

#### BP-5 Overdetermined System Verification Gate `[HARD — v2.42]`

**MANDATORY when a paper claims N fitted ratios from M < N independent quantities.** The N fits are mathematically overdetermined — they cannot all be simultaneously exact.

1. Identify the independent quantities (e.g., m_μ/m_e and m_τ/m_e; m_τ/m_μ is their ratio).
2. Compute the closure error for each derived ratio.
3. Report: "Closure error: X%. Claimed tolerance: Y%. Status: [CONSISTENT] / [INCONSISTENT]."
4. If INCONSISTENT → the fits are not a consistent parameter set. Acknowledge as a limitation.
5. Output: `artifacts/overdetermined-closure.md`.
6. **Why this gate:** The 3 lepton 5-smooth fits have 0.050% internal closure error. The framework's ~0.11% tolerance absorbs this, but it means the ratios are not simultaneously exact 5-smooth numbers.

#### BP-6 Derived-Quantity Recompute Gate `[HARD — v2.42]`

**MANDATORY when reporting any quantity derived from claimed primary results** (e.g., Koide Q-value from mass fits, cross-ratio from independent fits). Never assume claimed numbers are component-accurate.

1. Recompute from the primary claimed numbers using exact rational arithmetic where possible.
2. If the derived quantity is used as evidence, the recomputation MUST be from first principles — not by trusting the paper's own computation.
3. Output: recomputed value, method, and any discrepancy from prior reports.
4. **Why this gate:** My initial analysis claimed 5-smooth Koide Q deviates from 2/3 by "0.02%." Independent recomputation yields 0.00289% — a factor of ~7× error. The qualitative argument survived, but the quantitative claim required correction.

#### BP-7 Sigma/Error Propagation Audit Gate `[HARD — v2.42]`

**MANDATORY for every reported sigma deviation, confidence interval, or error-bound claim.** Every σ must trace to a specific, cited uncertainty source with documented propagation method.

1. **Source traceability:** "9,138σ" → must cite: PDG edition, specific table, exact value ± uncertainty, best-fit computation, and propagation formula (Δ/σ).
2. **Single-source rule:** If the same quantity appears with TWO different uncertainty values in the same paper, the paper carries a self-contradiction. BLOCK until reconciled.
3. **Rounding disclosure:** If the reported σ differs from the recomputed value, document the discrepancy. An audit paper auditing arithmetic errors cannot carry an unreproducible headline number.
4. Output: `artifacts/sigma-traceability.md`.
5. **Why this gate:** ACRP-04's 9,138σ figure does not reproduce under any combination of its own cited uncertainties or PDG 2024 Live (best: 8,943σ). The paper's two uncertainty values produce σ=4,114 and σ=8,227 — neither equals 9,138.

#### BP-8 Numerology Claim Classification `[DESIGN — v2.42]`

**MANDATORY before publication of any number-theoretic approximation claim.** Classify into one of five structural types, each triggering specific required gates:

| Class | Definition | Required Gates |
|:------|:-----------|:---------------|
| **Dense-Approximant** | Claims dense set S approximates values V to ε% | BP-3 (density gate) + BP-5 (overdetermined closure) |
| **Ratio-Factorization** | Claims ratio R=N/D is significant because N,D factor nicely | BP-3 adapted: null model for random ratios in same range |
| **Index-Selection** | Claims integer exponents (a,b,c) have physical meaning due to smallness | BP-3 adapted: test if random targets need larger exponents |
| **Transcendental** | Claims π/e/φ approximates a physical quantity | Pre-registered tolerance + falsifiable precision prediction |
| **Pattern-in-Noise** | Claims pattern discovered post-hoc in existing data | HARD BLOCK: not evidence. Pre-register on new data. |

**Why this gate:** ACRP-04 tested §7.2 (Class 1: Dense-Approximant). §6 (adelic factorization 976/919) is Class 2 (Ratio-Factorization) and has NOT undergone any density gate audit. Without this classification, structurally identical numerology claims in the same paper escape scrutiny.

#### BP-9 Audit-the-Auditor Gate `[SOFT — v2.42]`

**MANDATORY before publishing any audit paper that criticizes another paper's numerical accuracy.**

1. **Self-audit:** Run ALL of BP-1 through BP-7 on the AUDIT PAPER ITSELF before publication.
2. **Sigma recomputation:** Every σ value reported by the audit must be independently recomputed.
3. **Cross-check with live data:** Re-fetch current PDG values — don't assume the audit's values are current.
4. **Disclose any discrepancy:** If the audit's headline numbers don't reproduce, correct them or disclose with `[SELF-AUDIT: number X does not reproduce; best reconstruction Y]`.
5. **Why this gate:** ACRP-04's most prominent numerical claim (9,138σ) does not reproduce under any combination of cited uncertainties or PDG 2024 Live.

#### BP-10 Independent-Recompute Gate `[HARD — v2.42]`

**MANDATORY before citing any paper's numerical claim as evidence in new research.** "Cited in a paper" ≠ "independently verified."

1. Before treating a p-value, σ, percentage, or fit as established, recompute it in the current session.
2. For Monte Carlo results: run an independent implementation with a different seed. Verify consistency within sampling noise.
3. For PDG-dependent values: re-fetch PDG Live — do not assume the paper's PDG values are current.
4. If recomputation is not feasible, flag `[NOT-VERIFIED: independent recomputation blocked by <reason>]` and do NOT cite as "established."
5. Output: ephemeral verification script + result log in `artifacts/independent-recompute/`.
6. **Why this gate:** Two sessions cited ACRP-04's p=0.116 without running the Monte Carlo. The number is correct (this session independently confirmed p=0.1193), but trusting it without verification is an Anti-Phantom violation. Recomputation cost is negligible (~30 seconds for 50k-trial MC) vs. cost of propagating a wrong number.

---

### Numeracy Red Flags Checklist (v2.42)

**MANDATORY quick-scan BEFORE publishing or citing any numerical claim.** Any 🚩 hit → investigate before proceeding. This is a signal-detection checklist, not a substitution for the full gates above.

| 🚩 | Signal | Gate | Canonical Instance |
|:--|:-------|:-----|:-------------------|
| 🚩 | Two conflicting values for same quantity in same paper | BP-7 | ACRP-04: m_μ/m_e unc=1e-5 vs 5e-6 |
| 🚩 | Sigma/percentage without cited uncertainty source | BP-7 | "9,138σ" — untraceable to specific PDG ed. |
| 🚩 | Cross-paper inconsistency for same numerical result | BP-4 | 99.8% (ACRP-04) vs 99.85% (v4.0) |
| 🚩 | Overdetermined system claimed as independent fits | BP-5 | 3 lepton ratios, 2 DoF, 0.050% closure |
| 🚩 | Derived quantity cited without independent recomputation | BP-6 | Koide Q "0.02%" → actual: 0.00289% |
| 🚩 | Dense approximating set without density gate | BP-3 | 5-smooth, rationals, Diophantine approximants |
| 🚩 | Structurally similar claims with selective gate application | BP-8 | §7.2 tested but §6 (same class) not |
| 🚩 | "Within X%" tolerance never pre-registered | BP-3 | Post-hoc tolerance = extra look-elsewhere DoF |
| 🚩 | False-precision in p-values/percentages | BP-10 | "0.116" (3 sig figs) from MC (SE ~0.002) |
| 🚩 | p-value/σ reported without independent recomputation | BP-10 | Trusting paper claims without re-run |
| 🚩 | Post-hoc pattern discovery presented as evidence | BP-8 Class 5 | Pattern found AFTER data inspection |
| 🚩 | Exponent/search bounds selected post-hoc | BP-3 | B=14 selected after seeing data — 2nd DoF |
| 🚩 | Single-seed Monte Carlo without seed-sensitivity check | BP-10 | Seed 20260731; no alt seed tested |
| 🚩 | Audit paper with its own unreproducible headline number | BP-9 | ACRP-04's 9,138σ vs recomputed 8,943σ |

**Usage:** 0 🚩 → proceed. 1-2 🚩 → investigate, document, then proceed. 3+ 🚩 → HARD BLOCK: systemic numerical issues.

**Genre note (v2.30):** The certainty calibration, Professional Publication Standards, and inline labeling requirements in this section apply to Genre A (Epistemic Content - research papers, technical notes, investigation reports). For Genre B (Commercial/Marketing Content - landing pages, pitch decks, prospectuses), the certainty calibration protocol is MODIFIED per qnfo-core §0.1: no inline [speculative] labels on marketing pages; use a Forward-Looking Statements footer disclaimer and dagger footnotes for specific aspirational claims instead. For Genre C (Internal/Operations Content), only the banned-words and no-fabrication rules apply. See qnfo-core §0.1 for the full Genre Classification Protocol.
#### YAML Frontmatter (MANDATORY)
```yaml
---
title: "Paper Title"
author: "Author Name"
date: "YYYY-MM-DD"
license: "QNFO Unified License Agreement (QNFO-ULA)"
doi: "10.5281/zenodo.XXXXXXXXX" # Placeholder, replaced after Zenodo upload
status: "draft" | "published"
---
```

**YAML delimiter conflict check (kaizen fix D3):** a markdown table
separator row (`|---|---|`) or a horizontal rule elsewhere in the body can
contain the bare string `---`, which some naive frontmatter parsers
misinterpret as a second frontmatter block. Before building, count `---`
occurrences on their own line at column 0:
```bash
# Windows: write this to _yaml_check.py, then `python _yaml_check.py`; never inline python -c
# Build-paper.py handles this automatically -- prefer: python scripts/build-paper.py <slug>.md
python _yaml_check.py
```
Where `_yaml_check.py` contains:
```python
import sys; t=open('paper.md',encoding='utf-8').read(); print(sum(1 for l in t.splitlines() if l.strip()=='---'))
```
Only the FIRST TWO such lines (opening and closing the YAML block) are valid
frontmatter delimiters. `scripts/build-paper.py` (preprocess stage) already
handles this correctly (it anchors the frontmatter regex to the START of the
file with `^---\n...\n---\n`), but any custom tooling touching `paper.md`
must apply the same anchoring rule -- never a naive "split on ---".

#### Visible Author Block (MANDATORY)
**Author:** [Name] | **Date:** [YYYY-MM-DD] | **License:** QNFO-ULA: https://legal.qnfo.org/

#### Publication Language Gate (BLOCKING if any hit)
Scan for ALL of:
- **INTERNAL LANGUAGE:** "Module N", "Task N", "SPRINT", "PROCEED", "RESUME", "0.N.py", "PROJECT STATE", "ready for handoff", "new agent starting from cold" -> BLOCKING
- **INTERNAL METADATA:** Version numbers as visible headers, project identifiers, commit references -> absent from visible content
- **STYLE:** Straight quotes in body, bare Unicode math outside $...$, generation artifacts -> BLOCKING
- **CREDENTIAL LEAKS (kaizen fix D2):** `cfat_[a-zA-Z0-9_]{20,}`, `ghp_[a-zA-Z0-9]{36}`, `sk-[a-zA-Z0-9]{20,}`, `AKIA[0-9A-Z]{16}`, `Bearer [A-Za-z0-9._-]{20,}` -> BLOCKING. Run `scripts/credential-scan.py paper.md` as part of this gate, not just at git-commit time -- a token could be pasted into the paper body itself, which is a worse leak than a script file since it gets published to Zenodo/IPFS permanently.

#### Physics Writing Standards (18-point -- see qnfo-agent §7)
All 18 points apply. Minimum: certainty calibration on every non-textbook claim, falsifiability conditions on speculative claims, banned word operational definitions.

#### Self-Evaluation Rubric
| Dimension | 1 | 3 | 5 |
|:----------|:--|:--|:--|
| Evidence Quality | No sources | Most sourced | Every claim traceable |
| Clarity | Disorganized | Clear structure | Crisp, precise |
| Fabrication Risk | Invented data | All verifiable | Zero fabrication |
| Format Compliance | Bare Unicode | Most in LaTeX | All $...$, curly quotes |

**Publish only if ALL >= 3 AND average >= 4.0.**

### Professional Publication Standards (MANDATORY, HARD GATE -- 2026-07-25)

Every QNFO publication -- paper, PDF, or dissemination artifact -- MUST meet
the content, tone, structure, and copyediting bar that a subject-matter
peer reviewer at a serious journal (Foundations of Physics, Physical Review
A, New Journal of Physics, Quantum, or equivalent) would expect, such that
the submission is judged on its scientific merits and is NOT desk-rejected
or flagged for unprofessional presentation. This is a DISTINCT gate from
the Physics Writing Standards (`qnfo-agent` §7, content-integrity: banned
words, certainty labels, falsifiability) and the Publication Language Gate
(internal-language/credential scrubbing) -- both of those govern *what is
said*; this gate governs *how professionally it reads*. A paper can pass
both of those gates and still fail this one if it reads like a draft.

**Structural requirements (all must be present, in this order, for a
full research article):**
1. Title -- concise, informative, no acronyms undefined at first use.
2. Abstract -- 150-250 words (Springer Nature convention; adjust per
  target journal), self-contained, no undefined abbreviations, no
  citations unless the target journal explicitly permits them.
3. Keywords -- 4-6 terms suitable for indexing.
4. Introduction -- states the problem, situates it in the literature,
  states the paper's contribution and structure (a "roadmap" paragraph
  naming each subsequent section is expected in physics/math papers).
5. Body sections -- decimal numbering, no more than 3 heading levels
  (Springer Nature convention), one clear argument thread per section.
6. Conclusion -- restates contribution, is honest about limitations,
  does NOT introduce new citations or claims not defended in the body.
7. Declarations -- all 9 subsections per the template README (Funding,
  Conflicts of Interest, Ethics, Consent, Author Contributions, Data/
  Materials/Code Availability, Use of Artificial Intelligence).
8. Bibliography -- every entry cited in text, no orphan/unused entries,
  consistent citation style throughout (numbered XOR author-year, never
  mixed).

**Tone and prose requirements:**
- **Formal, third-person or first-person-plural ("we argue", "we show"),
 never first-person-singular ("I think") in the body text** -- singular
 first person is acceptable only in author-contribution/declaration
 statements about the author personally.
- **No hedging filler** ("it could perhaps be argued that", "in some
 sense") -- state the claim, then qualify it with an explicit certainty
 label per the Physics Writing Standards, not with vague hedge-words.
- **No rhetorical questions in the body text** of a research article
 (acceptable sparingly in a Discussion section framing an open problem,
 but the default is declarative prose).
- **No contractions** ("doesn't", "it's") -- expand to full form.
- **Active voice preferred** over passive, except where passive is the
 disciplinary convention (e.g., describing an experimental procedure:
 "the sample was prepared").
- **Consistent tense**: present tense for established facts and the
 paper's own ongoing argument ("Section 3 shows..."), past tense for
 prior work's specific findings ("Hardy derived...").
- **No AI-generated-sounding transitional filler** ("It is important to
   note that", "In conclusion, it can be seen that", "Moreover, it is worth
   mentioning") — these read as generation artifacts and are a Publication
   Language Gate concern as well as a tone concern. Replace
   with direct statements.

- **All physics formulas must use dimensionless Planck units ($\hbar = c = G = k_B = 1$)**
   per the Ostrowski Dimensionless Mandate (qnfo-core §0.7). Dimensional formulas
   (e.g., $S \leq 2\pi k_B R E / (\hbar c)$) implicitly privilege the Archimedean
   ($\infty$) place. Required: every dimensional formula MUST be accompanied by its
   dimensionless equivalent AND an Ostrowski rationale. Well-known formulas
   (Landauer's $E \geq k_B T \ln 2$) may present both forms — "In conventional
   dimensional form: $E \geq k_B T \ln 2$. In dimensionless Planck units: $E \geq T \ln 2$,
   where both $E$ and $T$ are pure numbers whose completions exist at every place
   per Ostrowski's theorem." See also: *Non-Anthropocentric Natural Units*
   (DOI: 10.5281/zenodo.21480756). ("It is important to
 note that", "In conclusion, it can be seen that", "Moreover, it is
 worth mentioning") -- these read as generation artifacts and are a
 Publication Language Gate concern as well as a tone concern. Replace
 with direct statements.

**Copyediting checklist (run before every publication, no exceptions):**
- [ ] Zero spelling errors (run a spell-check pass; do not rely on
   LaTeX/pandoc to catch these).
- [ ] Zero grammar errors -- subject-verb agreement, correct article use
   (a/an/the), correct preposition use throughout.
- [ ] Consistent hyphenation/compound-word conventions within the paper
   (e.g., "state-of-the-art" always hyphenated when adjectival, never
   "state of the art" and "state-of-the-art" mixed).
- [ ] Consistent capitalization of technical terms (e.g., "Hilbert space"
   not sometimes "Hilbert Space").
- [ ] Curly quotes and em-dashes in body prose (`` `` '' `` / `---` in
   LaTeX source), never straight quotes or double-hyphens in rendered
   output.
- [ ] No orphaned section headers (a heading immediately followed by
   another heading with no body text between them).
- [ ] No repeated words ("the the"), doubled spaces, or trailing
   whitespace artifacts from find-replace operations.
- [ ] Every acronym defined at first use, used consistently thereafter
   (Springer Nature Instructions for Authors requirement, verified
   live 2026-07-25).
- [ ] Every figure/table has a caption, is referenced from body text at
   least once, and captions do not simply repeat the section text.
- [ ] Every equation that is referenced elsewhere in the paper has a
   `\label{}`/`\ref{}` pair, not a hardcoded equation number.
- [ ] Reference list entries are complete (author, title, venue, year,
   DOI where available) and formatted identically to each other
   (same punctuation/ordering pattern for every entry of the same
   type -- journal article, book, preprint, etc.).

**Self-review protocol (MANDATORY before declaring a paper publication-ready):**
1. Read the paper start to finish as a hostile peer reviewer would --
  flag any sentence that would draw a reviewer comment about clarity,
  rigor, or presentation, not just correctness.
2. Read the Abstract in isolation -- does it stand alone as a complete
  summary without the reader needing the rest of the paper?
3. Read only the section headings in sequence -- do they form a
  coherent narrative arc on their own?
4. Check that no paragraph is a single run-on sentence and no section
  is a single paragraph longer than roughly half a page.
5. Confirm the Declarations section is complete per the checklist above
  -- an incomplete Declarations section is itself a professional-
  quality failure independent of the science.

**GATE:** A publication that fails ANY item in the structural,
tone/prose, or copyediting checklists above is NOT publication-ready,
regardless of scientific content quality. Fix the presentation issue,
then re-run this checklist, before proceeding to PDF build and upload.

### Source File Encoding Integrity (HARD GATE, KIF-28 MANDATE)

**BEFORE any build, commit, or publish operation on markdown source files:**

1. **Zero BOM (Byte Order Mark):** No `.md`, `.py`, `.js`, `.tex`, or `.bib` file
  shall contain a UTF-8 BOM (U+FEFF). BOM silently breaks: Pandoc frontmatter
  parsing, YAML libraries, `git diff` display, and some spell-checkers.
  Verify: first 3 bytes of the file MUST NOT be ``.

2. **Zero U+FFFD (REPLACEMENT CHARACTER):** This character means "bytes were
  decoded with the wrong encoding" -- it is ALWAYS a corruption signal, never
  intentional content. Any file containing U+FFFD MUST NOT be committed or
  published.

3. **Zero U+FFFF (NONCHARACTER):** This noncharacter appears in PDFs when a
  font lacks a glyph, but it must NEVER appear in source markdown. Its presence
  in a source file means a prior encoding corruption event is still propagating.

4. **All Python scripts: `# -*- coding: utf-8 -*-` on line 1 or 2** (after
  shebang). Every `open()` call for text files MUST specify `encoding='utf-8'`
  explicitly -- Python's default on Windows is `locale.getpreferredencoding()`
  (cp1252), which SILENTLY produces wrong characters without any exception.

5. **All PowerShell commands that interact with files: use `-Encoding UTF8`.**
  `Get-Content` without `-Encoding` defaults to the system codepage and will
  silently corrupt UTF-8 content.

**Pre-commit verification scan** (write to file via `write` tool, then execute — never inline `python -c`):
```bash
# Canonical: python scripts/credential-scan.py --staged
# Or: write _fffd_scan.py, then exec python _fffd_scan.py
python _fffd_scan.py
```
`_fffd_scan.py` content (use the `write` tool for the script body, then `exec`):
```python
import sys, os
for root, dirs, files in os.walk('.'):
  for fn in files:
    if any(fn.endswith(e) for e in ('.md','.py','.js','.tex','.bib','.json','.yaml','.yml')):
      fp = os.path.join(root, fn)
      with open(fp, 'rb') as f:
        data = f.read()
      issues = []
      if data[:3] == b'':
        issues.append('BOM')
      text = data.decode('utf-8', errors='replace')
      if '\\ufffd' in text:
        issues.append('U+FFFD')
      if '\\uffff' in text:
        issues.append('U+FFFF')
      if issues:
        print(f'{fp}: {" / ".join(issues)}')
        sys.exit(1)
print('ENCODING GATE: PASS')
```
**GATE:** If the pre-commit scan exits non-zero, BLOCK the git commit.
This is a HARD gate -- encoding corruption in source propagates to PDFs,
Zenodo archives, D1 inserts, and all downstream distribution channels.
A single U+FFFD in source can survive through Pandoc, XeLaTeX, Zenodo,
and IPFS, producing a permanently corrupted public artifact.

### PDF Building

**DEFAULT TEMPLATE (MANDATORY, 2026-07-25): the Springer Nature LaTeX
Template (`sn-jnl.cls`, v3.1, December 2024)** is the standard template
for ALL QNFO LaTeX-native publications and publication-grade PDFs. Files
are embedded in this skill at `templates/springer-nature-latex/` --
`sn-jnl.cls`, all 8 `.bst` bibliography styles, the official
`sn-article.tex` reference example, `sn-bibliography.bib`,
`user-manual.pdf`, and `qnfo-paper-template.tex` (a QNFO-conventions
starter with the mandatory Declarations block pre-populated). See
`templates/springer-nature-latex/README.md` for the full class-option
table and verified build sequence
(`pdflatex -> bibtex -> pdflatex -> pdflatex`, with the `.bst` file
copied alongside `paper.tex`/`refs.bib` -- bibtex does not search the
`bst/` subdirectory by default).

**Do NOT use the legacy `svjour3`/`svjour.cls` package** (CTAN package
name `springer`) for new LaTeX papers -- it was Springer Nature's
per-journal class system, retired in favor of the unified `sn-jnl.cls`
across essentially all Springer Nature journals (verified live against
Springer Nature's own LaTeX Author Support page, 2026-07-25). Existing
papers built on `svjour3` should be migrated to `sn-jnl.cls` at the next
substantive revision.

**For Markdown-native publications** (papers authored and maintained as
`<slug>.md` rather than `paper.tex` -- e.g., most QNFO working papers prior
to journal submission), continue using Pandoc+XeLaTeX per the pipeline
below. Convert to the Springer Nature LaTeX template at the point of
formal journal submission, or immediately if the target venue requires
LaTeX source at all revision stages.

**CANONICAL SOLUTION (v2.21, KIF-27):** A single script does everything:
preprocess Unicode math to LaTeX math mode, build the PDF, and verify zero
rendering errors. This replaces three previously fragmented scripts
(`unicode-latex-preprocess.py`, `check-pdf.py`, `build-pdf.py` -- all
DELETED as of v2.21).

```bash
python scripts/build-paper.py <slug>.md
# or with explicit output path:
python scripts/build-paper.py <slug>.md --output <slug>.pdf
```

> **Slug-based naming (v2.38):** Paper files MUST use the project slug, NOT generic `paper.md`/`paper.pdf` names. For project `computing-machines`, the files are `computing-machines.md` and `computing-machines.pdf`. This prevents confusion when multiple paper repos are cloned in the same temp directory. Generic `paper.md` naming is an anti-pattern (see Anti-Patterns table).

This single command:
1. Reads `<slug>.md` with UTF-8 forced (never trust ambient/locale encoding
  on Windows -- see `qnfo-agent` §8.7 PowerShell UTF-8 Encoding Protocol)
2. Converts every Unicode math character in prose (outside existing
  `$...$`/`$$...$$` spans) to its LaTeX equivalent, WRAPPED in `$...$` so
  XeLaTeX activates the math font for that span -- this is mandatory
  because `unicode-math` + a comprehensive math font (STIX Two Math, etc.)
  was tested live and does NOT make bare Unicode math symbols render
  correctly in prose text; the math font only activates inside math mode
3. Groups consecutive subscript/superscript characters into a single
  `_{...}`/`^{...}` block (naive one-character-at-a-time conversion
  produces INVALID LaTeX -- "Double superscript" errors)
4. Builds the PDF via `pandoc --pdf-engine=xelatex`
5. Verifies the output PDF has zero U+FFFD/U+FFFF characters and zero
  empty pages -- exit code 1 if verification fails, PDF MUST NOT publish

Exit codes: `0` = publication-ready, `1` = build or verification failed
(do not publish), `2` = missing dependency or bad invocation.

**Prior approaches, retracted:**
- v2.18 (KIF-26): dictionary-based conversion with an incomplete character
 table (only numeric subscripts, missing letter subscripts/superscripts) --
 fixed by comprehensive table in `build-paper.py`, not superseded.
- v2.19 (KIF-26 v2): claimed loading `unicode-math` + `STIX Two Math` font
 would make Unicode math symbols render correctly directly in prose text
 without needing `$...$` wrapping. **TESTED LIVE AND FALSE** -- `unicode-math`
 only activates the math font INSIDE math mode; prose text uses the
 running text font, which lacks these glyphs regardless of which math
 font is loaded.

**NEVER use reportlab or HTML fallbacks for publication-grade PDFs.**

**If the build still fails with a LaTeX error mentioning a specific missing
character or macro:** check whether the character is inside `$$...$$` and
was written directly in LaTeX already (not Unicode) -- some math symbols
(e.g. `\ket{}`, `\langle`) require the `physics` or `braket` LaTeX package;
add `--metadata header-includes="\usepackage{braket}"` if bra-ket macros are
used directly in the source rather than relying on the preprocessor's
`\langle`/`\rangle` fallback.

### R2 Archive (MANDATORY -- every publication)

Every publication's source (<slug>.md), rendered PDF (<slug>.pdf), and provenance bundle
(PROVENANCE-BUNDLE.zip) MUST be uploaded to Cloudflare R2 immediately after Zenodo publishing.

```bash
npx wrangler r2 object put qnfo-releases/releases/<YYYY>/<MM>/<slug>/<slug>.md --file=<slug>.md --remote
npx wrangler r2 object put qnfo-releases/releases/<YYYY>/<MM>/<slug>/<slug>.pdf --file=<slug>.pdf --remote
```

### DNSLink (OPTIONAL -- read-only IPFS resolution)

```bash
node ../cloudflare/scripts/dnslink-create.js <zone_id> <subdomain>.qnfo.org <ipfs_cid>
```

### PDF Rendering Verification (MANDATORY HARD GATE, KIF-27)

**THIS IS A BLOCKING GATE.** A PDF with any rendering error MUST NOT be
published to Zenodo, R2, or any public distribution channel.

As of v2.21, this verification is built INTO `scripts/build-paper.py` --
it is not a separate step. Running:
```bash
python scripts/build-paper.py <slug>.md
```
performs preprocessing, the pandoc/xelatex build, AND verification in one
invocation. Exit code `0` = publication-ready (proceed to Zenodo/R2
upload). Exit code `1` = rendering errors found or build failed -- the PDF
in that case MUST NOT be published; read the printed diagnostics, fix the
source markdown, and re-run.

Do NOT attempt to invoke `unicode-latex-preprocess.py`, `check-pdf.py`, or
`build-pdf.py` -- these files were DELETED as part of the KIF-27
consolidation (three fragmented scripts patched incrementally across 4
kaizen passes, one of which contained a retracted wrong claim, replaced by
the single `build-paper.py`). If a stale reference to any of these three
filenames is ever encountered elsewhere in this skill, it is a KNOWN STALE
REFERENCE from before the v2.21 consolidation -- treat `build-paper.py` as
the sole canonical entry point regardless.

### OSF Project Registration (MANDATORY for qualifying projects)

**GATE:** ONLY for major research programs with significant predictions and falsifiable claims. Do NOT register exploratory projects, single papers within existing programs, or minor updates. If the project doesn't make testable, falsifiable predictions with calibration registers, skip this section.

**POLICY:** ALL OSF resources MUST be public. NEVER expect or request manual browser interaction. Registration drafts, full form completion (all ~30 schema fields), subject taxonomy assignment, and final registration submission are ALL 100% achievable via the OSF v2 API (verified live 2026-07-20, registration `kj6ar` created via pure API calls, HTTP 201). Only file uploads specifically require Waterbutler (cookie-based sessions) — for those, link to external canonical sources (Zenodo DOI, GitHub tree, IPFS gateway) instead. Do not conflate the file-upload limitation with the registration/form-completion capability — they are different OSF subsystems with different constraints. See "OSF Registration — Full API Automation Protocol" below.

**HARD GATE: LLM-Executable Research** — OSF registration is ONLY valid for research that can be fully executed by this LLM agent within ONE chat thread, with NO human subjects, NO external resources (lab equipment, personnel, institutional partnerships), and NO IRB requirement. All data must be publicly available or computable from first principles. If the research involves human participants, lab equipment, funding applications, or any resource not immediately available in the current session, do NOT create OSF registrations — link to Zenodo/GitHub instead.

**Qualifying research types:**
- Automated data analysis of publicly available datasets
- Synthesis and meta-analysis of published literature
- Mathematical/computational models and simulations
- Algorithm development and validation on benchmark datasets
- Formal verification of claims against existing evidence
- Framework validation using existing published data
- Re-analysis of open-access data with pre-registered methods

**Non-qualifying research (link to Zenodo/GitHub only):**
- Any RCT, survey, interview, or behavioral experiment with human participants
- Any research requiring physical lab equipment or facilities
- Any research requiring new data collection from human subjects
- Any research requiring IRB/ethics committee approval
- Any research requiring hiring or contracting personnel
- Any research requiring institutional partnerships or funding applications
- NUMERATA Phase 2 experiments (N=324 human subjects, N=60 child participants, IRB required)

**BONA FIDE REGISTRATION REQUIREMENTS (MANDATORY — never create incomplete stubs):**

Every OSF registration MUST:
1. **Populate ALL ~30 structured fields** — the OSF Preregistration template includes hypothesis, design plan, sampling plan, variables, analysis plan, and falsification criteria. ALL must be populated via `registration_responses` as a JSON object with values for every required question. Empty `registration_responses = {}` is a STUB — NEVER submit a stub. Never submit what you cannot fully populate.
2. **Require explicit user approval** — use `deepchat_question` to present the complete registration text (all populated fields) and ask: "Submit this as an OSF Preregistration? This is a permanent, timestamped, immutable record. Once submitted, it cannot be edited or deleted." Only submit if user explicitly confirms.
3. **Track followup** — after submission, store the registration ID, DOI, and submission timestamp in D1/KG with status "registered." Set a reminder for the declared data collection/completion target date. This is a COMMITMENT — failing to close out is a negative reputational signal.
4. **Close out registration** — when research completes: (a) return to the OSF registration URL, (b) add a comment or results section, (c) formally complete or withdraw the registration, (d) update D1/KG status to "completed" or "withdrawn." A registration that is submitted and never closed out is an abandoned commitment — a detectable pattern of abandoned registrations on an OSF account undermines credibility.

**Registration Closeout Protocol:**
```python
# 1. Verify the registered research is complete (all analysis run, paper published with Zenodo DOI)
# 2. Navigate to OSF registration URL and add results/outcome comment
# 3. Update D1: UPDATE papers SET registration_status = 'completed', completed_at = datetime('now') WHERE registration_id = '{id}'
# 4. Update KG: json_set(properties, '$.registration_status', 'completed', '$.completed_at', '{date}')
# 5. Log to durable memory: "OSF registration {reg_id} closed out {date}. Results: {zenodo_doi}."
# 6. If research was NOT completed, mark as "withdrawn" with a brief explanation. Never abandon.
```

**STUB AUDIT PROTOCOL:** Periodically audit all draft registrations via `GET /v2/users/me/draft_registrations/`. If `registration_responses` is empty `{}` (no form content) AND the research does not qualify under the LLM-Executable Research Gate, DELETE the draft immediately. Empty stubs are a reputational risk. If `registration_responses` is PARTIALLY filled but the research will not be completed, DELETE. Only retain drafts that (a) pass the LLM-Executable Research Gate AND (b) have fully populated `registration_responses` AND (c) will be completed within the declared timeframe.

#### OSF Workflow (API-only, fully automated)

```python
# 1. Authenticate
TOKEN = "<OSF_PERSONAL_ACCESS_TOKEN>" # Stored in .osf_token, OSF_TOKEN env var, keys.json, Windows CM
HEADERS = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/vnd.api+json"}

# 2. Create project (ALWAYS public)
POST https://api.osf.io/v2/nodes/
Body: {"data": {"type": "nodes", "attributes": {"title": "...", "category": "project", "public": true, "description": "..."}}}

# 3. Create components (one per experiment/task)
POST https://api.osf.io/v2/nodes/{project_id}/children/
Body: {"data": {"type": "nodes", "attributes": {"title": "Experiment N...", "category": "data", "public": true, "description": "📦 Canonical files: [Zenodo DOI] | [GitHub tree URL] | [IPFS gateway]"}}}

# 4. Add external links to descriptions (REQUIRED — replaces file uploads)
PATCH https://api.osf.io/v2/nodes/{node_id}/
Body: {"data": {"type": "nodes", "id": "{node_id}", "attributes": {"description": "..." + String.fromCodePoint(0x1F4E6) + " Files: " + zenodo_doi + " | " + github_tree_url + " | " + ipfs_gateway}}}

# 5. Create draft registrations (one per experiment)
GET https://api.osf.io/v2/schemas/registrations/ # Find schema ID for "OSF Preregistration"
POST https://api.osf.io/v2/nodes/{component_id}/draft_registrations/
Body: {"data": {"type": "draft_registrations", "attributes": {}, "relationships": {"branched_from": {"data": {"type": "nodes", "id": "{cid}"}}, "registration_schema": {"data": {"type": "schemas", "id": "697b72f611a8e98484c6139b"}}}}}

# 6. Document all IDs, URLs, and registration draft links in project README/PROJECT-PLAN.md
# 7. Verify: all nodes public, all descriptions contain external links, registration drafts created
```

#### OSF File Upload — NOT SUPPORTED via API

**Waterbutler requires cookie-based browser sessions.** Do NOT attempt file upload via API — it will fail. Do NOT request manual browser interaction. Instead:

- Link to Zenodo DOI (canonical published version with all files)
- Link to GitHub tree URL (source code, analysis scripts, protocols)
- Link to IPFS gateway (permanent content-addressed copy)

The OSF project becomes a **discovery hub** pointing to canonical storage, not a file host.

#### OSF Registration — Full API Automation Protocol (CORRECTED 2026-07-20)

**Prior guidance in this section was WRONG and has been retracted.** The entire registration workflow — schema discovery, field population, subject taxonomy, final submission — is achievable via API with ZERO browser interaction. Verified live: registration `kj6ar` created 2026-07-20T12:48:47Z via pure API calls, HTTP 201.

**Step 1 — Discover real schema keys (NEVER assume `q1`/`q2` format):**
```python
r = requests.get(f'https://api.osf.io/v2/schemas/registrations/{SCHEMA_ID}/schema_blocks/?page[size]=100', headers=H)
# Real keys look like '344-2', '344-47', etc. Walk blocks tracking the preceding
# question-label to build a {key: label} map. Only required=True keys are mandatory.
```

**Step 2 — For select-type fields, get EXACT verbatim option text:**
```python
# API rejects any option text that doesn't match the schema's display_text VERBATIM.
# Walk schema_blocks from the select-input key forward, collecting select-input-option
# blocks until the next non-option block type.
```

**Step 3 — Populate ALL fields in one PATCH:**
```python
patch = {'data': {'id': draft_id, 'type': 'draft_registrations',
          'attributes': {'registration_responses': responses}}}
r = requests.patch(f'https://api.osf.io/v2/draft_registrations/{draft_id}/', headers=H, json=patch)
# 200 = success. 400 "must be one of the provided options" = re-check Step 2 exact text.
```

**Step 4 — MANDATORY subject taxonomy (registration 400s without this):**
```python
# Subjects require a root->leaf chain, set on the DRAFT (flat list), not the node
# (which uses list-of-lists). These are SEPARATE relationships.
chain = [] # build via GET /v2/subjects/{id}/ walking .relationships.parent.data.id to null
patch = {'data': {'id': draft_id, 'type': 'draft_registrations', 'attributes': {'subjects': chain}}}
requests.patch(f'https://api.osf.io/v2/draft_registrations/{draft_id}/', headers=H, json=patch)
```

**Step 5 — Submit:**
```python
reg_data = {'data': {'type': 'registrations', 'attributes': {
  'draft_registration': draft_id, 'registration_choice': 'immediate'}}}
r = requests.post(f'https://api.osf.io/v2/nodes/{NODE_ID}/registrations/', headers=H, json=reg_data)
# HTTP 201 = SUCCESS, fully immutable, date_registered timestamp set.
```

**Understanding `pending_registration_approval: true` after success:** This is NOT a manual-review queue — OSF confirmed via API error "OSF Registries is an unmoderated provider." It is OSF's mandatory email-confirmation anti-hijacking gate (like 2FA), applied uniformly to ALL registrations regardless of creation method, resolved only by the account holder clicking the emailed confirmation link. Report this precisely: "Registration submitted (HTTP 201, ID `{id}`). Pending only the account holder's email confirmation — OSF's standard anti-hijacking safeguard, not a data-entry step."

**Never again claim** "requires browser interaction" for registration/form completion. That was false. Only file uploads (Waterbutler) have this limitation.

#### OSF Cleanup

```python
# Delete a node (components, test projects, etc.)
DELETE https://api.osf.io/v2/nodes/{node_id}/

# List all nodes (check for orphans)
GET https://api.osf.io/v2/users/me/nodes/
```

### Zenodo Credential Protocol (MANDATORY — read before ANY Zenodo API call)

**Incident record (2026-07-20/21):** A session spent an entire multi-hour
block diagnosing repeated `{"status":403,"message":"Permission denied."}`
errors as "the token has read-only scope" / "the token is dead" across
~15 different curl/PowerShell/Python attempts, tried sandbox endpoints,
query-param auth, multipart uploads, and different Content-Type headers —
none of which was the actual problem. The real root cause: the token had
been read from a **truncated terminal display** (`Get-ChildItem env:`
showing `ZENODO_TOKEN = BkLOVH2EDBcc...` with only the prefix visible) and
then **manually retyped/reconstructed** by guessing the suffix from a
separate truncated output, producing a 59-character string that was
subtly wrong versus the real 60-character token. Zenodo returns the exact
same generic 403 for "wrong token" as for "right token, wrong scope" —
the two failure modes are **indistinguishable by symptom alone**.

**THE RULE:** Never hardcode, retype, or reconstruct a Zenodo (or any)
API token from a truncated/partial display. Always reference the live
environment variable directly in code:

```python
import os
TOKEN = os.environ.get('ZENODO_TOKEN')  # Python — correct
```
```powershell
$env:ZENODO_TOKEN             # PowerShell — correct, pass through directly
```

**NEVER do this:**
```python
TOKEN = 'BkLOVH2EDBccmqRMEYz0vJrmbph0Bb9wDqy19RHyxMpJE0eZKZMJoqjw72g' # WRONG — hand-copied from truncated output
```

If a token must be inspected for debugging, print ONLY its length
(`len(token)`) and confirm that length matches expectations — never print
the full value (credential-leak risk per `qnfo-agent` §Publication
Language Gate) and never re-derive the value from a partial print.

**Diagnostic script (run FIRST on any Zenodo 403):**
```bash
python <research-skill-path>/scripts/zenodo-token-check.py
```
This tests read (`GET /deposit/depositions`), write (`POST` a probe
deposit), and metadata-write (`PUT` on that probe), then cleans up the
probe deposit. It distinguishes "token has no write scope — generate a
new one with `deposit:write` + `deposit:actions` scopes" from "token
works fine, the problem is elsewhere in this call" — collapsing what was
previously ~15 exploratory tool calls into one.

**Required token scopes** (generate at
https://zenodo.org/account/settings/applications/):

| Scope | Purpose |
|---|---|
| `deposit:write` | Allow upload (but not publishing) |
| `deposit:actions` | Allow publishing of uploads |
| `user:email` | Allow access to email address (read-only) |

**Publish pipeline scripts** (replace ad hoc inline `python -c` snippets
or hand-written one-off scripts — see kaizen fix B1 on why inline
multi-line Python via `-c` is itself an anti-pattern on Windows):
```bash
python <research-skill-path>/scripts/zenodo-create-upload.py <bundle.zip> [--newversion <deposit_id>]
python <research-skill-path>/scripts/zenodo-metadata-publish.py --metadata-file <metadata.json> [--dry-run]
```
`zenodo-create-upload.py` handles both "brand-new deposit" and
"new version of an existing concept" (via `--newversion`, using the same
GET-verify-before-`actions/newversion` pattern as the C2 version-chain fix
below). `zenodo-metadata-publish.py` sets metadata, publishes, and
verifies the DOI resolves live via `doi.org` + `zenodo.org/api/records`
before declaring success — never trust the tool's immediate return value
alone (see the "General principle" memory: verify server-side state
independently for every remote publish action).

**Metadata gotcha:** Zenodo's REST API requires an `upload_type` (or
`resource_type`) field in metadata — omitting it produces
`HTTP 400 {"errors":[{"field":"metadata.resource_type","messages":["Missing data for required field."]}]}`
on the `actions/publish` call specifically (metadata PUT itself succeeds
with 200, making this easy to miss until the publish step). Common
values: `publication`, `dataset`, `software`, `poster`, `presentation`.

---

### Zenodo Metadata: Complete Data Dictionary & Template

> **Purpose:** Before constructing ANY Zenodo metadata PUT call, consult
> this data dictionary. Every field is documented with its type, constraints,
> allowed values, example, and known gotchas from live-session incidents.
> See also `references/zenodo-deposit-schema.json` for the canonical REST
> API endpoint schema and incident log.

#### Data Dictionary — ALL Zenodo Metadata Fields

| # | Field | JSON Type | Required | Constraints / Allowed Values | Example |
|:--|:------|:----------|:---------|:-----------------------------|:--------|
| 1 | `title` | string | **YES** | 1-250 chars; must be unique within concept | `"The Adelic Qubit v1.1"` |
| 2 | `upload_type` | string | **YES** | Enum: `publication`, `dataset`, `software`, `poster`, `presentation`, `image`, `video`, `lesson`, `physicalobject`, `other` | `"publication"` |
| 3 | `publication_type` | string | IF `upload_type=publication` | Enum: `annotationcollection`, `book`, `section`, `conferencepaper`, `datamanagementplan`, `article`, `patent`, `preprint`, `deliverable`, `milestone`, `proposal`, `report`, `softwaredocumentation`, `taxonomictreatment`, `technicalnote`, `thesis`, `workingpaper`, `other` | `"preprint"` |
| 4 | `description` | string | **YES** | HTML allowed; max 4000 chars; keep version+date+changelog format | `"Version 3.5 — Adelic Cross-Domain..."` |
| 5 | `creators` | array[object] | **YES** | Each object: `name` (required, "Family, Given"), `affiliation` (optional), `orcid` (optional) | `[{"name":"Quni-Gudzinas, Rowan Brad","affiliation":"Independent Researcher","orcid":"0009-0002-4317-5604"}]` |
| 6 | `access_right` | string | **YES** | Enum: `open`, `embargoed`, `restricted`, `closed` | `"open"` |
| 7 | `license` | string | IF `access_right=open` | SPDX identifier | `"CC-BY-4.0"` |
| 8 | `version` | string | Optional | Free-form version string | `"3.6"` |
| 9 | `publication_date` | string | Optional | ISO-8601 date: `YYYY-MM-DD` | `"2026-08-01"` |
| 10 | `keywords` | array[string] | Optional | **MUST be JSON array, NOT comma-joined string.** 2-50 chars each. | `["quantum","UQC","p-adic"]` |
| 11 | `related_identifiers` | array[object] | Optional | Each: `relation` (required), `identifier` (required), `scheme` (optional, `doi`/`url`), `resource_type` (optional) | See Relations table below |
| 12 | `contributors` | array[object] | Optional | Same as `creators` plus `type`: `ContactPerson`, `DataCollector`, `DataCurator`, `DataManager`, `Editor`, `Researcher`, `RightsHolder`, `Sponsor`, `Other` | `[{"name":"Doe, Jane","type":"Editor"}]` |
| 13 | `references` | array[string] | Optional | Raw reference strings (NOT related_identifiers) | `["Author et al. (2024)"]` |
| 14 | `communities` | array[object] | Optional | Each: `identifier` (community slug) | `[{"identifier":"qnfo"}]` |
| 15 | `grants` | array[object] | Optional | Each: `id` (grant DOI) | `[{"id":"10.13039/100000001"}]` |
| 16 | `journal_title` | string | Optional | Publication venue name | `"Foundations of Physics"` |
| 17 | `journal_volume` | string | Optional | Volume number | `"54"` |
| 18 | `journal_issue` | string | Optional | Issue number | `"3"` |
| 19 | `journal_pages` | string | Optional | Page range | `"045201"` |
| 20 | `conference_title` | string | Optional | Conference name | `"APS March Meeting"` |
| 21 | `conference_acronym` | string | Optional | Conference acronym | `"APS2027"` |
| 22 | `conference_dates` | string | Optional | Date range | `"2027-03-15 to 2027-03-19"` |
| 23 | `conference_place` | string | Optional | City, Country | `"Chicago, IL, USA"` |
| 24 | `conference_url` | string | Optional | Conference website | `"https://march.aps.org"` |
| 25 | `conference_session` | string | Optional | Session name | `"Quantum Information"` |
| 26 | `imprint_publisher` | string | Optional | Auto-set | `"Zenodo"` |
| 27 | `imprint_place` | string | Optional | Auto-set | `"Geneva, Switzerland"` |
| 28 | `imprint_isbn` | string | Optional | ISBN (books only) | `"978-3-16-148410-0"` |
| 29 | `partof_title` | string | Optional | Parent work title | `"QNFO Monographs Vol. 3"` |
| 30 | `partof_pages` | string | Optional | Page range in parent | `"45-67"` |
| 31 | `thesis_supervisors` | array[object] | Optional | Same as creators | `[{"name":"Advisor, Thesis"}]` |
| 32 | `thesis_university` | string | Optional | University name | `"Rutgers University"` |
| 33 | `subjects` | array[object] | Optional | Each: `term` (required), `identifier` (URL) | `[{"term":"Quantum Physics"}]` |
| 34 | `language` | string | Optional | ISO 639-1 code | `"eng"` |
| 35 | `notes` | string | Optional | Free-text notes, HTML allowed | `"Part of the QNFO Trilogy."` |
| 36 | `doi` | string | Auto-assigned | Zenodo assigns on publish | `10.5281/zenodo.21736614` |
| 37 | `prereserve_doi` | object | Auto-assigned | Pre-reserved on draft creation | `{"doi":"10.5281/zenodo.XXXXX","recid":XXXXX}` |

#### Related Identifier Relations (field #11)

| Relation | Meaning | Scheme | Example |
|:---------|:--------|:-------|:--------|
| `isNewVersionOf` | New version of prior deposit | `doi` | `"10.5281/zenodo.21725973"` |
| `isPreviousVersionOf` | Prior is older version | `doi` | `"10.5281/zenodo.21725973"` |
| `isVersionOf` | Concept DOI (stable) | `doi` | `"10.5281/zenodo.17176733"` |
| `isSupplementedBy` | External supplement | `url` | `"https://github.com/QNFO/resume"` |
| `cites` | This deposit cites reference | `doi` | `"10.5281/zenodo.21539547"` |
| `obsoletes` | This supersedes reference (errata) | `doi` | Use with BP-4 Correction-on-Discovery |

#### Ready-to-Fill Template — Fresh Deposit (Variant A)

```json
{
  "metadata": {
    "title": "<Paper Title — must match YAML title: exactly>",
    "upload_type": "publication",
    "publication_type": "preprint",
    "description": "<Version N.M — brief summary, date. Use <br> for line breaks.>",
    "creators": [
      {
        "name": "<Family, Given>",
        "affiliation": "<Institution or 'Independent Researcher'>",
        "orcid": "<0000-0000-0000-0000>"
      }
    ],
    "access_right": "open",
    "license": "CC-BY-4.0",
    "version": "<version string, e.g. '1.0'>",
    "publication_date": "<YYYY-MM-DD>",
    "keywords": ["<keyword1>", "<keyword2>", "<keyword3>"],
    "related_identifiers": [
      {
        "relation": "isNewVersionOf",
        "identifier": "<10.5281/zenodo.PREVIOUS_VERSION>",
        "scheme": "doi"
      },
      {
        "relation": "isSupplementedBy",
        "identifier": "https://github.com/<org>/<repo>",
        "scheme": "url"
      }
    ]
  }
}
```

#### Ready-to-Fill Template — New Version Draft (Variant B)

> **CRITICAL:** For drafts via `actions/newversion`, use `upload_type` + `publication_type`
> as **top-level string fields** (NOT nested in a `resource_type` object).
> The nested object form is rejected with `"Not a valid string"`.
> See incident_log in `references/zenodo-deposit-schema.json`.

```json
{
  "metadata": {
    "title": "<SAME title as prior version — must match exactly>",
    "upload_type": "publication",
    "publication_type": "preprint",
    "description": "<Updated description with new version changelog>",
    "creators": [
      {
        "name": "<Family, Given>",
        "affiliation": "<Institution or 'Independent Researcher'>",
        "orcid": "<0000-0000-0000-0000>"
      }
    ],
    "access_right": "open",
    "license": "CC-BY-4.0",
    "version": "<bumped version, e.g. '1.1'>",
    "publication_date": "<YYYY-MM-DD of this version>",
    "keywords": ["<keyword1>", "<keyword2>", "<keyword3>"],
    "related_identifiers": [
      {
        "relation": "isNewVersionOf",
        "identifier": "<10.5281/zenodo.PREVIOUS_VERSION_DOI>",
        "scheme": "doi"
      },
      {
        "relation": "isVersionOf",
        "identifier": "<10.5281/zenodo.CONCEPT_DOI>",
        "scheme": "doi"
      },
      {
        "relation": "isSupplementedBy",
        "identifier": "https://github.com/<org>/<repo>",
        "scheme": "url"
      }
    ]
  }
}
```

#### Template Usage Checklist (MANDATORY — before every metadata PUT)

- [ ] `title` matches paper YAML `title:` exactly (P5.IDENTITY gate)
- [ ] `upload_type` is set — use this, NOT `resource_type`, on newversion drafts
- [ ] `publication_type` is set IF `upload_type=publication`
- [ ] `creators[].name` format is "Family, Given"
- [ ] `keywords` is a JSON array, NOT a comma-joined string
- [ ] `related_identifiers` includes `isNewVersionOf` + `isSupplementedBy`
- [ ] `access_right` is `"open"` and `license` is `"CC-BY-4.0"`
- [ ] Auto-discovered QNFO papers added as `cites` entries (Phase 1 D4 fix)
- [ ] Run `scripts/zenodo-resource-type-fix.py --deposit-id <id>` on resource_type 400
- [ ] **Preview file uploaded first** — `<slug>.pdf` is the first file in the deposit (GATE P5.PREVIEW, v2.41)

#### Common Error Signatures

| Error | Root Cause | Fix |
|:------|:-----------|:----|
| `metadata.resource_type: Missing data` on publish | `upload_type` not set or silently dropped | Set `upload_type` top-level; re-GET to confirm |
| `metadata.resource_type: Not a valid string` on PUT | Nested object on newversion draft | Use Variant B (upload_type + publication_type strings) |
| `metadata.creators: Missing data` | No creators set | Add at least one creator with `name` |
| `keywords` 400 | Comma-joined string, not array | Wrap in `[...]` |
| `actions/newversion` 403 | Stale deposit ID | GET deposit first; check `.zenodo_versions.json` |
| `actions/newversion` 400 `files.enabled: Please remove all files first` | A newversion draft ALREADY EXISTS for this deposit (previous newversion call created it, or a concurrent session left one unsubmitted) | Do NOT call newversion again. GET the deposit and follow `links.latest_draft` to the existing draft; complete it (delete stale files → upload correct files → set metadata → publish). If the draft is a stale leftover, DELETE its files first, then reuse it. Creating a parallel newversion fragments the version chain (2026-08-02 ODR incident: deposit 21751722, draft 21752136). |
| Upload 415 | Missing Content-Type | Use `Content-Type: application/octet-stream` |

---

### Zenodo Upload (with retry + versioning)

**HARD GATE P5.PDF (KIF-30, MANDATORY — 2026-07-26): PDF RENDERING AND INCLUSION IS REQUIRED.**
**Zenodo does NOT render complex mathematical markdown natively.** A markdown-only deposit
is unreadable to human consumers on zenodo.org. Before ANY Zenodo upload:

1. All papers MUST be rendered to publication-quality PDFs via `scripts/build-paper.py`
2. ALL rendered PDFs MUST be confirmed present locally (`Test-Path` for every `.pdf`)
3. ALL rendered PDFs MUST be uploaded individually to the Zenodo deposit — in addition to
  the PROVENANCE-BUNDLE.zip that contains the source markdown
4. The PDF rendering pipeline ensures zero U+FFFD/U+FFFF errors (see §PDF Building)
5. This gate applies to both brand-new deposits AND new versions of existing deposits

**GATE:** If the deposit's file list does not contain individual PDFs for every paper,
the deposit is INCOMPLETE. A markdown-only deposit is a publication protocol violation
and must be remediated before the deposit is considered valid.

**Why this matters:** GitHub beautifully renders markdown in-browser. Zenodo does not.
A reader who visits a Zenodo landing page and downloads the markdown will see raw LaTeX
(`\mathbb{Z}`, `\mathrm{SU}(2)`, etc.) — not mathematical notation. The PDF is the
human-readable artifact. The markdown is the machine-readable source. Both are required.

**HARD GATE (kaizen fix A3):** `PROVENANCE-BUNDLE.zip` MUST be built and
verified BEFORE any Zenodo upload begins -- not added ad hoc during the
upload step. The bundle MUST contain: `<slug>.md`, `<slug>.pdf`,
`PROJECT-PLAN.md`, `README.md`, all `artifacts/*.md`, all `docs/*.md`.
Verify before upload:
```bash
# Windows-safe: write to _check_bundle.py, then exec; never inline python -c
python _check_bundle.py
```
`_check_bundle.py` content:
```python
import zipfile, sys
z = zipfile.ZipFile('PROVENANCE-BUNDLE.zip')
names = z.namelist()
# Check for slug-based filenames (not generic paper.md)
required_prefixes = ['.md', '.pdf']
has_md = any(n.endswith('.md') and 'PROJECT-PLAN' not in n and 'README' not in n for n in names)
has_pdf = any(n.endswith('.pdf') for n in names)
missing = []
if not has_md: missing.append('slug.md')
if not has_pdf: missing.append('slug.pdf')
print('Bundle contents:', names)
sys.exit(1 if missing else 0)
```
If this check is not run and passed, the Zenodo deposit is INCOMPLETE even
if `actions/publish` succeeds -- missing provenance is a silent failure, not
a hard error, so it must be caught here.

**BP-4 Correction-on-Discovery Protocol `[DESIGN — v2.39]`**

When an error is discovered in a published paper, correct it in the SAME session:
1. GitHub: add ERRATA.md with specific claim/error/correction/ACRP paper DOI.
2. Zenodo: `actions/newversion` from latest deposit → set `obsoletes` related_identifier → SUPERSESSION NOTICE → publish.
3. KG: create CORRECTS/SUPERSEDES edge via qnfo-gateway /sync.
4. If source permanently lost: flag in KG with `corruption_flag: true`.

**BP-5 KG Correction Edge Protocol `[DESIGN — v2.39]`**

Every correction MUST create a KG edge — without it, the correction is invisible to KG-First Discovery:
- Paper corrects claim: `CORRECTS` edge
- New version fully replaces: `SUPERSEDES` edge
- Error bounded but no new version: `OBSOLETES` edge
Use qnfo-gateway `/sync` with edge contract: `{id, source_id, target_id, relationship_type, properties}`.
Verify: `curl graph-api.qnfo.org/neighbors/<corrected-id>`.

**HARD GATE P5.IDENTITY (KIF-58, MANDATORY — 2026-07-31): CROSS-PROJECT PAPER IDENTITY VERIFICATION.**

Before ANY file upload to Zenodo OR any cross-population of files between Zenodo and GitHub:

1. **Verify paper title matches target Zenodo concept.** Read the paper's YAML `title:` field. Compare against the target Zenodo deposit's `title` field (via `GET /api/deposit/depositions/{id}`). They MUST match exactly. A title mismatch means the wrong paper is being uploaded.
2. **Verify paper DOI belongs to the target concept.** The paper's YAML `doi:` MUST belong to the same concept DOI as the target Zenodo deposit. If the paper references a different concept DOI, it belongs to a different project.
3. **Verify GitHub repo paper identity (REPO-TARGET GATE extension).** Before pushing files to any GitHub repo in the context of a Zenodo upload, verify the repo's existing `paper.md` YAML `title:` matches the paper being pushed. ADR-026's REPO-TARGET GATE (check `git remote -v`) is necessary but NOT sufficient — it confirms the repo URL, not the paper identity. A repo can be the correct target URL but contain the wrong paper.
4. **Verify temp directory content (KIF-32 extension).** If working from a temp directory, NEVER assume the directory name identifies the project. Read `paper.md` YAML frontmatter (`title:` + `doi:`) before using its contents for upload or cross-population.
5. **Zenodo bucket lock awareness.** A published Zenodo deposit CANNOT have its files deleted or overwritten (HTTP 403 "Bucket is locked for modifications"). Verify file contents before `actions/publish` — once published, wrong files are permanently tainted in that version DOI.

**GATE:** If any of checks 1-4 fail, BLOCK the upload/cross-population. A Zenodo deposit with wrong paper content is a PERMANENT contamination. This gate prevents the exact failure mode seen in the 2026-07-31 JPCUB-vs-Computing-Machines cross-contamination incident where "Computing After Silicon" paper files (31,785 bytes) were uploaded to the JPCUB Zenodo concept (21715609), and JPCUB paper content was pushed to the computing-machines GitHub repo. Cross-reference: KIF-58, memory "Do not assume temporary directory names identify the project."

#### 1. Create Deposit
```python
POST https://zenodo.org/api/deposit/depositions
Headers: Authorization: Bearer <ZENODO_TOKEN>
Body: {} # Empty metadata to create draft
```

#### 2. Upload Files — Preview-First Ordering (MANDATORY, v2.41)

**PREVIEW FILE DESIGNATION RULE:** Zenodo uses the **first file uploaded** to a deposit
as the landing-page preview/thumbnail. Upload order is therefore NOT arbitrary — it
controls how the deposit appears on zenodo.org search results, the concept page, and
third-party aggregators. Upload files in this EXACT priority order:

| Priority | File | Rationale |
|:---------|:-----|:----------|
| **1st (PREVIEW)** | `<slug>.pdf` | Main publication PDF — the human-readable artifact, always the best preview |
| **2nd** | `README.md` | Project overview — fallback preview if PDF build failed |
| **3rd** | `<slug>.md` | Primary markdown source — fallback preview if README absent |
| **4th** | `PROVENANCE-BUNDLE.zip` | Bundle of all source artifacts |
| **Remaining** | `artifacts/*.pdf` and other files | Individual document PDFs, supplementary data |

**If no PDF exists** (a build-only failure — the deposit MUST still include a PDF per
HARD GATE P5.PDF; do not skip the PDF requirement): fall back to README.md as the
preview, uploading it first. If neither PDF nor README exists, use `<slug>.md`.

**BUCKET URL RULE (v2.43, HARD):** The file upload endpoint is the deposit's **bucket URL**, extracted from the deposit record's `links.bucket` field — a UUID path (`https://zenodo.org/api/files/{uuid}`). NEVER construct the upload URL manually (e.g. `/api/files/{deposit_id}`) — the deposit ID is NOT the bucket UUID and manual construction returns HTTP 500 on upload. Procedure:
```python
# 1. Extract the REAL bucket URL from the deposit record
r = requests.get(f'https://zenodo.org/api/deposit/depositions/{id}', headers=headers)
bucket = r.json()['links']['bucket']   # e.g. https://zenodo.org/api/files/6f8a4407-...
# 2. Upload to bucket_url + '/' + filename (NOT /api/files/{deposit_id})
requests.put(f'{bucket}/{filename}', headers=headers, data=open(path,'rb'))
```
This is the canonical pattern already implemented in `scripts/zenodo-create-upload.py` (`upload_file` uses `f'{bucket_url}/{name}'` with the bucket URL returned by `create_deposit`). Follow the script, not the deprecated path below.

```python
# Upload the PREVIEW FILE FIRST, then remaining files in order
# DEPRECATED WRONG PATH (returns HTTP 500): PUT /api/deposit/depositions/{id}/files/<file>
# CORRECT: PUT {links.bucket}/{filename} — see BUCKET URL RULE above
PUT https://zenodo.org/api/files/{bucket_uuid}/<slug>.pdf    # ALWAYS first (PREVIEW)
PUT https://zenodo.org/api/files/{bucket_uuid}/README.md      # second
PUT https://zenodo.org/api/files/{bucket_uuid}/<slug>.md      # third
PUT https://zenodo.org/api/files/{bucket_uuid}/PROVENANCE-BUNDLE.zip  # fourth
PUT https://zenodo.org/api/files/{bucket_uuid}/<artifact>.pdf # remaining
```

**GATE P5.PDF:** Do not proceed to Step 3 until ALL PDFs AND the bundle are confirmed
present in the deposit's file list (`GET /api/deposit/depositions/{id}/files`).
This is a HARD GATE — a deposit without individual PDFs is INCOMPLETE and must
be remediated before publishing. See HARD GATE P5.PDF (KIF-30) above.

**GATE P5.PREVIEW (v2.41):** After uploading all files, verify the FIRST entry in
the deposit's file list IS the intended preview file (`<slug>.pdf`). If the first
file is NOT the PDF, the upload order was wrong and the preview is incorrect —
re-upload the PDF last (which will move it… actually, re-upload the files in the
correct order by deleting all files first, then re-uploading with the PDF first):
```python
# Verify preview file is first
GET https://zenodo.org/api/deposit/depositions/{id}/files
# Check: files[0].filename == '<slug>.pdf' — if not, BLOCK and re-order.
```

#### 3. Set Metadata
```python
PUT https://zenodo.org/api/deposit/depositions/{id}
Body: {
  "title": "...",
  "creators": [{"name": "..."}],
  "description": "...",
  "access_right": "open",
  "license": "CC-BY-4.0",
  "related_identifiers": [
    {"relation": "isNewVersionOf", "identifier": "10.5281/zenodo.PREVIOUS"},
    {"relation": "isSupplementedBy", "identifier": "https://github.com/..."},
    {"relation": "cites", "identifier": "10.5281/zenodo.CITED"}
  ]
}
```
**Auto-discover related QNFO papers (kaizen fix D4):** before hand-writing
`related_identifiers`, query the KG for prior QNFO publications on the same
topic/program so cross-references aren't missed:
```
query_graph({endpoint: "query", params: {query: "MATCH (p:Paper)-[:BELONGS_TO]->(d) WHERE d.name CONTAINS '<domain>' RETURN p.title, p.doi"}})
```
Add a `{"relation": "cites", "identifier": "<doi>"}` entry for each relevant
result found this way, in addition to any DOIs the author already knows to cite.

#### 4. Publish
```python
POST https://zenodo.org/api/deposit/depositions/{id}/actions/publish
```

#### 5. Verify
```bash
# Windows: use curl.exe (not PowerShell alias) and write Python to file, never pipe to python -c
curl.exe -sI https://doi.org/10.5281/zenodo/{id} # Must return HTTP 200
curl.exe -s https://zenodo.org/api/records/{id} -o _zenodo_record.json
python _verify_zenodo.py
```
`_verify_zenodo.py` content:
```python
import json
with open('_zenodo_record.json', 'r', encoding='utf-8') as f:
  r = json.load(f)
print('DOI:', r.get('doi'))
print('Related:', len(r.get('related_identifiers', [])))
```

#### Zenodo Retry Protocol
If Zenodo API returns 500 or timeout: retry up to 3 times with exponential backoff (1s, 4s, 16s). If deposit exists from prior attempt: recover draft via `GET /api/deposit/depositions?q=<title>`, update rather than recreate.

#### Version Chain Tracking (kaizen fix C2 -- `.zenodo_versions.json`)
Zenodo's concept-DOI/version-DOI split is easy to get wrong: calling
`actions/newversion` on a STALE deposit ID (not the latest version) returns
HTTP 403. Maintain a tracking file at the project root:
```json
{
 "concept_doi": "10.5281/zenodo.XXXXXXX",
 "latest_deposit_id": "YYYYYYY",
 "versions": [
  {"doi": "10.5281/zenodo.XXXXXXX", "deposit_id": "YYYYYYY", "tag": "v1.0", "published_at": "2026-07-20"}
 ]
}
```
Before calling `actions/newversion`, ALWAYS verify with a GET first:
```bash
curl -s -H "Authorization: Bearer $ZENODO_TOKEN" https://zenodo.org/api/deposit/depositions/<latest_deposit_id>
```
If the GET fails or the record's `state` shows it is not the latest, look up
the current latest via the concept DOI's `GET /api/records/?q=conceptdoi:"<concept_doi>"`
before proceeding. Update `.zenodo_versions.json` immediately after every
successful publish -- this file is the single source of truth for "what is
the latest deposit ID", preventing the fragmented-citation-record failure
mode where a disconnected new deposit gets created because the correct ID
was lost or misremembered.

#### Zenodo Versioning for Phase/Session Conclusions (MANDATORY -- see qnfo-agent §8.5 JIT Thin-Client Protocol, Phase-End and Session/Project-Conclusion Checkpoint subsections)

**PRE-CHECK (HARD, 2026-08-02): BEFORE calling `actions/newversion`, check for an
existing unsubmitted draft.** A prior newversion call (or a concurrent session) may
have already created a draft for this deposit. Calling `actions/newversion` again
returns HTTP 400 `files.enabled: Please remove all files first`. Detection:
```python
# 0. Check for existing unsubmitted drafts (authenticated deposit API)
GET /api/deposit/depositions?q=<title>&size=25
# Look for any hit with state == "unsubmitted" — that IS the draft to complete.
# If found, skip the newversion POST entirely and use that draft's ID.
#   - If its files are stale: DELETE them, upload correct files, set metadata, publish.
#   - If it is a concurrent session's in-flight work (recently modified): do NOT
#     touch it — coordinate instead. (2026-08-02 ODR incident: deposit 21751722,
#     concurrent draft 21752136 left unsubmitted since 08-01T23:26Z.)
```
Then proceed with the normal flow:

At every session or phase conclusion for a project with an existing Zenodo
deposit, create a NEW VERSION rather than a disconnected upload:
```python
# 1. Create a new version draft of the existing concept
POST https://zenodo.org/api/deposit/depositions/{existing_id}/actions/newversion
# Response includes a "latest_draft" link -> extract new draft deposit ID

# 2. MANDATORY: DELETE ALL stale files BEFORE uploading new ones (GATE P5.CLEAN, v2.45)
#    actions/newversion copies old files from the source deposit — they persist
#    and can become the wrong preview file. DELETE them all first.
GET https://zenodo.org/api/deposit/depositions/{new_id}/files  # enumerate
for file in response.json():
  DELETE https://zenodo.org/api/deposit/depositions/{new_id}/files/{file['id']}
# THEN upload the full fresh set in preview-first order (PDF, README, slug.md, bundle, REST)

# 3. Update metadata (bump version string, e.g. "1.0" -> "1.1")
PUT https://zenodo.org/api/deposit/depositions/{new_id}
Body: {"metadata": {"version": "1.1", ...}}

# 4. Publish the new version
POST https://zenodo.org/api/deposit/depositions/{new_id}/actions/publish
```
This keeps ALL phase-by-phase snapshots under one **concept DOI** (stable,
never changes) with each phase getting its own **version DOI** (changes per
version). Never create a brand-new unrelated Zenodo deposit for what is
really the next phase/version of an existing project -- that fragments the
citation record and breaks `isNewVersionOf`/`isPreviousVersionOf` relations.
Only use a genuinely NEW deposit for a genuinely NEW, unrelated publication.

---

## Phase 6: Cloudflare Deployment

### D1 Access Protocol (kaizen fix 2026-07-21 -- read BEFORE any D1 call)

**CANONICAL (KIF-36, 2026-07-27):** Use `cloudflare/scripts/d1-query.py` instead of
manual Steps 1-3 below. It auto-discovers token, account ID, and DB UUID:
```bash
python cloudflare/scripts/d1-query.py --db living-paper --sql "SELECT ..." --params ...
```
The script handles token discovery (4 sources), account ID (`npx wrangler whoami`),
DB UUID (`npx wrangler d1 list`), and session caching. Steps 4-6 (check-then-write,
verify, papers-server check) still apply after querying.

**Root-cause incident:** A session spent 8+ failed tool calls on D1 because
of (a) a wrong hardcoded Cloudflare account ID, (b) attempting
`wrangler d1 execute <name> --remote` against a database with no local
`wrangler.toml` binding, and (c) an `ON CONFLICT` upsert against a table
with FTS5 shadow tables, which returned HTTP 400. None of these were
"D1 is broken" -- all three were preventable with the sequence below.

**Step 1 -- ALWAYS get the live account ID first, never hardcode it:**
```bash
npx wrangler whoami
# prints Account Name + Account ID directly from the live CLOUDFLARE_API_TOKEN
```

**Step 2 -- list databases to get the live UUID (never hardcode a UUID either):**
```bash
npx wrangler d1 list
# or via REST: GET https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/d1/database
```
Known QNFO database (as of 2026-07-21, ALWAYS re-verify via Step 2, do not
trust this table blindly in future sessions): `living-paper` database
contains the `papers` table (also `papers_fts*` FTS5 shadow tables --
`period_matrices`, `citations`, `citation_edges`, `paper_clusters`,
`paper_versions`, `selmer_generators`).

**Step 3 -- if the DB has no local wrangler.toml binding, use the REST API
directly (write a `.py` file first per kaizen fix B1, never inline):**
```python
import urllib.request, os, json
TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN')
ACCOUNT = '<from Step 1>'
DB = '<uuid from Step 2>'
URL = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/d1/database/{DB}/query'
HEADERS = {'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'}

def d1_query(sql, params=None):
  body = json.dumps({'sql': sql, 'params': params or []})
  req = urllib.request.Request(URL, data=body.encode(), headers=HEADERS)
  return json.loads(urllib.request.urlopen(req).read())
```

**Step 4 -- CHECK-THEN-WRITE, never a combined upsert on `papers`:**
```python
# 1. Check existence first
exists = d1_query("SELECT COUNT(*) as c FROM papers WHERE slug = ?", [slug])['result'][0]['results'][0]['c']

# 2a. If not present: plain INSERT (no ON CONFLICT)
if not exists:
  d1_query(
    "INSERT INTO papers (slug, title, body_md, abstract, authors, doi, status, version) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    [slug, title, body_md, abstract, authors, doi, status, version]
  )
# 2b. If present: plain UPDATE
else:
  d1_query(
    "UPDATE papers SET body_md = ?, doi = ?, status = ?, version = ? WHERE slug = ?",
    [body_md, doi, status, version, slug]
  )
```
Note the column is `body_md`, not `body` -- verify column names with
`SELECT name FROM sqlite_master WHERE type='table' AND name='papers'`
followed by `PRAGMA table_info(papers)` if unsure, rather than assuming.
An `ON CONFLICT(slug) DO UPDATE` on this specific table returned HTTP 400
in production testing (2026-07-21) -- avoid it until root-caused further;
the check-then-write pattern above is the confirmed-working alternative.

**Step 5 -- verify via independent re-query (Anti-Phantom Gate):**
```python
rows = d1_query("SELECT slug, title, doi, status FROM papers WHERE slug = ?", [slug])['result'][0]['results']
assert rows, "INSERT/UPDATE did not persist -- do not report success"
```

**Step 6 -- verify papers-server actually serves it:**
```bash
curl -sI https://papers.qnfo.org/papers/<slug>/ # Both with and without trailing slash resolved as of 2026-07-30; trailing slash is canonical
```

### Papers-Server Worker Verification
```bash
# Windows: use curl.exe and write Python to file, never pipe to python -c
curl.exe -sI https://papers.qnfo.org/papers/<slug>/ # Must return HTTP 200
curl.exe -s https://papers.qnfo.org/papers/<slug>/ -o _papers_check.html
python _papers_verify.py <slug>
```
`_papers_verify.py` content:
```python
import sys
with open('_papers_check.html', 'r', encoding='utf-8') as f:
  c = f.read()
print('MathJax:', 'MathJax' in c)
print('Size:', len(c))
```

### R2 Archive
```bash
npx wrangler r2 object put releases/<YYYY>/<MM>/<slug>/<slug>.md --file=<slug>.md --remote
npx wrangler r2 object put releases/<YYYY>/<MM>/<slug>/<slug>.pdf --file=<slug>.pdf --remote
```

### Knowledge Graph Seed
Seed Paper node with: slug, DOI, title, author, pages_url, zenodo_url, r2_path. Connect BELONGS_TO domain/program edges.

### MCP-Driven Deployment Verification (HARD GATE — v2.25)

**MANDATORY after every D1 insert, R2 upload, or Worker deployment.** The prior
practice of `curl /health` or `npx wrangler` exit-code checks is insufficient —
it confirms the REQUEST was accepted, not that the artifact is live and healthy.
This gate replaces single-source verification with a cross-MCP verification chain.

**Verification chain (execute in order, ALL must pass before declaring deployment complete):**

```
1. cloudflare-builds   → confirm deploy/push succeeded, get build ID + timestamp
2. cloudflare-observability → confirm Worker is receiving healthy invocations (0 errors)
3. cloudflare-bindings  → verify declared wrangler.jsonc bindings match actual runtime
4. cloudflare-auditlogs  → confirm deploy action appears in account audit trail
```

**For D1/R2-only changes (no Worker deploy):**
```
1. cloudflare       → re-query the D1 row or R2 object to confirm write persisted
2. cloudflare-auditlogs  → confirm the write action is recorded
```

**Gate criteria:**
- `cloudflare-builds` returns a successful build with timestamp ≤ 5 min old
- `cloudflare-observability` shows ≥ 1 healthy invocation since build timestamp
- `cloudflare-bindings` shows zero missing/extra bindings
- `cloudflare-auditlogs` contains a matching action entry

**If any MCP server is unreachable:** fall back to the existing CLI/REST verification
(`npx wrangler deployments list`, `curl /health`, `GET /accounts/{id}/audit_logs`)
but explicitly flag `[MCP-UNAVAILABLE: <server>, fell back to CLI]`. Never silently
skip verification.

See `cloudflare` skill v3.9 §MCP-Driven Operations for the full decision matrix.

---

## Phase 7: Dissemination & Permanence

### SEO Audit (MANDATORY before declaring publication complete)

1. **robots.txt** — verify at root of papers.qnfo.org: allows crawling, points to sitemap
2. **sitemap.xml** — all paper pages listed with lastmod dates
3. **llms.txt** — machine-readable paper index for AI crawlers at papers.qnfo.org/llms.txt
4. **Meta tags** — `citation_title`, `citation_author`, `citation_doi`, `citation_date`
5. **Structured data** — Schema.org `ScholarlyArticle` with `@id`, `headline`, `author`, `datePublished`, `identifier` (DOI)
6. **Open Graph** — `og:title`, `og:description`, `og:type` (article), `og:url`

### Buffer Social Media (v2.11 — COMPLETE REWRITE, 2026-07-21)

> **v2.11 BUFFER MIGRATION:** The legacy `api.bufferapp.com/1.0/graphql.json` endpoint
> and `createDraft` mutation are **DEPRECATED** as of 2026-07-21. All Buffer API calls
> now use `https://api.buffer.com` with the `createPost` mutation. Verified live
> with 3-channel posting (Twitter, LinkedIn, Bluesky) for the Informational Universe
> paper. Old channel IDs are stale — ALWAYS discover live IDs via the channels query
> below; never hardcode them.

#### Endpoint & Auth

```
URL:   https://api.buffer.com/graphql  (also works at bare https://api.buffer.com — both resolve)
Auth:  Authorization: Bearer <token>
Method: POST with JSON GraphQL body
Legacy: api.bufferapp.com/1.0/graphql.json → 404 (DOMAIN DEPRECATED)
```

#### Buffer 401 Diagnostic Protocol (MANDATORY — v2.12, 2026-07-21)

**INCIDENT (2026-07-21):** A session diagnosed a working Buffer Personal Access
Token (43 chars, suffix `14Ky`, all 7 scopes active, created 2026-06-21) as
"stale/expired" after a single `urllib.request` call returned HTTP 401, delaying
dissemination by an entire session. The token was NEVER the problem — a transient
or request-format issue caused the 401, and the endpoint `https://api.buffer.com`
with the GraphQL query below works perfectly. **The token was subsequently
confirmed live in the SAME session with the SAME endpoint, SAME token value,
and SAME query — the original 401 was a false alarm.**

**THE RULE: NEVER diagnose a Buffer 401 as "stale token" without running
the endpoint-discovery diagnostic FIRST. A single 401 from a single call
is INSUFFICIENT EVIDENCE to declare a token dead.**

**Diagnostic script (write to `_buffer_diag.py`, never inline per kaizen B1):**

```python
import urllib.request, json, os
TOKEN = os.environ.get('BUFFER_TOKEN') # NEVER hand-copy

endpoints = [
  ('GraphQL api.buffer.com', 'POST',
   'https://api.buffer.com',
   json.dumps({"query": "query { account { organizations { id } } }"}).encode(),
   {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}),
  ('GraphQL api.buffer.com/graphql', 'POST',
   'https://api.buffer.com/graphql',
   json.dumps({"query": "query { account { organizations { id } } }"}).encode(),
   {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}),
]
for label, method, url, body, headers in endpoints:
  try:
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    resp = urllib.request.urlopen(req, timeout=15)
    print(f'OK {label}: HTTP {resp.getcode()}')
  except urllib.error.HTTPError as e:
    print(f'FAIL {label}: HTTP {e.code}')
  except Exception as e:
    print(f'FAIL {label}: {e}')
```

**Decision tree:**
- GraphQL at `api.buffer.com` returns 200 → token works, proceed with posting
- GraphQL at `api.buffer.com` returns 401 → try `api.buffer.com/graphql`
- Both GraphQL endpoints return 401 → token is genuinely stale, regenerate
- **Never try REST endpoints** (`api.bufferapp.com/1/*`) for diagnosis —
 Buffer Personal Access Tokens are GraphQL-only; REST returns 401
 `"Public API tokens are not accepted for REST API access"` even for
 valid tokens, producing a FALSE diagnostic

**This protocol MUST be run before any "stale token" diagnosis.** If it
passes, and the posting attempt still fails with 401, the problem is with
the request format (GraphQL query syntax, escaping, channel ID, text length)
— NOT the token.

#### Channel Discovery (MANDATORY — run before any post)

Never hardcode channel IDs. Always discover them live:

```python
import json, urllib.request

TOKEN = os.environ.get('BUFFER_TOKEN')
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

# Step 1: Get organization ID
query = {"query": "query { account { organizations { id } } }"}
req = urllib.request.Request('https://api.buffer.com', data=json.dumps(query).encode(), headers=HEADERS)
org_id = json.loads(urllib.request.urlopen(req).read())['data']['account']['organizations'][0]['id']

# Step 2: Get channels
query = {"query": f'query {{ channels(input: {{ organizationId: "{org_id}" }}) {{ id name service }} }}'}
req = urllib.request.Request('https://api.buffer.com', data=json.dumps(query).encode(), headers=HEADERS)
channels = json.loads(urllib.request.urlopen(req).read())['data']['channels']

for c in channels:
  print(f" {c['service']}: {c['name']} -> {c['id']}")
```

**Verified live channel IDs (2026-07-21 — ALWAYS re-discover, do not trust this table):**

| Platform | channelId | Profile |
|:---------|:----------|:--------|
| Twitter/X | `685cd2c2acfb098c697a8786` | @RowanQuni |
| LinkedIn | `6a170337c687a22dd430685f` | rowan-quni |
| Bluesky | `6a01d129090476fb9909d885` | Rowan Brad Quni-Gudzinas |

#### Post Creation (Buffer GraphQL — v2.13, 2026-07-22)

**Mutation:** `createPost` (replaces deprecated `createDraft`)

```graphql
mutation {
 createPost(input: {
  channelId: "<liveIdFromDiscovery>",
  text: "<post text>",
  schedulingType: automatic,   # REQUIRED enum: automatic | notification
  mode: addToQueue,       # REQUIRED enum: addToQueue | shareNow | shareNext | customScheduled
  assets: [],          # REQUIRED non-null list — always pass [] (empty list)
  saveToDraft: false       # optional: true = draft mode
 }) {
  __typename           # MANDATORY — PostActionPayload is a UNION
 }
}
```

**CRITICAL RULES (v2.14 — 2026-07-22, corrected):**
1. NEVER use `createDraft` — it no longer exists. Use `createPost`.
2. **The `assets` field is NON_NULL and REQUIRED.** Always pass `assets: []` (empty list). Omitting it causes `InvalidInputError`.
3. **Inline fragments on `PostActionPayload` DO WORK — v2.13's claim otherwise was FALSE and is retracted.** `PostActionPayload` is a real GraphQL union and its members (`PostActionSuccess`, `InvalidInputError`, `UnauthorizedError`, `UnexpectedError`, `NotFoundError`, `LimitReachedError`, `RestProxyError` — confirmed via `__type(name: "PostActionPayload") { possibleTypes { name } }`) ARE valid inline-fragment targets. The v2.13 error (`Unknown type "PostActionSuccess"`) was caused by fragmenting on a NON-existent type name (e.g. `Post`), not by a union limitation. **Always request `message` inside every error-variant fragment and `post { id }` inside `PostActionSuccess`** — querying only `__typename` throws away the single most useful piece of debugging information Buffer provides (e.g. the exact "10 scheduled posts out of 10 allowed" queue-limit text). See `scripts/buffer-post.py` v1.1 for the corrected, verified-live mutation.
4. `schedulingType: automatic` and `mode: addToQueue` are both REQUIRED. The `notification` enum value exists in the schema but does NOT work for posting — use `automatic`.
5. Twitter text limit: ~280 characters AFTER URL shortening (Buffer shortens URLs to ~23 chars, so raw text including URL can be up to ~410 chars). Bluesky limit: ~300 characters raw text. Violations return `InvalidInputError` with an exact message inside `data.createPost` (via the `... on InvalidInputError { message }` fragment) — read it rather than guessing.
6. Endpoint is `https://api.buffer.com/graphql` (preferred). The bare `https://api.buffer.com` also works. Legacy endpoint `https://api.bufferapp.com/1.0/graphql.json` returns 404.
7. **All enum values MUST be unquoted GraphQL identifiers** (e.g., `automatic` not `"automatic"`). Quoting them as strings causes `Enum "SchedulingType" cannot represent non-enum value`.
8. **`LimitReachedError` is a genuine account-level constraint (e.g. "10 scheduled posts out of 10 allowed"), not an agent/script failure.** It requires the human user to clear their Buffer queue or upgrade their plan — do not retry, do not treat as a bug to fix, and disclose it plainly as `[BLOCKED: account queue limit, user action required]` rather than a phantom "posted" claim.

#### Post Deletion

```graphql
mutation {
 deletePost(input: { id: "<postId>" }) {
  __typename
  ... on DeletePostSuccess { id }
  ... on VoidMutationError { message }
 }
}
```

#### Post Verification (Anti-Phantom Gate)

After posting, verify independently:

```python
# VERIFIED 2026-07-31: The GraphQL schema REJECTS `posts` as a field on
# type `Channel` — "Cannot query field "posts" on type "Channel""
# (GRAPHQL_VALIDATION_FAILED). The prior channels+posts subquery shape is
# STALE and MUST NOT be used. There is no confirmed post-enumeration query
# on the current schema. Verification alternatives:
#  a) createPost mutation response: inline fragment on PostActionSuccess
#   returns post { id } — this ID is the proof of acceptance.
#  b) Manual dashboard check by the user for scheduled posts.
# If posts were created via createPost and returned a post ID, that is the
# primary verification signal; a subsequent failed enumeration query does
# NOT disprove the post's existence.
query = {"query": """query {
 channels(input: { organizationId: "ORG_ID" }) {
  id name service
 }
}"""}
```

#### Token Protocol (v2.11 — REDUNDANT STORAGE MANDATORY)

Token is a Buffer Personal Access Token, 43 characters, suffix `14Ky`.

**Required storage locations (ALL 4-5 MUST exist, never rely on one):**
1. `%USERPROFILE%\buffer\token` — primary file
2. `%USERPROFILE%\.buffer_token` — fallback file
3. `%USERPROFILE%\keys.json` — `buffer_token` key in JSON doc
4. Environment variable `BUFFER_TOKEN` (session)
5. Environment variable `BUFFER_TOKEN` (user — set via `[Environment]::SetEnvironmentVariable`)

**Token format:** 43 chars, random alphanumeric + underscores, suffix `14Ky`.

**Token verification (MANDATORY before any post):**
```python
query = {"query": "query { account { organizations { id } } }"}
req = urllib.request.Request('https://api.buffer.com', data=json.dumps(query).encode(), headers=HEADERS)
resp = json.loads(urllib.request.urlopen(req).read())
# HTTP 200 + valid org_id = token works. 403/401 = dead token.
```

**Token regeneration:** Go to https://buffer.com → Settings → API Access Tokens. Overwrite ALL 4-5 storage locations with the new value immediately.

#### Red-Team / Anti-Patterns for Buffer

| Anti-Pattern | Correct |
|:-------------|:--------|
| `createDraft` mutation | `createPost` (v2.11 migration) |
| `api.bufferapp.com/1.0/graphql.json` endpoint | `https://api.buffer.com/graphql` |
| Hardcoded channel IDs | Discover live via channels query |
| Querying only `__typename` without `message` on error fragments | Request `message` inside every error-variant fragment (`InvalidInputError`, `LimitReachedError`, etc.) — it contains the exact actionable reason (v2.14 fix) |
| Claiming "inline fragments don't work on PostActionPayload" | FALSE (v2.13 error) — fragments DO work; the real bug was fragmenting on a non-existent type name like `Post` instead of a real union member (v2.14 fix, verified live) |
| Omitting `assets: []` in input | `assets` is NON_NULL required — always pass `assets: []` |
| Quoting enum values like `"automatic"` | Unquoted GraphQL identifiers: `automatic` (v2.13 fix) |
| Using `schedulingType: notification` | Use `automatic` — `notification` exists in schema but doesn't work |
| Single token location | 4-5 redundant locations |
| Diagnosing 404 as "token dead" | 404 from legacy endpoint = endpoint deprecated, not token |
| Diagnosing Buffer 401 as "stale token" without diagnostic | Run Buffer 401 Diagnostic Protocol — test GraphQL at `api.buffer.com` first; a single HTTP 401 is INSUFFICIENT evidence to declare a token dead |
| Twitter text > 280 chars after URL-shorten | Trim raw text to ≤410 chars (Buffer shortens URLs to ~23 chars) |
| Diagnosing "stale token" from truncated PowerShell output | ALWAYS read token via Python `open().read().strip()` — PowerShell `Get-Content` can return stale/cached values |
| Treating `LimitReachedError` as an agent bug and retrying indefinitely | It's a genuine account-level queue cap (e.g. 10/10 scheduled posts) — disclose as `[BLOCKED: account queue limit]`, do not retry, requires user to clear queue or upgrade plan (v2.14) |

#### Post Format
```
Title: <paper title>
DOI: <doi>
Paper URL: <papers.qnfo.org/papers/slug/>
Abstract: <1-2 sentence summary>
Hashtags: #QNFO #Research <domain-specific tags>
```

### IPFS Distribution — Cloudflare + DNSLink ONLY (v2.10, MANDATORY method)

**All third-party pinning services are deprecated (see v2.10 banner).**
The canonical, permanent QNFO IPFS distribution method is three steps,
zero third-party dependencies:

**Step 1 -- Compute the CIDv1 locally (no pinning service call needed for
content-addressing itself; write a `.py` file, never inline per kaizen B1):**
```python
import hashlib

def compute_cidv1(filepath):
  """CIDv1: raw codec (0x55) + sha2-256 multihash, base32-encoded (RFC4648, lowercase, no padding)."""
  with open(filepath, 'rb') as f:
    content = f.read()
  digest = hashlib.sha256(content).digest()
  cidv1_bytes = bytes([0x01, 0x55, 0x12, 0x20]) + digest # cidv1 + raw + sha2-256 + 32-byte len
  alphabet = 'abcdefghijklmnopqrstuvwxyz234567'
  bits, value, result = 0, 0, 'b'
  for byte in cidv1_bytes:
    value = (value << 8) | byte
    bits += 8
    while bits >= 5:
      bits -= 5
      result += alphabet[(value >> bits) & 0x1f]
  if bits > 0:
    result += alphabet[(value << (5 - bits)) & 0x1f]
  return result
```

**Step 2 -- Upload the durable byte-store to Cloudflare R2 (the CID is a
label for the content, R2 is what actually keeps it alive and servable):**
```bash
npx wrangler r2 object put qnfo-projects/<repo>/<file> --file=<local-path> --remote
```

**Step 3 -- Create DNSLink TXT records on Cloudflare DNS (the ONLY naming
layer -- write a `.py` file, never inline):**
```python
import urllib.request, os, json
TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN')
HEADERS = {'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'}
BASE = 'https://api.cloudflare.com/client/v4'

# Get zone ID once per domain
req = urllib.request.Request(f'{BASE}/zones?name=qnfo.org', headers={'Authorization': 'Bearer ' + TOKEN})
zone_id = json.loads(urllib.request.urlopen(req).read())['result'][0]['id']

body = json.dumps({
  'type': 'TXT',
  'name': f'_dnslink.{subdomain}',
  'content': f'dnslink=/ipfs/{cid}',
  'ttl': 3600,
  'comment': f'DNSLink for {label}'
})
req = urllib.request.Request(f'{BASE}/zones/{zone_id}/dns_records', data=body.encode(), headers=HEADERS)
urllib.request.urlopen(req)
```

**Verification (MANDATORY, Anti-Phantom Gate):**
```bash
nslookup -type=TXT _dnslink.<subdomain>.qnfo.org
# Must show: dnslink=/ipfs/<cid>
```
Gateway resolution (`https://dweb.link/ipns/<subdomain>.qnfo.org` or
`https://cloudflare-ipfs.com/ipns/<subdomain>.qnfo.org`) may take longer to
propagate than the DNS record itself -- `nslookup` returning the correct
TXT record is sufficient DNSLink verification; do NOT block publication
completion on gateway HTTP fetch succeeding within the same session, but DO
note `[GATEWAY-PROPAGATION-PENDING]` if it hasn't resolved yet rather than
silently omitting the check.

**What this deliberately does NOT do:** it does not "pin" content to a
distributed IPFS network in the traditional sense (no Filecoin deal, no
third-party pinning service holding a copy). R2 is the actual durable
store; the CID + DNSLink give it IPFS-compatible addressing and discovery.
This is an intentional simplification per product direction (2026-07-21) —
do not add a third-party pinning step back in without an explicit new
instruction to do so.

### Internet Archive (MANDATORY)

```
GET https://web.archive.org/save/https://papers.qnfo.org/papers/<slug>
```

### Publication URL Verification
```bash
curl -sI https://papers.qnfo.org/papers/<slug>/ # Must return HTTP 200
```

## Phase 8: Core Distribution Stack (MANDATORY)

### Trigger
Every publication MUST complete Phase 8 before publication status is set to "published."

### Core Distribution Stack (v2.8)

All distribution dimensions are satisfied by the core QNFO infrastructure:

| Layer | Implementation | Verification |
|:------|:--------------|:-------------|
| **GitHub** | Public repo with tags, releases, version history | `git tag -l`, `gh release view` |
| **Zenodo** | DOI with versioned deposits (concept DOI + version DOIs) | `curl -sI https://doi.org/<doi>` |
| **R2** | Canonical file archive (md, pdf, provenance bundle) | `npx wrangler r2 object get qnfo-releases/releases/<YYYY>/<MM>/<slug>/paper.md --remote --pipe` |
| **D1/KG** | Living-paper DB entry + Knowledge Graph node | `get_paper_context({slug})`, `query_graph({endpoint:"nodes"})` |

### Pipeline
```
Publication Ready (Phase 5 PDF + Phase 6 D1/R2)
  |
  |-- GitHub: git add, git commit, git push --tags (public repo)
  |-- Zenodo: create new version deposit, upload PDF+md+bundle, publish
  |-- R2:   npx wrangler r2 object put qnfo-releases/releases/<YYYY>/<MM>/<slug>/ --remote
  |-- D1/KG:  INSERT/UPDATE living-paper + sync Knowledge Graph
  |-- DNSLink (OPTIONAL): _dnslink.<slug>.qnfo.org -> /ipfs/<CID>
  |-- Internet Archive: submit papers.qnfo.org URL
```

### DNSLink (OPTIONAL -- convenience layer)
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"  -d '{"type":"TXT","name":"_dnslink.{subdomain}","content":"dnslink=/ipfs/{CID}","ttl":1}'
```

### Deployment Workflow
1. Confirm content exists (body_md in D1 or <slug>.md in R2)
2. Run Phase 5 (Publication: PDF, Zenodo DOI) + Phase 6 (Deploy: D1/R2)
3. Push to GitHub with version tag, create GitHub Release with DOI link
4. Upload all artifacts to R2 (canonical durable host)
5. Seed/update D1 living-paper and Knowledge Graph records
6. (OPTIONAL) Create DNSLink TXT record if an IPFS CID is available
7. Submit Internet Archive snapshot
8. **MCP-DRIVEN VERIFICATION (v2.25 — HARD GATE):** Run the cross-MCP chain from Phase 6 §MCP-Driven Deployment Verification:
  - `cloudflare-builds` → deploy confirmation
  - `cloudflare-observability` → Worker metrics, error rates
  - `cloudflare-bindings` → binding integrity
  - `cloudflare-auditlogs` → deploy action recorded
  - `dns-analytics` → DNS query volumes (if custom domain)
  - `dex-analysis` → end-user latency verification
9. Verify: papers.qnfo.org returns HTTP 200, DOI resolves, R2 content round-trips

## Verification Gates

| Gate | Check | Evidence |
|:-----|:------|:---------|
| **Due Diligence** | KG + D1 + 2+ external sources queried | Query output with counts |
| **Classification** | All papers classified as core/supporting/background/reject | Classification table |
| **Citation** | All citations trace to real papers, BibTeX verified | `_citation_audit.py` output (reusable inline pattern from Phase 3 — write to file, execute, then delete) |
| **Publication Language** | Zero internal language in <slug>.md | Scan output: 0 hits |
| **PDF** | PDF renders without Unicode errors | `build-paper.py` exit code 0 |
| **DOI** | Zenodo record resolves, cross-references correct, preview file is `<slug>.pdf` | `curl -sI https://doi.org/...` + `GET /deposit/depositions/{id}/files` check `files[0]` |
| **Deployment** | papers-server URL HTTP 200, D1 entry exists with slug/doi | curl output + wrangler D1 query |
| **MCP-Driven Deployment (v2.25)** | Cross-MCP verification chain: builds + observability + bindings + auditlogs + dns-analytics + dex-analysis all confirm deployment | MCP tool results with timestamps |
| **SEO** | robots.txt, sitemap, llms.txt, meta tags all present | Verify each URL |
| **Social** | Buffer posts confirmed in queue | `status: SCHEDULED` in response |
| **DNSLink (OPTIONAL)** | TXT record resolves, dweb.link gateway serves content | `nslookup -type=TXT` + `curl dweb.link/ipns/...` |
| **Core Distribution Gate (MANDATORY)** | All core layers: GitHub (public repo), Zenodo (DOI), R2 (archive), D1/KG (discoverability) | All 4 layers verified |
| **Cross-Domain Consilience (SOFT)** | For qualifying cross-domain research: `artifacts/consilience-gate.md` exists with Core Dynamic, 6-domain Lexicon, all Domain Translations, and Synthesis Consilience | File present OR `[CROSS-DOMAIN-NOT-APPLICABLE]` justification documented |
| **Practical Applications Extension (SOFT)** | For all research: `artifacts/practical-applications-extension.md` exists with domain mapping, operational signatures, domain-specific falsifiable claims, and additional calibration register entries | File present with populated domain mapping table |
| **Counterfactual Backcasting (SOFT)** | For all research: `artifacts/counterfactual-backcasting.md` exists with target discipline assessment, tiered fork classification, counterfactual technology stack table, and backcast calibration register entries | File present with populated fork tier table |

## Anti-Patterns
| Anti-Pattern | Fix |
|:-------------|:----|
| Searching only one source | Query all 8 sources in parallel (OpenAlex, Zenodo records, Crossref, Europe PMC, arXiv, web, Vectorize, KG) |
| Skipping dedup | Run dedup, report counts before analysis |
| Inventing citations | All citations must trace to real papers with DOIs |
| Presenting post-hoc as prediction | Use "consistent with" not "predicted by" |
| Pages-per-paper deployment | Use D1 + papers-server Worker (single Worker serves all papers) |
| No falsifiability conditions | Every speculative claim: "This would be disconfirmed if..." |
| Zenodo without retry | Retry 3x with exponential backoff; recover existing drafts |
| Missing cross-references in Zenodo | related_identifiers for prior versions + cited papers + GitHub |
| HTML PDF fallback | Pandoc+XeLaTeX ONLY for publication-grade PDFs |
| Buffer GraphQL with $var format | Use INLINE parameters -- Buffer silently drops $variables |
| Single-store publishing | Core stack REQUIRED: GitHub+Zenodo+R2+D1/KG. DNSLink optional. |
| No DNSLink for publications | Every paper must have `_dnslink.{slug}.qnfo.org` TXT record |
| Publishing without D1/KG records | Log `doi`, `r2_path` in D1 living-paper + Knowledge Graph Paper node |
| Skipping 4-D verification | All 4 core distribution layers (GitHub, Zenodo, R2, D1/KG) must be independently verified before status → "published" |
| Using ANY third-party IPFS pinning service (Filebase/Pinata/Lighthouse/w3up/web3.storage) | DEPRECATED as of v2.10 -- use ONLY Cloudflare R2 (durable store) + locally-computed CIDv1 + Cloudflare DNS DNSLink (naming). No third-party pinner. |
| Hardcoding a live secret VALUE (token/key) inside a skill file | Store only the FILE PATH where the secret lives (e.g. `%USERPROFILE%\buffer\token`); read it live every time. A hardcoded value in a skill file will silently go stale and cause a debugging session exactly like the 2026-07-21 Buffer incident. |
| Guessing/hardcoding a Cloudflare account ID or D1 database UUID | Always run `npx wrangler whoami` (account ID) and `npx wrangler d1 list` (database UUIDs) fresh — a wrong ID produces a misleading 401/404 indistinguishable from a real permission problem. |
| `wrangler d1 execute <name> --remote` on a DB with no local wrangler.toml binding | Use the Cloudflare REST API directly with the UUID from `wrangler d1 list` instead of the CLI. |
| `ON CONFLICT` upsert against a D1 table with FTS5 shadow tables | Use CHECK-THEN-WRITE (SELECT existence, then plain INSERT or plain UPDATE) instead of a combined upsert. |
| Treating a Buffer GraphQL 404 on an unsupported query (e.g. bulk `drafts`) as a dead token | Verify via the `createPost` mutation instead — a `404 endpoint not found` on a DIFFERENT query is a schema-shape issue, not an auth issue. |
| Skipping Phase 0 for a net-new long-lived project | HARD GATE -- scaffold repo, WBS, PROJECT-PLAN.md before Phase 1 |
| No pre-flight checklist before due diligence | Run P1-P11 before Phase 1 begins |
| No phase closeout (commit/tag/push/verify/log) | 5-step Phase Closeout Protocol at every phase end |
| No risk register at project init | ≥5 risks logged at Phase 0 using the risk register template |
| No deliverable registry | All deliverables tracked with paths and archival targets from Phase 0 |
| Creating a research phase tag/release inside `qnfo-skills` | `git remote -v` REPO-TARGET GATE before every tag/commit/release (ADR-026 Incident 3) |
| Assuming a "clean branch" audit is sufficient | Tags and GitHub Releases are independent refs -- audit `git tag -l` and `gh release list` separately, they survive a branch force-push |
| Project files existing ONLY on local disk across a turn boundary | R2-Immediate-Write mandate (ADR-028) -- upload every project artifact to R2 in the SAME turn it's created/edited, never deferred to closeout |
| Creating a disconnected new Zenodo deposit for each phase | Use Zenodo's `actions/newversion` API to keep phase snapshots under one concept DOI (ADR-028) |
| Constructing the Zenodo file-upload URL manually (e.g. `/api/files/{deposit_id}` or `/api/deposit/depositions/{id}/files/{file}`) instead of extracting `links.bucket` from the deposit record | **HARD (v2.43):** The upload endpoint is the deposit's bucket URL — `GET /api/deposit/depositions/{id}` → `links.bucket` (a UUID path like `https://zenodo.org/api/files/{uuid}`). The deposit ID is NOT the bucket UUID; manual construction returns HTTP 500 on upload. Root cause of the ODR v1.5 upload block (2026-08-02): the SKILL.md previously documented the wrong `PUT /api/deposit/depositions/{id}/files/{file}` path, leading agents to construct URLs that Zenodo's storage backend rejects. Follow `scripts/zenodo-create-upload.py` (`upload_file` uses `f'{bucket_url}/{name}'` with the bucket URL from `create_deposit`), never an ad-hoc constructed path. |
| Social-promoting every internal WBS phase transition | Reserve Buffer/social posts for FINAL public deliverables only, not interim phase closeouts |
| OSF registration for minor/exploratory projects | GATE-CONDITIONAL: OSF ONLY for major research with significant predictions and falsifiable claims. Skip for single papers, exploratory studies, or minor updates. |
| Waiting until after publication to create OSF project | Create OSF project during Phase 2 (experimental design) or Phase 4 (deep research) — not after. The registrations timestamp the pre-data-collection hypotheses. |
| Attempting OSF file upload via API | Waterbutler requires cookie sessions — Bearer tokens cannot upload. Use external links to Zenodo DOI + GitHub tree + IPFS instead. (Registration/form completion has NO such limitation — that is 100% API-automatable; only file uploads need Waterbutler.) |
| Claiming OSF registration form completion "requires browser interaction" | FALSE — corrected 2026-07-20. Discover real schema keys via `/schema_blocks/` (format `344-N`, not `q1`/`q2`), populate via PATCH, set subject taxonomy chain, submit via POST — all API, HTTP 201 confirmed live (registration `kj6ar`). |
| OSF tokens in only one location | Store OSF tokens redundantly: %USERPROFILE%\\.osf_token, OSF_TOKEN env var, keys.json, Windows Credential Manager, GitHub secrets. Follow the pattern used by Cloudflare/Zenodo/Buffer tokens. |
| OSF nodes set to private | ALL OSF nodes MUST be public by default. Verify with `GET /v2/nodes/{id}/` → `attributes.public === true`. |
| Not documenting OSF ID mappings | Maintain a mapping of project/component/draft IDs in PROJECT-PLAN.md. These IDs are needed for API updates and cross-referencing. |
| OSF descriptions without external links | Every node description MUST contain links to the canonical file locations (Zenodo DOI, GitHub tree, IPFS). OSF is the discovery hub, not the file host. |
| Creating OSF project without Zenodo DOI backlink | Every OSF project description MUST include the Zenodo DOI. This is the primary discoverability bridge between platforms.
| Submitting OSF registration with empty registration_responses | **HARD GATE:** Empty registration_responses is a STUB. NEVER submit. All ~30 template fields must be populated. |
| Submitting OSF registration without explicit user approval | Use deepchat_question to present the full registration content before submission. OSF registrations are permanent and immutable. |
| Creating OSF registrations then never closing them out | Every submitted registration must eventually be completed or withdrawn. Abandoned registrations are visible on the account and undermine credibility. Run periodic closeout audits. |
| Creating OSF registrations for non-executable research | LLM-Executable Research Gate: no human subjects, no external resources, no IRB. If the protocol cannot be executed in this chat thread, link to Zenodo/GitHub only. |
| Leaving draft registrations with partial registration_responses | If the research will not be completed and submitted, DELETE the draft. Partial stubs are a reputational risk. |
| Not storing OSF registration tracking in D1/KG | Store registration_id, doi, status, and dates in D1 + KG for lifecycle tracking and closeout audit. |
| `python -c "..."` inline scripts on Windows (kaizen fix B1) | Nested double-quotes in f-strings collide with `python -c "..."` outer quotes; Windows escaping of `\n`, dict literals, and Unicode breaks silently. `write` the script to a `_*.py` file first, `exec` it, then delete -- never inline for anything beyond a one-liner with zero quotes/dicts/regex. |
| `curl` on Windows PowerShell (kaizen fix B3) | PowerShell aliases `curl` to `Invoke-WebRequest`, which has different flags (`-s` is not recognized) and fails. Use `curl.exe` explicitly (the real binary, bypassing the alias). Never pipe to inline `python -c` — write Python to file first per KIF-37 §8.11. |
| Unicode math left unconverted for XeLaTeX (kaizen fix A1 — SUPERSEDED by KIF-27) | Run `scripts/build-paper.py` before every Pandoc+XeLaTeX build -- see PDF Building section above (v2.21+). |
| `keywords:` YAML field in Pandoc frontmatter (kaizen fix A2 — SUPERSEDED by KIF-27) | Strip it -- `scripts/build-paper.py` does this automatically (preprocess stage). It crashes some XeLaTeX templates via an undefined `\xmpquote` macro. |
| Ephemeral scripts with hardcoded API tokens reaching `git add` (kaizen fix A4) | Run `scripts/credential-scan.py --staged` before every commit (Phase Closeout Protocol STEP 0.5). Add `_*.py`/`.env`/`*.token` to `.gitignore` from Phase 0. |
| Obsidian/external-drive source notes assumed inaccessible or silently skipped (kaizen fix C5/D5) | Document the path limitation and ask the user to copy files in, or use `exec` with explicit `cwd` in Full Access mode. If imported notes mix internal monologue with delivered content and lack YAML frontmatter, load `doc-coauthoring` to help the user separate meta-planning from publishable content before it enters the research pipeline. |
| Guessing Zenodo `metadata.resource_type` shape from memory each session (silently fails to persist as a string, rejected as an object on newversion drafts) | Run `scripts/zenodo-resource-type-fix.py --deposit-id <id>` — tries known-working variants in order with re-GET verification. See `references/zenodo-deposit-schema.json` and `qnfo-agent` KIF-20. |
| Reconstructing Buffer GraphQL mutation shape from scattered prose each session | Consult `references/buffer-graphql-schema.json` for the single canonical schema (endpoint, auth, channel discovery, createPost input fields, union response handling). |
| Using the legacy `svjour3`/`svjour.cls` package for new LaTeX papers | Retired -- use `sn-jnl.cls` (Springer Nature's unified template, embedded at `templates/springer-nature-latex/`) as the mandatory default. |
| Placing a `.bst` bibliography style file in a `bst/` subdirectory relative to `paper.tex` | `bibtex` does not search subdirectories by default -- copy the needed `.bst` alongside `paper.tex`/`refs.bib` before running `bibtex`. |
| Declaring a paper "publication-ready" after only the Physics Writing Standards / Publication Language Gate pass | Also run the Professional Publication Standards structural, tone/prose, and copyediting checklists -- content-integrity and presentation-quality are separate gates, both mandatory. |
| PowerShell default encoding is NOT UTF-8 (system codepage silently corrupts Unicode) | Set [Console]::OutputEncoding AND $OutputEncoding to UTF-8 before any file/pipe operation (KIF-27, qnfo-agent SS8.7) |
| Python open() without encoding='utf-8' on Windows | Always specify encoding='utf-8' explicitly -- bare open() uses cp1252 default and SILENTLY produces wrong characters (KIF-27) |
| Source markdown files with BOM (U+FEFF) | Strip BOM before any commit; BOM breaks Pandoc frontmatter and YAML parsing (KIF-28) |
| U+FFFD/U+FFFF characters in source markdown | Run FFFD scanner pre-commit; these are ALWAYS corruption signals, never intentional (KIF-26, KIF-28) -- see Source File Encoding Integrity gate |
| Python script missing # -*- coding: utf-8 -*- declaration | Every .py file MUST declare encoding on line 1 or 2; Python reads files as ASCII by default on some platforms (KIF-28) |
| Get-Content/Out-File without -Encoding UTF8 on PowerShell | Default to system codepage; use -Encoding UTF8 or read via Python with explicit encoding='utf-8' (KIF-28) |
| Skipping FFFD/BOM scan before git commit or publication | Run pre-commit encoding scan per Source File Encoding Integrity gate; encoding corruption survives all downstream pipeline stages (KIF-28) |
| Submitting/publishing a paper with an incomplete Declarations section (missing any of the 9 mandatory subsections) | Springer Nature treats incomplete Declarations as an incomplete submission -- write "Not applicable" explicitly rather than omitting a subsection. |
| Research scoped entirely within one domain's lexicon, no cross-domain translation check exists | Cross-Domain Consilience Gate (KIF-29, SOFT) at Phase 1 for qualifying research — produce `artifacts/consilience-gate.md` with 6-domain structural translation |
| Cross-domain analogies made ad hoc, not structurally verified | Use the structured template: Core Dynamic → Cross-Domain Lexicon → Domain Translations (Lexicon/Instance/Ramification for each) → Synthesis Consilience |
| Literature search uses only source-domain terms on cross-domain projects | Translate Lexicon terms into parallel search queries for each target domain (e.g., physics "phase transition" → biology "phase transition in gene regulation", sociology "tipping points") |
| No structural bridge between domains in the final paper | Publish the Cross-Domain Lexicon table + Synthesis Consilience paragraph as a dedicated section of the research output |
| Consilience claimed without a unification principle | Synthesis Consilience MUST contain one invariant mechanism + one frontier question — otherwise flag `[CONSILIENCE-UNVERIFIED: no unifying meta-principle derived]` |
| Forcing strained analogies on genuinely single-domain research | Mark `[CROSS-DOMAIN-NOT-APPLICABLE: no non-trivial structural isomorphisms found]` — absence of consilience is a valid result, not a failure |
| Naming the methodology in research outputs (e.g., "per Stage 4 sensitivity analysis," citing protocol names or KIF tags in prose, "We applied a Structured Forecast Protocol") | Bury the method — write the ANALYSIS, not the process description. "Underlying this candidate are three critical assumptions" not "Stage 2 Assumption Audit found." The artifact file documents the full method for any reader who wants the details. |
| Assigning precise numeric likelihoods (0.90, 0.75, 0.20) to forecast assumptions with ZERO empirical anchoring | Execute Stage -1 Likelihood Calibration Protocol (KIF-31) BEFORE Stage 2 — every P > 0.80 MUST have an empirical pillar (base rate, reference class, calibrated confidence, or known prior). Unanchored likelihoods > 0.80 are capped at 0.80 with [CALIBRATION-CAP] tag. |
| Running ±20% sensitivity analysis on anchorless likelihoods, then presenting this as "validated" | Use Judgment Sensitivity Analysis (Stage 4, v2.27) — tests qualitative ranking under perturbation (pessimistic/optimistic/halved-priors/dependency-correlation) and produces a ROBUST/CONDITIONAL/FRAGILE statement. Do NOT compute numerical EVs. |
| Outputting Stage 5 Calibration Register entries with [CHECK: 2030] tags but no indication of how strong the underlying likelihood evidence is | Every register entry MUST tag its likelihood-anchor provenance: [STRONG] (base rate / reference class / known prior) or [WEAK] (calibrated subjective / [CALIBRATION-CAP]). This makes the epistemic basis visible to future readers. |
| Single-agent subjective confidence treated as objective probability, with no structured review | REVIEWER subagent (same model — consistency check, not independent verification) independently assigns every likelihood — if divergence > 0.15, use the MORE CONSERVATIVE value and flag the disagreement in `artifacts/likelihood-calibration.md`. Do NOT claim this is "inter-rater reliability" — it is a structured second-opinion check from the same underlying model. |
| Running calibration training with no Brier-score awareness | Before executing the protocol, complete a ≥20-question confidence-interval quiz. If Brier > 0.15, adjust all > 0.80 likelihoods downward by factor (1.0 − overconfidence_error). |
| Presenting rankings without showing the shift from raw (uncalibrated) to calibrated judgments | Mandatory side-by-side disclosure in Stage 4 output: Raw judgment ranking vs calibrated judgment ranking. A candidate that drops from #1 to #4 after calibration is the most important finding of the analysis. |
| Editing source files in a temp git clone across multiple turns without committing each turn (KIF-32, v2.26) | **HARD GATE (cross-ref git-github v2.3):** clone → edit ALL files in one batch → commit → push → delete, ALL in one turn. Phase 5 PDF build/edit cycles are especially dangerous: the agent often edits → builds → discovers more issues → edits again across turns on the same clone. Deferring commit to a "final batch" guarantees data loss when the temp directory is cleaned between turns. Re-clone each turn from the remote to get the latest state. |
| Assuming a temp clone's files survive across tool-call turns on Windows (v2.26) | `$env:TEMP` is volatile. System cleanup, session teardown, or storage-sense can evict files between turns. Never trust `Test-Path` results from a prior turn. |
| Batched "final commit" of edits accumulated across multiple turns on a temp clone (v2.26) | Commit each turn's edits as an atomic unit with `git push`. A "final commit at the end" that was deferred for 3+ turns will find the repo directory empty and all edits lost. |
| Skipping Stage 9 (Practical Applications) because "the forecast is too theoretical" | Stage 9 is MANDATORY for ALL projects. Even theoretical forecasts have practical applications — if not in technology, then in education, methodology, or cross-domain consilience. Flag `[PURELY THEORETICAL]` if genuinely no domain exists, but this should be rare. |
| Listing application domains without operational signatures (e.g., "this applies to quantum computing") | Every Stage 9 domain entry MUST articulate the specific change in practice — the operational signature. "Applies to X" is not an application; "changes how X is done by enabling Y" is. |
| Backcasting only one discipline or one fork tier | Stage 10 is most informative with cross-discipline interactions. A single-discipline backcast misses the primary insight: "if A advanced but B didn't, X exists but Y doesn't." |
| Using placeholder discipline names (Stratigraphy, Metrology, etc.) instead of the research's actual core disciplines | Stage 10's template uses generic placeholders. The agent MUST replace them with the actual core disciplines identified in Phase 1 due diligence. |
| Treating "OK" tool output as "confirmed no results" without investigating (KIF-56) | Tool responses returning `"OK"` with no visible content (search_papers_enriched, query_graph, search_papers) MUST be investigated — check for offloaded files, re-run with different parameters, or flag as `[NOT-VERIFIED: tool output unreadable]`. Never treat as a finding. "OK" means "output status unknown," not "no results." |
| Filling missing tool output with general knowledge dressed as search findings (KIF-56) | When search tools fail to return readable data (429 rate limit, 0-byte responses, offloaded output), the ONLY acceptable response is `[NOT-VERIFIED: <reason>]`. Never substitute general knowledge for search results. Specific paper names, years, and counts MUST NOT be asserted without a readable tool output file. |
| **Fabricating research priorities from qualitative frameworks (E2 incident, v2.39)** | A named statistical test ("Cramér-von Mises") does not validate missing input data. E2 was listed as a #2 priority with specific data ("8 rung energy scales") that does not exist in any artifact — the measurement stratigraphy paper defines 7 mathematical eras without energy scales. The test name lent false authority to a fabricated priority. Same failure class as the Fabrication Incident (RESEARCH-CONTINUITY-REGISTRY.md §9). Gate: verify input data exists before listing a named experiment as a priority. |
| **Adopting a paper's terminology (e.g., "Pythagorean semigroup") without checking standard math definitions** | BP-2: "Pythagorean semigroup" for {2^a·3^b·5^c} = misnomer — correct term is 5-smooth (Hamming/regular) numbers. The name alludes to the 3-4-5 triple (primes {2,3,5}) but brands a density property with false number-theoretic prestige. Every field-specific term must pass the Terminology Audit Gate. |
| **Hand-rolling Zenodo urllib upload calls when canonical scripts exist** | Use `scripts/zenodo-create-upload.py` + `scripts/zenodo-metadata-publish.py` for ALL Zenodo operations. urllib `PUT` without Content-Type → HTTP 415 (4× this session). |
| **Publishing approximating-numerology claims without a pre-registered density gate** | BP-3: If "X approximates Y to within Z%" and the approximating set is dense in ℝ⁺, a Monte Carlo null model with pre-registered tolerance is REQUIRED before publication. p>0.05 → report [CONSISTENT WITH LOOK-ELSEWHERE ARTIFACT]. v3.2 mass-ratio claim required expensive post-publication ACRP-04 audit. |
| Committing/tagging research artifacts without re-reading tool outputs that support each claim (KIF-57) | Pre-commit verification gate: re-read every tool output file cited in an artifact BEFORE git commit. A claim that cites `arxiv3.xml` but that file was never re-read in the same turn is an Anti-Phantom violation. Phase closeout MUST include independent re-verification of every cited finding.
| Writing research artifact claims without citing a specific, readable tool output file (KIF-55) | Every factual claim in a research artifact MUST cite a specific, readable tool output file or source. "arxiv3.xml:24000" or "OpenAlex API response: HTTP 200 count=5" — never a bare assertion without provenance. |
| Semantic Scholar as the PRIMARY academic search source (HTTP 429 under sustained load without a key — session-verified 2026-07-31, 4 queries lost) | Use OpenAlex as PRIMARY (keyless, verified HTTP 200 back-to-back); Crossref/Zenodo/EuropePMC as mandatory supplements. If Semantic Scholar 429s twice, substitute and flag `[RATE-LIMIT-OVERRIDE]`. |
| External literature search that queries arXiv/web but NEVER searches Zenodo records for OTHER users' deposits | Zenodo is a discovery source, not just an upload target — always run `zenodo.org/api/records?q=<topic>&size=10` in Phase 2. Verified: exact term "JPCUB" → 0 third-party deposits (only the author's own 2), a 5-source novelty confirmation (arXiv + OpenAlex + Crossref + Europe PMC + Zenodo). |
| Declaring novelty from fuzzy/tokenized search results alone | Always run an exact-phrase check before claiming novelty: Zenodo `q="TERM"` (quoted) or OpenAlex `filter=title.search:TERM`. Unquoted Zenodo q= OR-tokenizes — "JPCUB joules per computational unit" returned total=311,162 vs quoted `"JPCUB"` returning total=2. Fuzzy totals are meaningless for novelty claims (v2.36). |
| Subagent output truncation treated as audit completion | When a research subagent reads the input files but its output is truncated before it produces findings, the parent agent MUST fall back to direct audit. The subagent reading a file is NOT evidence that it completed the audit. See kaizen skill §Subagent Failure Handling. |
| **Using generic `paper.md`/`paper.pdf` filenames instead of slug-based naming** | Paper files MUST use the project slug: `<slug>.md` and `<slug>.pdf`. For `computing-machines`, this is `computing-machines.md` and `computing-machines.pdf`. Generic names cause confusion when multiple paper repos share a temp directory, and make it impossible to identify a paper from its filename alone. Update `build-paper.py` calls, R2 paths, Zenodo uploads, and provenance bundles accordingly. |
| **Assuming a temp-directory name identifies the project** | NEVER assume a temp directory name maps to the correct project. ALWAYS read `<slug>.md` YAML frontmatter (`title:` + `doi:`) before using file contents for upload or cross-population. A directory named `computing-machines` may contain a completely different paper (KIF-58 cross-contamination incident, 2026-07-31). |
| **Cross-populating files between Zenodo and GitHub without verifying paper identity** | Before pushing files to ANY GitHub repo in the context of a Zenodo upload, verify the repo's existing `paper.md` YAML `title:` matches the paper being uploaded to Zenodo. A paper title mismatch means you've found the wrong repo — even if the repo name seems related (KIF-58). |
| **Publishing an audit paper with an unreproducible headline number (v2.42)** | BP-9: Before publishing any audit, run BP-1 through BP-7 on the audit itself. ACRP-04's most prominent numerical claim (9,138σ) does not reproduce under any combination of its own cited uncertainties or PDG 2024 Live (best: 8,943σ). An audit that finds arithmetic errors cannot carry its own. |
| **Two conflicting uncertainty values for the same quantity in the same paper (v2.42)** | BP-7 Single-Source Rule: If m_μ/m_e appears as "±0.00001" in §3.5 prose and "206.76828(5)" in §4 table notation, the paper carries a self-contradiction. Resolve before publication. |
| **Claiming N fitted ratios from M < N independent quantities without checking internal closure (v2.42)** | BP-5: 3 lepton ratios from 2 independent DoF produces 0.050% closure error. Report the error; if it exceeds the claimed tolerance, the fits are not a consistent parameter set. |
| **Reporting a derived quantity without recomputing from first principles (v2.42)** | BP-6: Koide Q "0.02%" claimed from 5-smooth fits; actual recomputation: 0.00289% — factor of ~7× error. A 30-second recomputation catches this. |
| **Cross-paper numerical inconsistency for the same Monte Carlo result (v2.42)** | BP-4: ACRP-04 reports P(all-9-fit)=99.8%; Adelic v4.0 reports 99.85%. Both reference seed 20260731. Shared null-model results MUST match across all papers that cite them. |
| **Density gate applied to one numerology claim but not a structurally identical one (v2.42)** | BP-8: §7.2 mass ratios (Class 1: Dense-Approximant) were tested by ACRP-04. §6 adelic factorization 976/919 (Class 2: Ratio-Factorization) has NOT been tested. Selective gate application = confirmation bias. |
| **Reporting sigma deviations without citing the specific uncertainty source and propagation method (v2.42)** | BP-7: Every σ must state: PDG edition, specific table, exact value ± uncertainty, and propagation formula (Δ/σ). "9,138σ" sources to nothing traceable. |
| **Treating independent recomputation as optional for paper claims cited in new research (v2.42)** | BP-10: "Cited in a paper" ≠ "independently verified." Before treating a p-value/σ/fit as established, recompute it with a different seed. The cost (~30s for 50k MC trials) is negligible vs. cost of propagating wrong numbers. |
| **Post-hoc tolerance selection presented as a pre-registered prediction (v2.42)** | BP-3: The "within 0.29%" threshold was the maximum observed deviation AFTER fitting — it was not pre-registered. This is an additional look-elsewhere degree of freedom. Pre-register tolerances before computation. |
| **Publishing a Zenodo deposit without verifying file contents match the intended paper** | After uploading files but BEFORE `actions/publish`, download the uploaded `paper.md` from the deposit and verify its YAML `title:` matches the target Zenodo concept. Zenodo bucket lock means wrong files are PERMANENTLY tainted in that version DOI (KIF-58). |
| **Uploading files to Zenodo in arbitrary order without designating a preview file** | Upload `<slug>.pdf` FIRST — Zenodo uses the first file as the landing-page preview/thumbnail. Priority: PDF > README.md > `<slug>.md` > bundle > remaining artifacts. Verify via `GET /deposit/depositions/{id}/files` that `files[0].filename` is the PDF (GATE P5.PREVIEW, v2.41). |
| **Cross-project paper confusion from handoff ambiguity** | When a session handoff mentions a paper and a DOI but does NOT specify the GitHub repo, query all QNFO repos, find the paper by title, and verify the repo before any cross-population. A handoff that references "paper.md" and a Zenodo DOI is ambiguous — the paper could live in any of multiple QNFO repos (KIF-58). |
| **Treating a Zenodo record ID as proof of paper identity (2026-08-02)** | Zenodo record IDs are GLOBAL (shared across all users and deposits). A record ID that was 404 yesterday can be claimed by an unrelated third-party deposit tomorrow (21748026: 404 during ACRP-07 phantom-check, later occupied by an unrelated Chinese-language book archive). NEVER verify "the DOI exists" — verify TITLE + CREATOR match. Existence at an ID is not identity. |
| **Calling `actions/newversion` twice because a draft already exists (2026-08-02)** | HTTP 400 `files.enabled: Please remove all files first` = a newversion draft already exists for this deposit. Follow `links.latest_draft` and complete that draft instead of creating a parallel one (ODR incident: deposit 21751722, draft 21752136). |
| **Publishing to Zenodo without checking for in-flight unsubmitted drafts (2026-08-02)** | Before ANY publish/newversion, run the unsubmitted-draft pre-check (`GET /api/deposit/depositions?q=<title>` and filter `state=="unsubmitted"`). A recently-modified unsubmitted draft is a CONCURRENT SESSION's in-flight work — do not collide with it; coordinate. A stale one (older than a session) can be completed or discarded. |
| **Syncing D1 `body_md` from a stale local copy after a Zenodo publish (2026-08-02)** | After publishing a corrected newversion, sync D1 `body_md` from the ACTUAL PUBLISHED FILE (re-download from the new record), not the local pre-edit copy. Cross-Domain incident: D1 body was 47,134 chars with the old wrong mass-ratio table while the published v4.0 file was 49,515 chars corrected — the D1 record silently diverged. Verify `LENGTH(body_md)` ≈ published file size. |
| **Assuming `actions/newversion` creates a clean draft — old files from prior versions persist and can become the wrong preview file (GATE P5.CLEAN, 2026-08-02)** | **HARD (v2.45):** `actions/newversion` copies ALL files from the source deposit. If those files are not deleted before uploading new ones, they remain in the draft and can appear BEFORE the new PDF in the file list — making an old 798-byte `PROVENANCE-BUNDLE.zip` or a new `ERRATA.md` the preview instead of the 80KB PDF. After newversion, enumerate all files via `GET /deposit/depositions/{id}/files`, DELETE every one, THEN upload fresh files in preview-first order (PDF first). |
| **D1 living-paper slug drifted after terminology correction — Zenodo filename ≠ D1 slug (2026-08-02)** | After BP-2 terminology corrections that rename paper files (e.g., `pythagorean-semigroup-audit` → `acrp04-five-smooth-audit`), verify the D1 `papers` table slug still matches the Zenodo filename. Use `SELECT slug, title FROM papers WHERE title LIKE '%<keyword>%'` to find the right row if slugs diverge. In this session, the D1 slug was `acrp04-five-smooth-audit` but the old `pythagorean-semigroup-audit` search returned zero results. |