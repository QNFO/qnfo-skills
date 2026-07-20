#!/usr/bin/env node
// lighthouse-pin.js — Pin a file to IPFS/Filecoin via Lighthouse.
// SECONDARY IPFS pinner as of 2026-07-20 (Pinata removed, quota exceeded).
// Free tier available at files.lighthouse.storage — no credit card required.
// Usage: node lighthouse-pin.js <file-path>
// Requires: LIGHTHOUSE_API_KEY env var (or ~/.lighthouse_api_key)
//
// RED-TEAM FIX (2026-07-20, verified live): node.lighthouse.storage is
// UNREACHABLE (connection timeout on direct probe, not a 4xx/5xx). The
// correct/live upload host is upload.lighthouse.storage (confirmed via
// live probe: HTTP 401 for an invalid key -- endpoint exists and responds).

const fs = require('fs');

async function lighthousePin(filePath) {
  const LKEY = process.env.LIGHTHOUSE_API_KEY;
  if (!LKEY) throw new Error('LIGHTHOUSE_API_KEY not set');
  const content = fs.readFileSync(filePath);

  const r = await fetch('https://upload.lighthouse.storage/api/v0/add', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + LKEY },
    body: content
  });
  const d = await r.json();
  if (d.Hash) {
    console.log('IPFS CID:', d.Hash);
    console.log('Gateway (ipfs.io):', 'https://ipfs.io/ipfs/' + d.Hash);
    // RED-TEAM FIX (2026-07-20): cloudflare-ipfs.com no longer resolves via
    // DNS at all (ENODATA, verified live) -- Cloudflare decommissioned its
    // public IPFS gateway. Use dweb.link instead.
    console.log('Gateway (dweb.link):', 'https://dweb.link/ipfs/' + d.Hash);
  } else {
    console.error('Lighthouse pin failed:', JSON.stringify(d));
    process.exitCode = 1;
  }
  return d.Hash;
}

if (require.main === module) {
  const [filePath] = process.argv.slice(2);
  if (!filePath) {
    console.error('Usage: node lighthouse-pin.js <file-path>');
    process.exit(1);
  }
  lighthousePin(filePath).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { lighthousePin };
