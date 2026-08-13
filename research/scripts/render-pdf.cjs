// CDP PDF render — CANONICAL, permanent install.
// Location: C:\Users\LENOVO\.deepchat\cdp-pipeline\render-pdf.cjs (NEVER %TEMP%).
// Working process per user mandate: cached Chrome for Testing FIRST (NO Edge).
// CommonJS (.cjs) per NODE-MJS-ESM-1. path: IS REQUIRED (PDF-PATH-OPTION-1).
//
// Usage: node render-pdf.cjs <input.html> <output.pdf>
//
// The MathJax MUST already be inlined into the HTML (run inline-mathjax.py first
// or build-pdf.py). CDN is unreachable from headless Chrome on this machine.
const puppeteer = require('C:/Users/LENOVO/node_modules/puppeteer-core');
const { existsSync, statSync, readdirSync } = require('fs');
const os = require('os');

const HTML = process.argv[2];
const OUT = process.argv[3];

if (!HTML || !OUT) {
  console.error('Usage: node render-pdf.cjs <input.html> <output.pdf>');
  process.exit(2);
}

function findChrome() {
  const candidates = [];
  // 1. Cached Chrome for Testing (user mandate: reuse; the working process excludes Edge)
  candidates.push(os.homedir() + '/.cache/puppeteer/chrome/chrome-win64/chrome.exe');
  // 2. Permanent CfT copy (if ever moved here)
  candidates.push(os.homedir() + '/.deepchat/cdp-pipeline/chrome/chrome-win64/chrome.exe');
  // 3. Playwright chromium (discover via readdirSync)
  const pwRoot = os.homedir() + '/AppData/Local/ms-playwright';
  try {
    const dirs = readdirSync(pwRoot);
    const versions = dirs.filter(d => d.startsWith('chromium-'));
    for (const v of versions.sort()) {
      candidates.push(pwRoot + '/' + v + '/chrome-win64/chrome.exe');
    }
  } catch (e) { /* no playwright */ }
  // 4. Google Chrome (not Edge)
  candidates.push('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe');
  candidates.push('C:/Program Files/Google/Chrome/Application/chrome.exe');
  for (const c of candidates) { if (existsSync(c)) return c; }
  throw new Error('No Chromium found (CfT/Playwright/Chrome all missing)');
}

(async () => {
  const chromeExe = findChrome();
  console.log('CHROME-EXE:', chromeExe);
  const browser = await puppeteer.launch({
    executablePath: chromeExe,
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
  });
  try {
    const page = await browser.newPage();
    const fileUrl = 'file:///' + HTML.replace(/\\/g, '/');
    await page.goto(fileUrl, { waitUntil: 'load', timeout: 120000 });

    let mathCount = 0;
    try {
      await page.evaluate(() => window.MathJax.startup.promise);
      mathCount = await page.evaluate(() =>
        document.querySelectorAll('mjx-container, .MathJax, mjx-assistive-mml').length
      );
    } catch (e) {
      console.log('MathJax warn:', String(e).substring(0, 150));
    }
    console.log('MATH-COUNT:', mathCount);

    await new Promise(r => setTimeout(r, 3000));
    await page.pdf({
      path: OUT,
      format: 'A4',
      printBackground: true,
      margin: { top: '2cm', bottom: '2cm', left: '2cm', right: '2cm' }
    });
    const size = statSync(OUT).size;
    console.log('PDF-OK:', OUT, (size / 1024).toFixed(1), 'KB, math=' + mathCount);
    console.log('GATE:', size >= 102400 ? 'PASS >=100KB' : 'FAIL <100KB');
    process.exit(size >= 102400 ? 0 : 3);
  } finally {
    await browser.close();
  }
})().catch(e => { console.error('PDF-ERR', e); process.exit(1); });
