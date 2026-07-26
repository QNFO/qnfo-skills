#!/usr/bin/env node
/**
 * add-init-prompt.js v1.0
 * 
 * Adds the /init custom prompt to DeepChat's custom_prompts.json
 * This ensures qnfo-agent and system skills are loaded at session start.
 */

const fs = require('fs');
const path = require('path');

const PROMPTS_PATH = path.join(process.env.APPDATA, 'DeepChat', 'custom_prompts.json');

const INIT_PROMPT = {
  id: 'init-session',
  name: '🚀 INIT SESSION',
  description: 'Initialize session with core skills (qnfo-agent + system) and run skill hygiene check',
  content: `EXECUTE IMMEDIATELY without discussion:

1. Call skill_view("qnfo-agent") to load the safety-net core with 24-Skill Trigger Table
2. Call skill_view("system") to load skill management and config  
3. Call skill_run("system", "scripts/skill-hygiene.js") to verify skill locations
4. Report: "Session initialized. [skill-hygiene exit code] | qnfo-agent v[version] | system v[version]"

This ensures autonomous skill discovery works correctly for this session.`,
  parameters: [],
  enabled: true,
  source: 'local',
  createdAt: Date.now(),
  updatedAt: Date.now()
};

try {
  // Read existing prompts
  const content = fs.readFileSync(PROMPTS_PATH, 'utf8');
  const prompts = JSON.parse(content);
  
  // Find next available index
  const indices = Object.keys(prompts).map(k => parseInt(k)).filter(n => !isNaN(n));
  const nextIndex = indices.length > 0 ? Math.max(...indices) + 1 : 0;
  
  // Check if init-session already exists
  let exists = false;
  for (const key of Object.keys(prompts)) {
    if (prompts[key].id === 'init-session') {
      exists = true;
      prompts[key] = INIT_PROMPT;
      console.log('Updated existing init-session prompt');
      break;
    }
  }
  
  if (!exists) {
    prompts[nextIndex] = INIT_PROMPT;
    console.log(`Added init-session prompt at index ${nextIndex}`);
  }
  
  // Backup and write
  fs.copyFileSync(PROMPTS_PATH, PROMPTS_PATH + '.bak');
  fs.writeFileSync(PROMPTS_PATH, JSON.stringify(prompts, null, 2));
  
  console.log('✓ custom_prompts.json updated');
  console.log('✓ Backup saved to custom_prompts.json.bak');
  console.log('');
  console.log('To use: Type /init in DeepChat to initialize session with core skills');
  
} catch (err) {
  console.error('Error:', err.message);
  process.exit(1);
}
