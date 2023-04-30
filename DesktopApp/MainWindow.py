from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow
from WebcamCapture import WebcamCapture
from VipperInterface import VipperInterface
import threading

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        vipper_window = VipperInterface()
        vipper_window.setupUi(self)
        self.data_thread = threading.Thread(target=vipper_window.update_data, daemon=True)
        self.data_thread.start()


if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()
