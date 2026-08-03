# Windows Command Execution — Python-First Protocol v3.0 (POWERSHELL ZERO)

> **v3.0 (2026-08-03): TOTAL POWERSHELL BAN. User mandate: PowerShell is DELETED from this system.
> All 9 .ps1 scripts purged across 3 skills. All "last resort" carve-outs removed. Zero tolerance.
> The ONLY execution environments are Python (PRIMARY) and cmd.exe (cmd-native chaining only).**

---

## S-1.0 POWERSHELL IS DEAD. THIS IS NON-NEGOTIABLE.

**PowerShell does not exist on this system. It is not a fallback. It is not a "last resort."
It has been permanently deleted from every skill, every script, every reference.**

The cumulative damage caused by PowerShell exceeds every other tooling failure combined:
- 275 U+FFFF errors in resume PDF (encoding corruption)
- 42 CP1252 double-encoded dashes committed to GitHub
- 10+ lost tool calls in a single session (quote collapse, variable eating)
- D1 body_md corruption via JSON escaping
- Countless hours wasted on KIF-05/06/07/09/10/11/12/13/14 workarounds
- UTF-8 BOM silently breaking Node.js shebang scripts

**PowerShell is not a tool. It is a hazard.**

---

## S0.0 MANDATORY PRE-FLIGHT GATE

**Run this checklist BEFORE EVERY `exec` call. This is HARD, not optional.**

1. **Does the command string contain `powershell` anywhere?** → **ABORT. STOP. NEVER.**
2. **Does the command string contain `python -c`?** → **ABORT.** Write `_*.py` file, `exec python _*.py`.
3. **Does the command use `&&`, `||`, or `&` as separators?** → Use `cmd /c "cmd1 && cmd2"` for chaining.
4. **Does it contain nested double quotes?** → **ABORT.** Write to file instead.
5. **Can I write a `.py` file instead?** → YES (always). Do that.

---

## S1.0 PYTHON IS THE ONLY EXECUTION ENVIRONMENT

```
DECISION TREE (exactly 2 branches):
1. Write to .py file → exec python → DONE.
2. Need cmd-native chaining (&&, ||)? → exec cmd /c "..." → DONE.
   That's it. There is no branch 3.
```

### The Python Pattern (THE ONLY PATTERN)

```
Step 1: write tool → C:\Users\LENOVO\AppData\Local\Temp\_task.py
Step 2: exec python C:\Users\LENOVO\AppData\Local\Temp\_task.py
Step 3: exec cmd /c "del C:\Users\LENOVO\AppData\Local\Temp\_task.py"
```

### CMD Pattern (only for native chaining)

```
exec cmd /c "git add -A && git commit -m 'msg' && git push"
exec cmd /c "dir /s /b C:\path"
exec cmd /c "npx wrangler d1 list"
```

---

## S1.1 OPERATION REPLACEMENT TABLE

| Operation | PYTHON (always) |
|:----------|:----------------|
| File read | `open(p, encoding='utf-8').read()` |
| File write | `open(p, 'w', encoding='utf-8').write(...)` |
| JSON parse | `json.loads(text)` |
| HTTP request | `urllib.request.urlopen(url)` / `requests` |
| Regex search | `re.findall(pattern, text)` |
| Dir listing | `os.listdir(path)` |
| File existence | `os.path.exists(path)` |
| Environment var | `os.environ.get('VAR')` |
| Git operations | `subprocess.run(['git','-C',path,...])` |
| Cloudflare API | Python + `urllib.request` + `json.dumps` |
| PDF building | Python → `subprocess.run(['pandoc',...])` |
| Windows registry | `import winreg` |
| Windows services | `subprocess.run(['sc.exe', ...])` |
| WMI queries | `subprocess.run(['wmic.exe', ...])` |
| Process management | `subprocess.Popen` + `DETACHED_PROCESS` |
| System info | `platform`, `os`, `psutil`, `subprocess.run(['systeminfo'])` |
| AppX management | `subprocess.run(['wmic.exe', 'product', ...])` |

---

## S1.2 EXEC COMMAND REFERENCE

### Python (PRIMARY — use for EVERYTHING)
```
exec python C:\path\to\script.py
exec python C:\path\to\script.py arg1 arg2
```

### Native executables (run directly)
```
exec curl.exe -s https://api.example.com
exec git -C C:\path status
exec node --check C:\path\to\script.js
exec npx wrangler d1 list
exec pandoc input.md -o output.pdf --mathjax
```

### CMD (ONLY for native chaining)
```
exec cmd /c "cd /d C:\path && dir"
exec cmd /c "git add -A && git commit -m 'message'"
```

### PowerShell — BANNED FOREVER
```
# The following NEVER happens:
# exec powershell -NoProfile -Command "..."   ← BANNED
# exec powershell -File anything.ps1          ← BANNED
# Any .ps1 file creation                      ← BANNED
# Any PowerShell reference in any file        ← BANNED
```

---

## S1.3 WINDOWS SYSTEM ADMINISTRATION (Python-native)

### Registry Access
```python
import winreg

# Read
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\MyApp")
value, _ = winreg.QueryValueEx(key, "Setting")
winreg.CloseKey(key)

# Write
key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\MyApp")
winreg.SetValueEx(key, "Setting", 0, winreg.REG_SZ, "value")
winreg.CloseKey(key)
```

### Service Management
```python
import subprocess

# List services
subprocess.run(['sc.exe', 'query'], capture_output=True, text=True)

# Start/stop
subprocess.run(['sc.exe', 'start', 'ServiceName'])
subprocess.run(['sc.exe', 'stop', 'ServiceName'])
```

### WMI Queries
```python
import subprocess

# wmic is deprecated but still available on Windows
result = subprocess.run(
    ['wmic.exe', 'cpu', 'get', 'name'],
    capture_output=True, text=True
)
# Or use the `wmi` Python package: pip install wmi
```

### Process Management
```python
import subprocess

# List processes
subprocess.run(['tasklist.exe'], capture_output=True, text=True)

# Kill by PID
subprocess.run(['taskkill.exe', '/PID', '1234', '/F'])

# Kill by name
subprocess.run(['taskkill.exe', '/IM', 'notepad.exe', '/F'])
```

---

## S1.4 ENCODING PROTOCOL (UNCONDITIONAL)

```python
# ALWAYS explicit UTF-8
with open(path, 'r', encoding='utf-8') as f:    # read
with open(path, 'w', encoding='utf-8') as f:    # write (NO BOM)
```

**The `write` tool also writes clean UTF-8 (no BOM). Prefer it for script files.**

---

## S1.5 PRE-COMMIT GATE

```python
python C:\Users\LENOVO\.deepchat\pre-commit-mojibake-scan.py
```

Detects BOM, U+FFFD, U+FFFF, CP1252 double-encoding. HARD BLOCK on failure.

---

## S1.6 DETACHED PROCESS PATTERN (Python subprocess)

For long-running operations (>60s) that must survive the exec session:

```python
import subprocess
import os

log_file = os.path.join(os.environ['TEMP'], 'my-task.log')

# Remove old log
try:
    os.remove(log_file)
except FileNotFoundError:
    pass

# Launch detached process with output redirected to log
with open(log_file, 'w') as f:
    proc = subprocess.Popen(
        ['node.exe', r'C:\path\to\script.js'],
        stdout=f,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        env={**os.environ, 'MY_VAR': 'value'}
    )

# Write PID for later tracking
pid_file = os.path.join(os.environ['TEMP'], 'my-task.pid')
with open(pid_file, 'w') as pf:
    pf.write(str(proc.pid))

print(f"Launched PID {proc.pid}, log: {log_file}")
```

To check status later:
```python
import subprocess, os

pid_file = os.path.join(os.environ['TEMP'], 'my-task.pid')
log_file = os.path.join(os.environ['TEMP'], 'my-task.log')

# Check if running
with open(pid_file) as f:
    pid = int(f.read().strip())
result = subprocess.run(['tasklist.exe', '/FI', f'PID eq {pid}'], capture_output=True, text=True)
running = str(pid) in result.stdout

# Read log
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
        print(f.read())
```

---

## S1.7 NODE.JS FILE GATE

```python
import subprocess
result = subprocess.run(['node', '--check', r'C:\path\to\script.js'], capture_output=True)
if result.returncode != 0:
    print(f"SYNTAX ERROR: {result.stderr.decode()}")
```

---

## S2.0 POWERSHELL FAILURE ARCHIVE (Why It Died — Never Use This)

The following is preserved ONLY as a historical warning. **Do not attempt to use PowerShell.
Do not attempt workarounds. These patterns explain WHY PowerShell was killed.**

### KIF-05: Shell Mismatch
`&` is invoke operator, not separator. `||` and `&&` don't exist. `^` is not escape.

### KIF-06: Regex Pipe Collapse
`|` inside double quotes becomes pipeline operator, destroying regex.

### KIF-07: Pipeline Variable Omission
`$_` silently eaten in script blocks.

### KIF-09: Complex One-Liner Fragility
Multi-pipe JSON one-liners fail for structural reasons no escaping can fix.

### KIF-10: Set-Content UTF-8 BOM
Writes EF BB BF at byte 0, breaking Node.js shebang scripts.

### KIF-11: Start-Process on .cmd Shims
`npx`, `git`, `uvx` are `.cmd` not `.exe` — "not a valid Win32 application".

### KIF-12: Exec-Session Process Reaping
Long-running processes killed when harness reaps session.

### KIF-13: python -c f-string Dict Subscripts
`f'...{data["key"]}...'` — nested quotes collide with PowerShell parser.

### KIF-14: %VAR% Not Expanded in Config Files
`.npmrc`, `.env`, YAML parsers treat `%VAR%` as literal string.

### ENCODING CORRUPTION (FATAL)
`Get-Content`/`Out-File` default to CP1252, silently destroying Unicode. This single
failure mode caused more damage than every other bug combined.

---

## QUICK REFERENCE

| Task | DO THIS |
|:-----|:--------|
| Anything | Write `_task.py` → `exec python _task.py` |
| File read/write | Python `open(p, encoding='utf-8')` |
| JSON | Python `json.loads`/`json.dumps` |
| HTTP | Python `urllib.request` or `requests` |
| Regex | Python `re` module |
| Git | Python `subprocess.run(['git',...])` or `exec git ...` |
| CMD chaining | `exec cmd /c "cmd1 && cmd2"` |
| Windows registry | Python `winreg` |
| Windows services | Python `subprocess.run(['sc.exe',...])` |
| Long-running process | Python `subprocess.Popen` with `DETACHED_PROCESS` |
| PowerShell | **NEVER. DELETED. ZERO TOLERANCE.** |

## SELF-CHECK BEFORE EXECUTING

1. **Does this involve PowerShell in ANY way?** → **ABORT. HARD BLOCK. NO EXCEPTIONS.**
2. **Is this a Python operation?** → Write .py file, `exec python`. DONE.
3. **Is this a native executable?** → `exec curl.exe`, `exec git`, `exec node`, `exec pandoc`. DONE.
4. **Is this cmd-native chaining?** → `exec cmd /c "..."`. DONE.
5. **Is this long-running?** → Python `subprocess.Popen` with `DETACHED_PROCESS`.
6. **Writing scripts?** → Use `write` tool (clean UTF-8). `node --check` before running.

**Python is not the default. Python is the ONLY option.**

---

## DeepChat Runtime Context
- Skill root: `C:\Users\LENOVO\.deepchat\skills\windows-command-patterns`.
- Relative paths mentioned by this skill are relative to the skill root unless stated otherwise.
- When this skill needs script execution, prefer `skill_run` over `exec`.
- **No scripts are bundled.** All .ps1 files have been permanently deleted.
