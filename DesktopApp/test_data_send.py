import socket
import time

file_read = open('testestest.wav', 'rb')
final_data = file_read.read(16088)
file_read.close()

sensor_board_add = ('192.168.100.200', 1775)
        #self.sensor_board_add = (socket.gethostname(), 8081)
sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sensor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sensor_socket.connect(sensor_board_add)

print("Connected")
print("Total: " + str(len(final_data)))

i = 0
while (i*300 < 16088):
    begin = i*300
    end = (i + 1)*300
    if begin + 300 > 16000:
        end = 16088
    print(len(final_data[begin:end]))
    sensor_socket.send(final_data[begin:end])
    i += 1
    time.sleep(0.05)
