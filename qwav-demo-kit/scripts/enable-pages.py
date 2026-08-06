#!/usr/bin/env python3
"""enable-pages.py — enable GitHub Pages for a repo via the native gh-pages branch.

Usage:
    python enable-pages.py QNFO/<repo-slug>

Prereq: gh CLI authenticated; gh-pages branch exists with index.html at root.
"""
import sys, json, urllib.request, subprocess

def gh_token():
    r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
    return r.stdout.strip()

def api(method, path, data=None):
    token = gh_token()
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(
        f"https://api.github.com{path}", data=body, method=method,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json",
                 "User-Agent": "interactive-poc-builder"})
    try:
        resp = urllib.request.urlopen(req, timeout=25)
        content = resp.read()
        try:
            return json.loads(content), resp.status
        except Exception:
            return content, resp.status
    except urllib.error.HTTPError as e:
        content = e.read()
        try:
            return json.loads(content), e.code
        except Exception:
            return content, e.code

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    repo = sys.argv[1]

    print(f"[1] Enabling Pages for {repo} (source=gh-pages)")
    d, s = api("PUT", f"/repos/{repo}/pages",
               {"source": {"branch": "gh-pages", "path": "/"}})
    print(f"    PUT /pages: HTTP {s}")
    if s == 200:
        print(f"    status: {d.get('status')}")
        print(f"    html_url: {d.get('html_url')}")
    elif s == 204:
        print("    HTTP 204 (ok, empty body)")
    else:
        print(f"    {d}")

    print("\n[2] Checking Pages config")
    d2, s2 = api("GET", f"/repos/{repo}/pages")
    print(f"    GET /pages: HTTP {s2}")
    if s2 == 200:
        print(f"    status: {d2.get('status')}")
        print(f"    html_url: {d2.get('html_url')}")

    print("\n[3] Checking recent builds")
    d3, s3 = api("GET", f"/repos/{repo}/actions/runs?per_page=5")
    if s3 == 200:
        for run in d3.get("workflow_runs", []):
            print(f"    - {run.get('name','?')} | {run.get('status','?')} "
                  f"| {run.get('conclusion','?')} | {run.get('head_branch','?')}")

if __name__ == "__main__":
    main()
