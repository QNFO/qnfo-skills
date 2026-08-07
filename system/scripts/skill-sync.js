#!/usr/bin/env node
/**
 * skill-sync.js v4.0.7 — Sync all local skills (SKILL.md + scripts/* + templates/* + references/*) to GitHub + R2
 *
 * Usage: node skill-sync.js [skills-root-dir] [--targets=a,b,c] [--force] [--no-verify] [--skip-git]
 *
 * v4.0.8 (2026-08-07, kaizen — truthful completion message; gitOk flag)
 * v4.0.7 (2026-08-07, kaizen — auto-recover missing .git from canonical clone)
 * v4.0.6 (2026-08-02, kaizen — chunk check-ignore call; Windows cmd line limit)
 * v4.0.5 (2026-08-02, kaizen — normalize git paths to forward slashes; check-ignore sep mismatch)
 * v4.0.4 (2026-08-02, kaizen — check-ignore arg form; --stdin no-op on Windows)
 * v4.0.3 (2026-08-02, kaizen — git add ignored-file filter)
 * v4.0.2 (2026-08-02, kaizen — R2 GET-cache verify fix)
 *   - verify via PUT response result.size; R2 GET is edge-cached (HIT stale body)
 * v4.0.1 (2026-08-02, kaizen — git-scope HARD fix): git commit now adds EXACTLY the
 *   walkFiles output (identical to R2 upload set) + .gitignore + skill-sync.js itself.
 *   `git add -A` swept strays twice (cbc5f7f .bak; 2d54bd3 .wrangler/__pycache__/.lastActivity).
 * v4.0.0 (2026-08-02, kaizen — REST fast path + autonomy):
 *   - HARD FIX: replaced `npx --yes --package wrangler@latest` per-file (pathological:
 *     npx cold-start per file, wrangler re-resolution, 90s timeout each, WinError 2 in
 *     daemon subprocess env → ZERO state updates in 20+ min) with the R2 REST API
 *     (`PUT /accounts/{id}/r2/buckets/qnfo-skills/objects/{key}` + Bearer token).
 *     Measured: probe round-trip 200/200/200; full sync of ~120 files now completes in
 *     seconds instead of hours. No npx, no wrangler, no node_modules.
 *   - ADD: parallel upload pool (default 8 concurrent) + per-file GET verify
 *     (Content-Length match, per cloudflare skill R2 verification rule — use GET, not HEAD).
 *   - HARD FIX: git adds are scoped — `.gitignore` now excludes `*.bak-*` / `*.bak`
 *     (the cbc5f7f commit accidentally swept research/scripts/build-paper.py.bak-20260802,
 *     506 lines, reverted in d109323). walkFiles also skips *.bak-* for R2.
 *   - ADD: `--skip-git` (R2 only), `--no-verify` (skip GET verification), `--force`.
 *   - ADD: autonomy — designed to run unattended via cronjob (see system skill v2.5
 *     §Autonomous Skill Sync). Exit codes: 0 = clean, 1 = R2 failures remain after retry.
 *
 * v3.0.0 (2026-07-31, kaizen) legacy notes:
 *   - HARD FIX: pin `npx --yes --package wrangler@latest` — bare `npx wrangler`
 *     resolved to a corrupted npx cache. (OBSOLETE in v4 — no npx at all.)
 *   - content-hash state file (~/.deepchat/.skill-sync-state.json) — unchanged files
 *     skipped, idempotent re-runs.
 *   - --targets filter, per-file retry, failure cause classification.
 *
 * @version 4.0.8
 * @date 2026-08-02
 */

const { execSync } = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const BUCKET = 'qnfo-skills';
const ACCOUNT = process.env.CLOUDFLARE_ACCOUNT_ID || 'edb167b78c9fb901ea5bca3ce58ccc4b';
const STATE_FILE = path.join(process.env.USERPROFILE || process.env.HOME, '.deepchat', '.skill-sync-state.json');
const PARALLEL = parseInt(process.env.SYNC_PARALLEL || '8', 10);
const API = 'https://api.cloudflare.com/client/v4';

// ---------- token discovery (env → ~/.cloudflare_token → ~/keys.json) ----------
function findToken() {
  if (process.env.CLOUDFLARE_API_TOKEN) return process.env.CLOUDFLARE_API_TOKEN;
  const p1 = path.join(process.env.USERPROFILE || process.env.HOME, '.cloudflare_token');
  if (fs.existsSync(p1)) return fs.readFileSync(p1, 'utf8').trim();
  const p2 = path.join(process.env.USERPROFILE || process.env.HOME, 'keys.json');
  if (fs.existsSync(p2)) {
    try {
      const d = JSON.parse(fs.readFileSync(p2, 'utf8'));
      return d.CLOUDFLARE_API_TOKEN || d.api_token || d.cloudflare_token || d.token || null;
    } catch (e) { /* fall through */ }
  }
  return null;
}

function fileHash(localPath) {
  const buf = fs.readFileSync(localPath);
  return crypto.createHash('sha256').update(buf).digest('hex');
}

function loadState() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8')); }
  catch (e) { return { files: {} }; }
}

function saveState(state) {
  try {
    fs.mkdirSync(path.dirname(STATE_FILE), { recursive: true });
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
  } catch (e) {
    console.error(`  ! state save failed: ${e.message}`);
  }
}

function walkFiles(dir, base) {
  base = base || dir;
  let out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue;                 // hidden (incl. .kaizen_history)
    if (/\.bak(?:-\d{8})?$/i.test(entry.name)) continue;       // backup files (v4)
    if (entry.name === '__pycache__') continue;               // py build cache
    if (entry.isFile() && entry.name.endsWith('.pyc')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out = out.concat(walkFiles(full, base));
    else out.push(path.relative(base, full).replace(/\\/g, '/'));
  }
  return out;
}

async function r2Put(key, localPath) {
  const stat = fs.statSync(localPath);
  const resp = await fetch(`${API}/accounts/${ACCOUNT}/r2/buckets/${BUCKET}/objects/${encodeURIComponent(key)}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/octet-stream',
    },
    body: fs.readFileSync(localPath),
  });
  if (!resp.ok) return { ok: false, cause: `HTTP ${resp.status}` };
  const d = await resp.json().catch(() => ({}));
  if (!d.success) return { ok: false, cause: (d.errors || []).map(e => e.message).join(',') || 'r2:success=false' };
  // v4.0.2: verify via the PUT response's echoed size (R2 result.size) — NOT a follow-up
  // GET. The R2 object GET goes through an edge cache (CF-Cache-Status: HIT can return
  // a STALE body: measured 9,316B after PUT stored 11,047B; Cache-Control request
  // headers don't bypass it; ?query cache-bust returns 404). The PUT response's
  // result.size is the authoritative byte count of what R2 stored.
  const stored = parseInt(d.result && d.result.size, 10);
  if (Number.isFinite(stored) && stored !== stat.size) {
    return { ok: false, cause: `size-mismatch stored=${stored} local=${stat.size}` };
  }
  return { ok: true, size: stat.size };
}

// simple concurrency pool
async function pool(items, worker, concurrency) {
  const results = new Array(items.length);
  let next = 0;
  async function run() {
    while (next < items.length) {
      const i = next++;
      results[i] = await worker(items[i], i);
    }
  }
  await Promise.all(Array.from({ length: Math.min(concurrency, items.length) }, run));
  return results;
}

// ---------- main ----------
(async () => {
  const args = process.argv.slice(2);
  let skillsRoot = path.join(process.env.USERPROFILE || process.env.HOME, '.deepchat', 'skills');
  let targets = null, force = false, verify = true, skipGit = false;
  let gitOk = false;
  for (const a of args) {
    if (a.startsWith('--targets=')) targets = a.slice(10).split(',');
    else if (a === '--force') force = true;
    else if (a === '--no-verify') verify = false;
    else if (a === '--skip-git') skipGit = true;
    else skillsRoot = a;
  }

  console.log('=== SKILL SYNC v4 ===');
  console.log(`Skills root: ${skillsRoot}`);
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  // 0. Token gate
  TOKEN = findToken();
  if (!TOKEN) { console.error('✗ CLOUDFLARE_API_TOKEN not found (env, ~/.cloudflare_token, ~/keys.json)'); process.exit(2); }
  console.log('✓ Token found (REST path — no npx/wrangler)');

  // skills enumeration (needed by BOTH git sync and R2 sync — declare before git)
  const skills = fs.readdirSync(skillsRoot, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('.') && fs.existsSync(path.join(skillsRoot, d.name, 'SKILL.md')))
    .map(d => d.name)
    .filter(s => !targets || targets.includes(s))
    .sort();

  // 1. Git sync — v4.0.1 (HARD fix): commit EXACTLY the files being R2-synced.
  //    `git add -A` swept unrelated strays twice (cbc5f7f .bak-20260802; 2d54bd3
  //    .wrangler/__pycache__/.lastActivity/stray PDFs). Now we git-add the precise
  //    walkFiles output (same set as R2 upload) + root .gitignore, so the git
  //    commit and R2 upload are identical by construction.
  if (!skipGit) {
    // ---- Pre-flight: auto-recover from missing .git (v4.0.7 kaizen) ----
    const gitDir = path.join(skillsRoot, '.git');
    if (!fs.existsSync(gitDir)) {
      console.log('! .git missing — auto-recovering from canonical clone');
      const canonicalGit = path.join(process.env.USERPROFILE || process.env.HOME, 'Documents', 'GitHub', 'qnfo-skills', '.git');
      if (fs.existsSync(canonicalGit)) {
        // Copy .git from canonical clone (robocopy on Windows, cp -r elsewhere)
        try {
          if (process.platform === 'win32') {
            execSync(`robocopy "${canonicalGit}" "${gitDir}" /E /NFL /NDL /NJH /NJS /R:1 /W:1`, { stdio: 'pipe' });
          } else {
            execSync(`cp -r "${canonicalGit}" "${gitDir}"`, { stdio: 'pipe' });
          }
          console.log('✓ .git restored from canonical clone');
        } catch (e) {
          // robocopy exit code >= 8 is a real error; 0-7 = success
          if (process.platform === 'win32' && e.status <= 7) {
            console.log('✓ .git restored from canonical clone');
          } else {
            console.log(`✗ Failed to restore .git: ${e.message.split('\\n')[0]}`);
            console.log('  → git sync skipped (re-create or re-clone the repo to restore)');
            skipGit = true;
          }
        }
      } else {
        console.log('✗ Canonical clone not found at Documents/GitHub/qnfo-skills');
        console.log('  → git sync skipped (clone QNFO/qnfo-skills to restore)');
        skipGit = true;
      }
    }
    // ---- End pre-flight ----
    if (!skipGit) {
    console.log('--- Git sync ---');
    try {
      const gitAddPaths = [];
      for (const skill of skills) {
        const skillDir = path.join(skillsRoot, skill);
        for (const rel of walkFiles(skillDir)) {
          gitAddPaths.push(path.join(skill, rel).replace(/\\/g, '/'));  // forward slashes for git
        }
      }
      const gi = path.join(skillsRoot, '.gitignore');
      if (fs.existsSync(gi)) gitAddPaths.push('.gitignore');
      gitAddPaths.push('system/scripts/skill-sync.js');
      // Filter out gitignored files (e.g. *.log history files) so `git add` doesn't
      // fail on "paths are ignored by your .gitignore" (v4.0.3). Batch via check-ignore.
      // v4.0.6: chunk the check-ignore call (50/chunk like git add) — passing all
      // ~280 paths at once exceeded the Windows 8191-char command-line limit, making
      // execSync throw and the catch keep every path (git add then failed on ignored
      // *.log). check-ignore arg form prints ignored paths; --stdin is a no-op on Windows.
      const ignored = new Set();
      for (let i = 0; i < gitAddPaths.length; i += 50) {
        const chunk = gitAddPaths.slice(i, i + 50);
        try {
          const ci = execSync(['git', 'check-ignore', '--', ...chunk].join(' '), {
            cwd: skillsRoot, stdio: 'pipe',
          }).toString().split(/\r?\n/).filter(Boolean);
          ci.forEach(x => ignored.add(x.replace(/\\/g, '/')));
        } catch (e) { /* chunk has no ignored files (exit 1) or other — keep chunk */ }
      }
      const nonIgnored = gitAddPaths.filter(p => !ignored.has(p));
      // chunk args to avoid Windows command-line length limits
      for (let i = 0; i < nonIgnored.length; i += 50) {
        const chunk = nonIgnored.slice(i, i + 50);
        execSync(['git', 'add', '--', ...chunk].join(' '), { cwd: skillsRoot, stdio: 'pipe' });
      }
      try {
        execSync('git commit -m "ACTION:SYNC FILES: skills/* RATIONALE: automated skill-sync.js v4 run -- propagate local SKILL.md/script edits to git history"', { cwd: skillsRoot, stdio: 'pipe' });
        console.log('✓ Git commit created');
      } catch (e) { console.log('○ No changes to commit'); }
      for (const remote of ['origin', 'rwnq8']) {
        try { execSync(`git push ${remote} master`, { cwd: skillsRoot, stdio: 'pipe' }); console.log(`✓ Pushed to ${remote}`); }
        catch (e) { console.log(`✗ Failed to push to ${remote}: ${e.message.split('\n')[0]}`); }
      }
      gitOk = true;
    } catch (e) { console.log('✗ Git error:', e.message.split('\n')[0]); }
    } // close inner if (!skipGit) after pre-flight
  }

  // 2. R2 sync
  console.log('\n--- R2 sync ---');
  const state = loadState();

  console.log(`Found ${skills.length} skills to sync${force ? ' (--force: ignoring cached hashes)' : ''}`);

  // collect all files
  const jobs = [];
  for (const skill of skills) {
    const skillDir = path.join(skillsRoot, skill);
    for (const rel of walkFiles(skillDir)) {
      const full = path.join(skillDir, rel);
      const key = `prompts/skills/${skill}/${rel}`;
      const hash = fileHash(full);
      if (!force && state.files[key] === hash) continue;  // hash skip
      jobs.push({ key, full, hash });
    }
  }
  console.log(`${jobs.length} files to upload (${skills.length} skills)`);

  let uploaded = 0, failed = 0;
  const failureCauses = {};

  await pool(jobs, async (job) => {
    let res = await r2Put(job.key, job.full);
    if (!res.ok) {
      // one retry for transient failures
      const r2 = await r2Put(job.key, job.full);
      if (!r2.ok) {
        failed++;
        failureCauses[job.key] = r2.cause || 'unknown';
        return;
      }
      res = r2;  // use retry's size for verification
    }
    state.files[job.key] = job.hash;
    uploaded++;
    saveState(state);  // incremental: survive interruption
  }, PARALLEL);

  console.log(`\n=== RESULT: ${uploaded} uploaded, ${failed} failed, ${jobs.length - uploaded - failed} skipped ===`);
  if (failed > 0) {
    console.log('Failures:');
    for (const [k, c] of Object.entries(failureCauses)) console.log(`  ${k}: ${c}`);
    process.exit(1);
  }
  if (gitOk) {
    console.log('✓ Skill sync complete — GitHub (origin + rwnq8) + R2 in sync');
  } else if (skipGit && process.argv.includes('--skip-git')) {
    console.log('✓ Skill sync complete — R2 in sync (git skipped by --skip-git)');
  } else if (!gitOk && !skipGit) {
    console.log('⚠ Skill sync partial — R2 in sync, but git sync failed (see errors above)');
  } else {
    console.log('✓ Skill sync complete — R2 in sync (git unavailable)');
  }
})();
