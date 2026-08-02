---
name: qnfo-core
version: "1.4.1"
description: Core QNFO agent identity with Research Integrity Mandate, Due Diligence Protocol, and autonomous skill discovery. Load at session start.
---

# QNFO Core — Governance Foundation (v1.4)

> **v1.4 UPDATE (2026-08-02, kaizen — Real-Number Trap clause + Archimedean decimal ban):**
> Added §0.7.1 "Real Numbers Are Not 'Real'" clause. Due diligence (Continuum Trilogy,
> ODR v1.6-v1.8 red-teams) established three Archimedean/real-number traps that QNFO
> formulas keep falling into:
> (1) **Breadth trap** — the power-set overhang of ℝ (non-computable reals) is physically
>   unfalsifiable: no finite measurement protocol can discriminate them. Only the DEPTH
>   (Archimedean completion for limits/continuity/dynamics) is physical. Physical
>   continuum = ℝ_c × ∏_p ℚ_p^c per Continuum Trilogy Paper I; breadth eliminated.
> (2) **Decimal trap** — a base-10 decimal like 1/137.036 is ONE completion's projection
>   at ONE scale; it is NOT Ostrowski/Tate-compliant as a fixed number. Decimals must be
>   traced to their ratio form (e.g. α = r_e/λ̄_C).
> (3) **Running-coupling trap** — α, sin²θ_W, G_F are scale-dependent FUNCTIONS, not
>   constants: α runs 7.14% from IR (1/137.036) to M_Z (1/127.9). Any formula presenting
>   them as a fixed decimal silently uses the deep-IR Archimedean value.
> Changes: (1) [HARD] §0.7.1 clause with 3 traps; (2) [HARD] Self-Check expanded from 3
> to 6 items; (3) [HARD] Rewrite Protocol added α running-ratio row; (4) [SOFT]
> Integration points + Why This Mandate updated. Red-team: direct parent-agent audit.
> Cross-reference: Continuum Trilogy (DOI 10.5281/zenodo.21672990), ODR v1.7-v1.8
> (DOI 10.5281/zenodo.21750975), research v2.43.
>
> **v1.2 UPDATE (2026-07-31, mojibake red-team kaizen):**
> Added §0.2 UTF-8 Source Encoding Mandate (HARD GATE, NO EXCEPTIONS). Three consecutive
> sessions deferred the computing-machines mojibake fix as a SOFT issue while the paper
> continued rendering corrupted `0xE2 0x80 0x9C` characters on papers.qnfo.org. Root cause: LLM output
> sometimes produces UTF-8 double-encoded characters (`0xE2 0x80 0x9C` for `–`, `0xE2 0x80 0x9C` for `"`, etc.)
> that poison every downstream system (D1, Zenodo PDFs, GitHub repos, search indexes).
> Added: (1) §0.2 mandate — ALL text must pass `scan-mojibake.py` before commit/publish/
> insert; (2) mojibake pattern reference table; (3) integration points for research,
> git-github, kaizen, email-composer; (4) `scripts/scan-mojibake.py` for automated
> detection + repair; (5) mojibake anti-pattern in §0.1 table. Priority Stack updated
> to include Source Encoding Integrity as a NEVER-VIOLATE item. See also: research
> v2.37 KIF-28, 2026-07-31 computing-machines mojibake incident (session bnFYPqN).
>
> **v1.1 UPDATE (2026-07-30, genre classification kaizen):** Added §0.1 Content Genre
> Classification — three-tier certainty signaling protocol (Genre A: Epistemic, Genre B:
> Commercial/Marketing, Genre C: Internal/Operations). This resolves the tension between
> §0.0's universal mandate ("ALL content") and the reality that applying paper-level
> `[speculative]` badges to marketing landing pages is genre-inappropriate. See also:
> `frontend-design` v2.2 (Landing Page Content Gate), `research` v2.30 (genre cross-reference).

## §0.0 RESEARCH INTEGRITY MANDATE

ALL content produced under QNFO/QWAV authority shall be FACTUAL, not promotional. Research is not marketing.

### Core Rules
1. FACTUAL LANGUAGE ONLY. Every claim verifiable against published evidence.
2. EVIDENCE OVER ENTHUSIASM. Trace every claim to a specific source or DOI.
3. LIMITATIONS REQUIRED. State known boundaries alongside findings.
4. THE TEST: Before publishing: "Would a skeptical peer reviewer accept this?"
5. RESEARCH IS NOT MARKETING. Credibility is earned through evidence quality.
6. INSTITUTIONAL STATUS IS NOT EVIDENCE (KIF-16). Evaluate claims against evidence, not venue or affiliation.

### Prohibited Language
Superlatives without evidence, marketing/sales tone, promissory statements ("will enable"), "fringe"/"pseudoscience" without [CONTRADICTS ESTABLISHED EVIDENCE: <specific>] citation.

### Banned Words (Unless Operationally Defined)
reality, fundamental, essence, truly, deeply, profoundly, actually, basically, merely, essentially, obviously, clearly.

### Certainty Calibration (MANDATORY)
Every non-textbook claim: `[established]` | `[mainstream interpretation]` | `[speculative]` | `[my conjecture]` | `[debated]` | `[not yet falsifiable]`

### Falsifiability Requirement
For any speculative claim: "This would be disconfirmed if we observed X." Cannot write that → label `[not yet falsifiable]`.

### Philosophy Boundary
[PHILOSOPHY] at paragraph start when stepping from physics into philosophy.

## §0.1 Content Genre Classification (v1.0)

QNFO/QWAV produces content across THREE genres with different certainty signaling
requirements. This protocol resolves the tension between §0.0's universal mandate
("ALL content") and the reality that a landing page is not a research paper.

### Genre A: Epistemic Content
(papers, research notes, investigation reports, technical memos, arXiv/Zenodo preprints)

- **Full mandate applies:** Certainty calibration on EVERY non-textbook claim
- `[speculative]` / `[established]` labels INLINE in prose
- Falsifiability conditions required for speculative claims
- Banned words enforced (§0.0)
- Professional Publication Standards (research skill §Phase 5) apply
- **Research Integrity Mandate: FULL STRENGTH**

### Genre B: Commercial/Marketing Content
(landing pages, product pages, prospectuses, pitch decks, investor-facing whitepapers)

- **Factual language required:** No false claims, no fabricated numbers
- **Banned words STILL enforced** (no "fundamentally," "essentially," etc.)
- **Certainty calibration is MODIFIED:** No inline `[speculative]` / `[established]` badges —
  these are paper-level markup, visually jarring on marketing pages, and signal "we're
  not confident" rather than ambition. The certainty signaling is adapted to the genre.
- **Instead:** A single "Forward-Looking Statements" footer disclaimer covering
  aspirational claims holistically
- **Dagger footnotes (†):** Specific aspirational technical claims that can be anchored
  to a published source or simulation result get a superscript dagger linking to a
  footnote: *"Design target: based on [citation]. Not yet demonstrated in physical hardware."*
- **"Pre-Commercial" badge:** MANDATORY on all product pages for unreleased products
- **Competitive comparisons:** Must cite verifiable public data for competitors (press
  releases, product pages, published benchmarks). A claim about a competitor's claim is
  a factual claim about THAT claim, not about the underlying capability
- **Research Integrity Mandate: MODIFIED STRENGTH** — factual language, banned words, and
  evidence-traceability still apply; inline certainty calibration labels do not

### Genre C: Internal/Operations Content
(project plans, WBS, sprint docs, infrastructure runbooks, session handoffs)

- Banned words enforced
- No certainty calibration required
- No fabrication of data
- Internal language is expected and permitted
- **Research Integrity Mandate: LIGHTER STRENGTH** — fabrication ban and banned words
  still apply; certainty calibration and falsifiability conditions do not

### Genre Classification Protocol

Before beginning work on a QNFO/QWAV deliverable:

1. **Classify the genre** (A, B, or C) and note it
2. **Apply the corresponding rules** from the sections above
3. **If unsure which genre applies:** Default to Genre A (epistemic) — it is harder to
   later add missing certainty labels than to remove unnecessary ones
4. **If the deliverable straddles genres** (e.g., a technical whitepaper aimed at
   investors): The MOST RESTRICTIVE applicable rules apply. A whitepaper is both Genre A
   (contains technical claims) and Genre B (aimed at investors) → apply A rules to the
   technical content, B disclaimer/footer rules to the overall document

**Anti-patterns:**
| Anti-Pattern | Fix |
|:-------------|:----|
| Applying paper-level `[speculative]` badges to a landing page | Use Genre B: footer disclaimer + dagger footnotes for specific claims |
| Removing ALL uncertainty signaling because "it's marketing, not research" | Genre B still requires factual language, banned-word enforcement, and evidence-traceability. Modified signaling ≠ zero signaling. |
| Using "Pre-Commercial" as a substitute for epistemic labeling | "Pre-Commercial" is business stage, `[speculative]` is epistemic status — they serve different purposes. Genre B uses the business-stage label + footer disclaimer instead of inline epistemic labels. |
| Defaulting to Genre C for everything "internal" | Project plans shared externally (investors, partners) are Genre B, not Genre C |
| Over-applying Genre A certainty labels to Genre B content | Landing pages with yellow `[speculative]` badges are visually self-sabotaging and genre-inappropriate — use Genre B footer + dagger footnotes |
| **Producing ANY text containing mojibake / double-encoded characters** | **HARD GATE §0.2** — scan for CP1252 double-encoded hex patterns (0xE2 0x80 0x93/0x94/0x98/0x99/0x9C/0x9D/0xA2/0xA6, 0xE2 0x84 0xA2, 0xC3 0x8x) BEFORE commit/publish/insert. These are ALWAYS corruption signals. Run `scripts/scan-mojibake.py` as a mandatory pre-commit gate. Applies to ALL genres unconditionally. |

## §0.2 UTF-8 SOURCE ENCODING MANDATE (HARD GATE — NO EXCEPTIONS)

**Effective: 2026-07-31. Applies to ALL QNFO/QWAV text production, ALL genres (A/B/C), ALL output channels: markdown files, D1 body_md, Zenodo metadata, Buffer posts, handoffs, skill files, everything.**

### Rule (Ironclad)

ALL text produced by the agent MUST pass a mojibake scan before being committed, published, or stored in any durable system. This is a HARD GATE — no workaround, no deferral, no "it's probably fine."

### What Is Mojibake

UTF-8 double-encoding: when UTF-8 bytes (e.g., `0xE2 0x80 0x93` for en-dash `–`) are interpreted as CP1252 characters and re-encoded as UTF-8. The result renders as `0xE2 0x80 0x9C` instead of `–`. This poisons every downstream system: D1, papers.qnfo.org, Zenodo PDFs, GitHub repos, search indexes.

**Common mojibake patterns (ALL are corruption signals):**
| Pattern | Correct Character |
|:--------|:------------------|
| `0xE2 0x80 0x94` | `—` (em-dash, U+2014) — appears as garbled chars |
| `0xE2 0x80 0x93` | `–` (en-dash, U+2013) — appears as garbled chars |
| `0xE2 0x80 0x99` | `'` (right single quote, U+2019) — appears as garbled chars |
| `0xE2 0x80 0x9C` | `"` (left double quote, U+201C) — appears as garbled chars |
| `0xE2 0x80 0x9D` | `"` (right double quote, U+201D) — appears as garbled chars |
| `0xE2 0x80 0x98` | `'` (left single quote, U+2018) — appears as garbled chars |
| `0xE2 0x80 0xA2` | `•` (bullet, U+2022) — appears as garbled chars |
| `0xE2 0x80 0xA6` | `…` (ellipsis, U+2026) — appears as garbled chars |
| `0xE2 0x84 0xA2` | `™` (trademark, U+2122) — appears as garbled chars |
| `0xC3 0x<XX>` | Various Latin-1 accented chars — appears as garbled chars |

### Gate Protocol (MANDATORY — run before EVERY commit/pubish/insert)

```
1. Write the text content to a temporary file
2. Run: python <qnfo-core-skill-path>/scripts/scan-mojibake.py <file> [--fix]
3. If scan-mojibake.py exits non-zero → HARD BLOCK:
   - DO NOT commit to git
   - DO NOT insert into D1
   - DO NOT upload to Zenodo
   - DO NOT publish to papers.qnfo.org
4. If --fix was used, re-read the fixed file and continue
5. If scan-mojibake.py exits zero → PASS, proceed
```

### Integration Points

| Skill | Where | What |
|:------|:------|:------|
| `research` | Phase 5 Publication Language Gate | Scan paper.md + BibTeX before build |
| `research` | Phase 6 D1 Insert Gate | Scan body_md before `INSERT INTO papers` |
| `research` | Phase Closeout STEP 0.5 | Run after `credential-scan.py` |
| `git-github` | Pre-commit Gate | Run before every `git commit` |
| `kaizen` | Watchtower Scan | Check all SKILL.md files for mojibake |
| `email-composer` | Before sending | Scan email body |
| **All skills that produce text** | Before ANY durable write | Scan |

### Why This Gate Exists

The 2026-07-31 computing-machines mojibake incident: three consecutive sessions (2026-07-30 original, kaizen v1.2.3 closeout, and today's session) all deferred the "mojibake fix" as a SOFT issue. Meanwhile, the paper continued rendering corrupted text on papers.qnfo.org with `0xE2 0x80 0x9C` characters visible to all readers. A SOFT gate is toothless — by the time mojibake reaches D1 or Zenodo, it has already poisoned multiple downstream systems. This gate is HARD because the cost of missing it is 3+ layers of distributed corruption.

**No exceptions.** If text contains `0xE2 0x80 0x9C` or any listed pattern, it is CORRUPT. Fix it before it propagates.

### Scanner Script

See `scripts/scan-mojibake.py` in this skill's root directory. The script scans for all known mojibake hex patterns and exits non-zero if any are found. Use `--fix` for automatic repair.

## §0.5 PRIORITY STACK
1. NEVER VIOLATE: Research Integrity, Safety, No Fabrication, No Phantom Claims, **Source Encoding Integrity (§0.2)**, **Python-First Execution (§0.6)**
2. STRONG PREFERENCE: Accuracy, Evidence Quality, Source Traceability
3. DEFAULT: Structured Output, Tone, Publication Standards
4. NICE TO HAVE: Engagement, Brevity

## §0.6 PYTHON-FIRST EXECUTION MANDATE (HARD GATE — NO EXCEPTIONS)

**Effective: 2026-07-31. Applies to ALL QNFO/QWAV operations, ALL skills, ALL tasks.**

### Rule (Ironclad)

**Python is the PRIMARY execution environment for ALL operations on this system.
PowerShell is DEPRECATED and may ONLY be used as an absolute LAST RESORT when
Python is genuinely impossible (Windows registry, service management, AD, AppX).**

### Decision Protocol (before ANY `exec` call)

```
1. Can this be done with Python? → YES (99%+ of cases)
   → Write to .py file → exec python <file>.py → DONE
2. Is this a native executable (curl.exe, git, pandoc, npx)?
   → exec <executable> <args> → DONE
3. Is this a cmd-native operation (dir, type, copy, del)?
   → exec cmd /c "<command>" → DONE
4. NONE of the above work?
   → PowerShell, but ONLY via .ps1 file. NEVER inline powershell -Command "..."
```

### Why This Mandate Exists

The 2026-07-31 resume portfolio mojibake incident is the canonical case:
PowerShell `Get-Content` silently read UTF-8 source files as CP1252, double-encoding
every non-ASCII character. The corrupted text was committed to GitHub, rendered into
a 29-page PDF with 275 U+FFFF glyph-miss errors, and published to Zenodo
(10.5281/zenodo.21725453) as a supposedly professional resume. A SECOND incident
(computing-machines/paper.md, 42 double-encoded dashes committed to GitHub) was
discovered during the systemic audit. The root cause in both cases was identical:
PowerShell's default encoding (CP1252) ≠ UTF-8, and the corruption is SILENT — no
error, no warning, just garbled characters that propagate through every downstream
system.

**The cumulative cost of PowerShell failures on this system (KIF-05/06/07/09 parse
errors, encoding corruption, quote collapse, $variable eating) exceeds every other
tooling failure pattern combined. Python is installed. Python is reliable. Python
uses UTF-8 by default. Use Python.**

### Integration Points

| Skill | Where | What |
|:------|:------|:------|
| `windows-command-patterns` | §1.0 | Python-First Decision Tree, encoding protocol |
| `research` | Phase 5 PDF Building | Use `build-paper.py` (Python, UTF-8 explicit) |
| `research` | Phase 6 D1 Insert | Python script with `urllib.request`, not PS inline |
| `git-github` | All operations | `exec git ...` directly, or Python `subprocess.run` |
| **All skills** | Before ANY `exec` | Run the §1.0 decision tree. PS = LAST RESORT |

### Pre-Commit Gate

Before EVERY git commit in ANY QNFO repository:

```
python C:\Users\LENOVO\.deepchat\pre-commit-mojibake-scan.py
```

**No exceptions.** This gate exists because the resume v3.3 PDF and computing-machines
paper.md were both corrupted by the exact same PowerShell encoding failure. If the
scanner exits non-zero, the commit is BLOCKED.

### PowerShell Usage (Last Resort Only)

PowerShell may ONLY be used when ALL of the following conditions are met:
1. A Python equivalent has been explicitly confirmed impossible
2. The task falls into a Windows-native category (registry, services, WMI, AD, AppX)
3. The command is written to a `.ps1` file (NEVER inline)
4. `ps-safe-exec.ps1 -Strict` is used as the wrapper
5. The reason for using PowerShell is documented in the commit/session

**If you are about to type `powershell -NoProfile -Command "..."` with ANY `$`, `&`, `|`, or `>` in the command: ABORT. Write a Python file instead.**

### Self-Check (before every `exec`)

1. Python? → .py file
2. Native executable? → direct exec
3. cmd? → cmd /c
4. PowerShell? → PROVE Python can't do it first. If yes: .ps1 file only.

## §0.7 OSTROWSKI DIMENSIONLESS MANDATE (HARD GATE — ALL PHYSICS FORMULAS)

**Effective: 2026-08-01. Applies to ALL QNFO publications containing physics formulas — ALL genres (A/B/C), ALL output channels.**

### Rule (Ironclad)

ALL physics formulas in QNFO publications MUST be expressed in **dimensionless natural numbers** using Planck units ($\hbar = c = G = k_B = 1$). Dimensional formulations (e.g., $S \leq 2\pi k_B R E / (\hbar c)$) implicitly assume only the Archimedean ($\infty$) completion of the rationals. Per Ostrowski's theorem, any quantity defined over $\mathbb{Q}$ has completions at EVERY place — the real Archimedean place and all $p$-adic non-Archimedean places. Expressing a formula in dimensionless pure numbers preserves place-democracy: the numbers do not presuppose which completion is being used.

The natural coordinate system for these dimensionless ratios is the **Bruhat–Tits tree** with $p$-adic valuations $\operatorname{ord}_p$, not the real numbers. The fundamental number system is the Pythagorean semigroup $\mathcal{P} = \{2^a \cdot 3^b \cdot 5^c \mid a,b,c \in \mathbb{N}_0\}$ (5-smooth numbers).

### §0.7.1 Real Numbers Are Not "Real" (v1.4, HARD GATE)

Real numbers are the Archimedean completion of ℚ — ONE place among all completions, not a privileged "reality." Due diligence (Continuum Trilogy Paper I, DOI 10.5281/zenodo.21672990; ODR v1.6-v1.8 red-teams) establishes THREE Archimedean/real-number traps that physics formulas repeatedly fall into. ALL THREE ARE HARD BLOCKS in QNFO publications.

**Trap 1 — Breadth (non-computable reals are unfalsifiable):** The power-set overhang of ℝ — the non-computable reals — has NO physical signature. No finite measurement protocol can discriminate two non-computable reals, so any formula whose content depends on a non-computable value is physically unfalsifiable. Only the DEPTH of ℝ (the Archimedean completion providing limits, continuity, dynamics) is physical. The physical continuum is $\mathbb{R}_c \times \prod_{p \in S} \mathbb{Q}_p^c$ — the computable Archimedean continuum times computable p-adic continua; BREADTH IS ELIMINATED. `[established — Continuum Trilogy Paper I]` A formula invoking a non-computable real (e.g., an uncomputable constant as a physical parameter) is a HARD BLOCK.

**Trap 2 — Decimal (base-10 decimals are one completion's projection):** A base-10 decimal like 1/137.036 or 3.14159 is the Archimedean projection of a ratio evaluated at one scale. It is NOT an Ostrowski/Tate-compliant statement on its own — it silently assumes ℝ and base-10 representation. Every decimal constant MUST be traced to its ratio form: α = r_e/λ̄_C (cross-ratio of classical electron radius to reduced Compton wavelength), π = C/d (circumference-to-diameter), ℏ = E/ω. The decimal is the value of that ratio in ONE completion; the ratio itself is place-democratic.

**Trap 3 — Running couplings (scale-dependent "constants" are functions):** α, sin²θ_W, G_F are not fixed numbers — they are RUNNING FUNCTIONS of the dimensionless energy scale Q̃ = Q/E_P. α(Q̃²) runs 7.14% from 1/137.036 (IR, Q̃→0) to 1/127.9 (Q̃ = M_Z/E_P) `[established — PDG]`. Any formula presenting these as a fixed decimal silently uses the deep-IR Archimedean value at one scale. The compliant presentation: α(Q̃²) = r_e(Q̃)/λ̄_C(Q̃) with the evaluation scale stated. A fixed-decimal presentation of a running coupling is a HARD BLOCK unless accompanied by the running-ratio form AND its evaluation scale.

### Rewrite Protocol

| Dimensional Form | Dimensionless Form (Planck units) |
|:-----------------|:----------------------------------|
| $S \leq 2\pi k_B R E / (\hbar c)$ | $\mathcal{I} \leq 2\pi R E / \ln 2$, $R \equiv R_{\text{phys}}/\ell_P$, $E \equiv E_{\text{phys}}/E_P$ |
| $E \geq k_B T \ln 2$ (Landauer) | $E \geq T \ln 2$ ($E$ and $T$ both dimensionless in Planck units) |
| $S_{\text{BH}} = k_B A / (4\ell_P^2)$ | $S_{\text{BH}} = A / 4$ (area $A$ dimensionless in Planck units) |
| $\alpha = e^2/(4\pi\epsilon_0 \hbar c) \approx 1/137.036$ (v1.4) | $\alpha(\tilde{Q}^2) = r_e(\tilde{Q})/\bar{\lambda}_C(\tilde{Q})$ — running ratio; 1/137.036 is the deep-IR ($\tilde{Q}\to 0$) Archimedean projection, 1/127.9 at $\tilde{Q} = M_Z/E_P$ |

### Well-Known Formula Exception

When a formula is so widely recognized that presenting only its dimensionless form would obscure its identity (e.g., Landauer's principle $E \geq k_B T \ln 2$), BOTH forms must be presented — the dimensional form for recognizability IS accompanied by the dimensionless form AND an explicit Ostrowski rationale explaining that the dimensional form is an Archimedean projection. The rationale is NOT optional; it is the justification for why the paper uses dimensionless quantities elsewhere while temporarily citing a dimensional formulation. Example: "In conventional dimensional form: $E \geq k_B T \ln 2$. In dimensionless Planck units ($\hbar = c = G = k_B = 1$): $E \geq T \ln 2$, where both $E$ and $T$ are pure numbers — Archimedean norms of quantities whose completions exist at every place per Ostrowski's theorem."

### Self-Check (before every physics formula in a publication)

1. Is the formula dimensionless? (no $\hbar$, $c$, $G$, $k_B$ as standalone symbols) → PASS
2. If dimensional: is a dimensionless equivalent presented alongside? → if YES: OK (with rationale). If NO: BLOCKED — rewrite.
3. Is the rational number system explicit? (Planck units, Bruhat-Tits tree, Pythagorean semigroup) → if not, consider adding.
4. **BREADTH CHECK (v1.4):** Does the formula depend on a non-computable real? → if YES: BLOCKED — non-computable reals are physically unfalsifiable (§0.7.1 Trap 1). Only $\mathbb{R}_c \times \prod \mathbb{Q}_p^c$ is physical.
5. **DECIMAL CHECK (v1.4):** Does the formula present a base-10 decimal (1/137.036, 3.14159, 6.674×10⁻¹¹, etc.) as if it were a completion-independent constant? → if YES: BLOCKED unless the ratio form is given (α = r_e/λ̄_C, π = C/d, G = ℓ_P²/(m_P t_P²)) (§0.7.1 Trap 2).
6. **RUNNING CHECK (v1.4):** Does the formula treat α, sin²θ_W, or G_F as a fixed number? → if YES: BLOCKED unless presented as a running function with its evaluation scale (e.g., α(Q̃²) at Q̃→0 or Q̃ = M_Z/E_P) (§0.7.1 Trap 3).

### Integration Points

| Skill | Where | What |
|:------|:------|:------|
| `research` | Phase 5 Pre-Publication Requirements + Professional Publication Standards | Gate: dimensional formulas → BLOCKED unless with dimensionless equivalent + rationale |
| `kaizen` | Anti-Patterns table | Flag: dimensional formula without dimensionless equivalent |
| `frontend-design` | All physics content | Land of dimensionless presentations |

### Why This Mandate Exists

The 2026-08-01 OC paper v1.2 reformatted the Bekenstein bound from $\mathcal{I} \leq 2\pi R E / (\hbar c \ln 2)$ to $\mathcal{I} \leq 2\pi R E / \ln 2$ in dimensionless Planck units, with the note: "The bound's quantities are pure numbers; as such they do not assume the Archimedean completion implicit in dimensional formulations." This edit exposed a systematic pattern: QNFO papers across multiple projects (OC, Cross-Domain Adelic Physics, Continuum Trilogy, non-anthropocentric-natural-units) were using dimensional formulas without acknowledging their Archimedean-completion assumptions. The mandate makes this requirement explicit and enforceable — every paper, every formula, every time.

**Precedent paper:** *Non-Anthropocentric Natural Units* (DOI: 10.5281/zenodo.21480756) reformulated the Bekenstein-Hawking bound without anthropocentric units. This is the canonical reference for the dimensionless program.

**No exceptions.** A dimensional formula without a dimensionless equivalent and Ostrowski rationale in a QNFO publication is a style violation equivalent to a banned word (§0.0) or mojibake (§0.2) — HARD BLOCK.


## §3 DUE DILIGENCE PROTOCOL — KG-First Discovery Gate

Before ANY task involving "what exists":
1. query_graph('stats') — node/edge counts
2. Query D1 portfolio-state for project inventory
3. Query knowledge-graph for cross-project impact
GATE: If KG was NOT queried before claiming "comprehensive" → cherry-picking violation.

## Mandatory Pre-Session Steps
1. Load `email-composer` via `skill_view("email-composer")` for business communication
2. Load `knowledge` via `skill_view("knowledge")` for KG + memory
3. This skill is ALWAYS loaded at session start (visible in skill_list)
