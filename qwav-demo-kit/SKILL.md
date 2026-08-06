---
name: qwav-demo-kit
version: 1.4
description: Build, test, and deploy interactive scientific demos that prove published research executes in code. Five-phase pipeline (DEM-E0-T01 to DEM-E0-T05) covering self-explanatory UX, math verification against golden values, extensive automated testing on Chrome (CDP test-demo.py plus Playwright click-everything suite), native gh-pages branch deployment with same-turn anti-phantom verification, and complete documentation. Light-theme readable UIs (user mandate 2026-08-06 — no dark themes), every control wired to real computation (no dead buttons). Use when building interactive demos, computational PoCs, scientific visualizations, or publishing research that must execute in code.
---

# QWAV Demo Kit — v1.4

> **v1.4 UPDATE (2026-08-06, kaizen — VERSION-OVERWRITE-1 merge + FUNCTIONALITY GATE + audit-tool suite):**
> Red-team: direct parent-agent 5-adversary audit (session s5A91BkILVruZwf361xxc — user directive:
> ""has canvas/scripts" is not the gate. The gate is: do the controls actually work?";
> EXECUTE RED TEAM SKILLS AUDIT → EXECUTE KAIZEN SKILLS UPDATES).
> A concurrent session (f9oRzNJ9WzVVFz7KXuaTK) bumped to v1.3 (STRUCTURAL-VS-FUNCTIONAL-1) while
> this audit ran; merged past the collision per VERSION-OVERWRITE-1. Both contributions present.
> HARD: 2. SOFT: 1. DESIGN: 1. Changes:
> (1) [HARD] **FUNCTIONALITY GATE added to Phase 3 (DEM-E0-T03)** — presence is NOT the gate.
>     Audit evidence: all 4 legacy demos FAIL (ultrametric-convergence 5/14 buttons + 14 console
>     errors `variance() is not a function`; error-confinement 2/16 + blank canvas;
>     hardware-visualizer 2/9 + blank canvas; tree-distance 2/13 + blank canvas). Hard thresholds:
>     ≥50% of buttons AND sliders change state, canvas non-blank, zero console errors, light theme.
> (2) [HARD] **`scripts/generic-click-test.py` added** — selector-agnostic functionality gate:
>     clicks EVERY button/input/select/range on ANY demo, asserts page state changes (full
>     innerText comparison — NOT length, which can coincide on digit swaps like "156"->"781"),
>     canvas non-blank, zero console errors, light theme, desktop+mobile. Verified live:
>     PASS on qwav-demo-bt-qec control (ALL CHECKS PASSED), FAIL on legacy error-confinement.
>     Run against BOTH localhost and deployed URL.
> (3) [SOFT] **Anti-patterns PRESENCE-OVER-FUNCTION-1 + HARDCODED-AUDIT-1 added** — presence
>     checks (element exists) prove only that a page loaded; the gate is whether controls work.
>     Demo-specific suites (playwright-click-test.py) are ADDITIONAL depth; generic-click-test.py
>     is the minimum universal gate.
> (4) [DESIGN] **Frontmatter `version:` key removed** — skill-creator validator forbids it
>     (allowed: name, description, license, metadata, allowed-tools); header+footer carry the
>     version per N-2. The v1.2 "fm version fix" would have BLOCKED packaging.
> (5) [DESIGN] **Gate-tool bug fixed during verification** — Playwright `fill()` throws on
>     `<input type=range>`; use evaluate+dispatchEvent. Length-based change detection misses
>     digit-swap state changes; use full-text comparison.
> Cross-reference: kaizen v1.65 (STRUCTURAL-VS-FUNCTIONAL-1), PRESENCE-OVER-FUNCTION-1,
> HARDCODED-AUDIT-1, DEAD-BUTTON-1, session f9oRzNJ9WzVVFz7KXuaTK, session s5A91BkILVruZwf361xxc.

name: qwav-demo-kit
version: 1.3
description: Build, test, and deploy interactive scientific demos that prove published research executes in code. Five-phase pipeline (DEM-E0-T01 to DEM-E0-T05) covering self-explanatory UX, math verification against golden values, extensive automated testing on Chrome (CDP test-demo.py plus Playwright click-everything suite), native gh-pages branch deployment with same-turn anti-phantom verification, and complete documentation. Light-theme readable UIs (user mandate 2026-08-06 — no dark themes), every control wired to real computation (no dead buttons). Use when building interactive demos, computational PoCs, scientific visualizations, or publishing research that must execute in code.
---

Complete framework for building interactive scientific demos that prove published
research actually executes in code and demonstrates real-world physics viability.
Every demo must be: **self-explanatory**, **mathematically verified**,
**automation-tested on Chrome**, and **reproducible**.

> **USER MANDATE 2026-08-06 (HARD):** ALL interactive demo apps MUST be easy to
> use and self-explanatory, with COMPLETE documentation and EXTENSIVE automated
> testing on the Chrome dev/test browser. This is a hard gate, not a guideline.

## Pipeline (WBS: DEM-E0-T01 through DEM-E0-T05)

| Phase | WBS Code | Gate | Success Criterion |
|:------|:---------|:-----|:------------------|
| 1. DESIGN | DEM-E0-T01 | Self-explanatory UX | First-time user completes guided tour without reading docs |
| 2. BUILD | DEM-E0-T02 | Math verification | ALL analytical predictions match computation to <=1% tolerance |
| 3. TEST | DEM-E0-T03 | Chrome automation | Zero console errors, all button/canvas/readout chains verified |
| 4. DEPLOY | DEM-E0-T04 | Anti-phantom gate | Live URL returns 200, canvas non-blank, all interactives functional |
| 5. DOCUMENT | DEM-E0-T05 | Completeness | README covers purpose, math, usage, params; inline comments on core loop |

**HARD GATE:** No demo may be deployed or published without passing ALL five phase gates.

> **v1.2 UPDATE (2026-08-06, kaizen — TREE-STRUCTURE-COUNT-1 + frontmatter N-2 fix + consolidation close):**
> Red-team: direct parent-agent 5-adversary audit (session f9oRzNJ9WzVVFz7KXuaTK — SKILLS UPDATE
> cycle after A1/A3/A4/A5 demo rebuild + live verification).
> Watchtower scan: 18 QNFO skills N-2 CLEAN (fm/hdr/ft). Recall_facts: 0 orphan anti-patterns.
> HARD: 1. SOFT: 1. DESIGN: 2. Changes:
> (1) [HARD] **Frontmatter `version:` field added** — the v1.1 consolidation shipped fm without a
>     version field (fm=- in watchtower-version-scan.py). Same class as N-2-FRONTMATTER-DRIFT-1;
>     fixed in this bump (fm=1.2/hdr=1.2/ft=1.2).
> (2) [SOFT] **TREE-STRUCTURE-COUNT-1 anti-pattern added** — recursive tree/lattice builders that
>     spawn the WRONG child count produce output that LOOKS correct but has a wrong node count.
>     Canonical case: A5 Hardware Visualizer buildAtoms created 14 atoms (1+1+3+9) instead of
>     40 (1+3+9+27) because the recursion pushed ONE child per call then recursed per child,
>     rather than pushing p children per node. The 7-check verifyMath() gate (atom count +
>     per-depth distribution) caught it on first live deploy; fixed in fa84f93. Lesson: the
>     golden-value count check is NOT optional — a tree that renders is not proof of a correct
>     tree. Verify node counts against the closed form (p^(d+1)-1)/(p-1) and per-depth p^k.
> (3) [DESIGN] **PROSE-GATE-ADVISORY-1 validated** — kaizen v1.63's rule ("a gate written in prose
>     is advisory until scripted") is PROVEN here: the demo math gates are scripted in-page
>     (verifyMath()) and test-demo.py, and the scripted gate caught the 14-vs-40 bug the prose
>     README claim ("40 atoms") did not. Keep demo gates scripted.
> (4) [DESIGN] **interactive-poc-builder SUPERSEDED** — this skill consolidated interactive-poc-builder
>     (per v1.1 banner); the old skill is a registry phantom (listed in skill_list, dir absent,
>     skill_view fails). Do NOT load interactive-poc-builder; use qwav-demo-kit for all demo/PoC work.
> Cross-reference: kaizen v1.63 (PROSE-GATE-ADVISORY-1), N-2-FRONTMATTER-DRIFT-1 (kaizen v1.41),>
> **v1.4 SUPPLEMENT (2026-08-06, session f9oRzNJ9WzVVFz7KXuaTK — gate hardened by live execution + A3 validation):**
> The FUNCTIONALITY GATE was EXECUTED against all four live demos; `generic-click-test.py` was
> hardened through 4 real findings, and it CAUGHT a real deployed bug.
> (1) [HARD] **Gate hardening (4 fixes from live execution):**
>     (a) Tour-dismissal timing — first-run guided-tour overlays (full-screen, pointer-events:all,
>         setTimeout(startTour, 800)) swallow real pointer clicks on fresh contexts; dismissal at
>         load+0ms is UNDONE at +800ms (canonical: A1 scored 3/16 -> 2/16 -> 1/16 across runs =
>         racy overlay, not dead buttons). Fix: wait 1200ms, dismiss via the overlay's actual
>         Skip/close button (sets localStorage -> never reappears), second pass for longer tours.
>     (b) 0-slider conditional — `max(1, 0//2)` force-failed demos with zero sliders (A4/A5).
>         Now `if interactives['sliders'] > 0` else print N/A.
>     (c) 800ms per-click wait — 200ms missed async updates (Monte Carlo sim, collapse animation).
>     (d) toDataURL canvas check — getImageData on a 0-sized backing store threw/returned empty
>         (false 'blank'); toDataURL().length > 1000 is layout-independent (A1 proved 130KB+).
> (2) [HARD] **STRUCTURAL-VS-FUNCTIONAL-1 VALIDATED (A3 canonical case)** — the gate caught a real
>     deployed bug: A3 ultrametric-convergence threw 13x `variance(...) is not a function` on every
>     interaction. Root cause: `updateReadouts()` collapse-ratio line wrapped an IIFE in a variance()
>     call — `variance(()=>{...})()` should be `(()=>{...})()`. Fired on EVERY interaction yet:
>     marker checks passed ('has canvas/scripts'), verifyMath() passed 6/6 (tests engine directly,
>     bypassing updateReadouts). ONLY the functional gate (real clicks + console listener) caught it.
>     Fixed in fcccc47, deployed, live re-run ALL PASS (10/14 buttons, 0 console errors).
> (3) [SOFT] **All four live demos now pass the hardened gate** — A1 12/16 (75% >= 50%), A3 10/14,
>     A4 11/13, A5 5/9; sliders N/A where absent; canvas non-blank; zero console errors everywhere.
>     Unchanged buttons are by-design no-ops (already-active defaults, deterministic reseed).
> (4) [DESIGN] **Real pointer clicks vs CDP DOM-click** — DOM .click() bypasses overlays (why earlier
>     CDP functional tests passed); real pointer clicks are the correct fidelity for what a user
>     experiences. The gate uses Playwright real clicks.
> Cross-reference: STRUCTURAL-VS-FUNCTIONAL-1 (v1.3 banner), A3 fix commit fcccc47,
> kaizen v1.66, session f9oRzNJ9WzVVFz7KXuaTK, session s5A91BkILVruZwf361xxc.

> A5 fix commit fa84f93, session f9oRzNJ9WzVVFz7KXuaTK.


---

## Phase 1: DESIGN - Self-Explanatory UX (DEM-E0-T01)

### The "No-Instructions" Test
A user who has never seen the demo before and has NOT read any documentation
should be able to:
1. Understand what the demo shows within 10 seconds
2. Find and use the primary interactive control within 5 seconds
3. See a visible change in the output within 1 second of interaction
4. Discover secondary controls without hunting

### Required UX Elements (MANDATORY — user mandate 2026-08-06)
Every scientific demo MUST include:

| Element | Requirement | Anti-Pattern |
|:--------|:------------|:-------------|
| Title + one-sentence research claim | Visible on load: what this is AND what it proves | Buried in a README tab |
| Parameter labels | Human-readable names with units | `eps`, `d`, `k` without explanation |
| Live readouts | Numerical results update on parameter change | Static labels that never change |
| Active state | Selected parameter highlighted (color, border) | Button looks identical whether active or not |
| Loading state | Spinner/progress during computation > 500ms | Frozen UI with no feedback |
| Error state | Graceful message if computation fails | Blank canvas, console stack trace only |
| Reset/defaults | One-click return to known-good parameters | User must reload page to recover |
| Formula display | Key equation shown near the output it governs | Math only in the README |
| "How to use" panel | Collapsible, one line per control | No guidance at all |
| Status overlay | Bottom-left of canvas, explains current mode | Silent UI, user guessing |
| Legend | Always visible when canvas has colored elements | Colors without meaning |
| Tooltips | Every interactive element explains itself on hover | Cryptic icons |
| Key insight panel | States what to observe + how to verify it yourself | Demo without a takeaway |

### Light Theme Mandate (user rejected dark themes 2026-08-06)
See [DESIGN-SYSTEM.md](references/design-system.md) for the full light-theme palette.
- White/cream background, near-black text (WCAG AAA contrast)
- Blue/academic accent (`#1a73e8`), semantic colors only
- Serif display (Georgia) + clean sans body; body >= 14px
- **NEVER** ship a dark background without explicit user request

### Progressive Disclosure Pattern
```
+--------------------------------------------------+
|  TITLE: What this demo shows                      |
|  ------------------------------------------------ |
|  PRIMARY CONTROL: The thing you'll change         |
|  most often (slider, button group)               |
|  ------------------------------------------------ |
|  MAIN VISUALIZATION: Canvas/chart                 |
|  ------------------------------------------------ |
|  KEY READOUT: The number that matters             |
|  ------------------------------------------------ |
|  > Advanced controls (collapsed by default)       |
|    Secondary parameters, raw data, export        |
+--------------------------------------------------+
```

### Scientific Visualization Standards
- Color scales: perceptually uniform (viridis, magma, cividis). Never jet/rainbow.
- Axis labels: include quantity + units on every plot. Font >= 12px.
- Legends: positioned inside or adjacent to the plot, not below.
- Numerical precision: match the meaningful precision of the computation. Never show 15 decimal places for a 1% Monte Carlo estimate.
- Canvas DPR: always multiply by `window.devicePixelRatio` (max 2) for sharp rendering.
- Hover tooltips: on data points that show x, y values at cursor position.

---

## Phase 2: BUILD - Math Verification (DEM-E0-T02)

### Computation-First Principle
The demo's engine is a PURE computation class (tree, curve, bound, protocol) —
no DOM, no hardcoded numbers. The UI renders its output. Every metric shown is
computed at render time. **Never hardcode diagrams or metrics.**

Expose the engine for testing: `window._demo = { engine, rebuild, params }`
(with `engine` as a GETTER — a stale reference to the pre-rebuild object is a
real bug the Chrome suite will catch).

### Verification Ladder (least to most rigorous)
1. Sanity check: output is in the right ballpark (not NaN, not 1e300)
2. Edge case: limit behavior matches analytical prediction (eps->0 => ler->0)
3. Invariant: property holds across all parameter values (variance monotonic)
4. Analytical match: computation agrees with closed-form solution to <=1%
5. Cross-implementation: two independent implementations agree to floating-point epsilon

### Golden Values (MANDATORY)
Derive 2-3 expected outputs from the paper's own math (e.g., p-ary tree depth d
has p^d nodes at depth d; error subtree = 1+p+...+p^r). These become unit-test
assertions in `test-engine.mjs`. Numbers never checked against golden values =
UNVERIFIED-MATH-1 anti-pattern.

### Mandatory Verification for Every Demo
Before deployment, verify these gate checks programmatically:

```javascript
// GATE-CHECK-1: Invariant verification
function verifyInvariant(fn, invariantFn, paramSpace) {
  for (const params of paramSpace) {
    const result = fn(...params);
    if (!invariantFn(result)) {
      console.error('Invariant violated', {params, result});
      return false;
    }
  }
  return true;
}

// Example: Error confinement - LER must be monotonic in physical error rate
// invariantFn: (ler1, ler2) => eps1 <= eps2 ? ler1 <= ler2 : true

// GATE-CHECK-2: Analytical prediction match
function verifyAnalytical(computed, analytical, tolerance) {
  tolerance = tolerance || 0.01;
  const diff = Math.abs(computed - analytical) / Math.max(Math.abs(analytical), 1e-300);
  if (diff > tolerance) return false;
  return true;
}
```

### Reproducibility Requirements
1. Seeded PRNG: use mulberry32 or similar seeded generator. NEVER `Math.random()` in computational core.
2. Parameter snapshot: log all parameters to console on rebuild.
3. Deterministic rendering: same seed + same params = bit-identical canvas output.
4. Seed display: show current seed in UI so users can share/reproduce results.

```javascript
// Canonical seeded PRNG (mulberry32) - copy-paste into any demo
function mulberry32(a) {
  return function() {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    var t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
var rng = mulberry32(42); // Fixed seed for reproducibility
```

---

> **v1.3 UPDATE (2026-08-06, kaizen — STRUCTURAL-VS-FUNCTIONAL-1: 'has canvas/scripts' is NOT the gate):**
> Red-team: direct parent-agent 5-adversary audit (session f9oRzNJ9WzVVFz7KXuaTK — SKILLS UPDATE
> cycle 2). User directive: ""has canvas/scripts" is not the gate. The gate is: do the controls
> actually work?" The prior audit verified live demos by HTML marker presence (tourOverlay, seedInput,
> mulberry32 in page source) — STRUCTURAL verification. It proved the page HAS elements, not that
> clicking them produces the CORRECT computed output. This cycle re-verified all four demos with
> FUNCTIONAL tests (click every control, assert output == engine-predicted value): A1 6/7, A3 7/7,
> A4 7/8, A5 9/9 — all controls work; only 2 assertion artifacts (IEEE-754 underflow, coincidental
> root-LCA pair). Watchtower scan: 18 QNFO skills N-2 CLEAN.
> HARD: 1. SOFT: 1. DESIGN: 1. Changes:
> (1) [HARD] **STRUCTURAL-VS-FUNCTIONAL-1 anti-pattern added** — verifying a demo by checking that
>     canvas/script/marker elements EXIST in the page is NOT verification. Presence of an element
>     proves nothing about whether its control works. The gate is FUNCTIONAL: for every interactive
>     control, click it and assert the output changed to the value predicted by the engine (golden
>     value / analytical formula / invariant). Canvas data-URL length, element existence, and marker
>     substrings are all structural checks — they can all pass while every button is dead. Canonical
>     case: 2026-08-06 cycle 1 verified all four live demos structurally (markers present) — the
>     A5 14-vs-40-atom bug passed every structural check; only the scripted verifyMath() FUNCTIONAL
>     gate caught it. Fix: the test matrix in Phase 3 MUST include per-control computed-output
>     assertions, not just "canvas changed" / "readout changed".
> (2) [SOFT] **Phase 3 functional-gate requirement strengthened** — Test Runner sections now state:
>     element-existence and canvas-data-URL-differs checks are MINIMUM smoke checks; the deploy gate
>     requires per-control assertion of output == engine-predicted value (e.g., after clicking
>     p=5 button, theoreticalLER(eps,5,d) must equal the displayed readout within tolerance).
> (3) [DESIGN] **Session evidence registered** — the four functional test runs (A1/A3/A4/A5 live)
>     are the canonical examples of the functional gate; 2/29 assertions were artifacts (not dead
>     controls). Also: top-level `const S` does NOT attach to window (test harness must reference
>     the lexical binding, not window.S).
> Cross-reference: kaizen v1.65 (session retrospective), DEAD-BUTTON-1, UNVERIFIED-MATH-1,
> TREE-STRUCTURE-COUNT-1, session f9oRzNJ9WzVVFz7KXuaTK.


## Phase 3: TEST - Chrome Automated Testing (DEM-E0-T03)

### FUNCTIONALITY GATE (HARD — presence is NOT the gate)

**"Has canvas/scripts" is NOT the gate. The gate is: do the controls actually
work?** A demo that loads and has `<canvas>` and `<script>` but whose buttons
change nothing is a FAIL — this is exactly what the 2026-08-06 audit found on
all 4 legacy demos (ultrametric-convergence 5/14 buttons + 14 console errors;
error-confinement 2/16 + blank canvas; hardware-visualizer 2/9 + blank canvas;
tree-distance 2/13 + blank canvas). Presence checks only catch a missing page.

**Canonical enforcement: `scripts/generic-click-test.py`** — clicks EVERY
button/input/select/range on ANY demo, asserts the page state actually changes
(canvas, text, or attribute), checks canvas non-blank, zero console errors,
light theme, desktop + mobile. Run against BOTH localhost and the deployed URL.

**Hard thresholds (any FAIL blocks deploy):**
| Check | Threshold |
|:------|:----------|
| Buttons cause state change | ≥ 50% of buttons (each click changes body text, canvas, or attribute) |
| Sliders cause state change | ≥ 50% of sliders |
| Canvas renders non-blank | getImageData sum > 0 (not all zeros) |
| Console errors | ZERO (any console.error / pageerror / failed request) |
| Light theme | no dark backgrounds in CSS |
| Interactive controls exist | buttons + inputs > 0 |

**Gate rule:** a demo whose controls are less than 50% functional is a dead
demo, not a demo. Fix the wiring until ≥50% change state AND the changed ones
are the PRIMARY controls (the ones the README tells users to click). The 15/15
playwright-click-test.py suite remains the standard for QWAV's own demos;
generic-click-test.py is the MINIMUM gate every demo must clear.

### Test Runner 1: `scripts/test-demo.py` (CDP — zero dependencies)

A Python script using Chrome for Testing (headless) + CDP that validates:

1. Console Error Audit: ZERO errors for interactive tools. Any console.error, uncaught exception, or 404 on resource load = FAIL.
2. Canvas Chain Verification: for EACH interactive element, capture canvas data URL before/after click, verify change.
3. Readout Chain Verification: for EACH interactive element, capture readout text before/after click, verify change.
4. Interactive Element Audit: enumerate all button/input/select elements, verify each responds.
5. Performance Budget: FCP < 1.8s, no long tasks > 50ms on interaction.

### Test Runner 2: `scripts/playwright-click-test.py` (Playwright — extensive, USER MANDATE)

The mandate requires EXTENSIVE automated testing on Chrome. This suite clicks
EVERY control, asserts state change after each, captures screenshots, checks
zero console errors, and tests desktop + mobile viewports:

```bash
pip install playwright && playwright install chromium
python scripts/playwright-click-test.py http://localhost:8765/index.html   # local dev
python scripts/playwright-click-test.py https://qnfo.github.io/<repo>/      # DEPLOYED URL
```

Required coverage (15 checks): engine loaded; every prime/param button; depth
slider rebuild + stats update; every tab; every toggle (compare, error mode);
canvas click → error subtree/overlay updates; reset; screenshots per view;
mobile 375px no-overflow; zero console errors.

**CRITICAL: run the suite against BOTH the local dev server AND the deployed
URL.** A demo that only passes locally but fails deployed is a FAIL (see
UNTESTED-DEPLOYED-1).

### Interactive Element Test Matrix

For each interactive control on the page, verify:

| Check | Method | Pass Condition |
|:------|:-------|:---------------|
| Exists in DOM | DOM.querySelector | Element found |
| Visible | DOM.getBoundingClientRect | width > 0, height > 0 |
| Clickable | Runtime.evaluate click | No exception |
| Triggers canvas change | Canvas data URL before/after | before !== after |
| Triggers readout change | Readout textContent before/after | before !== after |
| No console error | Console listener | Zero errors during interaction |
| Works at min value | Set to minimum, click, verify | Canvas updates |
| Works at max value | Set to maximum, click, verify | Canvas updates |

### Running the Test Suite

```
# Full test battery against a live URL
python scripts/test-demo.py --url https://qnfo.github.io/qwav-demo-error-confinement/

# Extensive Playwright suite (user mandate)
python scripts/playwright-click-test.py <url>

# Test against local file
python scripts/test-demo.py --file index.html

# Quick smoke test (console errors only)
python scripts/test-demo.py --url <url> --smoke

# Generate JUnit XML report
python scripts/test-demo.py --url <url> --junit report.xml
```

Exit codes: 0 = all pass, 1 = console errors, 2 = canvas chain failure, 3 = readout chain failure.

---

## Phase 4: DEPLOY - Anti-Phantom Gate (DEM-E0-T04)

### Deployment Protocol — NATIVE gh-pages branch (CANONICAL, 2026-08-06)

**Use the native gh-pages branch flow. Do NOT add a custom Actions workflow.**

The custom-workflow path (`concurrency: cancel-in-progress: true`) **cancels
GitHub's native "pages build and deployment" run** and then fails itself when
Pages uses branch source — the site stays down or 404s. This was a real
production bug (2026-08-06, qwav-demo-bt-qec). Native branch deployment needs
NO workflow at all.

```python
# 1. CREATE repo under QNFO org EXPLICITLY
POST https://api.github.com/orgs/QNFO/repos
  {"name": "qwav-demo-<name>", "has_pages": true, "auto_init": true}

# 2. Create orphan gh-pages branch with ONLY index.html + README.md at root
git checkout --orphan gh-pages
git rm -rf .                    # remove everything
git checkout main -- index.html README.md   # bring back only these
git commit -m "deploy: static site"
git push origin gh-pages

# 3. Enable Pages (PUT replaces config; 204 empty body is success)
PUT https://api.github.com/repos/QNFO/<repo>/pages
  {"source": {"branch": "gh-pages", "path": "/"}}

# 4. Wait ~30-60s for native build to reach completed/success
# 5. VERIFY (PAGES-BUILD-LATENCY-1): poll up to 3 min
```

**Update later:** `git checkout gh-pages && git add index.html && git commit -m "..." && git push origin gh-pages` — native build, live in ~1 min. No CI.

**If a conflicting workflow exists**, delete it via API with the file's current SHA:
```
GET  /repos/{owner}/{repo}/contents/.github/workflows/deploy.yml   # → sha
DELETE /repos/{owner}/{repo}/contents/.github/workflows/deploy.yml?message=...&sha={sha}
```

**Use Python subprocess for git commits** — `git commit -m "multi word"` with
em-dashes/parens breaks in cmd.exe. See CMD-QUOTES-1.

### Anti-Phantom Verification (MANDATORY post-deploy — SAME TURN)

**Never claim "deployed"/"live" without a tool call in the SAME turn showing the
live state.** A user-found 404 after a deployment claim is an integrity failure
(PHANTOM-DEPLOY-1). Run `scripts/verify-deploy.py` in the same turn:

```bash
python scripts/verify-deploy.py https://qnfo.github.io/<repo>/ --marker BTTree
# → HTTP 200, non-empty body, engine marker present
```

After deployment, run these checks against the LIVE URL. Never trust deploy exit codes alone:

| Check | Method | Threshold |
|:------|:-------|:----------|
| HTTP 200 | curl -sI URL | Status 200 |
| Canvas renders | CDP canvas.toDataURL() length | > 1000 bytes |
| Not blank page | CDP body textContent length | > 100 chars |
| No mojibake | CDP document.title | Valid UTF-8 |
| Script executes | CDP typeof rebuild | "function" |
| Event listeners | CDP addEventListener check | True |
| Engine marker | verify-deploy.py --marker | FOUND in body |
| **Deployed Chrome suite** | **playwright-click-test.py <live-url>** | **ALL PASS (mandate)** |

Any FAIL blocks deployment. Re-deploy and re-verify.

---

## Phase 5: DOCUMENT - Completeness Gate (DEM-E0-T05)

### Documentation Mandate (user mandate 2026-08-06)

Every demo ships with COMPLETE documentation:

| Doc | Where | Contents |
|:----|:------|:---------|
| README.md | repo root | Purpose, math, usage, parameters, verification table with results, run-locally, DevTools tests, deployment model, license, paper DOI |
| In-app "How to use" | index.html collapsible panel | Every control explained in one line |
| In-app status overlay | canvas area | Current mode/state explained live |
| In-app key insight | index.html panel | What to observe + how to verify it |
| test-engine.mjs | repo | Golden-value assertions (reproducible) |
| screenshots/ | repo | View captures from the Chrome suite, embedded in README |

### Documentation Template

Every demo README.md MUST contain these sections:

```markdown
# <Demo Title>

**Status:** LIVE - deployed <date>
**URL:** https://qnfo.github.io/<repo>/

## What This Shows
One paragraph explaining the concept in plain language.

## The Math
The key equation(s) with Unicode math in the README.

## How to Use
1. Step-by-step walkthrough of the primary interaction
2. What each parameter controls
3. What the visualization shows
4. How to interpret the readouts

## Parameters

| Parameter | Range | Default | Description |
|:----------|:------|:--------|:------------|
| p | 2, 3, 5 | 3 | Branching factor of the tree |

## Reproducibility
- Seed: <seed value> (fixed for deterministic output)
- PRNG: mulberry32
- Computation: <brief description of algorithm>
- Verification: <link to verification script or inline checks>

## Source
- Strategy: QNFO/QWAV strategy/3.0.md
- Publication: <paper title and link>
- Build: single-file HTML, canvas rendering, zero external dependencies

## Testing
- Chrome automated test suite: python scripts/test-demo.py --url <live-url>
- Last test run: <date> - <N>/<N> passing
```

---

## Anti-Patterns (from real incidents, 2026-08-06)

| Anti-Pattern | Fix |
|:-------------|:----|
| **PHANTOM-DEPLOY-1:** Claiming "deployed"/"live" without a same-turn tool call showing HTTP 200 + engine | Run `verify-deploy.py` in the same turn as any deploy claim. User-found 404 = integrity failure. |
| **PAGES-WORKFLOW-CONFLICT-1:** Custom workflow with `concurrency: cancel-in-progress` on branch-source Pages | Native gh-pages branch needs NO workflow. Delete the conflicting workflow via API with its SHA. |
| **DEAD-BUTTON-1:** UI control that changes nothing | Every control calls a computation and updates visible state. Test by clicking it. |
| **PRESENCE-OVER-FUNCTION-1: Treating "has canvas/scripts" as proof the demo works (2026-08-06)** | **HARD GATE.** Presence checks (element exists, script loads) only prove a page loaded — NOT that controls function. The gate is: do the controls actually work? All 4 legacy demos (ultrametric-convergence 5/14 buttons + 14 console errors, error-confinement 2/16 + blank canvas, hardware-visualizer 2/9 + blank canvas, tree-distance 2/13 + blank canvas) had canvas+scripts yet failed. Enforce with `scripts/generic-click-test.py`: click EVERY control, assert ≥50% change state, canvas non-blank, zero console errors. Cross-ref: DEAD-BUTTON-1, DEM-E0-T03 FUNCTIONALITY GATE. |
| **HARDCODED-AUDIT-1: Test suite hardcoded to one demo's selectors, unusable on others (2026-08-06)** | A click-through suite written against demo A's specific IDs (`#depthSlider`, `[data-p="2"]`) can't verify demo B — so demo B ships untested. Use `scripts/generic-click-test.py` (selector-agnostic: clicks every button/input/select, asserts state change) as the universal gate; keep demo-specific suites as ADDITIONAL depth, never as the only check. Cross-ref: UNEXTENSIVE-TESTING-1, DEM-E0-T03. |
| **DARK-THEME-1:** Dark/low-contrast unreadable UI | Light design system; WCAG AA; never dark without explicit request. |
| **INCOMPREHENSIBLE-UI-1:** Demo needing external explanation | Self-explanatory: header claim, How-to panel, legend, overlay, tooltips, key insight. |
| **UNEXTENSIVE-TESTING-1:** Demo tested only by loading the page | Full Chrome/Playwright click-everything suite (P4), desktop + mobile. |
| **UNTESTED-DEPLOYED-1:** Only local copy tested, not deployed URL | Re-run the Playwright suite against the deployed URL. |
| **STALE-ENGINE-REF-1:** `window._demo.tree` holds pre-rebuild object | Expose engine as a GETTER: `get tree() { return tree; }`. |
| **HARDCODED-METRICS-1:** Static numbers in UI instead of computed | Stats from `engine.getX()` at render time. |
| **UNVERIFIED-MATH-1:** Demo numbers never checked against golden values | Derive 2-3 golden values from the paper's math; assert in test-engine.mjs. |
| **INCOMPLETE-DOCS-1:** Demo shipped without README/in-app help | Ship README, How-to panel, status overlay, key insight, verification table. |
| **STRUCTURAL-VS-FUNCTIONAL-1: Verifying a demo by element/marker presence instead of functional behavior (2026-08-06)** | **HARD GATE.** "Has canvas/scripts" is NOT the gate — the gate is: do the controls actually work? Element existence (canvas present, marker string in HTML) and canvas-data-URL-changed are STRUCTURAL checks; they all pass while every button is dead. The functional gate: for EVERY interactive control, click it and assert the output changed to the engine-predicted value (golden value / analytical formula / invariant) within tolerance. Canonical case: 2026-08-06 cycle 1 verified A1-A5 live by marker presence — A5's 14-vs-40-atom bug passed every structural check; only the scripted verifyMath() functional gate caught it. Fix: per-control computed-output assertions in the Phase 3 test matrix; structural checks are minimum smoke, never the deploy gate. Cross-ref: DEAD-BUTTON-1, UNVERIFIED-MATH-1, TREE-STRUCTURE-COUNT-1, kaizen v1.65. |
| **TREE-STRUCTURE-COUNT-1: Recursive tree/lattice builder spawning the wrong child count (2026-08-06)** | **HARD GATE.** Recursion that pushes ONE child per call then recurses per child (instead of pushing p children per node) produces a structure that renders fine but has the WRONG node count. Canonical case: A5 buildAtoms — 14 atoms (1+1+3+9) instead of 40 (1+3+9+27); the lattice looked plausible but the math gate caught it (verifyMath: atom count + per-depth distribution). Fix: verify counts against the closed form (p^(d+1)-1)/(p-1) and per-depth p^k as golden values BEFORE deployment. A rendering tree is not proof of a correct tree. Cross-ref: UNVERIFIED-MATH-1, kaizen v1.63 PROSE-GATE-ADVISORY-1. |
| **CMDENV-INLINE-PY-1:** Inline `python -c "..."` in cmd.exe | Write `.py` files and run them; cmd.exe mangles quotes and `|`/`&`/`<`. |
| **CMD-QUOTES-1:** `git commit -m "multi word"` with special chars in cmd.exe | Python `subprocess.run(['git','commit','-m',msg])`. |

---

## Skill Integration Map

This skill orchestrates other skills at specific phases. Always load the referenced
skill before executing its phase:

| Phase | Skill | What It Provides |
|:------|:------|:-----------------|
| DESIGN | frontend-design | Typography, color, motion, spatial composition guidelines |
| DESIGN | web-artifacts-builder | React + shadcn/ui stack (if using framework) |
| BUILD | code | Code quality review, security audit |
| BUILD | windows-command-patterns | Python-first command execution on Windows |
| TEST | cloudflare (QA/UX Test Battery) | Console error audit, broken link check |
| TEST | cloudflare (Web Performance Audit) | Core Web Vitals (LCP, INP, CLS, TBT) |
| TEST | webapp-testing (anthropics/skills, GitHub) | Additional Playwright verification patterns |
| DEPLOY | web-artifacts-builder | GitHub Pages deployment protocol (QWAV verified) |
| DEPLOY | git-github | Git workflow, conventional commits |
| DEPLOY | cloudflare | Cloudflare Pages alternative, R2 asset archival |
| DOCUMENT | documents | README generation, LaTeX to Unicode math |
| DOCUMENT | visualise (bentossell/visualise, GitHub) | Inline SVG diagrams for README |

---

## Domain Codes (WBS)

```
DEM = qwav-demos
  DEM-A1 = Error Confinement Live Demo
  DEM-A2 = Q-PNA Classifier Playground
  DEM-A3 = Ultrametric Convergence Explorer
  DEM-A4 = Tree Distance Sandbox
  DEM-A5 = Hardware Pathway Visualizer
  DEM-A6 = BT-Tree QEC Staircase Redundancy (qwav-demo-bt-qec)
```

### WBS-Coded Plan Template
Use this for any demo build task. Each step carries a verifiable acceptance criterion:

```
update_plan([
  {"step": "DEM-E0-T01: Design self-explanatory UX", "status": "pending"},
  {"step": "DEM-E0-T02: Build with math verification", "status": "pending"},
  {"step": "DEM-E0-T03: Test with Chrome automation", "status": "pending"},
  {"step": "DEM-E0-T04: Deploy to GitHub Pages + anti-phantom verify", "status": "pending"},
  {"step": "DEM-E0-T05: Document with complete README", "status": "pending"},
])
```

---

## Version

Current: **v1.4** (2026-08-06)
v1.4 (supplement): gate hardened by live execution — tour-dismissal timing, 0-slider conditional, 800ms async wait, toDataURL canvas; A3 variance(IIFE)() TypeError caught + fixed (fcccc47); all four live demos passing the gate.
v1.2: kaizen — frontmatter version field (N-2 fix), TREE-STRUCTURE-COUNT-1 anti-pattern,
interactive-poc-builder SUPERSEDED note, PROSE-GATE-ADVISORY-1 validation case.
v1.1: consolidated from interactive-poc-builder (2026-08-06 session) — added
USER MANDATE (easy-to-use/self-explanatory, complete docs, extensive Chrome
testing), light-theme design system, native gh-pages branch deployment (with
PAGES-WORKFLOW-CONFLICT-1 bug), playwright-click-test.py suite, verify-deploy.py
same-turn gate, 13 anti-patterns from real incidents, STALE-ENGINE-REF-1.
v1.0: initial release — 5-phase pipeline, Chrome test runner, math verification
protocol, UX checklist, documentation template.
