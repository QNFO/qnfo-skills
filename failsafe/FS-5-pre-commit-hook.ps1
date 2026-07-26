# FS-5: Pre-Commit Hook
# Git pre-commit hook that blocks commits containing encoding corruption markers.
# Detects: U+FFFD, U+FFFF, BOM, null bytes, and KIF-30 duplication garbage.
# Install: copy to .git/hooks/pre-commit (or use FS-5-install.ps1)
#
# Usage (as git hook): automatically invoked by git commit
# Usage (standalone): .\FS-5-pre-commit-hook.ps1 [-StagedOnly] [-RepoRoot <dir>]

param(
    [switch]$StagedOnly,
    [string]$RepoRoot = "$PSScriptRoot\.."
)

$FORBIDDEN_PATTERNS = @(
    @{ Name = "U+FFFD Replacement Character"; Pattern = [char]0xFFFD; Severity = "BLOCK" },
    @{ Name = "U+FFFF Noncharacter"; Pattern = [char]0xFFFF; Severity = "BLOCK" },
    @{ Name = "Null Byte"; Pattern = [char]0x0000; Severity = "BLOCK" },
    @{ Name = "BOM (UTF-8)"; Pattern = [char]0xFEFF; Severity = "BLOCK" }
)

# Regex patterns for structural corruption
$STRUCTURAL_PATTERNS = @(
    @{ Name = "KIF-30 Duplication Garbage"; Pattern = "HARD GATE.*HARD GATE.*HARD GATE"; Severity = "BLOCK"; Description = "Detects KIF-30 section duplicated >2 times (indicates loop corruption)" },
    @{ Name = "Truncated frontmatter"; Pattern = "^---\s*\n(?!.*^---\s*\n)"; Severity = "WARN"; Description = "YAML frontmatter may be unclosed" }
)

function Test-EncodingIntegrity {
    param([string]$FilePath, [string]$Content)
    
    $issues = @()
    
    # Check for forbidden characters
    foreach ($fp in $FORBIDDEN_PATTERNS) {
        if ($Content.Contains($fp.Pattern)) {
            $count = ([regex]::Escape($fp.Pattern) | ForEach-Object { 
                ([regex]::Matches($Content, $_)).Count 
            })
            $issues += @{
                File = $FilePath
                Check = $fp.Name
                Severity = $fp.Severity
                Count = $count
            }
        }
    }
    
    # Check structural patterns
    foreach ($sp in $STRUCTURAL_PATTERNS) {
        $matches = [regex]::Matches($Content, $sp.Pattern)
        if ($matches.Count -gt 0) {
            $issues += @{
                File = $FilePath
                Check = $sp.Name
                Severity = $sp.Severity
                Count = $matches.Count
                Description = $sp.Description
            }
        }
    }
    
    return $issues
}

function Invoke-PreCommitHook {
    param([bool]$StagedOnly, [string]$RepoRoot)
    
    Set-Location $RepoRoot
    
    $files = @()
    
    if ($StagedOnly -or ($env:GIT_INDEX_FILE -or $env:GIT_DIR)) {
        # Running as git hook -- check staged files
        $staged = git diff --cached --name-only --diff-filter=ACM 2>&1
        if ($LASTEXITCODE -eq 0 -and $staged) {
            $files = $staged | Where-Object { $_ -match '\.md$|\.py$|\.ps1$|\.json$|\.yaml$|\.yml$' }
        }
    } else {
        # Standalone -- check all tracked skill files
        $files = Get-ChildItem -Path $RepoRoot -Recurse -Include "SKILL.md" | 
                 Where-Object { $_.Directory.Name -ne "failsafe" } |
                 ForEach-Object { $_.FullName.Replace($RepoRoot + "\", "").Replace("\", "/") }
    }
    
    if ($files.Count -eq 0) {
        Write-Output "[FS-5] No files to check."
        return @{ Passed = $true; Issues = @() }
    }
    
    $allIssues = @()
    $blockers = @()
    
    foreach ($file in $files) {
        $fullPath = Join-Path $RepoRoot $file
        if (-not (Test-Path $fullPath)) { continue }
        
        $content = Get-Content $fullPath -Raw -ErrorAction SilentlyContinue
        if (-not $content) { continue }
        
        $issues = Test-EncodingIntegrity -FilePath $file -Content $content
        foreach ($issue in $issues) {
            $allIssues += $issue
            if ($issue.Severity -eq "BLOCK") {
                $blockers += $issue
            }
        }
    }
    
    $totalFiles = ($files | Measure-Object).Count
    
    Write-Output "`n[FS-5] SCAN: $totalFiles files checked"
    
    if ($allIssues.Count -eq 0) {
        Write-Output "[FS-5] PASS: No encoding issues found."
        return @{ Passed = $true; Issues = @(); FilesChecked = $totalFiles }
    }
    
    foreach ($issue in $allIssues) {
        $icon = if ($issue.Severity -eq "BLOCK") { "BLOCK" } else { "WARN" }
        Write-Output "[FS-5] $icon : $($issue.File) -- $($issue.Check)"
    }
    
    if ($blockers.Count -gt 0) {
        Write-Output "`n[FS-5] BLOCKED: $($blockers.Count) blocking issues found. Commit rejected."
        Write-Output "[FS-5] Fix by: removing forbidden characters, restoring from clean backup."
        return @{ Passed = $false; Issues = $allIssues; Blockers = $blockers; FilesChecked = $totalFiles }
    }
    
    Write-Output "[FS-5] PASS with warnings: $($allIssues.Count) non-blocking issues."
    return @{ Passed = $true; Issues = $allIssues; FilesChecked = $totalFiles }
}

# Main
$result = Invoke-PreCommitHook -StagedOnly:$StagedOnly -RepoRoot $RepoRoot

# When running as git hook, exit non-zero to block commit
if (-not $result.Passed) {
    exit 1
}
exit 0
