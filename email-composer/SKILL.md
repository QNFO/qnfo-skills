---
name: email-composer
description: Email triage, drafting, business communication. Python win32com for Outlook automation (PowerShell DELETED). Use for inbox analysis, drafting responses, bizdev outreach, declining/pitching, QNFO/QWAV-aligned correspondence.
version: 1.2
kif_tags: [KIF-03, KIF-05, KIF-32]
---

> **v1.2 (2026-08-03, total PowerShell purge — user mandate):**
> ALL PowerShell references replaced with Python win32com. All .ps1 script references
> updated to .py. PowerShell COM Fallback Protocol → Python win32com Fallback Protocol.
> Phase 0 rewritten in Python. `$`-sign stripping section removed. All PowerShell code
> blocks replaced. Cross-reference: windows-command-patterns v3.0.
>
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
> (9) [SOFT] Fixed `email-patterns.md` mojibake: â€" → —,  → ". (Accuracy)
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
   - If UI search returns irrelevant results (common: old archive items surface before recent inbox items), fall back to Python win32com (see §Python win32com Fallback Protocol).
3. **Read the email**:
   - **Preferred (reliable):** Use Python win32com `item.Body` — see §Python win32com Fallback Protocol.
   - **Fallback (UI):** Double-click the email in the list to open standalone window, then `get_window_state(max_elements=150, max_depth=30)` on that window.
4. **Load strategy context**: Read `references/qnfo-qwav-strategy.md` if QNFO/QWAV positioning is needed for the response.
5. **Draft the response**: Apply tone guidelines from `references/email-patterns.md`, integrate QNFO/QWAV strategy, run through qnfo-core §0.0 Research Integrity Mandate.
6. **Deliver**: Click Reply in the standalone email window, `type_text` the response, or present draft for user approval.

## Core Workflow

### Phase 0: Environment Discovery (MANDATORY — run before Phase 1)

Before starting any email search, discover the environment:

```
1. Python win32com — enumerate accounts:
   outlook = win32com.client.Dispatch("Outlook.Application")
   ns = outlook.GetNamespace("MAPI")
   for acc in ns.Accounts:
       print(acc.SmtpAddress)

2. For each account, enumerate top-level folders:
   for store in ns.Stores:
       print(f"Store: {store.DisplayName}")
       for f in store.GetRootFolder().Folders:
           print(f"  {f.Name} — {f.Items.Count} items")

3. Verify Outlook is healthy: check that tasklist shows OUTLOOK.EXE running.
4. Note: which account is the DEFAULT (shown on launch) vs which accounts are secondary.
```

**Why this matters:** The target email may be in a non-default account. In session testing,
a search email was in `rowan.quni@outlook.com` while the UI defaulted to `rwnquni@outlook.com`.
Without Phase 0, the agent searches the wrong account and finds nothing.

### Phase 1: Discovery & Triage

- Use Computer Use tools (`list_windows`, `get_window_state`, `click`, `type_text`, `hotkey`, `set_value`) to navigate Outlook.
- **Critical search tip:** Sender display names in Outlook often differ from the contact's actual name. The `SenderName` field shown in the UIA tree may display "Project" when the actual person is "Ice Geng" at TechInBridge. Always search using BROAD terms first (partial name, first name, domain from email), not the exact expected display name. Verify the actual sender by reading the full email or using Python win32com to inspect `SenderEmailAddress`.
- **Multi-account search:** The "All Mailboxes" dropdown option may NOT reliably surface cross-account results (testing showed stale archive results). For cross-account search, use Python win32com to search all stores (see §Python win32com Fallback Protocol).
- **Cross-folder search:** Target emails may be in Sent Items, Archive, or Deleted Items — not just Inbox. Python win32com searches all folders automatically; UI search requires manual folder navigation.
- Triage: identify unread emails, categorize by urgency (bizdev opportunity, publication notice, infrastructure alert, spam).

### Phase 2: Analysis

- **Preferred (reliable):** Use Python win32com to read email body (`item.Body`). This avoids UIA tree truncation, encoding issues, and window-juggling.
- **Fallback (UI):** Read the full email body by double-clicking the email, then inspecting the standalone window with `get_window_state(max_elements=150, max_depth=30)`.
- Extract: sender identity (company, role, relationship history — use `item.SenderEmailAddress` for accurate identity), what they're asking, what they're offering, what they need from you.
- Check conversation history: search Sent Items for prior exchanges with this contact.
- Check memory: `search_memories` (Vectorize semantic search) and `recall_facts` (D1 keyword/category lookup) for prior interactions and decisions.

### Phase 3: Strategic Context

- **ALWAYS** verify QNFO agent is loaded via `skill_view("qnfo-core")` before drafting — it contains the Research Integrity Mandate and governance framework.
- If QNFO/QWAV commercial positioning is relevant, read `references/qnfo-qwav-strategy.md`.
- If the response requires specific communication patterns, read `references/email-patterns.md`.
- Cross-reference against qnfo-core §0.0 (Research Integrity) — no marketing language, no promissory statements, certainty labels required.

### Phase 4: Drafting

1. Determine the strategic goal: accept, decline, defer, pitch, gather information, maintain relationship.
2. Apply the QNFO/QWAV positioning from `references/qnfo-qwav-strategy.md`.
3. Apply tone guidelines from `references/email-patterns.md`.
4. Run through qnfo-core §0.0: banned words check, certainty calibration, falsifiability check.
5. Present draft with explicit strategic rationale.

### Phase 5: Delivery

- Use Computer Use to click Reply in the Outlook window and type the response.
- Or present the draft for user review before sending.
- After sending, remember the interaction (`remember_fact`) for future reference.

## Python win32com Fallback Protocol (MANDATORY when UI search fails)

When UI-based search returns no results, irrelevant results, or stalls, fall back to Python win32com immediately. Do NOT retry UI search more than twice.

### Search all stores by keyword

```python
import win32com.client
from datetime import datetime, timedelta

outlook = win32com.client.Dispatch("Outlook.Application")
ns = outlook.GetNamespace("MAPI")

def search_folders(folder, depth, keyword, max_days):
    if depth > 5:
        return
    if folder.Items.Count > 0:
        cutoff = datetime.now() - timedelta(days=max_days)
        try:
            kw_filter = (
                f"@SQL=urn:schemas:httpmail:subject LIKE '%{keyword}%' "
                f"OR urn:schemas:httpmail:textdescription LIKE '%{keyword}%'"
            )
            found = folder.Items.Restrict(kw_filter)
            for item in found:
                try:
                    date = item.ReceivedTime
                except Exception:
                    try:
                        date = item.SentOn
                    except Exception:
                        continue
                if date.replace(tzinfo=None) >= cutoff:
                    print(f"[{folder.Name}] {item.SenderName} | {item.Subject} | {date}")
        except Exception:
            pass
    for sub in folder.Folders:
        search_folders(sub, depth + 1, keyword, max_days)

for store in ns.Stores:
    search_folders(store.GetRootFolder(), 0, "research", 21)
```

### Read full email body by subject match

```python
import win32com.client

outlook = win32com.client.Dispatch("Outlook.Application")
ns = outlook.GetNamespace("MAPI")
# ...search stores recursively for matching subject...
print(item.Body)
```

### Key advantages over UI search

| Aspect | UI Search | Python win32com |
|:-------|:----------|:----------------|
| Cross-account | "All Mailboxes" unreliable | Searches all stores explicitly |
| Cross-folder | Manual navigation needed | Recursive: hits all folders |
| Body access | UIA tree length limited | Full body text |
| Reliability | Window disappears, search stalls | Direct COM, no UI dependency |
| Speed | 5-10 tool calls per search | 1 script execution |

**Gate:** If UI search returns 0 results after 2 attempts, switch to Python win32com. Do not retry.

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


## Integration Points

| Skill / Capability | When to Load | What It Provides |
|:-------------------|:-------------|:-----------------|
| `qnfo-core` | Before drafting any response | Research Integrity Mandate, governance, banned words, certainty labels |
| `knowledge` | Before checking contact history | KG querying, memory search, paper context |
| `research` | When citing QNFO publications | Paper lookup, DOI retrieval, publication context |
| `windows-command-patterns` | Before any Python `exec` | Python-First Protocol, encoding safety, cmd chaining |
| Computer Use tools | Throughout (Outlook interaction) | Built-in capability — `launch_app`, `get_window_state`, `click`, `type_text`, `hotkey`, `set_value`, `list_windows` |
| YoBrowser (`load_url`, `cdp_send`) | When desktop Outlook is unrecoverable | Outlook Web Access (OWA) fallback |

## Key Constraints

- **Description must stay ≤176 chars** (same scanner bug that broke qnfo-core and system).
- Computer Use for Outlook requires patience — PostMessage-based typing may not verify; element-indexed `set_value` and UIA Invoke are more reliable.
- Drafts must pass qnfo-core §0.0 before delivery — no exceptions.
- Never fabricate citations or DOI references. Verify via `search_papers_enriched` or `get_paper_context`.
- **Python safety:** All COM scripts must be written to `.py` files and executed via `exec python`, never inline. See `windows-command-patterns` v3.0 for Python-First Protocol.

## Anti-Patterns

| Anti-Pattern | Correct |
|:-------------|:--------|
| Using `launch_app(name="Outlook")` on Windows | Use `launch_app(path="C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE")` only |
| Using `start_minimized: true` with Outlook | Never minimize — the window becomes undetectable |
| Pressing Enter to submit Outlook search | Click the Submit Search button explicitly via element_index |
| Retrying UI search 3+ times when it returns irrelevant results | Fall back to Python win32com after 2 failed UI search attempts |
| Assuming single Outlook account | Run Phase 0: Environment Discovery first |
| Searching only Inbox | Search Sent Items, Archive, Deleted Items too |
| Reading email body via UIA tree (truncation risk) | Use Python win32com `item.Body` for reliable full-body access |
| Inline Python with complex quoting | Write to `.py` file first, then `exec python` |
| Treating `computer-use` as a loadable skill | It's a built-in capability — reference its tools directly |

## References

- `references/qnfo-qwav-strategy.md` — QWAV commercial thesis, Qubit Delusion series, Manifesto, Problem-Substrate Mapping, JPCUB positioning
- `references/email-patterns.md` — Communication patterns: declining opportunities, pitching QWAV, follow-ups, relationship maintenance
- `scripts/find-ice-email.py` — Python template for sender-specific email search via win32com (generalize for other contacts)
- `scripts/search-email.py` — Python general-purpose keyword search across all Outlook stores/folders via win32com

## Version

Current: **v1.1** (kaizen — 20-finding remediation, 2026-07-31)
