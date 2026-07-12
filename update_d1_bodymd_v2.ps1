$ErrorActionPreference = "Continue"
$token = $env:CF_API_TOKEN
$accountId = (Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/accounts" -Headers @{"Authorization"="Bearer $token"}).result[0].id
$dbId = "70a58cb3-b2cd-498d-877f-ecca86859a22"
$apiUrl = "https://api.cloudflare.com/client/v4/accounts/$accountId/d1/database/$dbId/query"
$headers = @{"Authorization"="Bearer $token"; "Content-Type"="application/json"}
$tmpFile = "body.json"

Write-Output "=== Updating D1 body_md (direct SQL escaping) ==="

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
        Write-Output "MISS: [$($i+1)/$total] $identifier -- no file"
        $missing++
        continue
    }
    
    try {
        $contentRaw = [System.IO.File]::ReadAllText($filePath, [System.Text.UTF8Encoding]::new($false))
        $size = $contentRaw.Length
        
        if ($size -gt 900000) {
            Write-Output "SKIP: [$($i+1)/$total] $identifier -- ${size}B too large"
            $missing++
            continue
        }
        
        # Escape single quotes for SQL
        $escaped = $contentRaw -replace "'", "''"
        # Remove null bytes that break SQL
        $escaped = $escaped -replace "`0", ""
        
        $r2Key = "papers/${safeName}.md"
        
        $sql = "UPDATE papers SET body_md = '" + $escaped + "', r2_key = '" + $r2Key + "', updated_at = datetime('now') WHERE identifier = '" + $identifier + "'"
        $body = @{sql=$sql} | ConvertTo-Json
        
        $utf8NoBom = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllText($tmpFile, $body, $utf8NoBom)
        
        $r = Invoke-RestMethod -Uri $apiUrl -Method POST -Headers $headers -InFile $tmpFile -TimeoutSec 60
        
        if ($r.success) {
            Write-Output "OK: [$($i+1)/$total] $identifier -- ${size}B"
            $success++
        } else {
            $errMsg = ($r.errors | Select-Object -First 1).message
            Write-Output "ERR: [$($i+1)/$total] $identifier -- $errMsg"
            $fail++
        }
        
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
Remove-Item $tmpFile -Force -ErrorAction SilentlyContinue
exit ($fail -gt 0)
