from PyQt5.QtWidgets import QApplication, QMainWindow
from VipperInterface import VipperInterface
import threading

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        vipper_window = VipperInterface()
        vipper_window.setupUi(self)

        # Thread to update all data
        self.data_thread = threading.Thread(target=vipper_window.update_data, daemon=True)
        self.data_thread.start()
        # Thread to update and plot the map
        self.map_thread = threading.Thread(target=vipper_window.mapping_loop, daemon=True)
        self.map_thread.start()
        # Thread for the audio coming from the webcam
        self.audio_thread = threading.Thread(target=vipper_window.audio_loop, daemon=True)
        self.audio_thread.start()


if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()
