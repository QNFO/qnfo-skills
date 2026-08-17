# MCP AUDIT + v3.41 RECONCILIATION — KAIZEN REPORT (2026-08-17)

Cycle: CMD SKILLS UPDATE (MCP audit continuation + red-team skills audit + prompt reconciliation).
Session: PI64gnaq9r_E5tiK2Dx_y. Mirrors: system-prompt v3.40→v3.41, cloudflare v3.55 (existing).

## HARD findings fixed this cycle

1. **MCP-REGISTRY-LIVE-1 (HARD — dual-store truth corrected)**: the LIVE MCP registry in
   this DeepChat build is `AppData\Roaming\DeepChat\app_db\agent.db → mcp_servers` (startup
   store). `mcp-settings.json` is a settings file that is NOT merged at startup — 15 Cloudflare
   OAuth servers configured there (2026-08-11) were PHANTOM entries: enabled in JSON, never
   loaded, absent from the live registry, hence "could not stay connected". Fix: inserted the
   8 needed Cloudflare servers directly into the live registry (enabled=true) + mirrored
   mcp-settings.json (32→14 servers). deepchat-settings SKILL.md dual-store lesson
   (MCP-REGISTRATION-ONE-STORE-1) now needs updating: writes MUST go to agent.db mcp_servers;
   JSON mirror optional.

2. **FLEET-TOKEN-STALL-1 (HARD — root cause CONFIRMED 2026-08-17)**: all 15 fleet tokens were
   4.4 days stale (401 invalid_token) on 2026-08-17; manual refresh succeeded 13/13 (server-side
   refresh_token grant). Root cause, two layers:
   (a) PHANTOM REGISTRATION (primary): the Cloudflare OAuth servers existed only in
       mcp-settings.json, never in the live registry (app_db agent.db mcp_servers) — they never
       CONNECTED, so mcp-remote never auto-refreshed their cache tokens (mcp-remote refreshes on
       connect/request). A registered server self-heals at every app start; a phantom cannot.
   (b) CRON NEVER FIRES (contributing): cron_job_runs shows ZERO runs ever for 216e1d12
       (Daily Ops) while 7 other jobs have run histories — the 03:00 UTC slot (= 05:00 Amsterdam)
       fires only when the DeepChat app is open; the app is closed overnight, so the daily
       refresh never ran.
   FIX (applied): live registration of the 8 needed servers = self-healing fleet at every app
   start (mcp-remote refresh-on-connect). Daily Ops cron remains as a warm-backup. Optional
   hardening: move fleet-oauth-refresh.py into a SessionStart lifecycle hook (deepchat-hooks).

3. **OBSERVABILITY-NO-TOKEN-1 (HARD — removed)**: `cloudflare-observability` was enabled in the
   live registry but had NO cached OAuth token (needs one-time interactive browser OAuth) —
   the exact reason it was "enabled but never running" and was disabled 3× on 2026-08-08.
   Removed per user mandate (cannot stay connected). Same for `cloudflare-radar`.

4. **BROWSER-RUN-404-1 (HARD — removed)**: `qnfo-browser-run` config pointed at
   https://qnfo-browser-run.q08.workers.dev/mcp which returns HTTP 404 — the Worker was never
   deployed. A config entry for a non-existent endpoint = dead dependency. Removed. (If the
   Worker is ever deployed, re-register from the live endpoint.)

5. **WRITE-TEXT-NEWLINE-1 application (HARD — kaizen v2.66 codified by concurrent session)**:
   the v3.40 dual-write left CRLF drift in markdown stores (masked by read_text-normalized
   sha checks). This cycle completed the interrupted v3.41 reconciliation: ALL 7 stores now
   byte-identical LF, verified by RAW-BYTE sha256 c46bd2963315775c. Rule: prompt-store writes
   MUST use binary writes (or newline='\n'); parity checks MUST compare raw bytes.

## Servers removed (18) — user mandate (unneeded OR cannot stay connected)

- No OAuth token: cloudflare-observability, cloudflare-radar
- Not needed for QNFO/Cloudflare: cloudflare-logpush, cloudflare-browser-mcp-server,
  dns-analytics, containers-mcp, cloudflare-casb-mcp-server, cloudflare-autorag-mcp-server,
  dex-analysis, github (plaintext PAT), LinkedIn (plaintext creds), buffer (plaintext Bearer),
  filesystem, sequential-thinking, qnfo-mcp-portal, qwav-platform (alias), mcd-mcp, nowledge-mem
- Endpoint 404: qnfo-browser-run

## Servers kept/registered (14 enabled)

cloudflare, cloudflare-docs, cloudflare-bindings, cloudflare-builds, cloudflare-ai-gateway,
cloudflare-graphql, cloudflare-auditlogs, cloudflare-blog, cloudflare-agents-docs,
qnfo-memory-mcp, arxiv-mcp-server, context7, + 2 in-memory built-ins.
Fleet health post-trim: 9/9 (6 OAuth probe 200 + 3 public). Post-restart: DB registry 14/14
enabled, ~13 mcp-remote node processes live, 8/8 inserted servers present.

## Skills updated (commit 1eba19d + this cycle)

cloudflare/SKILL.md (coverage 18→9, decision matrix, verification chains, KIF-48/49, tool
tables), fleet-mcp-health-check.py / fleet-oauth-refresh.py / fleet-oauth-bootstrap.py
(15→6 OAuth), code/SKILL.md, deepchat-settings/SKILL.md, execution-mandate/SKILL.md,
research/SKILL.md, windows-command-patterns/SKILL.md, knowledge/SKILL.md (AutoRAG removed),
social-media-management/SKILL.md (Buffer MCP removed), system-prompt-v2.7.md (v3.41).

## GIT-OWNERSHIP-1 compliance

Committed ONLY this cycle's files: skills/system-prompt-v2.7.md (v3.41), this report.
LEFT UNCOMMITTED (foreign concurrent-session dirt, absorbed by their next cycle):
email-composer/references/contact-ledger.md, email-composer/references/outreach-log.md,
kaizen/SKILL.md (their v2.66 banner), knowledge/scripts/philpapers_monitor_state.json,
research/scripts/indexnow-submit.py.

## Action items for next cycle

1. Investigate Daily Ops 03:00 UTC refresh stall (cron_job_runs for 216e1d12).
2. Update deepchat-settings SKILL.md MCP-REGISTRATION-ONE-STORE-1 → agent.db-authoritative.
3. mcd-mcp + nowledge-mem re-appeared in DB (disabled) after the trim — concurrent
   re-registration; keep disabled or remove once the concurrent session settles.
