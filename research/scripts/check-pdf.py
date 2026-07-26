#!/usr/bin/env python3
"""
check-pdf.py -- PDF rendering + integrity verification (v3.0, KIF-26 v2)

VERSION: 3.0 (2026-07-26)

This script is a MANDATORY PRE-PUBLICATION GATE. A PDF that fails this check
MUST NOT be published to Zenodo, R2, or any public distribution channel.

CHECKS PERFORMED:
1. Opens without error (corrupt PDF detection)
2. Zero pages containing U+FFFD (replacement character -- Unicode glyph miss)
3. Zero completely empty pages (get_text() returns only whitespace)
4. Page count > 0
5. Reports per-page character count for sanity skim

EXIT CODES:
  0 = PASS - PDF is publication-ready
  1 = FAIL - Rendering errors detected, MUST NOT publish
  2 = BLOCKED - Script cannot run (missing dependency, bad arguments)

KAIZEN HISTORY:
- v1.0: Basic U+FFFD and empty page detection
- v2.0 (KIF-26): Added comprehensive glyph-miss pattern detection
- v3.0 (KIF-26 v2): Removed misleading "unconverted Unicode" warnings.
  When using unicode-math + STIX Two Math (the correct solution), Unicode
  characters render correctly but remain as Unicode in extracted text.
  The only true failure indicator is U+FFFD replacement characters.

Usage:
    python check-pdf.py paper.pdf

Integration with publication pipeline:
    python build-pdf.py paper.md  # This calls check-pdf.py automatically
"""
import sys
import time
import os
import shutil


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
    empty_pages = []
    total_chars = 0
    total_replacement_chars = 0
    
    for page in doc:
        text = page.get_text()
        page_chars = len(text)
        total_chars += page_chars
        
        # Check for U+FFFD replacement characters - the ONLY true failure indicator
        replacement_count = text.count('\ufffd')
        if replacement_count > 0:
            total_replacement_chars += replacement_count
            errors.append(
                f'Page {page.number + 1}: {replacement_count} U+FFFD replacement character(s) — '
                f'font is missing glyphs. Use unicode-math + STIX Two Math.'
            )
        
        # Check for empty pages
        if not text.strip():
            empty_pages.append(page.number + 1)
        
        print(f'[INFO] Page {page.number + 1}: {page_chars} chars')

    page_count = doc.page_count
    doc.close()
    
    print(f'\n[INFO] Total pages: {page_count}, Total chars: {total_chars}')

    if empty_pages:
        errors.append(f'Empty pages (no extractable text): {empty_pages}')

    # Report errors (blocking)
    if errors:
        print('\n[FAIL] PDF verification FAILED — MUST NOT PUBLISH:')
        for e in errors:
            print(f'  ❌ {e}')
        print('\n[REMEDIATION]:')
        print('  Use build-pdf.py which configures XeLaTeX with unicode-math + STIX Two Math.')
        print('  This font has comprehensive Unicode coverage and eliminates glyph-miss errors.')
        print('  Command: python build-pdf.py paper.md')
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
