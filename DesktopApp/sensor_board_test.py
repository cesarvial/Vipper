# Script to test the communication modules of the desktop app
import socket
import time
import wave

def sensor_board():
    #output_audio = pyaudio.PyAudio() 
    #output_stream = output_audio.open(format=pyaudio.paFloat32,
    #            channels=1,
    #            rate=8000,
    #            output=True,
    #            output_device_index=0)
    s = socket.socket()
    s.bind((socket.gethostname(), 8081))
    s.listen(1)
    conn, add = s.accept()
    print(add)
    data = None
    while (1):
        time.sleep(0.1)
        data = None
        conn.settimeout(0)
        try:
            data = conn.recv(80044)
            #file_write = wave.open('testestest.wav', 'wb')
            #file_write.setframerate(8000)
            #file_write.setnchannels(1)
            #file_write.setsampwidth(2)
            #file_write.writeframes(data)
            #file_write.close()
            #output_stream.write(data)
            #print(data)
        except Exception as e :
            #print("sending data")
            #msg = [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), 
            #       random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)]
            msg = b'\xff\x25\x00\x26\x00\x27\x00\x28\x00\x29\x00\x30\x00\x31\x00'
            try:
                conn.send(msg)
            except:
                print("Error sending")

if __name__ == "__main__":
    sensor_board()