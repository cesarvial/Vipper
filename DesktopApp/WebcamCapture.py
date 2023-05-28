import cv2
import pyaudio
import wave
import time
from audiofile import *

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QApplication, QFrame


class WebcamCapture(QFrame):
    def __init__(self, tab):
        super().__init__(tab)
        self.running = True
        self.fps = 8000

        # Set up the UI
        self.label = QLabel(self)
        self.label.resize(640, 480)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

        self.camera_connected = False
        self.input_head_init = False
        self.head_mic_index = -1

        # Set up audio capture
        self.input_audio_msg = pyaudio.PyAudio()
        self.output_audio = pyaudio.PyAudio() 

        self.frames_per_buffer = 4000 
        # TODO: maybe someway to choose the microphone for message

        # Start all the audio streams
        self.msg_input_stream = self.input_audio_msg.open(format=pyaudio.paInt16,  
                channels=1,  
                rate=self.fps,  
                frames_per_buffer=self.frames_per_buffer,  
                input=True,
                input_device_index=1)
        #self.head_input_stream = self.input_audio_head.open(format=pyaudio.paInt16,  
        #        channels=1,  
        #        rate=self.fps,  
        #        frames_per_buffer=self.frames_per_buffer,  
        #        input=True,
        #        input_device_index=self.head_mic_index)
        self.output_stream = self.output_audio.open(format=pyaudio.paInt16,
                channels=1,
                rate=self.fps,
                output=True)


    def display_video_stream(self):
        if self.camera_connected:
            try:
                # Capture frame-by-frame
                ret, frame = self.video_capture.read()
                frame = cv2.resize(frame, (640, 480))
                # Write in the file
                self.video_file.write(frame)
                # Convert the frame to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert the frame to QImage
                img = QImage(frame, 640, 480, QImage.Format_RGB888)
                # Display the QImage
                self.label.setPixmap(QPixmap.fromImage(img))
            except:
                self.video_capture.release()
                self.video_file.release()
                self.camera_connected = False
        else:
             # Set up video capture
            try:
                # Restart camera video
                self.video_capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                self.video_file = cv2.VideoWriter('head_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 20.0, (640,480))
                ret, frame = self.video_capture.read()
                frame = cv2.resize(frame, (640, 480))
                self.camera_connected = True
            except:
                self.camera_connected = False
                #print("ATTENTION: Head camera not found.")


    def play_head_audio_stream(self):
        if self.head_mic_index != -1 and self.camera_connected:
            try:
                # Read audio from stream
                data = self.head_input_stream.read(self.frames_per_buffer, exception_on_overflow = False)
                # Play the audio
                self.output_stream.write(data)
            except:
                self.head_input_stream.close()
                self.input_audio_head.terminate()
                self.head_mic_index = -1
                time.sleep(3)
        elif self.head_mic_index == -1 and self.camera_connected: 
            try:
                # Needs to find the head microphone
                self.input_audio_head = pyaudio.PyAudio()
                self.head_mic_index = -1
                for i in range(self.input_audio_head.get_device_count()):
                    print(self.input_audio_head.get_device_info_by_index(i).get('name'))
                for i in range(self.input_audio_head.get_device_count()):
                    if ('WEB CAM)' in self.input_audio_head.get_device_info_by_index(i).get('name')
                    and 'Microfone' in self.input_audio_head.get_device_info_by_index(i).get('name')):
                        self.head_mic_index = i
                        break
                if (self.head_mic_index == -1):
                    self.input_audio_head.terminate()
                    print("ATTENTION: Head microphone not found")
                else:
                    print("Headmic: " + str(self.head_mic_index))
                    self.head_input_stream = self.input_audio_head.open(format=pyaudio.paInt16,  
                        channels=1,  
                        rate=self.fps,  
                        frames_per_buffer=self.frames_per_buffer,  
                        input=True,
                        input_device_index=self.head_mic_index)
            except:
                #print("Head mic not connected")
                self.input_audio_head.terminate()
                self.head_mic_index = -1


    def capture_message(self):
        # Read audio from stream
        frames = []
        for i in range(0, 2):
            data = self.msg_input_stream.read(self.frames_per_buffer, exception_on_overflow = False)
            frames.append(data)
        # Send data
        file_write = wave.open('myfile.wav', 'wb')
        file_write.setframerate(self.fps)
        file_write.setnchannels(1)
        file_write.setsampwidth(2)
        file_write.writeframes(b''.join(frames))
        file_write.close()
        file_read = open('myfile.wav', 'rb')
        final_data = file_read.read(16044)
        file_read.close()
        return final_data


    def closeEvent(self):
        # save video
        self.running = False
        self.video_capture.release()
        self.video_file.release()
        self.msg_input_stream.stop_stream()
        self.head_input_stream.stop_stream()
        self.output_stream.stop_stream()
        self.msg_input_stream.close()
        self.head_input_stream.close()
        self.output_stream.close()
        self.output_audio.terminate()
        self.input_audio_head.terminate()
        self.input_audio_msg.terminate()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = QApplication([])
    window = WebcamCapture()
    window.show()
    app.exec_()
