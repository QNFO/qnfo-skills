#!/usr/bin/env python3
"""Apply non-admin optimizations + queue admin items."""
import winreg, os, json, subprocess
from datetime import datetime

actions = []

# 1. DISABLE TRANSPARENCY
try:
    k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize',
        0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(k, 'EnableTransparency', 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(k)
    actions.append('Transparency: DISABLED')
except Exception as e:
    actions.append(f'Transparency: FAILED ({e})')

# 2-5. QUEUE ADMIN ITEMS
qdir = os.path.expandvars(r'%USERPROFILE%\.deepchat\admin_queue')
os.makedirs(qdir, exist_ok=True)

queue_items = [
    ('hibernate_off', 'Disable hibernation', [
        {'type': 'exec', 'program': 'powercfg', 'arguments': '/h off'}]),
    ('vbs_off', 'Disable VBS/HypervisorEnforcedCodeIntegrity', [
        {'type': 'exec', 'program': 'bcdedit', 'arguments': '/set hypervisorlaunchtype off'},
    ]),
]

skill_dir = os.path.expandvars(r'%USERPROFILE%\.deepchat\skills\bloat-cleanup\scripts')

for item_id, desc, commands in queue_items:
    ts = datetime.now().strftime('%H%M%S')
    job = {
        'id': f'{item_id}_{ts}',
        'type': item_id,
        'description': desc,
        'commands': commands
    }
    path = os.path.join(qdir, f'{job["id"]}.signal')
    with open(path, 'w') as f:
        json.dump(job, f, indent=2)
    actions.append(f'{desc}: QUEUED ({job["id"]})')

# Defender exclusions
ts = datetime.now().strftime('%H%M%S')
job = {
    'id': f'defender_{ts}',
    'type': 'defender_exclusions',
    'description': 'Add Defender exclusions for DeepChat',
    'script': os.path.join(skill_dir, 'defender_exclusions.py'),
    'arguments': ''
}
with open(os.path.join(qdir, f'{job["id"]}.signal'), 'w') as f:
    json.dump(job, f, indent=2)
actions.append(f'Defender exclusions: QUEUED ({job["id"]})')

# Dynamic service disable  
ts = datetime.now().strftime('%H%M%S')
job = {
    'id': f'svc_disable_{ts}',
    'type': 'dynamic_disable',
    'description': 'Disable bloatware services dynamically',
    'script': os.path.join(skill_dir, 'dynamic_disable.py'),
    'arguments': '--apply --confirm'
}
with open(os.path.join(qdir, f'{job["id"]}.signal'), 'w') as f:
    json.dump(job, f, indent=2)
actions.append(f'Service disable: QUEUED ({job["id"]})')

# AppX removal
ts = datetime.now().strftime('%H%M%S')
job = {
    'id': f'appx_{ts}',
    'type': 'remove_appx',
    'description': 'Remove AppX bloatware packages',
    'script': os.path.join(skill_dir, 'remove_appx.py'),
    'arguments': ''
}
with open(os.path.join(qdir, f'{job["id"]}.signal'), 'w') as f:
    json.dump(job, f, indent=2)
actions.append(f'AppX removal: QUEUED ({job["id"]})')

for a in actions:
    print(f'  {a}')
print(f'\n{len(actions)} actions applied/queued.')
print('Admin items processed by SYSTEM watcher within 60s.')
