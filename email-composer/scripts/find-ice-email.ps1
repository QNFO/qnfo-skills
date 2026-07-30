try {
    $o = New-Object -ComObject Outlook.Application
    $ns = $o.GetNamespace('MAPI')
    
    $accts = $ns.Accounts | ForEach-Object { $_.SmtpAddress }
    Write-Output "Accounts: $($accts.Count)"
    $accts | ForEach-Object { Write-Output "  - $_" }
    
    # Get rowan.quni@outlook.com's inbox explicitly
    $account = $ns.Accounts | Where-Object { $_.SmtpAddress -eq 'rowan.quni@outlook.com' }
    Write-Output "Using account: $($account.SmtpAddress)"
    
    $store = $ns.Stores | Where-Object { $_.DisplayName -match 'rowan' }
    Write-Output "Store: $($store.DisplayName)"
    
    if ($store) {
        $folder = $store.GetRootFolder().Folders | Where-Object { $_.Name -eq 'Inbox' }
        if (-not $folder) { $folder = $ns.GetDefaultFolder(6) }
    } else {
        $folder = $ns.GetDefaultFolder(6)
    }
    
    $items = $folder.Items.Restrict("[SenderName] = 'Project'")
    Write-Output "`nIce emails found: $($items.Count)"
    $items | ForEach-Object { 
        Write-Output "  - From: $($_.SenderName) | Subject: $($_.Subject) | Received: $($_.ReceivedTime)"
    }
    
    if ($items.Count -gt 0) {
        $mail = $items.Item(1)
        Write-Output "Selected: $($mail.Subject) from $($mail.SenderName)"
        
        # Create new mail item from scratch (avoids 'inline response' error)
        $newMail = $o.CreateItem(0)
        $newMail.To = "ice@techinbridge.com"
        $newMail.Subject = "Re: Opportunity Sharing: Recommended Innovation Competition Suitable for Your Ongoing Project"
        $newMail.HTMLBody = @"
<p>Dear Ice,</p>
<p>Thank you for the detailed and honest responses — I appreciate the transparency about Hebei's fabrication capabilities. An honest answer saves everyone time, and yours was exactly that.</p>
<p>After reviewing the Shijiazhuang competition against my current roadmap, I've concluded this isn't a fit at this stage. Let me be specific about why, since I think it may clarify what QWAV actually is for future opportunities.</p>
<p>QWAV is not a platform or service layer. It's a company building next-generation computing systems using thermodynamic, optical, and neuromorphic physical substrates — the kind of computation where the physics does the work directly, rather than being forced through a symbolic scaffold. This genuinely requires advanced fabrication infrastructure that Hebei doesn't currently have.</p>
<p>I value the connection with your team and the Foreign Expert Administration Division. When Hebei develops semiconductor fabrication capabilities, or when opportunities aligned with first-principles physical computing research arise, I would be very interested.</p>
<p>Thank you again for thinking of me, and for the honest back-and-forth.</p>
<p>Best regards,<br>Rowan</p>
"@
        $newMail.Display()
        Write-Output "`n✅ New mail window opened. Review and send manually."
    }
} catch {
    Write-Output "ERROR: $_"
    Write-Output $_.ScriptStackTrace
}
