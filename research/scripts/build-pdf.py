"""build-pdf.py — CANONICAL one-shot CDP PDF build, permanent install.
Location: C:\\Users\\LENOVO\\.deepchat\\cdp-pipeline\\build-pdf.py
Pipeline: pandoc --mathjax (--citeproc when refs.bib present) -> CHTML->SVG +
inline cached MathJax -> render via Chrome for Testing -> verify
(>100KB, 0 U+FFFD/FFFF, math>0, STANDARD MARGINS).

Usage: python build-pdf.py <slug> [--pandoc <path>] [--skip-pandoc]
Requires: pandoc.exe at default path; cached MathJax; CfT chromium; pypdf (margin gate).

MARGIN MANDATE (user, 2026-08-21): rendered PDF page margins MUST be standard —
A4 with 2cm all around (top/bottom no smaller). Gate: static check of
render-pdf.cjs margin constants + dynamic pypdf geometry check of the produced
PDF (page size A4; text inset >= 40pt on all four sides).
"""
import os, sys, subprocess, re

PANDOC = r"C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = os.path.join(HERE, "render-pdf.cjs")
INLINE = os.path.join(HERE, "inline-mathjax.py")

def margin_static_gate():
    """Static gate: render-pdf.cjs must print A4 with 2cm margins on all sides."""
    try:
        src = open(RENDER, "r", encoding="utf-8").read()
    except Exception as e:
        return False, f"cannot read {RENDER}: {e}"
    if "format: 'A4'" not in src:
        return False, "render-pdf.cjs lacks format: 'A4'"
    m = re.search(r"margin:\s*\{\s*top:\s*'([^']+)'[^}]*bottom:\s*'([^']+)'[^}]*left:\s*'([^']+)'[^}]*right:\s*'([^']+)'\s*\}", src)
    if not m:
        return False, "render-pdf.cjs margin object not found"
    top, bottom, left, right = m.groups()
    for side, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        try:
            if float(val.rstrip("cm")) < 2.0:
                return False, f"margin {side}={val} < 2cm"
        except ValueError:
            return False, f"margin {side}={val} not parseable"
    return True, f"static margins OK (t={top} b={bottom} l={left} r={right})"

def margin_dynamic_gate(pdf):
    """Dynamic gate: produced PDF is A4 and text inset >= 40pt on all sides."""
    try:
        from pypdf import PdfReader
    except Exception as e:
        return False, f"pypdf unavailable ({e}); dynamic margin gate cannot run"
    try:
        reader = PdfReader(pdf)
        page = reader.pages[0]
        w, h = float(page.mediabox.width), float(page.mediabox.height)
        xs, ys = [], []
        def vis(text, cm, tm, font, size):
            if text and text.strip():
                xs.append(cm[4]); ys.append(cm[5])
        page.extract_text(visitor_text=vis)
        if not xs or not ys:
            return False, "no text found on page 1"
        min_x, min_y, max_y = min(xs), min(ys), max(ys)
        insets = {"left": min_x, "bottom": min_y, "top": h - max_y}
        for side, v in insets.items():
            if v < 40.0:
                return False, f"{side} inset {v:.1f}pt < 40pt (page {w:.1f}x{h:.1f})"
        if abs(w - 595.28) > 3.0 or abs(h - 841.89) > 3.0:
            return False, f"page size {w:.1f}x{h:.1f} != A4"
        return True, f"dynamic margins OK (A4 {w:.0f}x{h:.0f}pt; insets L={min_x:.0f} B={min_y:.0f} T={h-max_y:.0f}pt)"
    except Exception as e:
        return False, f"pypdf analysis failed: {e}"


def header_footer_static_gate():
    """Static gate: render-pdf.cjs MUST set displayHeaderFooter:false explicitly
    (PDF-NO-BROWSER-CHROME-1 — user directive: PDF MUST NEVER have web-browser
    headers/footers: date, URI, title, page chrome). Never rely on the implicit default."""
    try:
        src = open(RENDER, "r", encoding="utf-8").read()
    except Exception as e:
        return False, f"cannot read {RENDER}: {e}"
    if "displayHeaderFooter: false" not in src:
        return False, "render-pdf.cjs lacks explicit 'displayHeaderFooter: false' (browser header/footer risk)"
    return True, "displayHeaderFooter:false explicit (no browser header/footer)"

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python build-pdf.py <slug> [--pandoc <path>] [--skip-pandoc]")
        sys.exit(2)
    slug = args[0]
    pandoc = PANDOC
    skip_pandoc = False
    for i, a in enumerate(args):
        if a == "--pandoc" and i + 1 < len(args):
            pandoc = args[i + 1]
        if a == "--skip-pandoc":
            skip_pandoc = True

    md = None
    for cand in (f"{slug}.md", os.path.join("..", slug, f"{slug}.md"), os.path.join(slug, f"{slug}.md")):
        if os.path.exists(cand):
            md = cand
            break
    if not md:
        print("MD-NOT-FOUND for slug:", slug)
        sys.exit(2)

    base = os.path.splitext(md)[0]
    html = base + ".html"
    pdf = base + ".pdf"
    refs = os.path.join(os.path.dirname(md), "refs.bib")

    if not skip_pandoc:
        cmd = [pandoc, "--mathjax", "--standalone", md, "-o", html]
        if os.path.exists(refs):
            cmd += ["--citeproc", "--bibliography=" + refs]
            print("CITEPROC: refs.bib found — citations + bibliography enabled")
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        print("PANDOC-RC:", r.returncode)
        if r.returncode != 0:
            print(r.stdout, r.stderr)
            sys.exit(1)
    else:
        print("SKIP-PANDOC (HTML assumed present)")

    r = subprocess.run([sys.executable, INLINE, html], capture_output=True, text=True, timeout=120)
    print("INLINE-RC:", r.returncode)
    print(r.stdout)
    if r.returncode != 0:
        sys.exit(1)

    r = subprocess.run(["node", RENDER, os.path.abspath(html), os.path.abspath(pdf)],
                       capture_output=True, text=True, timeout=300)
    print("RENDER-RC:", r.returncode)
    print(r.stdout)
    if r.stderr:
        print("RENDER-STDERR:", r.stderr[:600])
    if r.returncode != 0:
        sys.exit(1)

    data = open(pdf, "rb").read()
    fffd = data.count(b"\xef\xbf\xbd")
    ffff = data.count(b"\xef\xbf\xbf")
    size = len(data)
    print(f"VERIFY: size={size} U+FFFD={fffd} U+FFFF={ffff}")

    ok_static, msg_static = margin_static_gate()
    print("MARGIN-STATIC:", "PASS" if ok_static else "FAIL", "-", msg_static)
    ok_hf, msg_hf = header_footer_static_gate()
    print("HEADER-FOOTER:", "PASS" if ok_hf else "FAIL", "-", msg_hf)
    ok_dynamic, msg_dynamic = margin_dynamic_gate(pdf)
    print("MARGIN-DYNAMIC:", "PASS" if ok_dynamic else "FAIL", "-", msg_dynamic)

    ok = size > 102400 and fffd == 0 and ffff == 0 and ok_static and ok_dynamic and ok_hf
    print("BUILD:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
