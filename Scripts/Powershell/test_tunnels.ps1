# Test if the tunnels are accessible
Write-Host "Testing tunnel endpoints..."

# Test LDAP tunnel
Write-Host "Testing LDAP tunnel (localhost:33389):"
try {
    $ldapTest = New-Object System.Net.Sockets.TcpClient
    $ldapTest.Connect("localhost", 33389)
    Write-Host "LDAP tunnel: SUCCESS"
    $ldapTest.Close()
} catch {
    Write-Host "LDAP tunnel: FAILED - $($_.Exception.Message)"
}

# Test Kerberos tunnel
Write-Host "Testing Kerberos tunnel (localhost:30088):"
try {
    $kerbTest = New-Object System.Net.Sockets.TcpClient
    $kerbTest.Connect("localhost", 30088)
    Write-Host "Kerberos tunnel: SUCCESS"
    $kerbTest.Close()
} catch {
    Write-Host "Kerberos tunnel: FAILED - $($_.Exception.Message)"
}

# Test WinRM tunnel
Write-Host "Testing WinRM tunnel (localhost:35985):"
try {
    $winrmTest = New-Object System.Net.Sockets.TcpClient
    $winrmTest.Connect("localhost", 35985)
    Write-Host "WinRM tunnel: SUCCESS"
    $winrmTest.Close()
} catch {
    Write-Host "WinRM tunnel: FAILED - $($_.Exception.Message)"
}

# Show job status
Write-Host "Job status:"
Get-Job | Format-Table Id, Name, State, HasMoreData
