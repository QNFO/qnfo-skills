# FS-5-Install.ps1 -- Install the pre-commit hook into the qnfo-skills repo
# Copies FS-5-pre-commit-hook.ps1 to .git/hooks/pre-commit
#
# Usage: .\FS-5-Install.ps1 [-RepoRoot <dir>] [-Force]

param(
    [string]$RepoRoot = "$PSScriptRoot\..",
    [switch]$Force
)

$hookScript = Join-Path $PSScriptRoot "FS-5-pre-commit-hook.ps1"
$hookTarget = Join-Path $RepoRoot ".git\hooks\pre-commit"

# Verify we're in a git repo
if (-not (Test-Path (Join-Path $RepoRoot ".git"))) {
    Write-Error "Not a git repository: $RepoRoot"
    exit 1
}

# Check if hook already exists
if (Test-Path $hookTarget) {
    if ($Force) {
        Write-Output "Overwriting existing pre-commit hook..."
    } else {
        $existing = Get-Content $hookTarget -Raw
        if ($existing -match "FS-5") {
            Write-Output "FS-5 hook already installed. Use -Force to reinstall."
            exit 0
        }
        Write-Output "Existing pre-commit hook found (non-FS-5). Use -Force to overwrite."
        exit 1
    }
}

# Create the hook wrapper that invokes PowerShell
$hookContent = @"
#!/bin/sh
# FS-5: Encoding Integrity Pre-Commit Hook
# Installed by failsafe/FS-5-Install.ps1
# Blocks commits containing U+FFFD, U+FFFF, BOM, null bytes, or KIF-30 garbage.

echo "[FS-5] Running encoding integrity check..."

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$hookScript" -StagedOnly -RepoRoot "$RepoRoot"

exit $LASTEXITCODE
"@

Set-Content -Path $hookTarget -Value $hookContent -NoNewline

# Make executable on Unix-like systems (git bash on Windows)
try {
    & git update-index --chmod=+x .git/hooks/pre-commit 2>$null
} catch {}

Write-Output "[FS-5] Pre-commit hook installed: $hookTarget"
Write-Output "[FS-5] Hook will block commits containing U+FFFD, U+FFFF, BOM, null bytes, or KIF-30 garbage."
exit 0
