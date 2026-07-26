# FS-3: Size Guard
# Blocks writes that would cause a SKILL.md to grow beyond safe thresholds.
# Prevents the corruption vector: 36KB -> 53.8MB blowup (1500x).
#
# Usage: .\FS-3-size-guard.ps1 -TargetPath <path> [-NewSize <bytes>]
# If NewSize is not provided, checks the file on disk after write.
# Returns: exit 0 if safe, exit 1 if blocked

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetPath,
    
    [long]$NewSize = 0,
    
    # Multiplier threshold: file cannot grow beyond this multiple of its original size
    [double]$MaxGrowthMultiplier = 3.0,
    
    # Absolute maximum size in bytes (default: 250KB -- all known skills are < 135KB)
    [long]$AbsoluteMaxBytes = 262144
)

function Test-SizeGuard {
    param([string]$TargetPath, [long]$NewSize, [double]$MaxGrowthMultiplier, [long]$AbsoluteMaxBytes)
    
    # If file doesn't exist pre-write, only apply absolute max
    if (-not (Test-Path $TargetPath)) {
        if ($NewSize -gt 0 -and $NewSize -gt $AbsoluteMaxBytes) {
            Write-Error "[FS-3] BLOCK: New file would be $NewSize bytes (max: $AbsoluteMaxBytes)"
            return $false
        }
        Write-Output "[FS-3] OK: New file, no size baseline. Absolute cap: $AbsoluteMaxBytes bytes"
        return $true
    }
    
    $originalSize = (Get-Item $TargetPath).Length
    
    # Pre-write check: if NewSize is provided, validate before writing
    if ($NewSize -gt 0) {
        if ($NewSize -gt $AbsoluteMaxBytes) {
            Write-Error "[FS-3] BLOCK: Proposed size $NewSize exceeds absolute max $AbsoluteMaxBytes"
            return $false
        }
        $ratio = [double]$NewSize / [double]$originalSize
        if ($ratio -gt $MaxGrowthMultiplier) {
            Write-Error "[FS-3] BLOCK: Proposed size is ${ratio}x original ($originalSize -> $NewSize). Max allowed: ${MaxGrowthMultiplier}x"
            return $false
        }
        Write-Output "[FS-3] OK: Pre-write size check passed ($originalSize -> $NewSize, ratio=$([math]::Round($ratio,2))x)"
        return $true
    }
    
    # Post-write check: verify file hasn't grown beyond thresholds
    $currentSize = (Get-Item $TargetPath).Length
    
    if ($currentSize -gt $AbsoluteMaxBytes) {
        Write-Error "[FS-3] ALERT: File $TargetPath is $currentSize bytes (max: $AbsoluteMaxBytes). RESTORE FROM BACKUP."
        return $false
    }
    
    $ratio = [double]$currentSize / [double]$originalSize
    if ($ratio -gt $MaxGrowthMultiplier) {
        Write-Error "[FS-3] ALERT: File grew ${ratio}x ($originalSize -> $currentSize). Max allowed: ${MaxGrowthMultiplier}x. RESTORE FROM BACKUP."
        return $false
    }
    
    Write-Output "[FS-3] OK: Post-write size check passed ($originalSize -> $currentSize, ratio=$([math]::Round($ratio,2))x)"
    return $true
}

# Main
$safe = Test-SizeGuard -TargetPath $TargetPath -NewSize $NewSize -MaxGrowthMultiplier $MaxGrowthMultiplier -AbsoluteMaxBytes $AbsoluteMaxBytes
if ($safe) {
    exit 0
} else {
    exit 1
}
