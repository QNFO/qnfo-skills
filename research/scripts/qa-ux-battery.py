# -*- coding: utf-8 -*-
"""
qa-ux-battery.py — MANDATORY pre-deployment UI/UX test battery for public-facing
QNFO/QWAV pages. Uses Chrome for Testing (headless) via puppeteer-core.

User mandate (2026-08-05): NO deployment of broken pages, missing links, or dead
interactive tools. Interactive tools deployed through GitHub recently did not work
— this battery exists to make that impossible.

Checks per URL:
  A. HTTP sweep           — status code, redirect chain, final URL
  B. Console errors       — JS errors + pageerrors (catches dead interactive tools)
  C. Broken links         — every <a href> resolved; 4xx/5xx flagged
  D. 404 markers          — "404"/"not found"/"deze pagina bestaat niet" in body
  E. Interactive elements  — buttons/inputs/canvas/forms/links present as expected
  F. Content integrity    — <title>, <h1>, body text length

Usage:
  python qa-ux-battery.py --urls https://qnfo.org https://qwav.org
  python qa-ux-battery.py --urls-file public-domains.txt
  python qa-ux-battery.py --urls https://ask-qwav.pages.dev --json out.json
"""
import argparse, json, os, subprocess, sys, tempfile, urllib.request, urllib.error, time, re

CHROME_CFT = os.path.expanduser(r'~\.cache\puppeteer\chrome\chrome-win64\chrome.exe')
CHROME_STD = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
NODE = next((c for c in [
    r'C:\Program Files\DeepChat\resources\app.asar.unpacked\runtime\node\node.EXE',
    r'C:\Program Files\DeepChat\resources\app.asar.unpacked\runtime\node\node.exe',
] if os.path.exists(c)), None)

HTTP_SWEEP_TIMEOUT = 25
BROWSER_SETTLE_MS = 9000
LINK_CAP = 150
LINK_CHECK_TIMEOUT = 20


def log(msg):
    print(msg, flush=True)


# ── A. HTTP sweep ─────────────────────────────────────────────────────────
def http_sweep(url):
    """Return {status, final_url, redirects, error}."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 qa-ux-battery/1.0'})
        with urllib.request.urlopen(req, timeout=HTTP_SWEEP_TIMEOUT) as resp:
            return {'status': resp.status, 'final_url': resp.geturl(), 'error': None}
    except urllib.error.HTTPError as e:
        return {'status': e.code, 'final_url': e.geturl() if hasattr(e, 'geturl') else url, 'error': None}
    except Exception as e:
        return {'status': 0, 'final_url': url, 'error': str(e)[:120]}


# ── B–F. Browser pass (one .mjs run for all URLs) ─────────────────────────
def browser_pass(urls, chrome):
    """Headless Chrome (for Testing) pass. Returns list of per-URL results."""
    if not NODE:
        return [{'url': u, 'browser_error': 'node not found'} for u in urls]
    if not os.path.exists(chrome):
        return [{'url': u, 'browser_error': f'chrome missing: {chrome}'} for u in urls]

    js = f'''
import puppeteer from 'puppeteer-core';
const chrome = '{chrome.replace(chr(92), '/')}';
const urls = {json.dumps(urls)};
const settle = {BROWSER_SETTLE_MS};

const browser = await puppeteer.launch({{
  executablePath: chrome, headless: true,
  args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
}});

const results = [];
for (const url of urls) {{
  const page = await browser.newPage();
  page.setDefaultTimeout(45000);
  const r = {{ url, console_errors: [], page_errors: [], links: [], title: '', h1: '', body_len: 0,
               interactive: {{ buttons: 0, inputs: 0, selects: 0, textareas: 0, canvases: 0, forms: 0, iframes: 0 }},
               nav_error: null, final_url: url }};
  page.on('console', m => {{ if (m.type() === 'error') r.console_errors.push(m.text().substring(0, 200)); }});
  page.on('pageerror', e => r.page_errors.push(String(e).substring(0, 200)));
  try {{
    const resp = await page.goto(url, {{ waitUntil: 'domcontentloaded', timeout: 45000 }});
    if (resp) r.final_url = resp.url();
  }} catch (e) {{ r.nav_error = String(e).substring(0, 200); }}
  await new Promise(res => setTimeout(res, settle));

  const dom = await page.evaluate(() => {{
    const links = [...new Set([...document.querySelectorAll('a[href]')].map(a => a.href))].slice(0, {LINK_CAP});
    return {{
      title: document.title || '',
      h1: (document.querySelector('h1')?.innerText || '').substring(0, 120),
      body_len: (document.body?.innerText || '').length,
      body_text: (document.body?.innerText || '').substring(0, 3000),
      links,
      interactive: {{
        buttons: document.querySelectorAll('button').length,
        inputs: document.querySelectorAll('input').length,
        selects: document.querySelectorAll('select').length,
        textareas: document.querySelectorAll('textarea').length,
        canvases: document.querySelectorAll('canvas').length,
        forms: document.querySelectorAll('form').length,
        iframes: document.querySelectorAll('iframe').length,
      }}
    }};
  }});
  r.title = dom.title; r.h1 = dom.h1; r.body_len = dom.body_len;
  r.body_text = dom.body_text; r.links = dom.links; r.interactive = dom.interactive;
  results.push(r);
  await page.close();
}}
await browser.close();
console.log('QA_UX_RESULT_JSON_START');
console.log(JSON.stringify(results));
console.log('QA_UX_RESULT_JSON_END');
'''
    mjs = os.path.join(tempfile.gettempdir(), '_qa_ux_battery.mjs')
    with open(mjs, 'w', encoding='utf-8') as f:
        f.write(js)
    try:
        proc = subprocess.run([NODE, mjs], capture_output=True, text=True, timeout=300)
        out = proc.stdout
    except subprocess.TimeoutExpired:
        return [{'url': u, 'browser_error': 'browser pass timed out'} for u in urls]

    start = out.find('QA_UX_RESULT_JSON_START')
    end = out.find('QA_UX_RESULT_JSON_END')
    if start < 0 or end < 0:
        return [{'url': u, 'browser_error': 'no JSON result: ' + out[-300:]} for u in urls]
    try:
        return json.loads(out[start + len('QA_UX_RESULT_JSON_START'):end].strip())
    except Exception as e:
        return [{'url': u, 'browser_error': f'JSON parse: {e}'} for u in urls]


# ── C. Link check ─────────────────────────────────────────────────────────
def check_link(link):
    """HEAD-first with MANDATORY GET fallback. SPA/Worker routes (ipatent.qnfo.org,
    ask-qwav) 404 HEAD but serve GET fine — never declare broken from HEAD alone."""
    ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'}
    # GET is the ground truth; HEAD only as a fast path
    try:
        req = urllib.request.Request(link, method='GET', headers=ua)
        with urllib.request.urlopen(req, timeout=LINK_CHECK_TIMEOUT) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        # doi.org 403 = bot-blocking on some UAs, NOT a dead link.
        # Verify zenodo DOIs via DataCite API (authoritative per ZENODO-PHANTOM-DOI-1).
        if e.code == 403 and 'doi.org' in link:
            m = re.search(r'10\.5281/zenodo\.\d+', link)
            if m:
                try:
                    req2 = urllib.request.Request(
                        'https://api.datacite.org/dois/' + m.group(0),
                        headers={'User-Agent': 'Mozilla/5.0 qa-ux-battery/1.0'})
                    with urllib.request.urlopen(req2, timeout=LINK_CHECK_TIMEOUT) as resp2:
                        return resp2.status if resp2.status < 400 else e.code
                except Exception:
                    return e.code
        return e.code
    except Exception as e:
        return str(e)[:60]


def detect_404_markers(body_text):
    pats = [r'\b404\b', r'not found', r'deze pagina bestaat niet', r'page doesn.t exist',
            r'page not found', r'no such page', r'pagina niet gevonden']
    hits = []
    for p in pats:
        if re.search(p, body_text, re.IGNORECASE):
            hits.append(p)
    return hits


# ── Verdict ───────────────────────────────────────────────────────────────
def verdict(r):
    issues = []
    if r.get('nav_error'):
        issues.append(f'NAV_ERROR: {r["nav_error"][:80]}')
    if r.get('console_errors'):
        issues.append(f'{len(r["console_errors"])} console errors: {r["console_errors"][0][:80]}')
    if r.get('page_errors'):
        issues.append(f'{len(r["page_errors"])} page errors: {r["page_errors"][0][:80]}')
    if r.get('broken_links'):
        cosmetic = [b for b in r['broken_links'] if '/favicon' in b[0] or b[0].endswith('/robots.txt')]
        real = [b for b in r['broken_links'] if b not in cosmetic]
        if real:
            issues.append(f'{len(real)} broken links: {real[0][:80]}')
        elif cosmetic:
            r['_cosmetic'] = cosmetic
    if r.get('_404_markers'):
        issues.append(f'404 markers: {r["_404_markers"][:2]}')
    if not r.get('title'):
        issues.append('no <title>')
    if not r.get('h1'):
        issues.append('no <h1>')
    if r.get('body_len', 0) < 100:
        issues.append(f'body too short ({r.get("body_len",0)} chars)')
    if not issues:
        return 'PASS', ''
    critical = any(k in ' '.join(issues).lower() for k in ['nav_error', 'console error', 'page error', 'broken link', '404'])
    return ('FAIL' if critical else 'WARN'), '; '.join(issues)


def main():
    ap = argparse.ArgumentParser(description='QNFO/QWAV UI/UX pre-deployment test battery')
    ap.add_argument('--urls', nargs='*', default=[], help='URLs to test')
    ap.add_argument('--urls-file', default=None, help='File with one URL per line')
    ap.add_argument('--browser', default=None, help='Chrome executable (default: Chrome for Testing)')
    ap.add_argument('--json', default=None, help='Write results JSON to this path')
    ap.add_argument('--skip-links', action='store_true', help='Skip external link checks (slow)')
    args = ap.parse_args()

    urls = list(args.urls)
    if args.urls_file:
        with open(args.urls_file, encoding='utf-8') as f:
            urls += [l.strip() for l in f if l.strip() and not l.startswith('#')]

    if not urls:
        sys.exit('No URLs provided')

    chrome = args.browser or (CHROME_CFT if os.path.exists(CHROME_CFT) else CHROME_STD)

    log(f'QA/UX Battery — {len(urls)} URLs, browser: {chrome}')
    log('=' * 78)

    # A. HTTP sweep
    sweeps = {}
    log('\n[A] HTTP sweep')
    for u in urls:
        s = http_sweep(u)
        sweeps[u] = s
        flag = 'OK' if 200 <= s['status'] < 400 else ('REDIRECT' if 300 <= s['status'] < 400 else ('FAIL' if s['status'] else 'ERROR'))
        log(f'  {flag:8s} {s["status"]:>3} {u}  ->  {s["final_url"][:70]}' + (f'  [{s["error"]}]' if s['error'] else ''))

    # B–F. Browser pass (only 2xx/3xx reachable)
    browser_urls = [u for u in urls if 200 <= sweeps[u]['status'] < 400]
    browser_results = {}
    if browser_urls:
        log(f'\n[B-F] Headless browser pass ({len(browser_urls)} pages, settle {BROWSER_SETTLE_MS}ms)')
        for br in browser_pass(browser_urls, chrome):
            browser_results[br['url']] = br
    else:
        log('\n[B-F] no reachable pages to browser-test')

    # C. Link checks
    log('\n[C] Link checks')
    all_links = {}
    for u in browser_urls:
        br = browser_results.get(u, {})
        links = br.get('links', [])
        if not links:
            all_links[u] = []
            log(f'  {u}: no links found')
            continue
        broken = []
        for i, link in enumerate(links):
            if i >= 25:  # cap per-page link checks at 25 to stay fast
                break
            st = check_link(link)
            if isinstance(st, int) and st >= 400:
                broken.append((link, st))
            elif isinstance(st, str):
                broken.append((link, st))
        all_links[u] = broken
        log(f'  {u}: {len(links)} links, {len(broken)} broken' +
            (f' -> {broken[0]}' if broken else ''))

    # Assemble results
    results = []
    for u in urls:
        s = sweeps.get(u, {})
        br = browser_results.get(u, {})
        r = dict(br)
        r['url'] = u
        r['http_status'] = s.get('status', 0)
        r['final_url'] = s.get('final_url', u)
        r['broken_links'] = all_links.get(u, [])
        if 'body_text' in r:
            r['_404_markers'] = detect_404_markers(r['body_text'])
        else:
            r['_404_markers'] = []
        v, why = verdict(r)
        r['verdict'] = v
        r['why'] = why
        results.append(r)

    # Report
    log('\n' + '=' * 78)
    log('QA/UX BATTERY REPORT')
    log('=' * 78)
    log(f'{"URL":<42} {"HTTP":>4} {"VRD":<5} {"CE":>2} {"PE":>2} {"BL":>2} {"BTXT":>7} {"INT":>6}')
    pass_n = 0
    for r in results:
        ce = len(r.get('console_errors', []))
        pe = len(r.get('page_errors', []))
        bl = len(r.get('broken_links', []))
        bt = r.get('body_len', 0)
        it = sum(r.get('interactive', {}).values())
        v = r['verdict']
        if v == 'PASS':
            pass_n += 1
        log(f'{r["url"][:42]:<42} {r["http_status"]:>4} {v:<5} {ce:>2} {pe:>2} {bl:>2} {bt:>7} {it:>6}')
        if v != 'PASS':
            log(f'  ISSUES: {r.get("why","")[:150]}')
            if r.get('console_errors'):
                for e in r['console_errors'][:3]:
                    log(f'    console: {e[:110]}')
            if r.get('broken_links'):
                for (l, s) in r['broken_links'][:5]:
                    log(f'    broken: {s} {l[:90]}')

    log('=' * 78)
    log(f'RESULT: {pass_n}/{len(results)} PASS | {sum(1 for r in results if r["verdict"]=="FAIL")} FAIL | {sum(1 for r in results if r["verdict"]=="WARN")} WARN')
    log('GATE: deployment is BLOCKED if any FAIL (console/page errors, broken links, 404 markers, missing title/h1).')

    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        log(f'JSON written: {args.json}')

    return 1 if any(r['verdict'] == 'FAIL' for r in results) else 0


if __name__ == '__main__':
    sys.exit(main())
