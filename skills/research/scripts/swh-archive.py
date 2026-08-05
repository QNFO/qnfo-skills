#!/usr/bin/env python3
"""Archive QNFO GitHub repos to Software Heritage — permanent swh:1: identifiers.

SCHEMA VERIFIED LIVE 2026-08-05 (session 3i_KVLownViukLTZB_BJ1):

1. ANUBIS ANTI-BOT (critical): archive.softwareheritage.org is behind Anubis
   proof-of-work. A plain urllib/curl client gets an HTML challenge page
   ("Making sure you're not a bot!"), NOT JSON. MUST drive via a real browser
   (session browser / CDP) — once the browser solves Anubis, same-origin fetch
   carries the cookie and API calls work.

2. ORIGIN CHECK (browser-context fetch):
   GET /api/1/origin/get/?origin_url={encodeURIComponent(origin)}
   -> 200 {"origin":{"url":...}} = ARCHIVED | 404 {"detail":"Origin ... not found"} = NOT ARCHIVED

3. SAVE REQUEST (browser-context fetch):
   POST /api/1/origin/save/  body: {"origin_url": origin, "visit_type": "git"}
   -> {"save_request_status":"accepted", "visit_type":"git", ...}
   REQUIRED fields: origin_url AND visit_type. The GitHub-specific endpoint
   /origin/save/github/url/ REJECTS visit_type=github ("Allowed types: bzr, cvs, git, hg, svn, tarball").

4. RATE LIMIT: unauthenticated save requests are throttled ~50/day burst-limited.
   429 {"exception":"Throttled","reason":"Expected available in N seconds"}.
   Respect it — hammering triggers harder blocks (same discipline as
   WIKIDATA-ABUSE-FILTER-296-1). Save requests queue server-side; a submitted
   request WILL be processed when the throttle clears.

5. swh:1: ID: after processing, GET /api/1/origin/visit/get/?origin_url=...&limit=1
   -> visit_id -> GET /api/1/visit/{visit_id}/directory/ -> "swhid"

Verified state 2026-08-05: all 6 pinned QNFO repos (aiq-bios, Friend,
ultrametric-ai-poc, unity-of-ultrametric-physics, two-ways-of-measuring,
adelic-qft) confirmed NOT ARCHIVED; save requests submitted via browser session;
throttled after burst (~58 min cooldown). Retry after cooldown.

Usage:
  python swh-archive.py              # print this doc (needs browser context, not plain exec)
"""
import sys

DOC = __doc__

def main():
    print(DOC)
    print('\nNOTE: This script documents the SWH API flow; execution REQUIRES a browser')
    print('session (Anubis challenge). Use the CDP/browser flow documented above.')
    print('\nRepos (all confirmed NOT ARCHIVED 2026-08-05, saves throttled):')
    for r in ['aiq-bios', 'Friend', 'ultrametric-ai-poc',
              'unity-of-ultrametric-physics', 'two-ways-of-measuring', 'adelic-qft']:
        print(f'  https://github.com/rwnq8/{r}')

if __name__ == '__main__':
    main()
