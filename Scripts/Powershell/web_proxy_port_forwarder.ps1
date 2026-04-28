# Simple HTTP proxy to tunnel traffic
Write-Host "Starting HTTP proxy for tunneling..."

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://127.0.0.1:8080/")
$listener.Start()

Write-Host "HTTP proxy listening on http://127.0.0.1:8080"

while ($true) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    
    try {
        # Parse the request to extract target
        $url = $request.Url.AbsoluteUri
        Write-Host "Request: $url"
        
        # Forward to target (DC2)
        if ($url -match "ldap") {
            $targetHost = "192.168.2.2"
            $targetPort = 389
        } elseif ($url -match "kerberos") {
            $targetHost = "192.168.2.2"
            $targetPort = 88
        } elseif ($url -match "winrm") {
            $targetHost = "192.168.2.2"
            $targetPort = 5985
        } else {
            $response.StatusCode = 404
            $response.Close()
            continue
        }
        
        # Create TCP client to target
        $targetClient = New-Object System.Net.Sockets.TcpClient
        $targetClient.Connect($targetHost, $targetPort)
        
        # Stream data between client and target
        $clientStream = $request.InputStream
        $targetStream = $targetClient.GetStream()
        
        $buffer = New-Object byte[] 4096
        $bytesRead = 0
        
        while (($bytesRead = $clientStream.Read($buffer, 0, $buffer.Length)) -gt 0) {
            $targetStream.Write($buffer, 0, $bytesRead)
        }
        
        $targetStream.Close()
        $targetClient.Close()
        
        $response.StatusCode = 200
        $response.Close()
        
    } catch {
        $response.StatusCode = 500
        $response.Close()
        Write-Host "Error: $($_.Exception.Message)"
    }
}
