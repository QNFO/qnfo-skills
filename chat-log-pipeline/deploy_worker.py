#!/usr/bin/env python3
"""deploy_worker.py - multipart PUT a Workers ES-module script via the CF API.

Usage: python deploy_worker.py <worker-name> <module-name> <js-file> [metadata.json]
Token: C:/Users/LENOVO/tokens/cloudflare (Bearer).
"""
import json, sys, uuid, urllib.request

ACCT = "edb167b78c9fb901ea5bca3ce58ccc4b"

def main():
    if len(sys.argv) < 4:
        print("usage: deploy_worker.py <worker-name> <module-name> <js-file> [metadata.json]")
        sys.exit(2)
    name, module, jsfile = sys.argv[1], sys.argv[2], sys.argv[3]
    metafile = sys.argv[4] if len(sys.argv) > 4 else None
    token = open(r"C:\Users\LENOVO\tokens\cloudflare", encoding="utf-8").read().strip()
    js = open(jsfile, "rb").read()
    meta = {"main_module": module,
            "compatibility_date": "2026-08-10",
            "compatibility_flags": ["nodejs_compat"]}
    if metafile:
        meta.update(json.load(open(metafile, encoding="utf-8")))
    b = uuid.uuid4().hex
    buf = bytearray()
    def part(name_, filename_, content, ctype):
        hdr = (f"--{b}\r\n"
               f'Content-Disposition: form-data; name="{name_}"; filename="{filename_}"\r\n'
               f"Content-Type: {ctype}\r\n\r\n").encode()
        buf.extend(hdr)
        buf.extend(content)
        buf.extend(b"\r\n")
    part("metadata", "metadata.json", json.dumps(meta).encode(), "application/json")
    part(module, module, js, "application/javascript+module")
    buf.extend(f"--{b}--\r\n".encode())
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/workers/scripts/{name}",
        data=bytes(buf), method="PUT",
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": f"multipart/form-data; boundary={b}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode()
    except urllib.error.HTTPError as e:
        print("HTTP", e.code)
        print(e.read().decode()[:2000])
        sys.exit(1)
    d = json.loads(raw)
    print("success:", d.get("success"))
    print("errors:", d.get("errors"))
    if d.get("success"):
        print("script_id:", d["result"]["id"])

if __name__ == "__main__":
    main()
