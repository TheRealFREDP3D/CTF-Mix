import socket
import sys
import threading

def create_listener(port):
    # Create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to all interfaces
    server.bind(('0.0.0.0', port))
    
    # Start listening
    server.listen(5)
    print(f'[*] Listening on 0.0.0.0:{port}')
    
    try:
        while True:
            client, addr = server.accept()
            print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')
            
            # Handle client connection in a new thread
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()
    except KeyboardInterrupt:
        print('\n[*] Shutting down listener...')
        server.close()
        sys.exit()

def handle_client(client_socket):
    try:
        while True:
            # Receive data
            request = client_socket.recv(4096)
            if not request:
                break
            print(request.decode('utf-8', errors='ignore'), end='')
            
            # Get command input
            command = input('') + '\n'
            if command.strip().lower() == 'exit':
                break
                
            # Send command
            client_socket.send(command.encode())
    except:
        pass
    finally:
        print('[*] Connection closed')
        client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <port>')
        sys.exit(1)
        
    port = int(sys.argv[1])
    create_listener(port)
