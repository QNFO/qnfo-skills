---
name: windows-command-patterns
description: Windows PowerShell error prevention. KIF-05/06/07/09 enforcement via ps-lint.ps1 and ps-safe-exec.ps1. Activate before any exec, grep, or Select-String on Windows.
---

# Windows Command Execution Patterns — v1.2 (Permanent Instruction Layer + Active Tools)

> **v1.1 UPDATE (2026-07-29):** Added `scripts/ps-lint.ps1` (KIF-05/06/07/09 pre-flight validator) and `scripts/ps-safe-exec.ps1` (lint-then-execute wrapper that BLOCKS bad commands). These tools eliminate the "execute first, fail later" anti-pattern — 100% of KIF-05/06/07 errors are now caught BEFORE exec. Added mandatory **Pre-Flight Protocol** below.

## execute_plan

**HARD GATE (v1.2, 2026-07-31): If PowerShell has failed with a $variable error in this
session, ALL subsequent PowerShell MUST go through a .ps1 file. No exceptions, no
"maybe this time it'll work." The pattern is: inline PowerShell → $variable eaten
→ syntax error → rewrite as .ps1 file. Skip directly to .ps1 file.**

Before EVERY `exec` call that contains PowerShell (or could be misinterpreted as PS):

update_plan([
  {"step": "HARD-CHECK: Has this session had a PS $variable parse error? If YES: write .ps1 file. STOP.", "status": "pending"},
  {"step": "SELF-CHECK: Does command contain $ (beyond simple $env:), &, ||, &&, regex in double-quotes, {.Property}, or >2 pipes?", "status": "pending"},
  {"step": "If ANY pattern found: ABORT — write .ps1 file. KIF-09 is not a suggestion.", "status": "pending"},
  {"step": "Only if command is 100% single-statement, zero-variable, zero-pipe: execute inline", "status": "pending"},
])

---

## MANDATORY Pre-Flight Protocol (v1.1 — DO NOT SKIP)

**This is the permanent fix layer.** Before ANY `exec` call on Windows:

### Step 1: Check if any KIF pattern is present
Scan your command for these red flags:
- `&` (not followed by `$`, `{`, `"`, or `'` — then it's a separator, not a call operator)
- `||` or `&&` (Unix operators — invalid in PS)
- Double-quoted regex containing `|`, `(`, `)`, `{`, `}`, `$`, `^`, or `\`
- `E={.Property}` in a calculated property (missing `$_`)
- `>2` pipe stages, `$var =`, `ConvertFrom-Json`, or `@{N=/E=}` in a one-liner

### Step 2: Run ps-lint.ps1 on the command
```powershell
# BEFORE executing, validate:
skill_run windows-command-patterns scripts/ps-lint.ps1 --args '-Command','<your command here>'

# Or via exec:
exec powershell -NoProfile -File "C:\Users\LENOVO\.deepchat\skills\windows-command-patterns\scripts\ps-lint.ps1" -Command '<your command>'
```

### Step 3: Interpret results
| Exit Code | Meaning | Action |
|:----------|:--------|:-------|
| 0 | PASS — no issues | Safe to execute |
| 1 | WARN — KIF-09 complexity flag | Consider .ps1 file; proceed at your discretion |
| 2 | FAIL — KIF-05/06/07 HARD BLOCK | **ABORT.** Fix the command. The suggested fix in the output is correct. |

### Step 4: If blocked, use ps-safe-exec.ps1 as a wrapper
```powershell
# This will lint first, then execute ONLY if clean:
exec powershell -NoProfile -File "C:\Users\LENOVO\.deepchat\skills\windows-command-patterns\scripts\ps-safe-exec.ps1" -Command '<fixed command>'

# Strict mode (blocks KIF-09 too):
exec powershell -NoProfile -File "C:\Users\LENOVO\.deepchat\skills\windows-command-patterns\scripts\ps-safe-exec.ps1" -Command '<command>' -Strict
```

### Step 5: If ps-lint says "write a .ps1 file" — DO IT
KIF-09 is not a soft suggestion. Multi-pipe/variable/JSON one-liners fail for structural reasons (quote collapse, scoping, pipeline quirks) that NO amount of escaping can fix. Write the script, save to disk, execute with `-File`.

---

## KIF-05: SHELL MISMATCH — Unix/cmd Operators in PowerShell

### BANNED: `&` for command chaining
In PowerShell, `&` is the call/invoke operator, NOT a command separator.

**FAILED** (session e4layp9):
```powershell
wmic os get Caption /format:list & systeminfo | findstr "Memory"
# Error: "The ampersand (&) character is not allowed"
```
**CORRECT:**
```powershell
wmic os get Caption /format:list; systeminfo | Select-String "Memory"
```

### BANNED: `||` and `&&` (Unix OR/AND)
PowerShell does not support `||` or `&&`.

**FAILED** (session e4layp9):
```powershell
dir /s /b "C:\path" 2>nul || echo "Not found"
# Error: "The token '||' is not a valid statement separator"
```
**CORRECT:**
```powershell
# Option A: cmd /c wrapper
cmd /c "dir /s /b C:\path 2>nul || echo Not found"

# Option B: PS native
$result = Get-ChildItem -Path "C:\path" -Recurse -ErrorAction SilentlyContinue
if (-not $result) { Write-Host "Not found" }
```

### BANNED: `^` as escape character in PowerShell
`^` is cmd.exe's escape character. PowerShell uses `` ` `` (backtick).

**FAILED** (session e4layp9):
```powershell
powershell -Command ^& { Get-Content ... }
# Error: "The ampersand (&) character is not allowed"
```
**CORRECT:**
```powershell
powershell -NoProfile -Command "Get-Content ..."
```

**ps-lint detection:** Flags `&` not followed by `$`, `{`, `"`, or `'`; always flags `||` and `&&`.

---

## KIF-06: QUOTE LAYER COLLAPSE — Regex `|` Becomes PowerShell Pipe

**THIS IS THE #1 MOST RECURRING FAILURE (4+ occurrences per session).**

### BANNED: Double-quoted regex with `|` alternation
Inside double quotes, PowerShell interprets `|` as the pipeline operator, even inside `-Pattern` arguments.

**FAILED** (session e4layp9 — 4 times):
```powershell
Select-String -Path "file.json" -Pattern "(theme|fontSize|sound)"
Get-Content "file.json" | Select-String -Pattern "\"(theme|fontSize)\""
# Error: "The term 'theme' is not recognized as the name of a cmdlet"
```

**CORRECT:**
```powershell
# ALWAYS use SINGLE-QUOTED strings for regex patterns
Select-String -Path "file.json" -Pattern '(theme|fontSize|sound)'
Get-Content "file.json" | Select-String -Pattern '"(theme|fontSize)"'
```

**Rule:** If your regex contains `|`, `(`, `)`, `{`, `}`, `$`, `^`, or `\` — use single quotes. Single-quoted strings in PowerShell are LITERAL.

### BANNED: `cmd /c findstr` with complex quoting
Triple-double-quotes cause "missing terminator" errors.

**FAILED** (session e4layp9):
```cmd
cmd /c "findstr /C:"""theme"" /C:"""fontSize""" file.json"
```

**CORRECT:** Always use `Select-String` instead of `findstr`.
```powershell
Select-String -Path "file.json" -Pattern 'theme|fontSize'
```

**ps-lint detection:** Flags any `-Pattern "..."`, `Select-String "..."`, `-replace "..."` where the double-quoted string contains `|`. Also flags generic `"(group1|group2)"` patterns.

---

## KIF-07: PIPELINE VARIABLE OMISSION — Missing `$_`

### BANNED: `.Property` without `$_` in script blocks
In `ForEach-Object { }` and `Select-Object @{E={ }}` blocks, reference the current pipeline object as `$_`.

**FAILED** (session e4layp9 — 2 times):
```powershell
Get-PSDrive C | Select-Object @{N='Used';E={[math]::Round(.Used/1GB,1)}}
# Error: "Missing ')' in method call" / "Unexpected token '.Used/1GB'"
```

**CORRECT:**
```powershell
Get-PSDrive C | Select-Object @{N='Used';E={[math]::Round($_.Used/1GB,1)}}
```

### BANNED: `; |` (semicolon immediately before pipe)
**CORRECT:** Remove the semicolon — pipe directly from the previous command.

**ps-lint detection:** Flags `E={.Property` pattern (dot-property without `$_`).

---

## KIF-08: TOOL SCOPE VIOLATION — grep/glob Outside Workspace

### BANNED: `grep` and `glob` for paths outside the workspace
Workspace is `C:\Users\LENOVO\AppData\Local\Programs\DeepChat`. `AppData\Roaming\DeepChat` and `.deepchat` are OUTSIDE.

**FAILED** (session e4layp9):
```
grep "C:\Users\LENOVO\AppData\Roaming\DeepChat" → "path outside allowed directories"
glob "C:\Users\LENOVO\.deepchat" → "path scope must be inside the workspace"
```

**CORRECT:** Use `exec` with PowerShell for external paths.
```powershell
exec powershell -Command "Get-ChildItem -Path 'C:\Users\LENOVO\AppData\Roaming\DeepChat' -Filter '*.json' -Recurse"
exec powershell -Command "Get-ChildItem -Path 'C:\Users\LENOVO\.deepchat' -Recurse | Select-String 'pattern'"
```

**Workspace-ONLY:** `grep`, `glob`
**Any-path:** `read`, `write`, `edit`, `exec`

---

## KIF-09: COMPLEX ONE-LINER FRAGILITY — Script-First Rule

### BANNED: Complex PS one-liners through exec
If your command has **ANY** of the following, write a `.ps1` file instead:
- More than 2 pipe stages
- Regex patterns with `|` alternation
- Variable assignments (`$x = ...`)
- Calculated properties (`@{N=;E={}}`)
- Mixed quoting (single + double quotes)
- JSON parsing with `ConvertFrom-Json`

**FAILED** (session e4layp9 — 8 of 10 failures):
- `Get-PSDrive | Select @{...}` (missing `$_`)
- `Get-Content | Select-String '(a|b)' | ForEach` (regex `|` → PS pipe)
- `$content = Get-Content; $obj = ConvertFrom-Json; $obj.prop` (scoping failures)

**CORRECT PATTERN:**
```powershell
# Step 1: Write script to temp file via write tool
# Target: C:\Users\LENOVO\AppData\Local\Temp\my_script.ps1

# Step 2: Execute
exec powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\LENOVO\AppData\Local\Temp\my_script.ps1"
```

**Inside the .ps1 file (example):**
```powershell
$content = Get-Content 'C:\Users\LENOVO\AppData\Roaming\DeepChat\app-settings.json' -Raw
$obj = ConvertFrom-Json $content
$obj | Select-Object -Property language, theme, soundEnabled, copyWithCotEnabled
```

**Why:** The .ps1 file is a SINGLE interpretation layer. No nested quote escaping between exec, cmd, and PowerShell.

**ps-lint detection:** Flags pipe count >2, variable assignments, `ConvertFrom-Json`, calculated properties, mixed quoting. In `-Strict` mode, these become HARD FAILS.

---

## Bundled Tools

### `scripts/ps-lint.ps1` — Pre-Flight Validator
Validates a PowerShell command against all KIF patterns. Returns structured output.
```powershell
# Check a command before executing:
skill_run windows-command-patterns scripts/ps-lint.ps1 --args '-Command','Select-String -Pattern "(a|b)" file.txt'
# → FAIL: KIF-06 regex in double quotes

# JSON output for programmatic use:
skill_run windows-command-patterns scripts/ps-lint.ps1 --args '-Command','Get-ChildItem | Select Name,Length','-Json'
# → {"severity":"PASS","issues":[],"command":"...","timestamp":"..."}

# Strict mode (KIF-09 warnings become errors):
skill_run windows-command-patterns scripts/ps-lint.ps1 --args '-Command','<cmd>','-Strict'
```

### `scripts/ps-safe-exec.ps1` — Lint-Then-Execute Wrapper
Validates THEN executes. If KIF-05/06/07 detected, BLOCKS execution entirely.
```powershell
# Safe execution (lint first, execute only if clean):
skill_run windows-command-patterns scripts/ps-safe-exec.ps1 --args '-Command','Get-ChildItem | Select -First 5'

# Validate only (no execution):
skill_run windows-command-patterns scripts/ps-safe-exec.ps1 --args '-Command','<cmd>','-NoExecute'

# Strict mode (blocks KIF-09 too):
skill_run windows-command-patterns scripts/ps-safe-exec.ps1 --args '-Command','<cmd>','-Strict'
```

---

## QUICK REFERENCE

| Task | Correct | Wrong |
|---|---|---|
| Command chaining | `cmd1; cmd2` | `cmd1 & cmd2` |
| Error-dependent exec | `cmd /c "cmd1 \|\| cmd2"` | `cmd1 \|\| cmd2` |
| Regex search PS | `Select-String -Pattern '(a\|b)'` | `Select-String -Pattern "(a\|b)"` |
| Search outside workspace | `exec powershell -Command "ls \| sls 'p'"` | `grep "p" C:\path` |
| Disk GB calc | `{$_.Used/1GB}` | `{.Used/1GB}` |
| JSON parse | Write a .ps1 file | Inline `ConvertFrom-Json` one-liner |
| Complex command | Write a .ps1 file | Multi-pipe one-liner through exec |

## SELF-CHECK BEFORE EXECUTING (v1.2 HARDENED)

**?? RULE ZERO (v1.2): IF ANY POWERSHELL COMMAND HAS FAILED WITH A $VARIABLE ERROR IN THIS SESSION, ALL SUBSEQUENT POWERSHELL GOES THROUGH .PS1 FILES. NO EXCEPTIONS. RE-ATTEMPTING INLINE POWERSHELL AFTER A PROVEN FAILURE IS A HARD ANTI-PATTERN.**

0. **Has this session had $variable parse errors?** -> **STOP. Write a .ps1 file. ALWAYS.**
1. Uses `$` (beyond simple `$env:VAR`)? -> STOP, write a .ps1 file.
3. Regex pattern uses double quotes? -> STOP, switch to single quotes.
4. Script block uses `.Property` without `$_`? -> STOP, add `$_` (in .ps1 file).
5. Using grep/glob for AppData/.deepchat? -> STOP, use exec + PowerShell.
6. More than 1 pipe or uses any variable assignment? -> STOP, write a .ps1 file.
7. **If you are about to type `powershell -NoProfile -Command "..."` with ANY `$`: ABORT.**

**The .ps1 file pattern:** `write` tool -> `exec powershell -NoProfile -ExecutionPolicy Bypass -File "<path>"` -> done. Three tool calls but ZERO failures. Faster than 5+ failed inline attempts.


## DeepChat Runtime Context
- Skill root: `C:\Users\LENOVO\.deepchat\skills\windows-command-patterns`.
- Relative paths mentioned by this skill are relative to the skill root unless stated otherwise.
- When this skill needs script execution, prefer `skill_run` over `exec`.
- Bundled runnable scripts:
  - `scripts/ps-lint.ps1` — KIF-05/06/07/09 pre-flight validator (v1.1)
  - `scripts/ps-safe-exec.ps1` — lint-then-execute wrapper (v1.1)
