$ErrorActionPreference = "Continue"
$token = $env:CF_API_TOKEN
$accountId = (Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/accounts" -Headers @{"Authorization"="Bearer $token"}).result[0].id
$dbId = "70a58cb3-b2cd-498d-877f-ecca86859a22"
$apiUrl = "https://api.cloudflare.com/client/v4/accounts/$accountId/d1/database/$dbId/query"
$headers = @{"Authorization"="Bearer $token"; "Content-Type"="application/json"}

Write-Output "=== Updating D1 body_md from recovered papers ==="

$papers = Get-Content zenodo_papers_d1.json -Raw | ConvertFrom-Json
$papersDir = "recovered_papers"
$success = 0
$fail = 0
$missing = 0
$total = $papers.Count

for ($i = 0; $i -lt $total; $i++) {
    $p = $papers[$i]
    $identifier = $p.identifier
    $safeName = $identifier -replace '[\\/:*?"<>|]', '_'
    $filePath = Join-Path $papersDir "${safeName}.md"
    
    if (-not (Test-Path $filePath)) {
        Write-Output "MISS: [$($i+1)/$total] $identifier"
        $missing++
        continue
    }
    
    try {
        $content = Get-Content $filePath -Raw -Encoding UTF8
        $size = $content.Length
        
        if ($size -gt 900000) {
            Write-Output "SKIP: [$($i+1)/$total] $identifier -- ${size}B too large"
            $missing++
            continue
        }
        
        $r2Key = "papers/${safeName}.md"
        
        # Build JSON and write to temp file to avoid PowerShell encoding issues
        $body = @{sql="UPDATE papers SET body_md = ?, r2_key = ?, updated_at = datetime('now') WHERE identifier = ?"; params=@($content, $r2Key, $identifier)} | ConvertTo-Json -Depth 3
        $tmpFile = "temp_d1_update.json"
        [System.IO.File]::WriteAllText($tmpFile, $body, [System.Text.UTF8Encoding]::new($false))
        
        $r = Invoke-RestMethod -Uri $apiUrl -Method POST -Headers $headers -InFile $tmpFile -TimeoutSec 60
        
        if ($r.success) {
            Write-Output "OK: [$($i+1)/$total] $identifier -- ${size}B"
            $success++
        } else {
            Write-Output "ERR: [$($i+1)/$total] $identifier -- $($r.errors[0].message)"
            $fail++
        }
        
        Remove-Item $tmpFile -Force -ErrorAction SilentlyContinue
        
    } catch {
        $errMsg = $_.Exception.Message
        if ($errMsg.Length -gt 150) { $errMsg = $errMsg.Substring(0, 150) }
        Write-Output "ERR: [$($i+1)/$total] $identifier -- $errMsg"
        $fail++
    }
    
    if (($i+1) % 15 -eq 0) {
        Write-Output "Progress: $($i+1)/$total -- OK:$success FAIL:$fail MISS:$missing"
    }
    
    Start-Sleep -Milliseconds 200
}

Write-Output "=== COMPLETE: $total papers -- OK:$success FAIL:$fail MISS:$missing ==="
Remove-Item temp_d1_update.json -Force -ErrorAction SilentlyContinue
exit ($fail -gt 0)
