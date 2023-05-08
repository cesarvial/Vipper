# Script to test the communication modules of the desktop app
import socket
import time
import random

def sensor_board():
    s = socket.socket()
    s.connect((socket.gethostname(), 8081))
    r = random.random()
    data = None
    while (1):
        time.sleep(0.1)
        data = None
        s.settimeout(0)
        try:
            data = s.recv(8192)
            print(len(data))
        except Exception as e :
            print("sending data")
            msg = [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), 
                   random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)]
            try:
                s.send(bytearray(msg))
            except:
                print("Error sending")

if __name__ == "__main__":
    sensor_board()