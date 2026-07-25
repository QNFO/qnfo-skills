# Springer Nature LaTeX Template — QNFO Default Standard

**Status: MANDATORY DEFAULT TEMPLATE for all QNFO publications, papers, and
publication-grade PDFs**, effective 2026-07-25.

This directory contains the **official, current Springer Nature LaTeX
authoring template** (`sn-jnl.cls`, v3.1, December 2024), downloaded directly
from Springer Nature's LaTeX Author Support page
(https://www.springernature.com/gp/authors/campaigns/latex-author-support),
plus a QNFO-conventions overlay (`qnfo-paper-template.tex`) that adds the
mandatory Declarations block, AI-disclosure language, and QNFO author
attribution as defaults.

## Why this template, and not `svjour3`/`svjour.cls`

An earlier version of this skill's guidance (and the original draft of *The
Macroscopic Boundary Problem in Quantum Reconstructions*) referenced the
legacy `svjour3.cls`/`svjour.cls` package (CTAN package name: `springer`,
`ctan.org/pkg/springer`). **That package is retired.** Springer Nature
unified all of its journals (Mathematics, Physics, Computer Science, Nature
Portfolio, BMC, etc.) onto a single `sn-jnl.cls` class starting around 2019.
The old per-journal `svjour3` class files (e.g., `svmult.cls`, `svcalco.clo`)
are still archived on CTAN but are **not the current submission standard**
for Foundations of Physics or any other live Springer Nature journal. Do not
resurrect `svjour3` for new work — this was corrected via live verification
against Springer Nature's own LaTeX Author Support page on 2026-07-25.

## Files in this directory

| File | Purpose |
|---|---|
| `sn-jnl.cls` | The official Springer Nature document class (v3.1, Dec 2024). Required in the same directory as any `.tex` file using it. |
| `sn-article.tex` | Springer Nature's own unmodified example/reference template — useful for seeing every supported feature (tables, algorithms, theorem environments, appendices). |
| `sn-bibliography.bib` | Springer Nature's example `.bib` file, paired with `sn-article.tex`. |
| `user-manual.pdf` | The official Springer Nature LaTeX template user manual — consult for the full class-option list and advanced formatting. **Present locally but excluded from the `qnfo-skills` git repo** per ADR-026 (binary/PDF bloat policy — `.gitignore` blocks `**/*.pdf` even inside allowlisted skill directories). Re-download from the Springer Nature LaTeX Author Support page if this file is missing after a fresh skill sync: https://www.springernature.com/gp/authors/campaigns/latex-author-support |
| `bst/*.bst` | All 9 supported bibliography styles (see table below). Copy the ONE needed style into the same directory as your `.tex`/`.bib` files before running `bibtex` — see Build Instructions. |
| `qnfo-paper-template.tex` | **START HERE for new QNFO papers.** A QNFO-conventions overlay pre-populated with: mandatory Declarations subsections (Funding, Conflicts of Interest, Ethics, Consent, Author Contributions, Data/Materials/Code Availability, Use of Artificial Intelligence), QNFO author attribution block, and section-numbering scaffold. |

## Class Options (choose ONE `sn-*` option per paper)

| Option | Use case |
|---|---|
| `sn-mathphys-num` | **QNFO DEFAULT.** Numbered references — Mathematics and Physical Sciences. Matches Foundations of Physics and most physics-foundations journals. |
| `sn-mathphys-ay` | Same discipline, Author-Year citation style (use only if the target journal explicitly requires author-year). |
| `sn-basic` | Generic Springer Nature style (non-physics, e.g., social science, humanities). |
| `sn-nature` | Nature Portfolio journals specifically. |
| `sn-aps` | American Physical Society reference style. |
| `sn-vancouver-num` / `sn-vancouver-ay` | Life sciences / medicine, Vancouver style. |
| `sn-chicago` | Chicago-based humanities reference style. |
| `sn-apacite`/APA | Social science APA style. |

Set via `\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}` in the preamble.

## Build Instructions (verified working, TeX Live 2025, Windows, 2026-07-25)

```powershell
$env:PATH += ';C:\texlive\2025\bin\windows'   # or wherever TeX Live is installed

# 1. Copy sn-jnl.cls into the SAME directory as your paper.tex
Copy-Item <this-dir>\sn-jnl.cls .

# 2. Copy the ONE .bst file matching your \documentclass option into the
#    SAME directory as paper.tex/refs.bib -- bibtex does NOT search
#    subdirectories by default and fails with
#    "I couldn't open style file <name>.bst" otherwise.
Copy-Item <this-dir>\bst\sn-mathphys-num.bst .

# 3. Four-pass build (standard LaTeX+BibTeX convergence)
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

**Kaizen finding (2026-07-25):** the single most common build failure with
this template is forgetting step 2 — the `.bst` files ship in a `bst/`
subdirectory, but `bibtex` on a default TeX Live install will not find them
there relative to the `.tex`/`.aux` file. Always copy the needed `.bst`
alongside the paper before running `bibtex`.

## Mandatory Declarations Block

Every QNFO paper MUST include a `\section*{Declarations}` with ALL of the
following subsections, even if the answer is "Not applicable" for a given
one (Springer Nature explicitly requires this — an omitted subsection is
treated as an incomplete submission):

1. Funding
2. Conflicts of Interest (or "Competing Interests" per journal preference)
3. Ethics Approval and Consent to Participate
4. Consent for Publication
5. Author Contributions
6. Data Availability
7. Materials Availability
8. Code Availability
9. **Use of Artificial Intelligence** (QNFO-specific mandatory addition,
   not part of the stock Springer Nature template — see Physics Writing
   Standards / Publication Language Gate in the `qnfo-agent` skill).
   Springer Nature's official AI-authorship policy (verified live from
   `link.springer.com/journal/10701/submission-guidelines`, 2026-07-25):
   LLMs "do not currently satisfy authorship criteria" (no accountability),
   and any LLM use beyond pure copy-editing MUST be disclosed in the
   Methods section (or, if no Methods section exists, in a suitable
   alternative part — QNFO convention: the Declarations section).

`qnfo-paper-template.tex` pre-populates all nine subsections with QNFO's
standard language — edit the content, do not delete the headings.

## See Also

- `research/SKILL.md` §"Professional Publication Standards" for the
  journal-grade copyediting, tone, and structural requirements that apply
  on top of this template's formatting.
- `qnfo-agent/SKILL.md` §"Physics Writing Standards (18-Point Checklist)"
  and §"Publication Language Gate" for content-integrity requirements.
