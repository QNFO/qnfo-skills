# QNFO Term Crosswalk v1.0 — Cross-Domain Terminology Infrastructure

**Status:** canonical, v1.0, 2026-08-24 | **Owner:** knowledge skill | **Source records:** 10.5281/zenodo.22075544 (Terminology Silos audit), 10.5281/zenodo.22071421 (seed audit), QNFO-KEYWORD-TAXONOMY v1.0

**Why this exists (user directive 2026-08-24):** cross-domain insights and
interdisciplinary/trans-disciplinary terminology and crosswalks/translations are
critical for breakthrough discoveries — no silos, no jargon, no domain walls.
Quantified: scientific vocabulary is ~97% domain-local; the 2.8% of terms that
bridge domains are massively method-biased (Fisher exact p = 8.5e-7, OR 70.2);
cross-domain semantic links carry ZERO lexical signal unless an author writes the
bridge into the title. A crosswalk is the machine-readable repair: the mapping
that makes the same concept findable across the vocabularies that partition it.

## 1. Domain-code crosswalk (QNFO programs ↔ plain-English)

| Code | Domain | Plain-English key |
|------|--------|-------------------|
| UMP | Ultrametric physics | non-Archimedean geometry, p-adic/adelic structure, hierarchical metric |
| SLB | Laws of Form | boundary calculus, self-reference, indication/observation |
| INM | Infomatics | integrated information, phi-measure, cause-effect structure |
| CFE | CFPE (Cascading Foresight) | forecasting, technology diffusion, s-curve models |
| RES | Consilience research | complexity, cross-domain synthesis, knowledge infrastructure |
| PLT | QWAV Platform | product/industry embodiment of the research |
| DEM | QWAV Demos | executable demonstrations of published results |

**Rule:** when reading or writing about any QNFO program, state the plain-English
key once (title/abstract/intro) — never assume the reader shares the program's
vocabulary.

## 2. Method-level bridge vocabulary (statistically blessed bridges)

The 13 terms that occur in exactly two of six external disciplines (deposited
evidence: silo_arxiv_external.json, record 10.5281/zenodo.22075544). Method terms
are the only general-purpose bridge family:

| Term | Class | Note |
|------|-------|------|
| machine-learning | method | THE canonical bridge word — use it in keywords/abstracts of any cross-domain artifact |
| language-model / language-models | method | |
| foundation-models | method | |
| upper-bound | method | math-NT/CS-theory shared shell |
| boron-nitride, quantum-defects, defects-zno, double-substitutional, optically-quantum, candidate-quantum, candidates-optically | shared object | two disciplines working on the same material — copy the object name, not the jargon |
| drug-discovery | shared application | |

**Rule:** cross-domain titles/abstracts/keywords MUST include at least one
method-level shared term plus the object/application name in BOTH domains'
spellings. Lexical retrieval cannot find connections the vocabulary does not
carry (Jaccard 0.0 for unnamed bridges; 0.333 for the authored "Valuation Without
R" bridge).

## 3. QNFO internal bridges (seed case)

- **complexity-measure** — the single keyword of 335 occurring in two programs
  (INM + RES). Anchor term for INM↔RES discovery queries.
- **Domain-anchored bridge subsections** (per-program named bridges, all
  program-local): e.g. ostrowski-theorem, idele-class-group (UMP valuation ↔
  number theory). These name connections WITHOUT instantiating shared vocabulary
  — a bridge subsection is not a bridge term until the name escapes its program.
- **Authored bridge exemplar:** "Valuation Without R" (10.5281/zenodo.21803677) —
  shares the token `valuation` with Measurement Stratigraphy
  (10.5281/zenodo.21705220); the ONLY cited cross-domain bridge with nonzero
  title overlap (Jaccard 0.333). Pattern: write the shared token into the title.

## 4. Usage protocol (search / storage / extension)

1. **Search:** any cross-domain due-diligence query runs >=2 vocabulary regimes:
   (a) the program's own terms, (b) the method-level bridge terms above, (c) the
   target domain's own terms. Semantic search (Vectorize) is REQUIRED — lexical
   search alone sees ~0% of cross-domain links.
2. **Storage/tagging:** when a paper is indexed, tag it with domain code(s) AND
   any bridge terms it uses. D1 living-paper.term_crosswalks mirrors this file
   row-for-row (id, term, class, domains, source_record, note).
3. **Extension:** when any QNFO record authors a new cross-domain bridge, add a
   row here + in D1, and re-run the partitionality instrument
   (scripts/terminology_silos.py, QNFO.CGS.002) against the affected taxonomy
   corpus. A crosswalk row without its partitionality re-check is a claim without
   evidence.
4. **Promotion:** interdisciplinary dissemination of any record uses its
   crosswalk rows — the message states the concept once in each audience's
   vocabulary (no jargon walls).

**Maintenance:** this file is the canonical source; D1 table is the mirror. Keep
them row-identical (CROSSWALK-PARITY-1); verify after every extension.
