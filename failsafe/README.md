# QNFO Skills Failsafe System

Designed 2026-07-26 after red-team audit identified the corruption vector: unguarded `write` tool calls expanding SKILL.md from 36KB to 53.8MB (1500× blowup).

## Architecture

```
failsafe/
├── Invoke-Failsafe.ps1          # Master orchestrator -- single entry point
├── FS-1-pre-write-backup.ps1    # Timestamped .bak before every write
├── FS-2-path-verification.ps1   # Validates target is a known skill file
├── FS-3-size-guard.ps1          # Blocks writes exceeding 3× growth or 250KB cap
├── FS-4-r2-backup.ps1           # Syncs skill snapshots to Cloudflare R2
├── FS-5-pre-commit-hook.ps1     # Git hook: blocks U+FFFD/U+FFFF/BOM/null bytes
├── FS-5-Install.ps1             # Installs FS-5 as .git/hooks/pre-commit
├── FS-6-session-integrity.ps1   # Session-start SHA256 comparison
├── FS-7-version-tracking.ps1    # Auto-records version bumps + size deltas
├── FS-8-audit-trail.ps1         # Structured JSONL audit log
└── README.md                    # This file
```

## Quick Start

### Per-Write Protection (FS-1, FS-2, FS-3)

Run before AND after any skill file modification:

```powershell
# Pre-write phase
.\failsafe\Invoke-Failsafe.ps1 -TargetPath ".\research\SKILL.md" -Action edit -PreWrite -SessionId "session-abc"

# ... perform the write/edit externally ...

# Post-write phase
.\failsafe\Invoke-Failsafe.ps1 -TargetPath ".\research\SKILL.md" -Action edit -PostWrite -SessionId "session-abc"
```

Or as a full pipeline:

```powershell
.\failsafe\Invoke-Failsafe.ps1 -TargetPath ".\research\SKILL.md" -Action edit -FullPipeline -SessionId "session-abc"
```

### Git Pre-Commit Hook (FS-5)

```powershell
.\failsafe\FS-5-Install.ps1 -Force
```

### Session Start (FS-6)

```powershell
.\failsafe\FS-6-session-integrity.ps1 -VerboseReport
```

### R2 Cloud Backup (FS-4)

```powershell
.\failsafe\FS-4-r2-backup.ps1 -FullSync
```

## Gate Specifications

| Gate | Check | Block? | Recovery |
|------|-------|--------|----------|
| FS-1 | Pre-write backup | No (warn only) | Restore from .bak |
| FS-2 | Path in skill allowlist | **Yes** | Verify target path |
| FS-3 | Size ≤ 250KB AND growth ≤ 3× | **Yes** | Restore from FS-1 backup |
| FS-4 | R2 snapshot sync | No | Pull from R2 |
| FS-5 | No U+FFFD/U+FFFF/BOM/null | **Yes (commit)** | Clean and re-commit |
| FS-6 | SHA256 match installed↔repo | No (warn) | Sync from canonical source |
| FS-7 | Version track record | No | Informational |
| FS-8 | Audit log append | No | Informational |

## Corruption Vectors Mitigated

1. **Wrong-path writes** (FS-2): Target must match a known skill directory
2. **Size blowup** (FS-3): Blocks growth beyond 3× or 250KB absolute cap
3. **Encoding corruption** (FS-5): Blocks U+FFFD, U+FFFF, BOM, null bytes at commit
4. **Unrecoverable loss** (FS-1): Timestamped backup before every modification
5. **Off-machine loss** (FS-4): R2 snapshots survive local disk failure
6. **Undetected drift** (FS-6): Session-start SHA256 comparison catches silent corruption
7. **Untracked changes** (FS-7): Version-track.json records every modification delta
8. **Unaccountable edits** (FS-8): Audit trail logs who/when/what for every write

## Version

v1.0 -- 2026-07-26 -- Initial implementation post red-team corruption audit closeout.
