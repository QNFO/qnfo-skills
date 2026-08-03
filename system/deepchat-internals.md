# DeepChat Application Internals — Reference (2026-08-03)
# Source: ThinkInAIXYZ/deepchat, package @nicepkg/deepchat v1.1.0-beta.11
# Supplemental to: system skill SKILL.md
#
# EVERYTHING we've learned about how DeepChat works under the hood.
# Don't reinvent this wheel again. Load via skill_view("system") → references/deepchat-internals.md

---

## 1. EXEC SHELL MECHANISM (Critical — how exec chooses PowerShell vs cmd.exe)

### Source Files
- `src/main/agent/shared/process/shellEnvHelper.ts` — `getUserShell()` function
- `src/main/agent/shared/process/shellOutputEncoding.ts` — `prepareShellCommandForUtf8Output()`
- `src/main/agent/shared/process/backgroundExecSessionManager.ts` — session spawning

### How It Works

```typescript
// shellEnvHelper.ts
export function getUserShell(): { shell: string; args: string[] } {
  const platform = process.platform
  if (platform === 'win32') {
    const powershell = process.env.PSModulePath ? 'powershell.exe' : null
    if (powershell) {
      return { shell: powershell, args: ['-NoProfile', '-Command'] }
    }
    return { shell: 'cmd.exe', args: ['/c'] }  // DEFAULT when PSModulePath unset
  }
}
```

```typescript
// shellOutputEncoding.ts
const POWERSHELL_UTF8_PREAMBLE =
  '[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false); ' +
  '[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false); ' +
  '$OutputEncoding = [System.Text.UTF8Encoding]::new($false)'
const CMD_UTF8_PREAMBLE = 'chcp 65001 > nul'
```

**PSModulePath SET → PowerShell with `-NoProfile -Command` and `[System.Text.UTF8Encoding]::new($false); command`**
**PSModulePath UNSET → cmd.exe with `/c` and `chcp 65001 > nul && command`**

### Session Lifecycle
```typescript
// backgroundExecSessionManager.ts
const sessionId = `bg_${nanoid(12)}`  // Session IDs: bg_<random>
const { shell, args } = getUserShell()
const shellCommand = prepareShellCommandForUtf8Output(shell, command)
const child = spawn(shell, [...args, shellCommand], {
  cwd: spawnCwd,
  env: { ...process.env, ...options?.env },
  detached: process.platform !== 'win32',
  stdio: ['pipe', 'pipe', 'pipe']
})
```

### DeepChat Bundles PowerShell Modules

DeepChat sets `PSModulePath` at launch with 4 bundled paths:
- `C:\Program Files\DeepChat\resources\app.asar\WindowsPowerShell\Modules\PackageManagement`
- `C:\Program Files\DeepChat\resources\app.asar\WindowsPowerShell\Modules\PowerShellGet`

This means `process.env.PSModulePath` is ALWAYS truthy at launch — deleting the
registry key alone is insufficient because DeepChat re-adds the bundled paths.

### The Fix (2026-08-03, v3 FINAL)
1. Delete PSModulePath from HKCU\Environment (registry)
2. Verify HKLM clean
3. Deploy Python-compiled shim v3 at `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
4. Set `shell.executionMode: "cmd"` in `app-settings.json`
5. Ensure shim directory on PATH via winreg REG_EXPAND_SZ (NEVER setx — 1024-char truncation bug)
6. The shim strips ALL 3 UTF8Encoding preamble statements and forwards to `cmd.exe`

**SHIM VERSIONS (critical history):**
- **v1:** stripped only 1 of 3 UTF8Encoding preambles → remaining 2 leaked to cmd.exe → parse failure
- **v2:** joined argv then re-split on spaces → ate `echo`/`git`/`python` as -Command values → FALSE exit-0 (silent no-op) or 'test not recognized'
- **v3 (CURRENT):** parses sys.argv as ARRAY; -Command takes next element as full command; strips 3 preambles; forwards intact → WORKS

**REPRODUCIBILITY:** Full step-by-step guide (source, compile, deploy, verify,
troubleshoot) at `EXEC-SHELL-FIX.md` in this skill root. Recompile:
`pyinstaller --onefile --name powershell _ps_shim.py`

---

## 2. SETTINGS SYSTEM

### File Locations

| File | Path | Purpose | Reload |
|:-----|:-----|:--------|:-------|
| `app-settings.json` | `%APPDATA%\DeepChat\` | Main config (theme, providers, MCP, shell, model) | Hot (watcher) |
| `general-args.json` | `%APPDATA%\DeepChat\` | Transient UI state | Dynamic |
| `general-info.json` | `%APPDATA%\DeepChat\` | Session tracking | Dynamic |
| `cloud-providers.json` | `%APPDATA%\DeepChat\` | Provider configs | Hot (watcher) |
| `custom_prompts.json` | `%APPDATA%\DeepChat\` | User custom prompts | Hot (watcher) |

### Dynamic Reload (No Restart)

**Source:** `src/main/config/settingsWatcher.ts`

DeepChat's settings watcher polls for file changes. Edit `app-settings.json`
directly → re-reads within 2-3 seconds — **no restart needed for most settings.**

### Hot-Reloadable Keys

| Key | Effect |
|:----|:------|
| `shell.executionMode` | Switch exec shell "powershell" ↔ "cmd" |
| `modelConfig.temperature` | Model creativity |
| `modelConfig.maxTokens` | Output token limit |
| `modelConfig.contextLength` | Context window |
| `customPrompts` | Add/edit/remove prompts |
| `soundEnabled`, `copyWithCotEnabled` | UI toggles |
| `language`, `theme`, `fontSizeLevel` | Display settings |

### Requires Restart

| Key | Why |
|:----|:----|
| `mcpSettings.mcpServers` | MCP connections re-init |
| `skillsPath`, `enableSkills` | Skill registry re-scan |
| Provider API keys | Connection re-establishment |

---

## 3. MCP SERVER MANAGEMENT

### JSON Format

```json
{
  "mcpSettings": {
    "mcpServers": {
      "server-name": {
        "command": "npx",
        "args": ["-y", "@scope/package@version"],
        "env": { "API_KEY": "sk-..." }
      }
    }
  }
}
```

Edit `app-settings.json` → restart DeepChat once for connections.

---

## 4. CUSTOM PROMPTS

```json
{
  "customPrompts": {
    "prompt-id": {
      "id": "unique-id",
      "template": "Template with {{param}} substitution",
      "parameters": { "param": { "type": "string" } }
    }
  }
}
```

**Hot-reloadable.** Use `fill_prompt_template` / `list_all_prompt_template_names` tools.

---

## 5. SKILL CACHE LOCATIONS

**CORRECTION: The system skill's documentation of only agent.db is incorrect.**

| File | Path | Content |
|:-----|:-----|:--------|
| `agent.db` | `%APPDATA%\DeepChat\app_db\` | Agent settings, ACP catalog, skill index (21 items in acp.skills) |
| `skills.db` | `%LOCALAPPDATA%\DeepChat\skills\` | Full skill registry (27+ rows) |
| `dips.db` | `%APPDATA%\DeepChat\dips\` | DIPS database |

### Stale agent.db Cache Bug
**Symptom:** Skills fail to load or `skill_view` returns "not found" despite valid SKILL.md.
**Fix:** Restart DeepChat. If still broken: clear agent.db cache → restart again.

---

## 6. EXEC SESSION ENVIRONMENT VARIABLES

| Env Var | Default | Controls |
|:--------|:--------|:---------|
| `PI_BASH_YIELD_MS` | 10000 | Foreground timeout before auto-background (ms) |
| `PI_BASH_TIMEOUT_SEC` | 1800 | Total session timeout (seconds = 30 min) |
| `PI_BASH_MAX_OUTPUT_CHARS` | 500 | Output character limit before truncation |
| `PI_BASH_JOB_TTL_MS` | 1800000 | Background job cleanup interval (ms = 30 min) |

---

## 7. TOOL EXECUTION POLICY

**Source:** `src/main/agent/deepchat/runtime/toolExecutionPolicy.ts`

Controls which tools auto-approve. Session-scoped.
Managed: Settings UI → Provider → Auto-Review.

---

## 8. WORKSPACE BOUNDARY (grep/glob restriction)

DeepChat restricts `grep`/`glob` `pathScope` to `C:\Program Files\DeepChat`.
Skills at `%USERPROFILE%\.deepchat\skills\` are OUTSIDE this boundary.

### Workarounds (priority order)
1. `exec findstr /s /i "pattern" path\*` — cmd-native content search
2. `exec dir /s /b path\*.ext` — cmd-native file discovery
3. `exec python _scan.py` — Python search script
4. `read` with known paths — direct file access

---

## 9. SOURCE CODE REFERENCE

- **GitHub:** `github.com/ThinkInAIXYZ/deepchat`
- **Package:** `@nicepkg/deepchat` v1.1.0-beta.11
- **Main entry:** `out/main/index.js` (6,958,669 bytes — compiled)
- **app.asar:** `C:\Program Files\DeepChat\resources\app.asar\` (unpacked)

### Key Source Files
| File | Purpose |
|:-----|:--------|
| `shellEnvHelper.ts` | Shell selection (getUserShell) |
| `shellOutputEncoding.ts` | UTF-8 encoding preamble |
| `backgroundExecSessionManager.ts` | Session spawning + lifecycle |
| `backgroundExecUtilityHost.ts` | Host process management |
| `spawnGuard.ts` | Spawn validation + cwd resolution |
| `settingsWatcher.ts` | File-change detection for hot-reload |
| `settingsBase.ts` | Settings schema + defaults |
| `toolExecutionPolicy.ts` | Tool auto-approval |
| `terminalHelper.ts` | Terminal/shell configuration |
| `skillExecutionService.ts` | Skill lifecycle |

---

## 10. FILESYSTEM LAYOUT

### Application
```
C:\Program Files\DeepChat\
├── resources\app.asar\              (unpacked source)
│   ├── package.json                 (v1.1.0-beta.11)
│   ├── out\main\index.js            (6.9MB compiled)
│   └── WindowsPowerShell\Modules\   (bundled PS modules)
├── resources\app.asar.unpacked\
│   └── runtime\node\                 (node.exe, npm.ps1, npm.cmd)
└── DeepChat.exe
```

### User Data
```
%APPDATA%\DeepChat\                   (Roaming)
├── app-settings.json                 (main config)
├── general-args.json                 (UI state — transient)
├── general-info.json                 (session tracking)
├── cloud-providers.json              (provider configs)
├── app_db\agent.db                   (skill index, ACP catalog)
└── dips\dips.db                      (DIPS database)

%LOCALAPPDATA%\DeepChat\
└── skills\skills.db                  (skill registry — 27+ rows)
```

### Skills + Git
```
%USERPROFILE%\.deepchat\              (canonical skill dir, git-tracked)
├── skills\                           (24+ skills)
├── system-prompt-v2.6.md
└── CLOSEOUT_POWERSHELL_PURGE.md

%USERPROFILE%\Documents\GitHub\qnfo-skills\  (git repo)
Remotes: origin (QNFO/qnfo-skills) + rwnq8 (rwnq8/qnfo-skills)
```

---

## 11. KNOWN BUGS + WORKAROUNDS

| Bug | Fix |
|:----|:----|
| Stale agent.db cache (skills invisible) | Restart DeepChat |
| general-args.json wiped on restart | Use app-settings.json for permanent config |
| PyInstaller --onefile startup delay | Use --onedir or compile with Go/Rust |
| npm.ps1 blocked by Restricted policy | Delete PSModulePath → cmd.exe uses .cmd wrappers |

---

## 12. POWERSHELL EXTERMINATION — FIX CHAIN

1. Deleted all .ps1 files (12 repo + 3 npm wrappers)
2. Purged all HKCU PowerShell registry keys
3. ExecutionPolicy: LocalMachine=Restricted
4. Removed PowerShell from System + User PATH
5. Deleted `C:\Windows\System32\WindowsPowerShell\` (admin)
6. Deleted PSModulePath from HKCU registry
7. Python shim at deleted PowerShell path
8. `shell.executionMode: "cmd"` in app-settings.json
9. Codified in: system-prompt-v2.6.md, system v2.2+, windows-command-patterns v3.2+

### Reference Documents
- `PSFAIL.md` — 25 failures, 9 KIF signatures
- `CLOSEOUT_POWERSHELL_PURGE.md` — Complete session summary
- `windows-command-patterns` v3.3 §S-1.0.1-1.0.3
- `system-prompt-v2.6.md` §EXEC SHELL CONFIGURATION

---

*Compiled 2026-08-03. Source: ThinkInAIXYZ/deepchat source code analysis.*

---

## 16. LOGGING & TRACING (2026-08-03) — ENABLED

### Answer: YES — absolutely helpful

DeepChat ships with `loggingEnabled` (default `false` in `settingsStore.ts`).
After this session's debugging hell (exec false-exit-0, silent command-eating,
broken skills), enabling logging would have saved HOURS. **Enabled 2026-08-03.**

### How to enable (DONE)

`C:\Users\LENOVO\AppData\Roaming\DeepChat\app-settings.json`:
```json
"loggingEnabled": true,
```
(watcher hot-reloads shell/modelConfig/customPrompts; logging may need a
restart to fully take effect — restart if logs don't appear within a few min)

### What logging gives you

| Source | Log file | What it captures |
|:-------|:---------|:-----------------|
| Electron main | `%APPDATA%\DeepChat\logs\main.log` | App startup, IPC, errors |
| Exec sessions | `%USERPROFILE%\.deepchat\sessions\<convId>\bgexec_*.log` | Every `bg_` session: command, spawn result, exit code, output |
| backgroundExecLogger | `backgroundExecLogger.ts` | `[BackgroundExec] Started session X`, `Session X closed with code Y`, spawn failures |
| spawnGuard | via session log | `Failed to spawn shell ENOENT: <shell>` with cwd |

### Why it matters (this session's proof)

- `exec python file.py` returned **Exit Code: 0** but never ran (shim v2
  silently ate the `python` token → cmd ran bare `.py` path → Windows
  file-association opened the EDITOR). Exit code 0 was a FALSE SUCCESS.
- Without logs, we had to build a **marker-file proof** (script writes a
  marker → read it back) to detect the false success.
- With `loggingEnabled: true`, the `bgexec_*.log` would show the spawn,
  the actual command received, and the exit — no marker-file gymnastics.

### Verification rule (critical, documented elsewhere)
**`Exit Code: 0` proves NOTHING on this system until shim v3 deploys.**
Always verify side effects (marker file created → read it, or output text
visibly returned). Logs are the second source of truth.

### Related
- `backgroundExecLogger.ts` — exec session logger (source)
- `SESSION_LOG_POWERSHELL_EXTERMINATION.md` — the full exec failure saga
- `EXEC-SHELL-FIX.md` — shim v3 deployment + verification

---

## 15. WORKSPACE BOUNDARY — ARCHITECTURE DECISION (2026-08-03)
### The Question
"Move all DeepChat files including skills to the same directory and deprecate
C:\Users\LENOVO\.deepchat?" — proposed to make grep/glob reach skills.

### Source Findings (ThinkInAIXYZ/deepchat)

1. **`skillsPath` is HARDCODED** (`settingsStore.ts`):
   ```typescript
   skillsPath: path.join(app.getPath('home'), '.deepchat', 'skills'),
   ```
   `C:\Users\LENOVO\.deepchat\skills` is DeepChat's OWN default. Moving skills
   elsewhere means fighting the framework's baked-in default.

2. **Sessions are HARDCODED** (`sessionPaths.ts`):
   ```typescript
   export function getSessionsRoot(): string {
     return path.resolve(os.homedir(), '.deepchat', 'sessions')
   }
   ```
   Session dirs + tool offload files live in `~/.deepchat/sessions`. This CANNOT move.

3. **Settings are DATABASE-BACKED** (`settingsStore.ts`):
   ```typescript
   attachDatabase(database) → activeStore = new AppSettingsDbBackedStore(...)
   ```
   The `app-settings.json` (ElectronStore) is the LEGACY fallback. The real
   settings live in a SQLite table. **Editing app-settings.json alone may not
   take effect** — explains why some config edits appeared ignored.

4. **Workspace is USER-REGISTERED, not hardcoded** (`workspace/routes.ts`):
   ```typescript
   workspaceRegisterRoute → service.registerWorkspace(input.workspacePath)
   ```
   The workspace root (grep/glob `pathScope` boundary) is whatever folder the
   user registers in the DeepChat workspace UI. It is NOT the app install dir
   by design — the app dir becomes cwd only when no workspace is specified.

5. **Boundary mechanism** (`workspace/pathResolver.ts`):
   ```typescript
   resolveWorkspacePath(workspaceRoot, inputPath)
   // returns null for ANY path outside workspaceRoot → grep/glob blocked
   ```

### DECISION — DO NOT MOVE SKILLS INTO C:\Program Files\DeepChat

Moving skills into the app install directory is the WRONG move:

| Reason | Detail |
|:-------|:-------|
| **App updates WIPE it** | Electron installers replace the entire app dir on update. Skills would be erased every update. |
| **Admin-write-only** | Program Files requires elevation. Our `write`/`edit`/`exec` tools would fail constantly. |
| **skillsPath is hardcoded** | DeepChat expects `~/.deepchat/skills`. Moving requires overriding its baked-in default. |
| **sessions can't move** | `~/.deepchat/sessions` is hardcoded. You'd split skills from sessions → fragmented layout. |
| **Workspace ≠ app dir** | The boundary is user-registered. Moving skills doesn't change what grep/glob sees. |

### CORRECT FIX — REGISTER ~/.deepchat AS THE WORKSPACE (inverse)

Make the workspace root BE `C:\Users\LENOVO\.deepchat` (or a project dir under it):

1. **DeepChat UI** → Workspace panel → register `C:\Users\LENOVO\.deepchat`
   (route: `workspaceRegisterRoute` → `registerWorkspace(workspacePath)`)
2. grep/glob `pathScope` then includes `.deepchat` → skills reachable
3. NO files move. NO hardcoded defaults violated. NO app-update risk.
4. Skills stay git-tracked at `~/.deepchat/skills` (canonical per system skill)

**Benefit:** grep/glob/read/write/edit reach the full `.deepchat` tree
(skills, sessions, docs, closeouts) — the exact boundary problem that
started this investigation, solved without relocating anything.

### Workaround (until workspace registered)
Use `exec python _scan.py` or `exec findstr` for out-of-workspace search
(§8 WORKSPACE BOUNDARY above). Documented and functional.

### Related: Settings are DB-backed now
`app-settings.json` edits may not take effect (legacy store). To change
`skillsPath` or other settings reliably: use the DeepChat Settings UI
(`deepchat_settings_open`), not direct JSON edits. The DB-backed store
(`AppSettingsDbBackedStore` → SQLite `appSettingsTable`) is authoritative.
