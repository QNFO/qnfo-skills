# Search-Email.ps1 — General-purpose Outlook email search across all stores/folders
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File search-email.ps1 -Keyword "research" -MaxDays 21
param(
    [Parameter(Mandatory=$true)]
    [string]$Keyword,
    [int]$MaxDays = 21,
    [switch]$ShowBody,
    [int]$BodyMaxChars = 500,
    [switch]$ListAll
)

$outlook = New-Object -ComObject Outlook.Application
$ns = $outlook.GetNamespace('MAPI')
$cutoff = (Get-Date).AddDays(-$MaxDays)

function Search-Folders {
    param($folder, $depth = 0)
    
    if ($depth -gt 6) { return }
    if ($folder.Items.Count -eq 0) { return }
    
    try {
        $kwFilter = "@SQL=urn:schemas:httpmail:subject LIKE '%$Keyword%' OR urn:schemas:httpmail:textdescription LIKE '%$Keyword%'"
        $found = $folder.Items.Restrict($kwFilter)
        
        if ($found.Count -gt 0) {
            foreach ($item in $found) {
                $date = $null
                $isSent = $false
                try { $date = $item.ReceivedTime; $sender = $item.SenderName; $recipient = $item.To }
                catch { $date = $item.SentOn; $isSent = $true; $sender = $item.SenderName; $recipient = $item.To }
                
                if ($date -ge $cutoff -or $ListAll) {
                    $dateStr = $date.ToString('yyyy-MM-dd HH:mm')
                    $direction = if ($isSent) { "SENT" } else { "RECV" }
                    Write-Output "[$($folder.Name)] $direction | $sender -> $recipient | $($item.Subject) | $dateStr"
                    
                    if ($ShowBody) {
                        try {
                            $body = $item.Body
                            $preview = $body.Substring(0, [Math]::Min($BodyMaxChars, $body.Length))
                            Write-Output "  BODY: $preview"
                        } catch {}
                        if ($item.Attachments.Count -gt 0) {
                            Write-Output "  ATTACHMENTS: $($item.Attachments.Count)"
                            foreach ($att in $item.Attachments) {
                                Write-Output "    - $($att.FileName) ($($att.Size) bytes)"
                            }
                        }
                    }
                }
            }
        }
    } catch {}
    
    foreach ($sub in $folder.Folders) {
        Search-Folders -folder $sub -depth ($depth + 1)
    }
}

Write-Output "===== Email Search: '$Keyword' (last $MaxDays days) ====="
Write-Output ""

foreach ($store in $ns.Stores) {
    Write-Output "--- Store: $($store.DisplayName) ---"
    $root = $store.GetRootFolder()
    Search-Folders -folder $root
}

Write-Output ""
Write-Output "Done."

# DEPRECATED 2026-08-02: PowerShell retired. Python-first only. See bloat-cleanup DEPRECATED-POWERSHELL-README.txt
