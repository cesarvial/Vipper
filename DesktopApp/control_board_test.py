import socket
import struct

def control_board():
    s = socket.socket()
    s.bind((socket.gethostname(), 8080))
    s.listen(1)
    conn, add = s.accept()
    print(add)
    while (1):
        try:
            conn.setblocking(True)
            command = struct.unpack('>h', b'\x00' + conn.recv(1))[0]
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