#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fleet-mcp-health-check.py — Read-only Cloudflare MCP fleet health audit.

Purpose: detect invalid_token / expired / missing-token fleet-wide states BEFORE
they surface as "Couldn't connect to cloudflare-observability" UI errors.
This is the proactive complement to fleet-oauth-refresh.py (which fixes, this one
flags). Add to the kaizen Autonomous Watchtower's INCIDENT-AXIS scan.

For each of the 17 Cloudflare MCP servers:
  - OAuth servers (14): check token cache exists + age vs expires_in; if token
    exists, probe MCP initialize (expect HTTP 200). No token -> [NO-TOKEN] warning.
  - Public servers (3): probe endpoint (expect HTTP 200).

Exit codes:
  0 = all live
  1 = warnings (no-token / expired / unverified)
  2 = hard failures (endpoint unreachable / probe 4xx/5xx with valid token)
"""
import hashlib
import json
import os
import sys
import time
import urllib.request
import urllib.error

CACHE_DIR = os.path.expandvars(r"%USERPROFILE%\.mcp-auth\mcp-remote-0.1.37")

# All 17 configured Cloudflare MCP servers (cloudflare skill v3.21).
OAUTH_SERVERS = {
    "cloudflare":              "https://mcp.cloudflare.com/mcp",
    "cloudflare-bindings":     "https://bindings.mcp.cloudflare.com/mcp",
    "cloudflare-builds":       "https://builds.mcp.cloudflare.com/mcp",
    "cloudflare-observability":"https://observability.mcp.cloudflare.com/mcp",
    "cloudflare-ai-gateway":   "https://ai-gateway.mcp.cloudflare.com/mcp",
    "cloudflare-graphql":      "https://graphql.mcp.cloudflare.com/mcp",
    "cloudflare-auditlogs":    "https://auditlogs.mcp.cloudflare.com/mcp",
    "cloudflare-logpush":      "https://logs.mcp.cloudflare.com/mcp",
    "cloudflare-browser-mcp-server": "https://browser.mcp.cloudflare.com/mcp",
    "dns-analytics":           "https://dns-analytics.mcp.cloudflare.com/mcp",
    "containers-mcp":          "https://containers.mcp.cloudflare.com/mcp",
    "cloudflare-casb-mcp-server": "https://casb.mcp.cloudflare.com/mcp",
    "cloudflare-autorag-mcp-server": "https://autorag.mcp.cloudflare.com/mcp",
    "dex-analysis":            "https://dex.mcp.cloudflare.com/mcp",
}
PUBLIC_SERVERS = {
    "cloudflare-docs":  "https://docs.mcp.cloudflare.com/mcp",
    "cloudflare-radar": "https://radar.mcp.cloudflare.com/mcp",
    "cloudflare-blog":  "https://blog.mcp.cloudflare.com/mcp",
}


def url_hash(url: str) -> str:
    return hashlib.md5(url.encode("ascii")).hexdigest()


def probe_mcp_initialize(server_url: str, access_token: str):
    """POST /mcp initialize. Returns (status_code, server_name_or_error)."""
    payload = json.dumps({
        "jsonrpc": "2.0", "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "fleet-health-check", "version": "1.0"}},
        "id": 1,
    }).encode("utf-8")
    req = urllib.request.Request(
        server_url, data=payload, headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, "OK"
    except urllib.error.HTTPError as e:
        body = ""
        if e.fp:
            try:
                body = e.read().decode("utf-8", errors="replace")[:150]
            except Exception:
                pass
        return e.code, body or e.reason
    except Exception as e:
        return 0, str(e)[:150]


def probe_public(url: str):
    """Streamable HTTP MCP endpoints REQUIRE POST — a GET returns 405/401 but that
    means the endpoint is LIVE. Per cloudflare skill MCP Verification Gate:
    401 = live (auth required), 404/530 = not deployed. Use POST initialize."""
    payload = json.dumps({
        "jsonrpc": "2.0", "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "fleet-health-check", "version": "1.0"}},
        "id": 1,
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload, headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "Mozilla/5.0",
        })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def main():
    if not os.path.isdir(CACHE_DIR):
        print("FATAL: mcp-remote cache dir missing:", CACHE_DIR)
        return 2

    print("=== CLOUDFLARE MCP FLEET HEALTH ===")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print()

    warnings = []
    failures = []
    healthy = 0

    for name, url in OAUTH_SERVERS.items():
        h = url_hash(url)
        token_file = os.path.join(CACHE_DIR, f"{h}_tokens.json")
        if not os.path.exists(token_file):
            warnings.append(name)
            print(f"[NO-TOKEN]  {name:36s} — no cached token (needs one-time browser OAuth)")
            continue
        try:
            with open(token_file, encoding="utf-8") as f:
                token = json.load(f)
            age = time.time() - os.path.getmtime(token_file)
            remaining = token.get("expires_in", 0) - age
            if remaining <= 0:
                # Refresh token may still make it valid; try the probe with access token
                pass
            status, detail = probe_mcp_initialize(url, token["access_token"])
            if status == 200:
                healthy += 1
                print(f"[HEALTHY]   {name:36s} — probe 200, token {remaining/60:.0f}m remaining")
            elif status == 401 or "invalid_token" in detail:
                warnings.append(name)
                print(f"[EXPIRED]   {name:36s} — probe {status} invalid_token (refresh scheduled 03:00 UTC)")
            else:
                failures.append((name, status, detail))
                print(f"[FAIL]      {name:36s} — probe {status}: {detail[:120]}")
        except Exception as e:
            failures.append((name, 0, str(e)))
            print(f"[FAIL]      {name:36s} — {str(e)[:120]}")

    for name, url in PUBLIC_SERVERS.items():
        code = probe_public(url)
        if code == 200:
            healthy += 1
            print(f"[PUBLIC]    {name:36s} — POST initialize HTTP {code}")
        elif code in (401, 403, 405):
            # Live endpoint responding; auth-variant behavior (normal per CF gate).
            healthy += 1
            print(f"[PUBLIC-LIVE] {name:35s} — POST initialize HTTP {code} (live, auth-gated)")
        else:
            failures.append((name, code, "public endpoint not live"))
            print(f"[FAIL]      {name:36s} — POST initialize HTTP {code} (404/530 = not deployed)")

    print()
    print("=== SUMMARY ===")
    print(f"Healthy:       {healthy}")
    print(f"Warnings:      {len(warnings)} -> {warnings if warnings else 'none'}")
    print(f"Failures:      {len(failures)}")
    for n, s, d in failures:
        print(f"  - {n}: HTTP {s} {d[:100]}")

    return 2 if failures else (1 if warnings else 0)


if __name__ == "__main__":
    sys.exit(main())
