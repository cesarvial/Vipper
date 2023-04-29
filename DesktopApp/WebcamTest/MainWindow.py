from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow
from CameraTest import VideoCapture
import threading

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the UI with the video being show
        video_widget = VideoCapture()
        video_widget.start_audio_stream()
        layout = QVBoxLayout()
        layout.addWidget(video_widget)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()
