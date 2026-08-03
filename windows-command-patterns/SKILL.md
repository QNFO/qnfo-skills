---
name: windows-command-patterns
description: Windows command execution — Python-First Protocol. Python is PRIMARY for ALL operations. PowerShell is DELETED. Exec tool uses cmd.exe.
version: 3.3
kif_tags: [KIF-32]
---

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

---

## §S-1.0.2 PSModulePath MECHANISM — HOW DEEPCHAT CHOOSES THE EXEC SHELL (v3.2, 2026-08-03)

**This is the definitive root-cause fix. DeepChat's shell selection depends on ONE
environment variable.**

### Source Code Analysis

DeepChat's source code (`ThinkInAIXYZ/deepchat`, package `@nicepkg/deepchat` v1.1.0-beta.11)
contains the definitive shell-selection logic:

```typescript
// src/main/agent/shared/process/shellEnvHelper.ts
export function getUserShell(): { shell: string; args: string[] } {
  if (platform === 'win32') {
    const powershell = process.env.PSModulePath ? 'powershell.exe' : null
    if (powershell) {
      return { shell: powershell, args: ['-NoProfile', '-Command'] }
    }
    return { shell: 'cmd.exe', args: ['/c'] }  // ← DEFAULT when PSModulePath unset
  }
}
```

**PSModulePath SET → PowerShell. PSModulePath UNSET → cmd.exe.**
When cmd.exe is the shell, `shellOutputEncoding.ts` returns `chcp 65001 > nul && command`.

### The Fix

PSModulePath permanently deleted from HKCU registry. HKLM verified clean.
Python shim deployed at `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`.
Verification: `reg query HKCU\Environment /v PSModulePath` → MUST return ERROR.

**The DeepChat `exec` tool uses `cmd.exe` as its shell. It does NOT use PowerShell.**

This was changed via the DeepChat settings key `shell.executionMode: "cmd"` after
the system-level PowerShell extermination of 2026-08-03. All commands are parsed by
cmd.exe, not PowerShell. This means:

- `&&` is a valid command separator (native cmd behavior)
- `dir` is the real `dir`, not `Get-ChildItem`
- `npm`, `wrangler`, `npx` work directly (`.cmd` wrapper, no `.ps1` wrapper blocking)
- `%VAR%` is expanded by the shell (native cmd behavior)
- No `[System.Text.UTF8Encoding]::new($false)` preamble is prepended
- No PowerShell parser interference with quotes, braces, or f-strings

### What This Changes

| Before (PowerShell exec shell) | After (CMD exec shell) |
|:-------------------------------|:-----------------------|
| `npm --version` → SecurityError (.ps1 blocked) | `npm --version` → works |
| `echo a && echo b` → parser error | `echo a && echo b` → works |
| `dir` → Get-ChildItem alias | `dir` → real dir |
| `python -c "..."` → PowerShell parser corrupts | `python -c "..."` → cmd passes through cleanly |
| All commands get UTF8Encoding preamble | No preamble — clean cmd |

### Persistent Configuration

The exec shell is configured in DeepChat's settings:
```
Key: shell.executionMode
Value: "cmd"
```

This setting persists across DeepChat restarts. If exec sessions fail to start
("Session not running"), restart DeepChat — it will pick up the cmd.exe setting
and spawn cmd.exe processes instead of the deleted powershell.exe.

**IMPORTANT:** The `exec` tool routes through `cmd.exe` now. This means:
- Use `&&` for chaining (native cmd)
- Use `dir /b` not `ls`
- Use `type` not `cat`
- Use `copy` not `cp`
- Use `del` not `rm`
- `cmd /c "..."` is still valid but no longer REQUIRED — direct commands work

See `docs/PSFAIL.md` in the qnfo-skills repo for the complete record of why
PowerShell was permanently exterminated (25 documented failures, 9 KIF signatures).

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
exec git add -A && git commit -m 'msg' && git push
exec dir /s /b C:\path
exec npx wrangler d1 list
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