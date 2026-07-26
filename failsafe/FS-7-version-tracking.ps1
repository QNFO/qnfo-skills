# FS-7: Version Tracking
# Automatically records version bumps and file size deltas on every SKILL.md change.
# Maintains a version-track.json database for all tracked skills.
#
# Usage: .\FS-7-version-track.ps1 -TargetPath <path> [-Action <edit|write|delete>] [-TrackFile <path>]
# Must be called AFTER a SKILL.md modification completes.

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetPath,
    
    [ValidateSet("edit","write","delete","restore")]
    [string]$Action = "edit",
    
    [string]$TrackFile = "$PSScriptRoot\..\version-track.json",
    [string]$BackupDir = "$PSScriptRoot\..\backups"
)

function Invoke-VersionTrack {
    param([string]$TargetPath, [string]$Action, [string]$TrackFile, [string]$BackupDir)
    
    # Extract skill name
    $skillName = ""
    if ($TargetPath -match '\\([^\\]+)\\SKILL\.md$') {
        $skillName = $matches[1]
    } else {
        Write-Error "[FS-7] Cannot determine skill name from path: $TargetPath"
        return
    }
    
    # Get current file state
    $currentSize = 0
    $currentHash = ""
    $exists = Test-Path $TargetPath
    
    if ($exists) {
        $currentSize = (Get-Item $TargetPath).Length
        $currentHash = (Get-FileHash $TargetPath -Algorithm SHA256).Hash
    }
    
    $timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"
    
    # Load existing track data
    $trackData = @{}
    if (Test-Path $TrackFile) {
        try {
            $trackData = Get-Content $TrackFile -Raw | ConvertFrom-Json -AsHashtable
        } catch {
            Write-Output "[FS-7] WARN: Could not parse existing track file, starting fresh."
            $trackData = @{}
        }
    }
    
    # Initialize skill entry
    if (-not $trackData.ContainsKey($skillName)) {
        $trackData[$skillName] = @{
            Skill = $skillName
            Created = $timestamp
            Events = @()
            CurrentSize = $currentSize
            CurrentHash = $currentHash
            TotalEdits = 0
        }
    }
    
    # Determine version change
    $skill = $trackData[$skillName]
    $prevEvent = if ($skill.Events.Count -gt 0) { $skill.Events[-1] } else { $null }
    
    $prevSize = if ($prevEvent) { $prevEvent.NewSize } else { 0 }
    $prevHash = if ($prevEvent) { $prevEvent.NewHash } else { "" }
    
    $sizeDelta = $currentSize - $prevSize
    $hashChanged = $currentHash -ne $prevHash
    
    # Detect version from SKILL.md frontmatter
    $version = "unknown"
    if ($exists) {
        $content = Get-Content $TargetPath -Raw
        if ($content -match 'version:\s*(\S+)') {
            $version = $matches[1]
        }
    }
    
    # Record event
    $event = @{
        Timestamp = $timestamp
        Action = $Action
        Version = $version
        OldSize = $prevSize
        NewSize = $currentSize
        SizeDelta = $sizeDelta
        OldHash = $prevHash
        NewHash = $currentHash
        HashChanged = $hashChanged
    }
    
    $skill.Events += $event
    $skill.CurrentSize = $currentSize
    $skill.CurrentHash = $currentHash
    $skill.TotalEdits = $skill.Events.Count
    
    # Check for latest backup
    $backupsForSkill = Get-ChildItem $BackupDir -Filter "${skillName}_SKILL.md_*.bak" -ErrorAction SilentlyContinue |
                        Sort-Object LastWriteTime -Descending
    if ($backupsForSkill) {
        $skill.LatestBackup = $backupsForSkill[0].Name
    }
    
    # Save
    $trackData | ConvertTo-Json -Depth 5 | Set-Content $TrackFile
    
    Write-Output "[FS-7] TRACKED: $skillName v$version | $Action | ${sizeDelta} bytes delta | $currentSize bytes total"
    
    return @{
        Skill = $skillName
        Version = $version
        SizeDelta = $sizeDelta
        NewSize = $currentSize
    }
}

# Main
Invoke-VersionTrack -TargetPath $TargetPath -Action $Action -TrackFile $TrackFile -BackupDir $BackupDir
exit 0
