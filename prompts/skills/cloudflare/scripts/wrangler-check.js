// wrangler-check.js -- Canonical wrangler availability + auth probe.
//
// ROOT CAUSE FIX (2026-07-25): Multiple prior sessions concluded "wrangler is
// not installed" from a SINGLE failed check such as:
//   - `npm ls -g wrangler` returning "(empty)" (wrangler is a devDependency /
//     npx-cached package, NOT expected to be globally installed)
//   - a `where wrangler` / `which wrangler` miss (there is no standalone
//     `wrangler` binary on PATH -- it is invoked exclusively via `npx`)
//   - a PATH issue inside a Python subprocess.run() call (subprocess does not
//     inherit the shell's PATH/npx resolution the way a direct `exec` does)
//
// ALL of the above are FALSE NEGATIVES. The correct, sufficient test is:
//     npx wrangler --version   (downloads/caches wrangler via npx on first run)
//     npx wrangler whoami      (confirms CLOUDFLARE_API_TOKEN auth works)
//
// If BOTH succeed, wrangler is fully usable via `npx wrangler <command>` for
// this session -- do not re-diagnose "not installed" from an unrelated
// global-install check or a broken subprocess PATH.
//
// Usage: node wrangler-check.js
// Exit code 0 = wrangler usable (version + whoami both succeeded)
// Exit code 1 = wrangler genuinely unusable (report the actual stderr)

const { execSync } = require('child_process');

function run(cmd) {
  try {
    const out = execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
    return { ok: true, out: out.trim() };
  } catch (e) {
    return { ok: false, out: (e.stdout || '') + (e.stderr || e.message || '') };
  }
}

console.log('=== wrangler-check.js: root-cause-fixed availability probe ===');

const version = run('npx wrangler --version');
console.log('npx wrangler --version:', version.ok ? 'OK -- ' + version.out : 'FAIL -- ' + version.out);

if (!version.ok) {
  console.log('RESULT: wrangler genuinely unavailable via npx. Check npm/npx installation, not global package list.');
  process.exit(1);
}

const whoami = run('npx wrangler whoami');
console.log('npx wrangler whoami:', whoami.ok ? 'OK' : 'FAIL');
console.log(whoami.out);

if (!whoami.ok || /not logged in|no credentials/i.test(whoami.out)) {
  console.log('RESULT: wrangler CLI works but CLOUDFLARE_API_TOKEN auth is missing/invalid. This is an AUTH issue, not an "installation" issue -- do not conflate the two.');
  process.exit(1);
}

console.log('RESULT: wrangler is fully usable via `npx wrangler <command>` in this session. Any prior "not installed" claim was a false negative from checking the wrong signal (global npm list / bare PATH lookup / subprocess PATH) -- see header comment for the specific anti-patterns this fixes.');
process.exit(0);
