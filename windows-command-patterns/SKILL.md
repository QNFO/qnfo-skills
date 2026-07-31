---
name: windows-command-patterns
description: Windows command execution — Python-First Protocol. Python is PRIMARY for ALL operations. PowerShell is DEPRECATED (LAST RESORT only). Use this skill to understand PowerShell's failure modes and when Python cannot be used.
version: "2.0"
---

# Windows Command Execution — Python-First Protocol (v2.0)

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
Get-Content path -Encoding UTF8                  # read
Set-Content path -Encoding UTF8 -Value ...       # write
[System.IO.File]::ReadAllText(path, [System.Text.UTF8Encoding]::new($false))  # read
[System.IO.File]::WriteAllText(path, ..., [System.Text.UTF8Encoding]::new($false))  # write (NO BOM)
```

**The `$false` parameter in `[System.Text.UTF8Encoding]::new($false)` means NO BOM.**
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

## QUICK REFERENCE

| Task | PRIMARY (Python) | LAST RESORT (PowerShell) |
|:-----|:-----------------|:-------------------------|
| File read | `open(p, encoding='utf-8').read()` | `Get-Content p -Encoding UTF8` |
| File write | `open(p, 'w', encoding='utf-8').write(...)` | `Set-Content p -Encoding UTF8` |
| JSON parse | `json.loads(text)` | `ConvertFrom-Json` (in .ps1 file ONLY) |
| HTTP GET | `urllib.request.urlopen(url)` | `Invoke-RestMethod` |
| Regex search | `re.findall(pattern, text)` | `Select-String -Pattern '...'` |
| Dir listing | `os.listdir(path)` | `Get-ChildItem path` |
| Git operations | `subprocess.run(['git',...])` | `git -C path ...` (via exec) |
| Complex task | Write a .py file | Write a .ps1 file |
| Windows registry | N/A | `Get-ItemProperty` (last resort) |

## SELF-CHECK BEFORE EXECUTING (v2.0)

1. **Is this a Python operation?** → Write .py file, use `exec python`. DONE.
2. **Is this a native executable?** → `exec curl.exe`, `exec git`, `exec pandoc`. DONE.
3. **Is this a cmd-native operation?** → `exec cmd /c "..."`. DONE.
4. **Is this genuinely impossible without PowerShell?** → OK, write .ps1 file, use ps-safe-exec.ps1.
5. **If you are about to type `powershell -NoProfile -Command "..."` with ANY `$`, `&`, `|`, or `>`: ABORT.** Write a Python file instead.

**Python is not a fallback. Python is the DEFAULT.**

---

## DeepChat Runtime Context
- Skill root: `C:\Users\LENOVO\.deepchat\skills\windows-command-patterns`.
- Relative paths mentioned by this skill are relative to the skill root unless stated otherwise.
- When this skill needs script execution, prefer `skill_run` over `exec`.
- Bundled runnable scripts:
  - `scripts/ps-lint.ps1` — DEPRECATED as of v2.0 (reference only, do not load)
  - `scripts/ps-safe-exec.ps1` — LAST RESORT wrapper (use only when Python is impossible)
