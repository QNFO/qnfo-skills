#!/usr/bin/env node
/**
 * skill-sync.js — Sync all local skills (SKILL.md + scripts/* + templates/* + references/*) to GitHub + R2
 * 
 * Usage: node skill-sync.js [skills-root-dir]
 * 
 * Requires:
 *   - git configured with push access to origin and rwnq8 remotes
 *   - wrangler authenticated (npx wrangler whoami should work)
 * 
 * This script:
 *   1. Commits and pushes to both GitHub remotes (origin + rwnq8)
 *   2. Uploads ALL skill files (not just SKILL.md) to R2 via wrangler
 * 
 * @version 2.0.0
 * @date 2026-07-26
 */

const { execSync, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const BUCKET = 'qnfo-skills';

function walkFiles(dir, base) {
  base = base || dir;
  let out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue; // Skip hidden files/dirs
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
  // Use wrangler for R2 uploads (handles auth correctly)
  const result = spawnSync('npx', ['wrangler', 'r2', 'object', 'put', `${BUCKET}/${key}`, `--file=${localPath}`, '--remote'], {
    encoding: 'utf8',
    timeout: 60000,
    shell: true,
  });
  return result.status === 0;
}

async function syncSkills(skillsRoot) {
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
    
    // Push to both remotes
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

  // 2. R2 sync — every file under each skill directory that has a SKILL.md
  console.log('\n--- R2 sync ---');
  const skills = fs.readdirSync(skillsRoot, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('.') && fs.existsSync(path.join(skillsRoot, d.name, 'SKILL.md')))
    .map(d => d.name);

  console.log(`Found ${skills.length} skills to sync`);

  let uploaded = 0;
  let failed = 0;
  
  for (const skill of skills) {
    const skillDir = path.join(skillsRoot, skill);
    const files = walkFiles(skillDir);
    let skillUploaded = 0;
    let skillFailed = 0;
    
    for (const rel of files) {
      const full = path.join(skillDir, rel);
      const key = `prompts/skills/${skill}/${rel}`;
      const ok = r2Put(key, full);
      if (ok) {
        skillUploaded++;
        uploaded++;
      } else {
        skillFailed++;
        failed++;
        console.error(`  ✗ FAILED: ${key}`);
      }
    }
    
    if (skillFailed === 0) {
      console.log(`✓ ${skill}: ${skillUploaded} files`);
    } else {
      console.log(`⚠ ${skill}: ${skillUploaded} OK, ${skillFailed} FAILED`);
    }
  }

  console.log(`\n=== SUMMARY ===`);
  console.log(`Skills: ${skills.length}`);
  console.log(`Files uploaded: ${uploaded}`);
  console.log(`Files failed: ${failed}`);
  
  if (failed > 0) {
    console.log('\n⚠ Some files failed to upload. Check wrangler authentication.');
    process.exitCode = 1;
  } else {
    console.log('\n✅ All files synced successfully');
  }
  
  return { skillCount: skills.length, filesUploaded: uploaded, filesFailed: failed };
}

if (require.main === module) {
  syncSkills(process.argv[2]).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { syncSkills };
