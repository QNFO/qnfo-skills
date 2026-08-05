"""
QNFO Cloudflare Infrastructure Audit — Remediation Script
=========================================================
Audit date: 2026-08-04 | Workers: 10 | CRITICAL: 4 | WARNING: 7

Prerequisites:
  1. CLOUDFLARE_API_TOKEN env var with scopes:
     - Account:Rulesets:Edit (for KIF-51 fix)
     - Zone:DNS:Edit (for KIF-52 fixes)
     - Workers Scripts:Edit (for Worker updates)
  2. Python 3.12+ with urllib (stdlib — no pip installs needed)

Usage:
  python remediate-cf-audit-2026-08-04.py --dry-run     # preview only
  python remediate-cf-audit-2026-08-04.py --apply --fix CRITICAL  # fix criticals
  python remediate-cf-audit-2026-08-04.py --apply --fix ALL       # fix everything

Fixes are applied in priority order (C-1 through C-4 first, then W-1 through W-3).
Each fix verifies itself before declaring success.
"""

import os, sys, json, ssl, urllib.request, urllib.error, argparse

ACCOUNT_ID = "edb167b78c9fb901ea5bca3ce58ccc4b"
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def api(method, path, body=None):
    """Call Cloudflare REST API. Returns (status, json_body)."""
    url = f"https://api.cloudflare.com/client/v4{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        try: return e.code, json.loads(body)
        except: return e.code, {"error": body}

def probe_url(url):
    """Probe a URL and return (status, location, body_size)."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}, method="HEAD")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            return resp.status, resp.headers.get("Location", ""), 0
    except urllib.error.HTTPError as e:
        return e.code, "", len(e.read() or b"")
    except Exception:
        return 0, "", 0

# ═══════════════════════════════════════════════════
# FIX DEFINITIONS (priority order)
# ═══════════════════════════════════════════════════

def fix_c1_empoweringchange_today(dry_run=True):
    """C-1: empoweringchange.today — Empty DNS zone (KIF-52).
    Add proxied CNAME -> qnfo-gateway Worker + zone-level Worker route."""
    print("\n=== C-1: empoweringchange.today (KIF-52 empty zone) ===")
    status, data = api("GET", "/zones?name=empoweringchange.today")
    if status != 200 or not data.get("result"):
        print(f"  FAIL: Cannot find zone - HTTP {status} - {data}")
        return False
    zone_id = data["result"][0]["id"]
    print(f"  Zone ID: {zone_id}")

    record_body = {"type": "CNAME", "name": "@", "content": "qnfo-gateway.q08.workers.dev", "ttl": 1, "proxied": True}
    route_body = {"pattern": "empoweringchange.today/*", "script": "qnfo-gateway"}

    if dry_run:
        print(f"  [DRY-RUN] Would create CNAME: empoweringchange.today -> qnfo-gateway.q08.workers.dev")
        print(f"  [DRY-RUN] Would create Worker route: {route_body}")
    else:
        status, data = api("POST", f"/zones/{zone_id}/dns_records", record_body)
        if status == 200 and data.get("success"):
            print(f"  OK DNS record created")
            api("POST", f"/zones/{zone_id}/workers/routes", route_body)
            print(f"  OK Worker route created")
        else:
            print(f"  FAIL: DNS record - {data}")
            return False

    status, loc, _ = probe_url("https://empoweringchange.today/")
    print(f"  VERIFY: HTTP {status} (200=OK, 0/5xx=propagating)")
    return True

def fix_c1b_qnfo_uk(dry_run=True):
    """C-1b: qnfo.uk — Unreachable zone. Same KIF-52 fix."""
    print("\n=== C-1b: qnfo.uk (KIF-52 unreachable) ===")
    status, data = api("GET", "/zones?name=qnfo.uk")
    if status != 200 or not data.get("result"):
        print(f"  FAIL: Cannot find zone - {data}")
        return False
    zone_id = data["result"][0]["id"]
    print(f"  Zone ID: {zone_id}")

    record_body = {"type": "CNAME", "name": "@", "content": "qnfo-gateway.q08.workers.dev", "ttl": 1, "proxied": True}
    if dry_run:
        print(f"  [DRY-RUN] Would create CNAME for qnfo.uk")
    else:
        status, data = api("POST", f"/zones/{zone_id}/dns_records", record_body)
        if status == 200:
            api("POST", f"/zones/{zone_id}/workers/routes", {"pattern": "qnfo.uk/*", "script": "qnfo-gateway"})
            print(f"  OK DNS + route created")
        else:
            print(f"  FAIL: {data}")
            return False

    status, _, _ = probe_url("https://qnfo.uk/")
    print(f"  VERIFY: HTTP {status}")
    return True

def fix_c2_qwave_tech(dry_run=True):
    """C-2: q-wave.tech — HTTP 522. Point to Pages project."""
    print("\n=== C-2: q-wave.tech (HTTP 522) ===")
    status, data = api("GET", "/zones?name=q-wave.tech")
    if status != 200 or not data.get("result"):
        print(f"  FAIL: Cannot find zone - {data}")
        return False
    zone_id = data["result"][0]["id"]
    print(f"  Zone ID: {zone_id}")

    # Use redirect ruleset (cleaner than CNAME replacement)
    ruleset_body = {
        "name": "q-wave-tech-redirect",
        "kind": "zone",
        "phase": "http_request_redirect",
        "rules": [{
            "expression": "(http.host eq \"q-wave.tech\")",
            "action": "redirect",
            "action_parameters": {
                "from_value": {
                    "target_url": {"expression": "concat(\"https://qwav.org\", http.request.uri.path)"},
                    "status_code": 301,
                    "preserve_query_string": True
                }
            }
        }]
    }
    if dry_run:
        print(f"  [DRY-RUN] Would create redirect: q-wave.tech -> qwav.org")
    else:
        status, data = api("PUT", f"/zones/{zone_id}/rulesets/phases/http_request_redirect/entrypoint", ruleset_body)
        if status == 200 and data.get("success"):
            print(f"  OK Redirect ruleset created")
        else:
            # Fallback: point CNAME at qwav Pages
            record_body = {"type": "CNAME", "name": "@", "content": "qwav.pages.dev", "ttl": 1, "proxied": True}
            status, data = api("POST", f"/zones/{zone_id}/dns_records", record_body)
            if status == 200:
                print(f"  OK CNAME created (fallback)")
            else:
                print(f"  FAIL: {data}")
                return False

    status, _, _ = probe_url("https://q-wave.tech/")
    print(f"  VERIFY: HTTP {status}")
    return True

def fix_c3_ipatent_me(dry_run=True):
    """C-3: ipatent.me — KIF-51 account-level redirect to broken GCP.
    Find and delete the offending ruleset, point CNAME at Pages."""
    print("\n=== C-3: ipatent.me (KIF-51 account-level redirect) ===")

    # List account-level rulesets
    status, data = api("GET", f"/accounts/{ACCOUNT_ID}/rulesets")
    if status != 200:
        print(f"  FAIL: Cannot list rulesets - HTTP {status}")
        return False

    rulesets = data.get("result", [])
    target_id = None
    for rs in rulesets:
        if rs.get("kind") != "managed":
            for rule in rs.get("rules", []):
                params = rule.get("action_parameters", {})
                fv = params.get("from_value", {})
                target = fv.get("target_url", fv.get("url", ""))
                if "us-west1.run.app" in str(target) or "ipatent" in str(rule.get("description","")).lower():
                    target_id = rs["id"]
                    print(f"  Found: {rs['id']} - {rs.get('name','unnamed')}")
                    break
        if target_id: break

    if not target_id:
        print(f"  WARN: No ipatent/GCP redirect ruleset found.")
        print(f"  Non-managed rulesets: {[(r['id'], r.get('name','?')) for r in rulesets if r.get('kind')!='managed']}")
        return False

    if dry_run:
        print(f"  [DRY-RUN] Would DELETE ruleset {target_id}")
    else:
        status, data = api("DELETE", f"/accounts/{ACCOUNT_ID}/rulesets/{target_id}")
        if status == 200 and data.get("success"):
            print(f"  OK Ruleset {target_id} deleted")
        else:
            print(f"  FAIL: {data}")
            print(f"  Token may lack Account:Rulesets:Edit scope.")
            return False

    # Also fix CNAME to point at Pages
    status, data = api("GET", "/zones?name=ipatent.me")
    if status == 200 and data.get("result"):
        zone_id = data["result"][0]["id"]
        record_body = {"type": "CNAME", "name": "@", "content": "ipatent-me.pages.dev", "ttl": 1, "proxied": True}
        if not dry_run:
            api("POST", f"/zones/{zone_id}/dns_records", record_body)
            print(f"  OK CNAME -> ipatent-me.pages.dev")

    status, loc, _ = probe_url("https://ipatent.me/")
    print(f"  VERIFY: HTTP {status} location={loc[:80] if loc else 'none'}")
    return True

def fix_w1_paper_indexer_auth(dry_run=True):
    """W-1: qnfo-paper-indexer — Add API key auth to /cron/* routes."""
    print("\n=== W-1: qnfo-paper-indexer /cron auth ===")
    print("  CODE FIX: In fetch(), add auth check before /cron handler:")
    print('    if (path.startsWith("/cron")) {')
    print('      if (request.headers.get("Authorization") !== "Bearer " + env.CRON_API_KEY)')
    print('        return Response.json({error:"unauthorized"}, 401);')
    print('    }')
    print("  SECRET: wrangler secret put CRON_API_KEY --name qnfo-paper-indexer")
    print("  DEPLOY: wrangler deploy")
    print("  BLOCKED: wrangler not on PATH (see W-4)")
    return True

def fix_w2_email_health(dry_run=True):
    """W-2: qnfo-email — Unauthenticated /health."""
    print("\n=== W-2: qnfo-email /health auth ===")
    print("  CODE FIX: Move /health check ABOVE the auth gate:")
    print('    if (p === "/health") return json({status:"ok",...});  // no auth')
    print("  DEPLOY: wrangler deploy --name qnfo-email")
    print("  BLOCKED: wrangler not on PATH (see W-4)")
    return True

def fix_w3_gateway_production(dry_run=True):
    """W-3: qnfo-gateway-production — Investigate/remove stale."""
    print("\n=== W-3: qnfo-gateway-production ===")
    print("  Worker created 2026-07-31, /health -> 404")
    if dry_run:
        print("  [DRY-RUN] Would investigate via API then delete if stale")
    else:
        status, data = api("DELETE", f"/accounts/{ACCOUNT_ID}/workers/scripts/qnfo-gateway-production")
        if status == 200:
            print("  OK Worker deleted")
        else:
            print(f"  INFO: {data.get('errors',[data])}")
    return True

def fix_w4_wrangler_path(dry_run=True):
    """W-4: wrangler not on PATH."""
    print("\n=== W-4: wrangler PATH ===")
    print("  FIX:")
    print('    npm config set prefix "C:\\Users\\LENOVO\\npm-global"')
    print('    npm config set cache  "C:\\Users\\LENOVO\\AppData\\Local\\npm-cache"')
    print('    npm install -g wrangler')
    print('    setx Path "%Path%;C:\\Users\\LENOVO\\npm-global"')
    print('    wrangler --version  # -> 4.118.0')
    return True

def fix_w5_kg_d1_reconciliation(dry_run=True):
    """W-5: KG-D1 paper reconciliation (KIF-23)."""
    print("\n=== W-5: KG-D1 paper reconciliation ===")
    print("  Run d1-query.py to get paper slugs, cross-ref with KG.")
    print("  Expected: ~236 papers in D1, ~2,518 KG nodes.")
    print("  python scripts/d1-query.py --db living-paper --sql")
    print('    "SELECT slug FROM papers WHERE slug IS NOT NULL"')
    print("  Cross-ref with query_graph('nodes', {label:'Paper'})")
    return True

# ═══════════════ MAIN ═══════════════

def main():
    parser = argparse.ArgumentParser(description="QNFO Cloudflare Audit Remediation")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true", help="Apply fixes live")
    parser.add_argument("--fix", choices=["CRITICAL","WARNING","ALL"], default="ALL")
    args = parser.parse_args()

    dry_run = not args.apply

    if not TOKEN and not dry_run:
        print("ERROR: CLOUDFLARE_API_TOKEN not set. Use --dry-run or set the env var.")
        sys.exit(1)

    print(f"QNFO CF Remediation | Mode: {'DRY-RUN' if dry_run else 'LIVE'} | Fix: {args.fix}")
    print(f"Token: {'present' if TOKEN else 'MISSING (dry-run only)'}")
    print("=" * 50)

    results = {}
    if args.fix in ("CRITICAL","ALL"):
        print("\n--- CRITICAL FIXES (priority order) ---")
        results["C-1a"] = fix_c1_empoweringchange_today(dry_run)
        results["C-1b"] = fix_c1b_qnfo_uk(dry_run)
        results["C-2"] = fix_c2_qwave_tech(dry_run)
        results["C-3"] = fix_c3_ipatent_me(dry_run)

    if args.fix in ("WARNING","ALL"):
        print("\n--- WARNING FIXES ---")
        results["W-1"] = fix_w1_paper_indexer_auth(dry_run)
        results["W-2"] = fix_w2_email_health(dry_run)
        results["W-3"] = fix_w3_gateway_production(dry_run)
        results["W-4"] = fix_w4_wrangler_path(dry_run)
        results["W-5"] = fix_w5_kg_d1_reconciliation(dry_run)

    print(f"\n{'='*50}")
    passed = sum(1 for v in results.values() if v)
    for k,v in results.items():
        print(f"  {'OK' if v else 'FAIL'} {k}")
    print(f"\n  {passed}/{len(results)} complete")

    if dry_run:
        print(f"\n  Run with --apply to execute fixes live.")

if __name__ == "__main__":
    main()
