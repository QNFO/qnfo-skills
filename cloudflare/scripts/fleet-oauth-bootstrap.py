#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fleet-oauth-bootstrap.py — PROGRAMMATIC first-time OAuth for Cloudflare MCP servers.

Completes the one-time browser OAuth flow for every server that has NO cached token,
without any DeepChat-settings toggling. For each server:
  1. GET discovery doc (.well-known/oauth-authorization-server)
  2. POST dynamic client registration (RFC 7591) with redirect_uri http://127.0.0.1:<port>/oauth/callback
  3. Generate PKCE verifier + S256 challenge
  4. Write <hash>_client_info.json + <hash>_code_verifier.txt (mcp-remote cache format)
  5. Start auto-exchange listener on <port> (zero-latency code exchange in-process)
  6. Print the auth URL to open (browser consent is the ONLY human step — one click per server)

Usage:
  python fleet-oauth-bootstrap.py --server cloudflare        # PoC for one server
  python fleet-oauth-bootstrap.py --list                     # list servers lacking tokens
  python fleet-oauth-bootstrap.py --all --port-base 23000    # prepare ALL servers

Exit codes: 0 = ok, 1 = error.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import threading
import http.server
import secrets
import base64

CACHE_DIR = os.path.expandvars(r"%USERPROFILE%\.mcp-auth\mcp-remote-0.1.37")

# All 15 OAuth Cloudflare MCP servers (cloudflare skill v3.41).
OAUTH_SERVERS = {
    "cloudflare":              "https://mcp.cloudflare.com/mcp",
    "cloudflare-bindings":     "https://bindings.mcp.cloudflare.com/mcp",
    "cloudflare-builds":       "https://builds.mcp.cloudflare.com/mcp",
    "cloudflare-observability":"https://observability.mcp.cloudflare.com/mcp",
    "cloudflare-radar":        "https://radar.mcp.cloudflare.com/mcp",
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


def url_hash(url: str) -> str:
    return hashlib.md5(url.encode("ascii")).hexdigest()


def server_host(url: str) -> str:
    """https://<sub>.mcp.cloudflare.com/mcp -> https://<sub>.mcp.cloudflare.com"""
    return url.rstrip("/").removesuffix("/mcp")


def http_json(url: str, method="GET", payload=None, headers=None, timeout=20):
    req_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
    }
    if headers:
        req_headers.update(headers)
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def discovery(server_url: str):
    """Fetch RFC 8414 discovery doc from the server origin."""
    origin = server_host(server_url)
    doc_url = f"{origin}/.well-known/oauth-authorization-server"
    try:
        return http_json(doc_url)
    except Exception:
        # Some servers only serve at /<issuer>/.well-known; fallback to /oauth/... defaults
        return {
            "issuer": origin,
            "authorization_endpoint": f"{origin}/oauth/authorize",
            "token_endpoint": f"{origin}/token",
            "registration_endpoint": f"{origin}/register",
        }


def register_client(disc, redirect_uri: str):
    reg = disc.get("registration_endpoint")
    if not reg:
        raise RuntimeError("no registration_endpoint in discovery")
    payload = {
        "redirect_uris": [redirect_uri],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
        "application_type": "native",
        "client_name": "DeepChat Agent Fleet Auth",
        "client_uri": "https://github.com/modelcontextprotocol/mcp-cli",
    }
    return http_json(reg, method="POST", payload=payload)


def pkce():
    verifier = secrets.token_urlsafe(64)[:100]
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("ascii")).digest()
    ).rstrip(b"=").decode("ascii")
    return verifier, challenge


def write_oauth_state(h, client_info, code_verifier):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(os.path.join(CACHE_DIR, f"{h}_client_info.json"), "w", encoding="utf-8") as f:
        json.dump(client_info, f, indent=2)
    with open(os.path.join(CACHE_DIR, f"{h}_code_verifier.txt"), "w", encoding="utf-8") as f:
        f.write(code_verifier)


def read_token(h):
    p = os.path.join(CACHE_DIR, f"{h}_tokens.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return None


def build_auth_url(disc, client_id, redirect_uri, code_challenge):
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{disc['authorization_endpoint']}?" + urllib.parse.urlencode(params)


class AutoExchangeHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if parsed.path != "/oauth/callback":
            self.send_response(404); self.end_headers(); return
        code = qs.get("code", [None])[0]
        error = qs.get("error", [None])[0]
        if error:
            self.send_response(400); self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "error": error}).encode())
            self.server.result = ("error", error)
            return
        if not code:
            self.send_response(400); self.end_headers()
            self.wfile.write(b'{"status":"error","error":"no code"}')
            return
        ctx = self.server.ctx
        try:
            data = urllib.parse.urlencode({
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": ctx["redirect_uri"],
                "client_id": ctx["client_id"],
                "code_verifier": ctx["code_verifier"],
            }).encode("ascii")
            req = urllib.request.Request(
                ctx["token_endpoint"], data=data, headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                    "User-Agent": "Mozilla/5.0",
                }, method="POST")
            with urllib.request.urlopen(req, timeout=20) as resp:
                token = json.loads(resp.read().decode("utf-8"))
            if "access_token" not in token:
                raise RuntimeError(f"no access_token: {token}")
            write_oauth_state(ctx["hash"], ctx["client_info"], ctx["code_verifier"])
            tmp = os.path.join(CACHE_DIR, f"{ctx['hash']}_tokens.json.tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(token, f, indent=2)
            os.replace(tmp, os.path.join(CACHE_DIR, f"{ctx['hash']}_tokens.json"))
            self.server.result = ("ok", token)
            self.send_response(200); self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        except Exception as e:
            self.server.result = ("error", str(e))
            self.send_response(500); self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode())
        finally:
            sys.stdout.write(f"CALLBACK:{self.server.result[0]}\n")
            sys.stdout.flush()

    def log_message(self, *a):
        pass


def prepare_server(name, server_url, port):
    h = url_hash(server_url)
    if read_token(h):
        print(f"[SKIP]      {name:36s} — token already cached")
        return None
    print(f"[PREPARE]   {name:36s} — {server_url}")
    disc = discovery(server_url)
    redirect_uri = f"http://127.0.0.1:{port}/oauth/callback"
    client = register_client(disc, redirect_uri)
    client_id = client.get("client_id")
    if not client_id:
        raise RuntimeError(f"registration returned no client_id: {client}")
    verifier, challenge = pkce()
    client_info = {
        "redirect_uris": [redirect_uri],
        "token_endpoint_auth_method": "none",
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "client_name": "DeepChat Agent Fleet Auth",
        "client_uri": "https://github.com/modelcontextprotocol/mcp-cli",
        "client_id": client_id,
        "client_id_issued_at": int(time.time()),
    }
    write_oauth_state(h, client_info, verifier)

    server = http.server.HTTPServer(("127.0.0.1", port), AutoExchangeHandler)
    server.ctx = {
        "hash": h,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_verifier": verifier,
        "token_endpoint": disc["token_endpoint"],
        "client_info": client_info,
    }
    server.result = None
    auth_url = build_auth_url(disc, client_id, redirect_uri, challenge)
    print(f"[LISTENER]  {name:36s} — port {port}, waiting for callback (auto-exchange)")
    print(f"[AUTH_URL]  {name:36s} -> {auth_url}")
    return server, auth_url


def run_sequential(targets, timeout_per=180):
    """Prepare + serve each target sequentially. Prints AUTH_URL for each; blocks
    until callback (auto-exchange) or timeout; continues to next target."""
    for name, url, port in targets:
        h = url_hash(url)
        if read_token(h):
            print(f"[SKIP]      {name:36s} — token already cached")
            continue
        try:
            prepared = prepare_server(name, url, port)
            if prepared is None:
                continue
            server, auth_url = prepared
            print(f"[BLOCKING]  {name:36s} — serving on port {port} until callback or {timeout_per}s timeout")
            sys.stdout.flush()
            server.timeout = timeout_per
            server.serve_forever()
            result = getattr(server, "result", None)
            if result and result[0] == "ok":
                print(f"[DONE]      {name:36s} — token cached + verified OK")
            else:
                print(f"[TIMEOUT]   {name:36s} — no callback within {timeout_per}s; retry by re-running")
            server.server_close()
        except Exception as e:
            print(f"[ERROR]     {name:36s} — {str(e)[:200]}")
        sys.stdout.flush()
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--server", help="server key to prepare (e.g. cloudflare)")
    ap.add_argument("--list", action="store_true", help="list servers lacking tokens")
    ap.add_argument("--all", action="store_true", help="prepare all servers lacking tokens")
    ap.add_argument("--port-base", type=int, default=23000)
    ap.add_argument("--timeout", type=int, default=180, help="seconds per server callback wait")
    args = ap.parse_args()

    if args.list:
        print("Servers WITHOUT cached token:")
        for name, url in OAUTH_SERVERS.items():
            if not read_token(url_hash(url)):
                print(f"  {name:36s} {url}")
        return 0

    targets = []
    if args.server:
        if args.server not in OAUTH_SERVERS:
            print(f"Unknown server: {args.server}. Known: {list(OAUTH_SERVERS)}")
            return 1
        targets = [(args.server, OAUTH_SERVERS[args.server], args.port_base)]
    elif args.all:
        port = args.port_base
        for name, url in OAUTH_SERVERS.items():
            if not read_token(url_hash(url)):
                targets.append((name, url, port))
                port += 1
    else:
        ap.print_help()
        return 1

    if not targets:
        print("No servers need OAuth bootstrap (all tokens cached).")
        return 0
    return run_sequential(targets, timeout_per=args.timeout)


if __name__ == "__main__":
    sys.exit(main())
