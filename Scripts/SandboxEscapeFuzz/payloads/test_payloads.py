import socket
import sys
import json
import os

# Configuration
HOST = '83.136.252.13'
PORT = 39615

# Read payloads from not_tested.txt
payloads = []
try:
    with open('not_tested.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                payloads.append({"payload": line, "tested": False})
except FileNotFoundError:
    print("Error: not_tested.txt file not found")
    sys.exit(1)

# Load existing tested payloads if file exists
tested_payloads = []
if os.path.exists('tested.json'):
    try:
        with open('tested.json', 'r') as f:
            tested_payloads = json.load(f)
    except json.JSONDecodeError:
        print("Warning: tested.json exists but is not valid JSON. Creating new file.")

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)  # Set timeout for connections

for i, payload in enumerate(payloads):
    try:
        # Connect to server
        sock.connect((HOST, PORT))
        
        # Send payload
        sock.sendall(payload['payload'].encode('utf-8'))
        
        # Receive response
        response = sock.recv(1024).decode('utf-8', errors='ignore')
        
        # Print results
        print(f"\nTest #{i+1}")
        print(f"Payload: {payload['payload']}")
        print(f"Response: {response}")
        
        # Mark payload as tested and add response
        payload["tested"] = True
        payload["response"] = response
        
        # Add to tested payloads
        tested_payloads.append(payload)
        
        # Write updated tested payloads to file after each test
        with open('tested.json', 'w') as f:
            json.dump(tested_payloads, f, indent=2)
            
    except Exception as e:
        print(f"Error with payload {i+1}: {str(e)}")
        continue
    finally:
        sock.close()

print(f"\nTesting complete. {len(tested_payloads)} payloads tested and saved to tested.json")
