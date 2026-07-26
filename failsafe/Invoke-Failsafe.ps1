# Invoke-Failsafe.ps1 -- Master Failsafe Orchestrator
# Runs FS-1 through FS-8 as a unified pipeline for any SKILL.md modification.
# This is the SINGLE ENTRY POINT for all skill-write operations.
#
# Usage: .\Invoke-Failsafe.ps1 -TargetPath <path> -Action <action> [-SessionId <id>] [-PostWrite]
#
# Pipeline:
#   FS-2 (path verify) -> FS-1 (backup) -> FS-3 (pre-size check) ->
#   [perform write externally] ->
#   FS-3 (post-size check) -> FS-7 (version track) -> FS-8 (audit trail)
#
# FS-4 (R2 backup) and FS-5 (pre-commit) run independently.
# FS-6 (session integrity) runs at session start, not per-write.

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetPath,
    
    [ValidateSet("write","edit","delete","restore")]
    [string]$Action = "edit",
    
    [string]$SessionId = "",
    [string]$AgentModel = "deepseek-v4-pro",
    
    # Pre-write: run FS-1, FS-2, FS-3(pre) only
    [switch]$PreWrite,
    
    # Post-write: run FS-3(post), FS-7, FS-8
    [switch]$PostWrite,
    
    # Full pipeline (pre + post)
    [switch]$FullPipeline,
    
    [long]$ExpectedNewSize = 0,
    
    [string]$FailsafeDir = "$PSScriptRoot",
    [string]$BackupDir = "$PSScriptRoot\..\backups",
    [string]$LogDir = "$PSScriptRoot\..\logs"
)

# Banner
Write-Output "============================================"
Write-Output "FAILSAFE PIPELINE -- $Action on $TargetPath"
Write-Output "Session: $SessionId | Agent: $AgentModel"
Write-Output "============================================"

$exitCode = 0
$errors = @()
$backupPath = $null

# === PRE-WRITE PHASE ===
if ($PreWrite -or $FullPipeline) {
    Write-Output "`n>>> PRE-WRITE PHASE <<<"
    
    # FS-2: Path Verification
    Write-Output "`n[FS-2] Path Verification..."
    $fs2Result = & (Join-Path $FailsafeDir "FS-2-path-verification.ps1") -TargetPath $TargetPath 2>&1
    if ($LASTEXITCODE -ne 0) {
        $errors += "[FS-2] Path verification FAILED: $fs2Result"
        Write-Output $fs2Result
        $exitCode = 1
    }
    
    # FS-1: Pre-Write Backup
    Write-Output "`n[FS-1] Pre-Write Backup..."
    $fs1Result = & (Join-Path $FailsafeDir "FS-1-pre-write-backup.ps1") -TargetPath $TargetPath -BackupDir $BackupDir 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Output $fs1Result
        # Backup failure is a warning, not a block (file might be new)
    } else {
        # Extract backup path
        foreach ($line in $fs1Result) {
            if ($line -match 'BACKUP_PATH=(.+)') {
                $backupPath = $matches[1]
            }
        }
    }
    
    # FS-3: Pre-Write Size Guard
    Write-Output "`n[FS-3] Pre-Write Size Guard..."
    $fs3Args = @{ TargetPath = $TargetPath }
    if ($ExpectedNewSize -gt 0) { $fs3Args.NewSize = $ExpectedNewSize }
    $fs3Result = & (Join-Path $FailsafeDir "FS-3-size-guard.ps1") @fs3Args 2>&1
    if ($LASTEXITCODE -ne 0) {
        $errors += "[FS-3] Pre-write size guard FAILED: $fs3Result"
        Write-Output $fs3Result
        $exitCode = 2
    }
}

# === POST-WRITE PHASE ===
if ($PostWrite -or $FullPipeline) {
    Write-Output "`n>>> POST-WRITE PHASE <<<"
    
    # FS-3: Post-Write Size Guard
    Write-Output "`n[FS-3] Post-Write Size Guard..."
    $fs3PostResult = & (Join-Path $FailsafeDir "FS-3-size-guard.ps1") -TargetPath $TargetPath -NewSize 0 2>&1
    if ($LASTEXITCODE -ne 0) {
        $errors += "[FS-3] Post-write size guard FAILED -- possible corruption: $fs3PostResult"
        Write-Output $fs3PostResult
        $exitCode = 2
    }
    
    # FS-7: Version Tracking
    Write-Output "`n[FS-7] Version Tracking..."
    $fs7Result = & (Join-Path $FailsafeDir "FS-7-version-tracking.ps1") -TargetPath $TargetPath -Action $Action 2>&1
    Write-Output $fs7Result
    
    # FS-8: Audit Trail
    Write-Output "`n[FS-8] Audit Trail..."
    if (-not $SessionId) { $SessionId = "manual-" + (Get-Date -Format "yyyyMMddHHmmss") }
    $delta = 0
    if ($ExpectedNewSize -gt 0 -and (Test-Path $TargetPath)) {
        $oldSize = 0
        # Try to get old size from version track
        $trackFile = "$FailsafeDir\..\version-track.json"
        if (Test-Path $trackFile) {
            try {
                $trackData = Get-Content $trackFile -Raw | ConvertFrom-Json
                $skillName = if ($TargetPath -match '\\([^\\]+)\\SKILL\.md$') { $matches[1] } else { "" }
                if ($trackData.$skillName -and $trackData.$skillName.CurrentSize) {
                    $oldSize = $trackData.$skillName.CurrentSize
                }
            } catch {}
        }
    }
    $fs8Result = & (Join-Path $FailsafeDir "FS-8-audit-trail.ps1") -TargetPath $TargetPath `
        -SessionId $SessionId -AgentModel $AgentModel -Action $Action -Delta $delta 2>&1
    Write-Output $fs8Result
}

# === SUMMARY ===
Write-Output "`n============================================"
if ($exitCode -eq 0) {
    Write-Output "FAILSAFE PIPELINE: ALL GATES PASSED"
} else {
    Write-Output "FAILSAFE PIPELINE: GATE FAILURE (code $exitCode)"
    Write-Output "Errors:"
    foreach ($e in $errors) { Write-Output "  $e" }
    if ($backupPath -and $exitCode -ge 2) {
        Write-Output "RESTORE: Backup available at $backupPath"
    }
}
Write-Output "Backup: $backupPath"
Write-Output "============================================"

exit $exitCode
