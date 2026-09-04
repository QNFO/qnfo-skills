# LAMPORT-STRUCTURED PROOFS — QNFO CANONICAL STYLE GUIDE

THEOREM (PURPOSE): every QNFO machine-instruction surface (system prompts, skill files, custom prompt templates, worker-embedded prompts) and every QNFO code module is written in Lamport's hierarchical structured-proof style — numbered assertions, nested PROOF blocks, explicit derivation by citation, zero prose narration. PROOF: by the grammar below; compliance is mechanically verifiable.

⟨1⟩1. INSTRUCTION-FORMAT GRAMMAR
⟨2⟩1. NUMBERING: step k at nesting depth N is written ⟨N⟩k; the top level is ⟨1⟩1, ⟨1⟩2, …; the PROOF of a ⟨N⟩ step contains ⟨N+1⟩1, ⟨N+1⟩2, …; depth resets per PROOF block.
⟨2⟩2. STATEMENT FORMS: every step opens with exactly one of ASSUME / ASSERT / CASE / ACTION / GATE / FACT / PROVE and is one complete declarative sentence; no fragment steps, no heading-only steps.
⟨2⟩3. PROOF BLOCKS: a step whose truth is non-immediate carries PROOF: + deeper-level steps + QED.
⟨2⟩4. DERIVATION BY CITATION: "QED by ⟨1⟩2, ⟨1⟩5." replaces prose like "as shown above"; no forward references.
⟨2⟩5. NARRATION BAN: forbidden — "we will show", "now consider", "obviously", "note that", meta-commentary about the document; the nesting IS the argument.
⟨2⟩6. GATE ENCODING: each governance gate is one step: "GATE-ID [canonical-date]" + ASSERT (rule) / CASE (canonical failure evidence) / ACTION (required remediation) / QED; pure-fact records use "FACT-ID [date]: facts." with no PROOF block.
⟨2⟩7. DATA CARRIERS: markdown tables/lists remain for rosters, matrixes, key-value facts; table rows may carry gate IDs.
QED.

⟨1⟩2. CODE-FORMAT GRAMMAR (proof-like code)
⟨2⟩1. MODULE THEOREM: every module/worker/script opens with a comment stating THEOREM: what it guarantees given its inputs; PROOF: by the ⟨N⟩ steps below.
⟨2⟩2. FUNCTION SPECS: non-trivial functions carry a comment block ⟨1⟩1. ASSUME preconditions … ⟨1⟩n. PROVE postconditions/invariants. QED.
⟨2⟩3. RUNTIME ASSERTIONS: invariants at branch points are assert() calls commented "⟨N⟩k. ASSERT: invariant".
⟨2⟩4. BRANCHES: each conditional branch is commented "CASE ⟨N⟩k. [condition]: consequence".
⟨2⟩5. LOOP INVARIANTS: loop headers comment "⟨N⟩k. INVARIANT: holds before/after each iteration; bound: ≤ X iterations".
⟨2⟩6. PROSE BAN: narrative comments ("// now we do X") are forbidden; comments are structured steps only.
QED.

⟨1⟩3. PRESERVATION RULE (zero semantic loss)
⟨2⟩1. ASSERT: every gate ID, canonical date, evidence pointer, DOI, hash, and fact from a legacy block appears in the structured form exactly once.
⟨2⟩2. ACTION: consolidation deduplicates repetition (PROMPT-PARITY-1 appears once, not per version); duplicate IDs union their CASE evidence; content is never dropped, only deduplicated.
⟨2⟩3. GATE: converted artifacts keep H1 title == top banner == footer "Current:" (TITLE-LINE-PARITY-1).
QED.

⟨1⟩4. SCOPE AND EXCLUSIONS
⟨2⟩1. IN SCOPE: DeepChat system prompt (all 7 stores); all skill SKILL.md bodies; all CMD template content fields (JSON schema unchanged); Cloudflare worker-embedded system prompts (qnfo-ai DEFAULT_SYSTEM_PROMPT, personal-api, qnfo-agent-orchestrator/ws, qnfo-tools-mcp, qnfo-email, qnfo-outreach composer, qnfo-social fact-checker, research-daily-brief digest, errata publish/respond); all QNFO source code.
⟨2⟩2. OUT OF SCOPE: publication prose and outreach copy (ANTI-TELEGRAPH-1 + PUBLICATION-BRAND-LANGUAGE-1 — structured style telegraphs AI construction and is prohibited there); third-party vendored code; data files.
⟨2⟩3. MIGRATION RULE: no gratuitous full-repo rewrites of behavior-bearing code; legacy code converts module-by-module at next touch; new/modified code MUST comply at write time.
QED.

⟨1⟩5. VERSIONING
⟨2⟩1. ASSERT: format-major conversion = v5.00 for the system prompt; each converted artifact records the source version it consolidates; subsequent updates follow the existing chain.
QED.

⟨1⟩6. ROLLOUT ORDER
⟨2⟩1. System prompt (foundation) → ⟨2⟩2. skills → ⟨2⟩3. CMD templates (11) → ⟨2⟩4. Cloudflare worker prompts → ⟨2⟩5. code repos.
⟨2⟩6. Each phase: draft artifact → user approval → install → parity verification (PROMPT-PARITY-1).
QED.

Current: v1.0 (2026-09-04 — Lamport-structured style guide; governs the v5.00 refactor program)
