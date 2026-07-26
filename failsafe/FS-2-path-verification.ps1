# FS-2: Path Verification
# Validates that the target path is a legitimate tracked skill file before any write.
# Prevents the corruption vector: unguarded write targeting wrong path.
#
# Usage: .\FS-2-path-verification.ps1 -TargetPath <path> [-SkillRoot <dir>] [-RepoRoot <dir>]
# Returns: exit 0 if valid skill path, exit 1 if rejected

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetPath,
    
    [string]$SkillRoot = "$env:USERPROFILE\.deepchat\skills",
    [string]$RepoRoot = "$PSScriptRoot\.."
)

# Known skill allowlist (from qnfo-skills repo ADR-026)
$TRACKED_SKILLS = @(
    "cloudflare", "code", "code-review", "deepchat-settings",
    "doc-coauthoring", "documents", "frontend-design", "git-commit",
    "git-github", "infographic-syntax-creator", "kaizen-skill-fixes",
    "knowledge", "mcp-builder", "qnfo-agent", "research", "system", "xlsx"
)

# Additional installed-only skills (not in repo but valid targets)
$INSTALLED_ONLY_SKILLS = @(
    "algorithmic-art", "docx", "memory-management", "pdf", "pptx",
    "skill-creator", "web-artifacts-builder"
)

$ALL_VALID_SKILLS = $TRACKED_SKILLS + $INSTALLED_ONLY_SKILLS

function Test-ValidSkillPath {
    param([string]$TargetPath, [string]$SkillRoot)
    
    # Must end with SKILL.md
    if ($TargetPath -notmatch 'SKILL\.md$') {
        Write-Error "[FS-2] REJECT: Target is not a SKILL.md file: $TargetPath"
        return $false
    }
    
    # Extract skill name from path
    $resolved = Resolve-Path $TargetPath -ErrorAction SilentlyContinue
    if (-not $resolved) {
        # File doesn't exist yet -- check if parent dir matches a valid skill
        $parent = Split-Path $TargetPath -Parent
        $skillName = Split-Path $parent -Leaf
        
        if ($skillName -in $ALL_VALID_SKILLS) {
            Write-Output "[FS-2] OK: New SKILL.md for known skill: $skillName (file does not exist yet)"
            return $true
        }
        Write-Error "[FS-2] REJECT: Unknown skill directory: $skillName"
        return $false
    }
    
    # File exists -- verify it's under a valid skill directory
    $pathStr = $resolved.ToString()
    foreach ($skill in $ALL_VALID_SKILLS) {
        if ($pathStr -match "\\$skill\\SKILL\.md$") {
            Write-Output "[FS-2] OK: Valid skill path: $skill"
            return $true
        }
    }
    
    Write-Error "[FS-2] REJECT: Path not under any known skill directory: $pathStr"
    return $false
}

# Main
$valid = Test-ValidSkillPath -TargetPath $TargetPath -SkillRoot $SkillRoot
if ($valid) {
    Write-Output "PATH_VERIFIED=true"
    exit 0
} else {
    Write-Output "PATH_VERIFIED=false"
    exit 1
}
