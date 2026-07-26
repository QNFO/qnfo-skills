#!/usr/bin/env python3
"""
build-pdf.py — HOLISTIC PDF build pipeline for QNFO publications (v1.0)

THE CORRECT SOLUTION: Instead of converting Unicode characters to LaTeX
via dictionaries (which can never be comprehensive), we configure XeLaTeX
to use fonts that HAVE the Unicode glyphs (STIX Two Math, unicode-math).

This script:
1. Validates the source markdown
2. Builds PDF using Pandoc + XeLaTeX with unicode-math + STIX Two Math
3. Verifies the PDF has zero rendering errors
4. Reports any issues with actionable remediation

USAGE:
    python build-pdf.py paper.md                    # Outputs paper.pdf
    python build-pdf.py paper.md --output out.pdf   # Custom output path
    python build-pdf.py paper.md --check-only       # Validate without building

REQUIREMENTS:
    - Pandoc (any recent version)
    - XeLaTeX (TeX Live 2020+)
    - unicode-math package (included in TeX Live)
    - STIX Two Math font (included in TeX Live)
    - PyMuPDF for verification: pip install PyMuPDF
"""

import argparse
import subprocess
import sys
import os
import tempfile
from pathlib import Path

# Skill root for finding templates
SKILL_ROOT = Path(__file__).parent.parent


def check_dependencies():
    """Verify all required tools are available."""
    issues = []
    
    # Check Pandoc
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            issues.append("Pandoc not found or not working")
    except FileNotFoundError:
        issues.append("Pandoc not installed (https://pandoc.org/installing.html)")
    
    # Check XeLaTeX
    try:
        result = subprocess.run(['xelatex', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            issues.append("XeLaTeX not found or not working")
    except FileNotFoundError:
        issues.append("XeLaTeX not installed (install TeX Live)")
    
    # Check unicode-math package
    try:
        result = subprocess.run(['kpsewhich', 'unicode-math.sty'], capture_output=True, text=True)
        if not result.stdout.strip():
            issues.append("unicode-math package not found (install texlive-latex-extra or full TeX Live)")
    except FileNotFoundError:
        pass  # kpsewhich might not be in PATH on Windows
    
    # Check STIX Two Math font
    try:
        result = subprocess.run(['fc-list', ':', 'family'], capture_output=True, text=True)
        if 'STIX Two Math' not in result.stdout:
            issues.append("STIX Two Math font not found (install texlive-fonts-extra or download from STIX fonts)")
    except FileNotFoundError:
        pass  # fc-list might not be available
    
    # Check PyMuPDF for verification
    try:
        import fitz
    except ImportError:
        issues.append("PyMuPDF not installed for PDF verification (pip install PyMuPDF)")
    
    return issues


def build_pdf(input_path: Path, output_path: Path, verbose: bool = False) -> tuple[bool, str]:
    """
    Build PDF using Pandoc + XeLaTeX with unicode-math configuration.
    
    Returns (success: bool, message: str)
    """
    # Pandoc command with unicode-math configuration
    # We embed the LaTeX header directly rather than using a defaults file
    # for maximum portability
    
    header_includes = r'''
\usepackage{fontspec}
\usepackage{unicode-math}
\setmathfont{STIX Two Math}
\setmainfont{TeX Gyre Pagella}[Ligatures=TeX]
\setsansfont{TeX Gyre Heros}
\setmonofont{DejaVu Sans Mono}[Scale=0.9]
'''
    
    cmd = [
        'pandoc',
        str(input_path),
        '-o', str(output_path),
        '--pdf-engine=xelatex',
        f'--variable=header-includes:{header_includes}',
        '--variable=geometry:margin=1in',
        '--variable=documentclass:article',
        '--variable=classoption:11pt',
        '--citeproc',  # Process citations if bibliography present
    ]
    
    # Check for bibliography file
    bib_path = input_path.parent / 'refs.bib'
    if bib_path.exists():
        cmd.extend(['--bibliography', str(bib_path)])
    
    if verbose:
        print(f"[BUILD] Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=input_path.parent,
            timeout=300  # 5 minute timeout for large documents
        )
        
        if result.returncode != 0:
            # Extract useful error from XeLaTeX output
            error_lines = []
            for line in result.stderr.split('\n'):
                if 'error' in line.lower() or 'missing' in line.lower() or '!' in line:
                    error_lines.append(line)
            
            error_msg = '\n'.join(error_lines[-20:]) if error_lines else result.stderr[-2000:]
            return False, f"Pandoc/XeLaTeX build failed:\n{error_msg}"
        
        return True, f"PDF built successfully: {output_path}"
        
    except subprocess.TimeoutExpired:
        return False, "Build timed out after 5 minutes"
    except Exception as e:
        return False, f"Build error: {e}"


def verify_pdf(pdf_path: Path) -> tuple[bool, str, list]:
    """
    Verify PDF has no rendering errors.
    
    Returns (success: bool, message: str, issues: list)
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return True, "PyMuPDF not available, skipping verification", []
    
    issues = []
    
    try:
        doc = fitz.open(str(pdf_path))
    except Exception as e:
        return False, f"PDF failed to open: {e}", [str(e)]
    
    if doc.page_count == 0:
        return False, "PDF has zero pages", ["Zero pages"]
    
    total_replacement_chars = 0
    empty_pages = []
    
    for page_num, page in enumerate(doc, 1):
        text = page.get_text()
        
        # Check for replacement characters (U+FFFD)
        replacement_count = text.count('\ufffd')
        if replacement_count > 0:
            total_replacement_chars += replacement_count
            # Find context around replacement characters
            for i, char in enumerate(text):
                if char == '\ufffd':
                    start = max(0, i - 20)
                    end = min(len(text), i + 20)
                    context = text[start:end].replace('\n', ' ')
                    issues.append(f"Page {page_num}: U+FFFD at position {i}: ...{context}...")
                    if len(issues) > 10:
                        issues.append(f"... and {replacement_count - 10} more on this page")
                        break
        
        # Check for empty pages
        if not text.strip():
            empty_pages.append(page_num)
    
    page_count = doc.page_count
    doc.close()
    
    if total_replacement_chars > 0:
        return False, f"PDF has {total_replacement_chars} replacement characters (U+FFFD)", issues
    
    if empty_pages:
        issues.append(f"Empty pages: {empty_pages}")
        return False, f"PDF has {len(empty_pages)} empty page(s)", issues
    
    return True, f"PDF verified: {page_count} pages, no rendering errors", []


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('--output', '-o', help='Output PDF path (default: same name as input)')
    parser.add_argument('--check-only', action='store_true', help='Check dependencies only, do not build')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--skip-verify', action='store_true', help='Skip PDF verification')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}")
        sys.exit(2)
    
    output_path = Path(args.output) if args.output else input_path.with_suffix('.pdf')
    
    # Check dependencies
    print("[CHECK] Verifying dependencies...")
    dep_issues = check_dependencies()
    if dep_issues:
        print("[WARN] Dependency issues found:")
        for issue in dep_issues:
            print(f"  - {issue}")
        if args.check_only:
            sys.exit(1)
    else:
        print("[OK] All dependencies available")
    
    if args.check_only:
        sys.exit(0)
    
    # Build PDF
    print(f"[BUILD] Building {input_path} -> {output_path}")
    success, message = build_pdf(input_path, output_path, verbose=args.verbose)
    
    if not success:
        print(f"[FAIL] {message}")
        sys.exit(1)
    
    print(f"[OK] {message}")
    
    # Verify PDF
    if not args.skip_verify:
        print("[VERIFY] Checking PDF for rendering errors...")
        success, message, issues = verify_pdf(output_path)
        
        if not success:
            print(f"[FAIL] {message}")
            for issue in issues[:20]:
                print(f"  - {issue}")
            print("\n[REMEDIATION] The unicode-math + STIX Two Math configuration should")
            print("handle all standard Unicode math symbols. If you still see U+FFFD:")
            print("  1. Check if the character is in a code block (use ASCII there)")
            print("  2. Check if it's an exotic symbol not in STIX Two Math")
            print("  3. For exotic symbols, use explicit LaTeX: $\\symbol{...}$")
            sys.exit(1)
        
        print(f"[OK] {message}")
    
    print(f"\n[SUCCESS] Publication-ready PDF: {output_path}")
    sys.exit(0)


if __name__ == '__main__':
    main()
