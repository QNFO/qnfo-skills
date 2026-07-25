// d1-safe-write.js -- Failsafe D1 CHECK-THEN-WRITE helper.
//
// Fixes two root-caused incidents:
//  1. ON CONFLICT upserts against FTS5-shadowed tables (e.g. living-paper.papers)
//     return HTTP 400 -- this script ALWAYS does SELECT-then-INSERT-or-UPDATE.
//  2. Large body_md/JSON payloads built via PowerShell ConvertTo-Json have been
//     observed to silently corrupt into the literal string "[object Object]"
//     (15 bytes) instead of the actual multi-KB content. Node's native
//     JSON.stringify on a string read via fs.readFileSync does not have this
//     failure mode -- ALWAYS use this script (or equivalent Node code) for any
//     D1 write payload larger than a few hundred characters, never PowerShell
//     string-building.
//
// Usage:
//   node d1-safe-write.js --account <ACCOUNT_ID> --db <DATABASE_UUID> \
//        --table papers --key-col slug --key-val my-slug \
//        --set-json '{"body_md_file":"paper.md","doi":"10.5281/zenodo.X","version":"3.2"}'
//
// --set-json values ending in _file are read from disk (fs.readFileSync) and
// substituted as the actual column value -- this is how large body_md content
// is safely injected without shell quoting corruption.
//
// Requires CLOUDFLARE_API_TOKEN in environment. Prints verification SELECT
// result at the end -- never trust the bare {success:true} write response.

const fs = require('fs');
const https = require('https');

function arg(name, def) {
  const i = process.argv.indexOf('--' + name);
  return i >= 0 ? process.argv[i + 1] : def;
}

const ACCOUNT = arg('account');
const DB = arg('db');
const TABLE = arg('table');
const KEY_COL = arg('key-col');
const KEY_VAL = arg('key-val');
const SET_JSON = arg('set-json');
const TOKEN = process.env.CLOUDFLARE_API_TOKEN;

if (!ACCOUNT || !DB || !TABLE || !KEY_COL || !KEY_VAL || !SET_JSON || !TOKEN) {
  console.error('Missing required args or CLOUDFLARE_API_TOKEN env var. See header comment for usage.');
  process.exit(1);
}

let setObj;
try {
  setObj = JSON.parse(SET_JSON);
} catch (e) {
  console.error('Invalid --set-json:', e.message);
  process.exit(1);
}

// Resolve _file suffixed keys to actual file contents (avoids shell-quoting corruption)
const resolved = {};
for (const [k, v] of Object.entries(setObj)) {
  if (k.endsWith('_file')) {
    const col = k.slice(0, -5);
    resolved[col] = fs.readFileSync(v, 'utf8');
  } else {
    resolved[k] = v;
  }
}

function d1Query(sql, params) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ sql, params: params || [] });
    const req = https.request({
      hostname: 'api.cloudflare.com',
      path: `/client/v4/accounts/${ACCOUNT}/d1/database/${DB}/query`,
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
    }, (res) => {
      let data = '';
      res.on('data', (c) => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { reject(new Error('Bad JSON response: ' + data.slice(0, 500))); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

(async () => {
  // Step 1: check existence
  const existsResp = await d1Query(`SELECT COUNT(*) as c FROM ${TABLE} WHERE ${KEY_COL} = ?`, [KEY_VAL]);
  const exists = existsResp.result?.[0]?.results?.[0]?.c > 0;
  console.log(`Existence check: ${TABLE}.${KEY_COL}=${KEY_VAL} -> exists=${exists}`);

  const cols = Object.keys(resolved);
  const vals = Object.values(resolved);

  if (!exists) {
    const placeholders = cols.map(() => '?').join(', ');
    const sql = `INSERT INTO ${TABLE} (${KEY_COL}, ${cols.join(', ')}) VALUES (?, ${placeholders})`;
    const resp = await d1Query(sql, [KEY_VAL, ...vals]);
    console.log('INSERT result:', JSON.stringify(resp.result?.[0]?.meta || resp));
  } else {
    const setClause = cols.map(c => `${c} = ?`).join(', ');
    const sql = `UPDATE ${TABLE} SET ${setClause} WHERE ${KEY_COL} = ?`;
    const resp = await d1Query(sql, [...vals, KEY_VAL]);
    console.log('UPDATE result:', JSON.stringify(resp.result?.[0]?.meta || resp));
  }

  // Step 2: MANDATORY independent re-verification (Anti-Phantom Gate)
  const verifyCols = cols.map(c => `LENGTH(${c}) as ${c}_len`).join(', ');
  const verifyResp = await d1Query(`SELECT ${KEY_COL}, ${verifyCols} FROM ${TABLE} WHERE ${KEY_COL} = ?`, [KEY_VAL]);
  const row = verifyResp.result?.[0]?.results?.[0];
  console.log('VERIFICATION (re-queried, not the write response):', JSON.stringify(row));

  for (const c of cols) {
    const expectedLen = String(resolved[c]).length;
    const actualLen = row?.[`${c}_len`];
    if (actualLen !== expectedLen) {
      console.error(`MISMATCH on column '${c}': expected length ${expectedLen}, got ${actualLen}. DO NOT report success -- write may be corrupted.`);
      process.exit(1);
    }
  }
  console.log('All column lengths verified matching. Write confirmed durable.');
})().catch(e => { console.error('FATAL:', e.message); process.exit(1); });
