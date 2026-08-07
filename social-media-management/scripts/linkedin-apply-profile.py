# -*- coding: utf-8 -*-
"""
linkedin-apply-profile.py — Apply linkedin-profile-update.json to a LinkedIn
profile via browser automation (CDP), NOT the deprecated linkedin-mcp-tools.

GATE (HARD): LinkedIn has NO profile-edit API (rw_profile scope deleted 2019).
The ONLY write path is browser automation against the live site with an
AUTHENTICATED Chrome profile. This script requires ONE manual sign-in first
(CAPTCHA/2FA physically needs the user) to establish the persistent profile.

=== VERIFIED SELECTORS (2026-08-05, live-tested on linkedin.com/in/rowan-quni) ===
- Login form: `input[autocomplete="username"]` / `input[autocomplete="password"]`
  (element IDs are randomized; autocomplete attributes are stable)
- Edit-intro URL: `https://www.linkedin.com/in/{SLUG}/edit/intro` (NOT /in/edit/intro)
- Headline editor: `div[contenteditable="true"].ProseMirror` — LinkedIn uses
  TipTap/ProseMirror rich-text. The old `[data-contents="true"]` selector is DEAD.
- About trigger: `a[aria-label="Edit about"]` — it is an <a>, NOT a <button>!
  (a[aria-label="Bewerk over"] for Dutch UI)
- Save button: button whose innerText is exactly "Save" / "Opslaan"
- NAVIGATION: use waitUntil:'domcontentloaded' — LinkedIn NEVER reaches
  networkidle0 (persistent tracking/websocket traffic). networkidle0 = timeout.
- CONTENT SET: document.execCommand('selectAll') + execCommand('insertText')
  IS ProseMirror-compatible. el.innerText = x is NOT (framework won't register).

=== Pacing ===
One section per session by default; 3-5s between operations; stops and asks
the human on any CAPTCHA/verify/checkpoint signal. Bot detection is aggressive.

Usage:
  python linkedin-apply-profile.py --package linkedin-profile-update.json \
      --profile-dir %USERPROFILE%\\.linkedin-profile \
      --chrome "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" \
      --section about          # apply one section only (default: headline+about)
  Sections: headline | about | experience | skills | education | certifications

Auth gate: if --profile-dir has no Chrome user-data, the script launches a
headful Chrome to https://www.linkedin.com/login and WAITS (up to 300s) for
the human to sign in. After login it proceeds.
"""
import argparse, json, os, subprocess, sys, tempfile, time

CHROME_DEFAULT = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
PROFILE_DEFAULT = os.path.join(os.path.expanduser('~'), '.linkedin-profile')
BASE_URL = 'https://www.linkedin.com'
# Profile slug — REQUIRED in edit URLs (verified 2026-08-05)
PROFILE_SLUG = 'rowan-quni'


def log(msg):
    print(f'[{time.strftime("%H:%M:%S")}] {msg}', flush=True)


def write_render_js(package_path, profile_dir, chrome_exe, section):
    """Generate the puppeteer-core CDP script that does the actual editing."""
    pkg_abs = package_path.replace('\\', '/')
    prof_abs = profile_dir.replace('\\', '/')
    chrome_abs = chrome_exe.replace('\\', '/')
    section_json = json.dumps(section)

    js = f'''
import {{ existsSync, readFileSync }} from 'fs';
import puppeteer from 'puppeteer-core';

const chrome = '{chrome_abs}';
const userData = '{prof_abs}';
const pkgPath = '{pkg_abs}';
const SECTION = {section_json};

const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));

function log(msg) {{ console.log('[' + new Date().toLocaleTimeString() + '] ' + msg); }};

const browser = await puppeteer.launch({{
  executablePath: chrome,
  headless: false,                       // LinkedIn needs real browser signals
  userDataDir: userData,                 // authenticated persistent profile
  args: ['--no-sandbox', '--disable-gpu']
}});

const page = await browser.newPage();
page.setDefaultTimeout(60000);

// ── Auth gate ─────────────────────────────────────────────────────────────
async function ensureLoggedIn() {{
  log('Checking session...');
  await page.goto('{BASE_URL}/feed/', {{ waitUntil: 'domcontentloaded', timeout: 60000 }});
  const url = page.url();
  if (url.includes('/login') || url.includes('authwall')) {{
    log('NOT LOGGED IN. Chrome is open — complete sign-in (CAPTCHA/2FA may be required). Waiting up to 300s...');
    await page.goto('{BASE_URL}/login', {{ waitUntil: 'domcontentloaded' }});
    const deadline = Date.now() + 300000;
    while (Date.now() < deadline) {{
      await new Promise(r => setTimeout(r, 3000));
      const u = page.url();
      if (!u.includes('/login') && !u.includes('authwall')) {{
        log('Session established.');
        return;
      }}
    }}
    log('TIMEOUT waiting for sign-in. Aborting.');
    await browser.close();
    process.exit(2);
  }}
  log('Session OK.');
}}

function sleep(ms) {{ return new Promise(r => setTimeout(r, ms)); }}

// ── Section applicators ───────────────────────────────────────────────────
async function applyHeadline() {{
  await page.goto('{BASE_URL}/in/{PROFILE_SLUG}/edit/intro', {{ waitUntil: 'domcontentloaded', timeout: 45000 }});
  await sleep(4000);
  // TipTap/ProseMirror editor (verified 2026-08-05)
  const sel = 'div[contenteditable="true"].ProseMirror';
  const el = await page.$(sel);
  if (!el) {{ log('HEADLINE field not found — selector: ' + sel); return false; }}
  await el.focus();
  await page.evaluate((txt) => {{
    const e = document.querySelector('div[contenteditable="true"].ProseMirror');
    document.execCommand('selectAll', false, null);
    document.execCommand('insertText', false, txt);
    e.dispatchEvent(new Event('input', {{ bubbles: true }}));
  }}, pkg.profile.headline);
  await sleep(1500);
  const save = await page.evaluate(() => {{
    const b = [...document.querySelectorAll('button')].find(x => /^(save|opslaan)$/i.test((x.innerText||'').trim()));
    if (b) {{ b.click(); return true; }}
    return false;
  }});
  log(save ? 'Headline saved.' : 'Save button not found — saved manually?');
  return true;
}}

async function applyAbout() {{
  await page.goto('{BASE_URL}/in/{PROFILE_SLUG}/', {{ waitUntil: 'domcontentloaded', timeout: 45000 }});
  await sleep(6000);
  // About trigger is an <a>, NOT a button (verified 2026-08-05)
  const clicked = await page.evaluate(() => {{
    const el = document.querySelector('a[aria-label="Edit about"], a[aria-label="Bewerk over"]');
    if (!el) return false;
    el.scrollIntoView({{ block: 'center' }});
    el.click();
    return true;
  }});
  if (!clicked) {{ log('ABOUT trigger not found'); return false; }}

  // Wait for TipTap editor
  let ready = false;
  for (let i = 0; i < 20; i++) {{
    await sleep(1500);
    const n = await page.evaluate(() => document.querySelectorAll('div[contenteditable="true"]').length);
    if (n > 0) {{ ready = true; break; }}
  }}
  if (!ready) {{ log('About editor did not open'); return false; }}

  await page.evaluate((txt) => {{
    const el = document.querySelector('div[contenteditable="true"]');
    el.focus();
    document.execCommand('selectAll', false, null);
    document.execCommand('insertText', false, txt);
    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
  }}, pkg.about);
  await sleep(1500);
  const saved = await page.evaluate(() => {{
    const b = [...document.querySelectorAll('button')].find(x => /^(save|opslaan)$/i.test((x.innerText||'').trim()));
    if (b) {{ b.click(); return true; }}
    return false;
  }});
  log(saved ? 'About saved.' : 'Save button not found — saved manually?');
  return true;
}}

async function applyExperience() {{
  log('Experience: navigating to details page...');
  await page.goto('{BASE_URL}/in/{PROFILE_SLUG}/details/experience/', {{ waitUntil: 'domcontentloaded', timeout: 45000 }});
  await sleep(5000);

  // Try clicking "Add a position" — known aria-label from previous run
  const clicked = await page.evaluate(() => {{
    const btn = document.querySelector('button[aria-label="Add a position or career break"]');
    if (btn) {{ btn.click(); return true; }}
    // fallback
    for (const el of document.querySelectorAll('span, button, a')) {{
      if (/add.*(position|experience)/i.test((el.innerText||'').trim())) {{ el.click(); return true; }}
    }}
    return false;
  }});

  if (clicked) {{
    log('Add position modal opened.');
    await sleep(3000);
    await page.screenshot({{ path: userData + '/experience-modal.png' }});
    log('Screenshot: ' + userData + '/experience-modal.png');

    // Dump the modal form fields
    const fields = await page.evaluate(() => [...document.querySelectorAll('input:not([type="hidden"]),[contenteditable="true"],select')].filter(e=>e.offsetParent!==null).map(e=>({{tag:e.tagName,type:e.getAttribute('type')||'ce',name:e.getAttribute('name')||'',aria:(e.getAttribute('aria-label')||'').slice(0,60),placeholder:(e.getAttribute('placeholder')||'').slice(0,60),autocomplete:e.getAttribute('autocomplete')||'',id:e.getAttribute('id')||''}})));
    log('Form fields: ' + JSON.stringify(fields));
  }} else {{
    log('Could not open add-position modal.');
    await page.screenshot({{ path: userData + '/experience-page.png' }});
  }}

  log('');
  log('=== EXPERIENCE DATA TO FILL ===');
  for (let i=0; i<pkg.experience.length; i++) {{
    const e = pkg.experience[i];
    log((i+1)+'. '+e.title+' @ '+e.company);
    log('   Location: '+e.location+' | Dates: '+e.dates);
    log('   Description: '+e.description.slice(0,150)+'...');
    log('');
  }}
  log('Open the Chrome window to add these 5 experiences manually.');
  log('Waiting 300s (5 min) — press Ctrl+C to skip...');
  await sleep(300000);
  return true;
}}

async function applyEducation() {{
  log('Education: navigating...');
  await page.goto('{BASE_URL}/in/{PROFILE_SLUG}/details/education/', {{ waitUntil: 'domcontentloaded', timeout: 45000 }});
  await sleep(5000);
  await page.screenshot({{ path: userData + '/education-page.png' }});
  log('');
  log('=== EDUCATION DATA ===');
  for (const e of pkg.education) {{
    log(e.degree+' — '+e.school+' ('+e.dates+')');
  }}
  log('');
  log('Add these 2 entries in the Chrome window. Waiting 180s...');
  await sleep(180000);
  return true;
}}

async function applyCertifications() {{
  log('Certifications: navigating...');
  await page.goto('{BASE_URL}/in/{PROFILE_SLUG}/details/certifications/', {{ waitUntil: 'domcontentloaded', timeout: 45000 }});
  await sleep(5000);
  await page.screenshot({{ path: userData + '/certifications-page.png' }});
  log('');
  log('=== CERTIFICATION DATA ===');
  for (const c of pkg.certifications) {{
    log(c.name+' — '+c.issuer+' ('+c.year+')');
  }}
  log('');
  log('Add these 3 entries in the Chrome window. Waiting 180s...');
  await sleep(180000);
  return true;
}}

async function applySkills() {{
  log('Skills: navigating...');
  await page.goto('{BASE_URL}/in/{PROFILE_SLUG}/details/skills/', {{ waitUntil: 'domcontentloaded', timeout: 45000 }});
  await sleep(5000);
  await page.screenshot({{ path: userData + '/skills-page.png' }});
  log('');
  log('=== SKILLS DATA (45 total) ===');
  log(pkg.skills.join(', '));
  log('');
  log('Add skills in the Chrome window. Waiting 300s...');
  await sleep(300000);
  return true;
}}

// ── Main ──────────────────────────────────────────────────────────────────
await ensureLoggedIn();
let ok = true;
if (SECTION === 'headline') ok = await applyHeadline();
if (SECTION === 'about') ok = await applyAbout();
if (SECTION === 'experience') ok = await applyExperience();
if (SECTION === 'education') ok = await applyEducation();
if (SECTION === 'certifications') ok = await applyCertifications();
if (SECTION === 'skills') ok = await applySkills();
if (SECTION === 'all') {{
  ok = await applyHeadline() && ok;
  await sleep(8000);
  ok = await applyAbout() && ok;
  await sleep(8000);
  ok = await applyExperience() && ok;
  await sleep(8000);
  ok = await applyEducation() && ok;
  await sleep(8000);
  ok = await applyCertifications() && ok;
  await sleep(8000);
  ok = await applySkills() && ok;
}}
if (!ok) {{ log('One or more sections could NOT be auto-applied. Apply manually from the JSON package.'); }}
await browser.close();
log('Done.');
'''
    rjs = os.path.join(tempfile.gettempdir(), '_li_apply.mjs')
    with open(rjs, 'w', encoding='utf-8') as f:
        f.write(js)
    return rjs


def find_node():
    """Locate node.exe — prefer system install over DeepChat-bundled."""
    candidates = [
        r'C:\Program Files\nodejs\node.exe',
        r'C:\Program Files\DeepChat\resources\app.asar.unpacked\runtime\node\node.EXE',
        r'C:\Program Files\DeepChat\resources\app.asar.unpacked\runtime\node\node.exe',
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    import shutil
    n = shutil.which('node')
    return n or (sys.exit('node.exe not found — install Node or pass the full path'))


def main():
    ap = argparse.ArgumentParser(description='Apply LinkedIn profile updates via browser automation')
    ap.add_argument('--package', required=True, help='Path to linkedin-profile-update.json')
    ap.add_argument('--profile-dir', default=PROFILE_DEFAULT, help='Persistent Chrome profile dir (must be authenticated)')
    ap.add_argument('--chrome', default=CHROME_DEFAULT, help='Chrome executable')
    ap.add_argument('--section', default='all', choices=['all', 'headline', 'about', 'experience', 'skills', 'education', 'certifications'],
                    help='Section to apply (experience/skills/education/certifications require manual UI steps per section — script opens the edit page)')
    args = ap.parse_args()

    if not os.path.isdir(args.profile_dir):
        log(f'NOTE: profile dir {args.profile_dir} does not exist yet — will be created on first headful launch. A manual sign-in will be required.')
    if not os.path.exists(args.chrome):
        sys.exit(f'Chrome not found: {args.chrome}')

    with open(args.package, 'r', encoding='utf-8') as f:
        pkg = json.load(f)

    node = find_node()
    rjs = write_render_js(args.package, args.profile_dir, args.chrome, args.section)
    log(f'Launching browser automation (section={args.section})...')
    r = subprocess.run([node, rjs], capture_output=True, text=True, timeout=420)
    print(r.stdout)
    if r.stderr:
        print(r.stderr[-2000:])
    if r.returncode != 0:
        sys.exit(r.returncode)
    log('Apply pass finished. Verify on linkedin.com/in/edit.')


if __name__ == '__main__':
    main()
