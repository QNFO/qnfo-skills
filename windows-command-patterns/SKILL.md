---
name: windows-command-patterns
description: Windows command execution — Python-First Protocol. Python is PRIMARY for ALL operations. PowerShell is DEPRECATED (LAST RESORT only). Use this skill to understand PowerShell's failure modes and when Python cannot be used.
version: "2.3"
---

# Windows Command Execution — Python-First Protocol (v2.3)

> **v2.3 UPDATE (2026-08-02, kaizen — MANDATORY PRE-FLIGHT GATE + python -c escalation):**
> Red-team: direct parent-agent 5-adversary audit per kaizen v1.2.5 HARD GATE. AUTO-TRIGGERED
> by Watchtower INCIDENT-AXIS 0.6 (python -c failures accumulated across 4+ sessions despite
> documented anti-patterns in KIF-13, SELF-CHECK #8, and the Python-First Mandate).
> HARD findings: 0 in this skill. DESIGN findings: 1.
> Root cause: the anti-pattern documentation is comprehensive but AGENTS DON'T CHECK IT before
> sending `exec python -c`. The SELF-CHECK list at the bottom of the skill is read LAST, after
> the agent has already sent 10+ failing `python -c` calls. Fix: **S0.0 MANDATORY PRE-FLIGHT GATE**
> inserted BEFORE S1.0 — a HARD, unskippable 4-item checklist that runs BEFORE EVERY exec command.
> Positioned at the very top of the skill so it's the FIRST thing an agent reads when loading
> this skill, not the last. The checklist ABORTS any `python -c` with quotes/dicts/f-strings
> before the exec tool call is dispatched.
> Changes:
> (1) [DESIGN] Added S0.0 MANDATORY PRE-FLIGHT GATE — 4-item checklist positioned BEFORE S1.0
>     (the Python-First Mandate). Item 1: "Does the command contain python -c? → ABORT."
>     Item 2: "Does it use &&, ||, &? → ABORT." Item 3: "Does it contain nested quotes? → ABORT."
>     Item 4: "Can I write a .py file instead? → YES (99%+). Do that."
>     This gate is read FIRST on skill activation, making it impossible to miss.
> Cross-reference: kaizen v1.4.1 (Watchtower auto-trigger protocol), research v2.45 (GATE P5.CLEAN
> deferred python -c escalation as EXTERNAL-BLOCK — this v2.3 fix is the skill-level counterpart;
> the true permanent fix requires DeepChat tool-level enforcement, deferred but documented).
> Red-team: direct parent-agent 5-adversary audit of a session that lost ~8 tool calls
> to inline `python -c` failures and 1 stray-directory incident. HARD findings: 2. SOFT: 1.
> Changes:
> (1) [HARD] Added **KIF-13: inline `python -c` with f-string DICT SUBSCRIPTS**
>     (`f'...{data["key"]}...'`) — the nested double-quotes inside the f-string
>     collide with PowerShell's outer-quote parsing, producing
>     `SyntaxError: unterminated string literal` / `Unexpected token '{'`.
>     This specific signature recurred ~8× in one session (`.zenodo_versions.json`
>     updates, JSON printouts). It is a SPECIFIC sub-pattern of the existing
>     B1/KIF-37 `python -c` block — the safe alternative is ALWAYS write-to-file
>     then `exec python file.py`, or single-quote JSON keys in f-strings
>     (`data['key']`) only when the outer shell context is a real POSIX shell,
>     NEVER under PowerShell (Accuracy + Completeness Auditors, parent-agent).
> (2) [HARD] Added **KIF-14: Windows `%VAR%` is NOT expanded in config files**
>     (`.npmrc`, `.env`, YAML) — npm config treats `%USERPROFILE%\npm-global` as a
>     LITERAL directory name and created a stray `%USERPROFILE%` folder in cwd.
>     Only `cmd.exe`/`set` expand `%VAR%`; config-file parsers use absolute paths
>     or `${VAR}`. ALWAYS write absolute paths into `.npmrc`/config files
>     (Completeness Auditor, parent-agent).
> (3) [SOFT] Quick Reference: added `python -c` dict-subscript row + `%VAR%`-in-config
>     row to the SELF-CHECK list (Novelty Auditor, parent-agent).
> Cross-reference: cloudflare v3.14 (wrangler env fix uses absolute paths),
> kaizen v1.2.5, research v2.40.

> **v2.1 UPDATE (2026-07-31, kaizen — LinkedIn MCP session):**
> Red-team: direct parent-agent 5-adversary audit (Accuracy, Completeness, Dependency,
> Novelty, Status). HARD findings: 1. SOFT findings: 3.
> Changes:
> (1) [HARD] S1.4 + Quick Reference recommended `Set-Content -Encoding UTF8` for last-resort
>     writes — but PS 5.1 writes a UTF-8 BOM with it, fatally breaking Node.js shebang scripts
>     (`SyntaxError: Invalid or unexpected token`). Hit 2026-07-31 writing linkedin-auto-login.js.
>     Replaced with `[System.IO.File]::WriteAllText(p, s, [Text.UTF8Encoding]::new($false))`.
>     Use the write tool (clean UTF-8) or Python for JS/Python/shell scripts. (Accuracy Auditor,
>     parent-agent).
> (2) [SOFT] Added S1.6 DETACHED PROCESS PATTERN — long-running ops (browser launches, MCP
>     servers, downloads > harness yield window) get killed when the exec session times out.
>     Use `[System.Diagnostics.Process]` with `BeginOutputReadLine` + `Register-ObjectEvent`
>     to write to a log file and survive independently. (Completeness Auditor, parent-agent).
> (3) [SOFT] Added `Start-Process "npx"` failure mode — npx is a .cmd batch file, not .exe;
>     "not a valid Win32 application". Use `cmd /c npx ...` or `npx.cmd` explicitly.
> (4) [SOFT] Added `node --check` syntax gate before running any written JS file — catches
>     BOM/shebang corruption and edit errors before execution.
> (5) [SOFT] Added anti-pattern rows: Set-Content BOM write, Start-Process on .cmd, exec-session
>     kill of long-running processes.
> Cross-reference: kaizen v1.2.4, linkedin-mcp skill (new, v1.0).

> **v2.0 UPDATE (2026-07-31): COMPLETE REWRITE — PowerShell Deprecation Mandate.**
> The prior v1.x skill taught how to COPE with PowerShell's failures (KIF-05/06/07/09
> patterns, `ps-lint.ps1`, `ps-safe-exec.ps1`). As of v2.0, the correct approach is
> to AVOID PowerShell entirely except as a genuine last resort. Python is the PRIMARY
> execution environment for ALL operations on this system. The v1.x KIF patterns are
> retained below as reference documentation on "why PowerShell fails" — they are NOT
> a recommendation to keep using PowerShell with workarounds.
>
> **Root-cause incidents driving this deprecation:**
> - 2026-07-31: Resume v3.3 PDF had 275 U+FFFF errors from PowerShell `Get-Content`
>   silently reading UTF-8 as CP1252, producing mojibake (`a+"` instead of `--`)
> - 2026-07-31: computing-machines/paper.md had 42 CP1252 double-encoded dashes
>   committed to GitHub — same root cause
> - 2026-07-28: Session e4layp9 lost 10+ tool calls to PowerShell KIF-05/06/07/09
>   failures (quote collapse, $variable eating, regex-pipe ambiguity)
> - 2026-07-21: D1 body_md insert corrupted via PowerShell JSON escaping
>
> **The cumulative cost of PowerShell on Windows exceeds every other tooling failure
> pattern combined.** Python is installed. Python is reliable. Use Python.

---

## S0.0 MANDATORY PRE-FLIGHT GATE (v2.3 — HARD, NO EXCEPTIONS)

**Run this checklist in your head BEFORE EVERY `exec` call. This is NOT optional.**

1. **Does the command string contain `python -c`?** → **ABORT.** Write a `_*.py` file via the `write` tool, then `exec python _*.py`. No exceptions. This includes ALL `python -c` calls — even single-line ones with no apparent quotes. The Windows PowerShell parser can silently corrupt: double-quotes, single-quotes, angle brackets, dollar signs, curly braces, and dict literals in the Python string before Python ever sees it. KIF-13 documents the specific f-string dict-subscript signature (`f'...{data["key"]}...'`) that failed ~8× in one session. S0.0 catches it BEFORE dispatch.
2. **Does the command use `&&`, `||`, or `&` as separators?** → **ABORT.** PowerShell treats `&&`/`||` as invalid statement separators. Use `;` to chain commands, or run separate `exec` calls. For `cmd.exe` native chaining, use `exec cmd /c "cmd1 && cmd2"`.
3. **Does it contain `"` (double quote) inside an outer `"..."` string?** → **ABORT.** The outer quotes will be stripped by the shell parser before the inner content reaches the target. Write to a `.py` or `.ps1` file instead.
4. **Can I write a `.py` file instead?** → YES (99%+ of cases). Skip the mental gymnastics. Write your Python to a file via the `write` tool, `exec python` it, and delete it. This is always correct.

**GATE:** If ANY of items 1-3 return YES, the exec call is BLOCKED. Do not attempt it. Write to file.

---

## S1.0 PYTHON-FIRST MANDATE (HARD GATE — NO EXCEPTIONS)

**Python is the PRIMARY execution environment for ALL operations on this system.**

Before ANY `exec` call:

```
DECISION TREE:
1. Can this be done with Python? → YES (99%+ of cases) → Write to .py file, exec python
2. Is this a pure system-administration task that Python genuinely cannot do?
   → Consider cmd.exe / CMD directly
3. Is this a Windows-native API call that ONLY PowerShell can reach?
   → PowerShell is LAST RESORT — use ps-safe-exec.ps1 with -Strict, write to .ps1 file
```

### The Python Pattern (CANONICAL for ALL operations)

```
Step 1: write tool → C:\Users\LENOVO\AppData\Local\Temp\_script.py
Step 2: exec python C:\Users\LENOVO\AppData\Local\Temp\_script.py
Step 3: exec cmd /c "del C:\Users\LENOVO\AppData\Local\Temp\_script.py"
```

**NEVER use `python -c "..."` via `exec` on Windows.** The PowerShell parser intercepts
single-quotes, double-quotes, angle brackets, dollar signs, and curly braces in the
Python string before Python ever sees it. Write to a file first. ALWAYS.

### What Python Replaces

| Operation | OLD (PowerShell) | NEW (Python) |
|:----------|:-----------------|:-------------|
| File content read | `Get-Content file.md` | `open('file.md','r',encoding='utf-8').read()` |
| File content write | `Set-Content / Out-File` | `open('file.md','w',encoding='utf-8').write(...)` |
| JSON parse | `ConvertFrom-Json` | `json.loads(...)` |
| HTTP request | `Invoke-WebRequest / curl.exe` | `urllib.request` or `requests` |
| Regex search | `Select-String -Pattern '(a|b)'` | `re.findall(r'(a|b)', text)` |
| String replace | `-replace / .Replace()` | `text.replace(old, new)` |
| Directory listing | `Get-ChildItem / ls` | `os.listdir(path)` |
| File existence | `Test-Path` | `os.path.exists(path)` |
| Environment var | `$env:VAR` | `os.environ.get('VAR')` |
| Git operations | `git -C path ...` | `subprocess.run(['git','-C',path,...])` |
| D1 queries | Inline JSON via PS | Python script with `urllib.request` |
| PDF building | Pandoc via PS | Python script → `subprocess.run(['pandoc',...])` |

### Why PowerShell Fails (Reference — NOT a Recommendation)

The following patterns are DOCUMENTED here for reference only. They explain WHY
PowerShell is deprecated. Do NOT attempt to work around them — use Python instead.

---

## S1.1 WHEN POWERSHELL IS GENUINELY THE ONLY OPTION (LAST RESORT)

PowerShell is acceptable ONLY in these narrow circumstances, and ONLY when a Python
equivalent has been explicitly confirmed impossible:

1. **Windows registry access** — `Get-ItemProperty`, `Set-ItemProperty`
2. **Windows service management** — `Get-Service`, `Start-Service`, `Stop-Service`
3. **WMI/CIM queries** — `Get-CimInstance`, `Get-WmiObject`
4. **Active Directory operations** — `Get-ADUser`, etc.
5. **AppX package management** — `Get-AppxPackage`, `Add-AppxPackage`
6. **PowerShell-specific modules** — PSDsc, PSRemoting, Exchange Online

**Even in these cases:**
- Use a .ps1 file (NEVER inline `powershell -Command "..."`)
- Use `ps-safe-exec.ps1 -Strict` as the wrapper
- Document WHY Python wasn't suitable

### The .ps1 Pattern (Last Resort Only)

```
Step 1: write tool → C:\Users\LENOVO\AppData\Local\Temp\_task.ps1
Step 2: exec powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\LENOVO\AppData\Local\Temp\_task.ps1"
Step 3: Delete the .ps1 file
```

---

## S1.2 POWERSHELL FAILURE MODES (Reference — Why Python Wins)

### KIF-13: Inline python -c with f-string DICT SUBSCRIPTS (2026-08-01)

`python -c "print(f'OK: {len(data[\"versions\"])}')"` — nested double-quotes inside
an f-string collide with PowerShell's outer-quote parsing. This exact pattern
failed **~8 times in one session** (`SyntaxError: unterminated string literal` /
`Unexpected token '{'`), every time on JSON-print or dict-lookup one-liners.

| Wrong (PowerShell + f-string double quotes) | Correct |
|:-------------------------------------------|:--------|
| `python -c "print(f'OK: {data[\"key\"]}')"` | Write `_check.py` via write tool → `exec python _check.py` |
| `python -c 'import json; print(json.dumps(x))'` (nested quotes) | Same — write to file first |

**Rule:** ANY `python -c` containing an f-string with `["..."]` subscript, a dict
literal, or nested quotes is GUARANTEED to fail under PowerShell. Write the script
to a `_*.py` file and `exec python` it. This is a hard sub-pattern of B1/KIF-37.

### KIF-14: Windows %VAR% NOT expanded in config files (2026-08-01)

`cmd.exe` and `set` expand `%VAR%`, but **config-file parsers do not**. Writing
`prefix=%USERPROFILE%\npm-global` into `~/.npmrc` (via `npm config set`) created a
stray directory literally named `%USERPROFILE%` in the current working directory —
npm used the string verbatim. `.npmrc`, `.env`, YAML, and JSON config values must
use **absolute paths** (`C:\Users\LENOVO\npm-global`) or `${VAR}` syntax (some
parsers). NEVER `%VAR%` in config files.

### KIF-05: Shell Mismatch

PowerShell uses `&` as the call/invoke operator, NOT a command separator. `||` and `&&`
do not exist. `^` is NOT an escape character (backtick is).

| Wrong | Error |
|:------|:------|
| `cmd1 & cmd2` | "The ampersand (&) character is not allowed" |
| `cmd1 || cmd2` | "The token '||' is not a valid statement separator" |
| `powershell -Command ^& { ... }` | "The ampersand (&) character is not allowed" |

### KIF-06: Regex Pipe Collapse

Inside PowerShell double-quoted strings, `|` is the pipeline operator. Any regex
containing `|` inside double quotes is silently reinterpreted as a PowerShell pipe.

| Wrong (double-quoted regex) | Correct (Python) |
|:----------------------------|:-----------------|
| `Select-String -Pattern "(a|b)"` | `re.findall(r'(a|b)', text)` |
| `-replace "(old|new)", "x"` | `re.sub(r'(old|new)', 'x', text)` |

### KIF-07: Pipeline Variable Omission ($_ eaten)

`.Property` without `$_` in PS script blocks silently fails. Python has no equivalent
ambiguity — `obj.property` always works.

### KIF-09: Complex One-Liner Fragility

Multi-pipe, multi-variable, JSON-parsing PowerShell one-liners fail for STRUCTURAL
reasons (quote collapse, scoping, pipeline quirks) that NO escaping can fix. WRITE
A PYTHON FILE instead of a .ps1 file.

### KIF-10: Set-Content BOM Write (2026-07-31)

`Set-Content -Encoding UTF8` / `Out-File -Encoding UTF8` on PowerShell 5.1 writes a
UTF-8 **BOM** (EF BB BF). A BOM at byte 0 is a fatal error for Node.js shebang
scripts: `#!/usr/bin/env node` → `SyntaxError: Invalid or unexpected token`.
Hit while writing linkedin-auto-login.js — the script crashed on launch until
rewritten via the write tool (clean UTF-8). **Never use Set-Content/Out-File for
script files. Use the write tool or Python; if PS is forced, use
`[IO.File]::WriteAllText(p, s, [Text.UTF8Encoding]::new($false))`.**

### KIF-11: Start-Process on .cmd Shims (2026-07-31)

`Start-Process -FilePath "npx"` fails with "not a valid Win32 application" —
npx, git, uvx, pip are `.cmd`/`.bat` shims, not `.exe`. Use `cmd /c npx ...`,
`Start-Process cmd.exe -ArgumentList '/c','npx ...'`, or resolve the real exe
(`node.exe C:\...\cli.js`).

### KIF-12: Exec-Session Process Reaping (2026-07-31)

Long-running processes started via `exec` (foreground auto-background OR
`background:true`) are killed when the harness reaps the session — even with a
long `timeoutMs`. A 4-minute login poll or MCP browser session dies mid-flight.
**Use the S1.6 DETACHED PROCESS PATTERN** (System.Diagnostics.Process +
Register-ObjectEvent → log file) for anything expected to run > ~60s.

### ENCODING CORRUPTION (MOST DANGEROUS)

`Get-Content` and `Out-File` on Windows DEFAULT TO THE SYSTEM CODEPAGE (CP1252),
NOT UTF-8. Any file containing Unicode characters (em dashes, curly quotes,
Greek letters, math symbols, degree signs) is SILENTLY CORRUPTED with NO error
raised. The corruption propagates to git commits, D1 inserts, Zenodo uploads,
and PDFs. This single failure mode has caused more damage than all other
PowerShell issues combined.

**ABSOLUTE RULE: Never use Get-Content / Out-File for text files containing any
character outside ASCII. Use Python open(path, encoding='utf-8') instead.**

---

## S1.3 EXEC COMMAND PATTERNS

### Python (PRIMARY — use for ALL operations)

```
exec python C:\path\to\script.py
exec python C:\path\to\script.py arg1 arg2
```

### Native executables (USE DIRECTLY, not through PowerShell)

```
exec curl.exe -s https://api.example.com
exec git -C C:\path status
exec npx wrangler d1 list
exec pandoc input.md -o output.pdf --pdf-engine=xelatex
```

### CMD (for cmd-native operations)

```
exec cmd /c "dir /s /b C:\path"
exec cmd /c "git add -A && git commit -m 'message' && git push"
```

### PowerShell (LAST RESORT — documented for reference only)

```
# NEVER inline:
exec powershell -NoProfile -Command "..."  ← BANNED for anything beyond Get-ChildItem C:\

# ALWAYS use .ps1 file:
exec powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\LENOVO\AppData\Local\Temp\_task.ps1"
```

---

## S1.4 ENCODING PROTOCOL (UNCONDITIONAL)

Every text file operation on this system MUST use explicit UTF-8 encoding:

```python
# Python (CORRECT — ALWAYS use this)
with open(path, 'r', encoding='utf-8') as f:    # read
with open(path, 'w', encoding='utf-8') as f:    # write
```

```powershell
# PowerShell (LAST RESORT ONLY — FORCE encoding)
Get-Content path -Encoding UTF8                  # read (PS 7+: utf8; PS 5.1: ReadAllText safer)
[System.IO.File]::ReadAllText(path, [System.Text.UTF8Encoding]::new($false))  # read (NO BOM expected)
[System.IO.File]::WriteAllText(path, content, [System.Text.UTF8Encoding]::new($false))  # write (NO BOM)
```

**NEVER use `Set-Content -Encoding UTF8` / `Out-File -Encoding UTF8` to WRITE files.** On
Windows PowerShell 5.1 these write a UTF-8 **BOM** (bytes EF BB BF). A BOM at byte 0 is a
fatal error for Node.js shebang scripts (`#!/usr/bin/env node` → `SyntaxError: Invalid or
unexpected token`), breaks YAML frontmatter, and corrupts diffs. This exact failure was hit
2026-07-31 while writing `linkedin-auto-login.js` via PowerShell — the script crashed on
start with a BOM SyntaxError. **Use the write tool (clean UTF-8) or Python for JS/Python/
shell scripts. If PowerShell is truly forced, use `[System.IO.File]::WriteAllText` with
`UTF8Encoding($false)` as shown above.**

The `$false` parameter in `[System.Text.UTF8Encoding]::new($false)` means NO BOM.
A BOM (byte order mark, U+FEFF) silently breaks Pandoc frontmatter, YAML parsing,
and some git diffs. Always use `$false` (no BOM) unless the target system explicitly
requires a BOM.

---

## S1.5 PRE-COMMIT GATE

Before EVERY git commit, run the system-wide mojibake scanner:

```
python C:\Users\LENOVO\.deepchat\pre-commit-mojibake-scan.py
```

This detects BOM, U+FFFD, U+FFFF, and CP1252 double-encoding patterns. Any failure
is a HARD BLOCK on the commit. This gate exists because the resume v3.3 PDF and
computing-machines paper.md were both corrupted by the exact same PowerShell
encoding failure.

---

## S1.6 DETACHED PROCESS PATTERN (long-running ops)

**Problem:** Any `exec`/background command running longer than the harness yield
window gets its session killed — the process tree is reaped when the exec session
ends. This silently kills browser launches, MCP servers, downloads, and logins
mid-flight (hit 2026-07-31: LinkedIn `--login` Chrome window + auto-login script
died twice at the harness timeout; 4-minute poll loops cannot survive).

**Solution:** Start the process as a **detached `System.Diagnostics.Process`** with
async output readers that write to a log file. The process survives the exec
session; poll the log file afterwards.

```powershell
# CANONICAL DETACHED PROCESS PATTERN (write to .ps1 or run as script block)
$logFile = "$env:TEMP\my-task.log"
Remove-Item $logFile -ErrorAction SilentlyContinue
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "node.exe"                       # real exe, NOT npx/.cmd
$psi.Arguments = "`"C:\path\to\script.js`""
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.CreateNoWindow = $true
$psi.Environment["MY_ENV_VAR"] = "value"
$proc = [System.Diagnostics.Process]::Start($psi)
$proc.Id | Set-Content "$env:TEMP\my-task.pid"   # remember PID for later checks
$proc.BeginOutputReadLine()
$proc.BeginErrorReadLine()
Register-ObjectEvent -InputObject $proc -EventName OutputDataReceived -Action {
    $line = $Event.SourceEventArgs.Data
    if ($line) { Add-Content "$env:TEMP\my-task.log" "[stdout] $line" }
} | Out-Null
Register-ObjectEvent -InputObject $proc -EventName ErrorDataReceived -Action {
    $line = $Event.SourceEventArgs.Data
    if ($line) { Add-Content "$env:TEMP\my-task.log" "[stderr] $line" }
} | Out-Null
```

**Rules:**
- `FileName` MUST be a real `.exe` (`node.exe`, `python.exe`, `cmd.exe`). `npx`,
  `git`, `uvx` are `.cmd`/`.bat` shims — `Start-Process "npx"` fails with
  "not a valid Win32 application". Use `cmd /c npx ...` or the full `node.exe`
  path to the CLI entry.
- Poll progress via `Get-Content $logFile` and process aliveness via
  `Get-Process -Id (Get-Content $pidFile)`.
- Monitor Chrome/browser windows via `Get-Process chrome | Where-Object
  MainWindowTitle` — a title change (e.g. login page → "Feed | LinkedIn") is a
  reliable completion signal.

---

## S1.7 NODE.JS FILE GATE

Before running ANY written `.js` file, verify syntax:

```
node --check C:\path\to\script.js
```

This catches BOM corruption (PowerShell `Set-Content -Encoding UTF8` writes a BOM
that makes `#!/usr/bin/env node` throw `SyntaxError: Invalid or unexpected token`),
shebang issues, and edit damage — before a wasted launch attempt. Exit code 0 =
clean. Also prefer the `write` tool over PowerShell for script files: it writes
clean UTF-8 with no BOM.

---

## QUICK REFERENCE

| Task | PRIMARY (Python) | LAST RESORT (PowerShell) |
|:-----|:-----------------|:-------------------------|
| File read | `open(p, encoding='utf-8').read()` | `Get-Content p -Encoding UTF8` |
| File write | `open(p, 'w', encoding='utf-8').write(...)` | `[IO.File]::WriteAllText(p, s, [Text.UTF8Encoding]::new($false))` (never `Set-Content -Encoding UTF8` — BOM) |
| JSON parse | `json.loads(text)` | `ConvertFrom-Json` (in .ps1 file ONLY) |
| HTTP GET | `urllib.request.urlopen(url)` | `Invoke-RestMethod` |
| Regex search | `re.findall(pattern, text)` | `Select-String -Pattern '...'` |
| Dir listing | `os.listdir(path)` | `Get-ChildItem path` |
| Git operations | `subprocess.run(['git',...])` | `git -C path ...` (via exec) |
| Complex task | Write a .py file | Write a .ps1 file |
| f-string with dict subscript in `python -c` | Write `_*.py` → `exec python _*.py` (KIF-13) | N/A — guaranteed failure under PowerShell |
| `%VAR%` in `.npmrc`/`.env`/config files | Absolute path or `${VAR}` (KIF-14) | `cmd /c set` expands `%VAR%`; config parsers DON'T |
| Windows registry | N/A | `Get-ItemProperty` (last resort) |

## SELF-CHECK BEFORE EXECUTING (v2.1)

1. **Is this a Python operation?** → Write .py file, use `exec python`. DONE.
2. **Is this a native executable?** → `exec curl.exe`, `exec git`, `exec pandoc`. DONE.
3. **Is this a cmd-native operation?** → `exec cmd /c "..."`. DONE.
4. **Is this a long-running operation (>60s)?** → Use S1.6 DETACHED PROCESS PATTERN.
5. **Am I writing a JS/Python script?** → Use the `write` tool (clean UTF-8), then `node --check` / `python -m py_compile` before running.
6. **Is this genuinely impossible without PowerShell?** → OK, write .ps1 file, use ps-safe-exec.ps1, and NEVER `Set-Content -Encoding UTF8` for writes (BOM).
7. **If you are about to type `powershell -NoProfile -Command "..."` with ANY `$`, `&`, `|`, or `>`: ABORT.** Write a Python file instead.
8. **If you are about to type `python -c "..."` with an f-string containing `["..."]` (dict subscript) or a JSON literal: ABORT** (KIF-13). The nested double-quotes collide with PowerShell. Write `_*.py` and exec it.
9. **If you are about to write `%VAR%` into `.npmrc`/`.env`/YAML/JSON config: ABORT** (KIF-14). Config parsers don't expand `%VAR%` — use absolute paths or `${VAR}`.

**Python is not a fallback. Python is the DEFAULT.**

---

## DeepChat Runtime Context
- Skill root: `C:\Users\LENOVO\.deepchat\skills\windows-command-patterns`.
- Relative paths mentioned by this skill are relative to the skill root unless stated otherwise.
- When this skill needs script execution, prefer `skill_run` over `exec`.
- Bundled runnable scripts:
  - `scripts/ps-lint.ps1` — DEPRECATED as of v2.0 (reference only, do not load)
  - `scripts/ps-safe-exec.ps1` — LAST RESORT wrapper (use only when Python is impossible)
