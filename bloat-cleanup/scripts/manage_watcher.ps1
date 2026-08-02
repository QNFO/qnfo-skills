<#
.SYNOPSIS DeepChat Admin Watcher Manager v1.0
Install, check, repair, or stop the SYSTEM watcher.
#>
param(
    [switch]$Install,
    [switch]$Check,
    [switch]$Repair,
    [switch]$Stop,
    [switch]$Status
)

$WatcherName = 'DC_Watcher'
$QueueDir = 'C:\Users\LENOVO\.deepchat\admin_queue'
$SkillDir = 'C:\Users\LENOVO\.deepchat\skills\bloat-cleanup\scripts'
$WatcherScript = Join-Path $SkillDir 'admin_watcher.ps1'
$SetupScript = Join-Path $SkillDir 'setup_admin_watcher.bat'

function Test-WatcherExists {
    $r = & schtasks.exe /query /tn $WatcherName /fo LIST 2>&1
    return ($LASTEXITCODE -eq 0)
}

function Test-WatcherProcessing {
    $lf = Join-Path $QueueDir 'watcher.log'
    if (-not (Test-Path $lf)) { return $false }
    $last = Get-Content $lf -Tail 1 -ErrorAction SilentlyContinue
    if (-not $last) { return $false }
    try {
        $ts = $last.Substring(0, 19)
        $lt = [datetime]::ParseExact($ts, 'yyyy-MM-dd HH:mm:ss', $null)
        return ($lt -gt (Get-Date).AddMinutes(-5))
    } catch { return $false }
}

function Show-Status {
    Write-Host '=== DEEPCHAT ADMIN WATCHER STATUS ===' -ForegroundColor Cyan
    Write-Host ''
    $ex = Test-WatcherExists; $pr = Test-WatcherProcessing
    if ($ex) { Write-Host '  Watcher task:   INSTALLED' -ForegroundColor Green }
    else { Write-Host '  Watcher task:   MISSING' -ForegroundColor Red }
    if ($pr) { Write-Host '  Last activity:  ACTIVE (<5 min)' -ForegroundColor Green }
    else { Write-Host '  Last activity:  STALE/STOPPED' -ForegroundColor Yellow }
    if (Test-Path $QueueDir) {
        $sig = @(Get-ChildItem (Join-Path $QueueDir '*.signal') -ErrorAction SilentlyContinue).Count
        $don = @(Get-ChildItem (Join-Path $QueueDir '*.done') -ErrorAction SilentlyContinue).Count
        Write-Host ('  Queue:          ' + $sig + ' pending, ' + $don + ' done')
    } else { Write-Host '  Queue:          Directory missing' -ForegroundColor Red }
    $lf = Join-Path $QueueDir 'watcher.log'
    if (Test-Path $lf) {
        Write-Host ''; Write-Host '  Recent log:' -ForegroundColor DarkGray
        Get-Content $lf -Tail 10 | ForEach-Object { Write-Host ('    ' + $_) -ForegroundColor DarkGray }
    }
    $db = Join-Path $env:APPDATA 'DeepChat\app_db\agent.db'
    if (Test-Path $db) { Write-Host ('  agent.db:       ' + [math]::Round((Get-Item $db).Length/1GB,2) + ' GB') }
    Write-Host ''
}

# ── Dispatch ──────────────────────────────────────────
if ($Status -or (-not ($Install -or $Check -or $Repair -or $Stop))) {
    Show-Status
    if (-not ($Install -or $Check -or $Repair -or $Stop)) {
        Write-Host 'USAGE: manage_watcher.ps1 -Install|-Check|-Repair|-Stop|-Status'
    }
    exit 0
}

if ($Check) {
    if (Test-WatcherExists -and Test-WatcherProcessing) {
        Write-Host 'OK - Watcher is alive' -ForegroundColor Green; exit 0
    } elseif (Test-WatcherExists) {
        Write-Host 'WARN - Watcher exists but stale' -ForegroundColor Yellow; exit 1
    } else {
        Write-Host 'FAIL - Watcher not installed. Run: manage_watcher.ps1 -Install' -ForegroundColor Red; exit 2
    }
}

if ($Install -or $Repair) {
    Write-Host 'Installing watcher (UAC popup)...' -ForegroundColor Yellow
    if (Test-Path $SetupScript) {
        $proc = Start-Process -FilePath $SetupScript -Verb RunAs -Wait -PassThru
        if ($proc.ExitCode -eq 0) {
            Write-Host 'Watcher installed!' -ForegroundColor Green; Show-Status
        } else { Write-Host ('Install failed (exit: ' + $proc.ExitCode + ')') -ForegroundColor Red }
    } else {
        Write-Host 'ERROR: Setup script missing. Trying direct creation...' -ForegroundColor Red
        & schtasks.exe /delete /tn $WatcherName /f 2>$null
        $cmd = 'powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ' + "'$WatcherScript'"
        & schtasks.exe /create /tn $WatcherName /tr $cmd /sc minute /mo 1 /ru SYSTEM /rl HIGHEST /f
        if ($LASTEXITCODE -eq 0) { Write-Host 'Watcher created directly' -ForegroundColor Green }
        else { Write-Host 'Failed. Run setup_admin_watcher.bat as Administrator' -ForegroundColor Red }
    }
}

if ($Stop) {
    Write-Host 'Stopping watcher...' -ForegroundColor Yellow
    & schtasks.exe /delete /tn $WatcherName /f 2>&1
    if ($LASTEXITCODE -eq 0) { Write-Host 'Watcher removed' -ForegroundColor Green }
    else { Write-Host 'Could not remove (may need UAC). Run setup_admin_watcher.bat as Admin' -ForegroundColor Yellow }
}

# DEPRECATED 2026-08-02: PowerShell retired. Python-first only. See bloat-cleanup DEPRECATED-POWERSHELL-README.txt
