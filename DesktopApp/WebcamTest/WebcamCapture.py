import cv2
import numpy as np
import pyaudio
import wave
import threading

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QApplication


class WebcamCapture(QWidget):
    def __init__(self):
        super().__init__()

        self.running = True

        # Set up the UI
        self.label = QLabel(self)
        self.label.resize(640, 480)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

        # Set up video capture
        try:
            try:
                self.video_capture = cv2.VideoCapture(1)
                ret, frame = self.video_capture.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except:
                self.video_capture = cv2.VideoCapture(0)
                ret, frame = self.video_capture.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except:
            raise Exception("No camera found. Closing application.")

        # Set up audio capture
        self.input_audio = pyaudio.PyAudio()
        self.output_audio = pyaudio.PyAudio() 
        self.frames_per_buffer = 1024 
        self.input_stream = self.input_audio.open(format=pyaudio.paFloat32,  
                channels=1,  
                rate=44100,  
                frames_per_buffer=self.frames_per_buffer,  
                input=True)
        self.output_stream = self.output_audio.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)
        
        self.audio_thread = threading.Thread(target=self.play_audio_stream, daemon=True)


    def display_video_stream(self):
        # Capture frame-by-frame
        ret, frame = self.video_capture.read()

        # Convert the frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to QImage
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)

        # Display the QImage
        self.label.setPixmap(QPixmap.fromImage(img))


    def start_audio_stream(self):
        self.audio_thread.start()


    def play_audio_stream(self):
        while(self.running):
            # Read audio from stream
            data = self.input_stream.read(self.frames_per_buffer, exception_on_overflow = False)
            data = np.frombuffer(data, dtype=np.float32)
            # Play the audio
            self.output_stream.write(data.tobytes())


    def closeEvent(self, event):
        self.running = False
        self.video_capture.release()
        self.input_stream.stop_stream()
        self.output_stream.stop_stream()
        self.input_stream.close()
        self.output_stream.close()
        self.audio.terminate()


if __name__ == '__main__':
    app = QApplication([])
    window = WebcamCapture()
    window.show()
    app.exec_()
