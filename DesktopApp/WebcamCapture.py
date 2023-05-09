import cv2
import numpy as np
import pyaudio
import wave
import threading

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QApplication, QFrame


class WebcamCapture(QFrame):
    def __init__(self, tab):
        super().__init__(tab)

        self.running = True

        # Set up the UI
        self.label = QLabel(self)
        self.label.resize(640, 480)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

        # Set up video capture
        # TODO: OpenCV cannot choose what camera to use, maybe find someway to choose the correct camera
        try:
            self.video_capture = cv2.VideoCapture(2)
            self.video_file = cv2.VideoWriter('head_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 20.0, (640,480))
        except:
            print("ATTENTION: Head camera not found.")

        # Set up audio capture
        self.input_audio = pyaudio.PyAudio()
        self.output_audio = pyaudio.PyAudio() 
        # Needs to find the head microphone
        self.head_mic_index = -1
        for i in range(self.input_audio.get_device_count()):
            print(self.input_audio.get_device_info_by_index(i).get('name'))
            if self.input_audio.get_device_info_by_index(i).get('name') == 'Microfone (WEB CAM)':
                self.head_mic_index = i
                break
        if (self.head_mic_index == -1):
            print("ATTENTION: Head microphone not found")
        
        self.frames_per_buffer = 1024 
        # TODO: maybe someway to choose the microphone for message
        self.msg_input_stream = self.input_audio.open(format=pyaudio.paFloat32,  
                channels=1,  
                rate=44100,  
                frames_per_buffer=self.frames_per_buffer,  
                input=True,
                input_device_index=1)
        self.head_input_stream = self.input_audio.open(format=pyaudio.paFloat32,  
                channels=1,  
                rate=44100,  
                frames_per_buffer=self.frames_per_buffer,  
                input=True,
                input_device_index=0)
        self.output_stream = self.output_audio.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)
        
        self.audio_thread = threading.Thread(target=self.play_head_audio_stream, daemon=True)


    def display_video_stream(self):
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


    def start_audio_stream(self):
        self.audio_thread.start()


    def play_head_audio_stream(self):
        while(self.running):
            # Read audio from stream
            data = self.head_input_stream.read(self.frames_per_buffer, exception_on_overflow = False)
            data = np.frombuffer(data, dtype=np.float32)
            # Play the audio
            self.output_stream.write(data.tobytes())


    def capture_message(self):
        # Read audio from stream
        data = self.msg_input_stream.read(self.frames_per_buffer, exception_on_overflow = False)
        data = np.frombuffer(data, dtype=np.float32)
        # Send data
        print(len(data.tobytes()))
        return data.tobytes()


    def closeEvent(self, event):
        # save video
        self.running = False
        self.video_capture.release()
        self.video_file.release()
        self.input_stream.stop_stream()
        self.output_stream.stop_stream()
        self.input_stream.close()
        self.output_stream.close()
        self.audio.terminate()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = QApplication([])
    window = WebcamCapture()
    window.show()
    app.exec_()
