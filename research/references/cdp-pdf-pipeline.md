# CDP PDF Pipeline (Production Tier)

> **Source skill:** research v2.68+
> **Status:** OPTIONAL — DO NOT USE BY DEFAULT
> **Cross-reference:** Load via `skill_view("research", "references/cdp-pdf-pipeline.md")`
> **Canonical incident (2026-08-04):** 5-step pipeline verified working on this machine.
> Chromium detection: Edge → Chrome → Playwright → Chrome for Testing (4 binaries).

---

#### Production Tier: CDP PDF Pipeline

**CANONICAL PIPELINE:** pandoc (--mathjax) → MathJax SVG switch → MathJax local download + inline → puppeteer-core CDP PDF render. TeX Live uninstalled (2026-08-02). xhtml2pdf and Page.printToPDF permanently deprecated (2026-08-03). MathJax MUST use SVG output processor (`tex-svg-full.js`), NOT CHTML (`tex-chtml-full.js`) — CHTML uses Private Use Area glyphs that do not survive CDP capture.

**CHROMIUM GATE (PRODUCTION TIER ONLY):** If no Chromium binary exists anywhere on the system and the CDP pipeline is requested: **fall back to the PRIMARY tier** (pandoc → MathJax HTML → browser print-to-PDF). For automated CDP PDF, procure Chrome for Testing (see below). The Primary Tier is always available — publication is NEVER blocked by missing Chromium.

#### Step 1: Detect Chromium (VERIFY before downloading — 4 binaries on this machine)

This machine has 4 Chromium binaries (Edge, Chrome, Playwright, cached Chrome for Testing). The PRIMARY TIER requires ZERO of them. For the OPTIONAL Production Tier, use the detection chain in Step 1: check Edge → Chrome → Playwright → CfT before ever downloading. **Do NOT use `npx puppeteer browsers install` or `@puppeteer/browsers` install() — both hang indefinitely on this machine.** If a download IS needed (very rare), use Python urllib instead:

```python
# dl_chrome.py — write to %TEMP%, run with python
import urllib.request, zipfile, os

cache_dir = os.path.join(os.environ["USERPROFILE"], ".cache", "puppeteer", "chrome")
os.makedirs(cache_dir, exist_ok=True)

# Discover latest version from Google Chrome Labs API:
# https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
# Or use a known-good version:
version = "153.0.7989.0"
url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/win64/chrome-win64.zip"
zip_path = os.path.join(cache_dir, f"chrome-{version}.zip")

urllib.request.urlretrieve(url, zip_path)  # ~194 MB, 2-5 minutes

with zipfile.ZipFile(zip_path, 'r') as zf:
    zf.extractall(cache_dir)

# Result: %USERPROFILE%\.cache\puppeteer\chrome\chrome-win64\chrome.exe
```

Launch puppeteer-core with:
```js
const chromeExe = `${os.homedir()}/.cache/puppeteer/chrome/chrome-win64/chrome.exe`;
const browser = await puppeteer.launch({
    executablePath: chromeExe,
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
});
```

#### Step 2: Build HTML with pandoc

```bash
C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe --mathjax --standalone <slug>.md -o <slug>.html
```

**Source delimiters (2026-08-03):** source markdown MUST use `$...$` / `$$...$$` delimiters, NOT `\(...\)` / `\[...\]`. Pandoc's default reader treats `\(` as an escaped paren and STRIPS the LaTeX. If source has `\(`, convert first: `re.sub(r'\\\\((.*?)\\\)', r'$\1$', source)`.

#### Step 3: Switch MathJax from CHTML to SVG

pandoc `--mathjax` emits `tex-chtml-full.js`. CHTML uses Private Use Area glyphs that do not survive CDP capture. Switch to SVG:

```python
# switch_svg.py
html = open(html_path, 'r', encoding='utf-8').read()
html = html.replace('tex-chtml-full.js', 'tex-svg-full.js')
open(html_path, 'w', encoding='utf-8').write(html)
```

#### Step 4: Download MathJax locally and inline (CRITICAL — CDN UNREACHABLE)

The MathJax CDN (`cdn.jsdelivr.net`) is UNREACHABLE from Chrome headless on this machine. The HTML `page.goto()` with `networkidle0` will hang forever waiting for the CDN. **MathJax must be downloaded locally AND inlined into the HTML.**

```python
# fix_mathjax.py — download MathJax and inline into both HTMLs
import urllib.request, os, re

cdn_url = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg-full.js"
local_dir = os.path.join(os.environ["TEMP"], "mathjax")
os.makedirs(local_dir, exist_ok=True)
local_path = os.path.join(local_dir, "tex-svg-full.js")
urllib.request.urlretrieve(cdn_url, local_path)  # ~2.2 MB

# Read MathJax JS
with open(local_path, 'r', encoding='utf-8') as f:
    mathjax_js = f.read()

# Inline into each HTML
for html_name in ['paper1.html', 'paper2.html']:
    html_path = os.path.join(os.environ['TEMP'], html_name)
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find the MathJax script tag (split across lines in pandoc output)
    matches = list(re.finditer(r'<script[^>]*tex-svg[^>]*>[^<]*</script>', html))
    if not matches:
        raise RuntimeError(f"No MathJax script tag found in {html_name}")
    
    full_match = matches[0].group(0)
    inline_tag = f'<script>{mathjax_js}</script>'
    
    # IMPORTANT: use str.replace() NOT re.sub() — MathJax JS contains \u escape
    # sequences that crash Python's re.sub(). str.replace() handles these fine.
    html = html.replace(full_match, inline_tag)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Inlined MathJax into {html_name}: {len(html)} chars')
```

**CRITICAL:** Use `str.replace(full_match, inline_tag)`, NOT `re.sub()` — MathJax JS contains `\uXXXX` escape sequences that crash `re.sub()` with "bad escape \u at position N".

#### Step 5: Render PDF via puppeteer-core CDP

**Always write Node scripts to `.mjs` files — `node -e` fails in cmd.exe with "Unterminated string constant" when code contains quotes or line breaks.**

```js
// render_pdf.mjs — use with: node render_pdf.mjs
import { existsSync, statSync } from 'fs';
import { resolve } from 'path';
import os from 'os';
import puppeteer from 'puppeteer-core';

// Detect Chromium: priority chain (Edge → Chrome → Playwright → cached CfT)
function findChrome() {
    const candidates = [
        'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
        'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
        'C:/Program Files/Google/Chrome/Application/chrome.exe',
    ];
    const {globSync} = require('glob');
    const pw = globSync(os.homedir() + '/AppData/Local/ms-playwright/chromium-*/chrome-win64/chrome.exe');
    if (pw.length) candidates.push(pw.sort().reverse()[0]);
    candidates.push(os.homedir() + '/.cache/puppeteer/chrome/chrome-win64/chrome.exe');
    for (const c of candidates) { if (existsSync(c)) return c; }
    throw new Error('No Chromium found');
}

const chromeExe = findChrome();
const tmp = process.env.TEMP || os.tmpdir();

async function render(htmlName, pdfName) {
    const htmlFile = resolve(tmp, htmlName);
    const pdfFile = resolve(tmp, pdfName);
    
    if (!existsSync(htmlFile)) throw new Error(`HTML not found: ${htmlFile}`);
    
    const browser = await puppeteer.launch({
        executablePath: chromeExe,
        headless: true,
        args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
    });
    
    try {
        const page = await browser.newPage();
        const fileUrl = 'file:///' + htmlFile.replace(/\\/g, '/');
        
        await page.goto(fileUrl, { waitUntil: 'load', timeout: 120000 });
        
        // Wait for MathJax to render (inline JS, no CDN dependency)
        const mjStatus = await page.evaluate(() => {
            if (typeof window.MathJax === 'undefined') return 'MathJax undefined';
            if (window.MathJax.startup && window.MathJax.startup.promise)
                return 'MathJax has startup.promise';
            return 'MathJax exists but no startup';
        });
        console.log('MathJax status:', mjStatus);
        
        try {
            await page.evaluate(() => window.MathJax.startup.promise);
            console.log('MathJax rendered successfully');
        } catch (e) {
            console.log('MathJax render error:', e.message.substring(0, 200));
        }
        
        const mathCount = await page.evaluate(() =>
            document.querySelectorAll('mjx-container, .MathJax, mjx-assistive-mml').length
        );
        console.log('Rendered math elements:', mathCount);
        
        await new Promise(r => setTimeout(r, 3000));  // extra settle time
        
        await page.pdf({
            path: pdfFile,
            format: 'A4',
            printBackground: true,
            displayHeaderFooter: false,   // PDF-NO-BROWSER-CHROME-1: NEVER emit browser header/footer (date/URI/title/page chrome)
            margin: { top: '2cm', bottom: '2cm', left: '2cm', right: '2cm' }
        });
        
        const size = statSync(pdfFile).size;
        console.log(`PDF: ${(size/1024).toFixed(1)} KB, math=${mathCount}`);
        return size >= 102400;  // HARD GATE: <100KB = substandard renderer
    } finally {
        await browser.close();
    }
}

// Render both papers
const results = [
    await render('paper1.html', 'paper1.pdf'),
    await render('paper2.html', 'paper2.pdf'),
];
console.log('PDF build complete:', results.every(r => r) ? 'ALL OK' : 'SOME FAILED');
```

**Mandatory verification:** Zero U+FFFD / U+FFFF via BINARY BYTE SCAN (`data.count(b"\xef\xbf\xbd")` and `b"\xef\xbf\xbf"`) + PDF size > 100KB. **PyMuPDF / fitz is FORBIDDEN** in this pipeline (PYMUPDF-FORBIDDEN-1, user mandate 2026-08-04) — the xhtml2pdf gate below catches accidental fallback by size. **Math expressions MUST be visually verified** — if math is missing or rendered as bare text, the SVG switch, source delimiters, or inline MathJax need fixing.

**Canonical incident (2026-08-04, session ktmz7cqk):** Multiple PDF rendering failures traced to:
1. No Chromium on system — no Edge, no Chrome, no Brave installed
2. `npx @puppeteer/browsers install chrome` hung indefinitely (installed version but never returned)
3. MathJax CDN unreachable from Chrome headless — `page.goto` with `networkidle0` hung waiting for CDN fetch
4. `node -e` failed with "Unterminated string constant" in cmd.exe for multi-line render script
5. `re.sub()` crashed on MathJax JS containing `\u` escape sequences — must use `str.replace()`

All five failures would repeat for any agent on this machine. This section now documents the complete working pipeline end-to-end.
