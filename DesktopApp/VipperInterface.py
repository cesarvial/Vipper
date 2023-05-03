# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vipper_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from WebcamCapture import WebcamCapture
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  
import numpy as np  
import random
import time

class VipperInterface(object):
    def __init__(self):
        self.temperature = 20
        self.dangerous_gas = False
        # Acceleration order x y z
        self.acc_data = [0, 0, 0]
        # Gyroscope order x y z
        self.gyro_data = [0, 0, 0]
        # position based on both data
        self.x_pos = [0]
        self.y_pos = [0]
        self.z_pos = [0]
        self.muted = True
        self.going_forward = False
        self.going_backward = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1000, 600))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_webcam = QtWidgets.QWidget()
        self.tab_webcam.setObjectName("tab_webcam")
        self.tab_webcam.setGeometry(QtCore.QRect(0, 0, 1000, 600))
        self.btn_forward = QtWidgets.QPushButton(self.tab_webcam)
        self.btn_forward.setGeometry(QtCore.QRect(700, 230, 91, 31))
        self.btn_forward.setObjectName("btn_forward")
        self.btn_forward.clicked.connect(self.go_forward)
        self.btn_backward = QtWidgets.QPushButton(self.tab_webcam)
        self.btn_backward.setGeometry(QtCore.QRect(700, 270, 91, 31))
        self.btn_backward.setObjectName("btn_backward")
        self.btn_backward.clicked.connect(self.go_backward)
        self.title_temp = QtWidgets.QLabel(self.tab_webcam)
        self.title_temp.setGeometry(QtCore.QRect(700, 40, 111, 21))
        self.title_temp.setObjectName("title_temp")
        self.btn_microphone = QtWidgets.QPushButton(self.tab_webcam)
        self.btn_microphone.setGeometry(QtCore.QRect(800, 230, 131, 71))
        self.btn_microphone.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.btn_microphone.setIconSize(QtCore.QSize(16, 16))
        self.btn_microphone.setObjectName("btn_microphone")
        self.btn_microphone.clicked.connect(self.mute_mic)
        self.vipper_info_box = QtWidgets.QListView(self.tab_webcam)
        self.vipper_info_box.setGeometry(QtCore.QRect(700, 31, 251, 181))
        self.vipper_info_box.setObjectName("vipper_info_box")
        self.title_gas = QtWidgets.QLabel(self.tab_webcam)
        self.title_gas.setGeometry(QtCore.QRect(700, 90, 131, 21))
        self.title_gas.setObjectName("title_gas")
        self.info_temp = QtWidgets.QLabel(self.tab_webcam)
        self.info_temp.setGeometry(QtCore.QRect(700, 60, 71, 21))
        self.info_temp.setObjectName("info_temp")
        self.info_gas = QtWidgets.QLabel(self.tab_webcam)
        self.info_gas.setGeometry(QtCore.QRect(700, 110, 71, 21))
        self.info_gas.setObjectName("info_gas")
        self.webcam_frame = WebcamCapture(self.tab_webcam)
        self.webcam_frame.setGeometry(QtCore.QRect(30, 30, 640, 480))
        self.webcam_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.webcam_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.webcam_frame.setObjectName("webcam_frame")
        self.btn_forward.raise_()
        self.btn_backward.raise_()
        self.btn_microphone.raise_()
        self.vipper_info_box.raise_()
        self.title_temp.raise_()
        self.title_gas.raise_()
        self.info_temp.raise_()
        self.info_gas.raise_()
        self.webcam_frame.raise_()
        self.tabWidget.addTab(self.tab_webcam, "")
        self.tab_mapping = QtWidgets.QWidget()
        self.tab_mapping.setObjectName("tab_mapping")
        self.tab_mapping.setGeometry(QtCore.QRect(0, 0, 1000, 600))
        self.btn_forward_m = QtWidgets.QPushButton(self.tab_mapping)
        self.btn_forward_m.setGeometry(QtCore.QRect(700, 230, 91, 31))
        self.btn_forward_m.setObjectName("btn_forward_m")
        self.btn_forward_m.clicked.connect(self.go_forward)
        self.btn_backward_m = QtWidgets.QPushButton(self.tab_mapping)
        self.btn_backward_m.setGeometry(QtCore.QRect(700, 270, 91, 31))
        self.btn_backward_m.setObjectName("btn_backward_m")
        self.btn_backward_m.clicked.connect(self.go_backward)
        self.btn_microphone_m = QtWidgets.QPushButton(self.tab_mapping)
        self.btn_microphone_m.setGeometry(QtCore.QRect(800, 230, 131, 71))
        self.btn_microphone_m.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.btn_microphone_m.setIconSize(QtCore.QSize(16, 16))
        self.btn_microphone_m.setObjectName("btn_microphone_m")
        self.vipper_info_box_m = QtWidgets.QListView(self.tab_mapping)
        self.vipper_info_box_m.setGeometry(QtCore.QRect(700, 31, 251, 181))
        self.vipper_info_box_m.setObjectName("vipper_info_box_m")
        self.info_gas_m = QtWidgets.QLabel(self.tab_mapping)
        self.info_gas_m.setGeometry(QtCore.QRect(700, 110, 71, 21))
        self.info_gas_m.setObjectName("info_gas_m")
        self.info_temp_m = QtWidgets.QLabel(self.tab_mapping)
        self.info_temp_m.setGeometry(QtCore.QRect(700, 60, 71, 21))
        self.info_temp_m.setObjectName("info_temp_m")
        self.title_temp_m = QtWidgets.QLabel(self.tab_mapping)
        self.title_temp_m.setGeometry(QtCore.QRect(700, 40, 111, 21))
        self.title_temp_m.setObjectName("title_temp_m")
        self.title_gas_m = QtWidgets.QLabel(self.tab_mapping)
        self.title_gas_m.setGeometry(QtCore.QRect(700, 90, 131, 21))
        self.title_gas_m.setObjectName("title_gas_m")
        # Plotting 
        self.mapping_fig = Figure()
        self.mapping_canvas = FigureCanvasQTAgg(self.mapping_fig)
        self.mapping_axes = self.mapping_fig.add_subplot(projection='3d')
        self.plot_layout = QtWidgets.QVBoxLayout()
        self.plot_layout.addWidget(self.mapping_canvas)    
        self.mapping_frame = QtWidgets.QFrame(self.tab_mapping)
        self.mapping_frame.setLayout(self.plot_layout)
        self.mapping_frame.setGeometry(QtCore.QRect(30, 30, 650, 490))
        self.mapping_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mapping_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mapping_frame.setObjectName("mapping_frame")

        self.mapping_label = QtWidgets.QLabel(self.tab_mapping)
        self.mapping_label.setGeometry(QtCore.QRect(220, 15, 240, 30))
        self.mapping_label.setObjectName("mapping_label")
        self.btn_forward_m.raise_()
        self.btn_backward_m.raise_()
        self.btn_microphone_m.raise_()
        self.vipper_info_box_m.raise_()
        self.info_gas_m.raise_()
        self.info_temp_m.raise_()
        self.title_temp_m.raise_()
        self.title_gas_m.raise_()
        self.mapping_frame.raise_()
        self.tabWidget.addTab(self.tab_mapping, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.webcam_frame.start_audio_stream()
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vipper - version 1.0"))
        self.btn_forward.setText(_translate("MainWindow", "Forward"))
        self.btn_forward.setShortcut(_translate("MainWindow", "Up"))
        self.btn_backward.setText(_translate("MainWindow", "Backward"))
        self.btn_backward.setShortcut(_translate("MainWindow", "Down"))
        self.title_temp.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Temp ºC</span></p></body></html>"))
        self.btn_microphone.setText(_translate("MainWindow", "Unmute"))
        self.btn_microphone.setShortcut(_translate("MainWindow", "Space"))
        self.title_gas.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Dangerous Gas</span></p></body></html>"))
        self.info_temp.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#1f1f55;\">20º</span></p></body></html>"))
        self.info_gas.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">Detected</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_webcam), _translate("MainWindow", "Camera"))
        self.btn_forward_m.setText(_translate("MainWindow", "Forward"))
        self.btn_forward_m.setShortcut(_translate("MainWindow", "Up"))
        self.btn_backward_m.setText(_translate("MainWindow", "Backward"))
        self.btn_backward_m.setShortcut(_translate("MainWindow", "Down"))
        self.btn_microphone_m.setText(_translate("MainWindow", "Unmute"))
        self.btn_microphone_m.setShortcut(_translate("MainWindow", "Space"))
        self.btn_microphone_m.setDisabled(True)
        self.info_gas_m.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">Not Detected</span></p></body></html>"))
        self.info_temp_m.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#1f1f55;\">20º</span></p></body></html>"))
        self.title_temp_m.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Temp ºC</span></p></body></html>"))
        self.title_gas_m.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Dangerous Gas</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mapping), _translate("MainWindow", "Mapping"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.mapping_label.setText(_translate("MainWindow", "Left button to move, right button to Zoom in/out."))

    
    def update_data(self):
        _translate = QtCore.QCoreApplication.translate
        i = 0
        y_m = 0
        z_m = 0
        while(1):
            if self.muted:
                self.tab_mapping.setDisabled(False)
                # get temperature
                if self.dangerous_gas:
                    self.temperature += random.random()
                else:
                    self.temperature -= random.random()
                # get gas
                self.dangerous_gas = bool(random.getrandbits(1))
                # get acc
                # self.acc_data = [random.random(), random.random(), random.random()]
                # get gyro data
                # TODO: make it actually work. For now just random stuff
                if (random.random() > 0.95):
                    y_m = random.random()
                    self.gyro_data = [0, y_m, 0]
                if (random.random() < 0.05):
                    z_m = random.random()
                    self.gyro_data = [0, 0, z_m]
                # updte position
                # It will start by going on X's direction, then with gyro data ir will turn
                if self.going_forward:
                    self.x_pos.append(i)
                    self.y_pos.append(i*y_m)
                    self.z_pos.append(i*z_m)
                    i += 0.01
                elif self.going_backward and len(self.x_pos) > 1:
                    self.x_pos.pop()
                    self.y_pos.pop()
                    self.z_pos.pop()
                    i -= 0.01
                # update mapping plot
                self.update_mapping_plot()

                # update temperature
                temp_string = "<html><head/><body><p><span style=\" font-size:11pt; color:#1f1f55;\">" + str(self.temperature)[0:6] + "º</span></p></body></html>"
                self.info_temp.setText(_translate("MainWindow", temp_string))
                self.info_temp_m.setText(_translate("MainWindow", temp_string))
                # update dangerous gas
                if self.dangerous_gas:
                    color = "ff0000"
                    gas = "Detected"
                else:
                    color = "00ff00"
                    gas = "Not detected"
                gas_string = "<html><head/><body><p><span style=\" font-size:10pt; color:#" + color + ";\">" + gas + "</span></p></body></html>"
                self.info_gas.setText(_translate("MainWindow", gas_string))
                self.info_gas_m.setText(_translate("MainWindow", gas_string))
                time.sleep(0.1)
            else:
                self.webcam_frame.capture_message()


    def go_forward(self):
        _translate = QtCore.QCoreApplication.translate
        # If it was going back, change text to backward again
        if self.going_backward:
            self.going_backward = False
            self.btn_backward.setText(_translate("MainWindow", "Backward"))
            self.btn_backward_m.setText(_translate("MainWindow", "Backward"))
        # If it was going forward, change text to go forward again, and stop
        if self.going_forward:
            self.going_forward = False
            self.btn_forward.setText(_translate("MainWindow", "Forward"))
            self.btn_forward_m.setText(_translate("MainWindow", "Forward"))
            print("Stop from going forward")
        # If it was stopped, go forward
        else:
            self.going_forward = True
            self.btn_forward.setText(_translate("MainWindow", "Stop"))
            self.btn_forward_m.setText(_translate("MainWindow", "Stop"))
            print("Started to go forward")
        


    def go_backward(self):
        _translate = QtCore.QCoreApplication.translate
        # If it was going back, change text to backward again
        if self.going_forward:
            self.going_forward = False
            self.btn_forward.setText(_translate("MainWindow", "Forward"))
            self.btn_forward_m.setText(_translate("MainWindow", "Forward"))
        # If it was going forward, change text to go forward again, and stop
        if self.going_backward:
            self.going_backward = False
            self.btn_backward.setText(_translate("MainWindow", "Backward"))
            self.btn_backward_m.setText(_translate("MainWindow", "Backward"))
            print("Stop from going backward")
        # If it was stopped, go forward
        else:
            self.going_backward = True
            self.btn_backward.setText(_translate("MainWindow", "Stop"))
            self.btn_backward_m.setText(_translate("MainWindow", "Stop"))
            print("Started to go backward")


    def mute_mic(self):
        _translate = QtCore.QCoreApplication.translate
        if self.muted:
            if self.going_backward:
                self.going_backward = False
                self.btn_backward.setText(_translate("MainWindow", "Backward"))
                self.btn_backward_m.setText(_translate("MainWindow", "Backward"))
            elif self.going_forward:
                self.going_forward = False
                self.btn_forward.setText(_translate("MainWindow", "Forward"))
                self.btn_forward_m.setText(_translate("MainWindow", "Forward"))
            self.muted = False
            self.btn_microphone.setText(_translate("MainWindow", "Mute"))
            self.btn_microphone_m.setText(_translate("MainWindow", "Mute"))
            self.btn_backward.setDisabled(True)
            self.btn_backward_m.setDisabled(True)
            self.btn_forward.setDisabled(True)
            self.btn_forward_m.setDisabled(True)
            self.tabWidget.tabBar().setDisabled(True)
        else: 
            self.muted = True
            self.btn_microphone.setText(_translate("MainWindow", "Unmute"))
            self.btn_microphone_m.setText(_translate("MainWindow", "Unmute"))
            self.btn_backward.setDisabled(False)
            self.btn_backward_m.setDisabled(False)
            self.btn_forward.setDisabled(False)
            self.btn_forward_m.setDisabled(False)
            self.tabWidget.tabBar().setDisabled(False)


    def update_mapping_plot(self):
        self.mapping_axes.clear()
        self.mapping_axes.set_xlabel("x (m)")
        self.mapping_axes.set_ylabel("y (m)")
        self.mapping_axes.set_zlabel("z (m)")
        self.mapping_axes.plot(self.x_pos, self.y_pos, self.z_pos, 'green')
        self.mapping_canvas.draw()
