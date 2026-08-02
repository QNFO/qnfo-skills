<#
.SYNOPSIS DeepChat Autonomous Admin Trigger v2.0
Queue admin operations. No admin required.
PARAMETERS: -KillBloat -DisableServices -RestartDeepChat -AggressivePrune
            -AgentDBPrune -StopService -DisableService -Status -Command
#>
param(
    [switch]$KillBloat,
    [switch]$DisableServices,
    [switch]$RestartDeepChat,
    [int]$DelaySeconds = 30,
    [switch]$AggressivePrune,
    [switch]$AgentDBPrune,
    [string]$StopService,
    [string]$DisableService,
    [switch]$Status,
    [string]$Command
)

$QueueDir = 'C:\Users\LENOVO\.deepchat\admin_queue'
$SkillDir = 'C:\Users\LENOVO\.deepchat\skills\bloat-cleanup\scripts'
$DC_EXE = 'C:\Users\LENOVO\AppData\Local\Programs\DeepChat\DeepChat.exe'

if (-not (Test-Path $QueueDir)) { New-Item -ItemType Directory -Path $QueueDir -Force | Out-Null }

# ── Status ────────────────────────────────────────────
if ($Status) {
    Write-Host '=== WATCHER STATUS ===' -ForegroundColor Cyan
    $tr = & schtasks.exe /query /tn 'DC_Watcher' /fo LIST 2>&1
    if ($LASTEXITCODE -eq 0) { Write-Host '  Watcher: INSTALLED' -ForegroundColor Green }
    else { Write-Host '  Watcher: NOT INSTALLED' -ForegroundColor Red; Write-Host '  Install: manage_watcher.ps1 -Install' }
    $sig = @(Get-ChildItem (Join-Path $QueueDir '*.signal') -ErrorAction SilentlyContinue)
    $don = @(Get-ChildItem (Join-Path $QueueDir '*.done') -ErrorAction SilentlyContinue)
    Write-Host ('  Queue: ' + $sig.Count + ' pending, ' + $don.Count + ' done')
    if ($sig.Count -gt 0) { $sig | ForEach-Object { Write-Host ('    PENDING: ' + $_.Name) -ForegroundColor Yellow } }
    $lf = Join-Path $QueueDir 'watcher.log'
    if (Test-Path $lf) {
        Write-Host '  Recent activity:'
        Get-Content $lf -Tail 8 | ForEach-Object { Write-Host ('    ' + $_) -ForegroundColor DarkGray }
    }
    $db = Join-Path $env:APPDATA 'DeepChat\app_db\agent.db'
    if (Test-Path $db) { Write-Host ('  agent.db: ' + [math]::Round((Get-Item $db).Length/1GB,2) + ' GB') }
    Write-Host ''
    exit 0
}

# ── Build commands ────────────────────────────────────
$commands = @()
$jobId = 'job_' + (Get-Date -Format 'yyyyMMdd_HHmmss')

if ($KillBloat) {
    $commands += @(
        @{ type = 'kill'; target = 'OfficeClickToRun' },
        @{ type = 'kill'; target = 'MSPCManagerService' },
        @{ type = 'kill'; target = 'SearchHost' },
        @{ type = 'kill'; target = 'SDXHelper' },
        @{ type = 'kill'; target = 'WidgetService' },
        @{ type = 'kill'; target = 'CrossDeviceService' },
        @{ type = 'kill'; target = 'StartMenuExperienceHost' },
        @{ type = 'kill'; target = 'TextInputHost' },
        @{ type = 'kill'; target = 'SecurityHealthSystray' }
    )
    $jobId = 'kill_bloat_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
}

if ($DisableServices) {
    $commands += @(
        @{ type = 'service'; action = 'stop'; name = 'ClickToRunSvc' },
        @{ type = 'service'; action = 'disable'; name = 'ClickToRunSvc' },
        @{ type = 'sc'; action = 'failure'; name = 'ClickToRunSvc'; extra = 'reset= 86400 actions= ' },
        @{ type = 'service'; action = 'stop'; name = 'MSPCManagerService' },
        @{ type = 'service'; action = 'disable'; name = 'MSPCManagerService' },
        @{ type = 'service'; action = 'stop'; name = 'WSearch' },
        @{ type = 'service'; action = 'disable'; name = 'WSearch' },
        @{ type = 'service'; action = 'stop'; name = 'SysMain' },
        @{ type = 'service'; action = 'disable'; name = 'SysMain' },
        @{ type = 'service'; action = 'stop'; name = 'DiagTrack' },
        @{ type = 'service'; action = 'disable'; name = 'DiagTrack' },
        @{ type = 'service'; action = 'stop'; name = 'WpnService' },
        @{ type = 'service'; action = 'disable'; name = 'WpnService' },
        @{ type = 'service'; action = 'stop'; name = 'DusmSvc' },
        @{ type = 'service'; action = 'disable'; name = 'DusmSvc' }
    )
    $jobId = 'disable_services_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
}

if ($RestartDeepChat) {
    $d = if ($DelaySeconds -gt 0) { $DelaySeconds } else { 30 }
    $commands += @{
        type = 'schtask_create'
        task_name = 'DC_RestartDeepChat'
        command = $DC_EXE
        delay_seconds = $d
    }
    $jobId = 'restart_' + (Get-Date -Format 'HHmmss')
    Write-Host ('DeepChat will restart ~' + $d + 's after watcher processes')
}

if ($AggressivePrune) {
    $ps = Join-Path $SkillDir 'agent_db_prune.py'
    $commands += @{ type = 'exec'; program = 'python'; arguments = ('"' + $ps + '" --vacuum --max-age-days 14') }
    $jobId = 'aggressive_prune_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
    Write-Host 'WARNING: Deletes ALL unpinned sessions >14 days'
}

if ($AgentDBPrune) {
    $ps = Join-Path $SkillDir 'agent_db_prune.py'
    $commands += @{ type = 'exec'; program = 'python'; arguments = ('"' + $ps + '" --vacuum --max-age-days 30') }
    $jobId = 'agentdb_prune_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
}

if ($StopService) {
    $commands += @{ type = 'service'; action = 'stop'; name = $StopService }
    $jobId = 'stop_' + $StopService + '_' + (Get-Date -Format 'HHmmss')
}

if ($DisableService) {
    $commands += @{ type = 'service'; action = 'disable'; name = $DisableService }
    $jobId = 'disable_' + $DisableService + '_' + (Get-Date -Format 'HHmmss')
}

if ($Command) {
    if (Test-Path $Command) {
        $job = Get-Content $Command -Raw | ConvertFrom-Json
        $jobId = $job.id
        $commands = $job.commands
    } else {
        Write-Error ('Command file not found: ' + $Command)
        exit 1
    }
}

if ($commands.Count -eq 0) {
    Write-Host 'USAGE: trigger_admin.ps1 -KillBloat|-DisableServices|-RestartDeepChat'
    Write-Host '       -AggressivePrune|-AgentDBPrune|-Status|-Command FILE'
    exit 0
}

$job = @{ id = $jobId; commands = $commands }
$signalPath = Join-Path $QueueDir ($jobId + '.signal')
$job | ConvertTo-Json -Depth 4 | Set-Content $signalPath -Encoding UTF8

Write-Host ''
Write-Host '=== ADMIN OPERATION QUEUED ===' -ForegroundColor Cyan
Write-Host ('  Job:      ' + $jobId)
Write-Host ('  Commands: ' + $commands.Count)
Write-Host ('  Signal:   ' + $signalPath)
Write-Host '  Processing within 60s...'
Write-Host ''
Write-Host 'Check: trigger_admin.ps1 -Status' -ForegroundColor DarkGray

# DEPRECATED 2026-08-02: PowerShell retired. Python-first only. See bloat-cleanup DEPRECATED-POWERSHELL-README.txt
