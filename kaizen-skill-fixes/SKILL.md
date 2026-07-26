---
name: kaizen-skill-fixes
description: QEC Skill Fixes — Pandoc XeLaTeX Unicode, credential leaks, PowerShell patterns, Zenodo provenance, Pub Language Gate, OSF full-API-automation correction, Epistemic Bias Fixes (Institution Fallacy, Convergence Trap, Symmetry Requirement)
version: 1.5.0
tags:
  - kaizen
  - skill-fix
  - qec
  - osf
  - epistemic-bias
---

# KAIZEN SKILL FIXES — v1.6

> Generated 2026-07-20 from the No Thing + Huang Response deep-dive session.
> v1.1: Added E1 (OSF full API automation — corrects prior false claim of manual-intervention requirement).
> v1.2: Added F1 (Buffer GraphQL API — fixes 3 critical bugs in the post-creation template).
> v1.3: Added G1/G2/G3 (Epistemic Bias Fixes from PQS AI-Evaluation Audit 2026-07-24 — Institution Fallacy, Convergence Trap, Symmetry Requirement).
> v1.4: Added H1 (Cross-Domain Consilience Translation Protocol — research skill Phase 1, 2026-07-26).
> v1.5: Added I1 — KIF-30 Mandatory PDF Inclusion in all Zenodo Deposits (2026-07-26).
> v1.6: Added J1 — KIF-31 Acronym Hallucination Gate (2026-07-26). Model fabricated "Zhu, Brad, Wang" as expansion of ZBW (Zitterbewegung) during paper-13 writing; published to Zenodo before detection. Added Acronym Expansion Gate to qnfo-agent §7 Publication Standards.
> All fixes are concrete skill-system improvements, not project-specific work.

## execute_plan

update_plan([
  {"step": "A1: Pandoc+XeLaTeX Unicode→LaTeX preprocessor (CRITICAL)", "status": "pending"},
  {"step": "A2: Strip keywords YAML before Pandoc build (CRITICAL)", "status": "pending"},
  {"step": "A3: PROVENANCE-BUNDLE.zip HARD GATE before Zenodo (CRITICAL)", "status": "pending"},
  {"step": "A4: Pre-commit credential scan + _*.py in .gitignore (CRITICAL)", "status": "pending"},
  {"step": "B1-B3: PowerShell/Windows anti-patterns (HIGH)", "status": "pending"},
  {"step": "C3: Vectorize confirmation bias disclosure (MEDIUM)", "status": "pending"},
  {"step": "D2: Pub Language Gate extended for credentials (LOW)", "status": "pending"},
  {"step": "E1: OSF full API automation — corrected false claim (CRITICAL, CORRECTION)", "status": "pending"},
  {"step": "F1: Buffer API — fix broken inline fragments, add missing assets:[] (CRITICAL, 2026-07-22)", "status": "pending"},
  {"step": "H1: Cross-Domain Consilience Translation Protocol — research skill Phase 1 (HIGH, 2026-07-26)", "status": "pending"},
  {"step": "I1: Mandatory PDF inclusion in all Zenodo deposits — research §5 P5.PDF HARD GATE (CRITICAL, 2026-07-26)", "status": "pending"},
  {"step": "J1: Acronym Hallucination Gate — KIF-31, qnfo-agent v3.50 §7 (CRITICAL, 2026-07-26)", "status": "completed"},
])

---

## E: CORRECTION — OSF Registration IS Fully API-Automatable (prior claim was FALSE)

### E1: OSF Preregistration Submission — Full API Automation Protocol

**Prior false claim (retracted):** The research skill previously stated "OSF Registration Completion... requires browser interaction with the registration form" and "Do NOT request manual browser interaction... document the draft URLs... but do NOT block publication on this step." **This was WRONG.** It was an untested assumption never verified against the live API.

**Verified truth (2026-07-20, live API test):** The entire OSF Preregistration submission — schema discovery, field population, subject taxonomy assignment, and final registration creation — is 100% achievable via the OSF v2 REST API with zero browser interaction. The task was completed live: registration `kj6ar` created with `date_registered` timestamp, all 18 schema fields populated, HTTP 201 on final submission.

**Root cause of the prior false claim:** The agent assumed the schema's `registration_responses` dict used documented/guessable keys (e.g., `q1`, `q2`) and failed silently or got 404s, then concluded "the API doesn't support this" instead of discovering the ACTUAL key format via the schema introspection endpoints below.

#### Step 1: Discover real schema question keys (NEVER guess keys like `q1`)

```python
import requests
H = {'Authorization': 'Bearer ' + OSF_TOKEN, 'Content-Type': 'application/vnd.api+json'}
SCHEMA_ID = '697b72f611a8e98484c6139b'  # OSF Preregistration

r = requests.get(f'https://api.osf.io/v2/schemas/registrations/{SCHEMA_ID}/schema_blocks/?page[size]=100', headers=H)
blocks = r.json()['data']

# Real keys look like '344-2', '344-4', '344-47' — NOT 'q1'/'q2'
last_label = None
question_map = []
for b in blocks:
    attrs = b['attributes']
    bt = attrs['block_type']
    key = attrs.get('registration_response_key')
    text = attrs.get('display_text') or ''
    if bt == 'question-label':
        last_label = text
    if key:
        question_map.append((key, last_label, bt, attrs.get('required', False)))

for key, label, bt, required in question_map:
    print(f'{key} | required={required} | {bt} | {label}')
```

This returns the REAL keys (e.g., `344-2` = "Research questions or hypotheses", `344-47` = "Data collection procedures"). Only fields where `required=True` MUST be populated; the rest are optional but recommended.

#### Step 2: For select/multi-select fields, get EXACT option text (must match verbatim)

```python
# For a given select-type key (e.g., '344-4'), fetch the exact allowed option strings.
# The API rejects any option text that doesn't match VERBATIM (not even truncation is allowed).
capture = False
options = []
for b in blocks:
    attrs = b['attributes']
    key = attrs.get('registration_response_key')
    if key == TARGET_KEY:
        capture = True
        continue
    if capture:
        if attrs['block_type'] == 'select-input-option':
            options.append(attrs.get('display_text'))
        else:
            break
print(options)  # Use EXACT strings from this list, not paraphrases
```

#### Step 3: Create draft, populate all fields in ONE PATCH call

```python
draft_data = {
    'data': {
        'type': 'draft_registrations',
        'attributes': {},
        'relationships': {
            'branched_from': {'data': {'type': 'nodes', 'id': NODE_ID}},
            'registration_schema': {'data': {'type': 'schemas', 'id': SCHEMA_ID}}
        }
    }
}
r = requests.post(f'https://api.osf.io/v2/nodes/{NODE_ID}/draft_registrations/', headers=H, json=draft_data)
draft_id = r.json()['data']['id']

# Populate ALL required + optional fields keyed by the REAL keys discovered in Step 1.
# Single-select: plain string (must exactly match an option from Step 2).
# Multi-select: list of strings.
# Long-text: plain string, any content.
responses = {
    '344-2': 'Full hypothesis text...',
    '344-4': 'Analyses in this plan have been conducted already. At least some of the analyses described in this analysis plan have been conducted by the authors making this a retrospective registration.',
    '344-17': ['Descriptive study: Describing some features of a dataset or sample, but typically not for the purposes of informing a causal effect.'],
    '344-32': ['No blinding is involved.'],
    # ... all other required keys (344-40, 344-47, 344-51, 344-55, 344-58, 344-62, 344-66, 344-71, 344-75, 344-77, 344-79, 344-81)
}
patch = {'data': {'id': draft_id, 'type': 'draft_registrations', 'attributes': {'registration_responses': responses}}}
r2 = requests.patch(f'https://api.osf.io/v2/draft_registrations/{draft_id}/', headers=H, json=patch)
# 200 = all fields validated successfully. 400 with "must be one of the provided options" = re-check Step 2 exact text.
```

#### Step 4: MANDATORY — Set subject taxonomy (registration will 400 without this)

**Gotcha:** `POST /nodes/{id}/registrations/` fails with `"Registration must have at least one subject to be registered"` even if the node/draft appears otherwise complete. Subjects use a **root→leaf chain**, not a bare category ID.

```python
# Search subject taxonomy by keyword
r = requests.get('https://api.osf.io/v2/subjects/?filter[text]=Physics', headers=H)
leaf_id = ...  # pick the most specific matching subject, e.g. "Quantum Physics"

# Walk parent chain to build full root->leaf list
chain = []
current = leaf_id
while current:
    r = requests.get(f'https://api.osf.io/v2/subjects/{current}/', headers=H)
    d = r.json()['data']
    chain.insert(0, current)
    parent = d.get('relationships', {}).get('parent', {}).get('data')
    current = parent['id'] if parent else None

# Set on the DRAFT REGISTRATION itself (not the parent node!) — flat list format
patch = {'data': {'id': draft_id, 'type': 'draft_registrations', 'attributes': {'subjects': chain}}}
r2 = requests.patch(f'https://api.osf.io/v2/draft_registrations/{draft_id}/', headers=H, json=patch)
# Must be 200. Note: node-level subjects (list-of-lists format) and draft-level subjects
# (flat-list format) are SEPARATE relationships — setting one does NOT set the other.
```

#### Step 5: Submit for final registration

```python
reg_data = {
    'data': {
        'type': 'registrations',
        'attributes': {
            'draft_registration': draft_id,
            'registration_choice': 'immediate'  # or 'embargo' with embargo_end_date
        }
    }
}
r = requests.post(f'https://api.osf.io/v2/nodes/{NODE_ID}/registrations/', headers=H, json=reg_data)
# HTTP 201 = SUCCESS. Registration is created with date_registered timestamp — fully immutable.
```

#### Step 6: Understand `pending_registration_approval` (this is NOT a manual-review blocker)

After successful `201 Created`, the registration attribute `pending_registration_approval` will show `true`. **This is expected and is NOT equivalent to "incomplete" or "requires manual browser action."** OSF's error message on any approve-trigger attempt confirms: `"OSF Registries is an unmoderated provider."`

This flag reflects OSF's built-in **email confirmation security gate** — identical in purpose to email-verify-your-account flows — sent automatically to the registering account holder, required uniformly for ALL registrations (human or API-created) as an anti-hijacking control so a leaked API token cannot alone publish immutable science under someone's name. It is:
- NOT a moderation queue (OSF Registries has none)
- NOT bypassable by design (this is intentional, not a bug or missing endpoint)
- Resolved by the account owner clicking the confirmation link OSF emails on registration creation

**Correct language for future skill/agent reporting:** "Registration submitted successfully (HTTP 201, ID `{reg_id}`). OSF requires email confirmation from the account holder before the registration is finalized and made public — this is OSF's standard anti-hijacking safeguard, not a manual data-entry step. No further API-side work is possible or required."

**Never again claim:** "requires browser interaction," "Waterbutler limitation," or "cannot be automated" for the registration submission itself. Those claims were false. Only the final email-click confirmation (equivalent to 2FA) is outside API scope, and that is a security feature, not a gap.

### Anti-Pattern Correction

| Old (WRONG) instruction in `research` skill | Corrected instruction |
|---|---|
| "Registration drafts are created via API but form completion... requires browser interaction with the registration form... do NOT block publication on this step" | Registration drafts AND full form completion AND final submission are 100% achievable via API. Discover real schema keys via `/schema_blocks/`, never assume `q1`/`q2` naming. Set subject taxonomy chain (mandatory, root→leaf) before submitting. After 201, `pending_registration_approval: true` is the expected final state pending only the account holder's email confirmation — report this precisely, do not describe it as "needs manual completion." |
| "OSF file upload — NOT SUPPORTED via API... link to Zenodo/GitHub instead" | This remains TRUE for file uploads specifically (Waterbutler requires cookie sessions) — do not conflate file upload limitations with registration/form-completion limitations. They are different subsystems with different constraints. |

---

## A: CRITICAL Fixes (Blocks publication quality or causes data loss)

### A1: Pandoc+XeLaTeX Unicode Math Rendering Failure

**Problem:** XeLaTeX default font (Latin Modern) lacks Unicode Greek subscript/superscript glyphs. Symbols ω₀₁, α, 10⁻⁴, |0⟩, ℚ, ℝ all produce `U+FFFF` (replacement characters) in PDF output.

**Fix:** Add Unicode→LaTeX math preprocessor to PDF build step.

```python
# _build_pdf.py — Pandoc+XeLaTeX with Unicode math preprocessing
import re, subprocess, os, fitz

with open('paper.md', 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('---', 2)
if len(parts) >= 3:
    yaml_header = parts[1]
    body = parts[2]
    yaml_header = re.sub(r'\nkeywords:\n(?:  - .+\n)+', '', yaml_header)
    math_blocks = []
    def save_math(m):
        math_blocks.append(m.group(0))
        return f'<<<MATH{len(math_blocks)-1}>>>'
    body = re.sub(r'\$\$[^$]+\$\$', save_math, body)
    body = re.sub(r'\$[^$]+\$', save_math, body)
    greek = {'α':'\\alpha','ω':'\\omega','φ':'\\phi','π':'\\pi',
             'ℚ':'\\mathbb{Q}','ℝ':'\\mathbb{R}','ℂ':'\\mathbb{C}','ℤ':'\\mathbb{Z}'}
    for uni, latex in greek.items():
        body = body.replace(uni, '$' + latex + '$')
    symbols = {'⊗':'\\otimes','×':'\\times','≈':'\\approx',
               '≥':'\\ge','≤':'\\le','⟨':'\\langle','⟩':'\\rangle'}
    for uni, latex in symbols.items():
        body = body.replace(uni, '$' + latex + '$')
    body = body.replace('−', '-')
    for sub, d in {'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9'}.items():
        body = body.replace(sub, '_{' + d + '}')
    for sup, d in {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9'}.items():
        body = body.replace(sup, '^{' + d + '}')
    for i, block in enumerate(math_blocks):
        body = body.replace(f'<<<MATH{i}>>>', block)
    content = '---' + yaml_header + '---' + body

with open('build.md', 'w', encoding='utf-8') as f:
    f.write(content)

result = subprocess.run(
    ['pandoc', 'build.md', '-o', 'paper.pdf', '--pdf-engine=xelatex', '--metadata', 'date=' + date_str],
    capture_output=True, text=True
)

if result.returncode == 0:
    os.remove('build.md')
    doc = fitz.open('paper.pdf')
    errors = [p.number for p in doc if '\ufffd' in p.get_text()]
    if errors:
        for pn in errors[:3]:
            for line in doc[pn].get_text().split('\n'):
                if '\ufffd' in line:
                    print(f'REPLACEMENT CHAR p{pn}: {line.strip()[:100]}')
        raise SystemExit('PDF contains Unicode replacement characters')
    print(f'OK: {len(doc)} pages, CLEAN')
```

**Affected skills:** `research` §5 (PDF Building), `pdf` skill

### A2: Pandoc Keywords YAML Causes \xmpquote Error

**Problem:** Pandoc passes the `keywords:` YAML list to XeLaTeX's XMP metadata module, which calls the undefined `\xmpquote` command.

**Fix:** Strip `keywords:` block from YAML frontmatter before Pandoc build. Already handled in A1 preprocessor above.

### A3: PROVENANCE-BUNDLE.zip Missing from Zenodo Deposits

**Problem:** Research skill Phase 5 lists `PROVENANCE-BUNDLE.zip` in the upload example but has NO hard gate check. Agents routinely skip it.

**Fix:** Add HARD GATE P5.5 to Pre-Flight checklist:
```
| P5.5 | PROVENANCE-BUNDLE.zip built and verified? | HARD | Bundle exists, contains paper.md, paper.pdf, PROJECT-PLAN.md, README.md, all artifacts/*.md, all docs/*.md; size ≥ 10 KB |
```

Add build script to Phase 5:
```python
import zipfile, os
files = ['paper.md', 'paper.pdf', 'PROJECT-PLAN.md', 'README.md']
for d in ['artifacts', 'docs']:
    for f in os.listdir(d):
        if f.endswith('.md'):
            files.append(f'{d}/{f}')
with zipfile.ZipFile('PROVENANCE-BUNDLE.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files:
        z.write(os.path.join(project_root, f), f)
```

### A4: API Tokens Committed to Git

**Problem:** `_zenodo_upload.py`, `_d1_insert.py` contain Zenodo/Cloudflare tokens. GitHub push protection blocks but remediation (amend, force-push) costs time.

**Fix:**
1. Add `_*.py` to default `.gitignore` template (Phase 0)
2. Add pre-commit credential scan to Phase Closeout Protocol:
```python
import re, sys, subprocess
result = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True)
for fname in result.stdout.strip().split('\n'):
    if not fname: continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    patterns = [r'cfat_[a-zA-Z0-9_]{30,}', r'ghp_[a-zA-Z0-9]{36}',
                r'sk-[a-zA-Z0-9]{48,}', r'Bearer [A-Za-z0-9+/=]{30,}']
    for p in patterns:
        if re.search(p, content):
            print(f'BLOCKED: {fname} contains credential matching {p[:20]}...')
            sys.exit(1)
print('GATE: No credentials found in staged files')
```

---

## B: HIGH Fixes (Causes failed tool calls or wrong output)

### B1-B3: Windows Shell Anti-Patterns

**Problem:** `python -c "..."` with nested quotes, `&&` chaining in PowerShell, `curl` alias to `Invoke-WebRequest` all cause tool call failures.

**Pattern 1:** Replace `python -c "..."` with `write`→`exec`→`rm` pattern for multi-line scripts.
**Pattern 2:** Use `;` not `&&` in PowerShell. Use `git -C <path>` not `cd && git`.
**Pattern 3:** Use `python -c 'import urllib.request;...'` or `curl.exe` not `curl` on Windows.

---

## C: MEDIUM Fixes

### C3: Vectorize Confirmation Bias Disclosure

**Problem:** QNFO Vectorize indexes 0 external papers. Every semantic search returns only QNFO-friendly results. Agents treat these as comprehensive literature searches.

**Fix:** Add to research skill Phase 1 Due Diligence protocol:
> **DISCLOSURE GATE:** If all Vectorize results are QNFO-internal (all DOIs contain 'zenodo' and author is 'QNFO Research'), append: "[CONFIRMATION BIAS WARNING: Vectorize index contains 0 external papers. This search may systematically underrepresent skeptical or contradictory external literature.]" Then run arXiv + Semantic Scholar search in parallel.

---

## D: LOW Fixes

### D2: Publication Language Gate Extended for Credential Leaks

**Problem:** Pub Language Gate scans for internal language (`Module N`, `SPRINT`, etc.) but not for API tokens.

**Fix:** Extend gate regex to include credential patterns as BLOCKING:
```python
cred_patterns = [
    r'cfat_[a-zA-Z0-9_]{30,}',
    r'ghp_[a-zA-Z0-9]{36}',
    r'sk-[a-zA-Z0-9]{48,}',
    r'Bearer [A-Za-z0-9+/=]{30,}',
    r'PINATA_API_KEY=',
    r'ZENODO_TOKEN=',
]
```

---

## Implementation Notes

1. All A-priority fixes go into `research` skill §5 (Publication)
2. B-priority fixes go into `qnfo-agent` skill §8.5 (JIT Thin-Client Protocol, Windows section)
3. C3 goes into `research` skill §1 (Due Diligence)
4. D2 goes into `research` skill §5 (Publication Language Gate)
5. **E1 REPLACES** the entire "OSF Registration Completion" subsection and "OSF File Upload" caveat in `research` skill §5 — the file-upload limitation is real and stays, but the "requires browser interaction" claim for registration/forms is DELETED and replaced with the full API protocol above.
6. **H1** goes into `research` skill Phase 1 as "Cross-Domain Consilience Gate (KIF-29, SOFT)", positioned after the existing epistemic bias gates (KIF-16/KIF-17/KIF-18).
7. **I1** goes into `research` skill §5 (Zenodo Upload section) as HARD GATE P5.PDF — verify all PDFs exist locally and pass KIF-27 verification before any Zenodo `actions/publish` call.

**Cross-references:**
- `research` v2.24 — HARD GATE P5.PDF, updated file upload list, newversion PDF requirement
- `qnfo-agent` v3.49 — KIF-30 registry entry, anti-pattern table extension
- Live demonstration: ALP v1.0 (no PDFs) → v2.0 (12 PDFs + bundle), DOIs 10.5281/zenodo.21609539 → 10.5281/zenodo.21609602

### Implementation Notes (I1)

I1 goes into `research` skill §5 (Zenodo Upload section) as HARD GATE P5.PDF. The gate must pass before any Zenodo `actions/publish` call — verify `paper.pdf` (and all program PDFs) exist locally, are built from the current source, and pass the KIF-27 PDF rendering verification gate.

---

## J: CRITICAL Fix — Acronym Hallucination Gate (KIF-31, 2026-07-26)

### J1: Model Fabricates Acronym Expansions

**Problem:** During paper-13 ("The Silent Parameter as the Local Langlands Correspondence for GL(1) at p = 2") writing in the ALP closeout session, the model parenthetically expanded "ZBW" as "(Zhu, Brad, Wang)" — three fabricated author initials. The correct expansion is "Zitterbewegung" — the quantum mechanical oscillatory phenomenon at the heart of the entire ZBW research program. The fabricated expansion was published in both the markdown source and the PDF, uploaded to Zenodo (deposit 21610573), and survived all existing quality gates undetected.

**Root cause:** The model encountered a 3-letter opaque token "ZBW" during prose generation. When expanding it for the "first use spells out" convention, no grounded expansion was available in immediate context. The model filled the ambiguity slot via intelligent completion — generating plausible words for each initial letter (Z→Zhu, B→Brad, W→Wang) — producing text that was syntactically correct, domain-adjacent (person names in an academic paper), and passed all existing gates: Publication Language Gate (no internal language), PDF rendering check (clean), credential scan (not a token).

**Why existing gates failed to catch this:**
| Gate | Why it passed |
|:-----|:--------------|
| Publication Language Gate | "Zhu, Brad, Wang" is well-formed English, not internal project language |
| PDF Rendering Gate (KIF-27) | No Unicode issues in ASCII names |
| Credential Scan (KIF-04) | Not a token pattern |
| Physics Writing Standards | Passes all 18 points — it's grammatical prose |
| Banned Words Scan | No banned words in the fabricated phrase |
| Pre-Publication Checklist | All items check out for well-formed text |

The failure is **structural**: all existing gates check *surface quality* (syntax, formatting, absence of bad patterns). None check *semantic grounding* — whether a claim that looks like a fact actually traces to a verifiable source in the project's knowledge base.

**Fix — Acronym Expansion Gate (KIF-31, MANDATORY):**

1. Added to `qnfo-agent` §7 Publication Standards: before publishing any paper containing a parenthetical acronym expansion, VERIFY the expansion against:
   - All prior papers in the project's `artifacts/` directory (grep the acronym)
   - Project memories (`search_memories` for acronym + expansion)
   - D1 living-paper entries and KG nodes
   - The project's PROJECT-PLAN.md and research plans

2. If zero prior occurrences found → flag: `[UNVERIFIED-ACRONYM: ZBW → "Zhu, Brad, Wang" — zero prior occurrences in any QNFO artifact. VERIFY before publication.]`

3. **HARD RULE:** If the full term is unknown, do not use the acronym. Spell out the term. If you cannot spell it out, that is evidence you should not be using the abbreviation.

4. Added KIF-31 to `qnfo-agent` §0.11 Known-Issues-Fixed Registry.

5. Added anti-pattern to `qnfo-agent` Anti-Patterns table: "Expanding an acronym with a fabricated phrase not grounded in any project artifact."

**Vulnerability surface analysis:** The acronym hallucination failure mode is a special case of a broader class: **intelligent slot-filling** — any time the model encounters a "slot" in generated text that requires specific, grounded knowledge not available in context, it will fill it with plausible fiction. Other potential slot types: citation references, equation numbers, author names, data values, DOI numbers. The remediation principle generalizes: **before publishing, every factual assertion that is NOT a self-contained logical deduction from the paper's own content must be traced to a prior project artifact or flagged as unverified.**

### Anti-Pattern Correction Table

| Old (WRONG) behavior | Corrected behavior |
|:---------------------|:-------------------|
| Expand acronym "ZBW" → "Zhu, Brad, Wang" (fabricated) | "Zitterbewegung (ZBW)" — verified against all prior project artifacts |
| Trust that well-formed prose expansions are correct | Verify every parenthetical acronym expansion against the project knowledge base |
| No check on acronym grounding before publication | Acronym Expansion Gate: flag `[UNVERIFIED-ACRONYM]` for any expansion with zero prior occurrences |
| Acronym defined on first use by any plausible expansion | If the full term is unknown, spell it out OR don't use the acronym |

### Verification

- Paper-13 corrected: "ZBW (Zhu, Brad, Wang)" → "Zitterbewegung (ZBW)" in source markdown
- PDF rebuilt: 12 pages, CLEAN (0 U+FFFD), verified "Zitterbewegung" rendered correctly
- qnfo-agent SKILL.md: v3.50 with KIF-31 registry entry, Acronym Expansion Gate in §7, anti-pattern in table
- kaizen-skill-fixes SKILL.md: v1.6 with §J1

### Implementation Notes (J1)

J1 goes into `qnfo-agent` §7 (Publication Standards) as "Acronym Expansion Gate (KIF-31, MANDATORY)." The verification procedure uses existing tools (`grep`, `search_memories`) and requires no new infrastructure. The gate is positioned before the Publication Language Gate in §7 so that fabricated expansions are caught before style-checking occurs.

**Verification:** After applying fixes, rebuild the Huang response v2.3 PDF — should render 16 pages CLEAN

---

## F: CRITICAL Fix — Buffer GraphQL API (2026-07-22)

### F1: Broken Inline Fragments + Missing `assets: []` in Post Creation Template

**Problem:** The `research` skill's Buffer section (v2.11) contained 3 critical bugs that prevented posting:

1. **Inline fragments don't work on `PostActionPayload` union**: `... on PostActionSuccess { post { id status } }` and `... on InvalidInputError { message }` cause `GRAPHQL_VALIDATION_FAILED` because `PostActionPayload` union member types are NOT accessible as fragment targets. Attempting them produces `Unknown type "PostActionSuccess". Did you mean "DeletePostSuccess", "CreatePostGroupSuccess"...`

2. **Missing `assets: []`**: The `assets` field in `CreatePostInput` is `NON_NULL` (required) but the mutation template omitted it entirely, producing `InvalidInputError` at runtime.

3. **Wrong schedulingType value**: The `notification` enum value exists in the schema but does NOT work for posting — only `automatic` works for `mode: addToQueue`.

**Root cause (Bug 1):** The previous fixer assumed union types support inline fragment dispatch, but `PostActionPayload` is a restricted union — its members are not introspectable as fragment targets. The typenames ARE correct (`PostActionSuccess`, `InvalidInputError`) at runtime, but the GraphQL validator rejects them in fragments.

**Root cause (Bug 2):** The `CreatePostInput` type introspection (via `__type(name: "CreatePostInput")`) shows `assets` as `NON_NULL` of type `LIST`. The field was simply never added to the template after the v2.11 migration from `createDraft` → `createPost`, which has a completely different input schema.

**Fix:**

1. **Replace inline fragments with bare `__typename`** in the mutation query. Check `data.createPost.__typename` in the response: `"PostActionSuccess"` = success; `"InvalidInputError"` = failure.

2. **Add `assets: []`** to the mutation input — always an empty list for text-only posts (media-free).

3. **Change `schedulingType: notification` → `schedulingType: automatic`** everywhere.

4. **Add enum quoting anti-pattern**: GraphQL enum values MUST be unquoted identifiers (`automatic` not `"automatic"`). Quoting them as strings produces `Enum "SchedulingType" cannot represent non-enum value: "automatic"`.

5. **Created `scripts/buffer-post.py`** — a reusable CLI tool for Buffer posting with live channel discovery, dry-run mode, and proper error handling. Located at `research/scripts/buffer-post.py`.

**Corrected mutation (v2.13):**
```graphql
mutation {
  createPost(input: {
    channelId: "<liveIdFromDiscovery>",
    text: "<post text>",
    schedulingType: automatic,
    mode: addToQueue,
    assets: [],                    # REQUIRED — always pass empty list
    saveToDraft: false
  }) {
    __typename                     # Just __typename, NO inline fragments
  }
}
```

**Additional findings from this session:**

- `https://api.buffer.com/graphql` is the preferred endpoint (bare `https://api.buffer.com` also works)
- `api.bufferapp.com` returns 404 for ALL paths — domain fully deprecated
- Buffer REST API actively rejects Personal Access Tokens: `"Public API tokens are not accepted for REST API access"`
- PowerShell `Get-Content` can return stale/cached token values — ALWAYS use Python `open().read().strip()` to read tokens
- Token is 43 chars, suffix `14Ky`, stored at `%USERPROFILE%\buffer\token`
- Organization ID: `683832fdf3b32ba49eb7cf34`
- Verified live channel IDs (2026-07-22): Twitter=`685cd2c2acfb098c697a8786`, LinkedIn=`6a170337c687a22dd430685f`, Bluesky=`6a01d129090476fb9909d885`

**Anti-pattern correction table:**

| Old (WRONG) instruction in `research` skill | Corrected instruction |
|---|---|
| "Always include `__typename` AND inline fragment `... on PostActionSuccess { post { id status } }`" | Just use `__typename` — inline fragments on `PostActionPayload` union members raise `GRAPHQL_VALIDATION_FAILED`. Check `typename == "PostActionSuccess"` in the response body instead. |
| Mutation template omitted `assets` field entirely | Always pass `assets: []` — `assets` is NON_NULL required in `CreatePostInput` |
| "`schedulingType: notification` is valid" | Use `schedulingType: automatic` — `notification` exists in schema but doesn't work for posting |
| "Always include `... on InvalidInputError { message }` to catch text-too-long" | Same fragment problem — check `__typename == "InvalidInputError"` in the response instead |

**Verification:** All 3 posts (Twitter, LinkedIn, Bluesky) published successfully via `createPost` with the corrected mutation template on 2026-07-22 for the IQM/DB quantum railway scheduling critique.

---

## G: EPISTEMIC BIAS FIXES (2026-07-24, PQS AI-Evaluation Audit Session)

### G1: Institution Fallacy (KIF-16)

**Problem:** Agent treated "not peer reviewed" as a heuristic for "fringe/unreliable" when evaluating the Post-Quantum Synthesis framework, replicating dismissive framing from AI source conversations without questioning it.

**Root cause:** Both Claude and Gemini conversations in the source material used "fringe" framing. The agent uncritically replicated this bias instead of evaluating the claims directly against evidence.

**Fix:**
1. Added **Institutional Status Neutrality Gate** to `research` skill Phase 1 Due Diligence
2. Added Rule 6 to `qnfo-agent` §0.0 Research Integrity Mandate: "INSTITUTIONAL STATUS IS NOT EVIDENCE"
3. Banned "fringe"/"pseudoscience"/"crank"/"crackpot" without specific `[CONTRADICTS ESTABLISHED EVIDENCE: <specific>]` citations
4. Replaced social categories with epistemic categories: `[UNFALSIFIABLE]`, `[CONTRADICTS ESTABLISHED EVIDENCE: <specific>]`, `[UNTESTED]`, `[CONTESTED: <specific debate>]`

**User statement for the record:** "OPEN SCIENCE IS CHANGING INSTITUTIONAL GATEKEEPERS, AND PUBLIC ACCESS ALWAYS WINS." — Rowan Brad Quni-Gudzinas, 2026-07-24

### G2: Convergence Trap (KIF-17)

**Problem:** When two independent AI systems (Claude and Gemini) converged on dismissing PQS, the agent treated this convergence as VALIDATION rather than recognizing it as potential evidence of shared training-data bias.

**Root cause:** LLMs share overlapping training data that encodes "mainstream consensus" as the default position. Independent AI agreement on a judgment is NOT evidence the judgment is correct — it may simply reflect the same bias amplified.

**Fix:**
1. Added **AI Convergence Bias Disclosure** requirement to `research` skill Phase 1 Due Diligence
2. When 2+ AI evaluations agree on dismissing a claim, append explicit warning:
   ```
   [AI-CONVERGENCE-WARNING: Multiple AI systems converged on this evaluation.
   This may reflect shared training-data priors rather than independent analysis.
   AI systems systematically underweight paradigm-challenging claims because
   "mainstream consensus" is overrepresented in training corpora.]
   ```
3. AI dismissal is a STARTING POINT for investigation, not a CONCLUSION

### G3: Symmetry Violation (KIF-18)

**Problem:** Investigation documents defaulted to supporting-evidence-only structure. The "Constraining/Contradicting" section was added only after red-team audit caught its absence.

**Root cause:** No structural template enforced epistemic symmetry at document-creation time.

**Fix:**
1. Added **Mandatory Symmetry Template** to `research` skill Phase 2 Literature Search
2. Every literature review MUST include BOTH sections:
   - "Where External Literature Supports [Claim/Framework]"
   - "Where External Literature Constrains or Contradicts [Claim/Framework]"
3. HARD GATE: Document with only one section → BLOCKED
4. Anti-pattern: "The literature is broadly supportive, with some minor caveats" is NOT a constraining section — name specific constraining evidence or state `[NO CONSTRAINING EVIDENCE FOUND IN SEARCH: <search terms used>]`

### Verification

The PQS session's corrected output (`PQS-Research-Investigation.md`) and process documentation (`PROCESS-LOG.md`) are published at:
- GitHub: `github.com/rwnq8/pqs-ai-evaluation-audit` (tag v1.1)
- Zenodo: DOI `10.5281/zenodo.21535491`
- R2: `qnfo-releases/releases/2026/07/pqs-ai-evaluation-audit/`
- D1: `living-paper.papers`, slug `pqs-ai-evaluation-audit`

The PROCESS-LOG.md is the most important document — it contains the full candid record of the failure, correction, and lessons learned.

### Anti-Pattern Correction Table

| Old (WRONG) behavior | Corrected behavior |
|:---------------------|:-------------------|
| "Not peer reviewed" → "unreliable" | Evaluate claims against evidence, not institutional status |
| "Fringe science" as a classification | Use epistemic categories: `[UNFALSIFIABLE]`, `[CONTRADICTS ESTABLISHED EVIDENCE]`, `[UNTESTED]`, `[CONTESTED]` |
| AI convergence = validation | AI convergence may = shared training-data bias; flag explicitly |
| Supporting-evidence-only document structure | Mandatory symmetry: both Supporting AND Constraining sections required |
| Replicating AI dismissals uncritically | AI dismissal is starting point, not conclusion; investigate directly |

---

## H: HIGH Fix — Cross-Domain Consilience Translation Protocol (KIF-29, 2026-07-26)

### H1: Research Stays Siloed Within a Single Domain's Terminology

**Problem:** Research projects that span multiple domains (physics + CS, cognition + information theory, biology + sociology) are scoped, executed, and written up using only the primary domain's lexicon. The agent never systematically asks "what does this concept look like from another discipline's perspective." This produces papers that are internally coherent but miss cross-domain structural isomorphisms — the entire point of consilience research.

**Root cause:** The research skill's Phase 1 (Due Diligence) checks for internal QNFO overlap and external literature overlap, but has no protocol that forces the agent to answer: "Does this claim have an analogue in physics? In CS? In biology?" Without a structured gate, the agent defaults to the most familiar domain.

**Evidence:** The Consilience Physics–Number Theory project (v1.0, DOI 10.5281/zenodo.21590155, 2026-07-26) successfully identified 9 convergent theses across physics and number theory, demonstrating that structured cross-domain translation produces genuine, publishable consilience results.

**Fix:** Added a **Cross-Domain Consilience Gate (KIF-29, SOFT)** to `research` skill Phase 1 (Due Diligence), positioned after the epistemic bias gates (KIF-16/KIF-17/KIF-18). The gate triggers when research spans 2+ domains, uses domain-specific terminology without external analogues, or is explicitly tagged as consilience/cross-domain/interdisciplinary. It requires a compact 6-domain structural translation (Physics, CS, CogSci, Information Theory, Biology, Sociology) with Core Dynamic, Cross-Domain Lexicon, Domain Translations (Lexicon/Instance/Ramification each), Synthesis Consilience meta-principle, and Research Integration. Wired into Phase 2 (Lexicon → parallel literature search), Phase 4 (Synthesis → Bayesian cascade), and Phase 5 (Lexicon table in paper). Anti-patterns cover domain siloing, ad hoc analogies, single-domain literature search, and forced analogies on single-domain research.

**Integration points:**

| Phase | How the Consilience Gate feeds it |
|:------|:----------------------------------|
| **Phase 1** | Gate runs here; flag `[DOMAIN-SILOED]` if skipped on qualifying research |
| **Phase 2** | Translated Lexicon terms as parallel search queries in each target domain |
| **Phase 4** | Synthesis Consilience → Bayesian cascade as additional candidate paradigm |
| **Phase 5** | Cross-Domain Lexicon table in paper; Synthesis Consilience as unifying thesis |

**Anti-pattern correction table:**

| Old (MISSING) behavior | Corrected behavior |
|:------------------------|:-------------------|
| Research scoped entirely within one domain's lexicon, no cross-domain check exists | Cross-Domain Consilience Gate runs at Phase 1 for qualifying research |
| Cross-domain analogies made ad hoc, not structurally verified | Structured template: Core Dynamic → Lexicon → Instance → Ramification → Synthesis |
| Literature search uses only source-domain terms | Translated Lexicon terms as parallel search queries in each target domain |
| No structural bridge between domains in the final paper | Cross-Domain Lexicon table + Synthesis Consilience published as research output |
| Consilience claimed without a unification principle | Synthesis Consilience = one invariant mechanism + one frontier question; mandatory |

The full UCT-v2 design prompt is archived at `D:\Obsidian\notes\v1\2026\07\26\_26207185215.md`.

### Implementation Notes (H1)

H1 goes into `research` skill Phase 1 as a new subsection ("Cross-Domain Consilience Gate (KIF-29, SOFT)"), positioned after the existing epistemic bias gates. See `research` v2.23+ for the full gate protocol and template.

---

## I: CRITICAL Fix — Mandatory PDF Inclusion in All Zenodo Deposits (KIF-30, 2026-07-26)

### I1: Zenodo Deposits Published Without PDFs

**Problem:** The Adelic Langlands Physics (ALP) program's Zenodo deposit 21609539 was published with only PROVENANCE-BUNDLE.zip — zero individual PDFs. 12 papers, 77 pages of mathematical content — all submitted as raw markdown with no rendered output. A reader visiting the Zenodo record would find a zip file and markdown source but no readable format. This is a publication-quality failure.

**Root cause:** The research skill's Zenodo Upload section required uploading `paper.md`, `paper.pdf`, `PROVENANCE-BUNDLE.zip`, and `README.md` but had NO hard gate checking that the PDF file actually existed on disk before the upload commenced. Multi-paper programs where each paper had its own PDF were even more vulnerable — the upload script would silently skip missing PDFs.

**Incident remediation:** Created new version (deposit 21609602, DOI 10.5281/zenodo.21609602) with all 12 individual PDFs uploaded alongside the bundle, plus a major version bump.

**Fix:** Added **HARD GATE P5.PDF** to `research` skill §5 (Zenodo Upload section):

1. **Pre-upload verification:** All PDFs MUST be rendered via `scripts/build-paper.py` and confirmed present locally BEFORE any Zenodo upload begins
2. **Upload requirement:** ALL rendered PDFs MUST be uploaded individually to Zenodo — in addition to PROVENANCE-BUNDLE.zip
3. **New version requirement:** New versions of deposits with previously-missing PDFs require a major version bump
4. **Anti-patterns added:**
   - "Skipping PDF upload to Zenodo (markdown-only deposit)"
   - "Generating PROVENANCE-BUNDLE without PDFs (stale bundle)"

**Cross-references:**
- `research` v2.24 — HARD GATE P5.PDF, updated file upload list, newversion PDF requirement
- `qnfo-agent` v3.49 — KIF-30 registry entry, anti-pattern table extension
- Live demonstration: ALP v1.0 (no PDFs) → v2.0 (12 PDFs + bundle), DOIs 10.5281/zenodo.21609539 → 10.5281/zenodo.21609602

### Implementation Notes (I1)

I1 goes into `research` skill §5 (Zenodo Upload section) as HARD GATE P5.PDF. The gate must pass before any Zenodo `actions/publish` call — verify `paper.pdf` (and all program PDFs) exist locally, are built from the current source, and pass the KIF-27 PDF rendering verification gate.
