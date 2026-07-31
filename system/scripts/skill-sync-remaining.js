#!/usr/bin/env node
/* skill-sync-remaining.js — upload ONLY the skills not yet synced to R2.
 * Fast targeted completion of skill-sync.js for: pdf, pptx, qnfo-agent,
 * qnfo-core, research, skill-creator, system, web-artifacts-builder,
 * windows-command-patterns, xlsx
 */
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const BUCKET = 'qnfo-skills';
const SKILLS_ROOT = path.join(process.env.USERPROFILE || process.env.HOME, '.deepchat', 'skills');
const TARGETS = ['pdf', 'pptx', 'qnfo-agent', 'qnfo-core', 'research', 'skill-creator', 'system', 'web-artifacts-builder', 'windows-command-patterns', 'xlsx'];

function walkFiles(dir, base) {
  base = base || dir;
  let out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out = out.concat(walkFiles(full, base));
    } else {
      out.push(path.relative(base, full).replace(/\\/g, '/'));
    }
  }
  return out;
}

function r2Put(key, localPath) {
  const result = spawnSync('npx', ['--yes', '--package', 'wrangler@latest', 'wrangler', 'r2', 'object', 'put', `${BUCKET}/${key}`, `--file=${localPath}`, '--remote'], {
    encoding: 'utf8',
    timeout: 90000,
    shell: true,
  });
  return result.status === 0;
}

let uploaded = 0;
let failed = 0;
const failedList = [];

for (const skill of TARGETS) {
  const skillDir = path.join(SKILLS_ROOT, skill);
  if (!fs.existsSync(skillDir) || !fs.existsSync(path.join(skillDir, 'SKILL.md'))) {
    console.log(`SKIP ${skill}: not found`);
    continue;
  }
  const files = walkFiles(skillDir);
  let ok = 0, fail = 0;
  for (const rel of files) {
    const full = path.join(skillDir, rel);
    const key = `prompts/skills/${skill}/${rel}`;
    if (r2Put(key, full)) {
      ok++; uploaded++;
    } else {
      fail++; failed++;
      failedList.push(key);
      console.error(`  X FAILED: ${key}`);
    }
  }
  console.log(`${fail === 0 ? 'OK' : 'WARN'} ${skill}: ${ok} files${fail ? `, ${fail} FAILED` : ''}`);
}

console.log(`\n=== SUMMARY ===`);
console.log(`Files uploaded: ${uploaded}`);
console.log(`Files failed: ${failed}`);
if (failed > 0) {
  failedList.forEach(k => console.error(`  FAILED: ${k}`));
  process.exit(1);
} else {
  console.log('ALL REMAINING SKILLS SYNCED TO R2');
}
