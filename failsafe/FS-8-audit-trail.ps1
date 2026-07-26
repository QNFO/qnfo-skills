# FS-8: Audit Trail
# Structured audit logging for all skill file modifications.
# Records who (session), what (skill), when (timestamp), and delta (size/hash).
# Writes to a JSONL audit log for easy parsing and analysis.
#
# Usage: .\FS-8-audit-trail.ps1 -TargetPath <path> -SessionId <id> -AgentModel <model> [-Delta <bytes>] [-Action <action>]
# Appends one record to the audit log.

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetPath,
    
    [Parameter(Mandatory=$true)]
    [string]$SessionId,
    
    [string]$AgentModel = "deepseek-v4-pro",
    
    [ValidateSet("write","edit","delete","restore","backup","sync","integrity-check")]
    [string]$Action = "edit",
    
    [long]$Delta = 0,
    
    [string]$AuditLog = "$PSScriptRoot\..\logs\audit.jsonl",
    
    [string]$Notes = ""
)

function Write-AuditRecord {
    param(
        [string]$TargetPath, [string]$SessionId, [string]$AgentModel,
        [string]$Action, [long]$Delta, [string]$AuditLog, [string]$Notes
    )
    
    # Extract skill name
    $skillName = ""
    if ($TargetPath -match '\\([^\\]+)\\SKILL\.md$') {
        $skillName = $matches[1]
    } else {
        $skillName = "unknown"
    }
    
    # File state
    $fileSize = 0
    $fileHash = ""
    if (Test-Path $TargetPath) {
        $fileSize = (Get-Item $TargetPath).Length
        $fileHash = (Get-FileHash $TargetPath -Algorithm SHA256).Hash
    }
    
    $record = @{
        Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffK"
        SessionId = $SessionId
        AgentModel = $AgentModel
        Skill = $skillName
        TargetPath = $TargetPath
        Action = $Action
        FileSize = $fileSize
        FileHash = $fileHash
        SizeDelta = $Delta
        Notes = $Notes
        Hostname = $env:COMPUTERNAME
        User = $env:USERNAME
    }
    
    # Ensure log directory and ensure JSONL
    $logDir = Split-Path $AuditLog -Parent
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    
    $jsonLine = $record | ConvertTo-Json -Compress -Depth 3
    Add-Content -Path $AuditLog -Value $jsonLine -Encoding UTF8
    
    Write-Output "[FS-8] AUDIT: $Action | $skillName | $fileSize bytes | session=$SessionId"
    
    return $record
}

# Main
Write-AuditRecord -TargetPath $TargetPath -SessionId $SessionId -AgentModel $AgentModel `
    -Action $Action -Delta $Delta -AuditLog $AuditLog -Notes $Notes
exit 0
