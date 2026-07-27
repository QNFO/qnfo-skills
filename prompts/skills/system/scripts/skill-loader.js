#!/usr/bin/env node
/**
 * skill-loader.js v1.0
 * 
 * Pre-session skill loading helper for DeepChat.
 * 
 * Purpose: Generate a compact skill discovery summary that can be
 * included in session context to help the LLM discover and load
 * appropriate skills without requiring qnfo-agent to be pre-loaded.
 * 
 * Usage:
 *   node skill-loader.js              # Generate skill discovery summary
 *   node skill-loader.js --json       # Output as JSON
 *   node skill-loader.js --triggers   # Output trigger keywords only
 * 
 * Exit codes:
 *   0 = Success
 *   1 = Error reading skills
 */

const fs = require('fs');
const path = require('path');

const SKILLS_PATH = path.join(process.env.USERPROFILE, '.deepchat', 'skills');

// Core skill trigger patterns extracted from qnfo-agent's 24-Skill Trigger Table
// This is a STATIC copy to enable discovery WITHOUT loading qnfo-agent first
const SKILL_TRIGGERS = {
  'cloudflare': ['deploy', 'wrangler', 'Pages', 'Workers', 'R2', 'D1', 'DNS', 'KV', 'Vectorize', 'Queues', 'AI', 'DO', 'Zero Trust', 'WAF', 'CDN', 'email', 'Turnstile', 'infra audit', 'Cloudflare'],
  'research': ['research', 'paper', 'literature', 'preprint', 'cite', 'BibTeX', 'paradigm forecast', 'deep dive', 'publish', 'Zenodo', 'DOI', 'OSF', 'social media', 'SEO', 'IPFS'],
  'frontend-design': ['UI', 'design', 'frontend', 'page', 'styling', 'dashboard', 'React component', 'Tailwind', 'shadcn', 'visualization', 'chart', 'Tufte', 'infographic', 'BLING audit'],
  'algorithmic-art': ['algorithmic art', 'generative art', 'p5.js', 'flow field', 'particle system', 'seeded randomness'],
  'code': ['MCP server build', 'Model Context Protocol', 'FastMCP', 'MCP SDK', 'API integration'],
  'code-review': ['code quality review', 'anti-pattern scan', 'line-numbered security findings', 'code review', 'security audit'],
  'documents': ['docx', 'pptx', 'xlsx', 'Word', 'PowerPoint', 'Excel', 'PDF form fill', 'merge', 'split', 'spreadsheet'],
  'docx': ['Word document', 'tracked changes', 'comments', '.docx'],
  'pptx': ['PowerPoint', 'outline-to-slides', 'speaker notes', 'layouts', '.pptx'],
  'xlsx': ['Excel', 'CSV', 'TSV', 'formulas', 'recalculation', '.xlsx'],
  'pdf': ['PDF', 'form filling', 'merge', 'split', 'text extraction', 'table extraction'],
  'git-github': ['git error', 'commit message', 'merge', 'rebase', 'detached HEAD', 'stash', 'branch recovery', 'GitHub Issues', 'PRs', 'Wiki', 'Releases', 'Projects', 'GitHub-D1 sync'],
  'git-commit': ['write me a commit message'],
  'knowledge': ['knowledge graph', 'KG', 'memory', 'remember', 'recall', 'durable learning', 'Vectorize', 'impact analysis', 'ultrametric clustering', 'cross-system discovery'],
  'deepchat-settings': ['DeepChat app settings', 'theme', 'language', 'font', 'model config', 'temperature', 'maxTokens', 'context'],
  'system': ['MCP server config', 'skill create', 'skill deploy', 'skill sync', 'desktop', 'window', 'click', 'Computer Use automation'],
  'mcp-builder': ['building a NEW MCP server', 'protocol design', 'tool schema', 'external API wrapper'],
  'skill-creator': ['creating a SKILL.md', 'updating a SKILL.md', 'skill authoring'],
  'doc-coauthoring': ['co-authoring docs', 'proposals', 'specs', 'decision docs', 'structured iterative workflow'],
  'infographic-syntax-creator': ['AntV Infographic DSL', 'infographic template'],
  'web-artifacts-builder': ['multi-component HTML artifact', 'React', 'Tailwind', 'shadcn', 'state', 'routing'],
  'memory-management': ['routing durable learning', 'Memory vs Skills vs Scheduled Tasks vs Tape'],
  'kaizen-skill-fixes': ['retrospective', 'red-team kaizen audit', 'skill ecosystem audit', 'historical bugfix'],
  'qnfo-agent': ['ALWAYS ACTIVE - safety-net core']
};

// Skills that should always be loaded (pinned)
const ALWAYS_LOAD = ['qnfo-agent', 'system'];

function getInstalledSkills() {
  try {
    const dirs = fs.readdirSync(SKILLS_PATH, { withFileTypes: true })
      .filter(d => d.isDirectory() && !d.name.startsWith('.'))
      .map(d => d.name);
    return dirs;
  } catch (err) {
    console.error('Error reading skills directory:', err.message);
    return [];
  }
}

function getSkillVersion(skillName) {
  try {
    const skillMd = fs.readFileSync(path.join(SKILLS_PATH, skillName, 'SKILL.md'), 'utf8');
    const match = skillMd.match(/version:\s*["']?([^"'\n]+)["']?/);
    return match ? match[1].trim() : 'unknown';
  } catch {
    return 'unknown';
  }
}

function generateDiscoverySummary() {
  const installed = getInstalledSkills();
  const output = [];
  
  output.push('=== SKILL DISCOVERY SUMMARY ===');
  output.push(`Timestamp: ${new Date().toISOString()}`);
  output.push(`Installed skills: ${installed.length}`);
  output.push('');
  output.push('--- SKILL TRIGGER TABLE (load via skill_view when task matches) ---');
  output.push('');
  
  for (const [skill, triggers] of Object.entries(SKILL_TRIGGERS)) {
    if (installed.includes(skill) || skill === 'qnfo-agent') {
      const version = getSkillVersion(skill);
      const triggerStr = triggers.slice(0, 5).join(', ') + (triggers.length > 5 ? '...' : '');
      output.push(`${skill} (v${version}): ${triggerStr}`);
    }
  }
  
  output.push('');
  output.push('--- ALWAYS-ACTIVE SKILLS ---');
  for (const skill of ALWAYS_LOAD) {
    if (installed.includes(skill)) {
      output.push(`✓ ${skill} (v${getSkillVersion(skill)})`);
    }
  }
  
  output.push('');
  output.push('--- USAGE ---');
  output.push('When task matches triggers above, call: skill_view(name="<skill-name>")');
  output.push('This activates the skill for the current message/tool loop.');
  
  return output.join('\n');
}

function generateJson() {
  const installed = getInstalledSkills();
  const result = {
    timestamp: new Date().toISOString(),
    installedCount: installed.length,
    skills: {},
    alwaysActive: ALWAYS_LOAD
  };
  
  for (const skill of installed) {
    result.skills[skill] = {
      version: getSkillVersion(skill),
      triggers: SKILL_TRIGGERS[skill] || []
    };
  }
  
  return JSON.stringify(result, null, 2);
}

function generateTriggers() {
  const output = [];
  for (const [skill, triggers] of Object.entries(SKILL_TRIGGERS)) {
    output.push(`${skill}: ${triggers.join(', ')}`);
  }
  return output.join('\n');
}

// Main
const args = process.argv.slice(2);

if (args.includes('--json')) {
  console.log(generateJson());
} else if (args.includes('--triggers')) {
  console.log(generateTriggers());
} else {
  console.log(generateDiscoverySummary());
}

process.exit(0);
