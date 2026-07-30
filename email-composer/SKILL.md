---
name: email-composer
description: Email triage, drafting, business communication. Use for inbox analysis, drafting responses, bizdev outreach, declining/pitching, QNFO/QWAV-aligned correspondence.
---

# Email Composer — Business Communication for QNFO/QWAV

## Quick Start

1. **Open Outlook** via Computer Use: `launch_app(name="Outlook")` or `launch_app(path="C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE")`
2. **Find the email**: Use `get_window_state` to inspect inbox; use Ctrl+E for search, type search term via `set_value` on SearchTextBox, click Submit Search
3. **Read the email**: Double-click to open in standalone window; read body via Document element with `get_window_state`
4. **Load strategy context**: Read `references/qnfo-qwav-strategy.md` if QNFO/QWAV positioning is needed for the response
5. **Draft the response**: Apply tone guidelines below, integrate QNFO/QWAV strategy, run through qnfo-agent §0.0 Research Integrity Mandate
6. **Deliver**: Click Reply in the standalone email window, `type_text` the response, or present draft for user approval

## Core Workflow

### Phase 1: Discovery & Triage
- Use Computer Use tools (`list_windows`, `get_window_state`, `click`, `type_text`) to navigate Outlook
- **Critical search tip:** Sender display names in Outlook often differ from the contact's actual name (e.g., "Ice Geng" at TechInBridge may appear as "Project" in the From field). Always search using BROAD terms first ("Talent", "Project", or the person's first name), not the exact company name ("TalentBridge" may return zero results because the display name is "Project"). Only search for the recipient's personal name if the display name search fails.
- **Server-side search:** For emails across all accounts or archived messages, expand the "Current Mailbox" combobox → select "All Mailboxes" → submit search. This reaches Exchange server-side storage, not just the local cache.
- **Common pitfall:** Searching for "TalentBridge" when the actual sender display name is "Project" returns 0 results. Search for "Talent" or "ice@techinbridge.com" instead. The UIA tree will show the actual display name — verify after each search.
- Triage: identify unread emails, categorize by urgency (bizdev opportunity, publication notice, infrastructure alert, spam)

### Phase 2: Analysis
- Read the full email body by double-clicking the email, then inspecting the standalone window with `get_window_state(max_elements=150, max_depth=30)`
- Extract: sender identity (company, role, relationship history), what they're asking, what they're offering, what they need from you
- Check conversation history: search sent items for prior exchanges with this contact
- Check memory (search_memories, recall_facts) for prior interactions and decisions

### Phase 3: Strategic Context
- **ALWAYS** verify QNFO agent is loaded via `skill_view("qnfo-agent")` before drafting — it contains the Research Integrity Mandate and governance framework
- If QNFO/QWAV commercial positioning is relevant, read `references/qnfo-qwav-strategy.md`
- If the response requires specific communication patterns, read `references/email-patterns.md`
- Cross-reference against qnfo-agent §0.0 (Research Integrity) — no marketing language, no promissory statements, certainty labels required

### Phase 4: Drafting
1. Determine the strategic goal: accept, decline, defer, pitch, gather information, maintain relationship
2. Apply the QNFO/QWAV positioning from `references/qnfo-qwav-strategy.md`
3. Apply tone guidelines from `references/email-patterns.md`
4. Run through qnfo-agent §0.0: banned words check, certainty calibration, falsifiability check
5. Present draft with explicit strategic rationale

### Phase 5: Delivery
- Use Computer Use to click Reply in the Outlook window and type the response
- Or present the draft for user review before sending
- After sending, remember the interaction (remember_fact) for future reference

## Integration Points

| Skill | When to Load | What It Provides |
|-------|-------------|-----------------|
| `qnfo-agent` | Before drafting any response | Research Integrity Mandate, governance, banned words, certainty labels |
| `knowledge` | Before checking contact history | KG querying, memory search, paper context |
| `research` | When citing QNFO publications | Paper lookup, DOI retrieval, publication context |
| `computer-use` | Throughout (Outlook interaction) | Desktop GUI automation |

## Key Constraints

- **Description must stay ≤176 chars** (same scanner bug that broke qnfo-agent and system)
- Computer Use for Outlook requires patience — PostMessage-based typing may not verify; element-indexed `set_value` and UIA Invoke are more reliable
- Drafts must pass qnfo-agent §0.0 before delivery — no exceptions
- Never fabricate citations or DOI references. Verify via `search_papers_enriched` or `get_paper_context`

## References

- `references/qnfo-qwav-strategy.md` — QWAV commercial thesis, Qubit Delusion series, Manifesto, Problem-Substrate Mapping, JPCUB positioning
- `references/email-patterns.md` — Communication patterns: declining opportunities, pitching QWAV, follow-ups, relationship maintenance
