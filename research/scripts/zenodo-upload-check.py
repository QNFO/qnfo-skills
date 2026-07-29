#!/usr/bin/env python3
"""Zenodo file upload diagnostic probe (KIF-44).

Creates a fresh micro-deposit, attempts a 1-byte PUT upload,
deletes the deposit. Returns exit code 0 if upload works,
exit code 1 if upload fails (backend down).

Usage: python zenodo-upload-check.py
Exit codes: 0 = upload OK, 1 = upload FAILED, 2 = auth/config error
"""
import os
import sys
import requests

TOKEN = os.environ.get('ZENODO_TOKEN', '')
if not TOKEN:
    print('[ZENODO-UPLOAD: NO_TOKEN]')
    sys.exit(2)

HEADERS = {'Authorization': f'Bearer {TOKEN}'}

# Step 1: Create fresh micro-deposit
try:
    r = requests.post('https://zenodo.org/api/deposit/depositions', json={}, headers=HEADERS, timeout=15)
    if r.status_code != 201:
        print(f'[ZENODO-UPLOAD: DEPOSIT_CREATE_FAILED] HTTP {r.status_code}: {r.text[:200]}')
        sys.exit(2)
    dep = r.json()
    deposit_id = dep['id']
    bucket_url = dep['links']['bucket']
except Exception as e:
    print(f'[ZENODO-UPLOAD: API_ERROR] {e}')
    sys.exit(2)

# Step 2: Attempt 1-byte upload
try:
    test_data = b'x'  # 1 byte
    r = requests.put(
        f'{bucket_url}/diagnostic-test.txt',
        headers=HEADERS,
        data=test_data,
        timeout=30
    )

    if r.status_code < 300:
        print(f'[ZENODO-UPLOAD: OK] 1-byte upload succeeded on deposit {deposit_id}')
        result = 0
    else:
        print(f'[ZENODO-UPLOAD: DOWN] 1-byte upload FAILED — HTTP {r.status_code}: {r.text[:200]}')
        print('[ZENODO-UPLOAD: DIAGNOSIS] Zenodo file storage backend is DOWN. Do NOT retry uploads.')
        result = 1
except Exception as e:
    print(f'[ZENODO-UPLOAD: ERROR] {e}')
    result = 1

# Step 3: Clean up — delete the diagnostic deposit
try:
    requests.delete(f'https://zenodo.org/api/deposit/depositions/{deposit_id}', headers=HEADERS, timeout=10)
except Exception:
    pass  # Best-effort cleanup

sys.exit(result)
