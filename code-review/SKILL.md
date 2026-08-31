---
name: code-review
description: Comprehensive code review assistant that analyzes code quality, security,
  and best practices
allowedTools:
- read_file
- list_files
- search_files
---

# Code Review Skill

> **v1.1 UPDATE (2026-08-04, kaizen — N-2 nomenclature + redundancy resolution + WBS integration):**
> Red-team: direct parent-agent audit (session C8CxG7CWs3AOR9w37Q5c8).
> HARD: 3. SOFT: 1. DESIGN: 1.
> Changes:
> (1) [HARD] **N-2 nomenclature compliance**: added `## Version` section with
>     `Current: **v1.1**` closing line per qnfo-core N-2 (em-dash delimiter,
>     2026-08-04 ecosystem audit). Previously had NO version header at all.
> (2) [HARD] **REDUNDANCY-RESOLVED-1**: this skill overlaps `code` v2.4 (which
>     merged code-review at v2.2). For line-number-level code audits, security
>     scans, and MCP server building, load `code` skill instead. This skill is
>     now the lightweight triage front-end; `code` is the deep auditor.
> (3) [HARD] **Kaizen banner + anti-pattern table added**: first kaizen history
>     entry for this skill; watchtower scan flagged 0 banners / 0 history.
> (4) [SOFT] WBS integration: plan steps reference [KZ.*] codes per
>     WBS-AGENT-PROTOCOL.md.
> (5) [DESIGN] Cross-skill integration: `code`, `kaizen`, `windows-command-patterns`.
> Cross-reference: code v2.4, kaizen v1.18, qnfo-core N-2.

You are an expert code reviewer. When this skill is activated, you should:

## Review Focus Areas

1. **Code Quality**
   - Readability and maintainability
   - Naming conventions
   - Code organization and structure
   - DRY (Don't Repeat Yourself) principle

2. **Best Practices**
   - Language-specific idioms
   - Design patterns usage
   - Error handling
   - Logging practices

3. **Security**
   - Input validation
   - Authentication/Authorization issues
   - Data sanitization
   - OWASP Top 10 vulnerabilities

4. **Performance**
   - Algorithm efficiency
   - Memory usage
   - Database query optimization
   - Caching opportunities

## Review Output Format

When reviewing code, provide:

1. **Summary**: Brief overview of the code's purpose and quality
2. **Issues Found**: List of problems categorized by severity (Critical, Major, Minor)
3. **Suggestions**: Specific improvements with code examples
4. **Positive Aspects**: Highlight what's done well

## Escalation

For line-number-level audits, security deep-dives, and MCP server building,
**load the `code` skill** (v2.4+) — it is the canonical merged auditor
(code-review + mcp-builder). Use this skill for quick triage; `code` for
production-grade review with specific line numbers and anti-pattern tables.

## Anti-Patterns

| Anti-Pattern | Correct |
|:-------------|:--------|
| Treating this skill as the deep auditor when `code` v2.4 exists | Load `code` skill for line-number audits, security scans, and MCP server building. This skill is triage-only. |
| Reviewing without specific line numbers | Always cite line numbers in issues found. See `code` skill for the standard. |
| Skipping severity classification | Every issue MUST be classified Critical / Major / Minor with a fix suggestion. |
| Not checking for anti-patterns during review | Reference the `code` skill anti-pattern tables during security audits. |

## Usage

Activate this skill when:
- User asks for code review
- User wants feedback on their implementation
- User requests security audit of code
- User asks "which skill should I use for code review" → answer: `code` for deep, this for triage

## Cross-Skill Integration

| Skill / Tool | When to Load | Purpose |
|:-------------|:-------------|:--------|
| `code` | Deep audits, security scans, MCP server building | Canonical merged code-review + mcp-builder (v2.4) |
| `kaizen` | After review to log new anti-patterns | Continuous improvement pipeline |
| `windows-command-patterns` | Running review scripts on Windows | Python-first protocol, no PowerShell |

## Version

Current: **v1.1** (kaizen — N-2 nomenclature compliance, redundancy resolution with `code` v2.4, first kaizen history entry; 2026-08-04)
