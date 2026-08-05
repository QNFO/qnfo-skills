#!/usr/bin/env python3
"""Budget Laptop Tuner — comprehensive Windows + DeepChat optimization for 6GB-RAM laptops.

KIF-50: 2026-07-29 red-team kaizen. Consolidates all budget-laptop optimizations
into a single diagnostic + action script. Runs read-only audit by default;
--apply performs non-admin optimizations and queues admin items.

Covers:
- System state audit (RAM, disk, services, startup, VBS, visual effects)
- Non-admin optimizations (transparency, startup cleanup, power plan, config)
- Admin queue (hibernation, VBS/Memory Integrity, visual effects, defender,
  service disable, AppX removal, Game Mode)
- DeepChat-specific (agent.db status, config .bak files, settings audit)
- Recommendations report

Usage:
    python budget_laptop_tune.py              # Audit only
    python budget_laptop_tune.py --apply      # Apply non-admin + queue admin
    python budget_laptop_tune.py --json       # Machine-readable output
"""
import os, sys, json, time, shutil, subprocess, ctypes
from datetime import datetime

ROAMING = os.path.expandvars(r'%APPDATA%\DeepChat')
DB_PATH = os.path.join(ROAMING, 'app_db', 'agent.db')


def fmt_size(b):
    for u in ['B', 'KB', 'MB', 'GB']:
        if b < 1024: return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} TB"


def get_disk_info():
    drives = {}
    for d in ['C:\\', 'D:\\']:
        try:
            total, used, free = shutil.disk_usage(d)
            drives[d] = {'total': total, 'used': used, 'free': free, 'pct': free/total*100}
        except: pass
    return drives


def get_ram_info():
    try:
        import ctypes
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [('dwLength', ctypes.c_ulong), ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', ctypes.c_ulonglong), ('ullAvailPhys', ctypes.c_ulonglong),
                        ('ullTotalPageFile', ctypes.c_ulonglong), ('ullAvailPageFile', ctypes.c_ulonglong),
                        ('ullTotalVirtual', ctypes.c_ulonglong), ('ullAvailVirtual', ctypes.c_ulonglong),
                        ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]
        m = MEMORYSTATUSEX()
        m.dwLength = ctypes.sizeof(m)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        return {'total_mb': m.ullTotalPhys / 1024**2, 'avail_mb': m.ullAvailPhys / 1024**2,
                'load_pct': m.dwMemoryLoad, 'total_pagefile_mb': m.ullTotalPageFile / 1024**2,
                'avail_pagefile_mb': m.ullAvailPageFile / 1024**2}
    except: return {'total_mb': 0}


def get_reg(key_path, value_name, hive=None):
    import winreg
    hives = {'HKLM': winreg.HKEY_LOCAL_MACHINE, 'HKCU': winreg.HKEY_CURRENT_USER}
    try:
        k = winreg.OpenKey(hives.get(hive, winreg.HKEY_CURRENT_USER), key_path)
        v, _ = winreg.QueryValueEx(k, value_name)
        winreg.CloseKey(k)
        return v
    except: return None


def set_reg(key_path, value_name, value, hive=None, type_hint='dword'):
    import winreg
    hives = {'HKLM': winreg.HKEY_LOCAL_MACHINE, 'HKCU': winreg.HKEY_CURRENT_USER}
    try:
        k = winreg.CreateKey(hives.get(hive, winreg.HKEY_CURRENT_USER), key_path)
        if type_hint == 'dword':
            winreg.SetValueEx(k, value_name, 0, winreg.REG_DWORD, value)
        else:
            winreg.SetValueEx(k, value_name, 0, winreg.REG_SZ, str(value))
        winreg.CloseKey(k)
        return True
    except Exception as e:
        return False


def queue_admin(item_type, description, commands=None, script_path=None, args=None):
    """Queue an admin operation for the SYSTEM watcher to process."""
    queue_dir = os.path.expandvars(r'%USERPROFILE%\.deepchat\admin_queue')
    os.makedirs(queue_dir, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    job_id = f"budget_tune_{ts}_{item_type}"
    
    job = {'id': job_id, 'type': item_type, 'description': description, 'created_at': ts}
    if commands:
        job['commands'] = commands
    if script_path:
        job['script'] = script_path
    if args:
        job['arguments'] = args
    
    signal_path = os.path.join(queue_dir, f"{job_id}.signal")
    with open(signal_path, 'w', encoding='utf-8') as f:
        json.dump(job, f, indent=2)
    return job_id, signal_path


def audit():
    """Collect full system state. Returns dict of findings."""
    f = {'timestamp': datetime.now().isoformat(), 'recommendations': [], 'actions_applied': []}
    
    # ── RAM ──
    ram = get_ram_info()
    f['ram'] = ram
    if ram.get('avail_mb', 0) < 1024:
        f['recommendations'].append({'item': 'RAM critically low', 'detail': f"Only {ram['avail_mb']:.0f} MB free of {ram['total_mb']:.0f} MB", 'severity': 'critical', 'action': 'Close unused apps, consider VBS off'})
    
    # ── Disk ──
    f['disk'] = get_disk_info()
    c = f['disk'].get('C:\\', {})
    if c.get('pct', 100) < 20:
        f['recommendations'].append({'item': 'C: drive low space', 'detail': f"{c['pct']:.1f}% free ({fmt_size(c['free'])})", 'severity': 'warning', 'action': 'VACUUM agent.db, disable hibernation, clean disk'})
    
    # ── Power plan ──
    try:
        r = subprocess.run(['powercfg', '/getactivescheme'], capture_output=True, text=True, timeout=5)
        plan = r.stdout
        f['power_plan'] = 'High Performance' if '8c5e7fda' in plan else ('Balanced' if '381b4222' in plan else 'other')
    except: f['power_plan'] = 'unknown'
    if f['power_plan'] != 'High Performance':
        f['recommendations'].append({'item': 'Power plan not High Performance', 'detail': f'Current: {f["power_plan"]}', 'severity': 'info', 'action': 'powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'})
    
    # ── Hibernation ──
    try:
        r = subprocess.run(['powercfg', '/a'], capture_output=True, text=True, timeout=5)
        f['hibernation_enabled'] = 'Hibernate' in r.stdout and 'not been disabled' not in r.stdout
    except: f['hibernation_enabled'] = 'unknown'
    if f['hibernation_enabled']:
        hiber_size = ram.get('total_mb', 6144) * 0.75 / 1024
        f['recommendations'].append({'item': 'Hibernation enabled', 'detail': f'hiberfil.sys ≈ {hiber_size:.1f} GB (75% of RAM)', 'severity': 'high', 'action': 'powercfg /h off (admin)', 'needs_admin': True})
    
    # ── Pagefile ──
    try:
        r = subprocess.run(['wmic', 'pagefile', 'get', 'AllocatedBaseSize,Description'], capture_output=True, text=True, timeout=5)
        f['pagefile'] = r.stdout.strip()
    except: f['pagefile'] = 'unknown'
    
    # ── Visual effects ──
    vfx = get_reg('Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects', 'VisualFXSetting')
    f['visual_effects'] = {None: 'not set', 0: 'Let Windows choose', 1: 'Best appearance', 2: 'Best performance', 3: 'Custom'}.get(vfx, 'unknown')
    if vfx not in (2, None):  # 2=BestPerformance
        f['recommendations'].append({'item': 'Visual effects not set to Best Performance', 'detail': f'Current: {f["visual_effects"]}', 'severity': 'info', 'action': 'Set to Best Performance in System Properties'})
    
    # ── Transparency ──
    trans = get_reg('Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize', 'EnableTransparency')
    f['transparency'] = trans
    if trans == 1:
        f['recommendations'].append({'item': 'Transparency effects enabled', 'detail': 'Minor GPU/RAM overhead', 'severity': 'low', 'action': 'Disable in Personalization settings'})
    
    # ── Game DVR/Game Mode ──
    gdv = get_reg('System\\GameConfigStore', 'GameDVR_Enabled')
    f['game_dvr'] = gdv
    
    # ── VBS/Device Guard ──
    try:
        r = subprocess.run(['msinfo32', '/report', '%TEMP%\\msinfo.nfo'], capture_output=True, timeout=10)
    except: pass
    # Quick check via bcdedit (needs admin for full output)
    vbs_cred = get_reg('SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\HypervisorEnforcedCodeIntegrity', 'Enabled', hive='HKLM')
    f['vbs_enabled'] = vbs_cred == 1
    
    # ── Agent.db ──
    if os.path.exists(DB_PATH):
        db_size = os.path.getsize(DB_PATH)
        f['agent_db'] = {'size': db_size, 'size_str': fmt_size(db_size)}
        import sqlite3
        conn = sqlite3.connect('file:'+DB_PATH+'?mode=ro', uri=True)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM new_sessions')
        f['agent_db']['sessions'] = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM deepchat_tape_entries')
        f['agent_db']['tape_entries'] = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM new_sessions WHERE is_pinned=1')
        f['agent_db']['pinned'] = c.fetchone()[0]
        conn.close()
        
        if db_size > 1024**3:  # >1 GB
            f['recommendations'].append({'item': 'agent.db still >1 GB', 'detail': f'{db_size/1024**3:.1f} GB — VACUUM needed', 'severity': 'high', 'action': 'Close DeepChat, run vacuum_only.py'})
    
    # ── Config files ──
    configs = {}
    for fn in ['app-settings.json', 'mcp-settings.json', 'custom_prompts.json', 'system_prompts.json']:
        fp = os.path.join(ROAMING, fn)
        if os.path.exists(fp):
            configs[fn] = os.path.getsize(fp)
    f['config_files'] = configs
    
    # ── Running processes (memory hogs) ──
    try:
        r = subprocess.run(
            ['powershell', '-NoProfile', '-Command',
             "Get-Process | Sort-Object -Descending WorkingSet64 | Select-Object -First 10 Name,Id,@{N='MB';E={[math]::Round($_.WorkingSet64/1MB,1)}} | ConvertTo-Json -Compress"],
            capture_output=True, text=True, timeout=15)
        f['top_processes'] = json.loads(r.stdout) if r.stdout else []
    except: f['top_processes'] = []
    
    # ── Startup items ──
    try:
        r = subprocess.run(['wmic', 'startup', 'get', 'caption,command'], capture_output=True, text=True, timeout=5)
        f['startup_items'] = [l.strip() for l in r.stdout.split('\n') if l.strip()][1:6]
    except: f['startup_items'] = []
    
    # ── DeepChat specific ──
    dc_processes = 0
    dc_ram = 0
    for p in f.get('top_processes', []):
        if isinstance(p, dict) and 'Name' in p and p.get('Name') == 'DeepChat':
            dc_processes += 1
            dc_ram += p.get('MB', 0)
    f['deepchat_processes'] = dc_processes
    f['deepchat_ram_mb'] = round(dc_ram, 1)
    
    if dc_ram > 1500:
        f['recommendations'].append({'item': f'DeepChat using {dc_ram:.0f} MB across {dc_processes} processes', 'detail': f'{dc_ram/ram.get("total_mb", 6144)*100:.0f}% of total RAM', 'severity': 'warning', 'action': 'Consider closing unused tabs/windows, reduce context in Settings'})
    
    return f


def apply_non_admin():
    """Apply all non-admin optimizations. Returns list of actions."""
    actions = []
    
    # 1. Set power plan to High Performance
    r = subprocess.run(['powercfg', '/setactive', '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'], capture_output=True)
    if r.returncode == 0:
        actions.append({'action': 'power_plan', 'result': 'Set to High Performance'})
    
    # 2. Disable transparency
    if set_reg('Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize', 'EnableTransparency', 0):
        actions.append({'action': 'transparency', 'result': 'Disabled'})
    
    # 3. Clean DeepChat .bak files
    bak_count = 0
    bak_size = 0
    for f in os.listdir(ROAMING):
        if f.endswith('.bak'):
            fp = os.path.join(ROAMING, f)
            bak_size += os.path.getsize(fp)
            bak_count += 1
            os.remove(fp)
    if bak_count > 0:
        actions.append({'action': 'clean_bak', 'result': f'Removed {bak_count} .bak files ({fmt_size(bak_size)})'})
    
    # 4. Queue admin operations
    admin_queue = []
    # (item_type, description, commands_list_OR_None, script_path_OR_None, args_OR_None)
    admin_queue.append(('hibernate_off', 'Disable hibernation (powercfg /h off)', 
        [{'type': 'exec', 'program': 'powercfg', 'arguments': '/h off'}], None, None))
    admin_queue.append(('vbs_off', 'Disable VBS / Hypervisor Enforced Code Integrity',
        [{'type': 'exec', 'program': 'bcdedit', 'arguments': '/set hypervisorlaunchtype off'}], None, None))
    admin_queue.append(('defender_exclusions', 'Add Defender exclusions for DeepChat paths',
        None, os.path.join(os.path.dirname(__file__), 'defender_exclusions.py'), ''))
    admin_queue.append(('service_disable', 'Dynamic service disable (bloatware)',
        None, os.path.join(os.path.dirname(__file__), 'dynamic_disable.py'), '--apply --confirm'))
    admin_queue.append(('appx_remove', 'Remove AppX bloatware packages',
        None, os.path.join(os.path.dirname(__file__), 'remove_appx.py'), ''))
    
    for item_type, desc, commands, script, args in admin_queue:
        kw = {'commands': [{'type': 'exec', 'program': 'powercfg', 'arguments': '/h off'}]} if commands else {}
        if script:
            kw['script_path'] = script
            kw['args'] = args
        jid, _ = queue_admin(item_type, desc, **{k: v for k, v in kw.items() if v})
        actions.append({'action': item_type, 'result': f'Queued: {desc} (job: {jid})'})
    
    return actions


if __name__ == '__main__':
    apply = '--apply' in sys.argv
    json_out = '--json' in sys.argv
    
    findings = audit()
    
    if json_out:
        print(json.dumps(findings, indent=2, default=str))
        sys.exit(0)
    
    # ── Pretty print ──
    print('=' * 70)
    print('BUDGET LAPTOP TUNER — SYSTEM AUDIT')
    print(f'{findings["timestamp"]}')
    print('=' * 70)
    
    # RAM
    ram = findings['ram']
    print(f'\n═══ RAM ═══')
    print(f'  Total: {ram["total_mb"]:.0f} MB │ Available: {ram["avail_mb"]:.0f} MB │ Load: {ram["load_pct"]}%')
    
    # Disk
    print(f'\n═══ DISK ═══')
    for d, info in findings['disk'].items():
        print(f'  {d} {fmt_size(info["free"])} free ({info["pct"]:.1f}%) of {fmt_size(info["total"])}')
    
    # Agent.db
    adb = findings.get('agent_db', {})
    if adb:
        print(f'\n═══ AGENT.DB ═══')
        print(f'  Size: {adb["size_str"]} │ Sessions: {adb["sessions"]} │ Pinned: {adb["pinned"]}')
        print(f'  Tape entries: {adb["tape_entries"]:,}')
    
    # System settings
    print(f'\n═══ SYSTEM SETTINGS ═══')
    print(f'  Power plan:    {findings["power_plan"]}')
    print(f'  Visual FX:     {findings["visual_effects"]}')
    print(f'  Transparency:  {"ON" if findings["transparency"] == 1 else "OFF"}')
    print(f'  Game DVR:      {"ON" if findings["game_dvr"] == 1 else "OFF"}')
    print(f'  Hibernation:   {"ENABLED" if findings.get("hibernation_enabled") else "OFF/Unknown"}')
    print(f'  VBS/HVCI:      {"DETECTED" if findings.get("vbs_enabled") else "Unknown (needs admin check)"}')
    
    # DeepChat
    print(f'\n═══ DEEPCHAT ═══')
    print(f'  Processes: {findings["deepchat_processes"]} │ RAM: {findings["deepchat_ram_mb"]:.0f} MB')
    print(f'  Config files: {len(findings["config_files"])} ({fmt_size(sum(findings["config_files"].values()))} total)')
    
    # Top RAM processes
    procs = findings.get('top_processes', [])
    if procs:
        print(f'\n═══ TOP RAM PROCESSES ═══')
        for p in procs[:8]:
            if isinstance(p, dict):
                print(f'  {p.get("Name","?"):15s} {p.get("MB",0):>8.1f} MB')
    
    # Recommendations
    recs = findings['recommendations']
    print(f'\n═══ RECOMMENDATIONS ({len(recs)}) ═══')
    for r in recs:
        sv = {'critical': '🔴', 'high': '🟠', 'warning': '🟡', 'info': '🟢', 'low': '⚪'}.get(r['severity'], '?')
        admin = ' [ADMIN]' if r.get('needs_admin') else ''
        print(f'  {sv} {r["item"]}{admin}')
        print(f'     → {r["detail"]}')
        print(f'     → Action: {r["action"]}')
    
    # Apply
    if apply:
        print(f'\n═══ APPLYING NON-ADMIN OPTIMIZATIONS ═══')
        actions = apply_non_admin()
        for a in actions:
            print(f'  ✓ {a["action"]}: {a["result"]}')
        print(f'\n  {len(actions)} optimizations applied/queued.')
    
    print()
