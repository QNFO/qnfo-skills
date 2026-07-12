$ErrorActionPreference = "Continue"
$token = $env:ZENODO_TOKEN
$headers = @{ "Authorization" = "Bearer $token" }
$outDir = "recovered_papers"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$jsonContent = Get-Content zenodo_papers_d1.json -Raw -Encoding UTF8
$papers = $jsonContent | ConvertFrom-Json
$total = $papers.Count
$success = 0
$fail = 0
$nomd = 0
$log = @()

Write-Output "=== Starting download of $total papers from Zenodo ==="

for ($i = 0; $i -lt $total; $i++) {
    $p = $papers[$i]
    $doi = $p.zenodo_doi
    $identifier = $p.identifier
    
    if ($doi -match 'zenodo\.(\d+)') {
        $recordId = $Matches[1]
    } else {
        $log += "WARN: $identifier -- cannot parse DOI: $doi"
        $fail++
        continue
    }
    
    try {
        $recordUrl = "https://zenodo.org/api/records/$recordId"
        $record = Invoke-RestMethod -Uri $recordUrl -Headers $headers -TimeoutSec 30
        
        # Find paper.md or any .md file
        $paperMd = $null
        foreach ($f in $record.files) {
            if ($f.key -eq "paper.md" -or $f.key.EndsWith("/paper.md")) {
                $paperMd = $f
                break
            }
        }
        if (-not $paperMd) {
            foreach ($f in $record.files) {
                if ($f.key.EndsWith(".md")) {
                    $paperMd = $f
                    break
                }
            }
        }
        
        if ($paperMd) {
            # Use /content endpoint for download
            $downloadUrl = "https://zenodo.org/api/records/$recordId/files/$($paperMd.key)/content"
            $safeName = $identifier -replace '[\\/:*?"<>|]', '_'
            $outFile = Join-Path $outDir "${safeName}.md"
            
            Invoke-RestMethod -Uri $downloadUrl -Headers $headers -OutFile $outFile -TimeoutSec 60
            $size = (Get-Item $outFile).Length
            $log += "OK: [$($i+1)/$total] $identifier -- $size bytes"
            $success++
        } else {
            $fileKeys = ($record.files | ForEach-Object { $_.key }) -join ', '
            $log += "NOMD: [$($i+1)/$total] $identifier ($recordId) -- files: $fileKeys"
            $nomd++
        }
    } catch {
        $errMsg = $_.Exception.Message
        if ($errMsg.Length -gt 150) { $errMsg = $errMsg.Substring(0, 150) }
        $log += "ERR: [$($i+1)/$total] $identifier ($recordId) -- $errMsg"
        $fail++
    }
    
    if (($i+1) % 10 -eq 0) {
        Write-Output "Progress: $($i+1)/$total -- OK:$success FAIL:$fail NOMD:$nomd"
    }
    
    Start-Sleep -Milliseconds 200
}

Write-Output "=== COMPLETE: $total papers -- OK:$success FAIL:$fail NOMD:$nomd ==="
$log -join "`n" | Out-File -FilePath "zenodo_download_log.txt" -Encoding UTF8
Write-Output "Log saved to zenodo_download_log.txt"
Write-Output "Papers saved to $outDir/"
exit $fail
