#!/usr/bin/env python3
"""IndexNow submission — fully automatable search-engine indexing, NO account needed.
Backed by Bing, Yandex, Seznam, Naver. Google uses robots.txt Sitemap: crawl instead.

PREREQ (one-time): host a key file at https://{host}/{key}.txt with content == key.
KEY FILE: C:\Users\LENOVO\qnfo-landing\fea6716717dc42059213070adcdf0e53.txt
(deployed to rwnq8.github.io + qnfo-landing.pages.dev, verified 2026-08-05).

Usage:
  python indexnow-submit.py                # submit both hosts with the QNFO key
  python indexnow-submit.py <host> <key>   # custom submission

NOTE: Google/Bing legacy sitemap ping endpoints are DEAD (404/410) — never use them.
Google discovery = robots.txt 'Sitemap:' line + crawl of linked sources.
"""
import json, sys, urllib.request, urllib.error

DEFAULT_KEY = 'fea6716717dc42059213070adcdf0e53'
DEFAULT_HOSTS = ['rwnq8.github.io', 'qnfo-landing.pages.dev']

def submit(host, key, url_list):
    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": url_list,
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        'https://api.indexnow.org/indexnow', data=data,
        headers={'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Mozilla/5.0'},
        method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode()[:100]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:200]

def main():
    if len(sys.argv) >= 3:
        hosts, key = [sys.argv[1]], sys.argv[2]
    else:
        hosts, key = DEFAULT_HOSTS, DEFAULT_KEY
    for host in hosts:
        urls = [f'https://{host}/', f'https://{host}/ai/', f'https://{host}/papers/']
        status, body = submit(host, key, urls)
        print(f'{host}: HTTP {status} {"(accepted)" if status == 202 else body}')

if __name__ == '__main__':
    main()
