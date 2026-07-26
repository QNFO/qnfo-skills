# FS-1: Pre-Write Backup
# Creates a timestamped backup of any SKILL.md before a destructive write.
# Invoked before write/edit tool calls in the agent loop targeting skill files.
#
# Usage: .\FS-1-pre-write-backup.ps1 -TargetPath <path> [-BackupDir <dir>]
# Returns: backup path on success, $null if skipped (file doesn't exist yet)

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetPath,
    
    [string]$BackupDir = "$PSScriptRoot\..\backups"
)

function Invoke-PreWriteBackup {
    param([string]$TargetPath, [string]$BackupDir)
    
    # Guard: only backup if target exists (no need to backup a new file)
    if (-not (Test-Path $TargetPath)) {
        Write-Output "[FS-1] SKIP: $TargetPath does not exist yet (new file, no backup needed)"
        return $null
    }
    
    # Create backup directory if needed
    if (-not (Test-Path $BackupDir)) {
        New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    }
    
    # Generate timestamped backup filename
    $timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
    $fileName = [System.IO.Path]::GetFileName($TargetPath)
    $dirName = (Get-Item (Split-Path $TargetPath -Parent)).Name
    $backupName = "$($dirName)_$($fileName)_$timestamp.bak"
    $backupPath = Join-Path $BackupDir $backupName
    
    # Copy with metadata preservation
    Copy-Item -Path $TargetPath -Destination $backupPath -Force
    $originalSize = (Get-Item $TargetPath).Length
    $backupSize = (Get-Item $backupPath).Length
    
    if ($originalSize -eq $backupSize) {
        Write-Output "[FS-1] OK: Backup created: $backupPath ($backupSize bytes)"
        return $backupPath
    } else {
        Write-Error "[FS-1] FAIL: Backup size mismatch ($originalSize vs $backupSize)"
        return $null
    }
}

# Main
$result = Invoke-PreWriteBackup -TargetPath $TargetPath -BackupDir $BackupDir
if ($result) {
    Write-Output "BACKUP_PATH=$result"
    exit 0
} else {
    exit 1
}
