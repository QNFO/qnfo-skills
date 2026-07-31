#!/usr/bin/env node
/**
 * skill-sync.js — Sync all local skills (SKILL.md + scripts/* + templates/* + references/*) to GitHub + R2
 *
 * Usage: node skill-sync.js [skills-root-dir] [--targets=a,b,c] [--force]
 *
 * Requires:
 *   - git configured with push access to origin and rwnq8 remotes
 *   - wrangler authenticated (CLOUDFLARE_API_TOKEN env var; verify: npx --yes --package wrangler@latest wrangler whoami)
 *
 * This script:
 *   1. Commits and pushes to both GitHub remotes (origin + rwnq8)
 *   2. Uploads ALL skill files (not just SKILL.md) to R2 via wrangler
 *
 * v3.0.0 (2026-07-31, kaizen):
 *   - HARD FIX: pin `npx --yes --package wrangler@latest` — bare `npx wrangler`
 *     resolved to a corrupted npx cache (missing @cloudflare/workerd-windows-64)
 *     which made EVERY upload fail with a workerd module error (misdiagnosed as
 *     auth). See mem-Hbi-G-pFovi8.
 *   - ADD: content-hash state file (~/.deepchat/.skill-sync-state.json) — files
 *     unchanged since last successful upload are SKIPPED, making re-runs fast
 *     and idempotent (previous runs were reaped at 19/29 skills by the harness
 *     timeout and re-uploaded everything from scratch).
 *   - ADD: --targets=a,b,c filter for partial syncs (companion to
 *     skill-sync-remaining.js).
 *   - ADD: per-file retry (1 retry on transient failure).
 *   - ADD: failure cause classification (auth vs cache-corruption vs timeout).
 *   - ADD: --force to bypass the hash skip.
 *
 * @version 3.0.0
 * @date 2026-07-31
 */

const { execSync, spawnSync } = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const BUCKET = 'qnfo-skills';
const WRANGLER_CMD = ['--yes', '--package', 'wrangler@latest', 'wrangler'];
const STATE_FILE = path.join(process.env.USERPROFILE || process.env.HOME, '.deepchat', '.skill-sync-state.json');

function fileHash(localPath) {
  const buf = fs.readFileSync(localPath);
  return crypto.createHash('sha256').update(buf).digest('hex');
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch (e) {
    return { files: {} };
  }
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
    if (entry.name.startsWith('.')) continue; // Skip hidden files/dirs (incl. .kaizen_history)
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out = out.concat(walkFiles(full, base));
    } else {
      out.push(path.relative(base, full).replace(/\\/g, '/'));
    }
  }
  return out;
}

function classifyFailure(errOut) {
  const text = (errOut || '').toLowerCase();
  if (text.includes('could not be found') && text.includes('workerd')) return 'cache-corruption';
  if (text.includes('not logged in') || text.includes('authentication') || text.includes('unauthorized') || text.includes('auth')) return 'auth';
  if (text.includes('timed out') || text.includes('timeout') || text.includes('etimedout')) return 'timeout';
  return 'other';
}

function r2Put(key, localPath, retry = true) {
  const args = [...WRANGLER_CMD, 'r2', 'object', 'put', `${BUCKET}/${key}`, `--file=${localPath}`, '--remote'];
  const result = spawnSync('npx', args, {
    encoding: 'utf8',
    timeout: 90000,
    shell: true,
    env: { ...process.env, NO_COLOR: '1' },
  });
  if (result.status === 0) return { ok: true };
  const cause = classifyFailure(result.stderr || result.stdout || result.error?.message);
  if (retry && cause !== 'auth' && cause !== 'cache-corruption') {
    // One retry for transient failures
    const r2 = r2Put(key, localPath, false);
    if (r2.ok) return { ok: true };
  }
  return { ok: false, cause };
}

async function syncSkills(skillsRoot, targets, force) {
  skillsRoot = skillsRoot || path.join(process.env.USERPROFILE || process.env.HOME, '.deepchat', 'skills');

  console.log('=== SKILL SYNC ===');
  console.log(`Skills root: ${skillsRoot}`);
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  // 1. Git commit + push to both remotes
  console.log('--- Git sync ---');
  try {
    execSync('git add -A', { cwd: skillsRoot, stdio: 'pipe' });
    try {
      execSync('git commit -m "ACTION:SYNC FILES: skills/* RATIONALE: automated skill-sync.js run -- propagate local SKILL.md/script edits to git history"', { cwd: skillsRoot, stdio: 'pipe' });
      console.log('✓ Git commit created');
    } catch (e) {
      console.log('○ No changes to commit');
    }

    try {
      execSync('git push origin master', { cwd: skillsRoot, stdio: 'pipe' });
      console.log('✓ Pushed to origin (QNFO/qnfo-skills)');
    } catch (e) {
      console.log('✗ Failed to push to origin:', e.message.split('\n')[0]);
    }

    try {
      execSync('git push rwnq8 master', { cwd: skillsRoot, stdio: 'pipe' });
      console.log('✓ Pushed to rwnq8 (rwnq8/qnfo-skills)');
    } catch (e) {
      console.log('✗ Failed to push to rwnq8:', e.message.split('\n')[0]);
    }
  } catch (e) {
    console.log('✗ Git error:', e.message.split('\n')[0]);
  }

  // 2. R2 sync
  console.log('\n--- R2 sync ---');
  const state = loadState();
  const skills = fs.readdirSync(skillsRoot, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('.') && fs.existsSync(path.join(skillsRoot, d.name, 'SKILL.md')))
    .map(d => d.name)
    .filter(s => !targets || targets.includes(s))
    .sort();

  console.log(`Found ${skills.length} skills to sync${force ? ' (--force: ignoring cached hashes)' : ''}`);

  let uploaded = 0;
  let skipped = 0;
  let failed = 0;
  const failureCauses = {};

  for (const skill of skills) {
    const skillDir = path.join(skillsRoot, skill);
    const files = walkFiles(skillDir);
    let skillUploaded = 0;
    let skillSkipped = 0;
    let skillFailed = 0;

    for (const rel of files) {
      const full = path.join(skillDir, rel);
      const key = `prompts/skills/${skill}/${rel}`;
      const hash = fileHash(full);

      // Hash skip: unchanged since last successful upload
      if (!force && state.files[key] === hash) {
        skillSkipped++;
        skipped++;
        continue;
      }

      const res = r2Put(key, full);
      if (res.ok) {
        state.files[key] = hash;
        skillUploaded++;
        uploaded++;
      } else {
        skillFailed++;
        failed++;
        failureCauses[res.cause] = (failureCauses[res.cause] || 0) + 1;
        console.error(`  ✗ FAILED [${res.cause}]: ${key}`);
      }
    }

    if (skillFailed === 0) {
      console.log(`✓ ${skill}: ${skillUploaded} uploaded, ${skillSkipped} skipped`);
    } else {
      console.log(`⚠ ${skill}: ${skillUploaded} OK, ${skillSkipped} skipped, ${skillFailed} FAILED`);
    }
  }

  saveState(state);

  console.log(`\n=== SUMMARY ===`);
  console.log(`Skills: ${skills.length}`);
  console.log(`Files uploaded: ${uploaded}`);
  console.log(`Files skipped (unchanged): ${skipped}`);
  console.log(`Files failed: ${failed}`);
  if (failed > 0) {
    console.log(`Failure causes: ${JSON.stringify(failureCauses)}`);
    if (failureCauses['cache-corruption']) {
      console.log('\n⚠ CACHE CORRUPTION DETECTED. Fix: remove the offending _npx\\<hash> dir from %LOCALAPPDATA%\\npm-cache\\_npx, then re-run. See mem-Hbi-G-pFovi8.');
    } else if (failureCauses['auth']) {
      console.log('\n⚠ AUTH FAILURE. Verify CLOUDFLARE_API_TOKEN is set: npx --yes --package wrangler@latest wrangler whoami');
    }
    process.exitCode = 1;
  } else {
    console.log('\n✅ All files synced successfully');
  }

  return { skillCount: skills.length, filesUploaded: uploaded, filesSkipped: skipped, filesFailed: failed };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const targetsArg = args.find(a => a.startsWith('--targets='));
  const targets = targetsArg ? targetsArg.split('=')[1].split(',').map(s => s.trim()).filter(Boolean) : null;
  const force = args.includes('--force');
  const rootArg = args.find(a => !a.startsWith('--'));
  syncSkills(rootArg, targets, force).catch(e => { console.error('FATAL:', e.message); process.exit(1); });
}
