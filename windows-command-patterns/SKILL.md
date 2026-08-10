---


name: windows-command-patterns


description: Windows command execution — Python-First Protocol. Python is PRIMARY for ALL operations. PowerShell is DELETED. Exec tool uses cmd.exe.


version: 3.19


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


> **v3.10 UPDATE (2026-08-04, kaizen — GIT-COMMIT-M-QUOTE-1 + EXEC-TOOL-QUOTE-1-PY):**


> Red-team: direct parent-agent audit of session 1tz85-vMiqh2TyFySznBA (IPR publication pipeline).


> HARD: 0. SOFT: 2. DESIGN: 0. Changes:


> (1) [SOFT] **GIT-COMMIT-M-QUOTE-1 anti-pattern row added** — `git commit -m` with em-dashes/


>     spaces fails on cmd.exe (4 failures this session); canonical fix is write-tool


>     message file + `git commit -F`. Was buried in §S1.0 prose; now in the table.


> (2) [SOFT] **EXEC-TOOL-QUOTE-1-PY anti-pattern row added** — exec also quotes `python <abs-path>.py`


>     arguments (workspace-path prefix + quotes); fix is cd + bare relative path.


>     `python -c` with nested quotes always fails (5 failures this session).


> Cross-reference: kaizen v1.20, research v2.63, session 1tz85-vMiqh2TyFySznBA.





> **v3.11 UPDATE (2026-08-04, kaizen — WIN-LONGPATH-1: MAX_PATH 260-char limit blocks deletion of deeply-nested trees):**


> Red-team: session 5ptZtvKLdqr3GzAykql8G (D-drive migration closeout).


> HARD: 1. Changes:


> (1) [HARD] **WIN-LONGPATH-1 anti-pattern added** — deleting a deeply-nested tree whose


>     absolute paths exceed Windows MAX_PATH (260 chars) fails with `rmdir /s /q` /


>     `shutil.rmtree` / `os.remove` even after clearing read-only attributes. Symptom:


>     `rmdir: exit 0` but `exists: True` (cmd swallows the per-file failure and prints


>     "The system cannot find the path specified"); shutil raises `PermissionError`


>     or `FileNotFoundError` on a specific long leaf. Canonical case: D:\Archive with


>     `.git/objects/xx/<40-hex>` files under 300+ char paths — D: stayed at 7.4 GB


>     after the first 3 delete attempts. **Fix: use the `\\?\` extended-length prefix:**


>     `shutil.rmtree('\\\\?\\' + os.path.abspath(path))` deletes the tree regardless


>     of path depth (verified: Archive 54,239 files + 6.2 GB deleted in one pass).


>     See §WIN-LONGPATH-1.









# windows-command-patterns — v3.19

> **v3.19 UPDATE (2026-08-10, kaizen — CURL-AUTH-QUOTE-1: exec-safe authenticated curl pattern; session bPhAUCI_FRVeZyA5Rxmsm):**
> Red-team: direct parent-agent 5-adversary audit (CMD SKILLS UPDATE; secrets rotation audit session — every
> quoted exec arg failed through cmd.exe/Node spawn). HARD: 1. SOFT: 1. DESIGN: 1. Changes:
> (1) [HARD] **CURL-AUTH-QUOTE-1 anti-pattern + S-1.0.10 section added** — through the exec tool, ALL quoted
>     args are mangled: `-H "Authorization: Bearer %VAR%"` → header dropped (Cloudflare 1001 "Missing
>     Authorization", GitHub 401); unquoted `-H Authorization:Bearer%VAR%` → 6111 "Invalid format" (no space
>     after scheme). Canonical reliable form (verified live 2026-08-10): `--oauth2-bearer %VAR%` (curl builds
>     `Authorization: Bearer <token>` with the required space; unquoted, no cmd mangling) + `-H Name:value`
>     for headers whose value has NO space (`-H Content-Type:application/json`) + `--data-binary @file` for
>     JSON bodies + `> out.txt` (cmd redirect, not `-o` which gets path-mangled). Applies to Cloudflare,
>     GitHub, Zenodo, D1 REST.
> (2) [SOFT] **`findstr`/`dir` with quoted args fail** — `findstr /n "# QNFO Core"` returned exit 1 (space in
>     quoted pattern split by cmd). Use write→exec python for pattern search, or single-token patterns.
> (3) [DESIGN] **S-1.0.10 section added** — full exec-safe HTTP recipe (auth + headers + body + redirect).
> Cross-reference: CURL-AUTH-QUOTE-1, cloudflare v3.37 (D1-REST-PAYLOAD-1, TOKEN-VERIFY-SCOPE-1),
> kaizen v1.96, qnfo-core v1.23, session bPhAUCI_FRVeZyA5Rxmsm.

> **v3.18 UPDATE (2026-08-10, kaizen — exec space-path false negatives + cleanup-claim masking + pywin32 COM):**
> Red-team: direct parent-agent 5-adversary audit (session FqszmI7iAvYDr6_X3C2qv — CMD SKILLS UPDATE).
> HARD: 3. SOFT: 1. DESIGN: 0. Changes:
> (1) [HARD] **EXEC-PATH-SPACE-FALSE-NEGATIVE-1** — broken-quoted probes on space-containing paths
>     produced a FALSE 'Outlook not installed' claim; user corrected the agent. 8.3 short names / os.listdir are the fix.
> (2) [HARD] **CMD-ECHO-SUCCESS-MASK-1** — `2>nul & echo CLEANED` faked exit 0 while files remained (H1 red-team finding).
> (3) [HARD] **WSH-OUTLOOK-COM-MEM-1** — cscript/WSH fails on this host; pywin32 COM is the verified Outlook path.
> (4) [SOFT] **CUA-DRIVER-QUARANTINE-1** — quarantined cua-driver kills list_apps; COM/filesystem fallback documented.
> Cross-reference: kaizen v1.95, S-1.0.4, computer-use skill, qnfo-core VERIFY-DONT-ASSUME-1.

> **v3.16 UPDATE (2026-08-06, kaizen — CUA tools integration: Computer Use as GUI automation path):**
> Red-team: direct parent-agent 5-adversary audit (session QPBAVeVkU0Y5qkMNG6CC9).
> HARD: 0. SOFT: 1. DESIGN: 0. Changes:
> (1) [SOFT] **CUA tools reference added** — WIN-TRUSTEDINSTALLER-REG-1 row now references
>     DeepChat Computer Use (CUA) tools (`list_apps` → `launch_app` → `get_window_state` →
>     `click`/`type_text`) as a programmatic GUI automation path for Settings GUI operations.
>     GUI automation row added to Operation Replacement table. Load `computer-use` skill for
>     the full CUA protocol.
> Cross-reference: kaizen v1.66, computer-use skill, session QPBAVeVkU0Y5qkMNG6CC9.

> **v3.15 UPDATE (2026-08-05, kaizen — EXEC-AUTOBG-DEATH-1 + write-file-read-back):**
> Red-team: direct parent-agent audit of session 8APhB8pdpgihrWgDLpXIP cycle 2.
> HARD: 0. SOFT: 1. DESIGN: 0. Changes:
> (1) [SOFT] **EXEC-AUTOBG-DEATH-1 anti-pattern row added** — short `exec` commands
>     repeatedly auto-background and die ("Session bg_XXX is not running") in this
>     environment. The reliable workaround is the **write-file-read-back pattern**:
>     the script writes its output to a `.txt` file, `exec` runs it, the agent reads
>     the file back. Canonical case: session 8APhB8pdpgihrWgDLpXIP — 10+ exec calls
>     died; every output-to-file pattern succeeded. See §S-1.0.9.
> Cross-reference: kaizen v1.47, PYTHON-BUFFERING-1, session 8APhB8pdpgihrWgDLpXIP.

> **v3.14 UPDATE (2026-08-05, kaizen — GH-API-HANG-1):**


> Red-team: direct parent-agent audit of session 8APhB8pdpgihrWgDLpXIP


> (research briefing system build — GitHub star backlog execution).


> HARD: 0. SOFT: 1. DESIGN: 0. Changes:


> (1) [SOFT] **GH-API-HANG-1 anti-pattern row added** — `gh api` (especially with


>     `--paginate`) hangs indefinitely in this environment (exec session never


>     returns, must be killed). Token-based urllib calls (GITHUB_TOKEN env or


>     `gh auth token`) complete reliably. Canonical case: session 8APhB8pdpgihrWgDLpXIP


>     — gh api -X GET user/starred --paginate hung 3x; same op via Python urllib


>     with GITHUB_TOKEN completed instantly; 4 repos starred successfully.


> Cross-reference: kaizen v1.43, git-github, session 8APhB8pdpgihrWgDLpXIP.





> **v3.12 UPDATE (2026-08-04, kaizen — PANDOC-FONT-QUOTE-1 + session retrospective ZDdTu9Qf):**


> Red-team: direct parent-agent audit of session ZDdTu9QfTZKY_kJALlXY_ (Consilience Framework


> synthesis). HARD: 0. SOFT: 1. DESIGN: 0. Changes:


> (1) [SOFT] **PANDOC-FONT-QUOTE-1 anti-pattern row added** — pandoc `-V mainfont="DejaVu Serif"`


>     fails on Windows cmd.exe with space-splitting; fix is omit font flags, use Python


>     subprocess, or use DejaVuSans font name without spaces. Canonical case: 37-page PDF


>     built successfully with default fonts after font argument failure.


> Cross-reference: kaizen v1.29, session ZDdTu9QfTZKY_kJALlXY_.





> **v3.13 UPDATE (2026-08-05, kaizen — Windows admin elevation + TrustedInstaller registry lesson):**


> Red-team: direct parent-agent 5-adversary audit of session VBvCOsXhzlQJUubBqtdFz


> (bloat extermination: Edge policies, Office ClickToRun, Widgets disable).


> HARD: 1. SOFT: 3. DESIGN: 1. Changes:


> (1) [HARD] **S-1.0.8 WINDOWS ADMIN ELEVATION section added** — ShellExecute "runas"


>     UAC pattern, elevate.exe usage, sc service control, taskkill, TrustedInstaller


>     caveat. Agent can now self-elevate for admin operations.


> (2) [SOFT] **WIN-TRUSTEDINSTALLER-REG-1 anti-pattern added** — certain Windows 11


>     registry keys (HKLM\Policies\Microsoft\Dsh, HKCU\Feeds) are ACL-protected


>     even from admin; use PolicyManager MDM path or manual Settings.


> (3) [SOFT] **Stale cross-refs fixed** — cloudflare v3.33/v3.27→v3.33,


>     kaizen v1.14→v1.29.


> (4) [SOFT] **Operation table expanded** — added Admin elevation, sc, taskkill rows.


> (5) [DESIGN] **ELEVATE-MISSING anti-pattern row** now links to new S-1.0.8 section.


> Cross-reference: kaizen v1.31, session VBvCOsXhzlQJUubBqtdFz.








> **v3.11 UPDATE (2026-08-04, kaizen — WIN-LONGPATH-1):**


> Red-team: direct parent-agent audit of session CGS_BRT26CX64OuSP1xJg infrastructure audit.


> HARD: 1. SOFT: 1. DESIGN: 0.


> Changes:


> (1) [HARD] **EXEC-TOOL-QUOTE-1 anti-pattern**: exec tool wraps absolute paths in quotes


>     and prepends workspace path, producing paths like


>     `C:\Users\...\workspaces\"C:\Users\LENOVO\npm-global"`.


>     This breaks `npm config set`, `npm install`, `node <path>`, and any command using


>     absolute paths. Fix: use `write`→`exec python <file>` pattern (S1.0 decision tree),


>     write `.npmrc` directly via Python, or use `.cmd` shim paths instead of `node`.


> (2) [SOFT] **npm-CONFIG-QUOTE-1**: `npm config set prefix "C:\path"` stores quotes


>     literally in `.npmrc` (e.g., `prefix="C:\Users\LENOVO\npm-global"`), breaking


>     all subsequent npm operations. Fix: write `.npmrc` directly via Python `open().write()`


>     or use Win32 registry PATH persistence instead of npm config.


> Cross-reference: cloudflare v3.33, kaizen v1.29, session CGS_BRT26CX64OuSP1xJg.





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


| **WIN-TRUSTEDINSTALLER-REG-1: Some Windows 11 registry keys are TrustedInstaller-protected, not just admin-protected (2026-08-05)** | Even ShellExecute "runas" admin elevation cannot write to keys owned by TrustedInstaller (e.g., `HKLM\SOFTWARE\Policies\Microsoft\Dsh`, `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Feeds`). Use the MDM/PolicyManager alternative path (e.g., `HKLM\SOFTWARE\Microsoft\PolicyManager\default\NewsAndInterests\AllowNewsAndInterests` = 0) or the Settings GUI. When the Settings GUI path is needed, DeepChat's Computer Use (CUA) tools (`list_apps` → `launch_app` → `get_window_state` → `click`/`type_text`) can drive the Settings app programmatically — load the `computer-use` skill for the full CUA protocol. Do NOT waste tool calls on icacls/takeown — TrustedInstaller outranks Admin. Canonical case: session VBvCOsXhzlQJUubBqtdFz — 20+ elevation attempts on Dsh/Feeds all failed; PolicyManager path succeeded on first try. See §S-1.0.8. |


| **ELEVATE-MISSING: Not using `elevate.exe` for admin operations** (v3.5) | `elevate.exe` ships with DeepChat at `C:\Program Files\DeepChat\resources\elevate.exe`. Use `elevate.exe -wait cmd.exe /c "..."` for operations requiring admin privileges. Requires UAC confirmation. See also ShellExecute "runas" pattern in §S-1.0.8. |


| **ASAR-PATCH-FRAGILE: Patching `app.asar` to fix exec quoting** (v3.5) | Do NOT patch `app.asar` in Program Files. Every DeepChat update overwrites it. Use the 3 sustainable strategies above instead. The correct fix (`windowsVerbatimArguments: true`) belongs in upstream source. |


| **ELEVATE-MISSING: Not using `elevate.exe` for admin operations**


| **EXEC-TOOL-QUOTE-1: exec wraps absolute paths in quotes, breaking npm/node commands (2026-08-04)** | The exec tool prepends workspace paths to absolute paths wrapped in quotes (e.g.,


  `C:\Users\...\workspaces\"C:\Users\LENOVO\npm-global"`). This breaks npm config set,


  npm install, `node <abs-path>`, and any command with absolute path arguments. Fix:


  use write->exec-python pattern (S1.0 decision tree), write .npmrc via Python open().write(),


  or use .cmd shim paths (C:\Users\LENOVO\npm-global\wrangler.cmd). Case: this session


  — 5+ failures across npm config, npm install, node module resolution. |


| **npm-CONFIG-QUOTE-1: npm stores quoted paths literally in .npmrc (2026-08-04)** | `npm config set prefix "C:\path"` stores `prefix="C:\path"` in .npmrc with literal


  quotes. npm then tries to mkdir the quoted path, creating directories like


  `workspaces\"C:\Users\LENOVO\npm-global"`. Fix: write .npmrc directly via


  Python `open().write()` — this bypasses npm's quote-stripping logic. Also use


  Win32 registry (`winreg`) for PATH persistence instead of `setx`. | (v3.5) | `elevate.exe` ships with DeepChat at `C:\Program Files\DeepChat\resources\elevate.exe`. Use `elevate.exe -wait cmd.exe /c "..."` for operations requiring admin privileges. Requires UAC confirmation. |


| **GIT-COMMIT-M-QUOTE-1: `git commit -m "msg with special chars"` fails on cmd.exe (2026-08-04)** | Any message containing em-dashes, parens, quotes, or multiple words → Node.js spawn() re-quotes, cmd.exe strips quotes, git sees fragmented args ("pathspec 'add' did not match", "pathspec '→' did not match"). ALWAYS: (1) `write` tool creates `%TEMP%\commit-msg.txt`; (2) `git commit -F %TEMP%\commit-msg.txt`. Same for `git tag -a -F`. Verified: 4 failures in session 1tz85-vMiqh2TyFySznBA before the -F pattern worked every time. Cross-ref: git-github SAME-TURN-COMMIT. |


| **EXEC-TOOL-QUOTE-1-PY: exec wraps `python <abs-path>.py` in quotes too (2026-08-04)** | When exec prepends the workspace path and quotes the python file path, python reports: `can't open file 'C:\...\workspaces\"C:\...\_task.py"'`. Fix: `cd` into the target dir first then `exec python _task.py` (bare relative path, no quotes). `python -c "..."` with nested quotes ALWAYS fails ("X was unexpected at this time") — S0.0 rule 2 (ABORT). Verified: 5 failures in session 1tz85-vMiqh2TyFySznBA. Cross-ref: S0.0, EXEC-TOOL-QUOTE-1, research PYTHON-C-AMPERSAND-1. |


| **EXEC-AUTOBG-DEATH-1: Short exec commands auto-background and die — "Session bg_XXX is not running" (2026-08-05)** | Observed 10+ times in session 8APhB8pdpgihrWgDLpXIP: `exec` on short Python scripts returns "Error: Session bg_XXX is not running" with output lost (the script may have run; output is unrecoverable). `yieldMs` does not reliably prevent it. **Fix — write-file-read-back pattern (§S-1.0.9):** the script WRITES its output to a `.txt` file, `exec` runs it, then the agent `read`s the file back. Succeeded every time in the canonical session. Cross-ref: kaizen v1.47 EXEC-AUTOBG-DEATH-1, PYTHON-BUFFERING-1. |
| **GH-API-HANG-1: `gh api` hangs indefinitely in this environment (2026-08-05)** | `gh api` — especially with `--paginate` or long-running GETs — hangs with no output and must be killed (exec session never returns). Verified 3x in session 8APhB8pdpgihrWgDLpXIP. Fix: use token-based Python urllib: get token via `gh auth token` (or GITHUB_TOKEN env), then `urllib.request.Request(url, headers={'Authorization': f'token {tok}'})` — completes reliably. For pagination, parse `Link` headers or use `per_page=100` + loop. Canonical case: gh api user/starred --paginate hung; identical op via urllib starred 4 repos (JulianDelBel/Adelic, PerretB/ultrametric-fitting, mmasdeu/darmonpoints, agent0ai/agent-zero) instantly. |
| **EXEC-PATH-SPACE-FALSE-NEGATIVE-1: Broken-quoted exec probes on paths with spaces produce FALSE 'not installed' conclusions (2026-08-10)** | **HARD.** `where outlook`, `reg query App Paths`, and `dir "C:\Program Files"` ALL failed this session while Outlook WAS installed (ClickToRun Office16 at `C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE`). ClickToRun does NOT register App Paths or an `Outlook.Application` class. User had to correct the agent. **Fix:** for ANY path containing spaces use 8.3 short names (`dir C:\Progra~1\...`) or Python `os.listdir`; never conclude 'not installed' from `where`/App-Paths alone; verify against real install dirs (`dir /b C:\Progra~1` lists `Microsoft Office`). Cross-ref: S-1.0.4, EXEC-TOOL-QUOTE-1, VERIFY-DONT-ASSUME-1 (qnfo-core). |
| **CMD-ECHO-SUCCESS-MASK-1: `2>nul & echo SUCCESS` masks failures and fakes exit 0 (2026-08-10)** | **HARD.** `del a.py b.py 2>nul & echo CLEANED` returned exit 0 + 'CLEANED' while the files REMAINED (deletion failed silently). Same class as GH-API-STDIN-NOOP-1 / PHANTOM-CLAIM-2 at the shell level. **Fix:** use `&&` (short-circuits on failure) or verify with `dir` afterward; NEVER chain `2>nul & echo <SUCCESS>` — the `&` always runs the echo regardless. Canonical case: session FqszmI7iAvYDr6_X3C2qv — 4 temp scripts falsely reported cleaned; red-team caught it. |
| **WSH-OUTLOOK-COM-MEM-1: cscript/WSH fails with 'Not enough memory resources' — use pywin32 for Outlook COM (2026-08-10)** | **HARD.** `cscript //nologo` fails on this host even for trivial `WScript.Echo` ("Execution of the Windows Script Host failed. Not enough memory resources"). **Fix:** use Python `win32com.client` (pywin32, verified available py3.12.10) — `Dispatch("Outlook.Application")` + `GetNamespace("MAPI")` + `GetDefaultFolder(9)` for calendar automation. Verified 2026-08-10: 7 appointments created + read-back verified. Outlook binary: `C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE`. |
| **CUA-DRIVER-QUARANTINE-1: computer-use plugin 'cua-driver' quarantined after unclean exit — list_apps dies (2026-08-10)** | **SOFT.** When the cua-driver plugin runtime is quarantined, `list_apps` fails with 'use Retry runtime to authorize one controlled attempt' (5 failures this session). **Fix:** fall back to COM automation (pywin32) or filesystem/registry probes; the user must click 'Retry runtime' in DeepChat to re-enable GUI automation. Cross-ref: computer-use skill, WSH-OUTLOOK-COM-MEM-1. |


| **PANDOC-FONT-QUOTE-1: pandoc `-V mainfont="Font Name With Spaces"` fails on Windows cmd.exe (2026-08-04)** | `pandoc paper.md -o out.pdf --pdf-engine=xelatex -V mainfont="DejaVu Serif"` fails with `pandoc: Serif": withBinaryFile: invalid argument` — cmd.exe or pandoc's argument parser splits on the space in the quoted font name. **Fix: (A) omit -V mainfont and let XeLaTeX use defaults (works on all platforms); (B) use a font without spaces (e.g., `-V mainfont=DejaVuSans`); (C) if the font name MUST have spaces, use `-V mainfont:"DejaVu Serif"` through a Python subprocess bypassing exec quoting.** Canonical case: session ZDdTu9QfTZKY_kJALlXY_ — pandoc failed on font arg, succeeded with defaults (37-page PDF built). Cross-ref: S-1.0.4 CMD.exe space-splitting bug, §PDF building in S1.1 operation table. |





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


0. **SINGLE-BATCH-SEQUENTIAL-1 (HARD GATE):** NEVER dispatch `write` and `exec` that reads that file in the SAME parallel tool batch — the exec can fire before the write completes (FileNotFoundError). Sequence: write in batch N, exec in batch N+1. Canonical case: session nRNLsnj-ytLg_xHL768uG — 10+ exec failures.

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


| Admin elevation | `ctypes.windll.shell32.ShellExecuteW(None, "runas", ...)` — see §S-1.0.8 |
| GUI automation | DeepChat CUA tools: `list_apps` → `launch_app` → `get_window_state` → `click`/`type_text`/`hotkey`. Use for Settings GUI, app dialogs, browser UI. Load `computer-use` skill. |


| Service control | `subprocess.run(['sc', 'stop', 'ServiceName'])` — also config/start/query |


| Process kill | `subprocess.run(['taskkill', '/F', '/IM', 'proc.exe'])` |


| Registry admin | `subprocess.run(['reg', 'add', ...])` but HKLM needs UAC elevation first |





## S-1.0.7 EXEC-TOOL-QUOTE-1 -- PATH QUOTING MANGLES npm/node COMMANDS (v3.9, 2026-08-04)





**The exec tool wraps absolute paths in quotes and prepends the workspace directory path,


producing paths like C:\Users\LENOVO\AppData\Local\Temp\deepchat-agent\workspaces


\"C:\Users\LENOVO\npm-global". This breaks npm, node, and any command using


absolute path arguments.**





### Affected Commands





| Command | Failure | Root Cause | Fix |


|:--------|:--------|:-----------|:----|


| npm config set prefix "C:\path" | Quotes stored literally in .npmrc | Exec wraps path in quotes, npm stores them | Write .npmrc via Python open().write() |


| npm install -g wrangler | ENOENT: no such file or directory | npm reads quoted prefix from .npmrc | Fix .npmrc first, then install |


| node "C:\path\to\script.js" | MODULE_NOT_FOUND | Exec prepends workspace path to quoted abs path | Use .cmd shim or Python subprocess |


| setx Path "%Path%;C:\path" | Invalid syntax | Exec rewrites %Path% with quotes | Use Python winreg directly |





### Permanent Workaround (write-then-exec pattern)





The ONLY reliable pattern is to write Python code to a temp file, then exec it:


1. write tool -> C:\Users\LENOVO\AppData\Local\Temp\_task.py


2. exec python C:\Users\LENOVO\AppData\Local\Temp\_task.py


3. exec cmd /c "del C:\Users\LENOVO\AppData\Local\Temp\_task.py"





This is why S0.0 rule 2 bans python -c -- the exec tool cannot safely pass


multi-line or quoted Python through cmd.exe. The write-then-exec pattern is NOT


a workaround; it is the ONLY canonical execution path on this system.





### npm-Specific Fix





Write .npmrc directly via Python -- never use npm config set for paths:





    open(r"C:\Users\LENOVO\.npmrc", "w").write(


        "prefix=C:\\Users\\LENOVO\\npm-global\n"


        "cache=C:\\Users\\LENOVO\\AppData\\Local\\npm-cache\n"


    )





For PATH persistence, use winreg instead of setx.





### Cross-Reference


- cloudflare skill v3.27: WRANGLER-PATH-REGRESSION-1 (wrangler PATH reverts)


- kaizen skill v1.17: BLAME-EXTERNAL-1 (assume your code is wrong first)


- DeepChat upstream: backgroundExecSessionManager.ts needs windowsVerbatimArguments: true





| **CURL-AUTH-QUOTE-1: Quoted curl args mangled by exec — auth headers dropped (2026-08-10)** | `-H "Authorization: Bearer %VAR%"` → header lost (CF 1001, GH 401); `-H Authorization:Bearer%VAR%` → 6111 no-space. Use `--oauth2-bearer %VAR%` + `-H Name:value` (no spaces) + `--data-binary @file` + `> out.txt`. See §S-1.0.10. Canonical case: session bPhAUCI_FRVeZyA5Rxmsm (3 failed auth attempts → 1 working pattern). |

## S-1.0.9 WRITE-FILE-READ-BACK PATTERN — EXEC-AUTOBG-DEATH-1 WORKAROUND (v3.15, 2026-08-05)

When `exec` on a short command auto-backgrounds and dies ("Session bg_XXX is not
running"), the output is lost. The reliable workaround:

```
1. write tool  -> C:\Users\LENOVO\.deepchat\_result.py
   (script prints results AND writes them to _result.txt)
2. exec python C:\Users\LENOVO\.deepchat\_result.py
   (may report session-death — IGNORE the error)
3. read tool   -> C:\Users\LENOVO\.deepchat\_result.txt
   (the output is there regardless of exec session status)
```

The script MUST write the output to a file inside the write — never rely on
stdout when exec sessions are dying. Cross-ref: kaizen v1.47 EXEC-AUTOBG-DEATH-1,
PYTHON-BUFFERING-1.

## S-1.0.10 EXEC-SAFE AUTHENTICATED CURL PATTERN (v3.19, 2026-08-10)

Through the DeepChat exec tool (cmd.exe + Node spawn), ANY argument containing double quotes is mangled
(opening quote stripped, closing quote glued to the last token). This breaks authenticated curl calls.

**Canonical exec-safe forms (all unquoted):**

```
# AUTH — use --oauth2-bearer (curl builds 'Authorization: Bearer <token>' with the space)
curl.exe -s --oauth2-bearer %CLOUDFLARE_API_TOKEN% https://api.cloudflare.com/client/v4/accounts/{acct}/d1/database > out.json

# HEADERS without spaces in the value — no quotes needed
-H Content-Type:application/json

# JSON BODY — write payload file first (write tool), then:
--data-binary @C:\path\payload.json

# OUTPUT — cmd redirect (never -o with an absolute path; it gets path-mangled)
> C:\path\out.json

# GitHub / Zenodo work identically
curl.exe -s --oauth2-bearer %GITHUB_TOKEN% https://api.github.com/user > out.json
```

**Do NOT use:** `-H "Authorization: Bearer %VAR%"` (→ 1001 Missing Authorization / 401),
`-H Authorization:Bearer%VAR%` (→ 6111 invalid format — no space), `-o C:\abs\path` (path-mangled ENOENT),
quoted URLs with query strings (exit 3 URL malformed).

Verified live 2026-08-10: Cloudflare account D1 list, GitHub /user, Zenodo deposit API, D1 REST read+write —
all via the unquoted pattern above. Cross-ref: CURL-AUTH-QUOTE-1, cloudflare v3.37 D1-REST-PAYLOAD-1,
S-1.0.4, S-1.0.7.

## Version





Current: **v3.19** (windows-command-patterns — CUA tools integration: Computer Use as GUI automation path; GUI automation row in Operation table; 2026-08-06)