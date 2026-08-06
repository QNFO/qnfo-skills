"""check-title-duplication.py — TITLE-DUPLICATION-1 scripted gate (research v2.86).

Usage: python check-title-duplication.py <rendered.html>

GATE: When the source markdown has a YAML `title:`, pandoc renders it as
`<h1 class="title">`. A body `# <Title>` H1 duplicates it on page 1.
PASS = exactly ONE `<h1 class="title">` AND zero body `<h1>` elements.
FAIL = any other combination (exit code 1). Prints the diagnosis.

Also counts the <head><title> meta tag and prints it for context — it is
NOT a rendered heading and does not count toward the gate (browser tab
title only). This prevents the N-2-SCAN-FALSE-POSITIVE-1 class of false
positive where a naive regex counts the meta title as a duplicate.

Canonical case: ODR 2026-08-06 v0.1-v0.3 — body H1 duplicated the YAML
title on page 1 through three published versions; v0.4 fixed + scripted
(this gate). Enforcement of TITLE-DUPLICATION-1 (research v2.84,
qnfo-core v1.16).
"""

import re
import sys
import os


def main():
    if len(sys.argv) < 2:
        print("ERROR: usage: python check-title-duplication.py <rendered.html>")
        sys.exit(1)

    html_path = sys.argv[1]
    if not os.path.exists(html_path):
        print(f"ERROR: file not found: {html_path}")
        sys.exit(1)

    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    # Rendered <h1> tags WITH attributes — the gate counts these
    h1_tags = re.findall(r"<h1[^>]*>", html)
    title_h1 = [t for t in h1_tags if 'class="title"' in t]
    body_h1 = [t for t in h1_tags if 'class="title"' not in t]

    # Meta title (browser tab) — informational only, NOT counted
    meta_title = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    meta_title_text = meta_title.group(1).strip() if meta_title else None

    print(f"HTML: {html_path}")
    print(f"  <head><title> (meta, not counted): {meta_title_text}")
    print(f"  Rendered <h1 class=\"title\"> (YAML): {len(title_h1)}")
    print(f"  Rendered body <h1>: {len(body_h1)}")

    if len(title_h1) == 1 and len(body_h1) == 0:
        print("GATE PASS: exactly one rendered title, zero body H1 duplicates")
        sys.exit(0)
    elif len(title_h1) == 0 and len(body_h1) == 0:
        print("GATE FAIL: no rendered title at all — YAML `title:` missing or pandoc did not emit it")
        sys.exit(1)
    elif len(body_h1) > 0:
        for h in body_h1:
            print(f"  BODY H1: {h}")
        print("GATE FAIL: TITLE-DUPLICATION-1 — body H1 duplicates the YAML title on page 1")
        print("  FIX: remove the body '# <Title>' H1; the YAML title is the single page-1 title")
        sys.exit(1)
    else:
        print(f"GATE FAIL: unexpected h1 structure (title_h1={len(title_h1)}, body_h1={len(body_h1)})")
        sys.exit(1)


if __name__ == "__main__":
    main()
