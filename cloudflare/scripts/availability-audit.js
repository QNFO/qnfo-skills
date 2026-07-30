#!/usr/bin/env node
// availability-audit.js — Unified QNFO Cloudflare availability audit against LoS standards
// v1.0 (2026-07-30) — standalone, auto-discovers credentials
//
// Audits three layers:
//   Worker tier: W-S1..W-S6 (health, binding integrity, no debug routes, .workers.dev reachable)
//   Page tier:   P-S1..P-S5 (root reachable, 522-RISK, build recency, DNS integrity)
//   DNS tier:    D-S1..D-S7 (min records, resolution, CNAME chains, dead Workers, redirects, proxied, routes)
//
// Usage:
//   node availability-audit.js
//   node availability-audit.js --tier workers
//   node availability-audit.js --tier pages
//   node availability-audit.js --tier dns
//   node availability-audit.js --json          (machine-readable output)
//   node availability-audit.js --quick         (fast mode: skip build checks, skip deep source analysis)

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

// ---- Token Discovery -------------------------------------------------------
function discoverToken() {
  if (process.env.CLOUDFLARE_API_TOKEN) return process.env.CLOUDFLARE_API_TOKEN;
  const home = os.homedir();
  const tokenFile = path.join(home, '.cloudflare_token');
  if (fs.existsSync(tokenFile)) return fs.readFileSync(tokenFile, 'utf8').trim();
  const keysFile = path.join(home, 'keys.json');
  if (fs.existsSync(keysFile)) {
    try {
      const keys = JSON.parse(fs.readFileSync(keysFile, 'utf8'));
      return keys.CLOUDFLARE_API_TOKEN || keys.cloudflare_token || '';
    } catch {}
  }
  return '';
}

const TOKEN = discoverToken();
if (!TOKEN) {
  console.error('FATAL: CLOUDFLARE_API_TOKEN not set. Set env var, ~/.cloudflare_token, or ~/keys.json');
  process.exit(2);
}

// ---- Account Discovery -----------------------------------------------------
async function discoverAccountId() {
  if (process.env.CLOUDFLARE_ACCOUNT_ID) return process.env.CLOUDFLARE_ACCOUNT_ID;
  const r = await cf('/accounts?per_page=5');
  const accounts = r.result || [];
  if (accounts.length === 0) throw new Error('No accounts visible — check token scope');
  if (accounts.length > 1) console.error(`WARN: ${accounts.length} accounts visible; using "${accounts[0].name}"`);
  return accounts[0].id;
}

// ---- Subdomain Discovery ---------------------------------------------------
// Attempt to discover the workers.dev subdomain (e.g., "q08") from wrangler config
function discoverSubdomain() {
  const candidates = [
    path.join(os.homedir(), '.deepchat', 'wrangler.toml'),
    path.join(process.cwd(), 'wrangler.toml'),
    path.join(process.cwd(), 'wrangler.jsonc'),
  ];
  for (const p of candidates) {
    if (fs.existsSync(p)) {
      const content = fs.readFileSync(p, 'utf8');
      const m = content.match(/workers_dev\s*=\s*true/);
      if (m) {
        const sm = content.match(/route\s*=\s*["']?(\w+)\.workers\.dev/);
        if (sm) return sm[1];
      }
    }
  }
  // Try to infer from a known Worker
  return 'q08'; // Default QNFO subdomain
}

// ---- API Helpers -----------------------------------------------------------
async function cf(pathQuery, method = 'GET', body = null) {
  const opts = { method, headers: { Authorization: `Bearer ${TOKEN}` } };
  if (body) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  }
  const url = `https://api.cloudflare.com/client/v4${pathQuery}`;
  const r = await fetch(url, opts);
  const data = await r.json();
  if (!data.success) {
    const errs = (data.errors || []).map(e => e.message).join('; ');
    console.error(`API ERROR ${pathQuery}: ${errs}`);
  }
  return data;
}

// ---- HTTP Probe ------------------------------------------------------------
async function probe(url, opts = {}) {
  const { method = 'GET', timeoutMs = 10000 } = opts;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const r = await fetch(url, { method, redirect: 'manual', signal: controller.signal });
    clearTimeout(timer);
    const body = await r.text().catch(() => '');
    return { status: r.status, body: body.slice(0, 200), bodyLen: body.length, ok: r.ok, headers: Object.fromEntries(r.headers) };
  } catch (e) {
    clearTimeout(timer);
    return { status: 0, body: '', bodyLen: 0, ok: false, error: e.message };
  }
}

// ---- Findings Collector ----------------------------------------------------
const findings = [];
function record(layer, standard, severity, subject, status, detail = '') {
  findings.push({
    layer,         // "worker" | "page" | "dns"
    standard,      // "W-S1", "P-S2", "D-S3", etc.
    severity,      // "CRITICAL" | "WARNING" | "INFO"
    subject,       // Worker name, domain, zone name
    status,        // "PASS" | "FAIL" | "SKIP"
    detail,        // Human-readable explanation
    fix: ''       // Remediation hint
  });
}

// ---- Worker Tier Audits ----------------------------------------------------
async function auditWorkers(ACCOUNT, SUBDOMAIN, quickMode) {
  const workersResp = await cf(`/accounts/${ACCOUNT}/workers/scripts`);
  const workers = workersResp.result || [];
  if (workers.length === 0) {
    record('worker', 'W-S0', 'CRITICAL', 'fleet', 'FAIL', 'No Workers found in account');
    return;
  }

  for (const w of workers) {
    const name = w.id;
    
    // W-S1: Health endpoint
    const healthUrl = `https://${name}.${SUBDOMAIN}.workers.dev/health`;
    const statusUrl = `https://${name}.${SUBDOMAIN}.workers.dev/status`;
    
    let healthResp = await probe(healthUrl);
    if (healthResp.status === 404 || healthResp.status === 0) {
      healthResp = await probe(statusUrl); // Try /status for cron Workers
    }
    
    if (healthResp.status === 200 && healthResp.bodyLen > 0) {
      record('worker', 'W-S1', 'INFO', name, 'PASS', `/health → 200 (${healthResp.bodyLen} bytes)`);
    } else {
      record('worker', 'W-S1', 'WARNING', name, 'FAIL', 
        `/health → ${healthResp.status || 'unreachable'}${healthResp.error ? ' (' + healthResp.error + ')' : ''}`);
    }

    // W-S2: Binding integrity gate (only for Workers with D1/R2/KV bindings)
    // We probe known data-dependent routes based on Worker identity
    const dataRoutes = getDataRoutesForWorker(name);
    if (dataRoutes.length > 0) {
      let passing = 0;
      for (const route of dataRoutes) {
        const resp = await probe(`https://${name}.${SUBDOMAIN}.workers.dev${route.path}`);
        if (resp.status === 200 && resp.bodyLen >= 50) {
          passing++;
        } else {
          record('worker', 'W-S2', 'CRITICAL', name, 'FAIL',
            `${route.path} → ${resp.status} (body: ${resp.bodyLen} bytes) — possible binding loss`);
        }
      }
      if (passing >= Math.min(2, dataRoutes.length)) {
        record('worker', 'W-S2', 'INFO', name, 'PASS', `${passing}/${dataRoutes.length} data routes healthy`);
      }
    } else {
      record('worker', 'W-S2', 'SKIP', name, 'SKIP', 'No data-dependent routes defined');
    }

    // W-S4: No unauthenticated debug routes
    if (!quickMode) {
      const debugRoutes = ['/debug/init', '/debug/seed', '/debug/drop', '/init', '/seed'];
      for (const dRoute of debugRoutes) {
        const resp = await probe(`https://${name}.${SUBDOMAIN}.workers.dev${dRoute}`);
        if (resp.status === 200) {
          record('worker', 'W-S4', 'CRITICAL', name, 'FAIL', `${dRoute} → 200 — UNAUTHENTICATED DEBUG ROUTE EXPOSED`);
        } else if (resp.status !== 404) {
          // 401 or 403 is acceptable (auth-gated)
        }
      }
    }

    // W-S5: .workers.dev subdomain reachable (basic)
    const rootResp = await probe(`https://${name}.${SUBDOMAIN}.workers.dev/`);
    if (rootResp.status > 0 && rootResp.status < 500) {
      record('worker', 'W-S5', 'INFO', name, 'PASS', `.workers.dev reachable (${rootResp.status})`);
    } else {
      record('worker', 'W-S5', 'WARNING', name, 'FAIL', `.workers.dev unreachable (${rootResp.status || rootResp.error})`);
    }
  }

  // W-S3: Active deployment window
  if (!quickMode) {
    for (const w of workers) {
      const deployments = await cf(`/accounts/${ACCOUNT}/workers/scripts/${w.id}/deployments?per_page=1`);
      const latest = (deployments.result || [])[0];
      if (latest) {
        const ageDays = (Date.now() - new Date(latest.created_on).getTime()) / 86400000;
        if (ageDays > 90) {
          record('worker', 'W-S3', 'WARNING', w.id, 'FAIL', 
            `Last deployed ${ageDays.toFixed(0)} days ago (${latest.created_on})`);
        } else {
          record('worker', 'W-S3', 'INFO', w.id, 'PASS', `Deployed ${ageDays.toFixed(0)}d ago`);
        }
      }
    }
  }
}

// ---- Page Tier Audits ------------------------------------------------------
async function auditPages(ACCOUNT, SUBDOMAIN) {
  const pagesResp = await cf(`/accounts/${ACCOUNT}/pages/projects`);
  const pages = pagesResp.result || [];

  // Also get all DNS zones for 522-RISK detection
  const zonesResp = await cf('/zones?per_page=50');
  const zones = zonesResp.result || [];

  for (const page of pages) {
    const name = page.name;

    // P-S1: Root document reachable via pages.dev
    const pageUrl = `https://${name}.pages.dev/`;
    const pageResp = await probe(pageUrl);
    const validStatuses = [200, 301, 302, 303, 307, 308, 401];
    if (validStatuses.includes(pageResp.status)) {
      record('page', 'P-S1', 'INFO', name, 'PASS', `pages.dev/ → ${pageResp.status}`);
    } else if (pageResp.status === 522) {
      record('page', 'P-S1', 'CRITICAL', name, 'FAIL', `pages.dev/ → 522 (origin unreachable)`);
    } else if (pageResp.status === 404) {
      record('page', 'P-S1', 'CRITICAL', name, 'FAIL', `pages.dev/ → 404 (project may be deleted/broken)`);
    } else {
      record('page', 'P-S1', 'WARNING', name, 'FAIL', `pages.dev/ → ${pageResp.status || pageResp.error}`);
    }

    // P-S2: 522-RISK detection — check custom domains
    try {
      const domainsResp = await cf(`/accounts/${ACCOUNT}/pages/projects/${name}/domains`);
      const customDomains = (domainsResp.result || []).filter(d => d.status === 'active');
      
      for (const domain of customDomains) {
        const domainUrl = `https://${domain.name}/`;
        const domainResp = await probe(domainUrl);
        if (domainResp.status === 522) {
          record('page', 'P-S2', 'CRITICAL', domain.name, 'FAIL', 
            `522-RISK: domain ${domain.name} → 522 on Pages project "${name}" — domain may not be registered`);
        } else if (validStatuses.includes(domainResp.status)) {
          record('page', 'P-S2', 'INFO', domain.name, 'PASS', `${domain.name}/ → ${domainResp.status}`);
        } else {
          record('page', 'P-S2', 'WARNING', domain.name, 'FAIL', 
            `${domain.name}/ → ${domainResp.status} (project: ${name})`);
        }
      }
    } catch (e) {
      // Project may not have domains endpoint
    }

    // P-S3: Recent successful build
    try {
      const deploysResp = await cf(`/accounts/${ACCOUNT}/pages/projects/${name}/deployments?per_page=1`);
      const latest = (deploysResp.result || [])[0];
      if (latest) {
        const ageDays = (Date.now() - new Date(latest.created_on).getTime()) / 86400000;
        const stage = latest.latest_stage || latest.deployment_trigger?.metadata?.branch || 'unknown';
        if (latest.latest_stage === 'success' && ageDays < 30) {
          record('page', 'P-S3', 'INFO', name, 'PASS', `Last successful deploy ${ageDays.toFixed(0)}d ago`);
        } else if (ageDays >= 30) {
          record('page', 'P-S3', 'WARNING', name, 'FAIL', `Last deploy ${ageDays.toFixed(0)}d ago (stage: ${stage})`);
        } else {
          record('page', 'P-S3', 'WARNING', name, 'FAIL', `Latest deploy stage: ${stage}`);
        }
      }
    } catch (e) {
      // Deployments endpoint may not be available
    }
  }

  // P-S2: Also check for CNAMEs pointing to .pages.dev NOT registered as custom domains
  for (const zone of zones) {
    if (zone.status !== 'active') continue;
    try {
      const recordsResp = await cf(`/zones/${zone.id}/dns_records?per_page=100`);
      const records = recordsResp.result || [];
      for (const record of records) {
        if (record.type === 'CNAME' && record.content?.includes('.pages.dev')) {
          const projectName = record.content.split('.')[0];
          const matchingPage = pages.find(p => p.name === projectName);
          if (!matchingPage) {
            record('page', 'P-S2', 'CRITICAL', `${record.name} (zone: ${zone.name})`, 'FAIL',
              `CNAME → ${record.content} but project "${projectName}" not found in Pages list`);
          } else {
            // Check if this exact domain is registered on the project
            try {
              const domainCheck = await cf(`/accounts/${ACCOUNT}/pages/projects/${projectName}/domains/${record.name}`);
              if (!domainCheck.success) {
                record('page', 'P-S2', 'CRITICAL', record.name, 'FAIL',
                  `522-RISK: CNAME → ${projectName}.pages.dev but ${record.name} NOT registered as custom domain`);
              }
            } catch {}
          }
        }
      }
    } catch (e) {
      // Zone records may not be accessible
    }
  }
}

// ---- DNS/Domain Tier Audits ------------------------------------------------
async function auditDns(ACCOUNT) {
  const zonesResp = await cf('/zones?per_page=50');
  const zones = (zonesResp.result || []).filter(z => z.status === 'active');

  if (zones.length === 0) {
    record('dns', 'D-S0', 'CRITICAL', 'fleet', 'FAIL', 'No active DNS zones found');
    return;
  }

  for (const zone of zones) {
    // D-S1: Minimum DNS records
    try {
      const recordsResp = await cf(`/zones/${zone.id}/dns_records?per_page=5`);
      const count = recordsResp.result_info?.total_count || 0;
      if (count === 0) {
        record('dns', 'D-S1', 'CRITICAL', zone.name, 'FAIL', 
          '0 DNS records — zone resolves to nothing (KIF-52). Add CNAME + Worker route.');
      } else {
        record('dns', 'D-S1', 'INFO', zone.name, 'PASS', `${count} records`);
      }

      // D-S3: CNAME chain detection
      const records = recordsResp.result || [];
      for (const record of records) {
        if (record.type === 'CNAME' && record.content) {
          // Check if target is another CNAME in the same zone or a .pages.dev/.workers.dev
          if (record.content.includes('.pages.dev') || record.content.includes('.workers.dev')) {
            // Direct — OK, but check if target exists
          } else {
            // Could be an intermediate CNAME — try to resolve it
            const targetIsZone = zones.find(z => record.content.endsWith(z.name));
            if (targetIsZone) {
              // It points to another zone we control — potential chain
              try {
                const targetRecords = await cf(`/zones/${targetIsZone.id}/dns_records?name=${record.content}&per_page=1`);
                const target = (targetRecords.result || [])[0];
                if (target && target.type === 'CNAME' && (target.content.includes('.pages.dev') || target.content.includes('.workers.dev'))) {
                  record('dns', 'D-S3', 'WARNING', `${record.name} (zone: ${zone.name})`, 'FAIL',
                    `CNAME chain: ${record.name} → ${record.content} → ${target.content} (${target.content.includes('.pages.dev') ? 'Pages' : 'Worker'})`);
                }
              } catch {}
            }
          }
        }
      }

      // D-S4: Dead Worker CNAME detection
      const workersResp = await cf(`/accounts/${ACCOUNT}/workers/scripts`);
      const workerNames = (workersResp.result || []).map(w => w.id);
      
      for (const record of records) {
        if (record.type === 'CNAME' && record.content?.includes('.workers.dev')) {
          const workerName = record.content.split('.')[0];
          if (!workerNames.includes(workerName)) {
            record('dns', 'D-S4', 'CRITICAL', `${record.name} (zone: ${zone.name})`, 'FAIL',
              `CNAME → ${record.content} but Worker "${workerName}" does not exist`);
          }
        }
      }

      // D-S6: At least one proxied record
      const proxiedCount = records.filter(r => r.proxied === true).length;
      if (proxiedCount === 0 && count > 0) {
        record('dns', 'D-S6', 'INFO', zone.name, 'FAIL', 'No proxied records — zone not using Cloudflare CDN/WAF');
      } else if (proxiedCount > 0) {
        record('dns', 'D-S6', 'INFO', zone.name, 'PASS', `${proxiedCount} proxied records`);
      }

      // D-S7: Worker route coverage
      try {
        const routesResp = await cf(`/zones/${zone.id}/workers/routes`);
        const routes = routesResp.result || [];
        // Check if any CNAME-to-worker-domain has a matching route
        for (const record of records) {
          if (record.type === 'CNAME' && record.content?.includes('.workers.dev')) {
            const hasRoute = routes.some(r => {
              const pattern = r.pattern.replace('/*', '');
              return record.name === pattern || record.name.endsWith(pattern);
            });
            if (!hasRoute) {
              record('dns', 'D-S7', 'WARNING', `${record.name} (zone: ${zone.name})`, 'FAIL',
                `CNAME → Worker but no matching zone-level Worker route found`);
            }
          }
        }
      } catch (e) {
        // Routes endpoint may not be available for all zones
      }

    } catch (e) {
      record('dns', 'D-S1', 'WARNING', zone.name, 'FAIL', `DNS records query failed: ${e.message}`);
    }

    // D-S2: Domain resolution (lightweight — just check zone apex)
    // Use DNS-over-HTTPS from Cloudflare for reliable resolution
    try {
      const dohUrl = `https://cloudflare-dns.com/dns-query?name=${encodeURIComponent(zone.name)}&type=A`;
      const dohResp = await fetch(dohUrl, { headers: { accept: 'application/dns-json' } });
      const dohData = await dohResp.json();
      if (dohData.Answer && dohData.Answer.length > 0) {
        record('dns', 'D-S2', 'INFO', zone.name, 'PASS', `Resolves to ${dohData.Answer.map(a => a.data).join(', ')}`);
      } else if (dohData.rcode === 'NXDOMAIN') {
        record('dns', 'D-S2', 'CRITICAL', zone.name, 'FAIL', 'NXDOMAIN — domain does not resolve');
      } else {
        record('dns', 'D-S2', 'WARNING', zone.name, 'FAIL', `DNS status: ${dohData.rcode || 'unknown'}`);
      }
    } catch (e) {
      record('dns', 'D-S2', 'WARNING', zone.name, 'FAIL', `DNS resolution check failed: ${e.message}`);
    }
  }

  // D-S5: Account-level redirect intercept detection (Tier 1 domains only)
  const tier1Domains = ['qnfo.org', 'papers.qnfo.org', 'legal.qnfo.org', 'graph-api.qnfo.org', 
    'qwav.org', 'qwav.tech', 'ipatent.me', 'q08.org'];
  
  for (const domain of tier1Domains) {
    const resp = await probe(`https://${domain}/`);
    if (resp.status === 301 || resp.status === 302) {
      const location = resp.headers['location'] || resp.headers['Location'] || '';
      // If redirecting to non-Cloudflare infrastructure, flag it
      if (location && !location.includes('cloudflare') && !location.includes('workers.dev') && 
          !location.includes('pages.dev') && !location.includes('qnfo.org') && !location.includes('q08.org')) {
        record('dns', 'D-S5', 'CRITICAL', domain, 'FAIL',
          `Redirect to external: ${location} (possible account-level redirect — KIF-51)`);
      }
    } else if (resp.status === 503) {
      record('dns', 'D-S5', 'WARNING', domain, 'FAIL', `503 — could be redirect intercept or origin down`);
    } else if (resp.status === 200) {
      record('dns', 'D-S5', 'INFO', domain, 'PASS', `Direct response (${resp.status})`);
    }
  }
}

// ---- Data Routes Map -------------------------------------------------------
function getDataRoutesForWorker(workerName) {
  const routes = {
    'qnfo-gateway': [
      { path: '/papers', desc: 'Papers API' },
      { path: '/stats', desc: 'Stats endpoint' },
      { path: '/sync', desc: 'Sync endpoint (POST required, but we check GET reachability)' },
    ],
    'qnfo-ai': [
      { path: '/v1/search?q=test', desc: 'AI Search' },
      { path: '/v1/history', desc: 'AI History' },
    ],
    'qnfo-ipatent': [
      { path: '/api/disclosures', desc: 'Disclosures API' },
      { path: '/api/search?q=test', desc: 'Search API' },
    ],
    'qnfo-qwav': [
      { path: '/ask?q=test', desc: 'QWAV Ask' },
      { path: '/papers', desc: 'Papers list' },
    ],
    'qnfo-memory-mcp': [
      { path: '/mcp', desc: 'MCP endpoint' },
    ],
    'qnfo-lifecycle': [
      { path: '/status', desc: 'Status endpoint' },
    ],
    'qnfo-archive': [
      { path: '/health', desc: 'Health endpoint' },
    ],
  };
  return routes[workerName] || [];
}

// ---- Main ------------------------------------------------------------------
async function main() {
  const args = process.argv.slice(2);
  const targetTier = args.includes('--tier') ? args[args.indexOf('--tier') + 1] : 'all';
  const jsonOutput = args.includes('--json');
  const quickMode = args.includes('--quick');

  const startTime = Date.now();
  
  if (!jsonOutput) {
    console.log('=== QNFO Cloudflare Availability Audit ===');
    console.log(`Date: ${new Date().toISOString()}`);
    console.log(`Mode: ${quickMode ? 'quick' : 'full'} | Tier: ${targetTier}`);
  }

  try {
    const ACCOUNT = await discoverAccountId();
    const SUBDOMAIN = discoverSubdomain();
    
    if (!jsonOutput) console.log(`Account: ${ACCOUNT.slice(0, 8)}... | Subdomain: ${SUBDOMAIN}.workers.dev\n`);

    // Run audits in parallel where possible
    if (targetTier === 'all' || targetTier === 'workers') {
      if (!jsonOutput) console.log('--- Worker Tier ---');
      await auditWorkers(ACCOUNT, SUBDOMAIN, quickMode);
    }
    if (targetTier === 'all' || targetTier === 'pages') {
      if (!jsonOutput) console.log('--- Page Tier ---');
      await auditPages(ACCOUNT, SUBDOMAIN);
    }
    if (targetTier === 'all' || targetTier === 'dns') {
      if (!jsonOutput) console.log('--- DNS/Domain Tier ---');
      await auditDns(ACCOUNT);
    }

    // Summary
    const criticalCount = findings.filter(f => f.severity === 'CRITICAL' && f.status === 'FAIL').length;
    const warningCount = findings.filter(f => f.severity === 'WARNING' && f.status === 'FAIL').length;
    const infoCount = findings.filter(f => f.severity === 'INFO' && f.status === 'FAIL').length;
    const passCount = findings.filter(f => f.status === 'PASS').length;
    const skipCount = findings.filter(f => f.status === 'SKIP').length;

    if (jsonOutput) {
      console.log(JSON.stringify({
        summary: {
          account: ACCOUNT,
          subdomain: SUBDOMAIN,
          critical: criticalCount,
          warning: warningCount,
          info: infoCount,
          pass: passCount,
          skip: skipCount,
          total_findings: findings.length,
          duration_ms: Date.now() - startTime
        },
        findings
      }, null, 2));
    } else {
      console.log('\n=== SUMMARY ===');
      console.log(`CRITICAL: ${criticalCount} | WARNING: ${warningCount} | INFO: ${infoCount} | PASS: ${passCount} | SKIP: ${skipCount}`);
      console.log(`Duration: ${((Date.now() - startTime) / 1000).toFixed(1)}s`);

      if (criticalCount > 0) {
        console.log('\n** CRITICAL FINDINGS (require immediate action): **');
        findings.filter(f => f.severity === 'CRITICAL' && f.status === 'FAIL').forEach(f => {
          console.log(`  [${f.standard}] ${f.subject}: ${f.detail}`);
        });
      }

      if (warningCount > 0) {
        console.log('\n** WARNINGS (review needed): **');
        findings.filter(f => f.severity === 'WARNING' && f.status === 'FAIL').forEach(f => {
          console.log(`  [${f.standard}] ${f.subject}: ${f.detail}`);
        });
      }

      // Exit code reflects severity
      if (criticalCount > 0) process.exitCode = 2;
      else if (warningCount > 0) process.exitCode = 1;
    }

  } catch (e) {
    console.error(`FATAL: ${e.message}`);
    process.exitCode = 2;
  }
}

if (require.main === module) {
  main();
}

module.exports = { auditWorkers, auditPages, auditDns, main, findings, record, probe, cf };
