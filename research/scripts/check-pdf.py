#!/usr/bin/env python3
"""
check-pdf.py -- PDF rendering + integrity verification (v2.0, KIF-26 HARD BLOCK gate)

VERSION: 2.0 (2026-07-26)

This script is a MANDATORY PRE-PUBLICATION GATE. A PDF that fails this check
MUST NOT be published to Zenodo, R2, or any public distribution channel.

CHECKS PERFORMED:
1. Opens without error (corrupt PDF detection)
2. Zero pages containing U+FFFD (replacement character -- Unicode glyph miss)
3. Zero completely empty pages (get_text() returns only whitespace)
4. Page count > 0
5. Reports per-page character count for sanity skim
6. (v2.0) Scans for common rendering failure patterns beyond U+FFFD

EXIT CODES:
  0 = PASS - PDF is publication-ready
  1 = FAIL - Rendering errors detected, MUST NOT publish
  2 = BLOCKED - Script cannot run (missing dependency, bad arguments)

KAIZEN HISTORY:
- v1.0: Basic U+FFFD and empty page detection
- v2.0 (KIF-26): Added comprehensive glyph-miss pattern detection, mandatory
  gate status, clearer error messages with remediation steps

Usage:
    python check-pdf.py paper.pdf

Integration with publication pipeline:
    # In your build script:
    python unicode-latex-preprocess.py paper.md
    pandoc paper.md -o paper.pdf --pdf-engine=xelatex
    python check-pdf.py paper.pdf || exit 1  # HARD BLOCK on failure
"""
import sys
import time
import os
import shutil
import re


def _require_fitz():
    try:
        import fitz  # PyMuPDF
        return fitz
    except ImportError:
        print('[BLOCKED] PyMuPDF is not installed. Install it first:')
        print('    pip install PyMuPDF')
        print('Verify with: pip show PyMuPDF')
        sys.exit(2)


def replace_with_retry(src, dst, attempts=3, delay_s=2):
    """Replace dst with src, retrying if dst is locked (e.g. open in a PDF
    viewer on Windows raises PermissionError on os.replace). Falls back to
    writing a timestamped sibling file if all retries fail, so the build
    never silently appears to succeed while leaving stale content in place.
    """
    last_err = None
    for i in range(attempts):
        try:
            os.replace(src, dst)
            return dst
        except PermissionError as e:
            last_err = e
            if i < attempts - 1:
                time.sleep(delay_s)
    fallback = dst.rsplit('.', 1)[0] + f'.{int(time.time())}.pdf'
    shutil.copy2(src, fallback)
    print(f'[WARN] Could not replace {dst} (locked by another process). '
          f'Wrote to {fallback} instead.')
    raise last_err


# Common rendering failure patterns (beyond U+FFFD)
GLYPH_MISS_PATTERNS = [
    ('\ufffd', 'U+FFFD replacement character'),
    ('□', 'missing glyph box'),
    ('▯', 'missing glyph box (vertical)'),
    ('\u25a1', 'white square (glyph placeholder)'),
    ('\u25a0', 'black square (glyph placeholder)'),
    ('\u2610', 'ballot box (glyph placeholder)'),
]

# Patterns that indicate the preprocessor was NOT run
UNPROCESSED_UNICODE_PATTERNS = [
    # Blackboard bold that should have been converted
    (r'[ℚℝℂℤℕℍ𝔸]', 'unconverted blackboard-bold letter'),
    # Subscript letters that should have been converted
    (r'[ₐₑₒₓₕₖₗₘₙₚₛₜ]', 'unconverted subscript letter'),
    # Greek letters outside math mode (heuristic: followed by space/punctuation)
    (r'[αβγδεζηθικλμνξπρστυφχψω]\s', 'possible unconverted Greek letter'),
    # h-bar and script ell
    (r'[ħℓ]', 'unconverted physics symbol (ħ or ℓ)'),
]


def check_pdf(path):
    fitz = _require_fitz()
    
    print(f'=== PDF PUBLICATION GATE: {path} ===\n')
    
    try:
        doc = fitz.open(path)
    except Exception as e:
        print(f'[BLOCKED] PDF failed to open (corrupt or invalid): {e}')
        return 1

    if doc.page_count == 0:
        print('[FAIL] PDF has zero pages.')
        return 1

    errors = []
    warnings = []
    empty_pages = []
    total_chars = 0
    
    for page in doc:
        text = page.get_text()
        page_chars = len(text)
        total_chars += page_chars
        
        # Check for replacement characters and glyph-miss patterns
        for pattern, desc in GLYPH_MISS_PATTERNS:
            if pattern in text:
                count = text.count(pattern)
                errors.append(
                    f'Page {page.number + 1}: {count} {desc}(s) found — '
                    f'run unicode-latex-preprocess.py and rebuild'
                )
        
        # Check for unprocessed Unicode (preprocessor was not run)
        for regex, desc in UNPROCESSED_UNICODE_PATTERNS:
            matches = re.findall(regex, text)
            if matches:
                warnings.append(
                    f'Page {page.number + 1}: {len(matches)} {desc}(s) detected — '
                    f'may indicate preprocessor was not run'
                )
        
        # Check for empty pages
        if not text.strip():
            empty_pages.append(page.number + 1)
        
        print(f'[INFO] Page {page.number + 1}: {page_chars} chars')

    print(f'\n[INFO] Total pages: {doc.page_count}, Total chars: {total_chars}')

    if empty_pages:
        errors.append(f'Empty pages (no extractable text): {empty_pages}')

    # Report warnings (non-blocking but should be reviewed)
    if warnings:
        print('\n[WARNINGS] (review recommended, not blocking):')
        for w in warnings:
            print(f'  ⚠ {w}')

    # Report errors (blocking)
    if errors:
        print('\n[FAIL] PDF verification FAILED — MUST NOT PUBLISH:')
        for e in errors:
            print(f'  ❌ {e}')
        print('\n[REMEDIATION STEPS]:')
        print('  1. Run: python unicode-latex-preprocess.py paper.md')
        print('  2. Rebuild: pandoc paper.md -o paper.pdf --pdf-engine=xelatex')
        print('  3. Re-run: python check-pdf.py paper.pdf')
        print('  4. Only publish after this script exits with code 0')
        return 1

    print('\n[PASS] PDF rendering verified — no replacement characters, no empty pages.')
    print('[OK] PDF is publication-ready.')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python check-pdf.py <path-to-pdf>')
        print('\nThis is a MANDATORY PRE-PUBLICATION GATE.')
        print('A PDF that fails this check MUST NOT be published.')
        sys.exit(2)
    sys.exit(check_pdf(sys.argv[1]))
