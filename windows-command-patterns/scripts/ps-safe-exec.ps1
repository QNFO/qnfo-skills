<#
.SYNOPSIS
    Safe PowerShell execution wrapper -- lints THEN executes.
    Fails fast if KIF-05/06/07 issues detected.
.DESCRIPTION
    Runs ps-lint.ps1 on the command FIRST. If KIF-05 or KIF-06 (HARD FAIL)
    are found, aborts with diagnostic and suggested fix. If KIF-09 (WARN)
    only, warns but proceeds. If clean, executes immediately.
.PARAMETER Command
    The PowerShell command to validate and execute.
.PARAMETER Strict
    Block on KIF-09 warnings too. Default: $false.
.PARAMETER NoExecute
    Validate only -- don't execute even if clean. Default: $false.
.EXAMPLE
    .\ps-safe-exec.ps1 -Command 'Get-ChildItem | Select-String "error|warn"'
    # BLOCKED: KIF-06 -- regex in double quotes
.EXAMPLE
    .\ps-safe-exec.ps1 'Get-ChildItem | Select-String ''error|warn'''
    # PASS -> executes
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Command,
    [switch]$Strict,
    [switch]$NoExecute
)

$skillRoot = Split-Path -Parent $PSScriptRoot
$lintScript = Join-Path $skillRoot "scripts\ps-lint.ps1"

if (-not (Test-Path $lintScript)) {
    Write-Host "[WARN] ps-lint.ps1 not found at $lintScript" -ForegroundColor Yellow
    Write-Host "[WARN] Executing without validation" -ForegroundColor Yellow
    Invoke-Expression $Command
    exit $LASTEXITCODE
}

# Run linter with JSON output. Use direct parameter binding (NOT splatting)
# because the command string may contain quotes that break argument parsing.
if ($Strict) {
    $lintOutput = & $lintScript -Command $Command -Json -Strict 2>&1 | Out-String
} else {
    $lintOutput = & $lintScript -Command $Command -Json 2>&1 | Out-String
}

try {
    $lintObj = $lintOutput | ConvertFrom-Json
} catch {
    Write-Host "[WARN] Lint output not valid JSON" -ForegroundColor Yellow
    Write-Host "[WARN] Executing without validation" -ForegroundColor Yellow
    Invoke-Expression $Command
    exit $LASTEXITCODE
}

# Check for HARD FAILS (KIF-05, KIF-06, KIF-07)
$hardFails = $lintObj.issues | Where-Object { $_.severity -eq "FAIL" }

if ($hardFails) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  PS-SAFE-EXEC: BLOCKED" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    foreach ($i in $hardFails) {
        Write-Host "  [$($i.kif)] $($i.category)" -ForegroundColor Red
        Write-Host "    Issue: $($i.found)"
        Write-Host "    Fix:   $($i.fix)" -ForegroundColor Cyan
        Write-Host ""
    }
    Write-Host "Command was NOT executed." -ForegroundColor Yellow
    exit 2
}

# Check for warnings (KIF-09 typically)
$warnings = $lintObj.issues | Where-Object { $_.severity -eq "WARN" }
if ($warnings) {
    Write-Host "[WARN] Pre-flight warnings:" -ForegroundColor Yellow
    foreach ($w in $warnings) {
        Write-Host "  [$($w.kif)] $($w.category): $($w.found)" -ForegroundColor Yellow
    }
}

if ($NoExecute) {
    Write-Host "[PASS] Validation only" -ForegroundColor Green
    exit 0
}

Write-Host "[PASS] Executing: $Command" -ForegroundColor Green
Write-Host ("-" * 60)

$ErrorActionPreference = "Continue"
try {
    Invoke-Expression $Command
    exit $LASTEXITCODE
} catch {
    Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
    exit 3
}

# DEPRECATED 2026-08-02: PowerShell retired. Python-first only. See bloat-cleanup DEPRECATED-POWERSHELL-README.txt
