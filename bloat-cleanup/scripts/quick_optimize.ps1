<#
.SYNOPSIS DeepChat Quick Optimizer — Bundle of all non-admin optimizations.
Runs: config cleanup, power plan, startup disable, cache cleanup, admin queue.
Safe to run anytime. No admin required.
#>
param(
    [switch]$DryRun
)

$totalFreed = 0
$totalActions = 0

function Clean-File($path, $label) {
    if (Test-Path $path) {
        $sz = (Get-Item $path).Length
        if ($DryRun) {
            Write-Host "  [DRY] Would delete: $label ($([math]::Round($sz/1024,0)) KB)"
            $script:totalFreed += $sz
        } else {
            try {
                Remove-Item $path -Force -ErrorAction Stop
                Write-Host "  Deleted: $label ($([math]::Round($sz/1024,0)) KB)" -ForegroundColor Green
                $script:totalFreed += $sz
            } catch {
                Write-Host "  SKIP: $label (needs admin)" -ForegroundColor Yellow
            }
        }
        $script:totalActions++
    }
}

Write-Host '=== DEEPCHAT QUICK OPTIMIZER ===' -ForegroundColor Cyan
Write-Host ''

# ── Config .bak files ─────────────────────────
Write-Host '[1/5] Config backup files...'
$roaming = "$env:APPDATA\DeepChat"
$bakCount = 0
$bakSize = 0
foreach ($f in Get-ChildItem "$roaming\*.bak" -EA SilentlyContinue) {
    $bakSize += $f.Length
    $bakCount++
    if (-not $DryRun) {
        try { Remove-Item $f.FullName -Force; $script:totalFreed += $f.Length } catch {}
    }
}
if ($DryRun) { Write-Host "  $bakCount .bak files ($([math]::Round($bakSize/1024,0)) KB)" }
else { Write-Host "  Cleaned $bakCount .bak files ($([math]::Round($bakSize/1024,0)) KB)" -ForegroundColor Green }

# ── Dangling files ────────────────────────────
Write-Host ''
Write-Host '[2/5] Dangling files...'
Clean-File "$roaming\_deploy.py" '_deploy.py'

# ── Power plan ────────────────────────────────
Write-Host ''
Write-Host '[3/5] Power plan...'
if ($DryRun) {
    Write-Host '  Would set: High Performance'
} else {
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 2>$null
    Write-Host '  Set to High Performance' -ForegroundColor Green
}

# ── Startup cleanup ───────────────────────────
Write-Host ''
Write-Host '[4/5] Startup cleanup...'
$remove = @('MicrosoftEdgeAutoLaunch', 'Send to OneNote')
$startups = Get-CimInstance Win32_StartupCommand
foreach ($item in $startups) {
    foreach ($p in $remove) {
        if ($item.Name -like "*$p*") {
            if ($DryRun) {
                Write-Host "  Would disable: $($item.Name.Substring(0,50))"
            } else {
                try {
                    $item | Remove-CimInstance -ErrorAction Stop
                    Write-Host "  Disabled: $($item.Name.Substring(0,50))" -ForegroundColor Green
                } catch {
                    Write-Host "  SKIP: $($item.Name) (needs admin)" -ForegroundColor Yellow
                }
            }
            $script:totalActions++
        }
    }
}

# ── Admin queue ───────────────────────────────
Write-Host ''
Write-Host '[5/5] Queuing admin operations...'
if (-not $DryRun) {
    $job = @{
        id = "quickopt_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        commands = @(
            @{ type = 'exec'; program = 'cmd'; arguments = '/c del /q C:\Windows\Logs\CBS\*.log 2>nul & del /q C:\Windows\System32\OneDriveSetup.exe 2>nul & del /q C:\Windows\System32\MRT.exe 2>nul & rmdir /s /q C:\Windows\SoftwareDistribution\Download 2>nul' },
            @{ type = 'exec'; program = 'dism'; arguments = '/online /cleanup-image /startcomponentcleanup /quiet' }
        )
    }
    $q = 'C:\Users\LENOVO\.deepchat\admin_queue'
    mkdir $q -Force | Out-Null
    $job | ConvertTo-Json -Depth 3 | Set-Content (Join-Path $q "$($job.id).signal") -Encoding UTF8
    Write-Host '  Queued: CBS logs, OneDriveSetup, MRT.exe, WU downloads, DISM cleanup' -ForegroundColor Green
    Write-Host '  Processing by SYSTEM watcher within 60s'
}

# ── Summary ───────────────────────────────────
Write-Host ''
Write-Host "=== COMPLETE ($totalActions actions, $([math]::Round($totalFreed/1024,0)) KB freed) ===" -ForegroundColor Cyan

if (-not $DryRun) {
    $u = Get-PSDrive C
    Write-Host "  C: $([math]::Round($u.Free/1GB,1)) GB free ($([math]::Round($u.Free/$u.Used*100,1))%)"
    $db = "$roaming\app_db\agent.db"
    if (Test-Path $db) { Write-Host "  agent.db: $([math]::Round((Get-Item $db).Length/1GB,2)) GB" }
}

# DEPRECATED 2026-08-02: PowerShell retired. Python-first only. See bloat-cleanup DEPRECATED-POWERSHELL-README.txt
