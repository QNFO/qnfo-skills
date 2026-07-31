#!/usr/bin/env node
/* skill-sync-remaining.js — upload ONLY the skills not yet synced to R2.
 * Fast targeted completion of skill-sync.js for: pdf, pptx, qnfo-agent,
 * qnfo-core, research, skill-creator, system, web-artifacts-builder,
 * windows-command-patterns, xlsx
 *
 * v1.1 (2026-07-31, kaizen): pin `npx --yes --package wrangler@latest`
 * (bare `npx wrangler` can resolve to a corrupted npx cache — see
 * mem-Hbi-G-pFovi8). Same hash-skip state file as skill-sync.js v3.
 */
const { spawnSync } = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const BUCKET = 'qnfo-skills';
const WRANGLER_CMD = ['--yes', '--package', 'wrangler@latest', 'wrangler'];
const STATE_FILE = path.join(process.env.USERPROFILE || process.env.HOME, '.deepchat', '.skill-sync-state.json');
const SKILLS_ROOT = path.join(process.env.USERPROFILE || process.env.HOME, '.deepchat', 'skills');
const TARGETS = ['pdf', 'pptx', 'qnfo-agent', 'qnfo-core', 'research', 'skill-creator', 'system', 'web-artifacts-builder', 'windows-command-patterns', 'xlsx'];

function fileHash(localPath) {
  return crypto.createHash('sha256').update(fs.readFileSync(localPath)).digest('hex');
}

function loadState() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8')); } catch (e) { return { files: {} }; }
}

function saveState(state) {
  try { fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2)); } catch (e) { /* ignore */ }
}

function walkFiles(dir, base) {
  base = base || dir;
  let out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out = out.concat(walkFiles(full, base));
    else out.push(path.relative(base, full).replace(/\\/g, '/'));
  }
  return out;
}

function r2Put(key, localPath, retry = true) {
  const args = [...WRANGLER_CMD, 'r2', 'object', 'put', `${BUCKET}/${key}`, `--file=${localPath}`, '--remote'];
  const result = spawnSync('npx', args, { encoding: 'utf8', timeout: 90000, shell: true, env: { ...process.env, NO_COLOR: '1' } });
  if (result.status === 0) return { ok: true };
  const text = (result.stderr || '').toLowerCase();
  const cause = text.includes('workerd') ? 'cache-corruption' : text.includes('auth') ? 'auth' : 'other';
  if (retry && cause !== 'auth' && cause !== 'cache-corruption') return r2Put(key, localPath, false);
  return { ok: false, cause };
}

const state = loadState();
let uploaded = 0, skipped = 0, failed = 0;

for (const skill of TARGETS) {
  const skillDir = path.join(SKILLS_ROOT, skill);
  if (!fs.existsSync(skillDir) || !fs.existsSync(path.join(skillDir, 'SKILL.md'))) {
    console.log(`SKIP ${skill}: not found`);
    continue;
  }
  const files = walkFiles(skillDir);
  let ok = 0, sk = 0, fail = 0;
  for (const rel of files) {
    const full = path.join(skillDir, rel);
    const key = `prompts/skills/${skill}/${rel}`;
    const hash = fileHash(full);
    if (state.files[key] === hash) { sk++; skipped++; continue; }
    const res = r2Put(key, full);
    if (res.ok) { state.files[key] = hash; ok++; uploaded++; }
    else { fail++; failed++; console.error(`  X FAILED [${res.cause}]: ${key}`); }
  }
  console.log(`${fail === 0 ? 'OK' : 'WARN'} ${skill}: ${ok} uploaded, ${sk} skipped${fail ? `, ${fail} FAILED` : ''}`);
}

saveState(state);

console.log(`\n=== SUMMARY ===`);
console.log(`Files uploaded: ${uploaded}`);
console.log(`Files skipped: ${skipped}`);
console.log(`Files failed: ${failed}`);
if (failed > 0) {
  if (state.files && Object.keys(state.files).length && Object.values(state.files).some(v => v === 'cache-corruption')) {
    // not tracked per-key; keep simple
  }
  process.exit(1);
} else {
  console.log('ALL REMAINING SKILLS SYNCED TO R2');
}
