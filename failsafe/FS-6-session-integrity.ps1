# FS-6: Session-Start Integrity Check
# Run at the beginning of every session to verify skill file integrity.
# Compares installed skills vs repo using SHA256 and size.
# Detects drift, corruption, or unauthorized changes before work begins.
#
# Usage: .\FS-6-session-integrity.ps1 [-InstallDir <dir>] [-RepoDir <dir>] [-VerboseReport]
# Returns: exit 0 if all checks pass, exit 1 if anomalies found

param(
    [string]$InstallDir = "$env:USERPROFILE\.deepchat\skills",
    [string]$RepoDir = "$PSScriptRoot\..",
    [switch]$VerboseReport,
    [string]$ReportDir = "$PSScriptRoot\..\logs"
)

$TRACKED_SKILLS = @(
    "cloudflare", "code", "documents", "frontend-design", "git-github",
    "kaizen-skill-fixes", "knowledge", "qnfo-agent", "research", "system"
)

# Size baselines from red-team closeout (v3.47 / v2.24 era)
$SIZE_BASELINES = @{
    "qnfo-agent" = @{ Min = 65000; Max = 80000; Baseline = 71004 }
    "research"    = @{ Min = 125000; Max = 140000; Baseline = 131707 }
    "kaizen-skill-fixes" = @{ Min = 30000; Max = 40000; Baseline = 34878 }
    "system"      = @{ Min = 17000; Max = 20000; Baseline = 18047 }
}

function Invoke-IntegrityCheck {
    param([string]$InstallDir, [string]$RepoDir)
    
    $anomalies = @()
    $allClear = @()
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    Write-Output "============ FS-6 SESSION INTEGRITY CHECK ============"
    Write-Output "Timestamp: $timestamp"
    Write-Output ""
    
    foreach ($skill in $TRACKED_SKILLS) {
        $installedPath = Join-Path $InstallDir "${skill}\SKILL.md"
        $repoPath = Join-Path $RepoDir "${skill}\SKILL.md"
        
        $installedExists = Test-Path $installedPath
        $repoExists = Test-Path $repoPath
        
        if (-not $installedExists) {
            $anomalies += ("[MISSING] ${skill}: not installed at $installedPath")
            Write-Output ("[FAIL] ${skill}: NOT INSTALLED")
            continue
        }
        
        if (-not $repoExists) {
            if ($VerboseReport) {
                Write-Output ("[INFO] ${skill}: installed only (not in repo)")
            }
            continue
        }
        
        $installedSize = (Get-Item $installedPath).Length
        $repoSize = (Get-Item $repoPath).Length
        $installedHash = (Get-FileHash $installedPath -Algorithm SHA256).Hash
        $repoHash = (Get-FileHash $repoPath -Algorithm SHA256).Hash
        
        $sizeMatch = $installedSize -eq $repoSize
        $hashMatch = $installedHash -eq $repoHash
        
        # Check size baselines
        if ($SIZE_BASELINES.ContainsKey($skill)) {
            $bl = $SIZE_BASELINES[$skill]
            if ($installedSize -lt $bl.Min -or $installedSize -gt $bl.Max) {
                $msg = "[SIZE] ${skill}: $installedSize bytes outside baseline [$($bl.Min)-$($bl.Max)]"
                $anomalies += $msg
            }
        }
        
        if ($sizeMatch -and $hashMatch) {
            $allClear += $skill
            Write-Output ("[PASS] ${skill}: $installedSize bytes, hash match")
        } elseif (-not $sizeMatch -and $hashMatch) {
            $diff = $installedSize - $repoSize
            Write-Output ("[WARN] ${skill}: $installedSize vs $repoSize bytes (diff=$diff) -- line-ending drift")
        } else {
            $anomalies += ("[MISMATCH] ${skill}: SHA256 differs! installed=$installedSize repo=$repoSize")
            Write-Output ("[FAIL] ${skill}: SHA256 MISMATCH -- installed=$installedSize repo=$repoSize")
        }
    }
    
    Write-Output ""
    Write-Output "--- SUMMARY ---"
    Write-Output "PASS: $($allClear.Count)/$($TRACKED_SKILLS.Count) skills"
    Write-Output "ANOMALIES: $($anomalies.Count)"
    
    if ($anomalies.Count -gt 0) {
        Write-Output ""
        Write-Output "--- ANOMALY DETAIL ---"
        foreach ($a in $anomalies) {
            Write-Output "  $a"
        }
        Write-Output ""
        Write-Output "ACTION REQUIRED: Review anomalies before proceeding."
    } else {
        Write-Output "INTEGRITY: ALL CLEAR -- Proceed with session."
    }
    
    Write-Output "====================================================="
    
    # Write report to file
    if (-not (Test-Path $ReportDir)) {
        New-Item -ItemType Directory -Path $ReportDir -Force | Out-Null
    }
    
    $reportDate = Get-Date -Format "yyyy-MM-dd"
    $reportFile = Join-Path $ReportDir "integrity-$reportDate.json"
    
    $report = @{
        Timestamp = $timestamp
        AllClear = $allClear
        Anomalies = $anomalies
        TotalChecked = $TRACKED_SKILLS.Count
        Passed = ($anomalies.Count -eq 0)
    }
    
    $report | ConvertTo-Json -Depth 2 | Set-Content $reportFile
    Write-Output "Report saved: $reportFile"
    
    return $report
}

# Main
$result = Invoke-IntegrityCheck -InstallDir $InstallDir -RepoDir $RepoDir
if (-not $result.Passed) {
    Write-Output ""
    Write-Output "[FS-6] INTEGRITY CHECK FAILED -- $($result.Anomalies.Count) anomalies detected."
    exit 1
}
exit 0
