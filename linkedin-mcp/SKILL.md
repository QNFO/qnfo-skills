---
name: linkedin-mcp
description: LinkedIn MCP integration management — linkedin-mcp-tools v2.0.3 via DeepChat. Covers auth (persistent browser profile, NOT cookies), the 22 tools (profiles, people/job/company search, feed, messaging, network, connections, posts), credential storage redundancy, live verification (--status/--spike), and safety caps. Use when operating LinkedIn through DeepChat, re-authenticating the LinkedIn session, or troubleshooting LinkedIn MCP tools.
version: "1.0"
---

# LinkedIn MCP — Operations Guide (v1.0)

Manage the LinkedIn MCP integration inside DeepChat: `linkedin-mcp-tools`
v2.0.3 (devag7) — a stealth-browser (patchright) MCP server exposing 22 tools.

---

## Auth Model (CRITICAL — v2.0.3)

**The ONLY working auth is a persistent browser profile.** Email/password env
vars are accepted by the schema but do NOT drive login; `LINKEDIN_COOKIE` is
**schema-only and inert** (verified in dist/index.js — zero `addCookies` /
`cookieSet` calls). Do not paste li_at cookies expecting them to work.

| Component | Value |
|:----------|:------|
| Profile dir | `%USERPROFILE%\.linkedin-mcp\profile` (env: `LINKEDIN_PROFILE_DIR`) |
| Chrome | `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe` |
| Auth flow | `linkedin-mcp --login` OR `linkedin-auto-login.js` (automated) |
| Session check | `linkedin-mcp --status` → "Session: ✅ logged in" |
| Live probe | `linkedin-mcp --spike` → all endpoints return 200 |

**Session persistence:** the profile holds cookies + localStorage + Cloudflare
clearance. Sessions last days–weeks; re-run login when `--status` reports logged
out.

### Automated login script

`C:\Users\LENOVO\.deepchat\scripts\linkedin-auto-login.js` — pre-fills
credentials and submits automatically (user only intervenes for CAPTCHA/2FA).
Uses `autocomplete` attribute selectors because LinkedIn randomizes element IDs
(verified 2026-07-31: `#username` absent; `input[autocomplete="username"]`
present). Launch as a DETACHED process (see windows-command-patterns S1.6) —
the 4-minute poll loop dies if started via plain exec.

```python
import subprocess, os

log_file = os.path.join(os.environ["TEMP"], "linkedin-auto-login.log")
pid_file = os.path.join(os.environ["TEMP"], "linkedin-auto-login.pid")

# Remove old artifacts
for f in [log_file, pid_file]:
    try:
        os.remove(f)
    except FileNotFoundError:
        pass

# Launch detached (survives exec session)
with open(log_file, "w") as lf:
    proc = subprocess.Popen(
        ["node.exe", r"C:\Users\LENOVO\.deepchat\scripts\linkedin-auto-login.js"],
        stdout=lf,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        env={
            **os.environ,
            "LINKEDIN_EMAIL": "rowan.quni@outlook.com",
            "LINKEDIN_PASSWORD": "REDACTED_READ_FROM_STORE",
        },
    )

with open(pid_file, "w") as pf:
    pf.write(str(proc.pid))

print(f"Launched PID {proc.pid}, log: {log_file}")
```

**Signals:** Chrome window title `login page → "Feed | LinkedIn"` = success;
log line `SUCCESS — li_at cookie present` = session persisted. Challenge text
("captcha|verify|checkpoint") = human must solve in the open window.

---

## The 22 Tools

### Read (17)
- `whoami` — server version, login status, tool count
- `health_check` — cookie state + LIVE Voyager probe + safety-budget headroom
- `close_session` — close browser, kill Chrome
- `get_my_profile` / `get_profile(username)` — own or any profile
- `get_feed(count)` / `get_notifications(count)` — home feed / notifications
- `search_people(keywords, count)` / `search_jobs(keywords, count)` /
  `search_companies(keywords, count)` — discovery
- `get_inbox` / `get_conversation(conversation_urn)` — messaging
- `get_job_details(job_id)` — full job posting
- `get_company(universal_name)` / `get_company_posts(...)` /
  `get_company_employees(universal_name, count)` — company + prospecting
- `get_pending_invitations(direction, count)` — inbound/outbound requests

### Write — ALL gated with `confirm: true` (safety layer)
- `connect_with_person(profile_id, message, confirm)` — connection request
  (300-char note; daily cap 5)
- `send_message(recipient_urn | thread_id, message, confirm)` — new/reply
- `create_post(text, visibility, confirm)` — PUBLIC or CONNECTIONS (3000 chars)
- `react_to_post(post_urn, reaction, confirm)` — LIKE/PRAISE/EMPATHY/INTEREST/
  APPRECIATION/ENTERTAINMENT
- `comment_on_post(post_urn, text, confirm)` — up to 1250 chars

**URN notes:** posts use the ACTIVITY urn (`urn:li:activity:...`), NOT the
share urn. Profiles use the `ACoAA...` fsd_profile id (from search results).

---

## Safety Caps (from health_check budget)

| Action | Daily cap |
|:-------|:----------|
| connections | 5 |
| messages | 0 (cap 0 = blocked in v2.0.3 — verify) |
| likes | 50 |
| comments | 50 |
| follows | 30 |
| endorsements | 20 |
| event-invites | 20 |
| profile-views | 10 |
| searches | 30 |

`LINKEDIN_PACING_DISABLED` exists for testing but raises ban risk — leave off.

---

## Credential Redundancy (never re-ask the user)

| # | Location |
|:--|:---------|
| 1 | `%APPDATA%\DeepChat\mcp-settings.json` → `mcpServers.LinkedIn.env` |
| 2 | `%USERPROFILE%\.linkedin.env` |
| 3 | `%USERPROFILE%\.deepchat\linkedin-credentials.json` |
| 4–5 | `%APPDATA%\DeepChat\sync\backups\deepchat-settings-backup-2026-07-21\|07-13\mcp-settings.json` |
| 6–7 | same backups → `linkedin-credentials.json` |
| 8 | `%APPDATA%\DeepChat\sync\backups\linkedin-redteam-verified-2026-07-31\` |
| 🧠 | Memory pointer `mem-qkw8yJIYmR-a` |

The user must NEVER be asked to re-provide LinkedIn credentials — read from
these stores.

---

## MCP Config (mcp-settings.json)

```json
"LinkedIn": {
  "enabled": true,
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "linkedin-mcp-tools@latest"],
  "env": {
    "LINKEDIN_EMAIL": "...",
    "LINKEDIN_PASSWORD": "...",
    "LINKEDIN_COOKIE": "...",
    "LINKEDIN_PROFILE_DIR": "C:\\Users\\LENOVO\\.linkedin-mcp\\profile"
  }
}
```

**First-start gotcha:** the first `npx` invocation downloads Playwright Chromium
(~412 MB) which exceeds DeepChat's MCP init timeout → server silently fails.
Fix: pre-install once with `npx playwright install chromium` (or the package's
own patchright install) and verify `chrome.exe` exists under
`%LOCALAPPDATA%\ms-playwright\chromium-*\chrome-win64\`.

**Browser boot race:** `whoami` called immediately after MCP initialize can
report `loggedIn: false` because the profile cookie DB takes ~20s to load.
`--status` and `--spike` do `ensureContext()` first and report correctly. Give
the server a boot window before trusting whoami.

---

## Verification Sequence

```bash
# 1. Session state
cmd /c "npx -y linkedin-mcp-tools@latest --status"   # expect "✅ logged in"

# 2. Live data path (all endpoints 200, profile publicIdentifier returned)
cmd /c "npx -y linkedin-mcp-tools@latest --spike"

# 3. MCP protocol (tools available + whoami)
# via DeepChat tools once the server connects
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|:--------|:------|:----|
| Tools never appear in DeepChat | Chromium not pre-installed; MCP init timeout | `npx playwright install chromium`; restart DeepChat |
| `loggedIn: false` via whoami | Browser boot race (instant call) | Wait ~20s; use `--status`/`--spike` to verify |
| `--status` says logged out | Session expired | Re-run auto-login (detached) |
| `CLOUDFLARE_BLOCKED` error | LinkedIn challenge | Re-run `--login` headful on clean IP |
| `AUTH_REQUIRED` error | Not logged in | Run `--login` |
| `quota_exhausted` on connect | Daily cap hit | Wait for next day |
| messages cap = 0 | v2.0.3 messaging blocked | Check upstream release for fix |

---

## Anti-Patterns

| Anti-pattern | Correct |
|:-------------|:--------|
| Pasting `li_at` cookie expecting auth | `LINKEDIN_COOKIE` is inert in v2.0.3 — use profile login |
| Running auto-login via plain exec | Process gets reaped — use DETACHED pattern (S1.6) |
| Selecting LinkedIn fields by `#username` | IDs are randomized — use `autocomplete` attributes |
| Trusting instant `whoami` loggedIn | Browser boot race — use `--status`/`--spike` |
| Ignoring the 412 MB first-run download | Pre-install Chromium or the server silently fails to connect |

---

## DeepChat Runtime Context
- Skill root: `C:\Users\LENOVO\.deepchat\skills\linkedin-mcp`.
- Relative paths mentioned by this skill are relative to the skill root unless stated otherwise.
- No bundled scripts (referenced scripts live in `C:\Users\LENOVO\.deepchat\scripts\`).
- Credentials: never ask the user — read from the redundancy table above.
