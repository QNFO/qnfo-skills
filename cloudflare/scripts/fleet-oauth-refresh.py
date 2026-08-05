#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fleet-oauth-refresh.py — Cloudflare MCP fleet-wide OAuth token refresh.

Per cloudflare skill v3.23 §Token Refresh Protocol: every MCP server token cache
includes a refresh_token (offline_access scope). The grant_type=refresh_token
flow at each server's /token endpoint works server-side WITHOUT browser consent,
so a single script can renew ALL cached tokens.

Usage:
    python fleet-oauth-refresh.py [--dry-run] [--verify]

Behavior:
  - For each of the 14 known Cloudflare OAuth MCP servers:
      - If <hash>_tokens.json exists  -> refresh via refresh_token grant (rotates access+refresh)
      - If <hash>_client_info.json missing or no token -> report "NEEDS FIRST-TIME AUTH"
  - Writes refreshed token back to the same cache file (atomic).
  - Optional --verify: POST /mcp initialize with each refreshed token (Accept: application/json, text/event-stream).

Exit codes:
  0 = all cached tokens refreshed (or none cached)
  1 = at least one refresh failed
  2 = fatal (cache dir missing)
"""
import hashlib
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse

CACHE_DIR = os.path.expandvars(r"%USERPROFILE%\.mcp-auth\mcp-remote-0.1.37")

# The 14 OAuth MCP servers (from cloudflare skill v3.21 §DeepChat MCP Server Coverage).
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

DRY_RUN = "--dry-run" in sys.argv
VERIFY = "--verify" in sys.argv


def server_url_to_hash(url: str) -> str:
    return hashlib.md5(url.encode("ascii")).hexdigest()


def server_url_to_token_endpoint(url: str) -> str:
    """https://<sub>.mcp.cloudflare.com/mcp -> https://<sub>.mcp.cloudflare.com/token"""
    return url.rstrip("/").removesuffix("/mcp") + "/token"


def refresh_token(server_url: str, token: dict, client_id: str) -> dict:
    """Exchange refresh_token for a new token pair. Returns new token dict."""
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": token["refresh_token"],
        "client_id": client_id,
    }).encode("ascii")
    req = urllib.request.Request(
        server_url_to_token_endpoint(server_url),
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        new_token = json.loads(resp.read().decode("utf-8"))
    if "access_token" not in new_token:
        raise RuntimeError(f"refresh response missing access_token: {new_token}")
    return new_token


def verify_token(server_url: str, access_token: str) -> bool:
    """POST /mcp initialize -> expect HTTP 200 (Streamable HTTP, SSE accept)."""
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "fleet-oauth-refresh", "version": "1.0"},
        },
        "id": 1,
    }).encode("utf-8")
    req = urllib.request.Request(
        server_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status == 200
    except urllib.error.HTTPError:
        return False


def main():
    if not os.path.isdir(CACHE_DIR):
        print(f"FATAL: cache dir not found: {CACHE_DIR}")
        return 2

    print(f"=== CLOUDFLARE MCP FLEET OAuth REFRESH ===")
    print(f"Cache: {CACHE_DIR}")
    print(f"Mode: {'DRY-RUN' if DRY_RUN else 'LIVE'} | Verify: {VERIFY}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print()

    refreshed = []
    failed = []
    need_auth = []
    no_client = []

    for name, url in OAUTH_SERVERS.items():
        h = server_url_to_hash(url)
        token_file = os.path.join(CACHE_DIR, f"{h}_tokens.json")
        client_file = os.path.join(CACHE_DIR, f"{h}_client_info.json")

        if not os.path.exists(token_file):
            need_auth.append(name)
            print(f"[NO-TOKEN]  {name:36s} — needs first-time browser OAuth (disable/re-enable in MCP settings)")
            continue

        if not os.path.exists(client_file):
            no_client.append(name)
            print(f"[NO-CLIENT] {name:36s} — token exists but client_info missing; cannot refresh")
            continue

        try:
            with open(token_file, encoding="utf-8") as f:
                token = json.load(f)
            with open(client_file, encoding="utf-8") as f:
                client = json.load(f)
            client_id = client.get("client_id")
            if not client_id:
                raise RuntimeError("client_info missing client_id")

            if DRY_RUN:
                age = time.time() - os.path.getmtime(token_file)
                print(f"[DRY-RUN]   {name:36s} — token age {age/60:.0f}m, refresh_token present, would refresh")
                refreshed.append(name)
                continue

            new_token = refresh_token(url, token, client_id)

            # Atomic write: temp file then replace
            tmp = token_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(new_token, f, indent=2)
            os.replace(tmp, token_file)

            ok = "UNVERIFIED"
            if VERIFY:
                ok = "OK" if verify_token(url, new_token["access_token"]) else "VERIFY-FAIL"
            print(f"[REFRESHED] {name:36s} — {ok}, expires {new_token.get('expires_in', '?')}s, scope {str(new_token.get('scope',''))[:50]}")
            refreshed.append(name)
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="replace")[:200] if e.fp else str(e)
            failed.append((name, f"HTTP {e.code}: {msg}"))
            print(f"[FAILED]    {name:36s} — HTTP {e.code}: {msg}")
        except Exception as e:
            failed.append((name, str(e)))
            print(f"[FAILED]    {name:36s} — {e}")

    print()
    print("=== SUMMARY ===")
    print(f"Refreshed:    {len(refreshed)}")
    print(f"Failed:       {len(failed)}")
    print(f"Need first-time auth: {len(need_auth)}")
    if no_client:
        print(f"No client_info (manual fix): {len(no_client)} -> {no_client}")
    if failed:
        print("Failures:")
        for n, e in failed:
            print(f"  - {n}: {e[:120]}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
