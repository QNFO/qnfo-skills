$ErrorActionPreference = "Continue"
$token = $env:CF_API_TOKEN
$accountId = (Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/accounts" -Headers @{"Authorization"="Bearer $token"}).result[0].id

Write-Output "Account ID: $accountId"
Write-Output "Uploading recovered papers to R2 bucket qnfo..."

$papersDir = "recovered_papers"
$files = Get-ChildItem $papersDir -Filter "*.md"
$total = $files.Count
$success = 0
$fail = 0
$log = @()

Write-Output "=== Uploading $total markdown files to R2 ==="

$i = 0
foreach ($f in $files) {
    $i++
    $objectKey = "papers/" + $f.Name
    
    try {
        $content = [System.IO.File]::ReadAllBytes($f.FullName)
        $body = $content
        
        $url = "https://api.cloudflare.com/client/v4/accounts/$accountId/r2/buckets/qnfo/objects/$objectKey"
        $headers = @{
            "Authorization" = "Bearer $token"
            "Content-Type" = "application/octet-stream"
        }
        
        $r = Invoke-RestMethod -Uri $url -Method PUT -Headers $headers -Body $body -TimeoutSec 30
        $log += "OK: [$i/$total] $objectKey"
        $success++
    } catch {
        $errMsg = $_.Exception.Message
        if ($errMsg.Length -gt 150) { $errMsg = $errMsg.Substring(0, 150) }
        $log += "ERR: [$i/$total] $objectKey -- $errMsg"
        $fail++
    }
    
    if ($i % 20 -eq 0) {
        Write-Output "Progress: $i/$total -- OK:$success FAIL:$fail"
    }
    
    Start-Sleep -Milliseconds 100
}

Write-Output "=== COMPLETE: $total files -- OK:$success FAIL:$fail ==="
$log -join "`n" | Out-File -FilePath "r2_upload_log.txt" -Encoding UTF8
Write-Output "Log saved to r2_upload_log.txt"
exit $fail
