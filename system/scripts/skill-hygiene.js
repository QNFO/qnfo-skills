#!/usr/bin/env node
/**
 * skill-hygiene.js — Skill Location Hygiene Audit
 * 
 * PURPOSE: Detect and report duplicate/stale/conflicting skill directories
 * across all known skill storage locations. This script should be run:
 * 1. On DeepChat startup (via scheduled task or manual invocation)
 * 2. Before any skill sync operation
 * 3. As part of infrastructure audits
 * 
 * CANONICAL SKILL LOCATION:
 *   %USERPROFILE%\.deepchat\skills\  (git-tracked: QNFO/qnfo-skills)
 * 
 * KNOWN STALE/DUPLICATE LOCATIONS TO CHECK:
 *   - %APPDATA%\.deepchat\skills\           (legacy bootstrap location)
 *   - %APPDATA%\DeepChat\skills\            (unused app data location)
 *   - %LOCALAPPDATA%\DeepChat\skills\       (potential electron cache)
 * 
 * GITHUB REMOTES (both should have identical HEAD):
 *   - origin: QNFO/qnfo-skills (primary)
 *   - rwnq8:  rwnq8/qnfo-skills (mirror)
 * 
 * R2 BACKUP:
 *   - qnfo-skills bucket, prompts/skills/<name>/SKILL.md
 * 
 * EXIT CODES:
 *   0 = All clean, no duplicates
 *   1 = Stale/duplicate locations found (needs cleanup)
 *   2 = Version conflicts detected (needs manual resolution)
 *   3 = Script error
 * 
 * @version 1.0.0
 * @date 2026-07-26
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const crypto = require('crypto');

// Configuration
const USERPROFILE = process.env.USERPROFILE || process.env.HOME;
const APPDATA = process.env.APPDATA || path.join(USERPROFILE, 'AppData', 'Roaming');
const LOCALAPPDATA = process.env.LOCALAPPDATA || path.join(USERPROFILE, 'AppData', 'Local');

const CANONICAL_PATH = path.join(USERPROFILE, '.deepchat', 'skills');
const STALE_LOCATIONS = [
  path.join(APPDATA, '.deepchat', 'skills'),
  path.join(APPDATA, 'DeepChat', 'skills'),
  path.join(LOCALAPPDATA, 'DeepChat', 'skills'),
];

const GITHUB_REMOTES = {
  origin: 'QNFO/qnfo-skills',
  rwnq8: 'rwnq8/qnfo-skills',
};

// Results
const results = {
  canonical: { path: CANONICAL_PATH, exists: false, skillCount: 0, gitStatus: null },
  staleLocations: [],
  versionConflicts: [],
  githubSync: { origin: null, rwnq8: null, inSync: false },
  supplementalFiles: { total: 0, bySkill: {} },
  recommendations: [],
};

// Utility functions
function sha256(content) {
  return crypto.createHash('sha256').update(content).digest('hex').substring(0, 16);
}

function getSkillVersion(skillPath) {
  const skillMd = path.join(skillPath, 'SKILL.md');
  if (!fs.existsSync(skillMd)) return null;
  const content = fs.readFileSync(skillMd, 'utf8');
  const match = content.match(/version:\s*["']?([0-9.]+)["']?/);
  return match ? match[1] : 'unknown';
}

function countSupplementalFiles(skillPath) {
  let count = 0;
  const subdirs = ['scripts', 'references', 'templates', 'assets'];
  for (const subdir of subdirs) {
    const dirPath = path.join(skillPath, subdir);
    if (fs.existsSync(dirPath)) {
      count += fs.readdirSync(dirPath, { recursive: true })
        .filter(f => fs.statSync(path.join(dirPath, f)).isFile()).length;
    }
  }
  return count;
}

function getGitHead(repoPath) {
  try {
    return execSync('git rev-parse HEAD', { cwd: repoPath, encoding: 'utf8' }).trim().substring(0, 7);
  } catch {
    return null;
  }
}

function getRemoteHead(repoPath, remote) {
  try {
    execSync(`git fetch ${remote} --quiet`, { cwd: repoPath, encoding: 'utf8', timeout: 10000 });
    return execSync(`git rev-parse ${remote}/master`, { cwd: repoPath, encoding: 'utf8' }).trim().substring(0, 7);
  } catch {
    return null;
  }
}

// Main audit
console.log('=== SKILL HYGIENE AUDIT ===');
console.log(`Timestamp: ${new Date().toISOString()}`);
console.log(`Canonical path: ${CANONICAL_PATH}\n`);

// 1. Check canonical location
if (fs.existsSync(CANONICAL_PATH)) {
  results.canonical.exists = true;
  const skills = fs.readdirSync(CANONICAL_PATH)
    .filter(d => {
      const fullPath = path.join(CANONICAL_PATH, d);
      return fs.statSync(fullPath).isDirectory() && 
             fs.existsSync(path.join(fullPath, 'SKILL.md')) &&
             !d.startsWith('.');
    });
  results.canonical.skillCount = skills.length;
  results.canonical.gitStatus = getGitHead(CANONICAL_PATH);
  
  // Count supplemental files per skill
  for (const skill of skills) {
    const count = countSupplementalFiles(path.join(CANONICAL_PATH, skill));
    if (count > 0) {
      results.supplementalFiles.bySkill[skill] = count;
      results.supplementalFiles.total += count;
    }
  }
  
  console.log(`✓ Canonical location exists: ${skills.length} skills, ${results.supplementalFiles.total} supplemental files`);
  console.log(`  Git HEAD: ${results.canonical.gitStatus || 'NOT A GIT REPO'}`);
} else {
  console.log(`✗ CRITICAL: Canonical location does not exist!`);
  results.recommendations.push('CREATE canonical skill directory and clone QNFO/qnfo-skills');
}

// 2. Check stale locations
console.log('\n--- Checking stale locations ---');
for (const stalePath of STALE_LOCATIONS) {
  if (fs.existsSync(stalePath)) {
    const staleSkills = fs.readdirSync(stalePath)
      .filter(d => {
        const fullPath = path.join(stalePath, d);
        return fs.statSync(fullPath).isDirectory() && 
               fs.existsSync(path.join(fullPath, 'SKILL.md'));
      });
    
    if (staleSkills.length > 0) {
      const staleInfo = {
        path: stalePath,
        skillCount: staleSkills.length,
        skills: staleSkills.map(s => ({
          name: s,
          version: getSkillVersion(path.join(stalePath, s)),
        })),
      };
      results.staleLocations.push(staleInfo);
      console.log(`✗ STALE: ${stalePath}`);
      console.log(`  Contains ${staleSkills.length} skills: ${staleSkills.join(', ')}`);
      
      // Check for version conflicts
      for (const skill of staleSkills) {
        const staleVersion = getSkillVersion(path.join(stalePath, skill));
        const canonicalVersion = getSkillVersion(path.join(CANONICAL_PATH, skill));
        if (canonicalVersion && staleVersion && staleVersion !== canonicalVersion) {
          results.versionConflicts.push({
            skill,
            stalePath,
            staleVersion,
            canonicalVersion,
          });
          console.log(`  ⚠ VERSION CONFLICT: ${skill} (stale: v${staleVersion}, canonical: v${canonicalVersion})`);
        }
      }
      
      results.recommendations.push(`DELETE stale directory: ${stalePath}`);
    } else {
      console.log(`○ Empty/no skills: ${stalePath}`);
    }
  } else {
    console.log(`✓ Clean: ${stalePath} (does not exist)`);
  }
}

// 3. Check GitHub remotes sync
console.log('\n--- Checking GitHub remotes ---');
if (results.canonical.gitStatus) {
  const localHead = results.canonical.gitStatus;
  results.githubSync.origin = getRemoteHead(CANONICAL_PATH, 'origin');
  results.githubSync.rwnq8 = getRemoteHead(CANONICAL_PATH, 'rwnq8');
  results.githubSync.inSync = 
    localHead === results.githubSync.origin && 
    localHead === results.githubSync.rwnq8;
  
  console.log(`  Local:  ${localHead}`);
  console.log(`  origin: ${results.githubSync.origin || 'FETCH FAILED'}`);
  console.log(`  rwnq8:  ${results.githubSync.rwnq8 || 'FETCH FAILED'}`);
  
  if (results.githubSync.inSync) {
    console.log(`✓ All remotes in sync`);
  } else {
    console.log(`✗ REMOTES OUT OF SYNC`);
    results.recommendations.push('Run: git push origin master && git push rwnq8 master');
  }
}

// 4. Summary
console.log('\n=== SUMMARY ===');
console.log(`Canonical skills: ${results.canonical.skillCount}`);
console.log(`Supplemental files: ${results.supplementalFiles.total}`);
console.log(`Stale locations: ${results.staleLocations.length}`);
console.log(`Version conflicts: ${results.versionConflicts.length}`);
console.log(`GitHub sync: ${results.githubSync.inSync ? 'OK' : 'OUT OF SYNC'}`);

// 5. Recommendations
if (results.recommendations.length > 0) {
  console.log('\n=== RECOMMENDATIONS ===');
  results.recommendations.forEach((r, i) => console.log(`${i + 1}. ${r}`));
}

// 6. Output JSON for programmatic consumption
const jsonOutput = path.join(CANONICAL_PATH, '..', 'audit', 'skill-hygiene-latest.json');
try {
  fs.mkdirSync(path.dirname(jsonOutput), { recursive: true });
  fs.writeFileSync(jsonOutput, JSON.stringify(results, null, 2));
  console.log(`\nJSON report: ${jsonOutput}`);
} catch (e) {
  console.error(`Failed to write JSON report: ${e.message}`);
}

// Exit code
if (results.versionConflicts.length > 0) {
  console.log('\n❌ EXIT CODE 2: Version conflicts require manual resolution');
  process.exit(2);
} else if (results.staleLocations.length > 0) {
  console.log('\n⚠ EXIT CODE 1: Stale locations found, cleanup recommended');
  process.exit(1);
} else {
  console.log('\n✅ EXIT CODE 0: All clean');
  process.exit(0);
}
