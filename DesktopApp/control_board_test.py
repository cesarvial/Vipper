import socket
import struct

def control_board():
    s = socket.socket()
    s.connect((socket.gethostname(), 8080))
    print("Control board")
    while (1):
        try:
            s.setblocking(True)
            command = struct.unpack('>h', b'\x00' + s.recv(1))[0]
            print(command)
            #c = struct.unpack('i', command)[0]
            if int(command) == 255:
                print("going backwards")
            elif int(command) == 0:
                print("going forward")
            else:
                print("Value different from 0 or 255 received")
        except Exception as e:
            raise e

if __name__ == '__main__':
    control_board()