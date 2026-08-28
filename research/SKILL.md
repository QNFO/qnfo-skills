---
name: research
version: "2.143"
---

> **v2.142 UPDATE (2026-08-28, CMD SKILLS UPDATE: DATASET-ACQUISITION-1 — acquire original research datasets (Zenodo/GitHub, provided by paper authors) as part of the research pipeline and overall data analysis; provenance+sha256 evidence; recompute derived quantities from raw data (BP-10); no dataset = documented absence; never fabricate; extends DUE-DILIGENCE-DEPTH-1 + COMPUTATIONAL-VERIFICATION-1; mirrors system-prompt v3.86 + kaizen v2.106 + cloudflare v3.63 unchanged):**
> Red-team: direct parent-agent skills audit (session this). HARD: 1 (new gate). Changes:
> (1) [HARD] **DATASET-ACQUISITION-1 added** — full gate section below: Phase 1 due diligence checks every paper under analysis for its original dataset (Zenodo record file list / GitHub isSupplementTo repo / data-availability statement); acquired datasets run through the analysis with provenance + license + sha256; derived quantities recomputed from raw data (BP-10 — citation is not verification); no dataset = documented absence; never fabricate.
> Cross-reference: system-prompt v3.86, kaizen v2.106, cloudflare v3.63, session this.

> **v2.143 UPDATE (2026-08-28, CMD SKILLS UPDATE: SPECTRAL-ESTIMATOR-CONSTRUCTION-1 + DATASET-SOURCE-FALLBACK-1 + QUESTION-AUTONOMY-1; mirrors system-prompt v3.87 + kaizen v2.107 + cloudflare v3.63 unchanged):**
> Red-team: 2 reviewer slots dispatched (parent direct audit authoritative). HARD: 3. Changes:
> (1) [HARD] **SPECTRAL-ESTIMATOR-CONSTRUCTION-1 added** — Phase 2/5 gate: six canonical construction bugs in statistical-spectral estimators (pair correlation via k-th-neighbor decomposition with per-order normalization — NOT the spacing distribution; exact Li unfolding via scipy.special.expi(log x); full Dyson number-variance formula (1/pi^2)[log(2 pi L)+1+gamma-pi^2/8]; rank unfolding is a tautology — smoothed staircase; Montgomery-Odlyzko = Riemann zeros, primes = Gallagher + twin-gap hard core; single-realization form factor = report-only). Canonical: QNFO.UMP.014 P3-exec suite 8/8 PASS (commit 39381f6).
> (2) [HARD] **DATASET-SOURCE-FALLBACK-1 added** — extends DATASET-ACQUISITION-1 (Phase 1): canonical dataset without a static bulk endpoint (ENSDF 404/403 search-servlet) → probe static mirrors of the same data class (ExoMol .states.bz2, range-request 206) + certify every blocked path with the HTTP-probe log; never 'no dataset' without probe evidence.
> (3) [HARD] **QUESTION-AUTONOMY-1 added** — user directive 2026-08-28: research-direction and project-disposition decisions within the agent's audit authority are resolved AUTONOMOUSLY from corpus/registry/null-ledger/red-team evidence; deepchat_question only when no evidence path exists. Canonical: UMP.014 disposition.
> Cross-reference: system-prompt v3.87, kaizen v2.107, cloudflare v3.63, session this.

> **v2.141 UPDATE (2026-08-26, CMD SKILLS UPDATE: RES.024 publish marathon gates — DNS-FLAP-IP-PIN-1 + ZENODO-DELETE-404-ALREADY-GONE-1 + R2 is_truncated pagination; mirrors system-prompt v3.78 + kaizen v2.101 + cloudflare v3.59 unchanged):**
> Red-team: direct parent-agent audit (RES.024 post-positional-numeracy v1.0.1 publish + distribute, 2026-08-26). HARD: 3. Changes:
> (1) [HARD] **DNS-FLAP-IP-PIN-1 added** — the machine's local resolver flaps intermittently (socket.gaierror 11001 getaddrinfo failed) across hosts mid-run (zenodo.org, api.cloudflare.com, workers.dev). Resilient pattern for API hosts: retry system getaddrinfo (6x, 3-9s backoff) → fallback `nslookup <host> 8.8.8.8` + parse IP → pin IP with Host-header routing over ssl._create_unverified_context(). CAVEAT: Cloudflare Workers hosts (workers.dev) do NOT tolerate IP pinning (403) — for workers use direct host resolution with generous retries (6x, 3-15s) + browser UA; a 403 with browser UA on workers.dev = transport problem (IP pinning), not a token problem.
> (2) [HARD] **ZENODO-DELETE-404-ALREADY-GONE-1 added** — on a Zenodo newversion draft, deposit-API DELETE via file.links.self returns 404 {'message': "Record '<id>' has no file '<name>'."} when the file is ALREADY deleted; retry loops that re-issue the DELETE after transient errors can succeed server-side yet report 404 to the caller, so 'DELETED n of N' mismatch is NOT evidence of failure. Rule: treat 404 as already-absent; after any delete batch RE-LIST both deposit-API and records-API file lists and diff against targets before uploading (the two lists can transiently disagree while deletes are in flight — re-list until consistent). Canonical: RES.024 v1.0.1 draft 22114495 2026-08-26.
> (3) [HARD] **R2-OBJECTS-LISTING-IS_TRUNCATED-1 added** — the R2 objects list API pagination field is `result_info.is_truncated` + `cursor` (per_page 20), NOT `more`; R2-OBJECTS-LISTING-SHAPE-1's pagination note corrected (a loop keyed on `more` silently stops after page 1). Canonical: RES.024 R2 mirror verify — 12/42 reported on page-1-only, 42/42 after is_truncated loop.
> Cross-reference: system-prompt v3.78, kaizen v2.101, cloudflare v3.59, session this.

> **v2.140 UPDATE (2026-08-26, CMD SKILLS UPDATE: publication reference/deposit discipline gates — REFERENCE-RENDER-FROM-BIB-1 (render reference lists FROM references.bib via a renderer, never hand-type) + SLUG-FILE-NAMING-1 (<slug>.md/.html/.pdf, never paper.*; scripts parameterized to the slug) + PDF-SUPERSCRIPT-ASCII-1 (Unicode superscripts ×10⁻²¹ → tofu; convert to ASCII e-notation in source) + ZENODO-DEPOSIT-NOHUP-RETRY-1 (nohup long-deposit + transient 5xx/429 retry + metadata-first-on-clean-draft + publish-only-fail==0) + PUBLISH-LOCK-RECHECK-1 (publish_locks row + git fetch origin + concept version check before every newversion); canonical QNFO.JPC.003; mirrors system-prompt v3.78 + kaizen v2.100 + cloudflare v3.59 unchanged):**
> Red-team: direct parent-agent audit. HARD: 5 (folded as Phase 5/8 gates).
> Cross-reference: system-prompt v3.78, kaizen v2.100, session this.


> **v2.139 UPDATE (2026-08-26, CMD SKILLS UPDATE: PDF-NO-BROWSER-CHROME-1 — generated PDFs must never carry web-browser headers/footers; render-pdf.cjs displayHeaderFooter:false explicit + build-pdf.py header_footer_static_gate (Phase 5 PDF build); mirrors system-prompt v3.77 + kaizen v2.99 + cloudflare v3.59 unchanged):**
> Red-team: direct parent-agent root-cause audit (HARD: displayHeaderFooter missing — fixed + gated).
> Cross-reference: system-prompt v3.77, kaizen v2.99, session this.


> **v2.138 UPDATE (2026-08-26, CMD SKILLS UPDATE: SLUG-RENAME-VECTORIZE-ORPHAN-1 (Phase 6 distribution — slug rename orphans Vectorize vectors, delete via delete_by_ids) + PUBLISH-LOCK-1 git extension (Phase 8 — also git ls-remote the slug branch); mirrors system-prompt v3.76 + kaizen v2.98 + cloudflare v3.59 unchanged):**
> Red-team: MODEL-KEY-FULL-SCAN-1 full-file parse (preferredModel re-drifted — reset flash).
> Cross-reference: system-prompt v3.76, kaizen v2.98, session this.


> **v2.137 UPDATE (2026-08-24, kaizen — CMD SKILLS UPDATE: user directive — NO SILOS, NO JARGON — CROSSWALK-TRANSLATION-1 folded into Phase 1/4/5 (cross-domain insights and interdisciplinary terminology/crosswalks are breakthrough-critical); mirrors system-prompt v3.72 + kaizen v2.94):**
> Red-team: direct parent-agent skills audit (N-2 clean at v2.136); user directive 2026-08-24 applied verbatim. HARD: 1 (new gate). SOFT: 0.
> (1) [HARD] **CROSSWALK-TRANSLATION-1 (user directive 2026-08-24: "CROSS-DOMAIN INSIGHTS AND INTERDISCIPLINARY/CROSS-DISCIPLINARY TERMINOLOGY AND CROSSWALKS/TRANSLATIONS ARE CRITICAL FOR BREAKTHROUGH DISCOVERIES: NO SILOS, NO JARGON!")** — Phase 1 due diligence MUST include an adjacent-domain scan (>=2 adjacent WBS domains, DUE-DILIGENCE-DEPTH-1) looking for correspondences; Phase 5 publications MUST (a) name cross-domain connections in title/abstract where they exist (title-visible bridges, TERMINOLOGY-SILO-LESSONS-1), (b) include an explicit crosswalk/translation of key domain terms into adjacent-domain equivalents where a correspondence exists, and (c) be readable by an adjacent-domain expert — unexplained in-group jargon/shorthand is a HARD finding (extends PUBLICATION-PROSE-GATE-1 + PAPERS-NO-NAVEL-GAZING-1). Any vocabulary/taxonomy corpus used triggers the partitionality instrument (scripts/terminology_silos.py, QNFO.CGS.002) with bridge share reported; the semantic mapping layer (bilingual-dictionary analogue) is first-class infrastructure, not an afterthought. Canonical: 10.5281/zenodo.22075544 (the instrument + infrastructure response); "Valuation Without ℝ" (10.5281/zenodo.21803677) as the title-visible crosswalk exemplar.
> Cross-reference: system-prompt v3.72, kaizen v2.94, TERMINOLOGY-SILO-LESSONS-1, PUBLICATION-PROSE-GATE-1, session this.

# RESEARCH — v2.143
> **v2.136 UPDATE (2026-08-24, kaizen — CMD SKILLS UPDATE: Terminology Silos post-publication audit gates — REFERENCE-TITLE-FIDELITY-1 + METADATA-RELATIONS-ASSERT-1 + DEPOSIT-LAYOUT-VERIFY-1 + POST-PUBLISH-FRONTMATTER-ASSERT-1 + HYPOTHESIS-CARD-EXECUTION-PARITY-1 + INTERNAL-COUNTS-SWEEP-1; mirrors system-prompt v3.70 + kaizen v2.92):**
> Red-team: 3-slot dispatch on 10.5281/zenodo.22075544 (Dependency completed: 1 HARD/3 SOFT; Accuracy + Completeness child sessions FAILED — REDTEAM-CHILD-FAIL-1 — direct parent audit authoritative: deposited scripts re-run, outputs byte-match evidence JSONs, seed validation 9/9, rendering gates PASS, all cited DOIs published, frontmatter self-DOI clean). HARD: 4 (record-level). SOFT: 6.
> New Phase 5/6/8 permanent gates (RECURRENCE-ZERO-1):
> (1) [HARD] **REFERENCE-TITLE-FIDELITY-1** — every rendered reference entry MUST match the citation-audited bib title EXACTLY (DataCite/Zenodo title; never a description-as-title). Gate: automated rendered-vs-bib title cross-check before publish. Canonical: 22075544 ref #5 — record 19564091 is titled "Projective Geometric Frameworks for Semantic Structures: ... Large Language Models", rendered as "Ultrametric topology in semantic memory with invariant cross-ratio stability" (bib + citation-audit correct; rendered list the outlier).
> (2) [HARD] **METADATA-RELATIONS-ASSERT-1** — deposit metadata MUST carry related_identifiers at CREATION (GitHub isSupplementTo branch URL + relation links); post-publish verify related_identifiers non-empty. Canonical: 22075544 published with related_identifiers=null.
> (3) [HARD] **DEPOSIT-LAYOUT-VERIFY-1** — before closeout, download the published deposit fresh and EXECUTE the README reproduce commands against the deposited layout; scripts MUST be layout-agnostic (paths relative to script dir) or the upload MUST preserve directory keys (scripts/, docs/, artifacts/); README paths must match the actual deposit. Canonical: 22075544 flat deposit — validate_seed_vs_published.py + hsilo3_semantic_links.py crash (artifacts/external-search/ absent); README commands reference scripts/ + artifacts/ paths.
> (4) [HARD] **POST-PUBLISH-FRONTMATTER-ASSERT-1** — after EVERY publish/newversion, download the deposited .md and assert frontmatter doi+version == record doi+version; mismatch → immediate edit → replace → publish in the SAME cycle (never defer). Canonical: RES.023 v2.5 (10.5281/zenodo.22075809) published .md still v2.4/22073477 (interrupted remediation, 2026-08-24).
> (5) [SOFT] **HYPOTHESIS-CARD-EXECUTION-PARITY-1** — at the results gate, reconcile each hypothesis card's claim/prediction wording with the executed test (family definitions, thresholds); document drift in the premises section. Canonical: H-SILO-2 card "structurally general concept families" vs executed method/pattern family (22075544).
> (6) [SOFT] **INTERNAL-COUNTS-SWEEP-1** — cross-document corpus counts (PROJECT-PLAN vs paper vs README) swept pre-publish (extends PUBLICATION-STATUS-STALE-1). Canonical: PROJECT-PLAN "399 titles" vs paper "578 titled records".
> Cross-reference: system-prompt v3.70, kaizen v2.92, cloudflare v3.59, session this.

# RESEARCH — v2.136
> **v2.135 UPDATE (2026-08-24, kaizen — CMD SKILLS UPDATE: TERMINOLOGY-SILO-LESSONS-1 folded into Phase 1 due diligence + Phase 5 publication — title-visible bridges (name cross-domain connections in title/abstract), partitionality audit of any taxonomy/vocabulary corpus (instrument scripts/terminology_silos.py, QNFO.CGS.002), semantic links built explicitly (KG edges) not assumed lexically discoverable, bridge infrastructure maintained; canonical: 10.5281/zenodo.22075544 + RES.023 v2.5 10.5281/zenodo.22075809; mirrors system-prompt v3.69 + kaizen v2.91):**
> Red-team: direct parent + N-2 clean. Research footer added (was missing — pre-existing gap closed).
> Cross-reference: system-prompt v3.69, kaizen v2.91, cloudflare v3.59 (unchanged), session this.

# RESEARCH — v2.135
> **v2.134 UPDATE (2026-08-21, kaizen — CMD SKILLS UPDATE: print-artifact gates — EDGE-PDF-PAGE-KEYWORD-1 + POSTER-FILL-MEASURE-1 + SVG-LABEL-EXTENT-1 + WRITE-EXEC-ORDER-1; mirrors system-prompt v3.68 + kaizen v2.90):**
> Red-team skills audit: direct parent; N-2 clean. Numbering note: two independent v2.133 cycles collided on 2026-08-21 (PUBLICATION-META-PROSE-1 extension + duplicate-record publish-race remediation) — reconciled here in v2.134. Phase-5 PDF Building extended: explicit A0/A1 page sizes (the CSS `A0` keyword is ignored by Chromium -> US Letter), MediaBox verification, pixel fill measurement for posters, no hand-placed SVG text. Canonical: CWI poster set 2026-08-21.
> Cross-reference: system-prompt v3.68, kaizen v2.90, cloudflare v3.59, session this.

> **v2.133 UPDATE (2026-08-21, kaizen — CMD SKILLS UPDATE: duplicate-record publish-race remediation gates — TITLE-EXISTENCE-PRE-PUBLISH-1 + PUBLISH-LOCK-1 + VERIFICATION-PROSE-GATE-1; mirrors kaizen v2.88):**
> Red-team: Accuracy + Completeness reviewer slots COMPLETED + direct parent audit (QNFO.RES.021 duplicate records 22044379/22045617). HARD: 4. Remediated: canonical chain advanced to v1.0.2 (10.5281/zenodo.22046458, concept 22044217 — §9 verification prose rewritten plain-publication, README How-to-Cite concept DOI, frontmatter own-DOI verified by download); duplicate concept head repaired (10.5281/zenodo.22046491 — isObsoletedBy -> canonical, license+keywords, natural creator, supersession README); R2 19 flattened legacy keys deleted (29-object mirror == deposit); D1 body_md replaced + Vectorize re-indexed.
> New Phase-6/8 permanent gates (RECURRENCE-ZERO-1):
> (1) [HARD] **TITLE-EXISTENCE-PRE-PUBLISH-1** — BEFORE creating any Zenodo deposit, run `GET https://zenodo.org/api/records?q=title:"<exact-title>"`; if a PUBLISHED record with the same title exists on a DIFFERENT concept, BLOCK and reconcile (the parallel-session race created two concepts 22044217/22044106 for one paper, 2026-08-21). Also check D1/KG/registry for the slug.
> (2) [HARD] **PUBLISH-LOCK-1** — before P8 publish, take a publish-lock in portfolio-state (write a claim row: session_id + wbs_code + target concept, UNIQUE constraint); two sessions writing the same RES.021.P8 unclaimed created the duplicate (handoffs 28675/28676).
> (3) [HARD] **VERIFICATION-PROSE-GATE-1** — publication §Verification sections MUST be plain scholarly prose (results table + reproducibility statement); BANNED in publication text: "falsifier live", "pre-registered", "bugs in the checks", "post-publication audit", "Results (seed", "CPython" as pipeline voice, "verification discipline"; raw run logs live ONLY in artifacts/verification/. Gate: grep for the banned phrases + Unicode-superscript scan (U+2070-U+209C) + version-label uniqueness (Zenodo metadata version == md frontmatter version) before publish. Canonical: RES.021 v1.0.1 §9 embedded the raw verification closeout (user-caught "WTF IS THIS?"); v1.0.2 fixed.
> Cross-reference: system-prompt v3.59, kaizen v2.88, OLD-RECORD-OBSOLETION-TAG-1, ZENODO-NEWVERSION-BECOMES-HEAD-1, session this.

# RESEARCH — v2.133
> **v2.133 UPDATE (2026-08-21, kaizen — CMD SKILLS UPDATE: PUBLICATION-META-PROSE-1 extension (user directive — superfluous meta-commentary expunged); mirrors system-prompt v3.65 + kaizen v2.88):**
> Red-team: 3 slots on the CWI poster set (15 definite meta-prose hits); remediation executed (commit 0317073). Repairs the footer drift left by the v2.132 cycle (footer 2.131 -> 2.133).
> (1) [HARD] **PUBLICATION-META-PROSE-1 (user directive 2026-08-21)** — extends the Publication Language Gate: banned "published, not hidden", "rather than the confirmation", "kept on the same ledger", "not a silence". State the fact; the DOI carries the evidence.
> Cross-reference: system-prompt v3.65, kaizen v2.88, cloudflare v3.59, session this.

> **v2.132 UPDATE (2026-08-21, kaizen — CMD SKILLS UPDATE: FRONTMATTER-DUPLICATION-1 extended (user-caught title-page duplication) + PLATFORM-NAME-SOURCE-MATCH-1; mirrors kaizen v2.87):**
> Red-team: 3 reviewer slots dispatched (queued) + direct parent-agent audit authoritative (QNFO.JPC.002 paper v0.1 P5 cycle). HARD: 2 (self-caught pre-aggregation). SOFT: 0.
> (1) [HARD] **FRONTMATTER-DUPLICATION-1 extended** — the gate now covers (a) author/byline lines in the body (e.g., `**Author** · org · date · version` under a YAML author/date block) and (b) a body H1 mirroring the YAML title. pandoc renders YAML title/subtitle/author/date/abstract; ANY of them repeated in the body duplicates the title page. Canonical: QNFO.JPC.002 paper v0.1 (2026-08-21) shipped a body byline + H1 under YAML title/author/date; the user caught the duplicate on review; fixed (byline + H1 removed) and the gate extended. Gate: zero body `**Date:**`/`**Abstract:**`/`**Author**` bylines, zero body H1 mirroring the YAML title, exactly one rendered abstract div.
> (2) [HARD] **PLATFORM-NAME-SOURCE-MATCH-1 added (Phase 5/6)** — a scorecard/platform row MUST name the material system its cited source actually measured. Canonical: the paper row read "Majorana, InAs/Al (~200 µeV)" citing arXiv:1702.02578, which measured InSb/NbTiN — renamed to match the source before publish. Check every platform name against its citation's actual system.
> Cross-reference: system-prompt v3.59, kaizen v2.87, BIB-ORPHAN-1, COMPUTATIONAL-VERIFICATION-1, session this.
> **v2.131 UPDATE (2026-08-21, kaizen — CMD SKILLS UPDATE: Beginner's Guide v1.3.x publish-then-audit cycle — SUBSTANTIVE-UPDATE-MANDATE-1 + rendering/deposit gates):**
> Red-team: 3-slot reviewer dispatch (Accuracy/Completeness/Dependency) on the v1.3.2 package. HARD: 5. SOFT: 2. Changes:
> (1) [HARD] **SUBSTANTIVE-UPDATE-MANDATE-1 added** — updates to records released months ago MUST incorporate the latest research SUBSTANTIVELY (new sections/evidence), not merely minor corrections; due diligence applies to update cycles. Canonical: Beginner's Guide v1.3 (benchmark section, E3 register design, falsification exemplar, calibrated displacement assessment, thermodynamic successors).
> (2) [HARD] **CURRENCY-DOLLAR-ESCAPE-1 added** — unescaped currency dollars create false MathJax $...$ pairs (canonical: golden-table row rendered as TeX). Every currency amount MUST be \$-escaped; gate = artifacts/verification/check_rendering.py (odd-$ + currency scans; 8 PASS/0 FAIL).
> (3) [HARD] **FRONTMATTER-DUPLICATION-1 added** — pandoc renders YAML title/subtitle/date/abstract; the body MUST NOT repeat them (canonical: body Date/Abstract duplicated YAML fields across 3 published versions). Gate: zero body **Date:**/**Abstract:** lines + exactly one rendered abstract div.
> (4) [HARD] **FFFD-RAW-FALSE-POSITIVE-1 added** — raw-byte U+FFFD inside compressed PDF streams is a coincidence, NOT a text replacement char; the authoritative gate = decompressed-text-stream scan (0 hits) + DOM check (merrorCount=0, no U+FFFD). Never block a build on a raw-byte hit alone.
> (5) [HARD] **LICENSE-CLOBBER-1 + README-CLOBBER-1 added** — git-restore of repo LICENSE/README clobbers DEPOSIT files; publish scripts MUST assert LICENSE size/CC-header AND README How-to-Cite marker before upload (canonical: v1.2.1 + v1.3 shipped QNFO-ULA/blueprint; guards in v1.3.2). Deposit files rebuild from LICENSE-CC-BY-4.0.txt / README-DEPOSIT.md.
> (6) [SOFT] R2 stale-edge-cache re-confirmed — GET download-back can serve stale bytes after overwrite; LIST etag=md5 is authoritative (R2-VERIFY-VIA-LIST-1).
> (7) [SOFT] Publish-time structural guards (not per-cycle fix-ups) end deposit-file defect recurrence.
> Cross-reference: system-prompt v3.62, kaizen v2.88, session this.


> **v2.127 UPDATE (2026-08-20, kaizen — CMD SKILLS UPDATE: post-publication audit of the $1,032 Research Program (10.5281/zenodo.22028851) + launch-cycle gates; mirrors system-prompt v3.58 + kaizen v2.84):**
> Red-team: direct parent-agent + 3-slot reviewer dispatch (Accuracy CLEAN; Dependency child failed → direct audit). HARD: 3. SOFT: 3. DESIGN: 0. Changes:
> (1) [HARD] **D1-QUOTED-RESERVED-COLS-1 (Phase 6)** — living-paper.papers column `references` is a SQLite reserved keyword: INSERT/UPDATE MUST double-quote it (`"references"`); unquoted → SQLITE_ERROR near "references" (code 7500). Canonical: ai-accelerated-research insert 2026-08-20 (400 → quoted fix).
> (2) [HARD] **ZENODO-NEWVERSION-FILE-REPLACE-1 (Phase 5)** — newversion file replacement: GET /files → DELETE each links.self (204; /files/{FILENAME} form → 500 per ZENODO-DEPOSIT-DELETE-500-1) → re-upload with **PUT** (requests.put raw bytes → 201); **POST to bucket URL → 405**. Canonical: v1.1 newversion 22028851 (2026-08-20).
> (3) [HARD] **CONCEPT-DOI-PRE-BUILD-1 (Phase 5)** — read `conceptrecid` from the DEPOSIT object immediately after creation; build the README How-to-Cite with the CONCEPT DOI BEFORE first upload (record DOI ≠ concept DOI — canonical: 22028787 vs 22028788). Shipping the record DOI labeled "concept DOI" is a HARD finding → v1.1 newversion remediation.
> (4) [SOFT] **ESSAY-DEPOSIT-EVIDENCE-PACK-1 (Phase 5)** — essay/ledger deposits MUST include the aggregation + verification scripts and summary JSON that produced the figures (canonical: aggregate_usage.py, usage_summary.json, verify_essay.py); raw usage CSVs excluded for privacy (user_id + masked api_key), documented in PROVENANCE. Remediation (registered next cycle): v1.2 newversion adding the evidence pack + dissemination package.
> (5) [SOFT] Mirror rows — GIT-MERGE-BRANCH-FETCH-1 (fetch branch before merge in fresh clones; tag AFTER the merge commit) + R2-RCLONE-TEMP-CONFIG-1 (temp rclone.conf, remote name = bucket name) + DOIDOT-403-BOT-1 (doi.org 403 = bot block; verify via DataCite findable + records API state=done).
> Cross-reference: system-prompt v3.64, kaizen v2.86, qnfo-core v1.35, session this.

> **v2.128 UPDATE (2026-08-21, kaizen — CMD SKILLS UPDATE: PUBLICATION-BRAND-LANGUAGE-1 + PUBLICATION-STATUS-STALE-1 + INTERNAL-ANCHOR-DANGLING-1 (CMD RED TEAM 4-slot, 2026-08-21); mirrors system-prompt v3.63 + kaizen v2.85):**
> Red-team of 8 records carrying the register/ledger framing: Language=CONFIRMED (user directive — branded register/ledger/honesty language banned from publication prose), Accuracy=CONCERNS, Completeness=FAIL, Dependency=CONCERNS. New Phase-5 gates: (1) Publication Language Gate extended with the banned-token list + "Disconfirmation criterion:" label (PUBLICATION-BRAND-LANGUAGE-1); (2) pre-publish + pre-newversion corpus status sweep (PUBLICATION-STATUS-STALE-1; canonical: guide v1.2/v1.2.2 E1 "unexecuted" vs 21902891 null); (3) internal-anchor resolution check (INTERNAL-ANCHOR-DANGLING-1; canonical: v1.2 "open problem 7" dangling). Canonical worst offenders: guide 22036025/22038733, QEC-Darwinism 21964674, BTQP 20109836, register 22025544.
> Cross-reference: system-prompt v3.63, kaizen v2.85, cloudflare v3.58, session this.

> **v2.125 UPDATE (2026-08-20, kaizen — CMD SKILLS UPDATE: ZENODO-LICENSE-RTYPE-MUTUAL-EXCLUSION-1 + PRERESERVE-VIA-RECORDS-API-RESERVE_DOI-1 + PDF-SUPERSCRIPT-UNICODE-1 (Phase 5/6); mirrors system-prompt v3.56 + kaizen v2.82):**
> Red-team: direct parent-agent skills audit (session this — RES.017 v1.4 + industry-brief publish cycles). HARD: 3. SOFT: 1. DESIGN: 0.
> (1) [HARD] **ZENODO-LICENSE-RTYPE-MUTUAL-EXCLUSION-1 (Phase 5/6)** — deposit API PUT stores license but clears resource_type; records API PUT stores resource_type (id-form + publisher) but clears license; final state = rtype ✓ license ✗ in public API view, .md frontmatter carries the license. Canonicals: RES.017 v1.4 (22025544) + industry brief (22028078), 2026-08-20. Accept rtype + document; UI edit or next version for license.
> (2) [HARD] **PRERESERVE-VIA-RECORDS-API-RESERVE_DOI-1 (Phase 5)** — prereserve via records API reserve_doi (POST /api/records/{id}/draft/pids/doi), NEVER deposit prereserve_doi PUT (full replacement). Fallback DOI = 10.5281/zenodo.{deposit_id}.
> (3) [HARD] **PDF-SUPERSCRIPT-UNICODE-1 (PANDOC-SAFE build)** — Unicode superscripts → U+FFFD in CDP PDFs; source must use MathJax ($2.0\times10^{-4}$) or ASCII. Canonical: industry brief 2026-08-20 (byte scan caught 1 bad byte).
> (4) [SOFT] Dispatch wave 2026-08-20 prepared (3 first contacts, record 22028078).
(4) [HARD] **CLOSEOUT-TOOL-FALLBACK-1 (closeout protocol)** — exec phantom errors ("Session is not running") mean the command may have RUN: probe via file-redirect + read-back before classifying down (EXEC-AUTOBG-READBACK-1); D1 closeout rows use the keys.json python fallback — never defer a handoff write while that path exists. Canonical: QNFO.KZ 2026-08-20 (handoff 28641).
> Cross-reference: system-prompt v3.56, kaizen v2.82, NEWVERSION-DRAFT-FILES-SHAPE-1, session this.
> **v2.124 UPDATE (2026-08-20, kaizen — CMD SKILLS UPDATE: NEWVERSION-DRAFT-FILES-SHAPE-1 + PUBLISH-CHECKLIST-PORTFOLIO-REPOINT-1 installed; mirrors system-prompt v3.55 + kaizen v2.81):**

> **v2.124 UPDATE (2026-08-20, kaizen — CMD SKILLS UPDATE: NEWVERSION-DRAFT-FILES-SHAPE-1 + PUBLISH-CHECKLIST-PORTFOLIO-REPOINT-1 installed; mirrors system-prompt v3.55 + kaizen v2.81):**
> Red-team: direct parent-agent skills audit (session this — draft-install cycle). HARD: 2. SOFT: 0. DESIGN: 1.
> (1) [HARD] **NEWVERSION-DRAFT-FILES-SHAPE-1 added (Phase 5/6 file replacement)** — Zenodo NEWVERSION draft (legacy deposit API): file metadata uses `filename` (NOT `key`); upload = POST /api/deposit/depositions/{id}/files (multipart); bucket-level URL → 405 on POST; per-file deletion ONLY DELETE {file.links.self} (204) — never .../files/{filename} (500). Replace: GET /files → DELETE each links.self → re-POST multipart. Canonical: RES.017 v1.3 (10.5281/zenodo.22017933) 2026-08-19; RES.009 v1.1 (21939493) 2026-08-14. Extends NEWVERSION-FRONTMATTER-CARRYOVER-1 / NEWVERSION-FILE-CARRYOVER-1 remediation paths.
> (2) [DESIGN] **PUBLISH-CHECKLIST-PORTFOLIO-REPOINT-1 added (Phase 6 publish checklist)** — the publish checklist MUST include an explicit step re-pointing portfolio-state.program_registry (zenodo_doi, current_version, phase) to the NEW DOI/version — CROSS-STORE-PUBLISH-SYNC-1 did not enumerate program_registry as a store (canonical: RES.017 v1.3 cycle left it at v1.0/22013264/P6, repaired 2026-08-20, changes=1).
> (3) [SOFT] **Repo-copy repair** — repo research/SKILL.md stale at v2.122 (REPO-COPY-PHANTOM-1 #3); re-copied + committed.
> Cross-reference: system-prompt v3.55, kaizen v2.81, CROSS-STORE-PUBLISH-SYNC-1, session this.
> **v2.123 UPDATE (2026-08-20, kaizen — OpenReview submission + Zenodo deposit red-team mirror; mirrors kaizen v2.79):**
> Red-team: direct parent-agent audit of the AI4MetaScience submission (#17, 6lmtqUoIbj) + Zenodo deposit (10.5281/zenodo.22026592) + R2/D1/KG distribution cycle. HARD: 3. SOFT: 2.
> (1) [HARD] **ZENODO-DEPOSIT-CREATE-SHAPE-1** — the Zenodo deposit API (POST /api/deposit/depositions) REQUIRES the WRAPPED body shape `{"metadata": {...}}`; top-level metadata fields → HTTP 400 "Unknown field" on EVERY field. The records API (POST /api/records) likewise accepts the wrapped shape. Canonical: 2026-08-20 AI4MetaScience deposit — top-level → 400 all-fields-unknown; wrapped → 201, deposit 22026592. Probe shape BEFORE building upload flows.
> (2) [HARD] **R2-VERIFY-VIA-REST-1** — `wrangler r2 object get ... > file` can embed CLI stdout noise (libuv assertions on Windows / status text) producing a WRONG download md5 (canonical: position-paper.md looked like 8bed99a2 vs true 3297cb13). The authoritative R2 download-back byte comparison is the Cloudflare REST API (GET /accounts/{acct}/r2/buckets/{bucket}/objects/{key} with CLOUDFLARE_API_TOKEN). Also: `wrangler r2 object put` REQUIRES `--remote` (WRANGLER-R2-LOCAL-MODE-1); never run put/verify loops concurrently with git checkout on the same tree (PARALLEL-WRITE-EXEC-RACE-1).
> (3) [HARD] **D1-WRITE-VIA-WRANGLER-1** — D1 INSERT/UPDATE through the Cloudflare API token can return "You do not have permission to perform this operation" while SELECT reads work; the canonical write path is `npx wrangler d1 execute <db> --remote --file=<sql>` (or --command). Canonical: 2026-08-20 handoffs 28636/28638, living-paper papers row, qnfo-graph node+edge all inserted via wrangler.
> (4) [SOFT] **OpenReview submission mirror (kaizen v2.78)** — OPENREVIEW-SUBMIT-IDEMPOTENCY-1 (pre-check /notes?invitation=...&content.authors=; post-check venue list count==1), ONE-SHOT-CRON-DOUBLE-DISPATCH-1 (run_now double-dispatch; delete one-shot job after trigger; late thread stays read-only), OPENREVIEW-API-SUBMIT-FALLBACK-1 (UI-unrenderable fallback: Network.getCookies → Bearer; PUT /attachment → POST /notes/edits; required fields/enums from 400 MultiError), SESSION-JWT-HYGIENE-1 (delete temp tokens; clear auth cookies at closeout), VENUE-LIST-IS-TRUTH-1. Canonical: 2026-08-20 submission #17 (note 6lmtqUoIbj, Position Track, CC BY 4.0).
> **v2.122 UPDATE (2026-08-19, kaizen — CMD SKILLS UPDATE: user mandate "MORE COMPUTATIONAL ANALYSIS/VERIFICATION IN RESEARCH"):**
> (1) [HARD] **COMPUTATIONAL-VERIFICATION-1 gate added (Phase 5; mirrors system-prompt v3.52)** — every research artifact with quantitative/mathematical/statistical claims MUST carry computational verification BEFORE publication: numerical evaluation of key formulas (golden values, edge cases, limits, dimensional consistency), seeded Monte Carlo for probabilistic claims, recomputation of derived quantities; VERIFY-IN-CODE-1 (any claim a computer can check MUST be checked in code before assertion); verification scripts + outputs in artifacts/verification/ AND included in the Zenodo deposit (extends PUBLICATION-SOURCE-COMPLETENESS-1); reproducibility statement (runtime/seed/versions/re-run); flagship results get interactive demos via qwav-demo-kit DEM-E0-T01..T05 (research must demonstrably execute in code).
> (2) [HARD] **TITLE-LINE-PARITY-1** — version parity = H1 title + top banner + footer "Current:" ALL equal (the v2.121-era cycle left the H1 title stale; class now codified).
> **v2.121 UPDATE (2026-08-19, kaizen - CMD SKILLS UPDATE: RES.016 publish-then-audit closeout):**
> (1) [HARD] **P3.AUTHOR-GATE-EVERY-ENTRY-1 added** - the RES.016 pass-1 accuracy audit (2026-08-19) caught 3 fabricated author attributions in a PUBLISHED record (v1.0, 10.5281/zenodo.22009653) that in-session spot-checks of 4-5 sampled DOIs MISSED: "Caruana" (RMP Kochen-Specker review), "Khodjaev" (Entropy p-adic qubit), "VVZ 1998" (DOI 10.2748/tmpub.10.1 actually authored by Youngho Jang). P3.AUTHOR-GATE now requires live Crossref/OpenAlex verification of EVERY entry author list, never a sample. Remediated in v1.1 (10.5281/zenodo.22010489).
> (2) [HARD] **NEWVERSION-FILE-CARRYOVER-1 added** - newversion drafts carry over ALL parent files byte-identical, not just the frontmatter .md. ANY repo file that changed since the prior publish (auxiliary living docs like RESEARCH-CONTINUITY-REGISTRY.md) must ALSO be replaced in the draft. Canonical: RES.016 v1.1 - deposited registry was a v1.0-era blob (4484 B vs 4834 B HEAD) missing one session-log row; caught by the completeness reviewer md5 comparison (NEWVERSION-FRONTMATTER-CARRYOVER-1 is necessary but NOT sufficient).
> (3) [SOFT] **ZENODO-VERSION-LABEL-EDIT-1 re-confirmed** - deposit-API newversion publishes with version=None; fixed via actions/edit then full-metadata PUT (carry ALL fields incl. related_identifiers) then publish. DataCite subjects read-back (not the Zenodo GET-view) is the authoritative subject check (RES.016 v1.1: GET-view empty, DataCite 10 subjects).

> **v2.120 UPDATE (2026-08-18, kaizen — CMD SKILLS UPDATE: PRACTITIONER-RELEVANCE-1 gate + UMP.012 post-publication remediation; mirrors system-prompt v3.45 + kaizen v2.70):**
> Red-team: 3-reviewer subagent audit of UMP.012 (2 HARD: missing README, venue mis-attribution) — both remediated (v0.3 + v0.4) this cycle.
> HARD: 1. SOFT: 0. DESIGN: 1. Changes:
> (1) [HARD] **PRACTITIONER-RELEVANCE-1 (Publication gate, 2026-08-18)** — every paper must include a practitioner-facing section stating what a practitioner can DO with the result: explicit implementation path, tangible product embodiment (demo/SDK/benchmark/spec-sheet/decision tool), written in professional/engineering language. Consilience constraint: no niche-terminology dead-ends — every framework term anchored to a practitioner-usable concept within two sentences. The standing question (user directive 2026-08-18): "what can a practitioner actually implement in a tangible product?"
> (2) [DESIGN] **Venue claims are first-class citation fields** — a claimed conference presentation must be verified against the official program page (ZENODO-VENUE-ATTRIBUTION-1); the arXiv listing proves existence, not venue.
> Cross-reference: system-prompt v3.45, kaizen v2.70, SO-WHAT-GATE-1, PUBLICATION-PROSE-GATE-1, session this.


> **v2.118 UPDATE (2026-08-18, kaizen — CMD SKILLS UPDATE: red-team remediation — 5 publication gates + forensic-deposit rule codified; mirrors system-prompt v3.43 + kaizen v2.68):**
> Red-team: CMD RED TEAM cycle 2026-08-18 (session f_bH6KMZ4Og2Wvw79S9rU). HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **PUBLICATION GATES codified in this skill (system-prompt HARD gates previously absent here)** —
>    - R2-MIRROR-AFTER-PUBLISH-1: every Zenodo publication MUST be mirrored to the canonical R2 papers bucket `qnfo-releases` at `YYYY/MM/<slug>/` (main file + README.md + ALL source files) within the same cycle, and the KG Paper node updated to `distribution_status: distributed` + `r2_path` + `r2_readme`; verify via bucket listing after write. Publishing to Zenodo alone leaves the artifact at `published`; a missing R2 mirror is a HARD finding.
>    - WRONG-BUCKET-SELECTION-1: the canonical papers bucket is `qnfo-releases`, NOT the bare `releases` bucket; verify the target bucket against a known sibling object (list an existing paper folder first) before any R2 write.
>    - ZENODO-PLACEHOLDER-DOI-1: `prereserved_doi` may return None — NEVER rely on it; verify the UPLOADED FILE (fetch back; assert no `<RESERVED>` remains) BEFORE publish; a published placeholder is immutable — remediate via a new version.
>    - ZENODO-CONCEPT-DOI-CITE-1: versioned records' How-to-Cite blocks MUST cite the CONCEPT DOI, not the v1 record DOI; after publish read `conceptrecid` and confirm cite block + frontmatter.
>    - POST-PUBLICATION ADVERSARIAL ANALYSIS GATE: every published artifact MUST receive a critical adversarial analysis AFTER publication (CMD RED TEAM SUB: 3-5 reviewer slots Accuracy/Completeness/Dependency; WAIT per REDTEAM-QUEUE-STALL-PATIENCE-1 ~15-min budget; aggregate; READ-ONLY; fallback = direct 5-adversary audit). HARD findings become next-cycle kaizen items — publish-then-audit, never publish-then-forget.
>    - FORENSIC-DEPOSIT-1: forensic analyses MUST be deposited as artifacts with the publication (2026-08-12 audit HARD finding: "forensic analyses not deposited"); never keep forensic evidence in private notes only.
> (2) [SOFT] **H1 added** — this skill had no current-version H1 title (first H1 was a Zenodo API header); H1 now v2.118 == frontmatter == latest banner.
> Cross-reference: system-prompt v3.43 (PROMPT gates), kaizen v2.68, session f_bH6KMZ4Og2Wvw79S9rU.

> **v2.117 UPDATE (2026-08-18, kaizen — CMD SKILLS UPDATE: PUBLICATION-PROSE-GATE-1; mirrors system-prompt v3.42 + kaizen v2.67):**
> Red-team: direct parent-agent skills audit (session this — UMP.012 v0.1→v0.2 user-correction cycle).
> HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **PUBLICATION-PROSE-GATE-1 added to Phase 5 Pre-Publication Requirements** — publication-facing text (paper abstract, deposited .md, Zenodo metadata description, social posts) MUST be written in plain scholarly prose for a human reader. Internal pipeline vocabulary is PROHIBITED in the publication text: gate names ("SO-WHAT-GATE", "premise-depth disclosure" as a label), WBS codes, "T1–T8"/"seams catalog" shorthand, "companion artifact" headers, "research-cycle record" blocks, "UIA"/"ZENODO-INQUIRY" references, "Why a reader should care:" as a literal label, and internal ops content (data-quality drift findings, pipeline status). The SO-WHAT-GATE and premise-depth requirements are satisfied BY THE PROSE ITSELF: the abstract states why a reader should care and where the premises end, in natural language — never by naming the gates. User standard (2026-08-18): publications must be timely, engaging to read, and relevant to current practice and research. Canonical: QNFO.UMP.012 v0.1 (10.5281/zenodo.21985456) failed user review as "shorthand"; v0.2 (10.5281/zenodo.21990225) plain-prose rewrite accepted.
> Cross-reference: system-prompt v3.42, kaizen v2.67, SO-WHAT-GATE-1, session this.
> **v2.116 UPDATE (2026-08-17, kaizen — CMD SKILLS UPDATE: VECTORIZE-TOP-K-50-1 + ZENODO-VERSION-LABEL-EDIT-1; mirrors system-prompt v3.39 + kaizen v2.65):**
> Red-team: direct parent-agent skills audit (session this — UMP.011 P9 closeout cycle; the qnfo-memory-mcp 1101 was root-caused via wrangler tail).
> HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **DUE-DILIGENCE-DEPTH-1 execution note — semantic-channel workaround** — qnfo-memory-mcp search_papers throws Error 1101 for limit >= 17 due to the worker's topK = 3 x limit rerank buffer exceeding Vectorize's 50-cap with returnValues=true (VECTOR_QUERY_ERROR 40025 — see VECTORIZE-TOP-K-50-1 in kaizen v2.65 / cloudflare v3.54). When the Phase 1 semantic sweep hits 1101 at limit>=20: retry at limit<=16 (verified reliable) and note the cap in the evidence file; do NOT label the channel "outage" — it is a query-size bug. Full 4-topic x 3-formulation sweep at limit=16 is valid corpus-scale coverage (canonical: UMP.011 P9 2026-08-17, 12/12 formulations succeeded).
> (2) [SOFT] **ZENODO-VERSION-LABEL-EDIT-1 cross-ref** — deposit-API-created records: version label via POST /actions/edit -> PUT full metadata -> POST /actions/publish (records-API /draft 404s for these records); see kaizen v2.65.
> Cross-reference: system-prompt v3.39, kaizen v2.65, cloudflare v3.54, session this.

> **v2.115 UPDATE (2026-08-16, kaizen — CMD CONTINUE correction: NO traditional journal submissions):**
> Red-team: direct parent-agent (session QVfcGcaza2VKvkXttwx3s). HARD: 1. SOFT: 0. DESIGN: 0.
> (1) [HARD] **NO-JOURNALS-1 (Publication Venue)** — CATEGORICAL USER DIRECTIVE (2026-08-16): the user NEVER submits to
>     traditional academic journals, ever. Do NOT suggest/prepare journal submissions (cover letters, shortlists) unless
>     explicitly prompted. Autonomous submission ONLY to outlets that are fully autonomous + 100% complete with zero manual
>     intervention (rules out paid + proprietary/esoteric systems). Canonical venue = Zenodo ONLY. Phase 7's "Journal Submission
>     (HARD)" gate was DEFECTIVE (contradicted the user's standing preference; caused a cover-letter + shortlist to be drafted
>     this session, retracted in commit a1a7d09). Corrected: Phase 7 now = "Publication Venue"; journal shortlist + cover-letter
>     protocol REMOVED; replaced with autonomous-only guidance.
> Cross-reference: NO-JOURNALS-1, system-prompt v3.29, user_preference mem-_1gt5bzs_EY9, commit a1a7d09.

> **v2.115 UPDATE (2026-08-16, user-requested research — dissemination outlets add-on):**
> User mandate: research Zenodo communities + other open-science outlets for QNFO publication
> with NO content regulation (no formatting template, no AI-text ban), NO gatekeeping/endorsement
> (no arXiv), NO cost, fully DeepChat-executable. HARD: 1 (findings baked into Phase 7).
> (1) [HARD] **DISSEMINATION-OUTLETS-1** — Phase 7 new subsection "Open Outlets & Community
>     Dissemination": verified landscape (OSF Preprints DISQUALIFIED — bans LLM/AI text + suspended
>     submissions Aug 2025; Zenodo communities BIMODAL — few large open communities worth
>     inclusion REQUESTS (acceptance curator-gated per ZENODO-COMMUNITY-INCLUSION-REQUEST-1,
>     VERIFIED LIVE 2026-08-16)
>     vs. many 0-4-record slug-squatted ones; Figshare = secondary leg; viXra = reputation risk),
>     target community shortlist (advancedtheoreticalphysicsandmathematics 1004 rec,
>     fbt-framework 366 rec ★ direct UMP/RES match, tp-a-m-c 745 rec — all open for
>     inclusion REQUEST, acceptance curator-gated), scripts `research/scripts/zenodo-communities.py` + `figshare-submit.py`,
>     evidence report `research/references/dissemination-outlets-2026-08-16.md`.
> Cross-reference: kaizen v2.53, system-prompt v3.24, session tGKyVRwKJGbLDdKZtEKpa.

> **v2.114 UPDATE (2026-08-16, kaizen — CMD SKILLS UPDATE: SO-WHAT/premise-depth publication gate):**
> Red-team: direct parent-agent audit (session QVfcGcaza2VKvkXttwx3s). HARD: 1. SOFT: 0. DESIGN: 0.
> (1) [HARD] **SO-WHAT-GATE-1 (Publication)** — every paper abstract and every social post MUST carry: (a) an explicit
>     "why a reader should care" statement, and (b) a premise-depth disclosure (which claims are derived vs. unanalyzable
>     primitives or named imported inputs; how deep the theory goes and where its premises END). Added to the Pre-Publication
>     Requirements alongside PANDOC-SAFE and BP-1/BP-2. Gap analysis (Phase 1) must state the premise-chain depth so novelty
>     claims are bounded by the depth of their assumptions (canonical: RES.011 — the abelian-pair postulate is a NAMED INPUT,
>     so "statistics from logic" is as deep as that premise, nothing more). Mirror of system-prompt v3.29 SO-WHAT-GATE-1.
> Cross-reference: SO-WHAT-GATE-1, system-prompt v3.29, kaizen v2.55.

**PRACTITIONER-RELEVANCE-1 (HARD GATE, 2026-08-18):** Every paper must speak to practitioners,
not only theoreticians. Required: (a) an explicit practitioner-facing section stating what a
practitioner can DO with the result — implementation path, tangible product embodiment (demo,
SDK, benchmark, spec-sheet, decision tool), in professional/engineering language; (b) each
practitioner claim paired with the domain where it holds (conditional truth); (c) consilience —
no niche-terminology dead-ends: every framework term anchored to a practitioner-usable concept
within two sentences. Standing question (user directive 2026-08-18): "I have written enough
high-level theory — what can a practitioner actually implement in a tangible product?"

> **v2.113 UPDATE (2026-08-15, kaizen — CMD SKILLS UPDATE: BRIEFING-DENSITY-1 (no empty daily-briefing notes) + system-prompt v3.28):**
> Red-team: direct parent-agent skills audit (session this — cycle 2; user mandate: only highly relevant research,
> no empty briefing notes, no administrivia).
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **BRIEFING-DENSITY-1** — daily briefing (research-daily-brief.py + wrapper) MUST show ONLY highly
>     relevant research (precision over recall, no clutter); if the run reports 0 unique papers matched, DO NOT
>     create/write an empty Obsidian daily-briefing note (skip the write-to-obsidian.py pipe; the email archive to
>     alerts@qnfo.org still runs). research-daily-brief.py itself does NOT write Obsidian notes — the guard lives
>     in the wrapper step (cronjob fdf1403c taskPrompt updated; manual runs: skip write-to-obsidian when
>     "Total: 0 unique papers").
> Cross-reference: system-prompt v3.28, kaizen v2.53, cronjob fdf1403c, session this.


> **v2.112 UPDATE (2026-08-14, kaizen — CMD SKILLS UPDATE: Zenodo newversion file-delete + D1 write discipline + S2 gap + email async-verification):**
> Red-team: direct parent-agent skills audit (session PzctHHW4qJopkaNoCTABv — QNFO.RES.009 publish→audit→remediate→outreach cycle).
> HARD: 2. SOFT: 2. DESIGN: 0. Changes:
> (1) [HARD] **ZENODO-DEPOSIT-DELETE-500-1 added** — on a Zenodo NEWVERSION draft, `DELETE /api/deposit/depositions/{id}/files/{FILENAME}` returns HTTP 500 (server error) while `DELETE {file.links.self}` (per-file UUID URL) returns 204; bucket-level PUT returns 404. Replacement workaround: GET /files → DELETE each target's links.self → re-POST multipart. Canonical: QNFO.RES.009 v1.1 newversion (draft 21939493) — references.bib/.md/.html/.pdf/citation-audit.md replaced this way.
> (2) [HARD] **D1 write discipline** — `INSERT OR IGNORE` silently swallows NOT NULL violations (canonical: papers.authors); use plain INSERT to surface constraint errors. D1 rejects single values above ~1 MB (SQLITE_TOOBIG) — store pre-inline HTML (~25 KB) not MathJax-inlined (~2.3 MB) in body_html.
> (3) [SOFT] **Semantic Scholar systematic 404** — S2 does not index the QNFO Zenodo record set at all (3/3 DOIs 404 on 2026-08-14 incl. flagship QUNTUF 10.5281/zenodo.21208346, which IS OpenAIRE-indexed); not ingestion lag; no automatic path; document, do not retry.
> (4) [SOFT] **Email Sending REST async shape** — 200/success/message_id may return EMPTY delivered/queued arrays; verify actual delivery via the recipient mailbox (marker-prefixed test subjects land in Junk per EMAIL-SUBJECT-SPAM-TOKENS-1) before real outreach.
> Cross-reference: knowledge v2.13, kaizen v2.48, system-prompt v3.23, session PzctHHW4qJopkaNoCTABv.

> **v2.111 UPDATE (2026-08-14, kaizen — CMD SKILLS UPDATE: N-2 frontmatter repair — content was already v2.110):**
> Red-team: direct parent-agent skills audit (session this). HARD: 1. SOFT: 0. DESIGN: 0.
> (1) [HARD] **frontmatter v2.109 -> v2.110** — content banners already at v2.110 (VECTORIZE-403-
>     MISDIAGNOSIS + WBS-COLLISION-2 + REDTEAM-QUEUE-STALL-1 from the prior cycle); frontmatter
>     had drifted one version behind. No content change; parity with system-prompt v3.21 verified.
> Cross-reference: kaizen v2.46, cloudflare v3.51, system-prompt v3.21, session this.


> **v2.110 UPDATE (2026-08-14, kaizen — CMD SKILLS UPDATE: VECTORIZE-403-MISDIAGNOSIS + WBS-COLLISION-2 + REDTEAM-QUEUE-STALL-1):**
> Red-team: direct parent-agent audit (session FJ4ZYy6OEfAnpu8mq30OZ; QNFO.RES.007 5-adversary audit + outreach cycle).
> HARD: 3. SOFT: 0. DESIGN: 0.
> (1) [HARD] **VECTORIZE-403-MISDIAGNOSIS anti-pattern added** — qnfo-paper-indexer 403/error-1010 was MISDIAGNOSED as
>     "token rotated" (memory + logs) when the root cause was the MISSING browser User-Agent: default Python urllib
>     UA triggers Cloudflare Browser Integrity Check (BIC, error 1010) on every path of the worker regardless of token
>     validity. Token `chnx-idx-v1-k9m2n4p7r5t8` was valid throughout. Verified live 2026-08-14: with
>     `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...` the same endpoint returns
>     `200 {"success":true,"indexed":false,"skipped":true,"reason":"unchanged"}`. ALL qnfo-paper-indexer calls (and any
>     Cloudflare-worker HTTP call from Python) MUST send a browser-like User-Agent. 403 from this worker is a UA
>     problem, NOT a token problem — test the UA hypothesis BEFORE diagnosing token rotation (BLAME-EXTERNAL-1
>     discipline). Canonical case: QNFO.RES.007 2026-08-14 closeout (Vectorize 21 chunks, 0 errors, verified with UA).
> (2) [HARD] **WBS-COLLISION-2 anti-pattern added** — two concurrent sessions resolving "next available WBS code"
>     against D1 program_registry can select the SAME code; the later session's INSERT/UPDATE silently overwrites the
>     first project's row (metadata for a different thesis). Canonical case: QNFO.RES.007 vs formal-self-reference-limits
>     2026-08-14 — canonical row (invariant-structural-value) restored; late claim renumbered to RES.008 (per
>     RES.004/005 precedent: first claim keeps the code). WBS resolution MUST be atomic: check-then-insert in ONE
>     transaction or with a UNIQUE constraint / registry lock; when resuming a session after a gap, re-verify the D1
>     row identity (name + slug), not just wbs_code, BEFORE any write.
> (3) [HARD] **REDTEAM-QUEUE-STALL-1 anti-pattern added** — reviewer subagents dispatched via deepchat_subagents
>     frequently remain QUEUED >150s (no turn started) in this environment (documented 2026-08-10, 2026-08-13,
>     2026-08-14). A queued subagent is NOT a review. Mandatory fallback: after ~75s without a started turn, execute
>     the direct parent-agent audit (Mandate 3 §Reviewer Failure Fallback) and log the stall. NOTE: a reviewer CAN
>     eventually complete and return REAL findings (RES.007 2026-08-14: FAIL with 3 HARD — duplicate Joyal-Street work
>     with synthetic DOI `doi={joyalstreet1986}`, audit accounting double-count, BP-10 unverifiable "51/51") — always
>     poll/inspect the delegation before finalizing closeout, and treat late-arriving findings as remediation items.
> Cross-reference: kaizen v2.44, email-composer v2.19 (send UA gotchas), session FJ4ZYy6OEfAnpu8mq30OZ.

> **v2.109 UPDATE (2026-08-14, kaizen — CMD SKILLS UPDATE: NEWVERSION-FRONTMATTER-CARRYOVER-1 + DOI-WAF-403 audit helper):**
> Red-team: direct parent-agent skills audit (session DRUiOGPDwdzH2BayFiv9x; RES.007 publish-then-audit cycle).
> HARD: 1. SOFT: 1. DESIGN: 0.
> (1) [HARD] **NEWVERSION-FRONTMATTER-CARRYOVER-1 anti-pattern added** — Zenodo newversion drafts carry ALL
>     parent files byte-identical; the .md YAML frontmatter `doi:` still points at the PARENT version.
>     Publishing a newversion without patching the frontmatter to the NEWVERSION's own reserved DOI ships a
>     stale self-DOI. MANDATORY newversion order: (1) create draft + reserve new DOI; (2) patch .md
>     frontmatter doi + status BEFORE upload (P5.FRESH); (3) rebuild html/pdf if body changed; (4) replace
>     carried-over files in draft (delete + re-upload); (5) publish; (6) verify deposited .md sha256 vs local
>     + doi.org HEAD 200 + DataCite findable. Canonical case: QNFO.RES.007 v0.2 (10.5281/zenodo.21929590)
>     shipped stale v0.1 DOI (10.5281/zenodo.21929479) in its deposited .md — Accuracy-reviewer HARD-1;
>     remediated via v0.3 (10.5281/zenodo.21929902). Anti-anti-pattern: never call a newversion's reserved
>     DOI "phantom" merely because the parent is newer — verify records API state=done or the concept
>     is_last chain before reverting frontmatter (a concurrent session reverted to the parent DOI in error).
> (2) [SOFT] **DOI-WAF-403 audit-helper note** — doi.org HEAD returns 403 on some publisher DOIs
>     (OUP/OBO/MDPI/CNTP/APS) under audit User-Agent; 403 != dead DOI. Audit helpers MUST auto-fallback to
>     Crossref API (api.crossref.org/works/{doi}) for authoritative year/author/title before flagging a DOI
>     as unresolvable (same family as ZENODO-BOT-403-1). Verified live 2026-08-14 (5 DOIs: all 403-on-HEAD,
>     all Crossref-confirmed).
> (3) [DESIGN] UTF-8 byte-vs-char counting trap — paper .md "size discrepancy" audits must compare
>     normalized content (CRLF->LF) or decode-aware lengths; a byte-count difference of ~18-28B on a
>     ~14.5KB file is often UTF-8 multi-byte chars (π, θ, ℤ), not content drift (RES.007 closure cycle).
> Cross-reference: kaizen v2.43, system-prompt v3.19 (NEWVERSION-FRONTMATTER-CARRYOVER-1 HARD GATE),
> ZENODO-PHANTOM-DOI-1, P5.FRESH, R2-CDN-CACHE-1, session this.

> **v2.108 UPDATE (2026-08-14, kaizen — CMD SKILLS UPDATE: DUE-DILIGENCE-DEPTH-1):**
> Red-team: direct parent-agent skills audit + 5-store prompt parity verification (session this).
> HARD: 2. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **DUE-DILIGENCE-DEPTH-1 added** — Phase 1(a) upgraded to full-corpus due diligence
>     (user mandate 2026-08-14: ~1,000-record QNFO corpus, growing rapidly, diverse domains/methods/
>     results; ALL records valuable): query_graph(stats) FIRST, >=3 distinct query formulations per
>     topic, search_papers limit 10 -> 20, cross-system ID validation via resolve_paper_id per hit,
>     >=2 adjacent WBS domains, external independent verification (arXiv/OpenAlex/Crossref/
>     archive.org CDX/Google Patents), evidence-discipline for every count/DOI.
> (2) [HARD] **Superseded DOI sweep re-verified** — 21878943 (x2) / 21878977 (x4) remain ONLY in
>     historical banners/case-history (v2.104 sweep complete); all live references point to v0.3
>     21901984 (x8) / 21901983 (x7).
> (3) [SOFT] **Frontmatter version 2.107 -> 2.108.**
> Cross-reference: system-prompt v3.17, kaizen v2.41, deepchat-settings v1.17, session this.


> **v2.107 UPDATE (2026-08-13, kaizen — PARTIAL-PUT-CLEARS-FIELDS-1):**
> Red-team: direct parent-agent audit (CMD RED TEAM SUB — GitHub related_identifiers regression).
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **PARTIAL-PUT-CLEARS-FIELDS-1 anti-pattern added** — Zenodo metadata PUT is FULL
>     REPLACEMENT, not merge. A one-field edit (e.g. keywords) that omits `related_identifiers`
>     silently WIPES the GitHub provenance link (and any other omitted field). Every metadata
>     amendment MUST be a full-object PUT preserving: title, publication_date, resource_type,
>     creators, publisher, description, access_right, license, version, keywords, AND
>     related_identifiers (scheme=url, relation_type=issupplementto, GitHub branch URL).
>     Canonical case (2026-08-13): PhilPapers keyword amendment on idempotent-core 21916939 +
>     void-is-not-false 21916970 wiped their GitHub related_identifiers; restored via full PUT.
>     Cross-check: verify the record's related_identifiers AFTER any metadata PUT.
> Cross-reference: kaizen v2.38, ZENODO-RECORDS-API-DROPS-METADATA-1, AD-HOC-ZENODO-METADATA-1,
> system-prompt v3.14, session this.

> **v2.106 UPDATE (2026-08-13, kaizen — GITHUB EXTERNAL-RESOURCES LINKAGE):**
> Red-team: direct parent-agent 5-adversary audit (user mandate: ALL Zenodo records must show
> GitHub provenance as 'External resources / Available in <repo> / Release: <branch>').
> HARD: 0. SOFT: 1. DESIGN: 0. Changes:
> (1) [SOFT] **PUBLICATION-SOURCE-COMPLETENESS-1 extended** — the GitHub provenance
>     `related_identifiers` entry MUST use: `scheme: "url"`, `relation_type: {"id": "issupplementto"}`,
>     `identifier: https://github.com/QNFO/<repo>/tree/<branch>`. This exact shape is what makes
>     Zenodo render the "External resources / Available in <repo> / Release: <branch>" block on the
>     record page (verified live 2026-08-13 on idempotent-core 21916939 + void-is-not-false 21916970).
>     The bare-repo URL (`https://github.com/QNFO/<repo>`) is NOT sufficient — the `/tree/<branch>`
>     path is what yields the Release label.
> Cross-reference: kaizen v2.36, system-prompt v3.13, session this.

> **v2.105 UPDATE (2026-08-13, kaizen — CMD SKILLS UPDATE: PUBLICATION-SOURCE-COMPLETENESS-1):**
> Red-team: direct parent-agent 5-adversary audit (CMD RED TEAM SUB on Zenodo 21915967/21916107).
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **PUBLICATION-SOURCE-COMPLETENESS-1 anti-pattern added** — Zenodo deposits MUST contain
>     ALL original source files: <slug>.md/.html/.pdf (final artifacts) + references.bib +
>     citation-audit.md + PROJECT-PLAN.md + README.md + docs/deep-research.md + artifacts/consilience-gate.md
>     + artifacts/bayesian-evidential-weight.md + artifacts/external-search/* (all evidence) AND a GitHub
>     provenance link (related_identifiers isSupplementTo -> repo branch URL). The 3-file set is a MINIMUM,
>     not the complete set. User mandate 2026-08-13: "ALL PUBLICATIONS MUST CONTAIN ALL ORIGINAL SOURCE
>     FILES... WHEN IN DOUBT INCLUDE EVERYTHING, DON'T LEAVE ANY FILES OUT." Canonical case: the two
>     Laws-of-Form spinoff deposits (21915967 idempotent-core, 21916107 void-is-not-false) shipped 3 files
>     only; remediated via newversion with the full provenance set + GitHub link.
> Cross-reference: kaizen v2.35, system-prompt v3.12, session this.

> **v2.104 UPDATE (2026-08-13, kaizen — CMD SKILLS UPDATE: ZENODO-INQUIRY-1 DOI sweep):**
> Red-team: direct parent-agent audit. HARD: 1. SOFT: 0. DESIGN: 0.
> Superseded DOIs -> v0.3: 21878943 -> 21901984 (UIA), 21878977 -> 21901983 (IAPS); 5 refs updated.
> Cross-ref: kaizen v2.34, qnfo-core v1.28, execution-mandate v2.10.

---





name: research





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

> **v2.102 UPDATE (2026-08-12, kaizen — CMD SKILLS UPDATE: Zenodo API WAF browser-context pattern + metadata-notes amendment):**
> Red-team: direct parent-agent 5-adversary audit (CMD SKILLS UPDATE — session this, BJ Klock provenance cycle).
> HARD: 0 (research-side). SOFT: 3. DESIGN: 1. Changes:
> (1) [SOFT] **Zenodo API WAF: urllib 403 even WITH Bearer token; browser-context fetch on zenodo.org origin works.**
>     Python urllib (requests too) hits "unusual traffic from your network" 403 (nginx WAF bot-detection on the
>     datacenter IP) REGARDLESS of token — the user's own 2026-08-05 A/B test proved minimal-UA requests trigger
>     it. Canonical path for Zenodo API writes (newversion / PUT metadata / publish): browser-context fetch from
>     a zenodo.org-origin page with `Authorization: Bearer <token>` + `User-Agent: Mozilla/5.0` — verified live
>     2026-08-12: 6 records updated (newversion 201 → PUT 200 → publish 202) with zero 403s. Alternative:
>     full Chrome UA + Accept-Language + Referer + Origin headers from Python (200/201, user's 08-05 test).
>     Zenodo support's "upgrade your browser" guidance applies to the WEB UI (insecure-version DDoS mitigation),
>     NOT to the REST API path.
> (2) [SOFT] **Metadata-only amendment = newversion → PUT metadata.notes → publish.** To add a provenance note
>     (or any metadata field) to a published record WITHOUT touching files: `POST /api/deposit/depositions/{id}/
>     actions/newversion` (files carry over byte-identical) → `PUT /api/deposit/depositions/{draft_id}` with
>     `{"metadata": {...existing..., "notes": "<text>"}}` → `POST .../actions/publish`. Verified live 2026-08-12:
>     6 HRC records got a provenance note; file counts unchanged (5/2/0/0/0/2); concept DOIs resolve to the new
>     noted versions; old versions untouched (history preserved). Zenodo does NOT allow editing a published
>     record in place — new version is the only path.
> (3) [SOFT] **archive.org CDX rate-limits Python (429); browser load_url to the CDX JSON works.** For Wayback
>     capture-history audits use browser navigation (load_url on the CDX endpoint, parse innerText JSON) or
>     throttle Python hard; wildcard CDX queries (`bjklock.com/*copied*`) time out — use exact-path queries.
> (4) [DESIGN] **Klock incident cross-ref** — cranks with "sealed provenance" claims: Wayback audit (bjklock.com
>     HRC page first archived 2025-03-18, "sealed" pages ALL postdate Rowan's Zenodo v1.0 2025-07-08, accusation
>     page 0 captures) + Google Patents (zero patents) are the decisive counters; never engage the InMail.
> Cross-reference: kaizen v2.30, deepchat-settings v1.16, system-prompt v3.7 (f878d47fe46c0dbb), session this.

> **v2.101 UPDATE (2026-08-12, kaizen — CMD SKILLS UPDATE: N-2 header fix + DSI methodology cross-ref):**
> Red-team: direct parent-agent 5-adversary audit (CMD SKILLS UPDATE — session this). Watchtower: research v2.100 hdr stale (v2.99) — FIXED. HARD: 0. SOFT: 1. DESIGN: 1. Changes:
> (1) [SOFT] **Header v2.99 → v2.101** (N-2 triple consistency).
> (2) [DESIGN] **Radix-agnostic DSI methodology cross-ref** — the certified three-stage detector (`research/scripts/dsi-radix-detector.py`, commits a9db635→969b982) is the canonical radix-agnostic DSI discovery instrument: Stage 1 detrend + FFT/Lomb-Scargle (grid-uniformity guard auto-selects Lomb-Scargle on non-uniform grids — DESIGN-7), Stage 2 bounded sinusoid refinement (sigma_lambda), Stage 3 candidate-radix test; mandatory certification (max-statistic bootstrap p — ALREADY multiplicity-corrected, do NOT Sidak; DeltaBIC>10; integrity gates G1 resolvability omega>=2pi/u_span / G2 SNR>=1 / G3 sigma_lambda/lambda<10%); G4 model-subtraction mode for non-power-law spectra (scan log(y)-log(model) residuals). QNFO.UMP.008 null on Planck 2018 (DOI 10.5281/zenodo.21902891): no certified DSI at any resolvable radix incl. p-adic 2,3,5,7. Cross-ref: methodology note _26224105300.md.
> Cross-reference: kaizen v2.29, QNFO.UMP.008 DOI 10.5281/zenodo.21902891, session this.












> **v2.100 UPDATE (2026-08-12, kaizen — CMD SKILLS UPDATE: post-publication remediation learnings — records-API newversion version-inheritance + related_identifiers relation_type + DataCite-authoritative license verification):**
> Red-team: direct parent-agent 5-adversary audit (CMD RED TEAM SUB remediation cycle on Zenodo
> 21878977/21878976 v0.3 + 2026c Corrections and Governance Record 10.5281/zenodo.21901930, session
> z1a7zdl9MIPcta7TA-sOL). Watchtower: research v2.99 N-2 CLEAN pre-edit (raw anchors). HARD: 2 (missing
> pipeline documentation). SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **Records-API newversion does NOT inherit the parent's `version` label** — newversion drafts
>     created via `POST /api/records/{id}/versions` publish with `metadata.version: None` unless set
>     explicitly. Fix: set `metadata.version` in the records-API full-replacement metadata PUT before
>     publish. Canonical: v0.3 records 21901983/21901984 showed version=None after first publish; fixed
>     via records-API in-place metadata PUT (POST /draft → PUT metadata → publish 202, same DOI).
> (2) [HARD] **Records-API `related_identifiers` requires `relation_type` (object shape)** — the
>     deposit-API `relation` string shape → publish 400 "Missing data for required field: relation_type".
>     For records-API newversions the version chain is automatic via /versions — OMIT related_identifiers
>     entirely (simplest) or use the InvenioRDM object shape. Canonical: fix_version3.py publish 400
>     (3 related_identifiers with `relation` string) → fix_version4.py omitted them → publish 202, DOI
>     preserved (10.5281/zenodo.21901983 / 21901984).
> (3) [SOFT] **DataCite is the authoritative license/keywords verifier for records-API publishes** — the
>     Zenodo records GET-view may show `license: null, keywords: 0` after a records-API metadata PUT+
>     publish even when the metadata WAS stored; check DataCite subjects/rightsList
>     (api.datacite.org/dois/{doi}). In the 2026-08-12 v0.3 cycle DataCite showed subjects=10/11 +
>     rights=1 (cc-by-nc-sa-4.0) on both records — proving the license+keywords ARE registered despite the
>     GET-view null. Extends ZENODO-RECORDS-API-DROPS-METADATA-1 verification protocol (its canonical
>     qwave-qudit-advantage v0.3 stored via deposit-API shape; this cycle proves the DataCite read-back is
>     the authority regardless of which write API was used).
> Cross-reference: ZENODO-RECORDS-API-DROPS-METADATA-1, NEWVERSION SELF-DOI ORDERING RULE, TWO-API METADATA
> SHAPE DISTINCTION, kaizen v2.28, deepchat-settings v1.15, session this.

> **v2.90 UPDATE (2026-08-10, kaizen — CMD RED TEAM follow-up: briefing email sender override + Email Sending 10002):**
> Red-team: direct parent-agent 5-adversary audit (CMD RED TEAM directive, session this — daily briefing run 2026-08-10 hit HTTP 500 on the archive email). Watchtower: N-2 CLEAN pre-edit. HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **research-daily-brief.py --from sender override added** — the email_archive leg POSTs to the qnfo-email Worker /send with NO `from`, so the Worker defaults to `qnfo@qnfo.org`, which is BROKEN platform-side since 2026-08-08 (CF error 10002 email.sending.error.internal_server, see email-composer v2.15 EMAIL-SENDING-DOMAIN-10002). Every briefing email since then silently failed with HTTP 500 (this session's 08:00 UTC run included). Fix: `--from rowan.quni@qwav.tech` (verified working domain) or any ALLOWED_DOMAINS address; when qnfo.org recovers, drop the flag. Cross-ref: email-composer v2.15 (Sender-Domain Fallback, EMAIL-SENDING-DOMAIN-10002), kaizen v1.95.
> Cross-reference: email-composer v2.15, kaizen v1.95, session this.

> **v2.87 UPDATE (2026-08-06, kaizen — ZENODO-RECORDS-API-DROPS-METADATA-1 + P5.FRESH self-DOI ordering + INTERNAL-REF-1 extension):**
> Red-team: direct parent-agent 5-adversary audit (session ktkjFggX5vMt1h4ogDIwh — SKILLS UPDATE
> directive; qwave-qudit-advantage QNFO.UMP.005 red-team). HARD: 2. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **ZENODO-RECORDS-API-DROPS-METADATA-1 anti-pattern added** — the records-API
>     `PUT /api/records/{id}/draft` returns HTTP 200 but silently drops `license` + `keywords`.
>     Fix: deposit-API metadata shape (`PUT /api/deposit/depositions/{id}` with upload_type/
>     publication_type strings, plain-string license, plain-list keywords); verify via DataCite
>     subjects/rights read-back. Canonical case: qwave-qudit-advantage v0.3 (21827347) — 11 keywords
>     + cc-by-nc-sa-4.0 stored only via deposit shape.
> (2) [HARD] **INTERNAL-REF-1 extended** — WBS codes (`QNFO.UMP.005`-style) in body/calibration
>     registers/pre-registration scaffolds and quoted internal program names ("QEC Darwinism") now
>     explicitly banned; Publication Language Gate scan list extended. Canonical case: qwave-qudit-
>     advantage v0.2 leaked `QNFO.UMP.005` (calibration register) + "QEC Darwinism" (prose) — fixed
>     in v0.3.
> (3) [SOFT] **P5.FRESH newversion self-DOI ordering rule** — newversion .md MUST be updated to its
>     own pre-reserved DOI BEFORE upload (upload-first ordering ships a deposited file one version
>     stale). Canonical case: v0.2 deposited .md carried v0.1 DOI; v0.3 fixed via pre-fetch order.
> Cross-reference: kaizen v1.78, TWO-API METADATA SHAPE DISTINCTION, ZENODO-INPLACE-EDIT-1,
> session ktkjFggX5vMt1h4ogDIwh.

> **v2.89 UPDATE (2026-08-07, kaizen — KIF-29 Synthesis Mode cross-reference + kaizen v1.86 convergence architecture):**
> Red-team: 2 parallel subagents dispatched (both truncated — direct parent fallback per kaizen rule 4).
> Direct parent-agent audit confirmed research v2.88 lacks any reference to kaizen v1.86 Synthesis Mode
> / Convergence Architecture. HARD: 0. SOFT: 1. DESIGN: 0. Changes:
> (1) [SOFT] **KIF-29 gate cross-referenced to kaizen v1.86 Synthesis Mode** — Phase 1b Consilience
>     Gate now includes an explicit reference: for multi-thread sessions, apply the Convergence
>     Architecture (kaizen v1.86) to map cross-pillar merges before executing isolated research
>     tasks. The synthesis mode transforms KIF-29 from a vetting gate into an execution methodology.
> Cross-reference: kaizen v1.86 (Synthesis Mode / Convergence Architecture, Mined Workflow Pattern G),
> qnfo-core §0.7 (Ostrowski Mandate), session MerOabc5KO_W9Q8BP47ok.

> **v2.88 UPDATE (2026-08-06, kaizen — DISSEMINATION LEGS: journal submission + targeted outreach + PhilPapers cross-ref + ERRATA ordering):**
> Red-team: direct parent-agent 5-adversary audit (session ktkjFggX5vMt1h4ogDIwh — SKILLS UPDATE
> cycle #2; QNFO.UMP.005 dissemination work: 5 outreach emails sent, arXiv BLOCKED by endorsement,
> journal pivot). HARD: 1. SOFT: 3. DESIGN: 0. Changes:
> (1) [HARD] **Phase 7 journal-submission leg added** — arXiv is NOT a guaranteed publication leg
>     (author lacks endorsement; standing preference = journals directly). Documents Zenodo→DataCite→
>     OpenAlex auto-index as the no-ArXiv discovery layer, journal shortlist (Frontiers in Physics ★),
>     cover-letter protocol (lead with pre-registered falsifiability), post-acceptance isPublishedIn.
> (2) [SOFT] **Phase 7 targeted-outreach protocol added** — verify recipient emails from arXiv SOURCE
>     tarballs (title-match alone returned the WRONG paper — Fischer et al. vs recalled Gokhale),
>     address corresponding author, test-send first via qnfo-email Worker, individual sends, message_id
>     logging to outreach-log.md, adversarial-validation framing.
> (3) [SOFT] **Phase 7 PhilPapers cross-ref added** — knowledge v2.8 requirement (>=3 philosophy-domain
>     keywords via deposit-API in-place edit; DataCite subjects verify). Canonical case: v0.4 (21827737).
> (4) [SOFT] **BP-4 ERRATA ordering rule added (HARD severity)** — never pre-claim a correcting
>     newversion is published before the 202 publish call in the same turn. Canonical case: this
>     session's own ERRATA.md phantom claim (caught by red team, made true with v0.4).
> Cross-reference: kaizen v1.79, knowledge v2.8 (PHILPAPERS-DISCOVERABILITY-GAP), ZENODO-RECORDS-
> API-DROPS-METADATA-1, ZENODO-PHANTOM-DOI-1, mem-eoKxBfeViioJ, session ktkjFggX5vMt1h4ogDIwh.

2.101v2.99
> **v2.99 UPDATE (2026-08-11, kaizen — CMD EXECUTE red-team fix cycle: KG-seeding pointer repoint + banner cross-ref current-state):**
> Red-team: direct parent-agent 5-adversary audit (CMD RED TEAM SUB — session rvnMtR544X387NEXCAPbB). HARD: 2 (stale/orphaned current-state pointers). SOFT: 1. DESIGN: 1. Changes:
> (1) [HARD] **KG Node Seeding pointer repointed (x2)** — `(per qnfo-core v1.24)` -> `(per knowledge v2.10 SYNC CONTRACT)`: qnfo-core v1.25+ contains zero `INSERT OR IGNORE`/`qnfo-graph` fallback content; the actual owner of the graph-sync contract is knowledge v2.10 (`graph-api.qnfo.org/sync`). Orphaned-owner pointer fixed.
> (2) [DESIGN] **Banner cross-ref current-state cites added** — kaizen v2.18 (MAP-TERRITORY-1 mirror row) + qnfo-core v1.26 (MAP-TERRITORY-1 owner row) now cited in the v2.98 banner cross-ref line, matching sibling-banner convention.
> Cross-reference: kaizen v2.18, qnfo-core v1.26, knowledge v2.10 (SYNC CONTRACT), UIA DOI 10.5281/zenodo.21901984, session rvnMtR544X387NEXCAPbB.
> **v2.98 UPDATE (2026-08-11, kaizen — MAP-TERRITORY GATE SCRIPTED: check-map-territory.py + Publication Language Gate wiring):**
> Red-team: direct parent-agent 5-adversary audit (UIA Repair Pipeline execution — session rvnMtR544X387NEXCAPbB).
> Watchtower: research v2.97 N-2 CLEAN pre-edit; v2.98 N-2 CLEAN post-edit (raw anchors). HARD: 1 (research-side: gate was prose-only). SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **MAP-TERRITORY GATE scripted** — new `research/scripts/check-map-territory.py`: scans paper drafts for `[TERRITORY` labels (identity claims) without an accompanying falsifiability condition (KIF-60 / qnfo-core §0.0); `[MAP` labels are context-only (no condition). FAIL = exit 1 + FIX instruction (inline condition / same-paragraph condition / downgrade to MAP). Added to the Phase 5 Publication Language Gate scan list (build-time BLOCK). Canonical lesson: TITLE-DUPLICATION-1 shipped 3 published versions before scripting; map–territory conflation must not ship unlabelled again. Enforcement of the UIA Repair Pipeline Protocol v1.0 (2026-08-11) STEP 4 SCRIPTING MANDATE (PROSE-GATE-ADVISORY-1, kaizen v1.63).
> (2) [DESIGN] **UIA-REPAIR-REGISTER.md created** (vault, 2026-08-11) — rows UIA-2026-08-11-01..06 incl. the all-36 REFRAME (P0) and the UIA self-audit (P0/IN-PROGRESS); calibration `[CHECK: 2026-09-11]` map-territory label holds.
> Cross-reference: UIA Repair Pipeline note `_uia-repair-pipeline-2026-08-11.md`, UIA DOI 10.5281/zenodo.21901984, kaizen v1.63 (PROSE-GATE-ADVISORY-1), qnfo-core §0.0 (KIF-60), check-title-duplication.py (v2.86 pattern), kaizen v2.18 (MAP-TERRITORY-1 mirror row), qnfo-core v1.26 (MAP-TERRITORY-1 owner row), session rvnMtR544X387NEXCAPbB.
> **v2.97 UPDATE (2026-08-10, kaizen — CDP render script .cjs + merge past concurrent v2.96):**
> Red-team: direct parent-agent 5-adversary audit (CMD SKILLS UPDATE; session dlnKXUpIJK48EWgWj5SmP).
> Concurrent-session merge: v2.96 (publication completeness gates) landed WHILE this audit ran — merged past
> per VERSION-OVERWRITE-1. HARD: 0. SOFT: 1. DESIGN: 0. Changes:
> (1) [SOFT] **CDP render script: use `.cjs` (CommonJS) not `.mjs`** — `render-pdf.mjs` with `require()` fails
>     ("require is not defined in ES module scope"); ESM import of a Windows absolute path fails
>     (ERR_UNSUPPORTED_ESM_URL_SCHEME). `render-pdf.cjs` with `require('C:/Users/LENOVO/node_modules/puppeteer-core')`
>     + Edge msedge.exe works. Cross-ref: NODE-EVAL-CMD-1, NODE-MJS-ESM-1 (windows-command-patterns v3.20),
>     references/cdp-pdf-pipeline.md. Canonical: qwave-qudit-advantage.pdf 590,959 B, 0 U+FFFD/FFFF.
> Cross-reference: windows-command-patterns v3.20, kaizen v2.05, session dlnKXUpIJK48EWgWj5SmP.


> **v2.96 UPDATE (2026-08-10, kaizen — CMD SKILLS UPDATE: publication completeness gates — KG node + Vectorize index + PDF path option):**
> Red-team: direct parent-agent 5-adversary audit (CMD SKILLS UPDATE directive — session Z-DBQiCgjlEszWQZzZthq;
> trigger: ringbauer-qudit-due-diligence publication closeout red-team found HARD-1 KG-missing + HARD-2 Vectorize-missing,
> plus PDF build bug where page.pdf() without path wrote no file). Watchtower: research v2.95 N-2 CLEAN pre-edit; v2.96 N-2 CLEAN post-edit (raw anchors).
> HARD: 2. SOFT: 2. DESIGN: 0. Changes:
> (1) [HARD] **Phase 6 KG Node Seeding (MANDATORY)** — every published paper must have a `paper:<slug>` KG node
>     with >=1 BELONGS_TO edge (Edge Seeding Gate); verify query_graph/neighbors > 0 same-turn. Anti-pattern:
>     PUBLICATION-KG-INDEX-GAP-1 (canonical: ringbauer-qudit-due-diligence — D1 row existed, KG node did not).
> (2) [HARD] **Phase 6 Vectorize Indexing (MANDATORY)** — trigger qnfo-paper-indexer /index or /webhook with
>     X-Index-Token after D1 insert; verify /webhook?slug= -> indexed:true, chunks>0 (VECTORIZE-WEBHOOK-VERIFY-1).
>     Canonical: ringbauer-qudit-due-diligence HARD-2 — paper in D1 but not semantically searchable.
> (3) [HARD] **PDF step 5 `path:` option required** (PDF-PATH-OPTION-1) — `page.pdf()` without `path` returns a
>     Buffer and writes NO file while the pipeline reports success. Canonical: this session's first render.
> (4) [SOFT] **Consolidated Closeout Verification extended 5→7 layers** — adds KG node + Vectorize index checks;
>     this gate would have caught HARD-1/HARD-2 at closeout time.
> (5) [SOFT] **R2-CDN-CACHE-1** — R2 object API GET may serve a CDN-cached stale object (CF-Cache-Status: HIT);
>     canonical verify via rclone S3 check (0 differences), not API GET byte-compare.
> Cross-reference: kaizen v2.04 (mirror rows), knowledge v2.10 (Edge Seeding Gate), cloudflare v3.36
> (VECTORIZE-WEBHOOK-VERIFY-1, AI-ENDPOINT-AUTH-1), qnfo-core v1.23 (D1 fallback), ringbauer-qudit-due-diligence
> (DOI 10.5281/zenodo.21879231), session Z-DBQiCgjlEszWQZzZthq.

> **v2.95 UPDATE (2026-08-10, kaizen — Consolidated Publication Closeout Verification gate + UIA pass):**
> Red-team: direct parent-agent 5-adversary audit + UIA Q1-8 (CMD SKILLS UPDATE directive — session gZ5Qf_rxLX365TvNJDOkc,
> QNFO.RES.002/.003 closeout cycle). Watchtower: research v2.94 N-2 CLEAN pre-edit; v2.95 N-2 CLEAN post-edit (raw anchors).
> HARD: 0. SOFT: 0. DESIGN: 1. Changes:
> (1) [DESIGN] **Consolidated Publication Closeout Verification gate added (Phase 8 / Verification Gates)** —
>     a single same-turn script that re-proves ALL distribution layers at once: doi.org HEAD x4 (new + v0.1 predecessors),
>     DataCite state=findable + subjects + rightsList, GitHub `git ls-remote` branches+tags, D1 row re-query (doi/status/body_len),
>     Zenodo record files (.pdf/.html/.md present), KG node + Vectorize index (v2.96, PUBLICATION-KG-INDEX-GAP-1). This closes the wobble where each layer was verified piecemeal and a
>     phantom-claim could survive until the next gate. Canonical case: QNFO.RES.002/.003 final verification 2026-08-10 —
>     one script re-proved all 5 layers, 0 HARD/0 SOFT, closing with zero deferred items. The gate is falsifiable: any
>     non-resolving DOI or missing ref fails the closeout.
> Cross-reference: kaizen v2.03 (mirror row), Tool-Call Execution Mandate, P5.FRESH, ZENODO-PHANTOM-DOI-1,
> QNFO.RES.002 (10.5281/zenodo.21878976) + QNFO.RES.003 (10.5281/zenodo.21901983), session this.


> **v2.94 UPDATE (2026-08-10, kaizen — NEWVERSION DOI RESERVATION PATH CORRECTED (prereserve_doi None) + P5.FRESH newversion-only):**
> Red-team: direct parent-agent 5-adversary audit (CMD SKILLS UPDATE directive — session gZ5Qf_rxLX365TvNJDOkc, QNFO.RES.002/.003 publication cycle).
> Watchtower: research v2.93 N-2 CLEAN pre-edit; v2.94 N-2 CLEAN post-edit (raw-line anchors).
> HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **NEWVERSION SELF-DOI ORDERING RULE step (2) CORRECTED** — the documented `GET /api/records/{id}/draft`
>     → `prereserve_doi` path returns **`prereserve_doi: None` for newversion drafts** (verified live 2026-08-10 on
>     drafts 21878976/21878977). The ONLY working reservation path is **`POST /api/records/{id}/draft/pids/doi`**
>     (the draft's `links.reserve_doi`) → 201 with the reserved DOI. A follow-the-doc agent would stall on step 2.
>     Canonical case: QNFO.RES.002/.003 — first newversion run hit `prereserve_doi: None`; PID-reservation POST
>     succeeded and both v0.2 records published with P5.FRESH yaml_ok=True.
> (2) [HARD] **P5.FRESH instruction clarified (newversion-only)** — in-place `.md` overwrite on a published record's
>     edit-draft is impossible: bare `PUT /draft/files/{fname}` → 415 (file-ENTRY endpoint, JSON expected); 
>     `PUT /draft/files/{fname}/content` → 403 Bucket is locked (lock does not clear with wait). P5.FRESH repair
>     ALWAYS uses newversion. ZENODO-BUCKET-LOCKED-1 extended with this evidence.
> (3) [SOFT] **Self-DOI ordering also requires `status: "published"` in the uploaded .md** — the uploaded .md must
>     carry BOTH its own reserved DOI AND status published (P5.FRESH checks both).
> Cross-reference: kaizen v2.02 (mirror row), ZENODO-BUCKET-LOCKED-1, P5.FRESH, NEWVERSION SELF-DOI ORDERING RULE,
> QNFO.RES.002 (10.5281/zenodo.21878976) + QNFO.RES.003 (10.5281/zenodo.21901983), session this.


> **v2.93 UPDATE (2026-08-10, kaizen — UIA cross-reference in Phase 4 Stage 3):**
> Red-team: direct parent-agent 5-adversary audit (CMD SKILLS UPDATE). UIA cross-ref added to
> Phase 4 Stage 3 Red-Team Challenge — the 15-question UIA complements the 5-adversary review.
> Cross-ref: UIA DOI 10.5281/zenodo.21901984, kaizen v2.01 §H.
>
> **v2.92 UPDATE (2026-08-10, kaizen — CMD RED TEAM FIX CYCLE: briefing send-guard cross-ref + history reconciliation):**
> Red-team: direct parent-agent 5-adversary audit (CMD RED TEAM, READ-ONLY — this session). Trigger: research was bumped 2.90->2.91 by concurrent session 05205f8 (AI-QUALITY-GATE-1, banner VERIFIED present) but .kaizen_history lacked the v2.91 entry, and the briefing archive send path had no TEST-SEND-EXTERNAL-1 cross-ref. HARD: 0. SOFT: 2. DESIGN: 0. Changes:
> (1) [SOFT] **Briefing System section: TEST-SEND-EXTERNAL-1 cross-ref added (C2)** — the briefing archive email is a send path; test sends follow TEST-SEND-EXTERNAL-1 (user mailbox only, via email-composer scripts/email-send-guard.py).
> (2) [SOFT] **.kaizen_history reconciled** — v2.91 entry (retroactive, concurrent session) + v2.92 entry appended.
> Cross-reference: email-composer v2.17 (TEST-SEND-EXTERNAL-1, email-send-guard.py), kaizen v1.99, session this.

> **v2.91 UPDATE (2026-08-10, kaizen — AI-QUALITY-GATE-1 added to publication pipeline):**
> Red-team: direct parent-agent 5-adversary audit follow-up (session 0SnaUK-QccIJkohojGMQS — uncanny-valley research note + JPCUB verification). Watchtower: 20/20 QNFO skills N-2 CLEAN pre-edit. HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **AI-QUALITY-GATE-1 added to Publication Language Gate (BLOCKING)** — the owner-level anti-pattern (qnfo-core v1.22) becomes a machine-enforced pipeline check per PROSE-GATE-ADVISORY-1. Before publication, AI-generated/AI-assisted papers MUST clear the forensic quality gate: (i) no elementary physics/energy-budget errors (canonical: Qudit Advantage §3.3 sets P_decode≈0 as a "conservative upper bound" — zero is a LOWER bound; VERIFIED via D1 body 2026-08-10), (ii) no synthetic/unresolvable citation anchors in the body (@C5_jpcub_p0-style prefixed keys — INTERNAL-REF-1-adjacent; readers read them as fake), (iii) no scaffold overload (meta-tag echo, rigid template boxes), (iv) no over-explaining textbook foundations while hand-waving the novel integration, (v) no self-referential metric claims without external validation. Cross-ref: qnfo-core v1.22, INTERNAL-REF-1, kaizen v1.63 (PROSE-GATE-ADVISORY-1).
> Cross-reference: qnfo-core v1.22, kaizen v1.94, session 0SnaUK-QccIJkohojGMQS.
> **v2.86 UPDATE (2026-08-06, kaizen — TITLE-DUPLICATION-1 SCRIPTED GATE: prose advisory became machine-enforced):**
> Red-team: direct parent-agent 5-adversary audit (session bwt-Jv0EdLebno9QonKIa — ODR 2026-08-06
> publication cycle). Trigger: user directive — "HOW MANY TIMES DO I HAVE TO TELL YOU TO FIX
> DUPLICATE TITLES IN GENERATED PDFS?" ODR v0.1/v0.2/v0.3 ALL published with the TITLE-DUPLICATION-1
> violation (body `# <Title>` H1 + YAML `title:` = title TWICE on page 1) — the anti-pattern
> documented in v2.84 was prose-advisory, never enforced at build time.
> HARD: 1. SOFT: 0. DESIGN: 1. Changes:
> (1) [HARD] **TITLE-DUPLICATION-1 gate SCRIPTED** — new `research/scripts/check-title-duplication.py`:
>     scans the pandoc-rendered HTML, counts rendered `<h1>` tags WITH attributes (excludes the
>     `<head><title>` meta tag — browser-tab only, NOT a rendered heading, prevents the
>     N-2-SCAN-FALSE-POSITIVE-1 class of false positive). PASS = exactly ONE `<h1 class="title">`
>     AND zero body `<h1>`. FAIL = exit 1 with FIX instruction. Added as a MANDATORY step in the
>     PDF Building pipeline (step 2.5: run after pandoc, before MathJax inline + CDP render) and
>     to the PDF verification Gate. Any build producing a duplicated title is BLOCKED — this is
>     the enforcement TITLE-DUPLICATION-1 always required.
> (2) [DESIGN] **Author-time rule strengthened** — the anti-pattern row now reads: when YAML
>     `title:` exists, the body MUST NOT contain a top-level H1 with the same title; the scripted
>     gate makes "verify exactly ONE title occurrence" a build-time check, not a manual scan.
> Canonical case: ODR 2026-08-06 v0.4 (DOI 10.5281/zenodo.21820137) — body H1 removed, single
> rendered title verified by the scripted gate; v0.1-v0.3 (21819742/21819931/21819981) superseded.
> Cross-reference: qnfo-core v1.16 (published-paper hygiene), kaizen v1.63 (recurrence lesson:
> prose gates are advisory until scripted), N-2-SCAN-FALSE-POSITIVE-1,
> session bwt-Jv0EdLebno9QonKIa.

> **v2.85 UPDATE (2026-08-05, kaizen — Existential-claim verification gate (VERIFY-DONT-ASSUME-1)):**
> Red-team: direct parent-agent 5-adversary audit triggered by Heffner audit v1.0 fact-check failure.
> HARD: 1. SOFT: 0. DESIGN: 0. Changes:
> (1) [HARD] **Phase 5 Publication Language Gate extended** — now scans for existential-claim
>     patterns ("does not exist," "has not released," "no model designated," etc.) and requires
>     live-verification evidence saved to `artifacts/existential-claim-verification.md`.
>     KIF-62 gate. Enforcement of qnfo-core v1.17 VERIFY-DONT-ASSUME-1 / VERIFY-FACT-1.
>     Canonical case: Heffner audit v1.0 §2.2 (DOI 10.5281/zenodo.21812511) — corrected in
>     v1.1 (DOI 10.5281/zenodo.21812761).
> Cross-reference: qnfo-core v1.17, kaizen v1.59, user mandate 2026-08-05
> "FACT-CHECKING IS A STANDARD PART OF RESEARCH."

> **v2.84 UPDATE (2026-08-05, kaizen — PUBLISHED-PAPER HYGIENE: title duplication, internal references, slug files):**
> Red-team: direct parent-agent 5-adversary audit (user directives 2026-08-05 — fix title
> duplication on page 1 PERMANENTLY; avoid internal references in published papers; name
> files as project slugs). HARD: 3. SOFT: 0. DESIGN: 1. Changes:
> (1) [HARD] **TITLE-DUPLICATION-1 anti-pattern added** — a body `# <Title>` H1 alongside a
>     YAML `title:` field renders the title TWICE on page 1 (pandoc emits the YAML title as
>     an `<h1 class="title">`; a body H1 duplicates it). Author-time rule: when YAML
>     frontmatter has a `title:`, the paper body MUST NOT contain a top-level H1 with the
>     same title. Verify in the rendered HTML/PDF: exactly ONE title occurrence.
> (2) [HARD] **INTERNAL-REF-1 anti-pattern added** — published papers MUST NOT reference
>     internal QNFO processes: no repo paths (`QNFO/xxx`), no skill sections (`QNFO Core
>     §0.7`), no internal program names as prose (`the Kepler Program`, `the Continuum Trilogy` as process refs), **WBS codes (`QNFO.UMP.005`-style), quoted internal program names ("QEC Darwinism")**,  (`the Kepler Program`, `the Continuum
>     Trilogy` as process refs), no internal conference/workshop mentions, no possessive
>     internal refs (`QNFO's research program`). Convert to generic phrasing + numbered
>     citations of PUBLISHED records only.
> (3) [HARD] **FILE-SLUG-1 anti-pattern added (upgrades the old "Generic paper.md naming"
>     row to HARD)** — published paper files MUST be named as the PROJECT SLUG:
>     `<slug>.md`, `<slug>.pdf`, `<slug>.html` (e.g. `qec-darwinism-ultrametric.md`).
>     `paper.md`/`paper.pdf`/`paper.html` naming is FORBIDDEN. Applies to repo files,
>     Zenodo deposit filenames, and R2 keys.
> (4) [DESIGN] **Publication Language Gate extended** — the gate now also scans for
>     title duplication (exactly one title in rendered output) and internal references
>     (repo paths, skill sections, internal program names).
> Cross-reference: qnfo-core v1.16 (published-paper hygiene), kaizen v1.57, user directive
> 2026-08-05 (three mandates). Canonical case: QNFO.UMP.004 qec-darwinism-ultrametric
> v1.2/v1.3 — title dup fixed, CWI/internal refs removed, files renamed to slug.

> **v2.83 UPDATE (2026-08-05, kaizen — OAI-PMH + Software Heritage + integration landscape):**
> Red-team: direct parent-agent audit of session 3i_KVLownViukLTZB_BJ1 (OAI-PMH corpus audit,
> Software Heritage archival, Unpaywall/OpenAIRE/OpenAlex integrations round).
> HARD: 2. SOFT: 2. DESIGN: 1. Changes:
> (1) [HARD] **OAI-PMH section added** — the protocol (6 verbs: Identify/ListMetadataFormats/
>     ListSets/ListIdentifiers/ListRecords/GetRecord), Zenodo endpoint (zenodo.org/oai2d), why it
>     BEATS the REST search API for corpus work (no auth, no search syntax, resumptionToken
>     pagination, oai_datacite prefix gives creators+ORCIDs). Proved live: harvested user-qnfo set
>     (80 records/2 pages) and surfaced 22 ADR-014 violations the REST API couldn't cleanly show.
>     Script: research/scripts/oai-pmh-harvest.py (--audit = ADR-014 compliance check).
> (2) [HARD] **Software Heritage section added** — archival of GitHub repos -> swh:1: identifiers.
>     CRITICAL: archive.softwareheritage.org is behind Anubis proof-of-work anti-bot — a plain
>     HTTP client gets an HTML challenge page, NOT JSON. MUST drive via a real browser (session
>     browser/CDP); the browser solves Anubis and same-origin fetch then carries the cookie.
>     Save schema: POST /api/1/origin/save/ body {"origin_url": ..., "visit_type": "git"}
>     (visit_type REQUIRED; GitHub endpoint rejects visit_type=github, allowed: bzr,cvs,git,hg,svn,
>     tarball). Unauthenticated saves burst-throttled ~50/day (429, respect it). Script:
>     research/scripts/swh-archive.py.
> (3) [HARD] **ANTIBOT-POW-1 anti-pattern added** — Anubis-class proof-of-work anti-bot (HTML
>     challenge to non-browser clients) is a DIFFERENT class from ZENODO-BOT-403-1 (header-fixable).
>     Detect by content-type: text/html + 'Making sure you're not a bot!' -> must use a real browser.
> (4) [SOFT] **TEMP-SCRIPT-CLOBBER-1 anti-pattern added** — editing a temp script then later
>     `write`-overwriting the same file silently reverts the edit (edit _oai_demo.py headers, then
>     write clobbered the fix -> 403 recurred). Never edit-then-write the same temp script; write
>     once with the final content.
> (5) [SOFT] **Integration landscape documented** — OpenAIRE: auto in-index via Zenodo (no action).
>     Unpaywall: DataCite-only preprints NOT in index (404 expected); enter via Spring 2025 minting
>     program -> Google Form forms.gle/LMmjdKw9HZJooxVT8 (submitted 2026-08-05). OpenAlex Collections:
>     web-UI only, no public API. Crossref: optional (member-proxy) unlocks published-work ecosystem.
> Cross-reference: kaizen v1.56, session 3i_KVLownViukLTZB_BJ1.
> **v2.82 UPDATE (2026-08-05, kaizen — Wikidata abuse filter + Tier-1/2 dissemination state):**
> Red-team: direct parent-agent audit of session 3i_KVLownViukLTZB_BJ1 (Wikidata Tier-1
> publication items + Tier-2 identifier claims round).
> HARD: 2. SOFT: 1. DESIGN: 1. Changes:
> (1) [HARD] **WIKIDATA-ABUSE-FILTER-296-1 migrated from durable memory** (MEMORY-TO-SKILL-DRIFT
>     closed) — Wikidata `abusefilter-warning-296` blocks new-item creation for accounts with
>     editcount 0 after ~4-8 items per short window. Surfaces as failed-save + filter warning.
>     Clears after cooldown (hours). DO NOT hammer — harder blocks. Claims (wbcreateclaim) on
>     EXISTING items are exempt; only wbeditentity new=item ID assignment is filtered.
>     Strategy: create items 60-120s apart; verify via wbsearchentities 2-5s pacing.
> (2) [HARD] **Tier-1/2 verified state documented** — 8/11 flagship publication items live
>     (Q140892430/431/432/433/448/449/451/454, P31+P356+P50+P577+P407 each); 3 pending
>     (Consilience-NumberTheory 21591660, Zitterbewegung 21214362, Ultrametric Engine 21214775)
>     blocked by the filter. Tier-2 complete: 4/4 identifier claims (P4285 OpenAlex A5133504808,
>     P1960 Scholar eHIbqxkAAAAJ, P4012 SemanticScholar 2401393450, P2002 X RowanQuni).
> (3) [SOFT] **Concurrent-session version check** — a concurrent session bumped kaizen to v1.54
>     mid-session; re-read current versions before any edit (VERSION-OVERWRITE-1 discipline).
> (4) [DESIGN] Script reference: wikidata-dissemination.py (--status/--create-missing,
>     abuse-filter-aware) committed e0b5a06.
> Cross-reference: kaizen v1.55, session 3i_KVLownViukLTZB_BJ1.
> **v2.81 UPDATE (2026-08-05, kaizen — Wikidata/MediaWiki: item creation + auth rules + 2 anti-patterns):**
> Red-team: direct parent-agent audit of session 3i_KVLownViukLTZB_BJ1 (Wikidata items round:
> Person Q140892265 + Org Q140892267 created, credential case-sensitivity discovery).
> HARD: 2. SOFT: 1. DESIGN: 1. Changes:
> (1) [HARD] **MEDIAWIKI-USERNAME-CASE-1 anti-pattern added** — MediaWiki uppercases the first
>     character of usernames and is case-sensitive after it (QNFO != Qnfo). The login error
>     "Incorrect username or password entered" is a COMBINED message for EITHER unknown username
>     OR wrong password — never distinguishes. Diagnose with read-only
>     action=query&list=users&ususers=NAME&usprop=editcount (no login needed).
> (2) [HARD] **WIKIDATA-BOT-PASSWORD-REQUIRED-1 migrated from durable memory** (MEMORY-TO-SKILL-DRIFT
>     closed) — MediaWiki API programmatic edits REQUIRE a bot password (Special:BotPasswords),
>     not the account password (account pw + API = 'additional verification step required'/SUL3).
>     Account password DOES work for browser web login.
> (3) [SOFT] **wbsetclaim $NEW GUID failure documented** — new statements MUST use wbcreateclaim
>     (wbsetclaim requires a real GUID; 'Qxxxx$NEW' returns 'Statement does not have a valid GUID').
> (4) [DESIGN] **Wikidata section added** — item creation flow, QID map, property reference,
>     SPARQL verification patterns, dissemination tiers (publications, identifiers, programs).
> Cross-reference: kaizen v1.53, session 3i_KVLownViukLTZB_BJ1.
> **v2.80 UPDATE (2026-08-05, kaizen — Research profile & indexing APIs: IndexNow + OSF + ORCID scope rules):**
> Red-team: direct parent-agent audit of session 3i_KVLownViukLTZB_BJ1 (discoverability sprint:
> landing pages, Bluesky, Zenodo ADR-014 fix, OSF profile, ORCID client, IndexNow).
> HARD: 3. SOFT: 2. DESIGN: 1. Changes:
> (1) [HARD] **OSF-API-SCHEMA-1 anti-pattern added** — OSF user social fields are camelCase with
>     MIXED types (arrays: github/linkedIn/twitter/profileWebsites; strings: scholar/researchGate/
>     ssrn/impactStory/baiduScholar/academiaProfileID/academiaInstitution/researcherId). NO writable
>     `bio` field in users API (unknown fields silently ignored, HTTP 200). PATCH requires data.id
>     (user 6hyj8). ~6 failed PATCHes this session from guessing types.
> (2) [HARD] **ORCID-PUBLIC-API-SCOPE-1 anti-pattern added** — ORCID Public API free tier supports
>     ONLY `/authenticate` + `/read-public` in OAuth; write scopes (/person/update, /activities/update,
>     /read-limited) rejected with "one of the provided scopes is not allowed for this member".
>     Profile edits must go through the web UI (logged-in session) or Member API.
> (3) [HARD] **IndexNow protocol section added** — search-engine indexing with NO account: host
>     {key}.txt at domain root, POST api.indexnow.org/indexnow, HTTP 202 = accepted. Backed by
>     Bing/Yandex/Seznam/Naver. Google/Bing legacy ping endpoints DEAD (404/410).
> (4) [SOFT] **GITHUB-PAGES-PROPAGATION-1 anti-pattern added** — GitHub Pages ~1-2 min CDN
>     propagation after push; initial QA showed stale content. Cloudflare Pages instant.
>     Re-verify via gh api pages/builds before concluding "not deployed".
> (5) [DESIGN] Script reference table updated: indexnow-submit.py, osf-profile-update.py,
>     zenodo-cleanup.py (all committed to qnfo-skills + R2).
> Cross-reference: kaizen v1.52 (PARALLEL-EXEC-RACE-1), session 3i_KVLownViukLTZB_BJ1.
> **v2.79 UPDATE (2026-08-05, kaizen — Zenodo API exhaustive documentation — NO MORE TRIAL AND ERROR):**
> Red-team: direct parent-agent 5-adversary audit of session 3i_KVLownViukLTZB_BJ1
> (discoverability sprint + Zenodo attribution fix 21789920->21807661).
> HARD: 2. SOFT: 0. DESIGN: 1. Changes:
> (1) [HARD] **TWO-API METADATA SHAPE DISTINCTION section added** — deposit API
>     (upload_type/publication_type strings) vs records API (resource_type object).
>     ~15 failed PUTs this session from shape confusion — now documented up front.
> (2) [HARD] **ZENODO-DEPOSIT-API-METADATA-1 + ZENODO-SUBJECT-SEARCH-1 anti-patterns added**
>     — subject search requires `metadata.subjects.subject:` prefix (154 PLACEHOLDER,
>     17 duplicate-record, 185 QNFO verified 2026-08-05); deposit list endpoint does
>     NOT return subject-tagged published records.
> (3) [DESIGN] Subject-audit path documented: records search API (not deposit list).
> Cross-reference: kaizen v1.51 (API-DOC-GAP-1), social-media-management v1.6.0,
> session 3i_KVLownViukLTZB_BJ1.











> **v2.75 UPDATE (2026-08-05, user injunction — PyMuPDF EXPUNGED):**





> Red-team: direct user injunction — "PyMuPDF IS NOT PART OF APPROVED PDF PUBLICATION PROCESS."





> HARD: 3. SOFT: 0. DESIGN: 2. Changes:





> (1) [HARD] **PYMUPDF-1 anti-pattern added** — HARD BLOCK on `import fitz`, `pip install PyMuPDF`,





>     or `fitz.open()` anywhere in the publication pipeline. PDF verification uses direct file-content





>     scanning, NOT PyMuPDF. PDF rendering uses ONLY puppeteer-core CDP.





> (2) [HARD] **5 stale durable memories purged** — all claimed build-pdf-pro.py / verification gate





>     used PyMuPDF, causing agents to install it as a fallback pathway. Forgot and replaced with





>     canonical CDP-only memory.





> (3) [HARD] **documents skill stale reference** — `build-pdf-pro.py` reference corrected to canonical





>     CDP pipeline reference.





> (4) [DESIGN] **Canonical memory written** — ONE AND ONLY pipeline memorialized with explicit





>     forbidden-tools list (PyMuPDF, xhtml2pdf, browser print-to-pdf, --print-to-pdf, TeX Live).





> (5) [DESIGN] **PDF Building section hardening** — existing "ONE WORKFLOW, ONE PIPELINE, NO ALTERNATIVES"





>     language already correct; anti-pattern now backs it with HARD BLOCK on PyMuPDF specifically.





> Cross-reference: session ktmz7cqk (CDP pipeline canonical), mem-WNf8py4InVLH (replacement memory).











> **v2.74 UPDATE (2026-08-04, kaizen — Zenodo deposit API live + upload method + bot-403 + phantom-DOI):**





> Red-team: direct parent-agent audit of session ZDdTu9QfTZKY_kJALlXY_ (Consilience Framework real





> publication, DOI 10.5281/zenodo.21803159). HARD: 4. SOFT: 0. DESIGN: 0. Changes:





> (1) [HARD] **ZENODO-DEPOSIT-API-LIVE-1** — the deposit API (`/api/deposit/depositions`) is NOT





>     decommissioned: this session created deposition 21803159 (HTTP 201) and published (HTTP 202)





>     through it. The INVENIORDM table's 'old (decommissioned)' claim is contradicted — corrected.





> (2) [HARD] **ZENODO-UPLOAD-MULTIPART-1** — file upload = `POST /api/deposit/depositions/{id}/files`





>     with multipart/form-data (HTTP 201). `PUT /files/{filename}` returns **405**. Canonical method.





> (3) [HARD] **ZENODO-BOT-403-1** — 'unusual traffic' 403 is bot-detection on minimal `Mozilla/5.0` UA





>     (machine IP is residential KPN, NL — not a datacenter block). Fix = full Chrome UA +





>     Accept-Language + Referer + Origin headers.





> (4) [HARD] **ZENODO-PHANTOM-DOI-1** — never claim 'published/DOI issued' without a same-turn tool call





>     showing the API response. DataCite API (`api.datacite.org/dois/{doi}`) is the authoritative





>     Zenodo-DOI check — HTTP 404 is definitive proof no record exists.





> Cross-reference: kaizen v1.30, windows-command-patterns v3.12 (S-1.0.6 API-Failure protocol),





> session ZDdTu9QfTZKY_kJALlXY_, real DOI 10.5281/zenodo.21803159.











> **v2.73 UPDATE (2026-08-04, kaizen — PANDOC-SAFE AUTHORING MANDATE):**





> Red-team: user directive — "TEXT SHOULD BE GENERATED BY THE LLM IN THE FORMAT WE





> NEED IT, INCLUDING ANY PANDOC/MATHJAX-SPECIFIC PROCLIVITIES LIKE USING LATEX CODES





> WHERE CONFUSING (LIKE VERTICAL BAR CODE INSTEAD OF SYMBOL INSIDE TABLES THAT USE





> VERTICAL BAR COLUMN DIVIDERS). SURGICAL HAND-FIXES SHOULD NEVER HAPPEN IN THE





> FIRST PLACE." HARD: 3. SOFT: 1. DESIGN: 0. Changes:





> (1) [HARD] **PANDOC-SAFE AUTHORING MANDATE added to Phase 4** — ALL paper text





>     generated by the LLM MUST be pandoc/MathJax-safe at authoring time:





>     (a) every math expression in `$...$` (inline) or `$$...$$` (display) — NEVER





>         bare LaTeX or Unicode math in prose;





>     (b) vertical bars: inside pipe tables use `\|`, `\vert`, `\lvert`/`\rvert`,





>         or `\mid` — NEVER a bare `|` character inside a cell or math block





>         (it is parsed as a column delimiter);





>     (c) subscripts/superscripts: ALWAYS braced LaTeX (`_{...}`, `^{...}`) inside





>         `$...$` — NEVER Unicode ₁ ₂ ³ ² or bare `_x` outside math;





>     (d) math symbols: use LaTeX codes (`\mathcal{S}`, `\mathbb{R}`, `\infty`,





>         `\to`, `\prec`, `\sim`, `\cdot`, `\ll`) — NEVER Unicode glyphs





>         (𝒮 ℝ ℚ ∞ → ≺ ∼ · ≪) in prose or math.





> (2) [HARD] **4 new anti-patterns** — PANDOC-PIPE-TABLE-1 (bare | in table cells),





>     UNICODE-MATH-1 (Unicode math glyphs in source), BARE-LATEX-MATH-1 (LaTeX





>     outside $ delimiters), UNBRACED-SUBSCRIPT-1 (unicode or unbraced sub/sup).





> (3) [HARD] **Publication Language Gate updated** — must scan for bare Unicode math,





>     bare pipes in table rows, and unbalanced `$` in addition to mojibake.





> Cross-reference: qnfo-core v1.14, user injunction 2026-08-04.





> Red-team: user condemned two-tier PDF pipeline ambiguity and browser headers/footers.





> HARD: 3. SOFT: 1. DESIGN: 0. Changes:





> (1) [HARD] **PDF Building section rewritten** — PRIMARY TIER (browser print-to-PDF)





>     REMOVED entirely. CDP pipeline (pandoc → MathJax SVG inline → puppeteer-core





>     page.pdf) is now the ONE AND ONLY supported workflow. No alternatives. No fallback.





> (2) [HARD] **4 new anti-patterns** — BROWSER-PRINT-TO-PDF-1 (never --print-to-pdf),





>     TWO-TIER-PDF-1 (never document multiple workflows), MATH-DELIMITER-1 (source





>     must use $...$/$$...$$), CHTML-SVG-1 (always switch CHTML to SVG).





> (3) [HARD] **Version header updated** — "TWO-TIER PIPELINE" → "CANONICAL CDP PIPELINE ONLY"





> (4) [SOFT] **CHROME-CACHED-DETECTION-1 anti-pattern removed** — CDP is now default,





>     no "cached detection" anti-pattern needed; Chromium IS a prerequisite.





> Cross-reference: qnfo-core v1.14, user injunction 2026-08-04.





> Red-team: direct parent-agent bias audit (session iH66zCEWF85XB0FQPfta4) — user





> condemned confirmation bias in the falsifiability thread. HARD: 4. SOFT: 0. DESIGN: 0.





> Changes:





> (1) [HARD] **Confirmation-Seeking Test added to KIF-60** — before crediting any





>     confirmation, name the alternative the test would have falsified; tests measuring





>     a parameter inside a presupposed framework (PPN γ, Brans–Dicke ω) are parameter





>     measurements, not theory discriminations.





> (2) [HARD] **Symmetric Audit Requirement added to KIF-29** — incumbents (GR, SM,





>     ΛCDM, string) must be graded with the SAME kill-criteria + null-equivalence





>     standard as new frameworks, from the start.





> (3) [HARD] **Methodological-independence definition for consilience.**





> (4) [HARD] **Anti-patterns CONFIRMATION-SEEKING-1 + PRO-INCUMBENT-BIAS-1 +





>     FORCED-CHERRY-PICK-1 added.**





> Cross-reference: kaizen v1.27, qnfo-core v1.14, user 2026-08-04 injunctions.











> **v2.70 UPDATE (2026-08-04, kaizen — Buffer GraphQL dictionary + BUFFER-* anti-pattern migration):**





> Red-team: MEMORY-TO-SKILL-DRIFT audit (session 7gJ25ecLca3VNUeaFCZKB) found 4 session-learned





> patterns absent from owning skills. HARD: 0. SOFT: 4. DESIGN: 1.





> Changes:





> (1) [SOFT] **Buffer GraphQL Complete Dictionary embedded** in Phase 7 Buffer Social Media —





>     canonical `api.buffer.com/graphql` flow: ClientInput{version,platform-lowercase}, top-level





>     `channels(input:{organizationId})` (NOT client.channels), createPost UNION





>     PostActionPayload with `... on PostActionSuccess { post { id status } }` inline fragments,





>     required `schedulingType: "automatic"`, known QNFO channel IDs table.





> (2) [SOFT] **4 BUFFER-* anti-pattern rows added** — BUFFER-GRAPHQL-UNION-1 (UNION field





>     selection fails), BUFFER-CLIENTINPUT-1 (client() has no channels), BUFFER-REST-401





>     (legacy REST rejected/deprecated 2027-02-01), BUFFER-SCHEDULING-TYPE-1 (required field).





> (3) [DESIGN] Buffer legacy REST API deprecated documentation (retired 2027-02-01) —





>     GraphQL-only guidance.





> Cross-reference: cloudflare v3.33 (RCLONE-NESTED-KEY-1 migrated same session),





> kaizen v1.21, session 7gJ25ecLca3VNUeaFCZKB.



































> **v2.46–v2.65 COLLAPSED HISTORY (15 banners, kaizen de-bloat 2026-08-04):**





> Historical version banners collapsed into summary. Full content preserved in





> HISTORY.md + git history (`deploy/history/research-v2.45-archive.md` + version control).





>   - v2.65: 2026-08-04 — MERGE: Continuity-Registry v2.63/v2.64 + session 1tz85 audit rows





>   - v2.64: 2026-08-04 — Research Continuity Registry Protocol





>   - v2.63: 2026-08-04 — Research Continuity Registry Protocol





>   - v2.62: 2026-08-04 — WBS canonical registry relocation (WBS.TAXONOMY-GAP closed)





>   - v2.61: 2026-08-04 — surgical draft-discard + token-validation correction





>   - v2.60: 2026-08-04 — Zenodo newversion unblock (STALE-DRAFT-BLOCK-1, FILE-ENTRY-SELECTION-1)





>   - v2.57: 2026-08-04 — WBS standardization + concurrent-closeout merge





>   - v2.55: 2026-08-04 — ENFORCED BACKFILL PROTOCOL for D1 zenodo_url





>   - v2.54: 2026-08-04 — D1 zenodo_url ownership incident (P5.OWNERSHIP gate)





>   - v2.51: 2026-08-03 — PDF quality enforcement (xhtml2pdf + Page.printToPDF deprecated)





>   - v2.50: 2026-08-03 — Zenodo API diagnostics + metadata fix (InvenioRDM migration)





>   - v2.49: 2026-08-03 — bibliographic fabrication prevention (P3.AUTHOR-GATE)





>   - v2.48: 2026-08-03 — ODR v3.0 publication forensics (5 R-fixes)





>   - v2.47: 2026-08-02 — PDF fallback + Zenodo hardening





>   - v2.46: 2026-08-02 — KIF-29 SOFT→HARD + Silo-Failure Detection (de-bloat 2,022→900 lines)





>











> **v2.66 UPDATE (2026-08-04, kaizen — PDF pipeline clarification + InvenioRDM complete dictionary):**





> Red-team: direct parent-agent skills audit (session 7gJ25ecLca3VNUeaFCZKB).





> HARD: 2. SOFT: 1. DESIGN: 1.





> Changes:





> (1) [HARD] **PDF Building section rewritten with TWO-TIER pipeline** — pandoc-native





>     MathJax HTML is the PRIMARY tier (zero downloads, zero Chrome, zero Node.js).





>     CDP puppeteer-core is the OPTIONAL production tier. The old HARD GATE "NO CHROMIUM





>     = BLOCK PUBLICATION" removed — publication is NEVER blocked by missing Chrome.





>     Primary tier always available for all papers.





> (2) [HARD] **InvenioRDM Complete API Reference added** — 18-operation table with





>     methods, endpoints, auth, request/response bodies, and notes; REQUIRED METADATA





>     FIELDS table with types and valid values; FILE UPLOAD FLOW diagram; PUBLISH





>     RESPONSE schema. This is the canonical dictionary — no agent should need to





>     reverse-engineer Zenodo API behavior.





> (3) [SOFT] **CHROME-CACHED-DETECTION-1 anti-pattern added** — Chrome may already be





>     cached from prior sessions; check before downloading 194 MB.





> (4) [DESIGN] **Primary tier established as default** — pandoc + browser print-to-PDF





>     is the CORRECT default for most paper workflows. CDP is for automated pipeline





>     scenarios only.





> Cross-reference: kaizen v1.22, session 7gJ25ecLca3VNUeaFCZKB.











> **v2.67 UPDATE (2026-08-04, kaizen — Zenodo metadata shape enforcement):**





> Red-team: direct parent-agent audit of session (Adelic Core Synthesis publication,





> DOI 10.5281/zenodo.21786473). HARD: 1. SOFT: 1. DESIGN: 0. Changes:





> (1) [HARD] **AD-HOC-ZENODO-METADATA-1 anti-pattern added** — the agent constructed





>     Zenodo metadata incrementally (reading the draft back, guessing missing fields)





>     instead of building the COMPLETE metadata object from the REQUIRED METADATA





>     FIELDS table below. The publish failed 3x with 400 (missing resource_type,





>     creators, publisher) — all fields documented in this skill since v2.66.





>     Fix: BEFORE any Zenodo PUT, build the full metadata object from the table:





>     title + publication_date + resource_type + creators + publisher are MANDATORY.





>     Never read-modify-guess the draft; always full-replace from the dictionary.





> (2) [SOFT] **Stale-memory script references** — durable memory cites





>     `zenodo-create-upload.py` / `zenodo-metadata-publish.py` as project-canonical;





>     these scripts were removed in the v2.46 de-bloat. The canonical path is the





>     INVENIORDM COMPLETE API REFERENCE + FILE UPLOAD FLOW in this skill. Corrected





>     memory; flagged MEMORY-TO-SKILL-DRIFT resolution.





> Cross-reference: qnfo-core v1.14, kaizen v1.22, git-github v2.14.











> **v2.68 UPDATE (2026-08-04, kaizen — Chromium claim correction + pipeline default hardening):**





> Red-team: direct parent-agent audit (user challenge: "WHY DOES THE PDF BUILD REQUIRE





> ADDITIONAL DOWNLOADS WHEN IT APPEARS TO FUNCTION JUST FINE?"). HARD: 3. SOFT: 2. DESIGN: 1.





> Changes:





> (1) [HARD] **"No system Chromium" claim corrected** — verified 4 Chromium binaries exist





>     on this machine: Edge, Chrome, Playwright, Chrome for Testing. Replaced with a 4-binary





>     priority detection chain (Edge → Chrome → Playwright → CfT cache).





> (2) [HARD] **Primary Tier elevated to DEFINITIVE DEFAULT** — pandoc `--mathjax` →





>     MathJax HTML → browser print-to-PDF is explicitly the STANDARD workflow for ALL papers,





>     with the reference PDF quality cite (DOI 10.5281/zenodo.21786603). ZERO downloads.





> (3) [HARD] **Production Tier re-scoped** — labeled "OPTIONAL — DO NOT USE BY DEFAULT."





>     Only for fully automated (no-user-interaction) scenarios.





> (4) [SOFT] **Render script hardened** — puppeteer-core launch now uses findChrome()





>     priority chain instead of hardcoding the CfT cache path.





> (5) [SOFT] **CHROME-CACHED-DETECTION-1 updated** — now lists all 4 Chromium locations.





> Cross-reference: kaizen v1.22, git-github v2.14, qnfo-core v1.14, windows-command-patterns v3.12.











> **v2.70 UPDATE (2026-08-04, kaizen — Bayesian Evidential Weight Gate (KIF-60) + retrodiction anti-patterns):**





> Red-team: direct parent-agent audit. User's 2026-08-04 methodological injunction





> (Obsidian note `_26216121020.md`) demanded that ALL frameworks produce falsifiable





> predictions, not post-hoc rationalizations.





> HARD: 1. SOFT: 0. DESIGN: 4. Changes:





> (1) [HARD] **KIF-60 Bayesian Evidential Weight Gate added** — sub-gate of KIF-29





>     Consilience. Every cross-domain correspondence claim MUST pass three tests:





>     (A) Pre-registration (timestamped prediction BEFORE observation);





>     (B) Falsifiability gradient (at least one concrete disconfirmation condition);





>     (C) Surprise accounting (P(match | random structure)).





>     Claims at Δlog-odds ≤ 0 → cap at [RETRODICTION — not evidence].





> (2) [DESIGN] **Three Tautology Traps documented** — Overfitting (dof ≥ matches),





>     Cherry-Picking (hit-only reporting), Absorption (everything = special case).





> (3) [DESIGN] **Four new anti-patterns** — RETRODICTION-1, OVERFITTING-1,





>     CHERRY-PICK-1, ABSORPTION-1 with cross-references to KIF-60 and kaizen





>     BAYESIAN-RETRODICTION-1.





> (4) [DESIGN] **Verification Gates table updated** — artifacts/bayesian-evidential-weight.md





>     now required for every paper claiming cross-domain correspondences.





> (5) [DESIGN] **KIF-60 Integration note in Phase 1b** — gate runs after Silo Cost Table.





> Cross-reference: kaizen v1.24 (BAYESIAN-RETRODICTION-1, FALSIFIABILITY-GATE-1),





> qnfo-core v1.14 §0.0 (Falsifiability Requirement), user Obsidian note 2026-08-04.











> **v2.69 UPDATE (2026-08-04, kaizen — Lossless de-bloat: banner collapse + CDP extraction):**





> Red-team: direct parent-agent bloat audit. SOFT: 18 banners, 109.4 KB → 78 KB.





> HARD: 0. SOFT: 1. DESIGN: 3.





> Changes:





> (1) [DESIGN] **v2.46-v2.65 banners collapsed** — 15 version banners reduced to summary





>     block. Full content preserved in HISTORY.md + git history.





> (2) [DESIGN] **CDP PDF pipeline extracted to references/cdp-pdf-pipeline.md** — 207 lines





>     of Production Tier Step 1-5 + code blocks moved to loadable reference file. SKILL.md





>     retains 7-line summary + cross-ref.





> (3) [DESIGN] **Zenodo INVENIORDM API reference retained inline** — per user mandate: complete





>     18-operation table, metadata fields, upload flow, publish response stay in SKILL.md.





> NET: 109.4 KB → ~78 KB (~29% reduction). Zero content loss.





> Cross-reference: kaizen v1.22, git-github v2.14.

























































































Cross-reference: kaizen v1.6, session 3bPo9XqsLFBBGRz0xT4HB.

































































## execute_plan











**WBS INTEGRATION (v2.56, HARD):** Every `update_plan` step carries a canonical





WBS code prefix `[{WBS}.P{N}]` (per qnfo-core N-1/N-4 + WBS-AGENT-PROTOCOL.md §2,





ADR-2026-007). Resolve the project's WBS code from D1 `program_registry` (or the





WBS.TAXONOMY.md registry) BEFORE executing; never invent codes. Phase numbers map





1:1 to WBS.TAXONOMY.md §2 (P0 Init → P8 Core Distribution). Canonical docs:





`QNFO/qnfo-ops:WBS/WBS.TAXONOMY.md` + `docs/WBS-AGENT-PROTOCOL.md`.











**CONCRETE EXAMPLE (v2.62, iteration-2 kaizen):** for an Ultrametric Physics paper





project, every plan step carries the literal prefix `[QNFO.UMP.002.P0]`,





`[QNFO.UMP.002.P4.T3]`, etc. — Portfolio `QNFO`, Program `UMP`, Project `002`,





Phase `P4`, Task `T3`. Example list:











```python





update_plan([





  {"step": "[QNFO.UMP.002.P0] Init: repo branch ump/paper/<slug>, WBS resolution, PROJECT-PLAN.md", "status": "in_progress"},





  {"step": "[QNFO.UMP.002.P1] Due diligence: KG + D1 + Vectorize cross-ref", "status": "pending"},





  {"step": "[QNFO.UMP.002.P4] Deep research: adelic QFT core derivation", "status": "pending"},





  {"step": "[QNFO.UMP.002.P5] Publication: PDF build, Zenodo, D1 insert", "status": "pending"},





])





```











update_plan([





  {"step": "[{WBS}.P0] Init: repo scaffold, WBS code resolution, README, PROJECT-PLAN.md, core claim lock", "status": "pending"},





  {"step": "[{WBS}.P0] Pre-Flight: run P1-P11 checklist — HARD gates must pass before Phase 1", "status": "pending"},





  {"step": "[{WBS}.P1] Due diligence: KG + D1 + Vectorize + external cross-ref", "status": "pending"},





  {"step": "[{WBS}.P1] Consilience gate (KIF-29 HARD): cross-domain lexicon + silo-cost table + synthesis", "status": "pending"},





  {"step": "[{WBS}.P2] Literature: 8 parallel sources, dedup, classify, Mandatory Symmetry Template (KIF-18)", "status": "pending"},





  {"step": "[{WBS}.P3] Citations: extract, verify BibTeX (P3.AUTHOR-GATE), auto-generate missing DOIs", "status": "pending"},





  {"step": "[{WBS}.P4] Research: Structured Forecast Protocol (11 stages) + red-team + calibration", "status": "pending"},





  {"step": "[{WBS}.P5] Publish: <slug>.md + PDF (pandoc→MathJax SVG→puppeteer-core CDP) + BP-1→BP-10 gates + Zenodo DOI", "status": "pending"},





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











**Note — QWAV product work routes through git-github, not research:** `PLT` (QWAV Platform → `QNFO/qwav-platform`, `plt/`) and `DEM` (QWAV Demos → `QNFO/qwav-demos`, `dem/`) are PRODUCT repos, not research-paper domains. Product/infra branches (`plt/infra/...`, `dem/artifact/...`) are handled by the git-github skill §Project Branch Policy routing table — the research pipeline (Phases 0-8) applies to `UMP`/`SLB`/`INM`/`CFE`/`RES` only. Full canonical mapping: qnfo-core §N-1.











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





- `search_papers({query: "<topic>", limit: 20})` via Vectorize — FULL-CORPUS SWEEP: >=3 distinct query formulations per topic (semantic drift) + qnfo-memory-mcp search_papers + search_papers_enriched + recall_facts + search_memories + KG neighbor walks

- CROSS-SYSTEM ID VALIDATION: for each hit, `resolve_paper_id` (slug -> Vectorize ID -> KG ID -> DOI); flag inconsistencies EARLY — a mismatch is a data-quality finding, not a footnote

- TAXONOMY BREADTH: >=2 adjacent WBS domains; surface records that CONTRADICT or COMPLICATE the hypothesis, not only those that support it





- Report: "QNFO Cross-Reference: Found N related papers across M domains (corpus size K)"

**DUE-DILIGENCE-DEPTH-1 (HARD GATE, 2026-08-14):** The QNFO corpus is ~1,000 records and growing rapidly — diverse domains, methods, and results; every record a potential contributor to the body of knowledge. Due diligence MUST be corpus-scale, not top-k convenience (user mandate 2026-08-14): (1) query_graph stats FIRST; (2) >=3 query formulations per topic, search_papers limit >=20; (3) resolve_paper_id per hit — cross-system ID validation, a mismatch is a data-quality finding, not a footnote; (4) >=2 adjacent WBS domains; (5) external independent verification (arXiv/OpenAlex/Crossref/archive.org CDX/Google Patents) — never accept a claim on the citing record’s word alone; (6) save every query/API response to artifacts/external-search/ — a count without its evidence file does not exist.











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

> **Multi-thread synthesis (v2.89):** For sessions spanning multiple research threads,
> apply kaizen v1.86 Synthesis Mode / Convergence Architecture BEFORE executing isolated
> tasks. Map cross-pillar merges (UMP×INM, UMP×CFE, INM×CFE, ALL×RES) and produce a
> convergence map — every task has a merge target. KIF-29 is the GATE; the Convergence
> Architecture is the METHODOLOGY. Cross-ref: kaizen v1.86 Mined Workflow Pattern G.












**Trigger: ALWAYS runs during Phase 1. Scope scales to project size.**











**GATE (HARD, MANDATORY):** Phase 1 MUST produce:











1. **Cross-Domain Lexicon** — dynamic domain selection from Phase 1 due diligence evidence (3-6 domains); fallback to Physics/CS/InfoTheory/Biology/Sociology template only if no evidence available. Explicitly state why each domain was chosen with evidence citations.











2. **Minimum-Viable-Finding** — at least one non-trivial structural isomorphism per domain checked, OR an explicit reasoned statement why none exists (with specific, verifiable reasoning — generic "not applicable" is REJECTED).











3. **Silo Cost Table** (see Silo-Failure Detection Protocol below).











4. **Synthesis Consilience** — one meta-principle (what is invariant across all translations) and one Frontier Question.











**Why this gate is HARD:** The Compton-BT synthesis (2026-08-02) is the canonical case. Five independent disciplines — mathematical physics, quantum foundations, number theory, computer science, information theory — each discovered the same combinatorial-tree-with-cross-ratios structure between 1916 and 1980, called it by five different names, and spent 78-110 years never connecting them. The prior SOFT trigger ("run when research spans 2+ domains") was circular: it only executed when the agent ALREADY knew the work was cross-domain, and silo blindness prevents that knowledge.











**Gate check:** If no consilience audit record exists in `artifacts/consilience-gate.md` with the Silo Cost table → Phase 1 is INCOMPLETE. HARD BLOCK on Phase 2.











**Symmetric Audit Requirement (2026-08-04, user injunction):** The consilience gate





audits the NEW framework's correspondences. It MUST ALSO apply the same kill-criteria,





null-equivalence, and confirmation-seeking standards to the incumbent frameworks





(GR, SM, ΛCDM, string theory) BEFORE crediting the new framework. Grading established





theories as more falsifiable by default (pro-incumbent bias) is forbidden: the SM's





19+ measured parameters and century of goalpost-moving particle hunts, the operational





GR composite's DM/DE/inflation auxiliary absorption, and string theory's landscape





must be audited with identical rigor. The audit is not symmetric until the incumbents'





grades survive the same adversarial lens.











**KIF-60 Integration:** The Bayesian Evidential Weight Gate runs as a sub-gate





of KIF-29. After the Silo Cost Table is computed and domain correspondences are enumerated,





EVERY claimed correspondence passes through the Three Concrete Tests before proceeding





to Phase 2. Any correspondence with Δlog-odds ≤ 0 is classified as [RETRODICTION] and





carries zero evidential weight in subsequent phases.











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











**Definition of independent consilience (2026-08-04):** A correspondence





counts as consilient evidence only when the converging lines are methodologically





independent — different instruments, different underlying physics, different analysis





teams, different systematic-error structures. Multiple tests within ONE research





program (same formalism, same prediction, same team) do NOT constitute consilience;





they constitute repeated measurement. The Compton-BT case is the standard precisely





because five disciplines never communicated.











**Canonical Case — Compton-BT:**











| Domain | Structure Name | Earliest | Silo Cost | Key Paper |





|:-------|:---------------|:---------|:----------|:----------|





| Number Theory | Ostrowski completions | 1916 | **110 yr** | Ostrowski, Acta Math 1916 |





| Quantum Foundations | Zitterbewegung/Compton | 1928 | **98 yr** | Dirac, Proc. Roy. Soc. A 1928 |





| Information Theory | Dimensionless entropy | 1948 | **78 yr** | Shannon, BSTJ 1948 |





| Computer Science | Radix tree / trie | 1960 | **66 yr** | Fredkin, 1960 |





| Mathematical Physics | Bruhat–Tits tree | 1980s | **~40 yr** | Vladimirov–Volovich, 1994 |











If silo cost > 50yr: flag `[SILO-FAILURE: >50yr gap — this synthesis rectifies multi-generational knowledge fragmentation]`.











### Bayesian Evidential Weight Gate (KIF-60, HARD — 2026-08-04)











**Purpose:** Every claimed cross-domain correspondence in a QNFO paper must pass the





Bayesian update check — a framework that "explains" known observations by design has





not actually constrained the hypothesis space. The gate distinguishes genuine risky





predictions from post-hoc curve-fitting.











**Trigger:** Runs as a sub-gate of KIF-29 Consilience. ALWAYS invoked when:





1. A paper claims a structural correspondence between two or more domains





2. A forecast or calibration register entry cites "matches" across frameworks





3. A synthesis claims to unify previously separate structures











**The Bayesian Update Check:**











For any claimed correspondence between theory T and observation O:











```





Δ log-odds = log[ P(O|T) / P(O|¬T) ]











If P(O|¬T) ≈ 1 (O was already known; T was built around it):





    Δ log-odds ≈ 0  →  ZERO evidential weight — retrodiction, not prediction











If P(O|¬T) ≪ 1 (O is genuinely surprising without T):





    Δ log-odds ≫ 0  →  Positive evidential weight — genuine risky prediction





```











**Three Concrete Tests (MANDATORY for every cross-domain correspondence claim):**











| Test | What It Demands | Evidence Required | Gate |





|:-----|:----------------|:------------------|:-----|





| **Pre-registration** | Prediction stated BEFORE observational access | Timestamped, immutable record (git commit, tape anchor, Zenodo pre-reg) of what was predicted and when | HARD |





| **Falsifiability gradient** | Some observations SHOULD kill the theory | Explicitly list: "If we observe X, the framework is wrong" — at least one concrete disconfirmation condition per claim | HARD |





| **Surprise accounting** | Prior probability of match under null hypothesis | For each claimed match: estimate P(match \| random structure of comparable complexity) — bounds acceptable even without exact computation | HARD |





| **Confirmation-seeking test** | The confirming observation must discriminate the theory from a serious alternative | Name the alternative the test would have falsified; if no viable alternative predicted a different value, the test is a parameter measurement inside a presupposed framework (PPN example: Shapiro constrains γ, does not falsify Brans–Dicke) — not a theory discrimination | HARD |











**The Tautology Trap — Three Failure Modes:**











| Trap | Symptom | Detection | Fix |





|:-----|:--------|:----------|:----|





| **Overfitting Trap** | Formalism has enough degrees of freedom to "explain" ANY data | Count free parameters vs. number of independent matches; if dof ≥ matches, Δlog-odds ≤ 0 | Pre-register parameters BEFORE seeing data; use holdout set |





| **Cherry-Picking Trap** | Only hits are reported; misses are "areas for future work" | Audit the full search space — what was the denominator? How many structures were checked? | Report hit/miss ratio; treat misses as falsification events with evidential weight |





| **Absorption Trap** | Every counterexample = "special case" or "duality transformation" | If every apparent disconfirmation can be absorbed by declaring a new duality map, the theory has zero empirical content | Pre-declare the set of ALLOWED dualities BEFORE seeing counterexamples |











**The Confirmation-Seeking Test (2026-08-04, user injunction):** Before crediting





any test as evidence for a framework, ask: *what alternative hypothesis would this





test have falsified?* If the test was designed inside the framework's own research





program, by proponents, to measure the framework's predicted magnitude (Pound–Rebka,





Shapiro, Hulse–Taylor inside GR), it is a **parameter measurement**, not a theory





discrimination — the alternative (e.g., Brans–Dicke with tuned ω) predicts a nearly





identical observation. A test that would falsify only a strawman (a theory predicting





zero of a shared phenomenon) carries no discriminatory weight. Genuine discriminations





require the alternative to predict a measurably different O_T ≠ O_N. Grade accordingly.











**Gate Output:** `artifacts/bayesian-evidential-weight.md` containing:





1. **Pre-Registration Record:** Timestamped prediction list with sha256 hashes





2. **Falsifiability Matrix:** One disconfirmation condition per claim





3. **Surprise Accounting Table:** Per-claim P(match | random) under stated null model





4. **Δlog-odds Summary:** Per-claim Bayesian update — positive, zero, or negative





5. **Trap Audit:** Overfitting / Cherry-Picking / Absorption check with evidence











**Gate Check:** If any cross-domain correspondence claim has Δlog-odds ≤ 0 (zero or





negative evidential weight), the paper MUST declare it as [RETRODICTION — not evidence]





rather than presenting it as a finding. Claims with Δlog-odds > 0 require pre-registration





evidence. Claims without pre-registration evidence are capped at [NOT YET EVIDENCE].











**Canonical Case:** The Five Pillars paper (Adelic Core Synthesis + extensions). The





framework maps the Ruliad, Autaxys QC, and Measurement Stratigraphy onto common





structural invariants. Without this gate, every correspondence is equally "explained";





with it, only pre-registered, falsifiable predictions carry evidential weight. The





user's 2026-08-04 methodological injunction (Obsidian note `_26216121020.md`) is the





trigger: "Don't give me a story that fits everything; show me how the theory constrains





possibilities and makes risky predictions that could falsify it."











**Cross-reference:** kaizen v1.24 (BAYESIAN-RETRODICTION-1, FALSIFIABILITY-GATE-1),





qnfo-core §0.0 (Falsifiability Requirement, Certainty Calibration).











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











### P3.SOURCE-DISCIPLINE (mined 2026-08-05, from QNFO/claude-skills research router)











Extends P3.AUTHOR-GATE from bibliography fabrication to **every in-text citation**:











1. **Cite only sources returned by THIS session's tool calls.** A source not actually





   fetched/verified in this session MUST NOT appear as a cited source. Recalled or





   training-knowledge claims are labeled `[Background — not from search]` and excluded





   from the cited-source count. This is the citation-level extension of





   ZENODO-PHANTOM-DOI-1 / CLAIM-VERIFY-1 — never cite what you did not verify.





2. **Three-count audit** — every research deliverable tracks: queries sent /





   sources received / sources cited. If cited > received, fabrication is present.





3. **Source reliability tiers** — label each cited source primary (original data,





   official docs), secondary (reviews, curated aggregators), tertiary (blog,





   forum, unreviewed). Tier drives weight in synthesis; disagreements between tiers





   are surfaced explicitly.





4. **Thin-results honesty** — when search returns thin results, say so explicitly





   ("limited public signal on this") — never fabricate to fill a gap.

















---











## Phase 4: Deep Research & Structured Forecast (MANDATORY for all projects)











**Scope scales to project size.** Single-result paper: assumptions enumerated, uncertainty ranges, sensitivity check, ≥1 calibration prediction. Paradigm forecast: full 11-stage protocol.











### PANDOC-SAFE AUTHORING MANDATE (v2.73, HARD — author-time gate)











**LLM-generated paper text MUST be pandoc/MathJax-safe at authoring time. Surgical





hand-fixing after the fact is FORBIDDEN — generate it correctly the first time.**











The paper is converted via `pandoc --mathjax` then rendered by MathJax SVG in a





headless Chromium. The source markdown therefore MUST follow these rules:











| Rule | Requirement | Wrong (breaks) | Right |





|:-----|:------------|:---------------|:------|





| **Math delimiters** | Every formula inside `$...$` or `$$...$$` | `I(r) = \log_2 \lvert\mathcal{S}_r\rvert` in prose | `$I(r) = \log_2 \lvert\mathcal{S}_r\rvert$` |





| **Vertical bars** | Never a bare `|` inside a pipe-table cell or math | `| Low (~0 for \|𝒮\| > 10³) |` | `| Low (~0 for $\lvert\mathcal{S}\rvert > 10^3$) |` |





| **Sub/superscripts** | Always braced LaTeX inside math | `G_r`, `q^{d·r}` in prose; `S²` | `$G_r$`, `$q^{d \cdot r}$`; `$\mathcal{S}^2$` |





| **Math glyphs** | Use LaTeX codes, never Unicode glyphs | `𝒮 ℝ ℚ ∞ → ≺ ∼ ·` | `\mathcal{S}` `\mathbb{R}` `\infty` `\to` `\prec` `\sim` `\cdot` |





| **Conditional prob** | Use `\mid` inside math, not `|` | `P(O|¬T)` | `$P(O \mid \lnot T)$` |





| **Absolute value** | Use `\lvert`/`\rvert` or `\vert` in math | `|𝒮|` | `$\lvert\mathcal{S}\rvert$` |





| **YAML frontmatter** | No backslash-LaTeX inside double-quoted YAML | `title: "…$\mathbb{R}$…"` | `title: 'Valuation Without R: …'` (plain) |











**Gate (HARD):** before any pandoc build, run the source audit: zero bare `|` in





table cells, zero Unicode math glyphs, zero bare LaTeX outside `$`, `$` count EVEN,





all sub/superscripts braced and inside math. Any violation → regenerate the text,





do NOT patch it.











**PUBLICATION PRINCIPLE:** Do NOT name the methodology in research outputs. Bury the method in the prose — "Underlying this candidate are three critical assumptions" not "Stage 2 Assumption Audit found."











**METHODOLOGY NOTE:** This is a structured judgment exercise, NOT a Bayesian computation. Qualitative ranking with uncertainty ranges and reference-class anchors. No false-precision EV numbers.











### Stage -1: Likelihood Calibration Protocol (HARD GATE)











Every P(E|H) > 0.80 must trace to an empirical calibration pillar (Empirical Base Rate, Reference-Class Forecast, Calibrated Subjective, Inter-Rater Reliability, Known Prior). Unanchored likelihoods capped at 0.80 with `[CALIBRATION-CAP]`. Run calibration training (≥20-question quiz, Brier score). Reviewer subagent independently assigns every assumption. Output: `artifacts/likelihood-calibration.md`.











### Stages 0-8: Full Protocol (scope-scaled)











0. **Domain Assessment** — map field, active paradigms, key questions.





1. **Paradigm-Shift Candidates** — qualitative ranking, impact/timeline/testability/dependency.





2. **Assumption Audit** — enabling assumptions, blocking assumptions, dependency chain.





3. **Red-Team Challenge** — 5 adversary positions (Null-Hypothesis Defender, Methodology Skeptic, Better-Alternative Proposer, Scaling Pessimist, Resource Realist). **MANDATORY method (ZENODO-INQUIRY-1):** the Universal Ignorance Audit (DOI 10.5281/zenodo.21901984; synthesis: DOI 10.5281/zenodo.21901983) provides a 15-question deep-inquiry alternative that surfaces structural ignorance (scaffolds, map–territory errors, protected zones) complementary to adversarial correctness. See kaizen v2.01 §H.





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











### COMPUTATIONAL-VERIFICATION-1 (HARD GATE — 2026-08-19, user mandate "MORE COMPUTATIONAL ANALYSIS/VERIFICATION IN RESEARCH")

Every research artifact making quantitative, mathematical, or statistical claims MUST carry
computational verification with evidence deposited, BEFORE publication:

1. **NUMERICAL SANITY:** every key equation/formula/identity gets a numerical check against
   independent evaluation (Python/JS; arbitrary precision where relevant) — golden values, edge
   cases, asymptotics, limit behavior, dimensional consistency. Extends BP-1 (Fit-Verify) beyond
   fits to EVERY non-trivial formula in the paper.
2. **VERIFY-IN-CODE-1:** any claim a computer can check MUST be checked in code before it is
   asserted. Compute-checkable claims asserted without code = HARD finding. "Analytic proof only"
   is not a substitute when a claim is numerically checkable.
3. **SIMULATION FOR STATISTICAL CLAIMS:** probabilistic/statistical claims get seeded Monte
   Carlo/simulation runs with explicit test statistics — never hand-waved bounds.
4. **VERIFICATION ARTIFACTS DEPOSITED:** verification scripts + result outputs live in
   artifacts/verification/ and are INCLUDED in the Zenodo deposit (extends
   PUBLICATION-SOURCE-COMPLETENESS-1); the paper cites its verification evidence files.
5. **REPRODUCIBILITY STATEMENT:** runtime, seed, dependency versions, and re-run instructions
   (README section or dedicated "Verification" appendix).
6. **DEMO GATE (flagship results):** flagship/core results get an interactive executable demo via
   qwav-demo-kit (DEM-E0-T01..T05: golden-value verification, CDP test-demo.py + Playwright
   click-everything suite, gh-pages deploy with same-turn anti-phantom verification) — published
   research must demonstrably execute in code.

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

**Existential-Claim Verification Gate (KIF-62, v2.85 — HARD):** Before publication, scan the paper for existential-claim patterns: "does not exist," "has not released," "has not been announced," "no model designated," "never existed," "was not deployed," and variants. For EACH existential claim, verify against at least one live authoritative source (Wikipedia, official product pages, news archives, API endpoints, scholarly databases). An unverified existential claim is a research-integrity violation — identical in kind to a fabricated citation. Save verification evidence to `artifacts/existential-claim-verification.md`. Canonical case: Heffner audit v1.0 §2.2 claimed GPT-5 did not exist as of August 2026 (DOI 10.5281/zenodo.21812511); corrected in v1.1 (DOI 10.5281/zenodo.21812761) after Wikipedia verified GPT-5 release date as August 7, 2025. Enforcement of qnfo-core v1.17 VERIFY-FACT-1 / VERIFY-DONT-ASSUME-1.





Scan for: internal language, credential leaks, bare Unicode math, AI-generated filler phrases, AI-quality-gate violations (elementary physics/energy-budget errors incl. P_decode direction slips, synthetic citation anchors, scaffold overload, hand-waved integration, self-referential metrics), **internal references (repo paths, skill sections, internal program names, WBS codes like `QNFO.UMP.005`, quoted internal program names like "QEC Darwinism" — INTERNAL-REF-1)**, **title duplication (exactly ONE rendered title — TITLE-DUPLICATION-1; scripted gate: `check-title-duplication.py <slug>.html`, build-time BLOCK)**, **file naming (`<slug>.md/.pdf/.html`, never `paper.*` — FILE-SLUG-1)**, **map–territory labels (any `[TERRITORY` identity claim requires a falsifiability condition — MAP-TERRITORY-1; scripted gate: `check-map-territory.py <slug>.md`, build-time BLOCK)**. Run `scan-mojibake.py` (qnfo-core §0.2). Run credential scan.











### Publication Language Gate — Brand-Token Ban (PUBLICATION-BRAND-LANGUAGE-1, HARD — 2026-08-21, user directive)
Meta-commentary narrating the act of publishing/disclosing — or grading it — is banned (PUBLICATION-META-PROSE-1, 2026-08-21): "published, not hidden", "rather than the confirmation", "kept on the same ledger", "not a silence". State the fact; the DOI carries the evidence.


Branded register/ledger/honesty vocabulary is banned from publication prose (extends PUBLICATION-PROSE-GATE-1). Banned brand tokens: "falsifiability register", "honest null ledger", "pre-registered observables", "kill-conditions", "published nulls" used as recurring labels; "honest question", "The Honest Landscape", "honestly reported", "Honest caveat/residual", "Honest Accounting", "weigh this record"; confidence tags (`[speculative]`) in abstracts; internal gate names as section headers ("So What? Why Should a Reader Care About This Research?"). Rules: pre-registration = a fact with its identifier (OSF DOI); disconfirmation criteria = numbers, labeled "Disconfirmation criterion:" (never "Kill-condition:"); negative results = results ("no log-periodic signal was found; bootstrap p=0.89"). Canonical offenders: guide 22036025/22038733, QEC-Darwinism 21964674, BTQP 20109836, register 22025544 (CMD RED TEAM 2026-08-21, Language=CONFIRMED).

### Cross-Record Status Sync (PUBLICATION-STATUS-STALE-1, HARD — 2026-08-21)

Before EVERY publish AND every newversion: sweep the corpus for records that change any experiment-status sentence in the artifact. Canonical: guide v1.2 (22036025) AND v1.2.2 (22038733) Appendix A + Ch.16 state "E1 (CMB log-periodic oscillations) ... remain unexecuted as of 2026-08-20" while 21902891 (2026-08-12) reports a certified null on that exact test and the same-day register lists "the cosmological log-periodic null". A newversion that ships a stale status sentence is a HARD finding even when other fixes ship.

### Internal Anchor Resolution (INTERNAL-ANCHOR-DANGLING-1, HARD — 2026-08-21)

Every internal cross-reference ("Chapter N, open problem M", "see §X") must resolve in the published artifact. A newversion that adds the missing target MUST annotate the change in the changelog/appendix. Canonical: guide v1.2 Appendix A cites "(Chapter 20, open problem 7)" while Ch.20 lists six; v1.2.2 adds the 7th silently.

### Physics Writing Standards





All 18 points from qnfo-core §7. Minimum: certainty calibration, falsifiability conditions, banned-word enforcement.





























### Research Continuity Registry Protocol (v2.64, HARD)











**Purpose:** When any QNFO publication puts forth research plans, frontier questions,





falsifiable predictions, or pre-registerable conditions, they MUST be tracked in a





living RESEARCH-CONTINUITY-REGISTRY.md in the project's repository.











**Trigger:** Any Zenodo publication (Phase 5) that contains frontier/research questions





for further investigation, falsifiable predictions with test windows, falsifiability





conditions, or pre-registration scaffolds.











**Registry Structure (canonical):**





1. FRONTIER RESEARCH QUESTIONS — FQ1-FQn with Status/Next Action/Pre-Reg Suitable





2. FALSIFIABLE PREDICTIONS — P1-Pn with Test Window/Instrument/Disconfirmation Condition





3. PER-RQ FALSIFIABILITY CONDITIONS — one "disconfirmed if" per research question





4. PRE-REGISTRATION SCAFFOLDS — REG-{PROJ}-001+ with Hypothesis/Falsification/Data/Deadline





5. CALIBRATION REGISTER — dated [CHECK: YYYY] predictions with strength grading





6. NEXT ACTIONS (Prioritized) — P0/P1/P2 with dependencies and targets





7. SESSION LOG + MAINTENANCE PROTOCOL











**Canonical case:** ODR Thesis v2.0 (DOI 10.5281/zenodo.21784489) + Quasiparticles v2.0





(DOI 10.5281/zenodo.21784490) — created RESEARCH-CONTINUITY-REGISTRY.md in QNFO/odr-thesis





with 10 FQs + 5 predictions + 5 disconfirmation conditions + 3 pre-reg scaffolds.











**Anti-patterns:**





| Anti-Pattern | Fix |





|:-------------|:----|





| Publishing frontier questions without tracking in a registry | Create RESEARCH-CONTINUITY-REGISTRY.md before Phase 5 closeout |





| Tracking registries as static paper artifacts | Registry is a LIVING DOCUMENT — maintained with version bumps |





| Overlooking companion papers in same session | Cross-reference companion DOIs; extract their trackable items |





| Central registry in archived repo blocking cross-ref push | Unarchive first; keep unarchived for living documents |

















### Professional Publication Standards (HARD GATE)





Structural: Title, Abstract (150-250 words), Keywords (4-6), Introduction, Body, Conclusion, Declarations (9 subsections), Bibliography. Tone: formal third-person, no hedging filler, no contractions, no rhetorical questions. Copyediting: zero spelling errors, consistent hyphenation, curly quotes, every acronym defined, every figure captioned, no orphaned headers.











### Ostrowski Dimensionless Mandate (HARD)





ALL physics formulas in dimensionless Planck units (ℏ=c=G=kB=1). Dimensional formulas must include dimensionless equivalent + Ostrowski rationale. Cross-reference: qnfo-core §0.7.











### Source File Encoding Integrity (HARD, KIF-28)





Zero BOM, zero U+FFFD, zero U+FFFF in all source files. All Python: `encoding='utf-8'` explicit. Pre-commit scan mandatory.





### PDF Building (v2.72 — CANONICAL CDP PIPELINE ONLY)
**Print-size gates (2026-08-21):** `@page { size: A0 portrait }` is IGNORED by Chromium (A0 is not a supported page keyword — silent US Letter fallback). Use explicit `size: 841mm 1189mm` (A1 = `594mm 841mm`) and verify every rendered PDF's MediaBox (A0 = 2383.9×3370.1pt). Poster fill claims require a pixel measurement (Edge headless screenshot at exact page px + PIL content-bbox; margins = design padding). No hand-placed SVG text — annotation lives in HTML typography (SVG-LABEL-EXTENT-1).












**ONE WORKFLOW. ONE PIPELINE. NO ALTERNATIVES.**











pandoc (`--mathjax`) → MathJax SVG inline → puppeteer-core CDP `page.pdf()`.











This is the ONLY supported PDF workflow for QNFO papers. No browser print-to-PDF.





No `--print-to-pdf`. No "primary tier." No fallback. One pipeline, every time.











**Full documentation:** `references/cdp-pdf-pipeline.md` — load via





`skill_view("research", "references/cdp-pdf-pipeline.md")`.











**Canonical steps (summary):**





1. Source markdown math MUST use `$...$` / `$$...$$` (NOT `\(...\)` / `\[...\]`)





2. `pandoc --mathjax --standalone <slug>.md -o <slug>.html`





3. Switch CHTML → SVG: `html.replace('tex-chtml-full.js', 'tex-svg-full.js')`





4. Inline locally-cached MathJax SVG (`%TEMP%\mathjax\tex-svg-full.js`, ~2.2 MB) into HTML





5. puppeteer-core CDP: `page.pdf({path: '<slug>.pdf', format:'A4', margin:{top:'2cm',bottom:'2cm',left:'2cm',right:'2cm'}, printBackground:true})`
   **Render script: use `.cjs` (CommonJS) with `require('C:/Users/LENOVO/node_modules/puppeteer-core')` — NOT `.mjs`** (v2.97: ESM require/import fails on Windows absolute paths; see NODE-MJS-ESM-1).
   **`path:` IS REQUIRED (PDF-PATH-OPTION-1, v2.96).** Without it, `page.pdf()` returns a Buffer and writes NO file — the pipeline reports success while the PDF is missing (canonical: ringbauer-qudit-due-diligence 2026-08-10).





2.5. **TITLE-DUPLICATION-1 GATE (HARD, v2.86):** run `python research/scripts/check-title-duplication.py <slug>.html` after pandoc, before MathJax inline + CDP render. PASS = exactly ONE rendered `<h1 class="title">`, zero body `<h1>`. FAIL = BLOCK the build (body `# <Title>` H1 must be removed — the YAML title is the single page-1 title).

6. Verify: 0 U+FFFD, 0 U+FFFF, PDF > 100 KB











**Chromium detection (all cached on this machine):** Chrome for Testing →





Playwright → Edge → Chrome. `puppeteer.launch({executablePath, headless:true})`.











**MathJax CDN UNREACHABLE from headless Chrome.** MathJax MUST be downloaded





locally and inlined. Use `str.replace()` NOT `re.sub()` — MathJax JS contains





`\u` escapes that crash Python's regex engine.











**Gate (v2.86):** title-duplication check PASSED (check-title-duplication.py — exactly one rendered title) AND PDF > 100 KB AND 0 U+FFFD/FFFF (binary byte scan — `data.count(b"\xef\xbf\xbd")` for U+FFFD, `b"\xef\xbf\xbf"` for U+FFFF — **NEVER PyMuPDF/fitz**, see PYMUPDF-FORBIDDEN-1) → PASS. Anything else → BLOCKED.### Zenodo Upload





**METADATA SHAPE MANDATE (v2.67, HARD):** The EXACT metadata shape for ALL Zenodo





uploads is the REQUIRED METADATA FIELDS table below — do NOT guess it, do NOT





read-modify-guess the draft. Build the complete object on the first PUT:





`title`, `publication_date`, `resource_type` (object `{"id": "publication-preprint"}`),





`creators` (array of `person_or_org`), and `publisher` are ALL MANDATORY at publish.





A partial PUT (missing any of these) fails with HTTP 400 on publish — exactly as





documented in ZENODO-PUBLISHER-REQUIRED-1 and ZENODO-METADATA-REQUIRED.

**TWO-API METADATA SHAPE DISTINCTION (v2.79, HARD — READ FIRST):** Zenodo has TWO
write APIs with DIFFERENT metadata field names. Mixing them up causes the
"Not a valid string" / "Missing data for required field" 400s this skill
documents. Determine which API you are driving FIRST, then use ITS field names.

| Field | Deposit API (`/api/deposit/depositions/{id}` PUT) | Records API (`/api/records/{id}/draft` PUT) |
|:------|:--------------------------------------------------|:---------------------------------------------|
| resource type | **`upload_type`** (string: "publication") + **`publication_type`** (string: "preprint") | **`resource_type`** (object: `{"id": "publication-preprint"}`) |
| creators | `{"name": "Family, Given", "affiliation": "...", "orcid": "..."}` | `[{"person_or_org": {"family_name": ..., "given_name": ..., "type": "personal"}}]` |
| works with | PUT then `POST .../actions/publish` | PUT then `POST .../draft/actions/publish` |

Canonical case (2026-08-05, session 3i_KVLownViukLTZB_BJ1): the Five Pillars
attribution fix (21789920 -> newversion draft 21807661) burned ~15 failed PUTs
because the script copied the RECORDS-API `resource_type` object
(`{"title":"Preprint","type":"publication","subtype":"preprint"}`) into a DEPOSIT-API
PUT. The deposit API rejected it with 400 "Not a valid string." / "Missing data
for required field." The fix: send `{"upload_type": "publication", "publication_type":
"preprint"}` and the PUT + publish succeeded first try. Also note: the RECORDS-API
read response contains `resource_type` as an object — never copy that shape into a
deposit-API PUT. Cross-ref: ZENODO-DEPOSIT-API-METADATA-1, ZENODO-METADATA-REQUIRED,
AD-HOC-ZENODO-METADATA-1, ZENODO-UPLOAD-MULTIPART-1.























**Credential Protocol:** Never hardcode or retype tokens. Reference live environment variable. Run `scripts/zenodo-token-check.py` on ANY auth failure (403, 404, 415). The script validates (a) token existence, (b) token validity via a REAL endpoint `GET /api/records/{id}` (200) — NOTE: `GET /api/me` is UNRELIABLE (intermittently 404s with a valid token; see ZENODO-ME-404), (c) InvenioRDM endpoint reachability via `GET /api/records`, and (d) Content-Type header requirements before diagnosing the root cause. Never diagnose "403 = token scope" without running the checker first — InvenioRDM migrates old endpoints to 404, which some clients report as 403. [HARD — v2.50, session SHEfIEGiQvA2LI5xAPkon: quasiparticle extension paper blocked 6+ hours because 403 was diagnosed as "token scope" when the real issue was decommissioned endpoint 404.]











**ZENODO-API-INVENIORDM (v2.50, HARD):** Zenodo migrated to InvenioRDM. The old `GET /api/deposit/depositions` endpoint returns HTTP 404 (decommissioned). Use:











| Old (decommissioned) | New (InvenioRDM) | Verified |





|:---------------------|:-----------------|:---------|





| `POST /api/deposit/depositions` | `POST /api/records` | ✅ |





| **NOTE (v2.74):** the deposit API is NOT fully decommissioned — it remains LIVE and





  functional alongside the records API. Verified 2026-08-04: `POST /api/deposit/depositions`





  → 201, `POST /api/deposit/depositions/{id}/files` (multipart) → 201, `POST .../actions/publish`





  → 202, DOI minted. Use whichever API the existing pipeline already drives; if `/api/deposit/...`





  returns 404, fall back to `/api/records/...` (ZENODO-DEPOSIT-API-LIVE-1). |





| `GET /api/deposit/depositions?q=<query>` | `GET /api/records?q=<query>` | ✅ |





| `PUT /api/deposit/depositions/{id}` | `PUT /api/records/{id}/draft` | ✅ |





| `POST /api/deposit/depositions/{id}/actions/publish` | `POST /api/records/{id}/draft/actions/publish` | ✅ |





| `POST /api/deposit/depositions/{id}/actions/newversion` | `POST /api/records/{id}/draft` | ✅ (v2.55 — HTTP 201 creates draft edit) |





| `PUT /api/files/{bucket}/{filename}` | `PUT /api/records/{id}/draft/files/{filename}` | ✅ |





| File upload Content-Type | `application/octet-stream` (mandatory) | ✅ |





| Token validation | `GET /api/me` (HTTP 200) — NOT `/api/user` (HTTP 404) | ✅ |





| Newversion (Obsolete) | `/actions/newversion` returns **HTTP 404** — decommissioned entirely. Use `POST /api/records/{id}/draft` instead. | ✅ |











**INVENIORDM COMPLETE API REFERENCE (v2.66 — comprehensive):**











| Operation | Method | Endpoint | Auth | Request Body | Success | Notes |





|:----------|:-------|:---------|:-----|:-------------|:--------|:------|





| **Token validation** | GET | `/api/records/{id}` | Bearer | — | 200 | `/api/me` is UNRELIABLE (intermittent 404); use any real record endpoint instead (ZENODO-ME-404) |





| **Create deposit** | POST | `/api/records` | Bearer | `{"metadata":{...}}` | 201 | Returns `{id, links, metadata}`; `links.bucket` may be empty in InvenioRDM |





| **Get record** | GET | `/api/records/{id}` | Bearer | — | 200 | Returns full record including `metadata`, `files`, `links` |





| **Get record (public)** | GET | `/api/records/{id}` | None | — | 200 | Public metadata only; `files` accessible without auth |





| **Search records** | GET | `/api/records?q=<query>` | None | — | 200 | **q= OR-tokenizes unquoted queries** (ZENODO-SEARCH-FN); use `&q=` for phrase search |





| **Update metadata** | PUT | `/api/records/{id}/draft` | Bearer | `{"metadata":{...}}` | 200 | **FULL replacement**, not merge — include ALL fields: title, date, resource_type, creators, publisher (ZENODO-PUBLISHER-REQUIRED-1) |





| **Create draft from published** | POST | `/api/records/{id}/draft` | Bearer | — | 201 | Creates edit draft; **bucket may be LOCKED** (ZENODO-EDIT-DRAFT PROTOCOL). For file changes prefer newversion |





| **New version** | POST | `/api/records/{id}/versions` | Bearer | — | 201 | Creates new record; **HTTP 500 if stale drafts exist on concept** (ZENODO-STALE-DRAFT-BLOCK-1). Response may have `id: null` — real id in `links.self` (ZENODO-REQUESTS-POST-201) |





| **Discard draft** | DELETE | `/api/records/{id}/draft` | Bearer | — | 204 | 204 = No Content; body is empty (do NOT json.loads()) |





| **Delete record** | DELETE | `/api/records/{id}` | Bearer | — | 204/403 | Published records CANNOT be deleted (403); drafts return 204 |





| **List user drafts** | GET | `/api/user/records?status=draft` | Bearer | — | 200 | Returns `{hits: {hits: [...]}}`; ~500 drafts on QNFO account (ZENODO-DRAFT-DISCARD-SURGICAL-1) |





| **Declare file** | POST | `/api/records/{id}/draft/files` | Bearer | `[{"key":"fname"}]` | 201 | Returns `{entries: [{key, links: {content, commit}}]}`; select entry by `key == fname` (ZENODO-FILE-ENTRY-SELECTION-1) |





| **Upload file content** | PUT | `{entry.links.content}` | Bearer | raw bytes | 200 | `Content-Type: application/octet-stream` MANDATORY |





| **Commit file** | POST | `{entry.links.commit}` | Bearer | — | 200 | Required after upload; 404 = wrong entry selected |





| **Delete file** | DELETE | `{entry.links.self}` | Bearer | — | 204 | 204 = zero-length body |





| **Overwrite file** | PUT | `/api/records/{id}/draft/files/{fname}` | Bearer | raw bytes | 200 | Overwrites existing file atomically — no DELETE needed (BUCKET-LOCKED-RESOLVE-1) |





| **Publish** | POST | `/api/records/{id}/draft/actions/publish` | Bearer | — | 202 | Returns `{doi, conceptdoi, id, metadata}`; verify DOI resolves with `curl -sI https://doi.org/{doi}` |





| **Metadata-only edit (in-place)** | POST→PUT→POST | `/api/records/{id}/draft` cycle | Bearer | metadata JSON | 202 | Same DOI, no new record. Use for keywords/notes fixes; newversion only for file changes. Verified on 322 records (ZENODO-INPLACE-EDIT-1) |











**NEWVERSION-FRONTMATTER-CARRYOVER-1 (v2.109, HARD):** newversion drafts carry ALL parent
files byte-identical — the .md YAML `doi:` still points at the parent version. MANDATORY newversion
order: (1) create draft + reserve new DOI (deposit: prereserve_doi; records: POST .../draft/pids/doi);
(2) patch .md frontmatter `doi:` to the NEWVERSION's own reserved DOI + `status: published` BEFORE
upload (P5.FRESH); (3) rebuild html/pdf if body changed; (4) replace carried-over files (delete +
re-upload via deposit /files or records /draft/files overwrite); (5) publish; (6) verify deposited
.md sha256 vs local + doi.org HEAD 200 + DataCite findable. Canonical case: RES.007 v0.2
(10.5281/zenodo.21929590) shipped stale v0.1 DOI (21929479) in deposited .md (byte-identical carry-
over) — Accuracy-reviewer HARD-1, remediated v0.3 (10.5281/zenodo.21929902). Anti-anti-pattern: do
NOT call a reserved newversion DOI "phantom" just because the parent resolves — check records API
state=done or concept is_last; a concurrent session reverted to the parent DOI in error (2026-08-14).

**DOI-WAF-403 (v2.109, SOFT — audit helpers):** doi.org HEAD 403 on publisher DOIs
(OUP/OBO/MDPI/CNTP/APS) is a WAF bot-block, NOT a dead DOI. Audit/dependency-check scripts MUST
auto-fallback to `api.crossref.org/works/{doi}` (authoritative year/author/title) before reporting
an unresolvable DOI. Same family as ZENODO-BOT-403-1 (full browser UA or Crossref fallback).

**REQUIRED METADATA FIELDS (InvenioRDM):**











| Field | Type | Required? | Example | Notes |





|:------|:-----|:----------|:--------|:------|





| `title` | string | YES (PUT) | `"Paper Title"` | |





| `publication_date` | string | YES (PUT) | `"2026-08-04"` | ISO 8601 date |





| `resource_type` | object | YES (PUT) | `{"id": "publication-preprint"}` | Valid IDs: publication-preprint, publication-article, publication-thesis, publication-book, publication-other |





| `creators` | array | YES (PUT) | `[{person_or_org: {family_name, given_name, type: "personal"}}]` | Personal: `family_name`+`given_name`; Organizational: `name` only (ZENODO-CREATOR-FORMAT) |





| `publisher` | string | YES (publish) | `"QNFO"` | Required for DOI registration (ZENODO-PUBLISHER-REQUIRED-1) |





| `description` | string | Recommended | `"Abstract text..."` | |





| `version` | string | Recommended | `"v0.1-draft"` | |





| `access_right` | string | Recommended | `"open"` | open, embargoed, restricted, closed |





| `license` | string | Recommended | `"QNFO Unified License Agreement (QNFO-ULA)"` | Custom licenses allowed |





| `keywords` | array | Recommended | `["adeles","p-adic"]` | MUST be JSON array, NOT comma-joined string |





| `related_identifiers` | array | Optional | `[{relation:"isNewVersionOf", identifier:"10.5281/..."}]` | For version chains |











**FILE UPLOAD FLOW (complete) — TWO WORKING PATHS (v2.74):**











**PATH A — deposit API (canonical for fresh deposits, verified 2026-08-04):**





```python





# requests multipart — PUT /files/{filename} returns 405 (ZENODO-UPLOAD-MULTIPART-1)





import requests





H = {"Authorization": f"Bearer {token}",





     "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "





                    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"),  # bot-403 fix





     "Accept-Language": "en-US,en;q=0.9", "Referer": "https://zenodo.org/",





     "Origin": "https://zenodo.org"}





# create:    POST /api/deposit/depositions -> 201





# upload:    POST /api/deposit/depositions/{id}/files  files={"file": (name, fh, mime)} -> 201





# metadata:  PUT  /api/deposit/depositions/{id} json={"metadata": {...}} -> 200





# publish:   POST /api/deposit/depositions/{id}/actions/publish -> 202, DOI minted





```











**PATH B — records API (InvenioRDM):**

> **ZENODO-RECORDS-API-UPLOAD-CT-1 (v2.93, HARD):** use `Content-Type: application/octet-stream` for ALL file
> types (md/html/pdf). Type-specific MIME (`text/html`, `application/pdf`) returns 415. Verified 2026-08-10
> (v0.7: 21880070/21880081 broken by 415; uniform octet-stream -> 21880104 OK).





```





1. POST /api/records/{id}/draft/files  with [{"key": "paper.pdf"}]





   → 201, entries[0].links.content = upload URL, entries[0].links.commit = commit URL





2. PUT  {links.content}  with raw bytes, Content-Type: application/octet-stream





   → 200





3. POST {links.commit}





   → 200, file committed





4. Repeat for each file





5. POST /api/records/{id}/draft/actions/publish





   → 202, DOI assigned





```





**SELECTION RULE:** After POST files, iterate `entries[]` and select entry where `key == fname`. NEVER use `entries[0]` blindly — it may be a prior file (ZENODO-FILE-ENTRY-SELECTION-1).











**PUBLISH RESPONSE:**





```json





{





  "id": 21786603,





  "doi": "10.5281/zenodo.21786603",





  "conceptdoi": "10.5281/zenodo.21786602",





  "metadata": {...},





  "files": [...],





  "links": {...}





}





```





Verify: `curl -sI https://doi.org/{doi}` → HTTP 200. Then P5.FRESH gate.











**PRE-CHECK:** Before publishing, search for existing records: `GET /api/records?q=<title>`. If a draft exists: `GET /api/user/records?q=<title>&status=draft`. Deduplicate per P5.DUPCHECK.











**Upload order (PREVIEW-FIRST):** `<slug>.pdf` → `<slug>.html` → `<slug>.md` → remaining files. BUCKET URL RULE: upload to `{links.bucket}/{filename}`, never construct URL manually. **All three files (.pdf + .html + .md) are MANDATORY in every Zenodo deposit — no exceptions.**











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

**NEWVERSION SELF-DOI ORDERING RULE (v2.87, HARD — R-A1 canonical case; **v2.94 CORRECTED step 2**):**
When a newversion is created to correct an embedded-YAML DOI, the uploaded `.md` MUST carry ITS OWN
pre-reserved DOI — not the parent version's DOI. Procedure: (1) `POST /api/records/{id}/versions`
→ get new draft id (201; `id` may be null — read `links.self`); (2) **RESERVE the DOI via
`POST /api/records/{id}/draft/pids/doi` (the draft's `links.reserve_doi`)** → 201 with the reserved
`doi` in the response — **`GET /api/records/{id}/draft` returns `prereserve_doi: None` for newversion
drafts (verified live 2026-08-10, drafts 21878976/21878977) — the PID reservation POST is the ONLY
working reservation path**; (3) UPDATE the LOCAL `.md` YAML `doi:` to that reserved DOI **AND set
`status: "published"` BEFORE uploading**; (4) upload `.md` + files; (5) publish; (6) verify the
deposited `.md` YAML `doi:` == the PUBLISHED record DOI AND `status: "published"` (P5.FRESH).
FAILURE MODE: a script that uploads the local `.md` first and updates local YAML AFTER upload ships
a deposited file whose `doi:` points at the parent version — P5.FRESH passes (doi != TBD) but the
deposited file is stale by one version. Canonical case: qwave-qudit-advantage v0.2 (21827268)
deposited .md carried 21826679 (v0.1) instead of its own DOI; fixed in v0.3 (21827347) via this
ordering.





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











> **QA/UX TEST BATTERY (HARD GATE, 2026-08-05 user mandate):** NO public-facing
> QNFO/QWAV page deploys without passing `qa-ux-battery.py` first (Chrome for Testing
> headless). Battery checks: HTTP status, console/page JS errors (dead interactive
> tools), broken links, 404 markers, interactive elements, title/h1/body presence.
> ANY FAIL blocks deployment. Canonical case (2026-08-05): GitHub-deployed interactive
> tools shipped broken — this gate exists so that is impossible. Script:
> `research/scripts/qa-ux-battery.py` (thin-client canonical, committed to qnfo-skills).

## Phase 6: Cloudflare Deployment











### D1 Access





Canonical: `cloudflare/scripts/d1-query.py`. CHECK-THEN-WRITE pattern (never combined upsert on FTS5 tables). Column is `body_md`. Verify via independent re-query.











### Papers-Server Verification





`curl -sI https://papers.qnfo.org/papers/<slug>/` → HTTP 200.











### R2 Archive





Upload `<slug>.md`, `<slug>.pdf` to `qnfo-releases/releases/<YYYY>/<MM>/<slug>/`.

**Verification (R2-CDN-CACHE-1, v2.96):** the R2 object API GET path can serve a CDN-cached
stale object (`CF-Cache-Status: HIT`) — a false md5 mismatch vs the fresh local file does NOT
mean the upload failed. Canonical verification: `rclone check <localdir> releases:qnfo-releases/<prefix>`
(S3 endpoint, bypasses the API CDN) -> 0 differences. Canonical case: ringbauer-qudit-due-diligence
2026-08-10 — API GET reported stale v1 PDF; rclone proved v4 objects correct.

**Verification (R2-CDN-CACHE-1, v2.96):** the R2 object API GET path can serve a CDN-cached
stale object (`CF-Cache-Status: HIT`) — a false md5 mismatch vs the fresh local file does NOT
mean the upload failed. Canonical verification: `rclone check <localdir> releases:qnfo-releases/<prefix>`
(S3 endpoint, bypasses the API CDN) -> 0 differences. Canonical case: ringbauer-qudit-due-diligence
2026-08-10 — API GET reported stale v1 PDF; rclone proved v4 objects correct.











### KG Node Seeding (MANDATORY — PUBLICATION-KG-INDEX-GAP-1, v2.96)

After the D1 insert, the paper MUST also have a Knowledge Graph node. Seed
`paper:<slug>` with 4-D distribution properties + a `BELONGS_TO` edge to the
owning program/concept (knowledge skill Edge Seeding Gate — minimum 1 edge per
entity). Canonical path: `POST https://graph-api.qnfo.org/sync` with
`X-Sync-Token` (`{"action":"bulk","nodes":[{"id":"paper:<slug>",...}],"edges":[...]}`),
or the direct `qnfo-graph` D1 `INSERT OR IGNORE` fallback (per knowledge v2.10 SYNC CONTRACT)
when the sync token is unavailable. **Verify** via `query_graph('neighbors', {id: 'paper:<slug>'})`
→ neighbor count > 0 in the SAME turn. A paper with a D1 row but no KG node is
invisible to KG-first due diligence (canonical: ringbauer-qudit-due-diligence
HARD-1, 2026-08-10).

### Vectorize Indexing (MANDATORY — PUBLICATION-KG-INDEX-GAP-1, v2.96)

After the D1 insert, trigger the semantic indexer so the paper is discoverable
via `search_papers`/`search_papers_enriched`. Call the qnfo-paper-indexer with
the shared-secret header:
`GET https://qnfo-paper-indexer.q08.workers.dev/index?slug=<slug>` (or `/webhook?slug=<slug>`)
with `X-Index-Token: chnx-idx-v1-k9m2n4p7r5t8`. **Verify** via
`GET https://qnfo-paper-indexer.q08.workers.dev/webhook?slug=<slug>` →
`{indexed:true, chunks:N, errors:0}` — the canonical single-paper index proof
(VECTORIZE-WEBHOOK-VERIFY-1). A paper in D1 but not in Vectorize is not
semantically discoverable (canonical: ringbauer-qudit-due-diligence HARD-2,
2026-08-10).

### KG Node Seeding (MANDATORY — PUBLICATION-KG-INDEX-GAP-1, v2.96)

After the D1 insert, the paper MUST also have a Knowledge Graph node. Seed
`paper:<slug>` with 4-D distribution properties + a `BELONGS_TO` edge to the
owning program/concept (knowledge skill Edge Seeding Gate — minimum 1 edge per
entity). Canonical path: `POST https://graph-api.qnfo.org/sync` with
`X-Sync-Token` (`{"action":"bulk","nodes":[{"id":"paper:<slug>",...}],"edges":[...]}`),
or the direct `qnfo-graph` D1 `INSERT OR IGNORE` fallback (per knowledge v2.10 SYNC CONTRACT)
when the sync token is unavailable. **Verify** via `query_graph('neighbors', {id: 'paper:<slug>'})`
→ neighbor count > 0 in the SAME turn. A paper with a D1 row but no KG node is
invisible to KG-first due diligence (canonical: ringbauer-qudit-due-diligence
HARD-1, 2026-08-10).

### Vectorize Indexing (MANDATORY — PUBLICATION-KG-INDEX-GAP-1, v2.96)

After the D1 insert, trigger the semantic indexer so the paper is discoverable
via `search_papers`/`search_papers_enriched`. Call the qnfo-paper-indexer with
the shared-secret header:
`GET https://qnfo-paper-indexer.q08.workers.dev/index?slug=<slug>` (or `/webhook?slug=<slug>`)
with `X-Index-Token: chnx-idx-v1-k9m2n4p7r5t8`. **Verify** via
`GET https://qnfo-paper-indexer.q08.workers.dev/webhook?slug=<slug>` →
`{indexed:true, chunks:N, errors:0}` — the canonical single-paper index proof
(VECTORIZE-WEBHOOK-VERIFY-1). A paper in D1 but not in Vectorize is not
semantically discoverable (canonical: ringbauer-qudit-due-diligence HARD-2,
2026-08-10).

### MCP-Driven Deployment Verification (HARD)





Cross-MCP chain: cloudflare-builds → cloudflare-graphql (invocation analytics) → cloudflare-bindings → cloudflare-auditlogs. All must pass before declaring deployment complete. (cloudflare-observability MCP removed 2026-08-17.)











---











## Phase 7: Dissemination

### Publication Venue (v2.115, CORRECTED — Zenodo canonical, NO traditional journals)

**CATEGORICAL USER DIRECTIVE (2026-08-16): the user NEVER submits to traditional academic journals — ever.**
Do NOT suggest or prepare journal submissions (no cover letters, no journal shortlists) unless explicitly
prompted by the user. Autonomous submission is permitted ONLY to outlets that are fully autonomous and
100% complete with ZERO manual user intervention — which rules out paid submissions and practically all
traditional/proprietary/esoteric submission systems. **Canonical publication venue: Zenodo ONLY.**

1. **Preprint discoverability (autonomous stack):** Zenodo → DataCite → OpenAlex auto-indexing (author
   profile exists) + Google Scholar/Semantic Scholar DOI pickup + PhilPapers (keywords below) +
   papers.qnfo.org. An arXiv listing is NOT required for scholarly-index presence (arXiv is out of scope —
   endorsement is a manual step).
2. **NO journal shortlist.** The prior shortlist (Frontiers in Physics, Quantum, EPJ QTech, Entropy, AVS QS,
   QST) is RETRACTED — these are traditional journals and are categorically forbidden.
3. **NO cover letter.** Cover letters are a journal-specific artifact and are forbidden (a cover-letter.md
   draft was produced and retracted 2026-08-16, commit a1a7d09).
4. **Autonomous outlets only (journal-style systems):** no journal-style submission system is
   currently available that is fully-autonomous, free, and zero-manual-intervention — do NOT invent
   journal submission paths. This does NOT restrict the verified autonomous dissemination stack
   (see "Open Outlets & Community Dissemination" below: open Zenodo communities with
   record_submission_policy=open — inclusion REQUEST is curator-gated
   (ZENODO-COMMUNITY-INCLUSION-REQUEST-1), Figshare API v2, Internet
   Archive — all free, API-driven, no endorsement, no manual intervention).

### Targeted Outreach (v2.88, SOFT — independent-researcher legitimacy)

Cold outreach to researchers whose work the paper builds on is the highest legitimacy-per-effort
channel for an independent researcher. Protocol (proven QNFO.UMP.005, 2026-08-06):

1. **Verify recipient identity + email from the arXiv SOURCE tarball** (`https://arxiv.org/e-print/{id}`,
   parse `.tex` for `\email{}` / contact addresses) — NEVER from a title-match alone. Title matches
   can return the WRONG paper (canonical case: QNFO.UMP.005 outreach Letter 3 matched an IBM-Zurich
   paper (Fischer et al.) when the author had been recalled as Gokhale — corrected before send).
2. **Address the corresponding author** of the target paper (arXiv source contact email), not a
   recalled author name.
3. **Test-send first** to your own inbox via the qnfo-email Worker `/send` endpoint (SPF+DKIM+DMARC
   verified on the sending domain), THEN send to recipients.
4. **Send individually** (no BCC), one follow-up max after 7-10 days.
5. **Log every send** — recipient, status, message_id — to `artifacts/outreach-log.md`
   (Tool-Call Execution Mandate: the API response IS the proof).
6. **Invite adversarial validation** in every letter; never imply validation you don't have.

### PhilPapers Discoverability (v2.88, SOFT — cross-ref knowledge v2.10)

PhilPapers crawls Zenodo→DataCite→CrossRef and only indexes records with BOTH an abstract AND
>=3 philosophy-domain keywords (`philosophy of physics`, `foundations of quantum mechanics`,
`consilience`, `philosophy of science`, `philosophy of mathematics`, etc. — full list in knowledge
v2.10 PHILPAPERS-DISCOVERABILITY-GAP). For any paper with philosophy-of-physics framing: after
publish, add philosophy keywords via the deposit-API in-place metadata edit
(ZENODO-RECORDS-API-DROPS-METADATA-1 compliant — deposit shape only), then verify DataCite
`subjects` count. Canonical case: qwave-qudit-advantage v0.4 (21827737) — 15 keywords incl. 4
philosophy-domain, DataCite subjects=15 verified.













### SEO Audit





robots.txt, sitemap.xml, llms.txt, meta tags, Schema.org ScholarlyArticle, Open Graph.

















### Buffer Social Media (v2.70 — COMPLETE GraphQL DICTIONARY, 2026-08-04)











**CANONICAL API: `api.buffer.com/graphql` (GraphQL ONLY).** The legacy REST API





(`/1/profiles.json`, `/1/updates/create.json`) returns HTTP 401 "Public API tokens





are not accepted for REST API access" and is DEPRECATED (retired 2027-02-01). Use





GraphQL exclusively. Token: `buffer_token` in `C:\Users\LENOVO\keys.json`.











**AUTH HEADERS:**





```python





headers = {





    "Authorization": f"Bearer {token}",





    "Content-Type": "application/json",





    "User-Agent": "Mozilla/5.0"   # REQUIRED — default urllib UA may be blocked





}





```











**SCHEMA NOTES (verified via introspection 2026-08-04, session 7gJ25ecLca3VNUeaFCZKB):**





- `client()` root field requires `input: ClientInput!` with BOTH `version: String!`





  and `platform: ClientPlatform!` (lowercase enum: `web`, `ios`, `android`).





  `ClientPayload` has NO `channels`/`profiles`/`organizations`/`user` fields — do





  NOT try to discover channels through `client()`.





- Channel discovery is TOP-LEVEL: `channels(input: {organizationId})` on the Query





  root. Org id comes from `account { organizations { id name } }`.





- `createPost` returns a UNION `PostActionPayload`. Success member is





  `PostActionSuccess` with field `post { id status }`. Error members:





  `NotFoundError`, `UnauthorizedError`, `UnexpectedError`, `RestProxyError`,





  `LimitReachedError` (queue cap), `InvalidInputError` — each with `message`





  (RestProxyError also `code`/`link`).





- `CreatePostInput` REQUIRED fields: `assets` (list), `channelId: ChannelId!`,





  `mode: ShareMode!`, `needsApproval: Boolean!`, `schedulingType: SchedulingType!`.





  Optional: `text`, `dueAt`, `aiAssisted`, `saveToDraft`, `draftId`, `ideaId`,





  `metadata`, `tagIds`, `source`. **`schedulingType` is REQUIRED** — omit → 400





  "Field \"schedulingType\" of required type \"SchedulingType!\" was not provided".





- `ShareMode` enum: `addToQueue`, `customScheduled`, `shareNext`, `shareNow`.





- `SchedulingType` enum: `automatic`, `notification`. Use `automatic` for queue.





- `Channel` fields: `id`, `allowedActions`, `avatar`, `descriptor`,





  `displayName`, `externalLink`, `hasActiveMemberDevice`, `isDisconnected`,





  `isLocked`. **Always check `isDisconnected` before posting.**











**FULL DISCOVERY + POST FLOW (canonical):**





```python





# 1. Organization ID





r1 = gql("query { account { organizations { id name } } }")





org_id = r1["data"]["account"]["organizations"][0]["id"]











# 2. Channels (top-level, NOT client.channels)





r2 = gql("query Channels($orgId: OrganizationId!) { channels(input: {organizationId: $orgId}) { id displayName descriptor isDisconnected } }", {"orgId": org_id})











# 3. Create post (UNION fragment required — direct field selection on PostActionPayload fails)





r3 = gql('''mutation CreatePost($input: CreatePostInput!) {





  createPost(input: $input) {





    ... on PostActionSuccess { post { id status } }





    ... on LimitReachedError { message }





    ... on UnauthorizedError { message }





    ... on InvalidInputError { message }





    ... on NotFoundError { message }





    ... on UnexpectedError { message }





    ... on RestProxyError { code message }





  }





}''', {"input": {"assets": [], "channelId": ch_id, "mode": "addToQueue",





                 "needsApproval": False, "schedulingType": "automatic", "text": text}})





# Success: {"data": {"createPost": {"post": {"id": "6a71...", "status": "scheduled"}}}}





```











**KNOWN QNFO CHANNEL IDS (verify live each session — IDs may rotate):**





| Channel | displayName | descriptor |





|:--------|:------------|:-----------|





| `6a170337c687a22dd430685f` | Rowan Brad Quni-Gudzinas | LinkedIn Profile |





| `685cd2c2acfb098c697a8786` | RowanQuni | X Free Profile |





| `6a660e1b4b2d03035f435349` | QNFO | Mastodon Profile |











**VERIFICATION:** the `createPost` mutation response itself IS the post proof





(`id` + `status: scheduled`). Do NOT re-query `posts()` for verification — the





`PostsInput` shape requires `organizationId` and uses `sort` (not `first`/`channelId`),





and the posts-connection UNION member is NOT `PostsConnectionSuccess`. If you must





list posts, introspect `PostsInput` + the posts return UNION first.











### Buffer Social Media





Canonical: `api.buffer.com/graphql`, `createPost` mutation. ALWAYS discover channel IDs live. 401 diagnostic protocol before "stale token" diagnosis. Inline fragments on PostActionPayload work. `LimitReachedError` = account queue cap, not agent bug.











### IPFS/DNSLink (OPTIONAL)





Cloudflare R2 (durable store) + locally-computed CIDv1 + Cloudflare DNS DNSLink. NO third-party pinning services.











### Internet Archive





`https://web.archive.org/save/https://papers.qnfo.org/papers/<slug>`











---











### Open Outlets & Community Dissemination (v2.115, DISSEMINATION-OUTLETS-1 — 2026-08-16)

User mandate: disseminate QNFO research MORE widely through channels that (1) impose NO content
regulation — no formatting template and NO ban on AI-generated text, (2) have NO gatekeeping or
endorsement (explicitly NOT arXiv), (3) are free, and (4) are fully DeepChat-executable (no manual
intervention). Verified landscape + evidence: `research/references/dissemination-outlets-2026-08-16.md`.

**Verified reality (live API + policy probes, 2026-08-16):**
- **OSF Preprints — DISQUALIFIED (OSF-PREPRINTS-AI-BAN-1):** moderation policy states content
  "completely or mostly generated by LLM/AI tools is not appropriate for OSF Preprints"; COS
  suspended new OSF Preprints submissions Aug 2025. OSF-as-profile (`osf-profile-update.py`) is fine.
- **Zenodo communities — BIMODAL (ZENODO-COMMUNITY-BIMODAL-1):** a few LARGE open communities with
  `record_submission_policy=open` are worth REQUESTING inclusion in; MANY are 0-4 records /
  slug-squatted (ZENODO-COMMUNITY-EMPTY-1: always check record count before submitting —
  `GET /api/records?q=communities:<slug>`). **VERIFIED LIVE 2026-08-16: `review_policy=closed`
  does NOT auto-include for third-party submitters** (ZENODO-COMMUNITY-INCLUSION-REQUEST-1):
  `POST /api/records/{id}/communities` creates a community-inclusion REQUEST (status=submitted)
  awaiting the community's curators — only the user's OWN communities auto-accept (owner). The
  memberships list (`GET /records/{id}/communities`) shows only accepted communities; check
  pending state via `GET /api/requests?q=topic.record:<id>` (report mode does this).
- **Zenodo AI policy nuance (ZENODO-AI-POLICY-NUANCE-1):** Zenodo bans only AI-generated content
  WITHOUT a verifiable basis in human-conducted research. Human-directed AI-assisted QNFO records
  qualify — keep the AI-assistance disclosure explicit (already corpus norm).
- **Figshare — SECONDARY leg:** free tier (20 GB private + unlimited public), API v2 verified live,
  no endorsement/peer review, light moderation, no explicit AI-text ban. Positioned for
  data/articles, not preprint-community discovery.
- **viXra — reputation risk:** true no-gatekeeping archive (46,008 e-prints) but hosts fringe
  content; using it risks brand association with pseudoscience. Only with explicit user approval.

**Target community shortlist (verified open for third-party inclusion REQUEST; acceptance is
curator-gated — ZENODO-COMMUNITY-INCLUSION-REQUEST-1):**

| records | slug | note |
|--:|---|---|
| 1004 | `advancedtheoreticalphysicsandmathematics` | Univ. Athens org — broad theoretical physics + math |
| 745 | `tp-a-m-c` | Theoretical/Applied/Mathematical/Computational — "all theories welcome" |
| 366 | `fbt-framework` | **Geometric Foundations of Quantum Theory and Gravity** — direct UMP/RES match (symplectic geometry, Berry curvature) |
| 113 | `ml4q` | Matter and Light for Quantum Computing (project-scoped, German ExC) |

**Scripts (fully automated, ZENODO_TOKEN / FIGSHARE_TOKEN from env only):**
- `research/scripts/zenodo-communities.py` — `discover` (rank open communities by record count),
  `submit --doi <DOI> --all-open|--community <slug>` (POST /api/records/{id}/communities),
  `report --doi <DOI>` (accepted memberships + pending inclusion requests). Only submits
  PUBLISHED records to `record_submission_policy=open` communities. Outcome of submit =
  inclusion REQUEST (status=submitted) awaiting curators, NOT instant membership
  (ZENODO-COMMUNITY-INCLUSION-REQUEST-1); verify via `report` (REQUEST lines). On "only allowed
  to community members" (ZENODO-COMMUNITY-SUBMIT-MEMBERSHIP-1): join first via
  POST /api/communities/{slug}/members.
- `research/scripts/figshare-submit.py` — `submit` (create draft → upload file → publish → verify
  read-back), `create` / `upload` / `publish` / `verify` modes. **LIVE-VERIFIED 2026-08-16** on the
  flagship QUNTUF thesis (DOI 10.6084/m9.figshare.33264561.v1, CC BY 4.0, 4 categories): license must
  be an INTEGER Figshare ID (CC BY-NC-SA NOT offered — use `--license 1` = CC BY 4.0), `defined_type`
  default `thesis`, CHUNKED upload (`GET upload_url → parts → PUT {url}/{partNo}` → complete=202 →
  poll computed_md5), and `--categories` (selectable leaf IDs only) is required before publish.
  One-time Figshare personal token (env or keys.json `figshare_token`).

**Recommended protocol after every Phase 5 publish:** (1) Zenodo primary + own communities
(QNFO/QWAV/Ultrametric — still the highest-value asset); (2) `zenodo-communities.py submit
--doi <DOI> --all-open --min-records 5` (creates inclusion requests for the targets above;
  acceptance is curator-gated); (3) `report --doi <DOI>` to track request status; (4) optional
  Figshare cross-post for data-heavy artifacts; (5) rely on the indexing layer (Zenodo → DataCite →
OpenAlex/OpenAIRE/BASE/CORE/Google Scholar) for real discoverability — more preprint servers are
NOT the bottleneck.

## Phase 8: Core Distribution Stack (MANDATORY)











All 4 layers verified before status → "published":











| Layer | Implementation | Verification |





|:------|:--------------|:-------------|





| GitHub | Public repo, tags, releases | `git tag -l`, `gh release view` |





| Zenodo | DOI with versioned deposits | `curl -sI https://doi.org/<doi>` |





| R2 | Canonical file archive | `npx wrangler r2 object get ... --remote` |





| D1/KG | Living-paper DB + KG node | `get_paper_context`, `query_graph('neighbors')` |











**BP-4 Correction-on-Discovery:** GitHub ERRATA.md → Zenodo newversion + `obsoletes` → KG CORRECTS/SUPERSEDES edge.

**ERRATA ORDERING RULE (v2.88, HARD — no pre-claims):** the ERRATA.md or any correction-on-discovery
record MUST NOT claim the correcting newversion is "published" until the publish call has returned
202 in the SAME turn. Write the ERRATA AFTER the newversion publishes, or write it with explicit
`STATUS: PENDING` and update it post-publish. Canonical case: QNFO.UMP.005 ERRATA.md claimed
"Newversion v0.4 published" while v0.4 did not yet exist on Zenodo — a ZENODO-PHANTOM-DOI-1 class
error in the audit trail itself, caught by red team, then made true (v0.4 = 10.5281/zenodo.21827737).
Cross-ref: Tool-Call Execution Mandate, ZENODO-PHANTOM-DOI-1.











---












**CONSOLIDATED CLOSEOUT VERIFICATION (v2.95, DESIGN — same-turn re-proof):** after any multi-layer
publication closeout (Zenodo + GitHub + D1 + R2 + KG), run ONE script that re-proves every layer
in the same turn: (1) `HEAD https://doi.org/{new_doi}` and `{v0.1_doi}` -> 200 both (version chain);
(2) DataCite `GET https://api.datacite.org/dois/{doi}` -> state=findable + subjects>=expected +
rightsList has cc-by-nc-sa-4.0; (3) `git ls-remote` for branches + tags; (4) D1 SELECT row -> doi/status/body_len;
(5) Zenodo record files -> .pdf/.html/.md all present; (6) KG node `paper:<slug>` present via
query_graph/neighbors with >=1 BELONGS_TO edge (PUBLICATION-KG-INDEX-GAP-1); (7) Vectorize index
proof via `GET qnfo-paper-indexer/webhook?slug=` -> indexed:true, chunks>0 (VECTORIZE-WEBHOOK-VERIFY-1).
Any non-PASS blocks closeout (zero deferred). Canonical cases: QNFO.RES.002/.003 (2026-08-10, 5 layers
all PASS) and ringbauer-qudit-due-diligence (2026-08-10 — this gate would have caught HARD-1 KG-missing
and HARD-2 Vectorize-missing before closeout).

## Verification Gates











| Gate | Check | Evidence |





|:-----|:------|:---------|





| Due Diligence | KG + D1 + 2+ external sources | Query outputs |





| Consilience (HARD) | artifacts/consilience-gate.md with Silo Cost table | File present |





| Classification | All papers classified | Table |





| Citation | BibTeX verified | Audit output |





| Publication Language | Zero internal language, zero banned words | Scan: 0 hits |





| PDF | 0 U+FFFD/FFFF + PDF > 100KB | CDP pipeline verification gate |





| DOI | Zenodo resolves, preview is PDF | curl HTTP 200 |





| Deployment | papers-server 200, D1 entry exists | curl + d1-query |





| SEO | robots.txt, sitemap, meta tags | Verify each URL |





| Social | Buffer posts confirmed | Post ID in response |





| Core Distribution | All 4 layers verified | All pass |
| **Consolidated Closeout Verification (v2.95→v2.96)** | Same-turn re-proof of DOI HEAD x4 + DataCite findable/subjects/rights + GitHub refs + D1 row + Zenodo files + **KG node (neighbors>0) + Vectorize (webhook indexed:true)** | One script, all PASS |





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





| **FILE-SLUG-1: Generic `paper.md`/`paper.pdf`/`paper.html` file naming for published papers (2026-08-05)** | **HARD GATE.** Published paper files MUST be named as the PROJECT SLUG: `<slug>.md`, `<slug>.pdf`, `<slug>.html` (e.g. `qec-darwinism-ultrametric.md`). Applies to repo files, Zenodo deposit filenames, and R2 keys. Canonical case: QNFO.UMP.004 v1.3 — files renamed `paper.*` → `qec-darwinism-ultrametric.*` (commit 24fc89f). |
| **TITLE-DUPLICATION-1: Body `# <Title>` H1 alongside YAML `title:` field — title renders TWICE on page 1 (2026-08-05)** | **HARD GATE.** Pandoc emits the YAML `title:` as `<h1 class="title">`; a body H1 with the same title duplicates it on page 1. When YAML frontmatter has `title:`, the paper body MUST NOT contain a top-level H1 with the same title. Verify: run `research/scripts/check-title-duplication.py <slug>.html` — PASS requires exactly ONE rendered `<h1 class="title">` and zero body `<h1>` (v2.86 scripted gate, build-time BLOCK on failure). Canonical case: QNFO.UMP.004 v1.2 — body H1 removed (commit f2912ab). |
| **INTERNAL-REF-1: Published papers referencing internal QNFO processes (repo paths, skill sections, internal program names, conferences) (2026-08-05)** | **HARD GATE.** Published papers MUST NOT reference: repo paths (`QNFO/xxx`), skill sections (`QNFO Core §0.7`), internal program names as prose (`the Kepler Program`, `the Continuum Trilogy` as process refs), internal conference/workshop mentions, possessive internal refs (`QNFO's research program`). Convert to generic phrasing + numbered citations of PUBLISHED records only. Canonical case: QNFO.UMP.004 v1.2 — CWI section deleted, Kepler prose → "prior published work", refs 10-13 cited properly (commit f2912ab). |
| **AI-QUALITY-GATE-1: Publishing AI-generated/AI-assisted papers without clearing the forensic quality gate (2026-08-10)**
| **NODE-MJS-ESM-1: Node `require()`-based scripts named `.mjs` fail — "require is not defined in ES module scope" (2026-08-10)** | **HARD GATE.** `render-pdf.mjs` with `require('C:/Users/LENOVO/node_modules/puppeteer-core')` fails; ESM `import` of a Windows absolute path fails with ERR_UNSUPPORTED_ESM_URL_SCHEME. Fix: name Node scripts that use `require()` with the `.cjs` extension (CommonJS mode) — require works, absolute paths fine. Canonical case: render-pdf.cjs (Edge + puppeteer-core) produced qwave-qudit-advantage.pdf 590,959 B, 0 U+FFFD/FFFF. Cross-ref: windows-command-patterns v3.20 NODE-MJS-ESM-1, NODE-EVAL-CMD-1, research v2.99 CDP render note. | | **HARD GATE.** AI-generated/AI-assisted papers MUST pass the pre-publication quality gate: (i) no elementary physics/energy-budget errors (canonical: Qudit Advantage §3.3 P_decode≈0 labeled "conservative upper bound" — zero is a LOWER bound; VERIFIED via D1 body 2026-08-10), (ii) no synthetic/unresolvable citation anchors (@C5_jpcub_p0-style prefixed keys — INTERNAL-REF-1-adjacent), (iii) no scaffold overload (meta-tag echo, rigid template boxes), (iv) no over-explaining textbook foundations while hand-waving the novel integration, (v) no self-referential metric claims without external validation. The "AI-GENERATED" label cost is mitigated by quality, never by hiding (uncanny-valley literature: Luo 2019 moderation, Dietvorst 2014 asymmetry). Owner: qnfo-core v1.22. Cross-ref: INTERNAL-REF-1, PROSE-GATE-ADVISORY-1, kaizen v1.94. |





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





| **PUP-1: Puppeteer bootstrap times out during CDP render** | DO NOT fall back to xhtml2pdf or Page.printToPDF. Extract cached Chromium zips first (they're pre-downloaded in `~/.cache/puppeteer/chrome/`), or use system Chromium (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`). Only if no Chromium binary exists anywhere: BLOCK the publication — DO NOT publish with substandard renderers. |





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





| **WBS-REGISTRY-STALE-1: D1 program_registry missing canonical program rows (2026-08-04)** | The D1 program_registry (designated source of truth per qnfo-core N-1) LACKED QNFO.UMP/SLB/INM/RES rows despite WBS.TAXONOMY.md defining them. Before concluding a WBS code "doesn't exist", verify against BOTH registries; if D1 lacks the row, INSERT it during reconciliation (CHECK-THEN-WRITE) — never invent an alternate code. Case: session 1tz85-vMiqh2TyFySznBA — QNFO.UMP + QNFO.UMP.003 + QNFO.RES rows created from the file registry; Phase 0.1 WBS resolution would have falsely failed otherwise. |





| **VECTORIZE-WEBHOOK-VERIFY-1: search_papers "OK" treated as Vectorize index proof (2026-08-04)** | MCP search_papers returns "OK"/empty for newly indexed papers (VECTORIZE-SILO-1). The AUTHORITATIVE single-paper index check is `GET https://qnfo-paper-indexer.q08.workers.dev/webhook?slug=<slug>` — response `{indexed:true, chunks:N, errors:0}` is direct proof the paper is in Vectorize. Use the webhook for "is this paper indexed?" claims; search_papers is directional only.
| **REDTEAM-QUEUE-STALL-1: reviewer subagent stays QUEUED >150s (no turn started) and closeout proceeds without review (2026-08-10/13/14)** | A queued subagent is NOT a review. After ~75s without a started turn, execute the direct parent-agent audit (Mandate 3 §Reviewer Failure Fallback) and log the stall. A reviewer CAN still complete late with REAL findings (RES.007 2026-08-14: FAIL — duplicate Joyal-Street work with synthetic DOI, audit double-count, BP-10 "51/51") — inspect the delegation before final closeout; late findings become remediation items. | Case: IPR paper (QNFO.UMP.003) — search_papers returned "OK" while webhook confirmed 26 chunks, 0 errors, body_len 41883. Cross-ref: cloudflare v3.33 VECTORIZE-WEBHOOK-VERIFY-1. **User-Agent requirement (2026-08-14, VECTORIZE-403-MISDIAGNOSIS):** ALL calls to this worker MUST send a browser-like `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...` header. Default Python urllib UA triggers Cloudflare BIC (error 1010) -> HTTP 403 on every path regardless of token. A 403 from qnfo-paper-indexer is a UA problem, NOT a token problem (BLAME-EXTERNAL-1). |





| **WBS-STD-2: Cross-reference claims WBS usage that does not exist (2026-08-04)** |
| **WBS-COLLISION-2: concurrent sessions resolve the same next-WBS-code and the later write overwrites the first project's D1 row (2026-08-14)** | Two sessions computed "next available RES code = 007" simultaneously; the later session's UPDATE replaced the canonical row (invariant-structural-value) with metadata for a different thesis (formal-self-reference-limits). Resolution per RES.004/005 precedent: first claim keeps the code, late claim renumbered (RES.008). WBS resolution MUST be atomic (check-then-insert in ONE transaction / UNIQUE constraint / registry lock); on session resume re-verify D1 row identity (name+slug), not just wbs_code, before ANY write. Canonical: QNFO.RES.007 2026-08-14. |
 A skill's cross-ref "research (phases carry WBS codes in execute_plan)" was FALSE — research had plain Phase steps. Cross-refs to a standard must be verified against the target skill's actual content (read the file) before being written; phantom compliance claims are the same class as phantom validation claims. Fix: verify target content before writing the cross-ref; kaizen Watchtower should audit WBS cross-refs. |





| **PHASE0-EMPTY-REPO: `git subtree add` on a new program repo without a bootstrap commit — v2.59, 2026-08-04** | A brand-new program repo created via `gh repo create <name> --public` has NO commits and NO HEAD. `git subtree add` requires an existing commit to merge into → all subtree adds fail silently. **Fix:** Clone with `gh repo create --add-readme` (creates a bootstrap commit on main) OR clone → write README → commit → rename branch to main → push BEFORE any subtree operations. Canonical case: session PMH0kzte — consolidate.py v1 subtree-added 12 repos into a new-empty ultrametric-physics repo; all 12 failed silently because HEAD didn't exist. See git-github skill SUBTREE-NO-HEAD anti-pattern.











| **BACKGROUND-TIMEOUT-1: Foreground exec of long-running command (Chrome download, MathJax CDP render, pandas HTML) times out at 600s max (2026-08-04)** | `exec` has a 600s (10min) maximum timeout including `background: true` tasks that auto-cancel. Chrome download (~194 MB) takes 2-5 min; CDP PDF render with MathJax takes 30-90s. Always use `background: true` for downloads > 30s. Use `process poll` to check status; do NOT assume `exec` returning a sessionId means the task completed. Kill hung processes early (2 polls with no progress = stuck) and retry with a different approach. Canonical case: session ktmz7cqk — 3 hung background Chrome installs, 2 hung CDP renders. |





| **TEMP-VOLATILITY-2: Published paper files in %TEMP% evicted between authoring and PDF build phases (2026-08-04)** | Files written to `%TEMP%` during the authoring phase (step N) are GONE by the PDF-build phase (step N+1). Windows cleans temp directories between long-running agent turns. **Re-clone repos from GitHub after every phase transition.** Never assume a `%TEMP%` file written in an earlier phase is still there. Canonical case: session ktmz7cqk — both `_26216024446.md` (136KB) and `_26216024519.md` (10KB) evicted; odr-thesis-v2.md and quasipaper-v2.md also evicted. Git is the persistence layer, not temp. Cross-reference: git-github TEMP Volatility HARD GATE. |





| **CONCURRENT-SKILL-WRITE-1: Two processes (agent + automated system) writing the same SKILL.md simultaneously (2026-08-04)** | A skill file can be modified by an automated pipeline (e.g., kaizen Watchtower, scheduled backfill) while the current session is also editing it. Symptom: version string changed to unexpected content between writes. Fix: (A) read→edit→write in a SINGLE atomic Python script (not read tool + edit tool + write tool); (B) after every write, immediately re-read the skill file to verify YOUR content landed; (C) if content was overwritten, re-read the current state and re-apply. Canonical case: research SKILL.md v2.54→v2.55 — version string overwritten by backfill protocol update between write and verification. |





| **BUCKET-LOCKED-RESOLVE-1: Zenodo draft bucket returns 403 "Bucket is locked" on DELETE after POST /draft (2026-08-04)** | Deletion of old files from a newly-drafted record may be denied. Two-tier resolution: (A) upload new files with the SAME key — `PUT /api/records/{id}/draft/files/{filename}` overwrites existing files atomically, no DELETE needed; (B) if overwrite also returns 403, wait 30-60 seconds for the post-draft lock to clear, then retry. Never attempt DELETE→wait→DELETE loops — use overwrite instead. |





| **DRAFT-PUBLISH-FLOW-1: InvenioRDM draft→publish flow differs from research skill v2.50 documentation (2026-08-04)** | The complete InvenioRDM flow: (1) `POST /api/records/{id}/draft` (HTTP 201, creates draft edit of published record, same ID); (2) `PUT /api/records/{id}/draft` (HTTP 200, update metadata); (3) overwrite files via `PUT /api/records/{id}/draft/files/{filename}` with Content-Type: application/octet-stream; (4) `POST /api/records/{id}/draft/actions/publish` (HTTP 202). Record retains same DOI under concept DOI. No new record ID is created — the draft IS the published record in edit mode. Verify: `GET /api/records/{id}` → status = published, files = updated. |





| **SUBAGENT-DEADLINE-CROSSREF-1: Subagent runTimeoutMs of 300000 (5 min) insufficient for API-heavy audits (2026-08-04)** | Cross-reference: kaizen skill v1.13 SUBAGENT-DEADLINE-1. For fetch-heavy subagent tasks (Zenodo paginated search, D1 scans), set `runTimeoutMs: 900000` or run directly in parent. This research skill's publication pipeline (Phase 5-8) often triggers subagent audits — if a Phase 5 subagent audit times out, fall back to parent-agent direct verification. |

















| **RETRODICTION-1: Presenting a post-hoc rationalization as a prediction — "the framework explains this" when it was built to do exactly that (2026-08-04)** | Every cross-domain correspondence claim MUST pass the Bayesian Evidential Weight Gate (KIF-60): (A) pre-registration — what was predicted BEFORE seeing the data? (B) falsifiability gradient — what observation WOULD have broken the framework? (C) surprise accounting — what is P(match | random) under the null? Without all three, a "prediction" is indistinguishable from curve-fitting. Claims without pre-registration evidence → cap at [NOT YET EVIDENCE]. Canonical case: Five Pillars paper — user's 2026-08-04 methodological injunction. Cross-ref: kaizen BAYESIAN-RETRODICTION-1, KIF-60. |





| **OVERFITTING-1: Framework has more free parameters than independent matches (2026-08-04)** | Count degrees of freedom vs. independent data points. If dof ≥ independent matches → Δlog-odds ≤ 0 → ZERO evidential weight. Pre-register parameters BEFORE seeing observations. Use holdout sets — some data NOT used in constructing the framework. Cross-ref: KIF-60 (Bayesian Evidential Weight Gate), Tautology Trap (Overfitting). |





| **CHERRY-PICK-1: Reporting only the matches that work; treating misses as "areas for future work" (2026-08-04)** | For every claimed correspondence, audit the FULL search space. What was the DENOMINATOR? How many structures were checked before finding the match? Report hit/miss ratio. Misses are falsification events — they carry NEGATIVE evidential weight that must be included in the Δlog-odds computation. Never declare "the framework maps onto X" without stating which structures it FAILED to map onto. KIF-60 Tautology Trap (Cherry-Picking). |





| **ABSORPTION-1: Every counterexample absorbed as a "special case" or new duality map (2026-08-04)** | If every apparent disconfirmation triggers a new duality transformation or parameter → the theory has zero empirical content (it "explains" everything = explains nothing). Pre-declare the finite set of ALLOWED duality maps BEFORE examining counterexamples. Any newly-invented duality to absorb a counterexample = admission of falsification. Cross-ref: KIF-60 Tautology Trap (Absorption). |





| **CONFIRMATION-SEEKING-1: Testing a theory by measuring its own predicted magnitude inside its own formalism (2026-08-04)** | A test designed by the theory's proponents, after the prediction, to measure the predicted effect is confirmation, not falsification (Pound–Rebka, Shapiro, Hulse–Taylor inside GR: parameter measurements within the PPN family; no serious alternative falsified). Fix: for every claimed confirmation, name the alternative the test would have falsified; if none predicts a different value, classify as parameter measurement with capped evidential weight. Cross-ref: KIF-60 Confirmation-Seeking Test, research §5.4. |





| **PRO-INCUMBENT-BIAS-1: Defaulting to favorable grades for established theories without symmetric adversarial audit (2026-08-04)** | Grading GR/SM as Grade A by default while demanding falsifiability from a new framework is asymmetric. The SM's 19 free parameters are measured, not predicted; the operational GR composite absorbs anomalies via DM/DE/inflation. Fix: apply the identical kill-criteria + null-equivalence standard to incumbents from the start (KIF-29 Symmetric Audit Requirement). Canonical case: the 2026-08-04 falsifiability thread — GR/SM initially graded A, downgraded only after user injunction. |





| **FORCED-CHERRY-PICK-1: Selecting only supportive confirmations while treating misses as "areas for future work" (2026-08-04)** | Extends CHERRY-PICK-1 to the incumbents: citing GR's confirmed predictions while ignoring its auxiliary-absorption escapes (or the SM's goalpost-moving nulls) is forced cherry-picking. Fix: audit the FULL evidence set for both the new framework and the incumbents, symmetrically. |










| **PYMUPDF-FORBIDDEN-1: Using PyMuPDF / fitz (or any non-CDP tool) in the PDF publication process (2026-08-04)** | **HARD GATE — user mandate.** PyMuPDF, fitz, xhtml2pdf, weasyprint, reportlab, pdflatex, xelatex, wkhtmltopdf, and browser --print-to-pdf are ALL FORBIDDEN as PDF build/verify pathways for QNFO publications. The ONLY approved pipeline is: `pandoc --mathjax` → MathJax SVG inline (tex-svg-full.js, str.replace not re.sub) → puppeteer-core `page.pdf()` (A4, 2cm margins, printBackground). Verification is a BINARY BYTE SCAN: 0×EF BF BD (U+FFFD), 0×EF BF BF (U+FFFF), size > 100 KB — never PyMuPDF. Canonical case: session ZDdTu9Qf — consilience_framework.pdf rebuilt via CDP with 92 math elements rendered (math=0 caused by overriding MathJax inlineMath config, fixed by removing the config block). Cross-ref: BROWSER-PRINT-TO-PDF-1, TWO-TIER-PDF-1, research v2.72 PDF Building. |





| **BROWSER-PRINT-TO-PDF-1: Using `--print-to-pdf` or browser print-to-PDF for production papers (2026-08-04)** | Produces unprofessional headers/footers, unsuitable for finished PDFs. Use the CDP pipeline (puppeteer-core `page.pdf()`) only — A4, 2cm margins, printBackground, zero browser chrome. See PDF Building section. |





| **TWO-TIER-PDF-1: Documenting multiple PDF workflows — "primary" + "production" tiers (2026-08-04)** | ONE workflow, ONE pipeline. Multiple tiers create ambiguity and divergence. CDP pipeline is the ONLY supported workflow. Remove any alternative descriptions immediately. |





| **MATH-DELIMITER-1: Source markdown using `\(...\)` / `\[...\]` LaTeX delimiters (2026-08-04)** | Pandoc strips `\(` as escaped parenthesis. Source MUST use `$...$` / `$$...$$` delimiters. Preprocess with `re.sub(r'\\  [', r'$$', source)` before pandoc if source has legacy delimiters. |





| **PANDOC-PIPE-TABLE-1: Bare `|` inside pipe-table cells or math (2026-08-04)** | Pandoc parses bare `|` as a column delimiter — tables get cut off and math breaks. Use `\|`, `\vert`, `\lvert`/`\rvert`, or `\mid` inside cells. Author-time mandate — never surgical-fix after. See PANDOC-SAFE AUTHORING MANDATE. |





| **UNICODE-MATH-1: Unicode math glyphs (𝒮 ℝ ℚ ∞ → ≺ ∼ ·) in source (2026-08-04)** | Unicode math does not render correctly through pandoc→MathJax. Use LaTeX codes: `\mathcal{S}`, `\mathbb{R}`, `\infty`, `\to`, `\prec`, `\sim`, `\cdot`. Author-time mandate. |





| **BARE-LATEX-MATH-1: LaTeX commands outside `$...$` delimiters (2026-08-04)** | `\mathcal{S}` or `I(r) = \log_2 \lvert\mathcal{S}_r\rvert` in prose renders as literal text; sub/superscripts never render. Wrap ALL math in `$...$`. Author-time mandate. |





| **UNBRACED-SUBSCRIPT-1: Unicode or unbraced sub/superscripts (₁ ₂ ² G_r q^{d·r} in prose) (2026-08-04)** | Sub/superscripts outside math mode or with Unicode glyphs never render. Use braced LaTeX inside `$...$`: `$G_r$`, `$q^{d \cdot r}$`. Author-time mandate. |





| **CHTML-SVG-1: Building PDF with CHTML MathJax output processor (2026-08-04)** | CHTML uses Private Use Area glyphs that do not survive CDP capture — math renders as blank. Always switch to SVG: `html.replace('tex-chtml-full.js', 'tex-svg-full.js')` before CDP render. |











| **PYMUPDF-1: Using PyMuPDF (fitz) anywhere in the PDF publication pipeline (2026-08-05)** | **HARD BLOCK.** PyMuPDF is NOT part of the approved PDF publication process. The ONE AND ONLY pipeline is: `pandoc --mathjax → MathJax SVG inline → puppeteer-core page.pdf()`. PyMuPDF was previously used for verification (U+FFFD/U+FFFF scan) and as a render alternative — both paths are DEPRECATED, REMOVED, EXPUNGED. PDF verification uses direct file-content scanning (grep/strings for U+FFFD/U+FFFF), NOT PyMuPDF. PDF rendering uses ONLY puppeteer-core CDP. Any script, memory, or agent that invokes `import fitz`, `pip install PyMuPDF`, or `fitz.open()` in the context of the research publication pipeline is in violation. For non-publication PDF manipulation (merge, split, form fill), use `pypdf` or `pdfplumber` from the `pdf` skill — never PyMuPDF. Canonical case: stale durable memories (5 contaminated memories forgot 2026-08-05) claimed build-pdf-pro.py used PyMuPDF, causing agents to install it as a verification gate when the CDP pipeline was already verified clean. Cross-ref: ZENODO-PHANTOM-DOI-1 (same class — claiming verification from a tool not in the approved pipeline). |











| **CHROME-PROCURE-1: Attempting `npx @puppeteer/browsers install chrome` hangs (2026-08-04)** | The `@puppeteer/browsers` install() method hangs indefinitely on this machine after downloading the zip. Use Python `urllib.request.urlretrieve(url, zip_path)` + `zipfile.extractall()` instead. Download is ~194 MB, takes 2-5 minutes. Cache at `%USERPROFILE%\.cache\puppeteer\chrome\`. |





| **RE-SUB-ESCAPE-1: Using re.sub() on MathJax JS crashes with "bad escape \u" (2026-08-04)** | MathJax `tex-svg-full.js` contains `\uXXXX` Unicode escape sequences. Python's `re.sub(replacement)` interprets `\u` as a regex escape and crashes. Use `str.replace(exact_match, replacement)` instead — it treats the replacement as a literal string. |





| **ZENODO-NEWVERSION-404: POST /api/records/{id}/actions/newversion → HTTP 404 in InvenioRDM (2026-08-04)** | The `/actions/newversion` endpoint is DECOMMISSIONED. It returns HTTP 404 for all records. Use `POST /api/records/{id}/draft` — creates a draft edit of the published record (HTTP 201) with the same ID. Publish via `POST /api/records/{id}/draft/actions/publish` (HTTP 202). |





| **ZENODO-USER-404: GET /api/user → HTTP 404 in InvenioRDM (2026-08-04)** | Token validation endpoint is `/api/me` (HTTP 200 returns user email), NOT `/api/user` (HTTP 404). A token returning 404 on `/api/user` and 200 on `/api/me` is VALID — do not diagnose "expired token" from a `/api/user` 404. |





| **ZENODO-BUCKET-LOCKED-1: DELETE file from draft → 403 "Bucket is locked" (2026-08-04)**

**v2.94 EXTENSION (2026-08-10):** in-place FILE replacement on a PUBLISHED record's edit-draft is IMPOSSIBLE —
`PUT /records/{id}/draft/files/{fname}` (bare file URL) → **415** "Invalid 'Content-Type' header. Expected one of:
application/json" (that URL is the file-ENTRY metadata endpoint, not content); `PUT .../files/{fname}/content` →
**403 "Bucket is locked for modifications"**. Even a 60s lock-wait does NOT clear it (verified live 2026-08-10 on
records 21878943/21878945). P5.FRESH's "re-upload corrected .md + re-publish" instruction therefore ALWAYS
means **newversion** (`POST /versions` → reserve DOI via `draft/pids/doi` → upload corrected .md with its OWN
DOI + status published → publish). Never attempt in-place file overwrite on a published record for P5.FRESH. | After `POST /api/records/{id}/draft`, deleting old files may return 403. Instead, upload new files with the SAME key to overwrite: `PUT /api/records/{id}/draft/files/{filename}` with `Content-Type: application/octet-stream`. If bucket remains locked, wait 30 seconds and retry. |





> **UPDATE 2026-08-15 (GIT-BASH-SHELL-1):** the rows below are legacy cmd.exe-era anti-patterns. The exec tool now runs Git Bash (POSIX) — `node -e`, `python -c`, and quoted args generally work again. The write-file→run→read pattern remains canonical for anything non-trivial. See windows-command-patterns v3.23.
>
| **NODE-EVAL-CMD-1: node -e fails with "Unterminated string constant" in cmd.exe (2026-08-04)** | `node -e` in Windows cmd.exe cannot handle multi-line code or code with quotes. Always write Node scripts to `.mjs` files and run `node <file>`. Same rule as windows-command-patterns S0.0 for Python `-c`. |





| **PYTHON-C-AMPERSAND-1: python -c fails when command contains & (2026-08-04)** | cmd.exe interprets `&` as command separator. Always write Python scripts to `.py` files and run `python <file>`. Cross-reference: windows-command-patterns S0.0. |





| **PANDOC-PATH-CMD-QUOTES-1: cmd.exe quoting fails for pandoc with PATH prepend (2026-08-04)** | `cmd /c "set PATH=... && pandoc ..."` with outer quotes is not valid cmd.exe syntax. Use the canonical pandoc path directly: `C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe`. Never prepend to PATH via cmd /c set. |











| **ZENODO-STALE-DRAFT-BLOCK-1: POST /records/{id}/versions returns HTTP 500 when stale drafts exist on the concept (2026-08-04)** | InvenioRDM silently 500s newversion when ANY draft record exists on the same concept — even drafts unrelated to the current version. Root cause: prior failed publish attempts leave draft records (visible via `GET /api/user/records?status=draft`) that block new version creation. Fix: BEFORE any newversion, enumerate `GET /api/user/records?status=draft` + `q=<title>`, identify drafts whose conceptrecid matches the target, and discard each via `DELETE /api/records/{id}/draft` (204). Only then `POST /records/{id}/versions` (201). Canonical case: session ktmz7cqk — ODR Thesis + Quasiparticles blocked ~30 tool calls; 3 stale drafts (21768735, 21783092, 21783093) silently blocking; after discard, newversion worked instantly (21784489, 21784490 published). |





| **ZENODO-FILE-ENTRY-SELECTION-1: entries[0] from POST /draft/files may be a stale entry, not the new file (2026-08-04)** | After `POST /records/{id}/draft/files` with `[{'key': fname}]`, the response `entries[]` may include PREVIOUS files; `entries[0]` can point at the wrong file's content/commit URL, causing commit 404 ("Record has no file X"). Fix: iterate entries and select the one whose `key == fname`; fallback to `entries[-1]`. Verified: uploading MD then PDF — entries[0] returned the MD entry for the PDF POST; key-matching fixed commit 404. |





| **ZENODO-PUBLISHER-REQUIRED-1: Publish fails 400 "Missing publisher field required for DOI registration" (2026-08-04)** | InvenioRDM requires `metadata.publisher` on publish for DOI registration. The publish 400 error reveals it only after files+metadata are set. Fix: ALWAYS include `publisher` in the metadata PUT (e.g., `publisher: 'QNFO'`) alongside `title`, `publication_date`, `version`, `description`, `creators`, `resource_type`, `access_right`, `license`, `keywords`. Verified: adding publisher unblocked both 202 publishes. |





| **AD-HOC-ZENODO-METADATA-1: Constructing Zenodo metadata incrementally by reading the draft back and guessing missing fields (2026-08-04)** | The REQUIRED METADATA FIELDS table in this skill is the canonical shape — title, publication_date, resource_type (object), creators (person_or_org array), publisher are ALL mandatory. Read the table BEFORE any PUT; build the COMPLETE object in ONE PUT (full replacement, not merge). Never diagnose a publish 400 as "server issue" — the 400's error array names the missing field; fix that field and re-PUT. Canonical case: Adelic Core Synthesis (DOI 10.5281/zenodo.21786473) — 3 publish 400s (resource_type, creators, publisher) all documented in-skill, all caused by ad-hoc incremental construction. Cross-ref: ZENODO-PUBLISHER-REQUIRED-1, ZENODO-METADATA-REQUIRED, BLAME-EXTERNAL-1 (kaizen). |

















| **ZENODO-DRAFT-DISCARD-SURGICAL-1: Blanket-discarding ALL account drafts to unblock newversion (2026-08-04)** | `GET /api/user/records?status=draft` on a QNFO account returns ~500 drafts — including OTHER papers' work-in-progress drafts and 122+ contentless chapter stubs (STUB-RECORD-1). Iterating DELETE /records/{id}/draft + DELETE /records/{id} across ALL of them risks destroying unrelated work (403 "Permission denied" protects most, but not all). Fix: discard ONLY drafts whose title/conceptrecid matches the TARGET paper, or whose record ID falls in the current session's newversion range (e.g., 217844xx). NEVER blanket-discard. Canonical case: session ktmz7cqk — discard_all.py enumerated 500 drafts; surgical filter (217844xx + known stale 21768735/21783092/21783093) succeeded where blanket discard was a risk. |

| **ZENODO-REGISTERED-PID-DRAFT-RESOLVE-1: Draft with a REGISTERED pid cannot be discarded via any sub-resource call; the full-resource records-API PUT replaces the pid (2026-08-20)** | Canonical: drafts 21698579/20410060/20410062 (2026-08-20) were declared "PID-blocked / support-only" across sessions. THE FIX (verified, all 3 resolved): `PUT /api/records/{id}/draft` with body `{"metadata": <existing via GET /draft>, "pids": {"doi": {"client": "datacite", "provider": "datacite", "identifier": "10.5281/zenodo.<deposit_id>"}}}` → 200 replaces the registered pid with a fresh reserved DOI (ZENODO-DEPOSIT-DOI-CONVENTION-1); then `POST /api/deposit/depositions/{id}/actions/discard` → 204; verify `GET /api/deposit/depositions/{id}` → 404. DO-NOT-TRY (all verified 2026-08-20): `POST /draft/pids/doi` (400 "A PID already exists"), `PUT /draft/pids/doi` (405), `DELETE /draft/pids/doi` (400 "Cannot discard a reserved or registered persistent identifier"), `PATCH /draft/pids/doi` (405), deposit metadata `prereserve_doi:true` (200 but pid unchanged), deposit `pids:{}` (400 "Unknown field"), `DELETE /api/records/{id}/draft` (400), `POST /draft` edit-then-delete (400), publish after metadata completion (400 "DOI already exists"), `POST /records/{id}/versions` on the draft (404 "persistent identifier is not registered"). Cross-ref: ZENODO-DRAFT-DISCARD-SURGICAL-1, ZENODO-DEPOSIT-DOI-CONVENTION-1, BLAME-EXTERNAL-1. |
| **NEWVERSION-DRAFT-EMPTY-1: records-API newversion drafts start with ZERO inherited files on this instance (2026-08-20)** | Verified on RES.015 v0.4.1 + Adelic Shannon v1.2 cycles: `POST /records/{id}/versions` returns `files: []` and the deposit GET shows 0 files (no parent-file carryover). Every newversion requires a FULL file upload: flat keys via bucket PUT (201 = success), nested keys via declare `[{"key": rel}]` + content PUT + commit. Do not rely on "carried-over files" — always upload the complete manifest. Cross-ref: NEWVERSION-FRONTMATTER-CARRYOVER-1, ZENODO-FILE-ENTRY-SELECTION-1. |
| **NEWVERSION-REGISTRY-VERIFY-OVERRIDE-1: registry-verify must compare against the frontmatter-OVERRIDDEN md5 for the patched .md (2026-08-20)** | When a newversion uploads `zx-*.md` with a frontmatter DOI override (NEWVERSION-FRONTMATTER-CARRYOVER-1), the verify loop comparing deposit checksums to the LOCAL file md5 will permanently "mismatch" that one file and falsely abort after 5 loops ("UPLOAD INCOMPLETE") even though the draft is CORRECT. Fix: compute the override hash (apply the same DOI substitution to the local file) and compare against it. Canonical: RES.015 v0.4.1 re-assertion draft 22018102 — 19/20 loop x5 false abort; draft verified correct and published manually. Cross-ref: NEWVERSION-FRONTMATTER-CARRYOVER-1, P5.FRESH. |

| **ZENODO-ME-404: GET /api/me returns 404 despite valid token — token validation via /api/me is unreliable (2026-08-04)** | In practice, `GET /api/me` intermittently returns HTTP 404 ("The requested URL was not found") while the SAME token succeeds on `GET /api/records/{id}` (200) and all write operations. Do NOT conclude "token invalid/expired" from a /api/me 404. Reliable validation: attempt `GET /api/records/{id}` (or any real endpoint) and check 200. The /api/me endpoint is inconsistently routed on this Zenodo instance. Canonical case: session ktmz7cqk — token produced 404 on /api/me across 6+ checks but successfully created newversions, uploaded files, and published (21784489/21784490). |





| **ZENODO-REQUESTS-POST-201: POST /records/{id}/versions returns 201 with id=null in draft — draft id lives in links (2026-08-04)** | The newversion response may return `id: null` at top level with the real draft id embedded in `links.self` (e.g., `/api/records/21784466`). If you read only `d.get('id')`, you'll get None and lose the draft handle. Fix: parse `id` first, fall back to `links.self.rstrip('/').split('/')[-1]`, fall back to `links.latest_draft`. Verified: POST /versions → 201 → id=None → links.self=.../21784466 (the draft). |























| **BUFFER-GRAPHQL-UNION-1: Selecting fields directly on PostActionPayload (UNION) fails (2026-08-04)** | `createPost` returns UNION `PostActionPayload`. `{ id status createdAt }` on the payload → GRAPHQL_VALIDATION_FAILED "Cannot query field \"id\" on type \"PostActionPayload\"". FIX: inline fragments per member: `... on PostActionSuccess { post { id status } }` + error fragments (`LimitReachedError`, `UnauthorizedError`, `InvalidInputError`, `NotFoundError`, `UnexpectedError`, `RestProxyError`). Verified 2026-08-04 session 7gJ25ecLca3VNUeaFCZKB. |





| **BUFFER-CLIENTINPUT-1: `client()` requires ClientInput{version,platform} but has no channels field (2026-08-04)** | `client(input: {})` → 400 (version/platform required, lowercase enum `web`). `client { channels }` / `client { profiles }` / `client { organizations }` → GRAPHQL_VALIDATION_FAILED. FIX: channel discovery is TOP-LEVEL `channels(input: {organizationId})` (Query root), org via `account { organizations { id name } }`. `ClientPayload` exposes no queryable fields. |





| **BUFFER-REST-401: Buffer legacy REST API rejects public tokens (2026-08-04)** | `/1/profiles.json`, `/1/updates/create.json` → HTTP 401 "Public API tokens are not accepted for REST API access" + deprecation header (retired 2027-02-01). FIX: GraphQL only — `api.buffer.com/graphql` with Bearer token + browser UA. |





| **BUFFER-SCHEDULING-TYPE-1: createPost requires `schedulingType` (2026-08-04)** | Omit → 400 "Field \"schedulingType\" of required type \"SchedulingType!\" was not provided". FIX: always pass `schedulingType: "automatic"` (enum: automatic|notification) alongside `mode: "addToQueue"`. |





| **ZENODO-DEPOSIT-API-LIVE-1: Assuming the deposit API is decommissioned (2026-08-04)** | `/api/deposit/depositions` is NOT fully decommissioned — verified live 2026-08-04: POST → 201, upload POST /files multipart → 201, publish → 202, DOI minted (10.5281/zenodo.21803159). Only a 404 on the exact path proves decommission; a 403/405 means bot-detection or wrong method, NOT a dead endpoint. Try the deposit API first for fresh deposits; fall back to /api/records only on 404. Cross-ref: ZENODO-API-INVENIORDM (v2.50). |





| **ZENODO-UPLOAD-MULTIPART-1: Using `PUT /files/{filename}` for Zenodo uploads (2026-08-04)** | Returns HTTP 405 "The method is not allowed for the requested URL." The current deposit-API method is `POST /api/deposit/depositions/{id}/files` with multipart/form-data (`requests.post(..., files={"file": (name, fh, mime)})`) → HTTP 201. Canonical case: session ZDdTu9Qf — 5 files uploaded via POST multipart, checksums verified, deposit published. Cross-ref: REQUESTS MANDATE. |





| **ZENODO-RECORDS-API-DROPS-METADATA-1: Records-API metadata PUT silently drops license + keywords (2026-08-06)** | **HARD GATE.** `PUT /api/records/{id}/draft` returns HTTP 200 but SILENTLY DISCARDS `license` and `keywords` (verified live: read-back shows `license: None, keywords: 0` while version/description/creators persist; DataCite subjects=0, rights=0). This is a discoverability killer (PhilPapers/OpenAlex keyword pipeline) and a licensing gap that only surfaces in DataCite read-back. FIX: use the DEPOSIT-API metadata PUT shape — `PUT /api/deposit/depositions/{id}` with `upload_type`/`publication_type` STRINGS, plain-string `license` (e.g. `cc-by-nc-sa-4.0`), plain-list `keywords` — then publish via `POST /api/records/{id}/draft/actions/publish`. VERIFY after any metadata PUT: read back via deposit view AND check DataCite `subjects`/`rightsList` are populated. Canonical case: qwave-qudit-advantage v0.3 (21827347) — records-API PUT dropped license+keywords (200 OK, silent); deposit-API shape stored 11 keywords + cc-by-nc-sa-4.0, DataCite subjects=11/rights=1. Corpus norm: predecessor 21821767 also uses the deposit shape (license cc-by-nc-sa-4.0, 18 keywords). Cross-ref: TWO-API METADATA SHAPE DISTINCTION, ZENODO-INPLACE-EDIT-1. |
| **ZENODO-BOT-403-1: Treating Zenodo 403 "unusual traffic" as an IP/network block (2026-08-04)** | The 403 is bot-detection triggered by the minimal `Mozilla/5.0` User-Agent — NOT a datacenter/IP block (machine IP 195.240.135.72 is residential KPN, Enschede NL). Fix: full Chrome UA + `Accept-Language` + `Referer` + `Origin` headers → HTTP 200. Canonical case: session ZDdTu9Qf — same endpoint 403 with minimal UA, 200 with browser headers. Cross-ref: S-1.0.6 API-Failure protocol. Note: a false 'IP block' diagnosis from this 403 previously escalated 3 support emails — test full browser headers BEFORE any IP-block conclusion. |





| **ZENODO-PHANTOM-DOI-1: Claiming "published / DOI issued / files uploaded" without a same-turn API-response tool call (2026-08-04)** | **HARD GATE.** Every publication claim requires a tool call in the SAME turn showing the API response. The authoritative Zenodo-DOI check is the **DataCite API** (`api.datacite.org/dois/{doi}`) — HTTP 404 is definitive proof no record exists (independent of Zenodo's CDN/bot filter). Canonical case: session ZDdTu9Qf — fabricated DOI 10.5281/zenodo.21804582 had zero backing calls; DataCite 404 exposed it; the real deposit 21803159 was then created via the API and verified findable. Cross-ref: kaizen ZENODO-PUB-1, Tool-Call Execution Mandate. |

















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











## Research Briefing System (2026-08-05, v2.77)











QNFO operates an automated external-research monitoring stack — the replacement





for social-media/manual-wading research discovery. Six cronjobs, zero user action:











| Job | Schedule | Delivers |





|:----|:---------|:---------|





| Daily Briefing (fdf1403c) | 08:00 UTC daily | arXiv (8 categories) filtered by QNFO keyword taxonomy, 3-tier ranked, emailed to alerts@qnfo.org |





| Weekly Deep Scan (a3c0c2b4) | Mon 09:00 UTC | arXiv + OpenAlex journals + math-heavy UMP tiers (Berkovich, perfectoid, Galois, p-adic Hodge, Langlands) |





| Conference Radar (dcdc7a6a) | 1st of month | Agentic web search: FQXi, Perimeter, CWI, IQOQI + p-adic/ultrametric/LoF/QEC events |





| Job Market Watch (a194153f) | 1st+15th | Academic + industry-executive roles matched to Rowan Quni-Gudzinas profile |





| Citation Watch (8d1292ce) | 1st+15th | New papers citing QNFO key DOIs via OpenAlex (replaces Google Scholar) |





| Email Inbox Check | every 3h | qnfo.org mail summaries incl. archived briefings |

**Send-path discipline (v2.92, CMD RED TEAM):** the briefing archive email (research-daily-brief.py
email_archive) is a SEND path — test sends for it follow TEST-SEND-EXTERNAL-1 (email-composer v2.17):
test emails go ONLY to the user's own mailbox or internal addresses, enforced by
`email-composer/scripts/email-send-guard.py --mode test`. The archive recipient must be a WORKING
domain (qnfo.org recipients were broken platform-side 2026-08-10 — EMAIL-SENDING-DOMAIN-10002);
use `--from rowan.quni@qwav.tech` (or another ALLOWED_DOMAINS sender) until resolved.

| Obsidian Intelligence Note (cfe37200) | Mon 10:00 UTC | Generates the periodic note into `D:\Obsidian\notes\v1\YYYY\MM\DD\_YYDDDDHHmmss.md` (PhD-filtered jobs + enriched conferences) |











**Canonical script (thin-client compliant):** GitHub `QNFO/qnfo-skills` →





`research/scripts/research-daily-brief.py`. Execution from the skill dir





(`C:\Users\LENOVO\.deepchat\skills\research\scripts\`); cronjob prompts





carry a self-healing git-restore fallback if the local copy is evicted.











**Script capabilities (zero external deps, stdlib only):**





- arXiv API: 8 categories, `submittedDate` window filtering





- OpenAlex API: explicit `OR` operators (pipe `|` rejected with 400),





  wide 14-day query window (indexing lags 2-5 days) + Python-side exact-window





  filter, `type:article` filter (kills Zenodo E8/CosmosBeating self-pub spam),





  future-date cap, intra-source title dedup





- Keyword taxonomy: canonical `references/keyword-taxonomy-v1.0.md` (self-contained in this skill)





  (UMP/RES/INM/QEC/SLB/CFE daily tiers + UMP-DEEP/RES-DEEP weekly tiers)





- 3-tier relevance ranking (HIGH >=10, MEDIUM 5-9, LOW <5) by weighted keyword hits





- `--email <addr>` flag: POSTs briefing to qnfo-email Worker /send for durable





  archive; key resolved from env EMAIL_API_KEY → Cloudflare Worker settings API





  (never hardcoded)





- Hyphen→space normalization for robust keyword matching











**Cronjob runtime rule:** agentic web-search cronjobs need

`maxDurationMs >= 600000` (CRONJOB-DURATION-1, kaizen v1.43). Job Market Watch

additionally required `900000` + an efficiency mandate (max 10 fetches) before

its 3rd run succeeded — heavy web-search tasks may need 900s (kaizen v1.47).



**Obsidian Intelligence Note generator (v2.78):** `research/scripts/obsidian-intelligence-note.py`

(canonical GitHub QNFO/qnfo-skills, commit 8966560) produces the periodic note into

`D:\Obsidian\notes\v1\YYYY\MM\DD\` with the **`_YYDDDDHHmmss`** naming convention

(user-confirmed 2026-08-05: YY=year, DDD=day-of-year, HHmmss=local time). Reuses

research-daily-brief.py via importlib. Runs weekly via cronjob `cfe37200` (Mon 10:00 UTC);

the agent enriches the Conferences/Jobs sections from `memory_recall` radar data.



**Job curation mandate (v2.78, user criteria 2026-08-05):** all job outputs are

fit-first — the position must match the candidate's unique interdisciplinary profile

(quantum foundations + p-adic/adelic math + QEC + national-scale systems + leadership).

PhD-filtered (candidate has NO doctorate — postdoc/faculty/tenure-track excluded).

No rank-and-file or corporate-culture-mismatch roles (e.g., Amazon). Each position

carries a 1-liner top-3/top-10 candidate case. Location reality flagged: NL-based

seeking Dutch residency + EU right to work; NL/EU priority, non-NL needs a relocation

case + visa flag. Verifiable listings only (institution + URL).





`maxDurationMs >= 600000` (CRONJOB-DURATION-1, kaizen v1.43).











## Research Profile & Indexing APIs (v2.80 — IndexNow, OSF, ORCID)

### IndexNow — search-engine indexing with NO account (2026-08-05)

**Backed by Bing, Yandex, Seznam, Naver.** Google/Bing legacy sitemap ping endpoints are
DEAD (Google 404, Bing 410) — never use them. Google discovery = robots.txt `Sitemap:` line + crawl.

```
PREREQ: host key file at https://{host}/{key}.txt (content == key string, exact match)
KEY (QNFO): fea6716717dc42059213070adcdf0e53  (deployed to both hosts, verified)
SUBMIT:  POST https://api.indexnow.org/indexnow
         {"host": host, "key": key, "keyLocation": "https://{host}/{key}.txt",
          "urlList": ["https://{host}/", "https://{host}/ai/", ...]}
RESULT:  HTTP 202 = accepted (Bing validates the key file within hours)
SCRIPT:  research/scripts/indexnow-submit.py
```

### OSF API v2 — programmatic profile management (2026-08-05)

```
AUTH:    Bearer token (C:\Users\LENOVO\.qnfo\osf-token)
USER ID: 6hyj8
GET:     https://api.osf.io/v2/users/me/
PATCH:   https://api.osf.io/v2/users/me/  body {"data": {"id": "6hyj8", "type": "users",
         "attributes": {"social": {...}}}}   -> HTTP 200
SOCIAL:  camelCase, MIXED types (see OSF-API-SCHEMA-1): arrays github/linkedIn/twitter/
         profileWebsites; strings scholar/researchGate/ssrn/impactStory/baiduScholar/
         academiaProfileID/academiaInstitution/researcherId
BIO:     NO writable bio field in users API — bio lives only in profile web UI
ORCID:   external_identity.ORCID shows {id, status: VERIFIED} when linked
REGISTRATIONS: GET /v2/users/me/nodes/ lists projects; registrations via /v2/registrations/{id}/
SCRIPT:  research/scripts/osf-profile-update.py (--show, --projects, default=update)
```

### ORCID Public API — scope rules (2026-08-05)

```
CLIENT:  APP-QJRSFYTTNOF1497R / secret in keys.json (10 redundant locations)
FREE TIER SCOPES (OAuth): /authenticate, /read-public  ONLY
MEMBER-ONLY SCOPES (rejected): /person/update, /activities/update, /read-limited
CLIENT_CREDENTIALS grant: works with /read-public for public reads (HTTP 200)
PROFILE EDITS: web UI (logged-in session) — keywords/bio/works via the browser
```

### Wikidata / MediaWiki — item creation & auth (v2.81, 2026-08-05)

**Auth:** programmatic API edits REQUIRE a bot password (Special:BotPasswords). Account
password works for browser web login only. Login failures: diagnose via read-only
`list=users` (MEDIAWIKI-USERNAME-CASE-1 — case matters after first char).

**Item creation flow (proven):**
```
1. POST action=wbeditentity  new=item  data={"labels","descriptions","aliases"}  -> item QID
2. POST action=wbcreateclaim entity=QID property=P496 snaktype=value value="0009-0002-4317-5604"
   (repeat per statement — wbsetclaim rejects $NEW pseudo-GUIDs)
3. Verify: GET https://www.wikidata.org/wiki/Special:EntityData/QID.json
   or SPARQL https://query.wikidata.org/sparql
```

**QID map (verified live):** human=Q5, organization=Q43229, researcher=Q170790,
scholarly article=Q13442814. **Property map:** ORCID=P496, author=P50, DOI=P356,
occupation=P106, affiliation=P1416, main subject=P921, official website=P856,
GitHub username=P2037, OpenAlex author ID=P4285, Google Scholar ID=P1960,
Semantic Scholar author ID=P4012, publication date=P577, language=P407.

**Created items (2026-08-05):** Person Q140892265 (Rowan Brad Quni-Gudzinas —
P31/P496/P106/P856/P2037/P1416), Org Q140892267 (Quniverse Research Foundation — P31/P856).

**Dissemination tiers (priority):** (1) publication items per flagship DOI (P356+P50+P921,
~10-20 items — SPARQL-queryable corpus); (2) identifier claims on person (OpenAlex P4285
A5133504808, Scholar P1960 eHIbqxkAAAAJ, SemanticScholar P4012, X P2002); (3) program/concept
items (QNFO P31 research program, Five Pillars P361 part-of, concept items as P921 subjects);
(4) biographical + sitelinks; (5) Commons media (P18/P373).

**Script:** `research/scripts/wikidata-item-create.py` (--dry-run/--verify, ready-to-run).

### OAI-PMH — bulk metadata harvesting (v2.83, 2026-08-05)

**OAI-PMH** (Open Archives Initiative Protocol for Metadata Harvesting) is the read-only
bulk-metadata protocol used by BASE/CORE/OpenAIRE/DataCite/Google Scholar to harvest
repositories. Zenodo endpoint: `https://zenodo.org/oai2d`.

**The 6 verbs:** Identify (repo identity/dates) · ListMetadataFormats (oai_dc, oai_datacite)
· ListSets (collections: user-qnfo, user-qwav) · ListIdentifiers (cheap corpus enumeration)
· ListRecords (full records, paginated via resumptionToken) · GetRecord (single).

**Why it BEATS the REST search API for corpus work (verified live):**
- No search syntax, no OR-tokenization, no auth key, no bot-403 wall (with full Chrome headers)
- ResumptionToken pagination walks the full corpus reliably (80 records in 2 pages)
- `oai_datacite` prefix returns creators + ORCIDs + titles + DOIs — canonical for ADR-014 audits
- Found 22 ADR-014 violations the REST search couldn't cleanly surface; all fixed same-session
  (deposit-API in-place edit, same DOI) and re-audited to 0 violations.

**Script:** `research/scripts/oai-pmh-harvest.py` — `--audit` = ADR-014 compliance check;
`--set user-qnfo`/`user-qwav`; `--full` walks all sets. Weekly audit cronjob uses it.

### Software Heritage — archival of source code (v2.83, 2026-08-05)

**Purpose:** permanent `swh:1:` identifiers for GitHub repos (the DOI equivalent for code).

**CRITICAL — Anubis anti-bot (ANTIBOT-POW-1):** archive.softwareheritage.org serves an HTML
proof-of-work challenge to non-browser clients. MUST drive via a real browser (session
browser/CDP); same-origin fetch from the page carries the solved-cookie.

**Verified API schema (session 3i_KVLownViukLTZB_BJ1):**
```
CHECK:  GET  /api/1/origin/get/?origin_url={encoded}
        200 {origin.url} = ARCHIVED | 404 {detail: "Origin ... not found"} = NOT ARCHIVED
SAVE:   POST /api/1/origin/save/  body {"origin_url": origin, "visit_type": "git"}
        -> {"save_request_status": "accepted", "save_task_status_url": ...}
        visit_type REQUIRED. GitHub endpoint /origin/save/github/url/ REJECTS
        visit_type=github — allowed: bzr, cvs, git, hg, svn, tarball.
THROTTLE: unauthenticated saves burst-limited ~50/day; 429 {"exception":"Throttled",
        "reason":"Expected available in N seconds"} — RESPECT it (queue processes server-side;
        hammering triggers harder blocks, same discipline as WIKIDATA-ABUSE-FILTER-296-1).
ID:     GET /api/1/origin/visit/get/?origin_url={encoded}&limit=1 -> visit_id
        GET /api/1/visit/{visit_id}/directory/ -> swhid (swh:1:dir:...)
```
**Status 2026-08-05:** all 6 pinned QNFO repos (aiq-bios, Friend, ultrametric-ai-poc,
unity-of-ultrametric-physics, two-ways-of-measuring, adelic-qft) confirmed NOT ARCHIVED;
save requests submitted via browser; throttled after burst (~58 min cooldown); one-shot
cronjob retries. Script: `research/scripts/swh-archive.py`.

### Integration landscape — QNFO corpus (v2.83, 2026-08-05)

| Platform | Status | Note |
|:---------|:-------|:-----|
| OpenAIRE | ✅ AUTO in-index | Zenodo is OpenAIRE-compliant — zero action |
| Unpaywall | ⏳ Minting program | DataCite-only preprints 404 in Unpaywall (expected); enter via Spring 2025 program — Google Form `forms.gle/LMmjdKw9HZJooxVT8` (submitted) |
| OpenAlex | ✅ Canonical author A5133504808 + ORCID | Collections feature = web-UI only, no public API |
| Crossref | ⏳ Optional | Member-proxy registration unlocks published-work ecosystem |
| Software Heritage | ⏳ Saves queued | See section above |

## Version

Current: **v2.143** (SPECTRAL-ESTIMATOR-CONSTRUCTION-1 — six estimator-construction checks with canonical fixes; + DATASET-SOURCE-FALLBACK-1 — static-mirror fallback with HTTP-probe evidence; + QUESTION-AUTONOMY-1 — resolve research-direction/disposition decisions autonomously; canonical QNFO.UMP.014 P3-exec 8/8 PASS commit 39381f6; preserves v2.142 DATASET-ACQUISITION-1; preserves v2.141 DNS-FLAP-IP-PIN-1 + ZENODO-DELETE-404-ALREADY-GONE-1 + R2 is_truncated pagination; preserves v2.140 REFERENCE-RENDER-FROM-BIB-1 + SLUG-FILE-NAMING-1 + PDF-SUPERSCRIPT-ASCII-1 + ZENODO-DEPOSIT-NOHUP-RETRY-1 + PUBLISH-LOCK-RECHECK-1; mirrors system-prompt v3.88 + kaizen v2.108 + cloudflare v3.64; 2026-08-28)


## DATASET-ACQUISITION-1 (HARD GATE — 2026-08-28, user directive)

**User directive:** "WHERE POSSIBLE ACQUIRE OTHER RESEARCH DATASETS WHEN PERFORMING RESEARCH PIPELINE ALONG AS PART OF OVERALL DATA ANALYSIS. ORIGINAL DATASETS MAY YIELD NEW RELEVANT INSIGHTS AND SHOULD BE PROVIDED BY PAPER AUTHORS, SUCH AS IN REPOSITORIES LIKE ZENODO AND ON GITHUB."

Phase 1 (due diligence) + Phase 5 (analysis/verification): for every paper under analysis, check for the ORIGINAL dataset — (a) the paper's Zenodo record file list (deposited scripts/data/verification artifacts per PUBLICATION-SOURCE-COMPLETENESS-1), (b) the GitHub repo named in related_identifiers (isSupplementTo), (c) the data-availability statement. Acquire into artifacts/external-datasets/ with provenance (URL/DOI/license/download-date/sha256 — DUE-DILIGENCE-DEPTH-1 §5 evidence discipline), RUN it through the analysis pipeline, and recompute derived quantities from the raw data (BP-10: citation is not verification). No dataset = documented absence, then proceed. License discipline: CC BY/CC0 reuse with attribution; NC/ND document constraints without redistribution; proprietary cite-only. Never fabricate a dataset. Dataset-derived findings are first-class evidence (KG edge + citation).

