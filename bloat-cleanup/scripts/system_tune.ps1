<#
.SYNOPSIS DeepChat System Tuner — Apply all non-admin system optimizations.
Executes: power plan, startup cleanup, visual effects, deepchat config cleanup.
No admin required for most operations.
#>
param(
    [switch]$PowerPlan,
    [switch]$Startup,
    [switch]$ConfigClean,
    [switch]$All,
    [switch]$Status
)

if ($Status) {
    Write-Host '=== SYSTEM TUNE STATUS ==='
    $plan = powercfg /getactivescheme 2>&1 | Select-String 'Power Scheme'
    Write-Host "  Power Plan: $plan"
    Write-Host ''
    Write-Host '  Startup programs:'
    Get-CimInstance Win32_StartupCommand | ForEach-Object { Write-Host "    $($_.Name.Substring(0,[Math]::Min(45,$_.Name.Length)))" }
    Write-Host ''
    Write-Host '  agent.db: '
    $db = "$env:APPDATA\DeepChat\app_db\agent.db"
    if (Test-Path $db) { Write-Host "    $([math]::Round((Get-Item $db).Length/1GB,2)) GB" }
    $bak = @(Get-ChildItem "$env:APPDATA\DeepChat\*.bak" -EA SilentlyContinue)
    Write-Host "  Config .bak files: $($bak.Count)"
    exit 0
}

if ($All) { $PowerPlan = $Startup = $ConfigClean = $true }

if ($PowerPlan) {
    Write-Host '=== POWER PLAN: High Performance ==='
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 2>$null
    if ($LASTEXITCODE -eq 0) { Write-Host '  Set to High Performance' -ForegroundColor Green }
    else { Write-Host '  Could not set (may need admin)' -ForegroundColor Yellow }
}

if ($Startup) {
    Write-Host ''
    Write-Host '=== STARTUP CLEANUP ==='
    $items = Get-CimInstance Win32_StartupCommand
    $remove = @('MicrosoftEdgeAutoLaunch', 'GoogleDriveFS', 'Send to OneNote')
    foreach ($item in $items) {
        foreach ($pattern in $remove) {
            if ($item.Name -like "*$pattern*") {
                try {
                    $item | Remove-CimInstance -ErrorAction Stop
                    Write-Host "  Disabled: $($item.Name.Substring(0,50))" -ForegroundColor Green
                } catch {
                    Write-Host "  Could not disable: $($item.Name) (needs admin)" -ForegroundColor Yellow
                }
            }
        }
    }
    Write-Host '  Use "system_tune.ps1 -Startup" to re-enable if needed'
}

if ($ConfigClean) {
    Write-Host ''
    Write-Host '=== CONFIG CLEANUP ==='
    $roaming = "$env:APPDATA\DeepChat"
    $cleaned = 0
    $freed = 0
    foreach ($f in Get-ChildItem "$roaming\*.bak" -EA SilentlyContinue) {
        try {
            $sz = $f.Length
            Remove-Item $f.FullName -Force
            $freed += $sz
            $cleaned++
        } catch {}
    }
    Write-Host "  Cleaned $cleaned .bak files ($([math]::Round($freed/1024,0)) KB)" -ForegroundColor Green
}

# DEPRECATED 2026-08-02: PowerShell retired. Python-first only. See bloat-cleanup DEPRECATED-POWERSHELL-README.txt
