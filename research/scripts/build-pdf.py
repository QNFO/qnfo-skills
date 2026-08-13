"""build-pdf.py — CANONICAL one-shot CDP PDF build, permanent install.
Location: C:\\Users\\LENOVO\\.deepchat\\cdp-pipeline\\build-pdf.py
Pipeline: pandoc --mathjax -> CHTML->SVG + inline cached MathJax -> render via
Chrome for Testing (NO Edge) -> verify (>100KB, 0 U+FFFD/FFFF, math>0).

Usage: python build-pdf.py <slug> [--pandoc <path>] [--skip-pandoc]
Requires: pandoc.exe at default path; cached MathJax; CfT chromium.
"""
import os, sys, subprocess, io

PANDOC = r"C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = os.path.join(HERE, "render-pdf.cjs")
INLINE = os.path.join(HERE, "inline-mathjax.py")

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

    # find the .md (search cwd + project dirs)
    md = None
    for cand in (f"{slug}.md", os.path.join("..", slug, f"{slug}.md"), os.path.join(slug, f"{slug}.md")):
        if os.path.exists(cand):
            md = cand
            break
    if not md:
        print("MD-NOT-FOUND for slug:", slug)
        sys.exit(2)

    base = os.path.splitext(md)[0]  # <slug> (same dir)
    html = base + ".html"
    pdf = base + ".pdf"

    # 1. pandoc
    if not skip_pandoc:
        r = subprocess.run([pandoc, "--mathjax", "--standalone", md, "-o", html],
                           capture_output=True, text=True, timeout=120)
        print("PANDOC-RC:", r.returncode)
        if r.returncode != 0:
            print(r.stdout, r.stderr)
            sys.exit(1)
    else:
        print("SKIP-PANDOC (HTML assumed present)")

    # 2. inline MathJax
    r = subprocess.run([sys.executable, INLINE, html], capture_output=True, text=True, timeout=120)
    print("INLINE-RC:", r.returncode)
    print(r.stdout)
    if r.returncode != 0:
        sys.exit(1)

    # 3. render
    r = subprocess.run(["node", RENDER, os.path.abspath(html), os.path.abspath(pdf)],
                       capture_output=True, text=True, timeout=300)
    print("RENDER-RC:", r.returncode)
    print(r.stdout)
    if r.stderr:
        print("RENDER-STDERR:", r.stderr[:600])
    if r.returncode != 0:
        sys.exit(1)

    # 4. verify binary bytes
    data = open(pdf, "rb").read()
    fffd = data.count(b"\xef\xbf\xbd")
    ffff = data.count(b"\xef\xbf\xbf")
    size = len(data)
    print(f"VERIFY: size={size} U+FFFD={fffd} U+FFFF={ffff}")
    ok = size > 102400 and fffd == 0 and ffff == 0
    print("BUILD:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
