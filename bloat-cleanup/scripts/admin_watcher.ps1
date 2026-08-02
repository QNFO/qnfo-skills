<#
.SYNOPSIS
DeepChat Autonomous Admin Watcher v2.0 — Runs as SYSTEM via Scheduled Task.
Polls a queue directory for signal files and executes admin commands.

COMMAND TYPES SUPPORTED:
  kill              — Stop-Process -Force                     (admin only processes)
  service           — Stop/Disable/Start Windows services     (admin only services)
  sc                — sc.exe commands with arbitrary args
  registry          — Set-ItemProperty on any registry path
  schtask_create    — Create SYSTEM scheduled task (for autonomous restart)
  exec              — Run arbitrary .exe with args
  test              — Heartbeat test (watcher health check)

CHANGELOG v2.0:
  + schtask_create handler for autonomous DeepChat restart
  + exec handler for arbitrary program execution
  + Health log entry on every poll (even with no signals)
  + Truncates log at 1000 lines to prevent log bloat
#>
param()

$QueueDir = "C:\Users\LENOVO\.deepchat\admin_queue"
$LogFile = Join-Path $QueueDir "watcher.log"
$MAX_LOG_LINES = 1000

# Create queue dir if missing
if (-not (Test-Path $QueueDir)) {
    New-Item -ItemType Directory -Path $QueueDir -Force | Out-Null
}

# ── Health heartbeat (every poll) ─────────────────────
$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$activeSignals = (Get-ChildItem -Path $QueueDir -Filter "*.signal" -ErrorAction SilentlyContinue).Count

# Process all .signal files
$signals = Get-ChildItem -Path $QueueDir -Filter "*.signal" -ErrorAction SilentlyContinue
$processed = 0

foreach ($signal in $signals) {
    try {
        $content = Get-Content $signal.FullName -Raw -ErrorAction Stop
        $job = $content | ConvertFrom-Json -ErrorAction Stop
        
        $resultFile = Join-Path $QueueDir "$($job.id).done"
        $results = @()
        
        foreach ($cmd in $job.commands) {
            $result = @{ type = $cmd.type; status = "unknown"; output = "" }
            
            switch ($cmd.type) {
                "kill" {
                    $proc = Get-Process -Name $cmd.target -ErrorAction SilentlyContinue
                    if ($proc) {
                        Stop-Process -Name $cmd.target -Force -ErrorAction SilentlyContinue
                        $proc2 = Get-Process -Name $cmd.target -ErrorAction SilentlyContinue
                        if (-not $proc2) {
                            $result.status = "killed"
                            $result.output = "Process $($cmd.target) terminated"
                        } else {
                            $result.status = "failed"
                            $result.output = "Process $($cmd.target) still running"
                        }
                    } else {
                        $result.status = "not_running"
                        $result.output = "Process $($cmd.target) was not running"
                    }
                }
                "service" {
                    try {
                        $svc = Get-Service -Name $cmd.name -ErrorAction Stop
                        if ($cmd.action -eq "stop") {
                            if ($svc.Status -ne "Stopped") {
                                Stop-Service -Name $cmd.name -Force -ErrorAction Stop
                                $result.status = "stopped"
                            } else {
                                $result.status = "already_stopped"
                            }
                        } elseif ($cmd.action -eq "disable") {
                            Set-Service -Name $cmd.name -StartupType Disabled -ErrorAction Stop
                            $result.status = "disabled"
                        } elseif ($cmd.action -eq "start") {
                            Start-Service -Name $cmd.name -ErrorAction Stop
                            $result.status = "started"
                        }
                    } catch {
                        $result.status = "error"
                        $result.output = $_.Exception.Message
                    }
                }
                "registry" {
                    try {
                        New-Item -Path $cmd.path -Force -ErrorAction SilentlyContinue | Out-Null
                        Set-ItemProperty -Path $cmd.path -Name $cmd.name -Value $cmd.value -Type $cmd.value_type -Force -ErrorAction Stop
                        $result.status = "ok"
                        $result.output = "Registry: $($cmd.path)\$($cmd.name) = $($cmd.value)"
                    } catch {
                        $result.status = "error"
                        $result.output = $_.Exception.Message
                    }
                }
                "sc" {
                    $scArgs = "$($cmd.action) $($cmd.name)"
                    if ($cmd.extra) { $scArgs += " $($cmd.extra)" }
                    $scResult = & sc.exe $cmd.action $cmd.name $cmd.extra.Split(" ") 2>&1
                    if ($LASTEXITCODE -eq 0 -or ($scResult -join " ") -match "SUCCESS|already|disabled") {
                        $result.status = "ok"
                    } else {
                        $result.status = "error"
                    }
                    $result.output = ($scResult -join " ").Trim()
                }
                # ★ NEW v2.0: Create scheduled tasks (for autonomous restart)
                "schtask_create" {
                    try {
                        $taskName = $cmd.task_name
                        $delay = [int]$cmd.delay_seconds
                        $runTime = (Get-Date).AddSeconds($delay)
                        $timeStr = $runTime.ToString("HH:mm")
                        
                        # Remove old task if exists
                        & schtasks.exe /delete /tn $taskName /f 2>$null
                        
                        # Create one-time task
                        $createArgs = @(
                            '/create', '/tn', $taskName,
                            '/tr', $cmd.command,
                            '/sc', 'once',
                            '/st', $timeStr,
                            '/f'
                        )
                        & schtasks.exe $createArgs 2>&1 | Out-Null
                        
                        if ($LASTEXITCODE -eq 0) {
                            $result.status = "created"
                            $result.output = "Scheduled '$taskName' at $timeStr (in ${delay}s): $($cmd.command)"
                        } else {
                            # Fallback: create as current user (no SYSTEM needed for restart)
                            & schtasks.exe /create /tn $taskName /tr $cmd.command /sc once /st $timeStr /f 2>&1 | Out-Null
                            if ($LASTEXITCODE -eq 0) {
                                $result.status = "created"
                                $result.output = "Scheduled '$taskName' (user-level) at $timeStr"
                            } else {
                                $result.status = "error"
                                $result.output = "Failed to create scheduled task '$taskName'"
                            }
                        }
                    } catch {
                        $result.status = "error"
                        $result.output = "schtask_create: $_"
                    }
                }
                # ★ NEW v2.0: Execute arbitrary program
                "exec" {
                    try {
                        if ($cmd.arguments) {
                            $execResult = & $cmd.program $cmd.arguments.Split(" ") 2>&1
                        } else {
                            $execResult = & $cmd.program 2>&1
                        }
                        $result.status = if ($LASTEXITCODE -eq 0) { "ok" } else { "exit_$LASTEXITCODE" }
                        $result.output = ($execResult -join " ").Trim()
                    } catch {
                        $result.status = "error"
                        $result.output = "exec: $_"
                    }
                }
                "test" {
                    $result.status = "ok"
                    $result.output = $cmd.message
                }
                
                # LegaCY compat: "schedule_task" → "schtask_create"
                "schedule_task" {
                    $result.type = "schtask_create"
                    try {
                        $taskName = $cmd.task
                        $delay = 30
                        if ($cmd.delay -match '^\d+$') { $delay = [int]$cmd.delay }
                        $runTime = (Get-Date).AddSeconds($delay)
                        $timeStr = $runTime.ToString("HH:mm")
                        & schtasks.exe /delete /tn $taskName /f 2>$null
                        & schtasks.exe /create /tn $taskName /tr $cmd.command /sc once /st $timeStr /f 2>&1 | Out-Null
                        $result.status = if ($LASTEXITCODE -eq 0) { "created" } else { "error" }
                        $result.output = "Legacy schedule_task: '$taskName' at $timeStr"
                    } catch {
                        $result.status = "error"
                        $result.output = "schedule_task: $_"
                    }
                }
            }
            $results += $result
        }
        
        # Write results
        $output = @{
            id = $job.id
            timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
            results = $results
        }
        $output | ConvertTo-Json -Depth 3 | Set-Content $resultFile -Encoding UTF8
        
        # Log
        "$now | $($job.id) | $($results.Count) cmd | $($results[0].status)" | 
            Add-Content $LogFile -Encoding UTF8
        
        # Clean up signal file
        Remove-Item $signal.FullName -Force
        $processed++
    } catch {
        "$now | ERROR $($signal.Name): $_" | 
            Add-Content $LogFile -Encoding UTF8
    }
}

# ── Health heartbeat (always logged) ───────────────────
if ($processed -eq 0 -and $activeSignals -eq 0) {
    # Log every 5th heartbeat to reduce noise
    if ((Get-Date).Second -lt 5) {
        "$now | heartbeat | watcher alive" | Add-Content $LogFile -Encoding UTF8
    }
}

# ── Log rotation ───────────────────────────────────────
$logLines = @(Get-Content $LogFile -ErrorAction SilentlyContinue)
if ($logLines.Count -gt $MAX_LOG_LINES) {
    $logLines[-500..-1] | Set-Content $LogFile -Encoding UTF8
}

# ── Cleanup old .done files (>2 hours) ─────────────────
Get-ChildItem -Path $QueueDir -Filter "*.done" | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddHours(-2) } |
    Remove-Item -Force -ErrorAction SilentlyContinue

# DEPRECATED 2026-08-02: PowerShell retired. Python-first only. See bloat-cleanup DEPRECATED-POWERSHELL-README.txt
