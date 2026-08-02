<#
.SYNOPSIS
    Pre-flight validator for PowerShell commands -- catches KIF-05 through KIF-09
    BEFORE execution. Returns structured JSON with issues found and suggested fixes.
.DESCRIPTION
    Checks a PowerShell command string against all KIF patterns documented in
    windows-command-patterns/SKILL.md. Design goal: ZERO false positives.
    If it flags something, the command WILL fail if executed as-is.
.PARAMETER Command
    The PowerShell command string to validate.
.PARAMETER Strict
    When true, KIF-09 (complex one-liner) warnings become FAIL. Default: $false.
.PARAMETER Json
    Output structured JSON instead of human text. Default: $false.
.EXAMPLE
    .\ps-lint.ps1 'Select-String -Pattern "(a|b)" file.txt'
    # KIF-06 FAIL: double-quoted regex with | alternation
.EXAMPLE
    .\ps-lint.ps1 'dir C:\ & echo done' -Strict -Json
    # KIF-05 FAIL + KIF-09 FAIL; JSON output
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Command,
    [switch]$Strict,
    [switch]$Json
)

$issues = @()
$severity = "PASS"

# ============================================================================
# KIF-05: UNIX SHELL OPERATORS -- & (as separator), ||, &&
# ============================================================================

# && -- always invalid in PowerShell
if ($Command -match '&&') {
    $severity = "FAIL"
    $issues += @{ kif="KIF-05"; severity="FAIL"; category="Shell Mismatch"
        found='&& (Unix AND -- invalid in PowerShell)'
        fix='Use ; for unconditional chaining, or cmd /c "cmd1 && cmd2" for conditional exec' }
}

# || -- always invalid
if ($Command -match '\|\|') {
    $severity = "FAIL"
    $issues += @{ kif="KIF-05"; severity="FAIL"; category="Shell Mismatch"
        found='|| (Unix OR -- invalid in PowerShell)'
        fix='Use cmd /c "cmd1 || cmd2" or if (-not (cmd1)) { cmd2 }' }
}

# & as separator: & followed by non-variable, non-brace, non-quoted text
# Valid call operator: & $var, & {block}, & "path", & 'path' -- these are fine
$ampMatches = [regex]::Matches($Command, '\s+&\s+(\S+)')
foreach ($m in $ampMatches) {
    $after = $m.Groups[1].Value
    if ($after -notmatch '^[\$\{\"''"]') {
        $severity = "FAIL"
        $issues += @{ kif="KIF-05"; severity="FAIL"; category="Shell Mismatch"
            found="& $after (intended as separator, but & is the PS call operator)"
            fix="Replace & with ; -- ; is the PowerShell command separator" }
        break
    }
}

# ============================================================================
# KIF-06: QUOTE LAYER COLLAPSE -- #1 most recurring error
# ============================================================================
$kif06 = @()

# -Pattern "regex|with|pipe"
$m1 = [regex]::Matches($Command, '-[Pp]attern\s+"([^"]*\|[^"]*)"')
foreach ($m in $m1) { $kif06 += "-Pattern `"$($m.Groups[1].Value)`" -- | inside double quotes becomes PS pipe" }

# Select-String "regex|..." without -Pattern
$m2 = [regex]::Matches($Command, 'Select-String\s+"([^"]*\|[^"]*)"')
foreach ($m in $m2) { $kif06 += "Select-String `"$($m.Groups[1].Value)`" -- regex in double quotes, | will become pipe" }

# -replace "regex|with|pipe"
$m3 = [regex]::Matches($Command, '-replace\s+"([^"]*\|[^"]*)"')
foreach ($m in $m3) { $kif06 += "-replace `"$($m.Groups[1].Value)`" -- regex in double quotes, | will become pipe" }

# Generic double-quoted regex: "(alt1|alt2)" pattern
$m4 = [regex]::Matches($Command, '"([^"]*\([^)]*\|[^)]*\)[^"]*)"')
foreach ($m in $m4) {
    $v = $m.Groups[1].Value
    if ($kif06 -notmatch [regex]::Escape($v)) {
        $kif06 += "`"$v`" -- regex alternation ()| inside double quotes"
    }
}

if ($kif06.Count -gt 0) {
    $severity = "FAIL"
    $issues += @{ kif="KIF-06"; severity="FAIL"; category="Quote Layer Collapse"
        found=($kif06 -join ' | ')
        fix="Replace DOUBLE quotes with SINGLE quotes around regex patterns. Single-quoted strings in PS are LITERAL -- | is never interpreted as pipe." }
}

# ============================================================================
# KIF-07: PIPELINE VARIABLE OMISSION -- {.Property} without $_
# ============================================================================
$eBlocks = [regex]::Matches($Command, 'E\s*=\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}')
$kif07 = @()
foreach ($block in $eBlocks) {
    $body = $block.Groups[1].Value
    # Body has .Property access but no $_ anywhere -> violation
    if ($body -match '\.(\w+)' -and $body -notmatch '\$_') {
        $kif07 += "E={$body`} -- member access .Property without `$_ in script block"
    }
}
if ($kif07.Count -gt 0) {
    $severity = "FAIL"
    $issues += @{ kif="KIF-07"; severity="FAIL"; category="Pipeline Variable Omission"
        found=($kif07 -join ' | ')
        fix="Add `$_ before .Property: use {`$_.Used/1GB} not {.Used/1GB}" }
}

# ============================================================================
# KIF-09: COMPLEX ONE-LINER -- should be a .ps1 file
# ============================================================================
$kif09 = @()
$pipes = ([regex]::Matches($Command, '\|')).Count
if ($pipes -gt 2) { $kif09 += "$pipes pipe stages (>2 threshold)" }

$vars = ([regex]::Matches($Command, '\$\w+\s*=')).Count
if ($vars -gt 0) { $kif09 += "$vars variable assignment(s)" }

if ($Command -match 'ConvertFrom-Json') { $kif09 += "ConvertFrom-Json in one-liner" }

$calc = ([regex]::Matches($Command, '@\{[NE]\s*=')).Count
if ($calc -gt 0) { $kif09 += "$calc calculated property/ies" }

if ($Command -match '"' -and $Command -match "'") { $kif09 += "Mixed quoting (single+double)" }

if ($kif09.Count -gt 0) {
    $sev = if ($Strict) { "FAIL" } else { "WARN" }
    if ($severity -eq "PASS") { $severity = $sev }
    $issues += @{ kif="KIF-09"; severity=$sev; category="Complex One-Liner"
        found=($kif09 -join '; ')
        fix="Write a .ps1 file instead. Multi-pipe/variable/JSON one-liners fail from quote collapse, scoping, and pipeline quirks. A .ps1 file is a SINGLE interpretation layer -- no errors." }
}

# ============================================================================
# OUTPUT
# ============================================================================
if ($Json) {
    $result = @{ severity=$severity; issues=$issues; command=$Command; timestamp=(Get-Date -Format 'o') }
    ConvertTo-Json -InputObject $result -Depth 4 -Compress
} elseif ($issues.Count -eq 0) {
    Write-Host "[PASS] Clean -- no KIF-05/06/07/09 issues detected" -ForegroundColor Green
} else {
    $label = if ($severity -eq 'FAIL') { 'FAIL' } else { "PASS (with $($issues.Count) warning(s))" }
    $color = if ($severity -eq 'FAIL') { 'Red' } else { 'Yellow' }
    Write-Host "[$label]" -ForegroundColor $color
    foreach ($i in $issues) {
        $ic = if ($i.severity -eq 'FAIL') { 'Red' } else { 'Yellow' }
        Write-Host "  [$($i.kif)] $($i.category)" -ForegroundColor $ic
        Write-Host "    Found: $($i.found)"
        Write-Host "    Fix:   $($i.fix)" -ForegroundColor Cyan
    }
}

exit $(if ($severity -eq "PASS") { 0 } elseif ($severity -eq "WARN") { 1 } else { 2 })

# DEPRECATED 2026-08-02: PowerShell retired. Python-first only. See bloat-cleanup DEPRECATED-POWERSHELL-README.txt
