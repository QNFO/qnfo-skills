# Self-Explanatory UX Checklist for Scientific Demos

Use this checklist during the DESIGN phase (DEM-E0-T01). Every item must pass
for the demo to clear the Self-Explanatory UX Gate.

## Visual Hierarchy (First Impression: 0-5 seconds)

- [ ] **Title visible on load** — user knows what this is without scrolling
- [ ] **One-liner sub-title** — why this matters (max 12 words)
- [ ] **Primary visualization is above the fold** — no scrolling needed
- [ ] **No walls of text** — explanations are 1-2 sentence labels, not paragraphs
- [ ] **Visual weight goes to the data** — controls are smaller/dimmer than the output

## Interactive Controls (First Interaction: 5-15 seconds)

- [ ] **Primary control is visually obvious** — largest, brightest, or positionally prominent
- [ ] **Active state is unmistakable** — selected parameter has distinct color/border/glow
- [ ] **All controls have labels** — never rely on data attributes or developer notation
- [ ] **Labels include units** — "Physical Error Rate (epsilon)" not just "eps"
- [ ] **Hover state exists** — cursor changes, tooltip appears, button highlights
- [ ] **Click feedback is immediate** — button depresses, color shifts within 50ms
- [ ] **Single click per action** — no double-click or long-press required
- [ ] **Undo/reset is available** — one click returns to known-good defaults

## Visual Feedback (During/After Interaction: 0.5-2 seconds)

- [ ] **Canvas updates within 500ms** of parameter change
- [ ] **Readout text updates within 500ms** of parameter change
- [ ] **Loading indicator appears** for computation taking > 500ms
- [ ] **No flash of blank canvas** during re-render (use offscreen canvas or double-buffer)
- [ ] **Transitions are animated** — parameter changes cause smooth interpolation, not jumps
- [ ] **Hover tooltips on data points** — show x, y values at cursor position

## Readout & Data Display

- [ ] **Key readout is prominent** — the most important number is visually dominant
- [ ] **Readout precision matches computation** — Monte Carlo at 1% precision → 3 digits
- [ ] **Readout has context** — show both the value and what it means
- [ ] **Formula is displayed near the output it governs** — not buried in a README

## Error & Edge States

- [ ] **NaN/Infinity handled** — never show raw NaN, display dash or "N/A"
- [ ] **Empty canvas state** — if nothing to render, show explanatory message
- [ ] **Parameter bounds enforced** — sliders have reasonable min/max
- [ ] **Graceful degradation** — if WebGL fails, fall back to Canvas 2D with notice
- [ ] **No raw console errors visible to user** — all errors caught and displayed gracefully

## Accessibility

- [ ] **Color not the only differentiator** — shapes, patterns, or labels back up color coding
- [ ] **Canvas has a text alternative** — readout values replicate the key insight
- [ ] **Interactive elements are keyboard-accessible** — Tab navigates, Enter/Space activates
- [ ] **Font size >= 12px for all labels** — including axis ticks and legends

## First-Run Experience

- [ ] **Guided tour available** — optional step-by-step walkthrough of controls
- [ ] **Tour activates on first visit** (localStorage flag) — skip on return visits
- [ ] **Each tour step highlights ONE control** and explains what it does
- [ ] **Tour auto-advances when user interacts** — don't make them click "Next"
- [ ] **Example parameter set** — "Try these settings" button loads an interesting configuration

## Scientific Integrity

- [ ] **Source cited** — link to the publication or paper the demo is based on
- [ ] **Limitations stated** — what this demo does NOT show (simplifications, assumptions)
- [ ] **Reproducibility noted** — seed value displayed, PRNG type stated
- [ ] **No misleading axis ranges** — truncated axes are clearly marked
- [ ] **Error bars or confidence intervals** — for Monte Carlo or statistical outputs
