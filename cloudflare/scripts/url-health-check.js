#!/usr/bin/env node
// url-health-check.js — Quick probe of all known QNFO public URLs
// v1.0 (2026-07-30) — standalone, no API token needed (pure HTTP probes)
//
// Usage:
//   node url-health-check.js
//   node url-health-check.js --json          (machine-readable)
//   node url-health-check.js --domain qnfo.org  (single domain)

// ---- Known Public URLs -----------------------------------------------------
const KNOWN_URLS = [
  // --- Gateway-tier domains (qnfo-gateway Worker) ---
  { domain: 'qnfo.org',             paths: ['/', '/papers', '/stats'],             tier: 1, note: 'QNFO hub' },
  { domain: 'papers.qnfo.org',      paths: ['/', '/papers'],                       tier: 1, note: 'Papers server' },
  { domain: 'legal.qnfo.org',       paths: ['/', '/legal'],                        tier: 1, note: 'Legal hub' },
  { domain: 'graph-api.qnfo.org',   paths: ['/', '/stats'],                        tier: 1, note: 'Graph API' },
  { domain: 'q08.org',              paths: ['/'],                                  tier: 2, note: 'Worker subdomain parent' },

  // --- Pages-tier domains ---
  { domain: 'qwav.org',             paths: ['/'],                                  tier: 1, note: 'QWAV landing' },
  { domain: 'qwav.tech',            paths: ['/'],                                  tier: 1, note: 'QWAV tech' },

  // --- Worker-direct URLs ---
  { domain: 'qnfo-gateway.q08.workers.dev',    paths: ['/health', '/papers', '/stats'], tier: 1, note: 'Gateway Worker' },
  { domain: 'qnfo-ai.q08.workers.dev',         paths: ['/health', '/v1/search?q=test'],  tier: 2, note: 'AI Worker' },
  { domain: 'qnfo-ipatent.q08.workers.dev',    paths: ['/health', '/api/disclosures'],    tier: 2, note: 'IPatent Worker' },
  { domain: 'qnfo-qwav.q08.workers.dev',       paths: ['/health', '/papers'],             tier: 2, note: 'QWAV Worker' },
  { domain: 'qnfo-memory-mcp.q08.workers.dev', paths: ['/health'],                        tier: 2, note: 'Memory MCP' },
  { domain: 'qnfo-lifecycle.q08.workers.dev',  paths: ['/status'],                        tier: 2, note: 'Lifecycle Worker' },
  { domain: 'qnfo-archive.q08.workers.dev',    paths: ['/health'],                        tier: 2, note: 'Archive Worker' },

  // --- Pages.dev domains ---
  { domain: 'qnfo-publications.pages.dev',     paths: ['/'],                        tier: 2, note: 'Publications Pages' },
  { domain: 'qwav.pages.dev',                  paths: ['/'],                        tier: 2, note: 'QWAV Pages' },
  { domain: 'qnfo-hub.pages.dev',              paths: ['/'],                        tier: 2, note: 'Hub Pages' },
  { domain: 'ipatent-me.pages.dev',            paths: ['/'],                        tier: 2, note: 'IPatent Pages' },
  { domain: 'ask-qwav.pages.dev',              paths: ['/'],                        tier: 2, note: 'Ask QWAV Pages' },

  // --- Known dead/problem domains ---
  { domain: 'ipatent.me',            paths: ['/'],                                  tier: 1, note: 'IPatent (redirect-broken — KIF-51)' },
  { domain: 'empoweringchange.today', paths: ['/'],                                 tier: 3, note: 'Dormant' },
  { domain: 'qnfo.net',              paths: ['/'],                                  tier: 3, note: 'Empty zone — KIF-52' },
  { domain: 'qnfo.uk',               paths: ['/'],                                  tier: 3, note: 'Empty zone — KIF-52' },
  { domain: 'q-wave.tech',           paths: ['/'],                                  tier: 3, note: 'Empty zone — KIF-52' },
  { domain: 'qwave.tech',            paths: ['/'],                                  tier: 3, note: 'Domain' },
  { domain: 'qwav.net',              paths: ['/'],                                  tier: 3, note: 'Domain' },
  { domain: 'qwav.uk',               paths: ['/'],                                  tier: 3, note: 'Domain' },
];

// ---- Probe -----------------------------------------------------------------
async function probe(url, timeoutMs = 15000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  const start = Date.now();
  try {
    const r = await fetch(url, { method: 'GET', redirect: 'manual', signal: controller.signal });
    clearTimeout(timer);
    const latency = Date.now() - start;
    const body = await r.text().catch(() => '');
    return {
      url,
      status: r.status,
      bodyLen: body.length,
      latencyMs: latency,
      ok: r.status >= 200 && r.status < 400,
      redirect: r.status >= 300 && r.status < 400 ? r.headers.get('location') || '' : '',
      server: r.headers.get('server') || '',
      cfRay: r.headers.get('cf-ray') || '',
      contentType: r.headers.get('content-type') || '',
    };
  } catch (e) {
    clearTimeout(timer);
    return {
      url,
      status: 0,
      bodyLen: 0,
      latencyMs: Date.now() - start,
      ok: false,
      error: e.message,
      redirect: '',
      server: '',
      cfRay: '',
      contentType: '',
    };
  }
}

// ---- Color helpers (ANSI) --------------------------------------------------
const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const GRAY = '\x1b[90m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';

function statusColor(status) {
  if (status >= 200 && status < 300) return GREEN;
  if (status >= 300 && status < 400) return CYAN;
  if (status >= 400 && status < 500) return YELLOW;
  if (status >= 500 || status === 0) return RED;
  return RESET;
}

function tierLabel(tier) {
  if (tier === 1) return RED + 'T1' + RESET;
  if (tier === 2) return YELLOW + 'T2' + RESET;
  return GRAY + 'T3' + RESET;
}

// ---- Main ------------------------------------------------------------------
async function main() {
  const args = process.argv.slice(2);
  const jsonOutput = args.includes('--json');
  const targetDomain = args.includes('--domain') ? args[args.indexOf('--domain') + 1] : null;

  let urls = KNOWN_URLS;
  if (targetDomain) {
    urls = KNOWN_URLS.filter(u => u.domain === targetDomain);
    if (urls.length === 0) {
      console.error(`Domain "${targetDomain}" not in known URLs list.`);
      process.exit(1);
    }
  }

  const results = [];

  if (!jsonOutput) {
    console.log(`${BOLD}QNFO Public URL Health Check${RESET}`);
    console.log(`${new Date().toISOString()}`);
    console.log(`Probing ${urls.reduce((sum, u) => sum + u.paths.length, 0)} URLs across ${urls.length} domains\n`);
    console.log('STATUS LATENCY    SIZE TIER  URL');
    console.log('------ ------- ------- ----  ' + '-'.repeat(40));
  }

  // Probe all URLs (sequential to avoid rate-limiting)
  for (const entry of urls) {
    for (const path of entry.paths) {
      const fullUrl = `https://${entry.domain}${path}`;
      const result = await probe(fullUrl);
      result.tier = entry.tier;
      result.note = entry.note;
      result.domain = entry.domain;
      results.push(result);

      if (!jsonOutput) {
        const statusStr = result.status === 0 ? 'DOWN' : String(result.status);
        const colorStart = statusColor(result.status);
        const statusCol = `${colorStart}${statusStr.padStart(6)}${RESET}`;
        const latencyCol = `${result.latencyMs}ms`.padStart(7);
        const sizeCol = result.bodyLen > 1024 
          ? `${(result.bodyLen / 1024).toFixed(1)}k`.padStart(7)
          : `${result.bodyLen}B`.padStart(7);
        const noteSuffix = result.error ? ` ${RED}(${result.error})${RESET}` : 
          result.redirect ? ` ${CYAN}→ ${result.redirect.slice(0, 40)}${RESET}` : '';
        console.log(`${statusCol} ${GRAY}${latencyCol}${RESET} ${sizeCol} ${tierLabel(entry.tier)}  ${fullUrl}${noteSuffix}`);
      }
    }
  }

  // Summary
  const total = results.length;
  const up = results.filter(r => r.status >= 200 && r.status < 400).length;
  const down = results.filter(r => r.status === 0).length;
  const errors = results.filter(r => r.status >= 400).length;
  const critical = results.filter(r => r.status >= 500 || r.status === 0).length;

  if (jsonOutput) {
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      summary: { total, up, redirect: results.filter(r => r.status >= 300 && r.status < 400).length, down, errors, critical },
      results
    }, null, 2));
  } else {
    console.log(`\n${BOLD}=== RESULTS ===${RESET}`);
    console.log(`Total: ${total} | ${GREEN}UP: ${up}${RESET} | ${RED}DOWN: ${down}${RESET} | ${YELLOW}ERRORS: ${errors}${RESET} | ${RED}CRITICAL: ${critical}${RESET}`);

    if (critical > 0) {
      console.log(`\n${RED}${BOLD}CRITICAL — these URLs are unreachable:${RESET}`);
      results.filter(r => r.status >= 500 || r.status === 0).forEach(r => {
        console.log(`  ${r.url} → ${r.status === 0 ? 'UNREACHABLE' : r.status}${r.error ? ' (' + r.error + ')' : ''}`);
      });
    }

    // Tier-1 health summary
    const tier1Urls = results.filter(r => r.tier === 1);
    const tier1Ok = tier1Urls.filter(r => r.status >= 200 && r.status < 400).length;
    console.log(`\n${BOLD}Tier-1 (public-facing):${RESET} ${tier1Ok}/${tier1Urls.length} healthy`);
    if (tier1Ok < tier1Urls.length) {
      console.log(`${RED}** ACTION REQUIRED: Tier-1 URLs are down${RESET}`);
    }
  }

  // Exit code
  if (critical > 0) process.exitCode = 2;
  else if (errors > 0) process.exitCode = 1;
}

if (require.main === module) {
  main().catch(e => { console.error('FATAL:', e.message); process.exit(2); });
}

module.exports = { probe, KNOWN_URLS, main };
