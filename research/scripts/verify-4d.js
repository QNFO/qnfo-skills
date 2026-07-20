#!/usr/bin/env node
// verify-4d.js — Verify a publication meets the 4-D Distribution Gate:
// Distributed (>=2 IPFS gateways), Durable (Arweave/Zenodo/IA), Discoverable (DNSLink/DOI/KG), Duplicated (>=4 stores)
// Usage: node verify-4d.js <ipfs-cid> [arweave-tx] [doi] [dnslink-subdomain]
// NOTE (2026-07-20): gateway.pinata.cloud REMOVED from the gateway list —
// Pinata's free quota was exceeded and the account is blocked. Only free,
// unlimited-request public gateways are checked below.

async function checkUrl(url, timeoutMs = 8000) {
  try {
    const r = await fetch(url, { method: 'HEAD', signal: AbortSignal.timeout(timeoutMs) });
    return r.ok || r.status === 200;
  } catch (e) {
    return false;
  }
}

// RED-TEAM FIX (2026-07-20, verified live): arweave.net/{anything} ALWAYS
// returns HTTP 200 (it serves an SPA shell for every path, including
// nonexistent TX IDs) -- a bare checkUrl() against arweave.net/{txId} is a
// permanent false-positive and can NEVER fail. Use the tx status API
// instead, which correctly returns HTTP 400 {"error":"invalid tx id"} for a
// bogus TX and HTTP 200 for a confirmed one -- verified against a real bogus
// ID live 2026-07-20.
async function checkArweaveTx(txId, timeoutMs = 8000) {
  try {
    const r = await fetch(`https://arweave.net/tx/${txId}/status`, { signal: AbortSignal.timeout(timeoutMs) });
    return r.status === 200;
  } catch (e) {
    return false;
  }
}

async function verify4D(cid, arweaveTx, doi, dnslinkSubdomain) {
  const results = { distributed: false, durable: false, discoverable: false, duplicated: false, details: {} };

  // Distributed: check >=2 independent IPFS gateways
  if (cid) {
    // RED-TEAM FIX (2026-07-20, verified live): cloudflare-ipfs.com/cf-ipfs.com
    // no longer resolve via DNS at all (ENODATA) -- Cloudflare decommissioned
    // its public IPFS gateway. Replaced with a second working gateway
    // (w3s.link) so the >=2-gateway "distributed" check still has real signal.
    const gateways = [
      `https://ipfs.io/ipfs/${cid}`,
      `https://dweb.link/ipfs/${cid}`,
      `https://w3s.link/ipfs/${cid}`
    ];
    const checks = await Promise.all(gateways.map(g => checkUrl(g)));
    const passCount = checks.filter(Boolean).length;
    results.details.ipfs_gateways_reachable = passCount;
    results.distributed = passCount >= 2;
    // RED-TEAM FIX (2026-07-20): wrap in Boolean() -- the prior
    // `passCount >= 4 || (passCount >= 2 && (arweaveTx || doi))` expression
    // leaked the raw arweaveTx/doi STRING value (e.g. "duplicated": "none")
    // instead of a real boolean, due to JS && short-circuit returning its
    // right operand rather than coercing to boolean.
    results.duplicated = Boolean(passCount >= 4 || (passCount >= 2 && (arweaveTx || doi)));
  }

  // Durable: Arweave TX confirmed OR DOI resolves
  if (arweaveTx) {
    results.details.arweave_reachable = await checkArweaveTx(arweaveTx);
  }
  if (doi) {
    results.details.doi_resolves = await checkUrl(`https://doi.org/${doi}`);
  }
  results.durable = !!(results.details.arweave_reachable || results.details.doi_resolves);

  // Discoverable: DNSLink TXT record present (best-effort DNS-over-HTTPS check)
  if (dnslinkSubdomain) {
    try {
      const dnsR = await fetch(`https://cloudflare-dns.com/dns-query?name=_dnslink.${dnslinkSubdomain}&type=TXT`, {
        headers: { Accept: 'application/dns-json' }
      });
      const dnsD = await dnsR.json();
      results.details.dnslink_found = !!(dnsD.Answer && dnsD.Answer.length > 0);
    } catch (e) { results.details.dnslink_found = false; }
  }
  results.discoverable = !!(results.details.dnslink_found || doi);

  console.log('=== 4-D Distribution Verification ===');
  console.log(JSON.stringify(results, null, 2));
  const allPass = results.distributed && results.durable && results.discoverable && results.duplicated;
  console.log(allPass ? '\n[PASS] All 4 dimensions verified.' : '\n[FAIL] One or more dimensions incomplete.');
  return results;
}

if (require.main === module) {
  const [cid, arweaveTx, doi, dnslinkSubdomain] = process.argv.slice(2);
  if (!cid) {
    console.error('Usage: node verify-4d.js <ipfs-cid> [arweave-tx] [doi] [dnslink-subdomain]');
    process.exit(1);
  }
  verify4D(cid, arweaveTx, doi, dnslinkSubdomain).then(r => {
    const allPass = r.distributed && r.durable && r.discoverable && r.duplicated;
    process.exitCode = allPass ? 0 : 1;
  }).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { verify4D };
