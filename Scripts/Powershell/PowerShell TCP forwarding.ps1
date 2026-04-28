# Fixed PowerShell TCP forwarding
Write-Host "Setting up PowerShell TCP forwarders..."

# LDAP (389) -> 192.168.2.2:389
$ldapJob = Start-Job -ScriptBlock {
    $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Any, 33389)
    $listener.Start()
    Write-Host "LDAP forwarder listening on port 33389"
    
    while ($true) {
        $client = $listener.AcceptTcpClient()
        $target = New-Object System.Net.Sockets.TcpClient
        try {
            $target.Connect("192.168.2.2", 389)
            $clientStream = $client.GetStream()
            $targetStream = $target.GetStream()
            
            # Simple bidirectional forwarding
            $buffer = New-Object byte[] 4096
            $clientToTarget = {
                param($src, $dst)
                $buf = New-Object byte[] 4096
                while (($bytes = $src.Read($buf, 0, $buf.Length)) -gt 0) {
                    $dst.Write($buf, 0, $bytes)
                    $dst.Flush()
                }
            }
            
            # Start forwarding in separate jobs
            $job1 = Start-Job -ScriptBlock $clientToTarget -ArgumentList $clientStream, $targetStream
            $job2 = Start-Job -ScriptBlock $clientToTarget -ArgumentList $targetStream, $clientStream
            
            # Wait for jobs to complete
            $job1 | Wait-Job
            $job2 | Wait-Job
            
        } catch {
            Write-Host "Error in LDAP forwarding: $($_.Exception.Message)"
        } finally {
            $client.Close()
            $target.Close()
        }
    }
}

# Kerberos (88) -> 192.168.2.2:88
$kerbJob = Start-Job -ScriptBlock {
    $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Any, 30088)
    $listener.Start()
    Write-Host "Kerberos forwarder listening on port 30088"
    
    while ($true) {
        $client = $listener.AcceptTcpClient()
        $target = New-Object System.Net.Sockets.TcpClient
        try {
            $target.Connect("192.168.2.2", 88)
            $clientStream = $client.GetStream()
            $targetStream = $target.GetStream()
            
            # Simple bidirectional forwarding
            $buffer = New-Object byte[] 4096
            $clientToTarget = {
                param($src, $dst)
                $buf = New-Object byte[] 4096
                while (($bytes = $src.Read($buf, 0, $buf.Length)) -gt 0) {
                    $dst.Write($buf, 0, $bytes)
                    $dst.Flush()
                }
            }
            
            # Start forwarding in separate jobs
            $job1 = Start-Job -ScriptBlock $clientToTarget -ArgumentList $clientStream, $targetStream
            $job2 = Start-Job -ScriptBlock $clientToTarget -ArgumentList $targetStream, $clientStream
            
            # Wait for jobs to complete
            $job1 | Wait-Job
            $job2 | Wait-Job
            
        } catch {
            Write-Host "Error in Kerberos forwarding: $($_.Exception.Message)"
        } finally {
            $client.Close()
            $target.Close()
        }
    }
}

# WinRM (5985) -> 192.168.2.2:5985
$winrmJob = Start-Job -ScriptBlock {
    $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Any, 35985)
    $listener.Start()
    Write-Host "WinRM forwarder listening on port 35985"
    
    while ($true) {
        $client = $listener.AcceptTcpClient()
        $target = New-Object System.Net.Sockets.TcpClient
        try {
            $target.Connect("192.168.2.2", 5985)
            $clientStream = $client.GetStream()
            $targetStream = $target.GetStream()
            
            # Simple bidirectional forwarding
            $buffer = New-Object byte[] 4096
            $clientToTarget = {
                param($src, $dst)
                $buf = New-Object byte[] 4096
                while (($bytes = $src.Read($buf, 0, $buf.Length)) -gt 0) {
                    $dst.Write($buf, 0, $bytes)
                    $dst.Flush()
                }
            }
            
            # Start forwarding in separate jobs
            $job1 = Start-Job -ScriptBlock $clientToTarget -ArgumentList $clientStream, $targetStream
            $job2 = Start-Job -ScriptBlock $clientToTarget -ArgumentList $targetStream, $clientStream
            
            # Wait for jobs to complete
            $job1 | Wait-Job
            $job2 | Wait-Job
            
        } catch {
            Write-Host "Error in WinRM forwarding: $($_.Exception.Message)"
        } finally {
            $client.Close()
            $target.Close()
        }
    }
}

Write-Host "PowerShell TCP forwarders started"
Write-Host "LDAP: localhost:33389 -> 192.168.2.2:389"
Write-Host "Kerberos: localhost:30088 -> 192.168.2.2:88"
Write-Host "WinRM: localhost:35985 -> 192.168.2.2:5985"

# Show running jobs
Get-Job
