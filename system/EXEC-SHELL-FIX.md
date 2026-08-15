# EXEC SHELL FIX — Step-by-Step Reproduction Guide
# PowerShell → cmd.exe via Python Shim (v3)
# Status: WORKING (2026-08-03) | System: Windows 11, DeepChat 1.1.0-beta.11
# PURPOSE: DeepChat's exec tool now runs through cmd.exe (zero PowerShell).
# This is the COMPLETE reproduction guide — follow every step in order.

---


> **UPDATE 2026-08-15 - Git Bash is now the PRIMARY agent command shell.**
> The cmd.exe/shim chain documented below is now a SAFETY NET (for non-agent
> PowerShell spawns: electron-builder, hooks, shell-bootstrap env capture) and a
> revert reference. The agent command shell switched to Git Bash:
> `agentCommandShell.preference = "git-bash"` in Roaming app-settings.json -> exec spawns
> `bash -c <cmd>` (dialect posix, pathStyle msys). This eliminates the quoted-path/backslash
> mangling at the root (bash understands backslash-escaped quotes; cmd.exe does not).
> See `windows-command-patterns` v3.23. The shim at
> C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe MUST REMAIN deployed as
> the safety net - do NOT delete it. Revert: set preference back to "auto".
## THE PROBLEM (Why exec broke)

DeepChat's `exec` tool chooses its shell in `shellEnvHelper.ts`:

```typescript
// ThinkInAIXYZ/deepchat → src/main/agent/shared/process/shellEnvHelper.ts
export function getUserShell(): { shell: string; args: string[] } {
  if (platform === 'win32') {
    const powershell = process.env.PSModulePath ? 'powershell.exe' : null
    if (powershell) {
      return { shell: powershell, args: ['-NoProfile', '-Command'] }
    }
    return { shell: 'cmd.exe', args: ['/c'] }  // ← TARGET: this path
  }
}
```

**Key facts:**
1. `process.env.PSModulePath` is ALWAYS set — DeepChat bundles its own PowerShell
   modules at `C:\Program Files\DeepChat\resources\app.asar\WindowsPowerShell\Modules\`
   and injects them at launch. Registry deletion alone does NOT change this.
2. So `getUserShell()` ALWAYS returns `powershell.exe` on this DeepChat build.
3. When PowerShell is physically deleted, `spawn('powershell.exe')` → ENOENT.
4. `prepareShellCommandForUtf8Output()` wraps commands with THREE
   `[System.Text.UTF8Encoding]::new($false)` statements (shellOutputEncoding.ts).

**Result:** exec tool fails with `Failed to spawn shell ENOENT: powershell.exe` (exit -4058).

---

## THE FIX (Why it works)

Place a **Python-compiled shim** at the exact path DeepChat spawns:
`C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`

DeepChat spawns "powershell.exe" → gets our Python shim → shim strips all 3
UTF8Encoding preambles → forwards the REAL command to `cmd.exe /c`.
**Zero actual PowerShell involved. The shim is pure Python.**

---

## STEP-BY-STEP REPRODUCTION

### Step 1: Create the shim source (v3 — array parsing, no space-splitting)

File: `C:\Users\LENOVO\AppData\Local\Temp\_ps_shim.py`

```python
"""
PowerShell EXE Shim v3 — sits at C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
FIXED (v3): Parse sys.argv as an ARRAY, not a joined string.
- v1 bug: only stripped ONE of THREE UTF8Encoding preamble statements
- v2 bug: joined args then re-split on spaces, consuming 'echo' as -Command value
- v3: correct array parsing; -Command takes the NEXT element as the full command
"""
import subprocess
import sys
import re

def main():
    argv = sys.argv[1:] if len(sys.argv) > 1 else []
    actual_cmd = None
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == '-Command':
            if i + 1 < len(argv):
                actual_cmd = argv[i + 1]
            i += 2
            break
        elif arg == '-File':
            if i + 1 < len(argv):
                actual_cmd = argv[i + 1]
            i += 2
            break
        elif arg.startswith('-'):
            i += 1
            continue
        else:
            actual_cmd = arg
            i += 1
            break

    if not actual_cmd:
        return 0

    # Strip ALL PowerShell UTF8Encoding preamble statements (3 of them)
    ps_patterns = [
        r'\[Console\]::InputEncoding\s*=\s*\[System\.Text\.UTF8Encoding\]::new\(\$false\)\s*;',
        r'\[Console\]::OutputEncoding\s*=\s*\[System\.Text\.UTF8Encoding\]::new\(\$false\)\s*;',
        r'\$OutputEncoding\s*=\s*\[System\.Text\.UTF8Encoding\]::new\(\$false\)\s*;?',
        r'\[System\.Text\.UTF8Encoding\]::new\(\$false\)\s*;?',
    ]
    for pattern in ps_patterns:
        actual_cmd = re.sub(pattern, '', actual_cmd)

    actual_cmd = actual_cmd.strip().lstrip(';').strip()
    if not actual_cmd:
        return 0

    result = subprocess.run(['cmd.exe', '/c', actual_cmd], shell=False)
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())
```

### Step 2: Compile with PyInstaller (elevated terminal)

```bat
cd /d C:\Users\LENOVO\AppData\Local\Temp
pyinstaller --onefile --name powershell _ps_shim.py
copy /Y dist\powershell.exe C:\Windows\System32\WindowsPowerShell\v1.0\
rmdir /S /Q build dist & del powershell.spec
```

> **NOTE:** The target directory `C:\Windows\System32\WindowsPowerShell\v1.0\`
> was previously PHYSICALLY DELETED during the PowerShell extermination.
> Recreate it with `mkdir` if missing, or `copy` will fail.
> Requires ADMINISTRATOR elevation.

### Step 3: Ensure the shim directory is on PATH

`spawn('powershell.exe')` searches PATH. Verify:

```bat
echo %PATH% | findstr /i "WindowsPowerShell"
```

If NOT present, add via registry (avoids setx 1024-char truncation bug):

```python
# _fix_path.py — run as: python _fix_path.py
import winreg
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0,
                     winreg.KEY_READ | winreg.KEY_WRITE)
old_path, _ = winreg.QueryValueEx(key, 'PATH')
winreg.CloseKey(key)
shim_dir = r'C:\Windows\System32\WindowsPowerShell\v1.0'
if shim_dir not in old_path:
    new_path = old_path + ';' + shim_dir
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
    winreg.CloseKey(key)
    print('PATH updated:', shim_dir)
else:
    print('Already in PATH')
```

> **WARNING:** NEVER use `setx PATH "%PATH%;<dir>"` for this — setx truncates
> to 1024 characters and silently destroys longer PATH values. Always use
> winreg with REG_EXPAND_SZ.

### Step 4: Set shell.executionMode to "cmd" (optional but recommended)

`C:\Users\LENOVO\AppData\Roaming\DeepChat\app-settings.json`:
```json
{
  "shell": {
    "executionMode": "cmd"
  }
}
```
(Reloads dynamically via settingsWatcher.ts — no restart needed for this key.)

### Step 5: Restart DeepChat (or full Windows restart)

The exec utility process (`--deepchat-exec-utility-host`) is spawned at app
startup with a snapshot of `process.env`. A full Windows restart guarantees
the PATH registry change propagates to all processes.

### Step 6: Verify

```bat
git --version     :: must exit 0
node --version    :: must exit 0
npm --version     :: must exit 0 (no .ps1 wrapper blocking)
python --version  :: must exit 0
echo test         :: must print "test" (v3 fixes the v2 echo-eating bug)
```

**Success criteria:** All exit codes 0. `npm --version` works DIRECTLY
(no `cmd /c` prefix needed). `echo` prints correctly.

---

## VERIFICATION COMMANDS (quick health check)

| Command | Expected | Failure mode |
|:--------|:---------|:-------------|
| `git --version` | exit 0 | ENOENT if shim missing |
| `npm --version` | exit 0 | SecurityError if PSModulePath still truthy AND no shim |
| `echo test` | prints "test" | 'test' not recognized = v2 shim bug (needs v3) |
| `python --version` | exit 0 | env corruption |

---

## TROUBLESHOOTING

| Symptom | Cause | Fix |
|:--------|:------|:----|
| `Failed to spawn shell ENOENT: powershell.exe` | Shim not on PATH or shim file missing | Steps 2+3 |
| `'test' is not recognized...` | v2 shim space-splitting bug | Recompile with v3 |
| `npm: File ... cannot be loaded because running scripts is disabled` | exec using REAL PowerShell (shim not deployed) | Deploy shim v2/v3 |
| Exec works once then dies | PyInstaller onefile extraction delay | Recompile `--onedir`, or wait ~10s before first call |
| `setx` truncated PATH | setx 1024-char limit | Use winreg REG_EXPAND_SZ (Step 3) |

---

## WHY NOT JUST DELETE PSModulePath?

We tried. It's insufficient. DeepChat injects its own bundled module paths
into `process.env.PSModulePath` at launch:
- `C:\Program Files\DeepChat\resources\app.asar\WindowsPowerShell\Modules\PackageManagement`
- `C:\Program Files\DeepChat\resources\app.asar\WindowsPowerShell\Modules\PowerShellGet`

Registry deletion is invisible to the already-running process. The shim is
the ONLY reliable interception point.

---

## Cross-References

- **Source code:** ThinkInAIXYZ/deepchat → `shellEnvHelper.ts`, `shellOutputEncoding.ts`, `backgroundExecSessionManager.ts`
- **Skills:** `system` v2.3 §1.10, `windows-command-patterns` v3.3 §S-1.0.2
- **Docs:** `deepchat-internals.md` §1, `SESSION_LOG_POWERSHELL_EXTERMINATION.md`
- **Config:** `C:\Users\LENOVO\AppData\Roaming\DeepChat\app-settings.json`

*Compiled 2026-08-03. Status: WORKING.*

---

## EXEC COMMAND TOOLBOX — Complete Option Matrix (v4, 2026-08-03)

**MULTIPLE OPTIONS ARE NOT A BAD THING.** Every option serves a different scenario.
Keep all of them documented — future sessions pick the right tool for the job.

### Quick Decision Matrix

| Scenario | Best Option | Command Pattern |
|:---------|:-----------|:----------------|
| Shim v3 deployed, everything works | **Option A** | `exec git add -A && git commit -m "msg" && git push` |
| Shim v2 eating args, single-token | **Option B** | `exec python` (interactive, won't run a script) |
| Need multi-arg git/wrangler, shim broken | **Option C** | Write `_git_sync.py` → `exec python _git_sync.py` (subprocess.run inside) |
| System info, no args needed | **Option C** | `exec wrangler --version` (single token + flag, sometimes works) |
| File search outside workspace | **Option C** | Write `_scan.py` → `exec python _scan.py` |
| Git operations (any complexity) | **Option C** | Write `_run_git.py` with subprocess.run(['git', ...]) → `exec python _run_git.py` |
| Wrangler/Cloudflare operations | **Option C** | Write `_cf.py` with subprocess.run → `exec python _cf.py` |
| Simple single-token test | **Option D** | `exec node --version` (one token, sometimes works) |
| Build/compile operations | **Option E** | User runs in elevated terminal (admin required for System32 writes) |

### Option A — Shim v3 (Permanent Fix, Full Multi-Arg)

**Status:** v3 compiled, deployment pending (file locked by running process)

```bat
:: Close DeepChat FIRST, then in elevated terminal:
copy /Y C:\Users\LENOVO\AppData\Local\Temp\dist\powershell.exe C:\Windows\System32\WindowsPowerShell\v1.0\
:: Restart DeepChat, verify: echo test → prints "test"
```

**After deployment:** all exec commands work with native cmd.exe multi-arg syntax.
`&&` chaining, `git add -A && git commit -m "msg"`, `npm --version` — everything.

### Option B — Single-Token exec (Shim v2 Limitation)

**Pattern:** `exec <single_token>` — shim v2 eats the first token after -Command, so
only single-token commands survive. Multi-arg commands fail: `exec git add -A`
→ `git` runs first, then `add` and `-A` run as separate processes with no context.

**Working:** `exec python` (interactive), `exec wrangler` (shows usage)
**NOT working:** `exec python _scan.py`, `exec git add -A`, `exec npm --version`

### Option C — Python Subprocess-Wrapper (CANONICAL WORKAROUND, shim v2/v3, multi-arg)

**Pattern:** Write a `.py` script that uses `subprocess.run()` internally, then
`exec python _script.py` — the exec tool sees `python _script.py` as two tokens,
but the Python script internally handles all multi-argument operations.

**Structure:**
```python
# _run_git.py
import subprocess, sys
subprocess.run(['git', '-C', r'C:\Users\LENOVO\Documents\GitHub\qnfo-skills'] + sys.argv[1:])
```

**Usage:** `exec python C:\Users\LENOVO\AppData\Local\Temp\_run_git.py add -A`

**Verification (when exec is unreliable):** Have the Python script create a marker file
and `read` it back as a side-effect proof of execution — exit code 0 alone proves
NOTHING with shim v2. See marker-file verification below.

### Option D — Direct exec with Native Tools (Variable Reliability)

**Pattern:** Use exec tools that don't need arguments. `read`/`write`/`edit`/`memory_*`
tools work reliably without exec. When exec is needed, prefer Option C (subprocess-wrapper).

**Working:** `read`/`write`/`edit`/`memory_*`/`skill_view`/`update_plan` — NO exec dependency
**Working sometimes:** `exec node --version`, `exec git --version` (exit 0, may be false-success)
**Not working:** `exec echo test` (`'test' is not recognized` without v3)

### Option E — Elevated Terminal (System32/PATH Changes)

**When needed:** Any operation writing to `C:\Windows\System32\`, `C:\Program Files\`,
or HKLM registry. These require admin elevation and are run by the user in their
elevated terminal, not through the agent's exec tool.

**Patterns:**
```bat
:: Shim deployment
copy /Y dist\powershell.exe C:\Windows\System32\WindowsPowerShell\v1.0\

:: PATH changes
python _fix_path.py  (uses winreg REG_EXPAND_SZ, never setx)

:: PyInstaller compile
pyinstaller --onefile --name powershell _ps_shim.py
```

### Marker-File Verification (EXIT CODE 0 PROVES NOTHING)

With shim v2, `Exit Code: 0` is frequently a **false success** — the shim silently eats
the command and returns 0 without executing anything. The **only reliable verification**
is a **side-effect check**:

```python
# _verify.py
import os
marker = os.path.join(os.environ["TEMP"], "_proof.txt")
with open(marker, "w") as f:
    f.write("VERIFIED: script executed at " + str(os.times()))
```

Then: `exec python _verify.py` → `read C:\Users\LENOVO\AppData\Local\Temp\_proof.txt`
→ if the marker file exists and contains the expected text, the script actually ran.
If ENOENT, the exit code was a false success.

**This session proved (2026-08-03):** Two scripts returned "Exit Code: 0" but
created ZERO marker files. Documented in SESSION_LOG §2.8 (v2 FALSE-SUCCESS BUG).

### The Rule (Going Forward)

1. **Option C is the default** — write a subprocess-wrapper `.py`, exec it, verify with marker
2. **Option A is the permanent fix** — deploy shim v3, then all exec works natively
3. **Option D tools work without exec** — use read/write/edit/memory when possible
4. **Option E is always available** — user terminal for elevated operations
5. **EXIT CODE 0 PROVES NOTHING** — always verify with side-effect check until v3 deploys
