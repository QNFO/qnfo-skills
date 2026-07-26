# FS-4: R2 Backup
# Periodically mirrors skill file snapshots to Cloudflare R2 (qnfo-backups bucket).
# Provides off-machine backup in case of local corruption or machine failure.
#
# Usage: .\FS-4-r2-backup.ps1 [-FullSync] [-SkillsDir <dir>]
#   -FullSync: sync all tracked skill files to R2
#   -Default (no flag): incremental backup of changed files only

param(
    [switch]$FullSync,
    [string]$SkillsDir = "$env:USERPROFILE\.deepchat\skills",
    [string]$R2Remote = "r2:qnfo-backups/skills",
    [string]$LogDir = "$PSScriptRoot\..\logs"
)

$TRACKED_SKILLS = @(
    "cloudflare", "code", "code-review", "deepchat-settings",
    "doc-coauthoring", "documents", "frontend-design", "git-commit",
    "git-github", "infographic-syntax-creator", "kaizen-skill-fixes",
    "knowledge", "mcp-builder", "qnfo-agent", "research", "system", "xlsx"
)

function Invoke-R2Backup {
    param([bool]$FullSync, [string]$SkillsDir, [string]$R2Remote, [string]$LogDir)
    
    # Ensure log directory
    if (-not (Test-Path $LogDir)) {
        New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
    }
    
    $timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
    $logFile = Join-Path $LogDir "r2-backup-$timestamp.log"
    $errors = @()
    $uploaded = 0
    $skipped = 0
    
    # Check rclone availability
    $rclone = Get-Command rclone -ErrorAction SilentlyContinue
    if (-not $rclone) {
        Write-Error "[FS-4] FAIL: rclone not found. Install rclone and configure R2 remote."
        return @{ Success = $false; Error = "rclone not available" }
    }
    
    # Verify R2 remote exists
    $remoteCheck = & rclone lsd "r2:qnfo-backups" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "[FS-4] FAIL: Cannot access R2 remote 'r2:qnfo-backups'. Check rclone config."
        return @{ Success = $false; Error = "R2 remote inaccessible" }
    }
    
    # Create timestamped snapshot directory in R2
    $snapshotDir = "$R2Remote/$timestamp"
    
    foreach ($skill in $TRACKED_SKILLS) {
        $localPath = Join-Path $SkillsDir "$skill\SKILL.md"
        if (-not (Test-Path $localPath)) {
            Write-Output "[FS-4] SKIP: $skill/SKILL.md not found locally"
            continue
        }
        
        $localSize = (Get-Item $localPath).Length
        
        # Check if R2 already has this version (by hash)
        $localHash = (Get-FileHash $localPath -Algorithm SHA256).Hash
        $hashFile = Join-Path $SkillsDir "$skill\.r2-hash"
        
        if (-not $FullSync) {
            if (Test-Path $hashFile) {
                $storedHash = Get-Content $hashFile -Raw
                if ($storedHash.Trim() -eq $localHash) {
                    Write-Output "[FS-4] SKIP: $skill unchanged (hash match)"
                    $skipped++
                    continue
                }
            }
        }
        
        # Upload to R2
        $r2Path = "$snapshotDir/$skill/SKILL.md"
        Write-Output "[FS-4] UPLOAD: $skill ($localSize bytes) -> $r2Path"
        
        $uploadResult = & rclone copyto $localPath $r2Path --s3-upload-cutoff=100M --no-check-certificate 2>&1
        if ($LASTEXITCODE -eq 0) {
            $localHash | Set-Content $hashFile -NoNewline
            $uploaded++
            Write-Output "[FS-4] OK: $skill uploaded successfully"
        } else {
            $errors += "[FS-4] FAIL: $skill upload failed: $uploadResult"
            Write-Error "[FS-4] FAIL: $skill upload failed: $uploadResult"
        }
    }
    
    # Cleanup old snapshots (keep last 10)
    $snapshots = & rclone lsd "r2:qnfo-backups/skills" 2>&1 | ForEach-Object { ($_ -split '\s+')[-1] } | Where-Object { $_ -match '^\d{4}-\d{2}-\d{2}_\d{6}$' } | Sort-Object -Descending
    if ($snapshots.Count -gt 10) {
        $toDelete = $snapshots[10..($snapshots.Count - 1)]
        foreach ($old in $toDelete) {
            Write-Output "[FS-4] CLEANUP: Removing old snapshot $old"
            & rclone purge "r2:qnfo-backups/skills/$old" 2>&1 | Out-Null
        }
    }
    
    $summary = @{
        Success = ($errors.Count -eq 0)
        Uploaded = $uploaded
        Skipped = $skipped
        Errors = $errors
        SnapshotDir = $snapshotDir
        Timestamp = $timestamp
    }
    
    # Write log
    $summary | ConvertTo-Json -Depth 3 | Set-Content $logFile
    
    Write-Output "`n[FS-4] SUMMARY: $uploaded uploaded, $skipped skipped, $($errors.Count) errors"
    return $summary
}

# Main
$result = Invoke-R2Backup -FullSync:$FullSync -SkillsDir $SkillsDir -R2Remote $R2Remote -LogDir $LogDir
if ($result.Success) {
    exit 0
} else {
    exit 1
}
