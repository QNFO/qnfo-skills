"""Inline cached MathJax into pandoc HTML — CANONICAL, permanent install.
Location: C:\\Users\\LENOVO\\.deepchat\\cdp-pipeline\\inline-mathjax.py (NEVER %TEMP%).
Follows references/cdp-pdf-pipeline.md Steps 3-4. Uses the PERMANENT cached MathJax
at ~/.deepchat/cdp-pipeline/mathjax/tex-svg-full.js (never re-downloads; falls back
to ~/.deepchat/mathjax/tex-svg-full.js then to CDN ONLY if both are missing).

Usage: python inline-mathjax.py <input.html> [--check-only]
"""
import os, sys, re, io, urllib.request

PERM = os.path.join(os.path.expanduser("~"), ".deepchat", "cdp-pipeline", "mathjax", "tex-svg-full.js")
ALT = os.path.join(os.path.expanduser("~"), ".deepchat", "mathjax", "tex-svg-full.js")

def mathjax_path():
    for p in (PERM, ALT):
        if os.path.exists(p) and os.path.getsize(p) > 500000:
            return p
    return None

def fetch_mathjax_fallback():
    """Only if NO cached copy exists (should never happen after permanent install)."""
    cdn = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg-full.js"
    UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    data = urllib.request.urlopen(urllib.request.Request(cdn, headers={"User-Agent": UA}), timeout=120).read()
    os.makedirs(os.path.dirname(PERM), exist_ok=True)
    with open(PERM, "wb") as f:
        f.write(data)
    return PERM

def main():
    html_path = sys.argv[1]
    check_only = "--check-only" in sys.argv
    html = io.open(html_path, encoding="utf-8").read()

    src = mathjax_path()
    if src:
        print("MATHJAX-SOURCE:", src)
    else:
        print("MATHJAX-CACHE-MISSING -> fallback download (should not happen)")
        src = fetch_mathjax_fallback()
    mj = io.open(src, encoding="utf-8", errors="replace").read()
    print("MATHJAX-LEN:", len(mj))

    if "tex-chtml-full.js" in html:
        html = html.replace("tex-chtml-full.js", "tex-svg-full.js")
        print("STEP3: switched CHTML -> SVG")

    matches = list(re.finditer(r'<script[^>]*tex-svg[^>]*>[^<]*</script>', html))
    if not matches:
        matches = list(re.finditer(r'<script[^>]*src="[^"]*tex-svg[^"]*"[^>]*></script>', html))
    if not matches:
        raise RuntimeError("No MathJax script tag found in HTML")
    full_match = matches[0].group(0)
    inline_tag = "<script>" + mj + "</script>"
    html = html.replace(full_match, inline_tag)  # str.replace, NEVER re.sub (\\u escapes)
    print("STEP4: inlined MathJax via str.replace")

    if not check_only:
        io.open(html_path, "w", encoding="utf-8").write(html)
    print("INLINE-OK:", len(html), "bytes")

if __name__ == "__main__":
    main()
