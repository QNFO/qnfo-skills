# restart_deepchat.ps1 — Canonical DeepChat Restart Script (v1.0)
# 
# Referenced by: skill-creator §7, skill-sync §Mandatory Post-Sync Restart, kaizen-autonomous-update §9
# Canonical home: skill-creator/scripts/restart_deepchat.ps1
# Mirrors: skill-sync/scripts/, kaizen-autonomous-update/scripts/
#
# Kills all DeepChat processes and launches a fresh instance.
# After skill changes, prompts, templates, skills, agents, and subagents are all loaded 
# at application startup — none take effect until DeepChat is restarted.

$ErrorActionPreference = "Stop"

Write-Host "[RESTART] Killing all DeepChat processes..." -ForegroundColor Yellow

$deepchatProcesses = Get-Process | Where-Object { $_.ProcessName -match "DeepChat|deepchat" } -ErrorAction SilentlyContinue
if ($deepchatProcesses) {
    $deepchatProcesses | ForEach-Object {
        Write-Host "  Killing: $($_.ProcessName) (PID: $($_.Id))"
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2
    Write-Host "[RESTART] DeepChat processes terminated." -ForegroundColor Green
} else {
    Write-Host "[RESTART] No DeepChat processes found." -ForegroundColor Yellow
}

$possiblePaths = @(
    "$env:LOCALAPPDATA\Programs\DeepChat\DeepChat.exe",
    "$env:APPDATA\DeepChat\DeepChat.exe",
    "$env:ProgramFiles\DeepChat\DeepChat.exe"
)

$deepchatPath = $null
foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $deepchatPath = $path
        break
    }
}

if ($deepchatPath) {
    Write-Host "[RESTART] Launching DeepChat: $deepchatPath" -ForegroundColor Green
    Start-Process -FilePath $deepchatPath
    Write-Host "[RESTART] DeepChat launched with updated skills." -ForegroundColor Green
} else {
    Write-Host "[RESTART] WARNING: DeepChat.exe not found. Relaunch manually." -ForegroundColor Red
}
Write-Host "[RESTART] Done." -ForegroundColor Green
