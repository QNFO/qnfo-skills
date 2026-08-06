# Design System — Light, Readable, Academic, Self-Explanatory

Default theme for interactive PoC demos. Dark themes are rejected by users (unreadable, indecipherable). This system is deliberately plain and high-contrast — the content (your math) is the hero, not the chrome.

## Self-Explanatory Mandate (USER MANDATE 2026-08-06 — HARD)

Any person opening the demo must understand — within 10 seconds, with zero instruction — what it is, what it proves, and how to interact. Every demo MUST include:

1. **One-sentence header claim:** the header states the research claim the demo demonstrates (e.g., "Bruhat–Tits QEC: staircase redundancy vs smooth Archimedean codes").
2. **Labeled controls:** every button/slider/tab has visible descriptive text. No cryptic icons without adjacent text.
3. **"How to use" panel:** collapsible (default collapsed, one click), one line per control explaining what it does.
4. **Live status overlay:** bottom-left of the canvas, explains the current interaction state ("Error mode: click a node to inject an error").
5. **Legend:** always visible when the canvas has colored elements.
6. **Tooltips:** every interactive element (buttons, canvas nodes) shows a tooltip on hover.
7. **Key insight panel:** states what the user should observe and how to verify it themselves (e.g., "Count the horizontal steps in the curve — each is a QEC-Darwinism coexistence window").
8. **Zero unexplained jargon:** if a term must appear (e.g., "redundancy"), define it inline once in the key insight panel.

## Palette

| Token | Value | Use |
|:------|:------|:----|
| `--bg` | `#ffffff` | Page background |
| `--surface` | `#f8f9fa` | Cards, panels, sidebar |
| `--border` | `#dee2e6` | Hairlines, dividers |
| `--text` | `#212529` | Primary text (WCAG AAA on white) |
| `--muted` | `#6c757d` | Labels, captions, secondary text |
| `--accent` | `#1a73e8` | Interactive elements, primary buttons, links |
| `--accent-soft` | `#e8f0fe` | Active states, selected backgrounds |
| `--error` | `#d93025` | Errors, error-subtree highlighting |
| `--compare` | `#b06000` | Comparison curve (gold/amber, on light bg) |

## Typography

- **Display / headings:** Georgia, 'Times New Roman', serif — academic, trustworthy.
- **Body / UI / code:** system stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`.
- **Monospace (numbers, math):** `'JetBrains Mono', Consolas, monospace`.
- Body ≥ 14px; labels ≥ 12px; never below 11px.
- Headings with clear size hierarchy (h1 = 1.5rem, h2 = 1.15rem, section titles = 0.7rem uppercase tracked).

## Layout

- Header: page title (with the one-sentence claim) left, status dot right.
- Main: fixed control sidebar (300-360px) + fluid canvas viewport.
- Sections: cards with 1px border, 6px radius, 12-16px padding.
- Tabs for multi-view (e.g., "Geometry" / "Curve").
- Legend bar under canvas with color swatches.
- "How to use" collapsible: details/summary element, open on first visit (auto-open once, then collapsed).
- Responsive: sidebar stacks above viewport on <768px; controls stay reachable.

## Canvas rendering

- Canvas background: white (`#ffffff`).
- Tree edges: `#adb5bd` (default), error edges `rgba(217,48,37,0.4)`.
- Nodes: root = accent outline; internal = `#f8f9fa` fill + `#ced4da` border; leaf = `#e9ecef`; selected = accent fill; error = `#d93025` fill.
- Axis lines: `#ced4da`; grid: `#f1f3f5`; curves: accent solid; comparison dashed.
- Canvas title/labels: axis labels in muted, ≥ 10px.

## Interaction feedback

- Hover: border-color → accent on controls; tooltip on canvas nodes.
- Active toggle: accent background + white text (`--accent` bg, `#fff` text).
- Overlay status line: bottom-left of canvas, muted text; error mode → `--error` text.
- Every action visibly changes: stats grid, overlay line, or canvas — never nothing.
- Keyboard: controls reachable and operable via keyboard (buttons = native `<button>`).

## Console self-test

On page load, print a verification line with actual computed values and PASS/FAIL:

```js
console.log('p=' + p + ' d=' + d + ' nodes=' + tree.nodeCount +
  ' redundancy=' + tree.getRedundancy(d));
console.log('Verification: ' + (assertion ? 'PASS' : 'FAIL'));
```

## Anti-patterns

| Pattern | Fix |
|:--------|:----|
| Dark background / neon text | Use the light palette above |
| `#00e5a0` green on black "hacker" style | Replace with blue accent on white |
| Centered everything, huge hero | Grid layout with real information density |
| Decorative metrics that don't change | Live computed stats only |
| Fonts below 11px | Raise to ≥ 12px; body ≥ 14px |
| Icon-only buttons with no text label | Add visible descriptive text (self-explanatory mandate) |
| No legend / no status overlay | Always include legend + live status line |
| No "How to use" | Include the collapsible help panel |
| Header without the research claim | One sentence stating what the demo proves |
