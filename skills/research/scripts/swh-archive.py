"""Archive QNFO GitHub repos to Software Heritage — permanent swh:1: identifiers.

SWH = the archival counterpart of DOIs for source code. Free, programmatic.

Correct API endpoints (verified 2026-08-05; the naive /origin/get/ 404s and
HTML-error responses when the origin param is not URL-encoded properly):
  CHECK:   GET  https://archive.softwareheritage.org/api/1/origin/get/?origin_url={urlencode(origin)}
  SAVE:    POST https://archive.softwareheritage.org/api/1/origin/save/   body: {"origin_url": origin}
           -> {"save_request_status": "accepted", "visit_type": "git", "save_task_status_url": ...}
  POLL:    GET  {save_task_status_url}  until "succeeded" -> then query
           GET  https://archive.softwareheritage.org/api/1/origin/visit/get/?origin_url=...&limit=1
  VISIT:   GET  https://archive.softwareheritage.org/api/1/origin/visit/get/?origin_url={urlencode(origin)}&limit=1
           -> "visit_id", "status": "full" when archived
  ID:      GET  https://archive.softwareheritage.org/api/1/visit/{visit_id}/directory/
           -> "swhid" like swh:1:dir:...

Usage:
  python swh-archive.py                      # check + save all 6 pinned QNFO repos
  python swh-archive.py --check-only         # just report archive status
  python swh-archive.py <github_url>         # single repo
"""
import json, sys, time, urllib.request, urllib.error, urllib.parse

SWH = 'https://archive.softwareheritage.org/api/1'
REPOS = [
    'https://github.com/rwnq8/aiq-bios',
    'https://github.com/rwnq8/Friend',
    'https://github.com/rwnq8/ultrametric-ai-poc',
    'https://github.com/rwnq8/unity-of-ultrametric-physics',
    'https://github.com/rwnq8/two-ways-of-measuring',
    'https://github.com/rwnq8/adelic-qft',
]
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
     'Content-Type': 'application/json'}

def api(method, path, body=None, timeout=60):
    url = SWH + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return r.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {'_raw': raw.decode('utf-8', 'replace')[:200]}
    except Exception as e:
        return 0, {'_err': str(e)}

def origin_status(origin):
    q = urllib.parse.quote(origin, safe='')
    st, d = api('GET', f'/origin/get/?origin_url={q}')
    if st == 200:
        return 'ARCHIVED', d
    if st == 404:
        return 'NOT_ARCHIVED', {}
    return f'UNKNOWN({st})', d

def request_save(origin):
    st, d = api('POST', '/origin/save/', {'origin_url': origin})
    return st, d

def visit_info(origin):
    q = urllib.parse.quote(origin, safe='')
    st, d = api('GET', f'/origin/visit/get/?origin_url={q}&limit=1')
    return st, d

def main():
    check_only = '--check-only' in sys.argv
    targets = REPOS
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        targets = [sys.argv[1]]
    if '--repo' in sys.argv:
        targets = [sys.argv[sys.argv.index('--repo') + 1]]

    for origin in targets:
        status, info = origin_status(origin)
        print(f'{origin}')
        print(f'  status: {status}')
        if status == 'ARCHIVED':
            visits = info.get('visits', [])
            vids = [v.get('visit_id') for v in visits]
            print(f'  visit_ids: {vids[:5]}')
            # try to get the swhid
            if vids:
                st2, d2 = api('GET', f'/visit/{vids[-1]}/directory/')
                swhid = d2.get('swhid', '?')
                print(f'  swhid: {swhid}')
            else:
                print(f'  swhid: ? (no visits)')
        elif status == 'NOT_ARCHIVED':
            if check_only:
                print(f'  NOT ARCHIVED — would request save (--check-only)')
            else:
                st, d = request_save(origin)
                print(f'  save request: HTTP {st} {json.dumps(d)[:200]}')
        else:
            print(f'  {json.dumps(info)[:200]}')
        time.sleep(2)

if __name__ == '__main__':
    main()
