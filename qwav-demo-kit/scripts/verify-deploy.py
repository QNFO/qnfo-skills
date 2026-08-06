#!/usr/bin/env python3
"""verify-deploy.py — same-turn live deployment verification.

Usage:
    python verify-deploy.py <url> [--marker ENGINE_MARKER]

Example:
    python verify-deploy.py https://qnfo.github.io/qwav-demo-bt-qec/ --marker BTTree

Notes:
    - cmd.exe splits "class BTTree" into two args with literal quotes, so
      prefer a single-token marker (e.g. BTTree) OR pass multiple tokens
      and they will be joined (quotes stripped).
    - MUST run in the same turn as any "deployed"/"live" claim.
"""
import sys, urllib.request


def _clean(tok):
    """Strip surrounding quotes cmd.exe leaves on quoted args."""
    return tok.strip('"').strip("'").strip()


def verify(url, marker=None):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        r = urllib.request.urlopen(req, timeout=20)
        body = r.read()
        ok = r.status == 200 and len(body) > 0
        marker_found = None
        if marker and ok:
            marker_found = marker.encode() in body
            ok = marker_found
        print(f"{url}: HTTP {r.status} | {len(body):,} bytes | "
              f"marker={'FOUND' if marker_found else ('n/a' if not marker else 'MISSING')}")
        print(f"VERIFIED: {'YES' if ok else 'NO'}")
        return 0 if ok else 1
    except urllib.error.HTTPError as e:
        print(f"{url}: HTTP {e.code} — {e.reason}")
        print("VERIFIED: NO")
        return 1
    except Exception as e:
        print(f"{url}: ERROR — {e}")
        print("VERIFIED: NO")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    url = sys.argv[1]
    marker = None
    if "--marker" in sys.argv:
        idx = sys.argv.index("--marker")
        # join all tokens after --marker, stripping cmd.exe quote artifacts
        marker = " ".join(_clean(t) for t in sys.argv[idx + 1:]) or None
    sys.exit(verify(url, marker))
