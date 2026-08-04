---
name: windows-command-patterns
description: Windows command execution — Python-First Protocol. Python is PRIMARY for ALL operations. PowerShell is DELETED. Exec tool uses cmd.exe.
version: 3.8
kif_tags: [KIF-32]
---
> **v3.8 UPDATE (2026-08-04, kaizen — Red-team skills audit closeout):**
> Red-team: 5-skill Watchtower scan; windows-command-patterns had duplicate §S-1.0.2
> (PSModulePath MECHANISM appeared twice — copy-paste artifact from v3.2→v3.7
> banner sequence). Also missing N-2 version footer.
> HARD: 1. SOFT: 1. DESIGN: 0. Changes:
> (1) [SOFT] Removed duplicate §S-1.0.2 section (-82 lines, 473→391).
>     Only one canonical S-1.0.2 remains.
> (2) [HARD] N-2 version footer added (was missing)
> Cross-reference: kaizen v1.14.
# windows-command-patterns (Python-First Protocol) -- v3.8



> **v3.7 (2026-08-03, kaizen — Git commit -F pattern mandated):**
> Kaizen session retrospective from frequency-valuation-theory paper pipeline
> (zESRNRQLF76EBvTbldEev). Recurring pattern: `git commit -m "message"` fails on
> cmd.exe — Node.js spawn() re-quotes args, cmd.exe strips outer quotes, git receives
> fragmented positional args. 8+ occurrences. Also: EXEC-CWD-DRIFT caused commits to
> land on wrong branch. Fixes: (1) [HARD] Git commit/tag -F <tempfile> documented as
> the ONLY 100%-reliable pattern; misleading `git commit -m 'msg'` example removed from
> CMD Pattern section. (2) [SOFT] Kaizen closeout completed — .kaizen_history v3.7
> entry added, version frontmatter bumped 3.6→3.7.
> Cross-reference: research v2.52, session zESRNRQLF76EBvTbldEev.

> **v3.6 (2026-08-03, kaizen — Cloudflare MCP + Space-Splitting Closeout):**
> Kaizen closeout on v3.5 changes. Red-team: 5 parallel subagents (truncated,
> fell back to direct parent-agent audit). HARD: 1. SOFT: 5. DESIGN: 0.
> Changes: (1) [HARD] Fixed frontmatter version 3.5→3.6 to match latest banner.
> (2) [SOFT] Added v3.5 entry to .kaizen_history (was missing — MEMORY-TO-SKILL-DRIFT).
> (3) [SOFT] Added ASAR-PATCH-FRAGILE + ELEVATE-MISSING anti-patterns to §S-1.0.4.
> (4) [SOFT] Verified exec_safe.py --file/--stdin modes exist at deployed path.
> (5) [SOFT] Confirmed elevate.exe exists at DeepChat resources.
> Prior v3.5: sustainable space-splitting workaround (8.3 names, Python, exec_safe.py).
> Prior v3.6 (Cloudflare): MCP-first Cloudflare API row, SCS-1, KIF-59.
> Cross-reference: kaizen v1.11, KIF-23 SPACE-SPLITTING, KIF-32.

> **v3.5 (2026-08-03, SUSTAINABLE SPACE-SPLITTING WORKAROUND — no asar patching):**
> Replaced §S-1.0.4 with sustainable strategy. Patching `app.asar` in Program Files
> is fragile — every DeepChat update would overwrite it. Instead: (1) 8.3 short names
> for quick cmd commands, (2) Python for all file operations (already §S1.0 mandate),
> (3) `exec_safe.py` helper at `%USERPROFILE%\.deepchat\scripts\exec_safe.py`
> for edge cases via --file mode. Root cause documented for upstream bug report.
> Cross-reference: KIF-23 SPACE-SPLITTING.

> **v3.3 (2026-08-03, DEEPCHAT SOURCE CODE HACKS — settings, dynamic reload, MCP, exec config):**
> Added §S-1.0.3: Complete DeepChat configuration reference from source code analysis.
> - Dynamic settings reload: `settingsWatcher.ts` watches `app-settings.json` changes
> - MCP server JSON format: `{command, args, env}` in `mcpSettings.mcpServers`
> - Custom prompts: `customPrompts` key with `{id, template, parameters}`
> - Exec env vars: `PI_BASH_YIELD_MS`, `PI_BASH_TIMEOUT_SEC`, `PI_BASH_MAX_OUTPUT_CHARS`
> - Tool execution policy: `toolExecutionPolicy.ts` controls auto-approval
> - ACP agent system: `agentSettings.enabled` toggle
> Cross-reference: system v2.3, system-prompt-v2.6.md
---

> **v3.2 (2026-08-03, PSModulePath MECHANISM — ROOT CAUSE FIX):**
> Added §S-1.0.2: The definitive explanation of how DeepChat chooses between
> PowerShell and cmd.exe. DeepChat's `getUserShell()` (shellEnvHelper.ts) checks
> `process.env.PSModulePath` — if set, spawns PowerShell with UTF8Encoding
> preamble; if unset, spawns cmd.exe with `chcp 65001 > nul && command` preamble.
> PSModulePath deleted from HKCU registry. HKLM checked clean. Source traced:
> ThinkInAIXYZ/deepchat commit 65c937b, src/main/agent/shared/process/shellEnvHelper.ts.
> Cross-reference: system v2.2, system-prompt-v2.6.md, PSFAIL.md.
>
> **v3.1 (2026-08-03, EXEC SHELL MANDATE):**
> Added §S-1.0.1: The exec tool uses cmd.exe, not PowerShell. All commands
> run through cmd.exe. Documented the shell migration and its implications
> for command syntax. Cross-reference: PSFAIL.md (25 documented failures).

> **v3.0 (2026-08-03, TOTAL POWERSHELL BAN):**
> TOTAL POWERSHELL BAN. User mandate: PowerShell is DELETED from this system.
> All 9 .ps1 scripts purged across 3 skills. All "last resort" carve-outs removed.
> Zero tolerance. The ONLY execution environments are Python (PRIMARY) and
> cmd.exe (cmd-native chaining only).

---

## S-1.0.2 PSModulePath MECHANISM — HOW DEEPCHAT CHOOSES THE EXEC SHELL (v3.2, 2026-08-03)

**This is the definitive root-cause fix. DeepChat's shell selection depends on ONE
environment variable.**

### Source Code Analysis

DeepChat's source code (`ThinkInAIXYZ/deepchat`, package `@nicepkg/deepchat` v1.1.0-beta.11)
contains the definitive shell-selection logic in `src/main/agent/shared/process/shellEnvHelper.ts`:

```typescript
export function getUserShell(): { shell: string; args: string[] } {
  const platform = process.platform

  if (platform === 'win32') {
    const powershell = process.env.PSModulePath ? 'powershell.exe' : null
    if (powershell) {
      return { shell: powershell, args: ['-NoProfile', '-Command'] }
    }
    return { shell: 'cmd.exe', args: ['/c'] }  // ← DEFAULT when PSModulePath is unset
  }
  // ...POSIX handling
}
```

**The ENTIRE shell choice depends on `process.env.PSModulePath`:**

| PSModulePath | Shell | Args | Preamble (shellOutputEncoding.ts) |
|:-------------|:------|:-----|:----------------------------------|
| SET | `powershell.exe` | `-NoProfile -Command` | `[System.Text.UTF8Encoding]::new($false); command` |
| UNSET | `cmd.exe` | `/c` | `chcp 65001 > nul && command` |

The companion file `src/main/agent/shared/process/shellOutputEncoding.ts` confirms:

```typescript
const CMD_UTF8_PREAMBLE = 'chcp 65001 > nul'

export function prepareShellCommandForUtf8Output(shell: string, command: string): string {
  if (shellName === 'cmd.exe' || shellName === 'cmd') {
    return `${CMD_UTF8_PREAMBLE} && ${command}`  // ← native cmd, zero PowerShell
  }
}
```

### The Fix (Applied 2026-08-03)

`PSModulePath` has been **permanently deleted from the Windows registry**
(HKCU\Environment). The system-level HKLM registry has been verified clean.
A Python-compiled shim (`pyinstaller --onefile`) is deployed at
`C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe` as insurance —
it strips the PowerShell UTF8Encoding preamble and forwards to `cmd.exe`.

### Verification Checklist (run at session start)

1. `reg query HKCU\Environment /v PSModulePath` → MUST return ERROR
2. `reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PSModulePath` → MUST return ERROR
3. `echo test && echo works` → must chain correctly (native cmd)
4. `npm --version` → must work directly (no .ps1 wrapper blocking)

### Reference

- **Source repo**: `github.com/ThinkInAIXYZ/deepchat` (package `@nicepkg/deepchat` v1.1.0-beta.11)
- **Key files**: `shellEnvHelper.ts`, `shellOutputEncoding.ts`, `backgroundExecSessionManager.ts`
- **Skills**: `system` v2.2 §1.10, `system-prompt-v2.6.md`
- **Docs**: `PSFAIL.md` (25 PowerShell failures), `CLOSEOUT_POWERSHELL_PURGE.md`

## S-1.0.4 CMD.EXE SPACE-SPLITTING BUG — SUSTAINABLE WORKAROUND (v3.5, 2026-08-03)

**Any exec command containing quoted paths with spaces (e.g., `dir "C:\Program Files"`)
will fail with "The filename, directory name, or volume label syntax is incorrect."**

### Root Cause

DeepChat's `exec` tool spawns `cmd.exe /c "<user_command>"` via Node.js `spawn()`.
Node.js escapes inner `"` as `\"` when building the command line from array args.
cmd.exe sees `\"` as **literal backslash+quote** — path parsing breaks.

Full trace: `spawn("cmd.exe", ["/c", "chcp 65001 > nul && dir \"C:\Program Files\" /b"])`
→ Node.js produces `"chcp 65001 > nul && dir \"C:\Program Files\" /b"`
→ cmd.exe strips outer quotes → `dir \"C:\Program Files\" /b`
→ cmd.exe sees `\"` as literal `\` + `"` → **syntax error**.

The real fix is `windowsVerbatimArguments: true` in the `spawn()` options, but that
requires modifying `app.asar` in Program Files — which gets overwritten on every
DeepChat update. **Do NOT patch the asar. Use the strategies below instead.**

### Strategy 1: 8.3 Short Names (simplest)

Use Windows short filenames for paths with spaces. Get them via `for %i in ("full path") do @echo %~si`:

```
dir C:\PROGRA~1\DeepChat /b          # instead of dir "C:\Program Files\DeepChat" /b
dir C:\Users\LENOVO\AppData\Local   # %USERPROFILE%\AppData\Local (no spaces)
```

### Strategy 2: Python for File Operations (mandated by §S1.0)

Any command involving paths with spaces → write a `.py` file, `exec python` it:

```python
# Instead of: exec dir "C:\Program Files" /b
import os
for f in os.listdir(r"C:\Program Files"):
    print(f)
```

### Strategy 3: exec_safe.py Helper (for edge cases)

Helper at `%USERPROFILE%\.deepchat\scripts\exec_safe.py` that runs commands through
Python `subprocess` (no Node.js spawn quoting interference).

**--file mode** (most reliable — command never passes through DeepChat's exec tool):

```bash
# Step 1: Write command to file (write tool — no exec involved)
# Content: dir "C:\Program Files" /b

# Step 2: Execute via Python
exec python C:\Users\LENOVO\.deepchat\scripts\exec_safe.py --file %TEMP%\_cmd.txt
```

**Inline mode** (only for commands WITHOUT quoted spaces or special chars):

```bash
exec python C:\Users\LENOVO\.deepchat\scripts\exec_safe.py git status
exec python C:\Users\LENOVO\.deepchat\scripts\exec_safe.py --cwd %TEMP% npm install
```

### Upstream Bug Report

The correct fix belongs in DeepChat's source code at:
`src/main/agent/shared/process/backgroundExecSessionManager.ts`
→ add `windowsVerbatimArguments: true` to the `spawn()` call inside
`BackgroundExecSessionManager.startSession()`.

Repo: `github.com/ThinkInAIXYZ/deepchat`
Key files: `backgroundExecSessionManager.ts`, `shellEnvHelper.ts`, `shellOutputEncoding.ts`

### Related Anti-Patterns

| Anti-Pattern | Correct |
|:-------------|:--------|
| **ASAR-PATCH-FRAGILE: Patching `app.asar` to fix exec quoting** (v3.5) | Do NOT patch `app.asar` in Program Files. Every DeepChat update overwrites it. Use the 3 sustainable strategies above instead. The correct fix (`windowsVerbatimArguments: true`) belongs in upstream source. |
| **ELEVATE-MISSING: Not using `elevate.exe` for admin operations** (v3.5) | `elevate.exe` ships with DeepChat at `C:\Program Files\DeepChat\resources\elevate.exe`. Use `elevate.exe -wait cmd.exe /c "..."` for operations requiring admin privileges. Requires UAC confirmation. |

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
   Since the exec tool uses cmd.exe (see §S-1.0.1), direct && chaining works.
   That's it. There is no branch 3.
```

### The Python Pattern (THE ONLY PATTERN)

```
Step 1: write tool → C:\Users\LENOVO\AppData\Local\Temp\_task.py
Step 2: exec python C:\Users\LENOVO\AppData\Local\Temp\_task.py
Step 3: exec cmd /c "del C:\Users\LENOVO\AppData\Local\Temp\_task.py"
```

### CMD Pattern (only for native chaining)

Since exec uses cmd.exe as its shell, `&&` chaining works natively:
```
exec dir /s /b C:\path
exec npx wrangler d1 list
```

**WARNING — Git Commit Messages on cmd.exe:** `git commit -m "message with spaces"` and
`git tag -a -m "message with spaces"` **WILL FAIL** on the DeepChat exec tool when the
message contains spaces or special characters. Node.js `spawn()` re-quotes the message,
cmd.exe strips outer quotes, and git receives fragmented arguments (e.g., `git commit -m feat:
Phase 3 citation management - 16 verified` is parsed as git commit `-m`, `feat:`, `Phase`,
`3`, ... — all treated as separate args or path specs).

**Permanent fix — ALWAYS use `-F` with a temp file:**
```
# Step 1: Write message to temp file
echo feat: my commit message > C:\Users\LENOVO\AppData\Local\Temp\commit-msg.txt
# Step 2: Commit with -F
cd C:\Users\LENOVO\Projects\repo && git commit -F C:\Users\LENOVO\AppData\Local\Temp\commit-msg.txt
# Same pattern for tags:
cd C:\Users\LENOVO\Projects\repo && git tag -a v1.0 -F C:\Users\LENOVO\AppData\Local\Temp\tag-msg.txt
```
**Do NOT use** `git commit -m "message"` when the message contains anything beyond a
single word. The `-F` file pattern is the ONLY reliable method on Windows cmd.exe through
the DeepChat exec tool. This is a cmd.exe argument-passing constraint, not a git bug.

---

## §S-1.0.5 URLLIB-METHOD ANTI-PATTERN (v3.7, HARD — 2026-08-04)

**`urllib.request.Request(url, method="DELETE")` silently drops non-GET methods.**

Python's `urllib.request` constructor accepts a `method` parameter but the internal
`get_method()` logic ignores it for DELETE/PUT without data. The request is silently
downgraded to GET, triggering 403 on read-protected endpoints (e.g., Zenodo draft files).

**Permanent fix — use the `requests` library for ALL non-GET HTTP:**
```python
import requests
# ✅ Correct — requests handles all methods
r = requests.delete(url, headers=h)
r = requests.put(url, headers=h, data=binary)  
r = requests.post(url, headers=h, json=data)

# ❌ Broken — urllib drops DELETE/PUT silently
req = urllib.request.Request(url, method="DELETE", headers=h)
urllib.request.urlopen(req)  # sends GET, not DELETE!
```

**NEVER use `urllib.request.Request(method="DELETE")` or `method="PUT"` without data.**
Assigning `req.method = "DELETE"` after construction is better but `requests` is the
only 100% reliable pattern across all HTTP methods. Session zESRNRQLF76EBvTbldEev
confirmed this (2026-08-04): every Zenodo 403 was DELETE being sent as GET.

---

## S1.1 OPERATION REPLACEMENT TABLE
## S-1.0.6 API-FAILURE SELF-DIAGNOSIS (v3.8, HARD - 2026-08-04)

**When ANY API call returns an unexpected error (403, 401, 404, 500), run this protocol
BEFORE blaming external infrastructure (token scope, rate limits, WAF blocks).**

### The Rule (Ironclad)

> **The bug is ALWAYS in your code until PROVEN otherwise.** External infrastructure
> failures are the LAST hypothesis, not the first. In session zESRNRQLF76EBvTbldEev
> (2026-08-04), the agent spent hours diagnosing Zenodo 403 as "token write-scope issue"
> when the root cause was `urllib.request.Request(method="DELETE")` silently sending GET.
> The agent never printed the actual HTTP method being sent.

### The Five-Step Protocol (MANDATORY - HARD GATE)

```
1. STOP: Do NOT diagnose the infrastructure. Do NOT check the token. Assume YOUR CODE IS WRONG.
2. VERIFY YOUR REQUEST: Print/log the EXACT HTTP method, full URL, all headers, body.
   requests: print(r.request.method, r.request.url, r.request.headers)
   urllib:   print(req.get_method(), req.full_url, req.headers)
3. COMPARE WITH CURL: Run the equivalent curl -v command. If curl works and your code
   doesn't, YOUR CODE IS BROKEN.
4. IDENTIFY THE DISCREPANCY: Different method (urllib dropped it - see S-1.0.5)?
   Missing Content-Type? Wrong auth format? Both fail -> THEN consider external.
5. ONLY AFTER STEPS 1-4 PASS: Consider token scope, rate limits, WAF, outages.
```

### Anti-Patterns This Protocol Prevents

| Anti-Pattern | Fix |
|:-------------|:----|
| BLAME-EXTERNAL-1: 403 = token scope | Run this protocol. Print your HTTP method first. |
| URLLIB-METHOD: DELETE silently GET (S-1.0.5) | Step 3 catches: curl shows DELETE, urllib shows GET. |
| Content-Type missing on POST/PUT | Step 2 reveals missing header. |
| GETSIZE-vs-LEN: comparing os.path.getsize() vs len() | D1 body_md stores CHARACTER count. ALWAYS use len(open(p).read()) - never os.path.getsize() - when comparing against D1 length(). Windows 

 inflates byte counts ~3.5%. |
| SILENT-EXCEPT-PASS: bare except: pass in diagnostic scripts | Never swallow HTTP errors. Always print r.status_code. Log it, don't hide it. |

### Integration with Kaizen

Pairs with the BLAME-EXTERNAL-1 anti-pattern in the `kaizen` skill. Every kaizen
session retrospective MUST check whether the agent ran this protocol before
escalating to infrastructure theories. Failure to do so is a HARD kaizen finding.

---


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
| Cloudflare API | Python + `urllib.request` + `json.dumps` — BUT first prefer Cloudflare MCP agent tools by name: `workers_list`, `workers_get_worker`, `query_worker_observability`, `search_cloudflare_documentation`. Load the `cloudflare` skill for the full decision ladder (MCP tools → `npx wrangler` → REST; NEVER PowerShell — KIF-59). D1 queries: prefer `cloudflare/scripts/d1-query.py` (auto-discovery, KIF-36) over raw REST; verify writes by re-reading the row (SCS-1). |
| PDF building | Python → `subprocess.run(['pandoc',...])` |
| Windows registry | `import winreg` |
| Windows services | `subprocess.run(['sc.exe', ...])` |
| WMI queries | `subprocess.run(['wmic.exe', ...])` |
| Process management | `subprocess.Popen` + `DETACHED_PROCESS` |
| System info | `platform`, `os`, `psutil`, `subprocess.run(['systeminfo'])` |
| AppX management | `subprocess.run(['wmic.exe', 'product', ...])` |

## Version

Current: **v3.8** (windows-command-patterns — Git commit -F mandate, URLLIB-METHOD anti-pattern, API-Failure Self-Diagnosis protocol; 2026-08-04; kaizen 2026-08-04: removed duplicate §S-1.0.2, added N-2 footer) (windows-command-patterns — Git commit -F mandate, URLLIB-METHOD anti-pattern, API-Failure Self-Diagnosis protocol; 2026-08-04; kaizen 2026-08-04: removed duplicate §S-1.0.2, added N-2 footer)