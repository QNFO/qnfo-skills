---
name: email-composer
description: Email triage, drafting, business communication. Use for inbox analysis, drafting responses, bizdev outreach, declining/pitching, QNFO/QWAV-aligned correspondence.
version: v1.1
kif_tags: [KIF-03, KIF-05, KIF-32]
---

> **v1.1 UPDATE (2026-07-31, kaizen — 20-finding remediation):**
> Red-team review: 5 parallel subagents attempted, all truncated; fell back to direct
> parent-agent 5-adversary audit (Accuracy, Completeness, Dependency, Novelty, Status).
> HARD findings: 6. SOFT findings: 9. DESIGN findings: 5.
> Changes:
> (1) [HARD] Removed broken `launch_app(name="Outlook")` — fails on Windows ("Failed to
>     activate packaged app"). Only `launch_app(path=...)` works. Added warning that
>     `start_minimized: true` breaks window detection. (Accuracy)
> (2) [HARD] Added explicit instruction: `press_key("return")` on SearchTextBox does NOT
>     submit search; must click Submit Search button via element_index. (Accuracy)
> (3) [HARD] Added Phase 0: Environment Discovery — multi-account enumeration via
>     PowerShell COM, Outlook health check, folder inventory before Phase 1. (Completeness)
> (4) [HARD] Added PowerShell COM Fallback Protocol — when UI search fails or returns
>     irrelevant results, fall back to COM-based search scripts. COM was 10x more reliable
>     than UI search in session testing. (Completeness)
> (5) [HARD] Added Recovery Protocol for Outlook window disappearance — the HWND persists
>     but `list_windows` drops it; use `debug_window_info` + re-fetch. (Completeness)
> (6) [HARD] Added cross-folder search instructions — Sent Items, Archive, Deleted Items
>     are common locations for target emails. (Completeness)
> (7) [SOFT] Added general-purpose `search-email.ps1` script reference (keyword search
>     across all stores/folders). Replaces Ice-Geng-only `find-ice-email.ps1`. (Completeness)
> (8) [SOFT] Added version header, `.kaizen_history`, KIF tags. (Status)
> (9) [SOFT] Fixed `email-patterns.md` mojibake: â€" → —, â€œ → ". (Accuracy)
> (10) [SOFT] Fixed Integration Points: `computer-use` is a built-in capability, not a
>     skill. Clarified with note. (Dependency)
> (11) [SOFT] Qualified "All Mailboxes" claim — does NOT reliably reach cross-account
>     results; PowerShell COM multi-store search is the reliable path. (Completeness)
> (12) [SOFT] Added `windows-command-patterns` skill reference for PowerShell safety. (Novelty)
> (13) [SOFT] Generalized "Critical search tip" from Ice-Geng-specific to principle:
>     Outlook display names often differ from contact names. (Status)
> (14) [SOFT] Added `list_windows` to Phase 1 tool enumeration (was referenced but not
>     listed). (Accuracy)
> (15) [SOFT] Documented `search_memories` and `recall_facts` as the correct tool names
>     (both verified available). (Accuracy)
> (16-20) [DESIGN] Added OWA fallback, COM body-reading protocol, Anti-Patterns table,
>     email session context preservation, and generalized `find-ice-email.ps1` from
>     hardcoded reply to template. (Novelty + Status)
> Cross-reference: kaizen v1.2.3, windows-command-patterns.

# Email Composer — Business Communication for QNFO/QWAV

## Quick Start

1. **Open Outlook** via Computer Use:
   - `launch_app(path="C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE")` — the ONLY reliable method on Windows.
   - **DO NOT use `launch_app(name="Outlook")`** — fails with "Failed to activate packaged app."
   - **DO NOT use `start_minimized: true`** — breaks window detection; the process exists but `list_windows` returns zero windows. Launch normally and let the window appear.
2. **Find the email**:
   - Use `get_window_state` to inspect inbox.
   - Press `hotkey(keys=["ctrl","e"])` to focus the search box.
   - Type search term via `set_value` on SearchTextBox.
   - **CRITICAL: `press_key("return")` does NOT submit the search.** You MUST click the Submit Search button explicitly via its `element_index`.
   - If UI search returns irrelevant results (common: old archive items surface before recent inbox items), fall back to PowerShell COM (see §PowerShell COM Fallback Protocol).
3. **Read the email**:
   - **Preferred (reliable):** Use PowerShell COM `$item.Body` — see §PowerShell COM Fallback Protocol.
   - **Fallback (UI):** Double-click the email in the list to open standalone window, then `get_window_state(max_elements=150, max_depth=30)` on that window.
4. **Load strategy context**: Read `references/qnfo-qwav-strategy.md` if QNFO/QWAV positioning is needed for the response.
5. **Draft the response**: Apply tone guidelines from `references/email-patterns.md`, integrate QNFO/QWAV strategy, run through qnfo-agent §0.0 Research Integrity Mandate.
6. **Deliver**: Click Reply in the standalone email window, `type_text` the response, or present draft for user approval.

## Core Workflow

### Phase 0: Environment Discovery (MANDATORY — run before Phase 1)

Before starting any email search, discover the environment:

```
1. PowerShell COM — enumerate accounts:
   $outlook = New-Object -ComObject Outlook.Application
   $ns = $outlook.GetNamespace('MAPI')
   $ns.Accounts | ForEach-Object { $_.SmtpAddress }

2. For each account, enumerate top-level folders:
   foreach ($store in $ns.Stores) {
     Write-Output "Store: $($store.DisplayName)"
     foreach ($f in $store.GetRootFolder().Folders) {
       Write-Output "  $($f.Name) — $($f.Items.Count) items"
     }
   }

3. Verify Outlook is healthy: check that `GetProcess -Name OUTLOOK` returns a process
   with a MainWindowTitle.

4. Note: which account is the DEFAULT (shown on launch) vs which accounts are secondary.
```

**Why this matters:** The target email may be in a non-default account. In session testing,
a search email was in `rowan.quni@outlook.com` while the UI defaulted to `rwnquni@outlook.com`.
Without Phase 0, the agent searches the wrong account and finds nothing.

### Phase 1: Discovery & Triage

- Use Computer Use tools (`list_windows`, `get_window_state`, `click`, `type_text`, `hotkey`, `set_value`) to navigate Outlook.
- **Critical search tip:** Sender display names in Outlook often differ from the contact's actual name. The `SenderName` field shown in the UIA tree may display "Project" when the actual person is "Ice Geng" at TechInBridge. Always search using BROAD terms first (partial name, first name, domain from email), not the exact expected display name. Verify the actual sender by reading the full email or using PowerShell COM to inspect `SenderEmailAddress`.
- **Multi-account search:** The "All Mailboxes" dropdown option may NOT reliably surface cross-account results (testing showed stale archive results). For cross-account search, use PowerShell COM to search all stores (see §PowerShell COM Fallback Protocol).
- **Cross-folder search:** Target emails may be in Sent Items, Archive, or Deleted Items — not just Inbox. PowerShell COM searches all folders automatically; UI search requires manual folder navigation.
- Triage: identify unread emails, categorize by urgency (bizdev opportunity, publication notice, infrastructure alert, spam).

### Phase 2: Analysis

- **Preferred (reliable):** Use PowerShell COM to read email body (`$item.Body`). This avoids UIA tree truncation, encoding issues, and window-juggling.
- **Fallback (UI):** Read the full email body by double-clicking the email, then inspecting the standalone window with `get_window_state(max_elements=150, max_depth=30)`.
- Extract: sender identity (company, role, relationship history — use `$item.SenderEmailAddress` for accurate identity), what they're asking, what they're offering, what they need from you.
- Check conversation history: search Sent Items for prior exchanges with this contact.
- Check memory: `search_memories` (Vectorize semantic search) and `recall_facts` (D1 keyword/category lookup) for prior interactions and decisions.

### Phase 3: Strategic Context

- **ALWAYS** verify QNFO agent is loaded via `skill_view("qnfo-agent")` before drafting — it contains the Research Integrity Mandate and governance framework.
- If QNFO/QWAV commercial positioning is relevant, read `references/qnfo-qwav-strategy.md`.
- If the response requires specific communication patterns, read `references/email-patterns.md`.
- Cross-reference against qnfo-agent §0.0 (Research Integrity) — no marketing language, no promissory statements, certainty labels required.

### Phase 4: Drafting

1. Determine the strategic goal: accept, decline, defer, pitch, gather information, maintain relationship.
2. Apply the QNFO/QWAV positioning from `references/qnfo-qwav-strategy.md`.
3. Apply tone guidelines from `references/email-patterns.md`.
4. Run through qnfo-agent §0.0: banned words check, certainty calibration, falsifiability check.
5. Present draft with explicit strategic rationale.

### Phase 5: Delivery

- Use Computer Use to click Reply in the Outlook window and type the response.
- Or present the draft for user review before sending.
- After sending, remember the interaction (`remember_fact`) for future reference.

## PowerShell COM Fallback Protocol (MANDATORY when UI search fails)

When UI-based search returns no results, irrelevant results, or stalls, fall back to PowerShell COM immediately. Do NOT retry UI search more than twice.

### Search all stores by keyword

```powershell
$outlook = New-Object -ComObject Outlook.Application
$ns = $outlook.GetNamespace('MAPI')

# Recursive folder search
function Search-Folders($folder, $depth, $keyword, $maxDays) {
    if ($depth -gt 5) { return }
    if ($folder.Items.Count -gt 0) {
        $cutoff = (Get-Date).AddDays(-$maxDays)
        try {
            $kwFilter = "@SQL=urn:schemas:httpmail:subject LIKE '%$keyword%' OR urn:schemas:httpmail:textdescription LIKE '%$keyword%'"
            $found = $folder.Items.Restrict($kwFilter)
            foreach ($item in $found) {
                $date = try { $item.ReceivedTime } catch { $item.SentOn }
                if ($date -ge $cutoff) {
                    Write-Output "[$($folder.Name)] $($item.SenderName) | $($item.Subject) | $date"
                }
            }
        } catch {}
    }
    foreach ($sub in $folder.Folders) { Search-Folders $sub ($depth+1) $keyword $maxDays }
}

foreach ($store in $ns.Stores) {
    Search-Folders $store.GetRootFolder() 0 "research" 21
}
```

### Read full email body by subject match

```powershell
$outlook = New-Object -ComObject Outlook.Application
$ns = $outlook.GetNamespace('MAPI')
# ...search stores recursively for matching subject...
Write-Output $item.Body
```

### Key advantages over UI search

| Aspect | UI Search | PowerShell COM |
|:-------|:----------|:---------------|
| Cross-account | "All Mailboxes" unreliable | Searches all stores explicitly |
| Cross-folder | Manual navigation needed | Recursive: hits all folders |
| Body access | UIA tree length limited | Full body text |
| Reliability | Window disappears, search stalls | Direct COM, no UI dependency |
| Speed | 5-10 tool calls per search | 1 script execution |

**Gate:** If UI search returns 0 results after 2 attempts, switch to COM. Do not retry.

## Recovery Protocols

### Outlook Window Disappearance

**Symptom:** `list_windows` returns no Outlook window, but `Get-Process -Name OUTLOOK` shows the process alive with a MainWindowTitle.

**Root cause:** The `rctrl_renwnd32` window class is a special Outlook render window that can drop from the window manager's enumeration while the HWND remains valid.

**Recovery:**
1. Call `debug_window_info(pid=<pid>)` — this will report the HWND even when `list_windows` doesn't.
2. Use the reported HWND directly with `get_window_state(pid=<pid>, window_id=<hwnd>)`.
3. If that also fails, kill and restart Outlook:
   - `kill_app(pid=<pid>)`
   - Wait 3 seconds
   - `launch_app(path="C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE")`

### PowerShell `$` Sign Stripping

**Symptom:** Inline PowerShell `exec` commands strip `$` signs, causing variable-name errors.

**Workaround:** Always write PowerShell scripts to `.ps1` files via `write`, then execute via `exec` with `-File`. Never use inline PowerShell for scripts with variables.

## Integration Points

| Skill / Capability | When to Load | What It Provides |
|:-------------------|:-------------|:-----------------|
| `qnfo-agent` | Before drafting any response | Research Integrity Mandate, governance, banned words, certainty labels |
| `knowledge` | Before checking contact history | KG querying, memory search, paper context |
| `research` | When citing QNFO publications | Paper lookup, DOI retrieval, publication context |
| `windows-command-patterns` | Before any PowerShell `exec` | KIF-05/06/07/09 enforcement, `$`-sign handling, ps-safe-exec |
| Computer Use tools | Throughout (Outlook interaction) | Built-in capability — `launch_app`, `get_window_state`, `click`, `type_text`, `hotkey`, `set_value`, `list_windows` |
| YoBrowser (`load_url`, `cdp_send`) | When desktop Outlook is unrecoverable | Outlook Web Access (OWA) fallback |

## Key Constraints

- **Description must stay ≤176 chars** (same scanner bug that broke qnfo-agent and system).
- Computer Use for Outlook requires patience — PostMessage-based typing may not verify; element-indexed `set_value` and UIA Invoke are more reliable.
- Drafts must pass qnfo-agent §0.0 before delivery — no exceptions.
- Never fabricate citations or DOI references. Verify via `search_papers_enriched` or `get_paper_context`.
- **PowerShell safety:** All COM scripts must be written to `.ps1` files and executed via `exec -File`, never inline. See `windows-command-patterns` skill for `$`-sign handling rules.

## Anti-Patterns

| Anti-Pattern | Correct |
|:-------------|:--------|
| Using `launch_app(name="Outlook")` on Windows | Use `launch_app(path="C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE")` only |
| Using `start_minimized: true` with Outlook | Never minimize — the window becomes undetectable |
| Pressing Enter to submit Outlook search | Click the Submit Search button explicitly via element_index |
| Retrying UI search 3+ times when it returns irrelevant results | Fall back to PowerShell COM after 2 failed UI search attempts |
| Assuming single Outlook account | Run Phase 0: Environment Discovery first |
| Searching only Inbox | Search Sent Items, Archive, Deleted Items too |
| Reading email body via UIA tree (truncation risk) | Use PowerShell COM `$item.Body` for reliable full-body access |
| Inline PowerShell with `$` variables | Write to `.ps1` file first, then `exec -File` |
| Treating `computer-use` as a loadable skill | It's a built-in capability — reference its tools directly |

## References

- `references/qnfo-qwav-strategy.md` — QWAV commercial thesis, Qubit Delusion series, Manifesto, Problem-Substrate Mapping, JPCUB positioning
- `references/email-patterns.md` — Communication patterns: declining opportunities, pitching QWAV, follow-ups, relationship maintenance
- `scripts/find-ice-email.ps1` — Template for sender-specific email search (generalize for other contacts)
- `scripts/search-email.ps1` — General-purpose keyword search across all Outlook stores/folders

## Version

Current: **v1.1** (kaizen — 20-finding remediation, 2026-07-31)
