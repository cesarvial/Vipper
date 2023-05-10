# echo-client.py
import time
import socket

HOST = "192.168.100.200"  # The server's hostname or IP address
PORT = 1775  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while(1):
        print(s.recv(9))
        time.sleep(1)
        s.sendall(bytes(b'\x00\x01\x02\x03\x04\x05\x06'))
        
