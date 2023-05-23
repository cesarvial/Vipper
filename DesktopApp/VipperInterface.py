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
import time
import socket
import struct

class VipperInterface(object):
    def __init__(self):
        self.temperature = 20
        self.dangerous_gas = False

        # 2: inplace; 1: forward, 0:backward
        self.direction = 2

        # Gyroscope order x y z
        self.gyro_data = [0, 0, 0]

        # Accelerometer order x y z
        self.acc_data = [0, 0, 0]

        # Compensated acceleration
        self.comp_acc = [0, 0, 0]

        self.gravity_taken = False

        # Gravity acceleration order x y z
        self.gravity = [0, 0, 0]

        # postion array for plotting
        self.x_pos = [0]
        self.y_pos = [0]
        self.z_pos = [0]

        # velocity order x y z
        self.velocity = [0.01, 0, 0]

        self.muted = True
        self.is_control_conn = False
        self.is_sensor_conn = False

        # Initiate the sockets
        # control board
        self.control_board_add = ('192.168.4.1', 1775)
        #self.control_board_add = (socket.gethostname(), 8080)
        #self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.control_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # sensor board
        self.sensor_board_add = ('192.168.4.2', 1775)
        #self.sensor_board_add = (socket.gethostname(), 8081)
        #self.sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sensor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_loading = QtWidgets.QLabel(MainWindow)
        self.label_loading.setGeometry(QtCore.QRect(0, 0, 1000, 600))
        self.label_loading.setObjectName("label_loading")
        self.label_loading.setFont(QtGui.QFont('Times', 25, 60))
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1000, 600))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_webcam = QtWidgets.QWidget()
        self.tab_webcam.setObjectName("tab_webcam")
        self.tab_webcam.setGeometry(QtCore.QRect(200, 0, 600, 600))
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

        #self.webcam_frame.start_audio_stream()
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vipper - version 1.0"))
        self.label_loading.setText(_translate("MainWindow", ""))
        self.btn_forward.setText(_translate("MainWindow", "Unroll"))
        self.btn_forward.setShortcut(_translate("MainWindow", "Up"))
        self.btn_backward.setText(_translate("MainWindow", "Roll"))
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
        self.mapping_axes.set_xlabel("x (m)")
        self.mapping_axes.set_ylabel("y (m)")
        self.mapping_axes.set_zlabel("z (m)")

    
    def update_data(self):
        _translate = QtCore.QCoreApplication.translate
        sensor_data = None

        while(1):
            # In case some board is not connected, re-stablish connection
            if (not self.is_sensor_conn) or (not self.is_control_conn):
                self.loading()
            else:
                # if muted, receive and process all data
                if self.muted:
                    self.tab_mapping.setDisabled(False)

                    # 9 Bytes 
                    try:
                        self.sensor_socket.settimeout(10)
                        sensor_data = self.sensor_socket.recv(15)
                    except:
                        print("Lost Connection to sensor board")
                        self.is_sensor_conn = False
                        continue

                    if sensor_data == b'':
                        print("Lost Connection to sensor board")
                        self.is_sensor_conn = False
                        continue

                    # gas/movement - byte 0
                    # 10000000 - 128
                    # 1xxxxxxx - dangerous gas // 0xxxxxxx - no dangerous gas
                    if (sensor_data[0] & 128) == 128:
                        self.dangerous_gas = True
                    else:
                        self.dangerous_gas = False

                    # x_gyro - bytes 1 and 2
                    self.gyro_data[1] = np.float16(struct.unpack('>h', sensor_data[1:3])[0]/1000 + 0.02)
                    if (self.gyro_data[1] <= 0.06) and (self.gyro_data[1] >= -0.06):
                        self.gyro_data[1] = 0.00
                    # y_gyro - bytes 3 and 4
                    self.gyro_data[2] = np.float16(struct.unpack('>h', sensor_data[3:5])[0]/1000 - 0.05)
                    if (self.gyro_data[2] <= 0.06) and (self.gyro_data[2] >= -0.06):
                        self.gyro_data[2] = 0.00
                    # z_gyro - bytes 5 and 6
                    self.gyro_data[0] = np.float16(struct.unpack('>h', sensor_data[5:7])[0]/1000 - 0.01)
                    if (self.gyro_data[0] <= 0.06) and (self.gyro_data[0] >= -0.06):
                        self.gyro_data[0] = 0.00

                    # temperature - bytes 7 and 8
                    self.temperature = np.float16(struct.unpack('>h', sensor_data[7:9])[0]/100)

                    # z_acc - bytes 9 and 10
                    self.acc_data[1] = np.float16(struct.unpack('>h', sensor_data[9:11])[0]/1000)
                    # y_acc - bytes 11 and 12
                    self.acc_data[2] = np.float16(struct.unpack('>h', sensor_data[11:13])[0]/1000)
                    # x_acc - bytes 13 and 14
                    self.acc_data[0] = np.float16(struct.unpack('>h', sensor_data[13:15])[0]/1000)*-1

                    if not self.gravity_taken:
                        self.gravity = np.copy(self.acc_data)
                        self.gravity_taken = True

                    # update temperature text
                    temp_string = "<html><head/><body><p><span style=\" font-size:11pt; color:#1f1f55;\">" + str(self.temperature)[0:6] + "º</span></p></body></html>"
                    self.info_temp.setText(_translate("MainWindow", temp_string))
                    self.info_temp_m.setText(_translate("MainWindow", temp_string))

                    # update dangerous gas text
                    if self.dangerous_gas:
                        color = "ff0000"
                        gas = "Detected"
                    else:
                        color = "00ff00"
                        gas = "Not detected"
                    gas_string = "<html><head/><body><p><span style=\" font-size:10pt; color:#" + color + ";\">" + gas + "</span></p></body></html>"
                    self.info_gas.setText(_translate("MainWindow", gas_string))
                    self.info_gas_m.setText(_translate("MainWindow", gas_string))
                    time.sleep(0.08)
                # If not muted, send all microphone to the sensor socket
                else:
                    try:
                        message = self.webcam_frame.capture_message()
                        # msg size is 16044
                        i = 0
                        padding = 56 * b'0'
                        self.sensor_socket.send(message+padding)
                    except:
                        print("Lost connection to sensor board.")
                        self.is_sensor_conn = False


    def loading(self):
        _translate = QtCore.QCoreApplication.translate
        loading_text = "Establishing Connection\n"
        
        if not self.is_control_conn:
            loading_text += "Control Board - Not Connected\n"
        else:
            loading_text += "Control Board - Connected\n"
        if not self.is_sensor_conn:
            loading_text += "Sensor Board - Not Connected"
        else:
            loading_text += "Sensor Board - Connected"

        self.centralwidget.setDisabled(True)
        self.label_loading.setStyleSheet("background-color: White")
        self.label_loading.setAlignment(QtCore.Qt.AlignCenter)
        self.label_loading.setGeometry(QtCore.QRect(0, 0, 1000, 600))
        self.label_loading.setText(_translate("MainWindow", loading_text))

        if not self.is_control_conn:
            self.connect_control()
        if self.is_control_conn:
            loading_text = loading_text.replace("Control Board - Not Connected\n", "Control Board - Connected\n")
            self.label_loading.setText(_translate("MainWindow", loading_text))

        if not self.is_sensor_conn:
            self.connect_sensor()

        if (self.is_sensor_conn) and (self.is_control_conn):
            self.label_loading.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.label_loading.setText(_translate("MainWindow", ""))
            self.centralwidget.setDisabled(False)


    # Try to connect the control board
    def connect_control(self):
        try:
            self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.control_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.control_socket.connect(self.control_board_add)
            self.is_control_conn = True
        except:
            self.is_control_conn = False


    # Try to connect the sensor board
    def connect_sensor(self):
        try:
            self.sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sensor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sensor_socket.connect(self.sensor_board_add)
            self.is_sensor_conn = True
        except:
            self.is_sensor_conn = False


    # Send message to go forward
    def go_forward(self):
        self.btn_backward.setDisabled(True)
        self.btn_forward.setDisabled(True)
        try:
            self.control_socket.send(b'\x00')
        except:
            print("Lost connection to control board.")
            self.is_control_conn = False
        time.sleep(0.5)
        self.btn_backward.setDisabled(False)
        self.btn_forward.setDisabled(False)
        

    # Send message to go backward
    def go_backward(self):
        self.btn_backward.setDisabled(True)
        self.btn_forward.setDisabled(True)
        try:
            self.control_socket.send(b'\xff')
        except:
            print("Lost connection to control board.")
            self.is_control_conn = False
        time.sleep(0.5)
        self.btn_backward.setDisabled(False)
        self.btn_forward.setDisabled(False)
    

    # mute/unmute the microphone and update the UI
    def mute_mic(self):
        _translate = QtCore.QCoreApplication.translate
        if self.muted:
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

    # function to run the mapping on a different thread
    def mapping_loop(self):
        while (True):
            if (self.gravity_taken and self.is_sensor_conn and self.is_control_conn and self.muted):
                self.update_position()
                time.sleep(0.1)


    def audio_loop(self):
        while(True):
            if(self.muted):
                self.webcam_frame.play_head_audio_stream()


    # Update the position of the head
    def update_position(self):
        # calculate the direction it is going
        # For this we need to compesate for the gravity acceleration
        rotation = self.calc_rotation_matrix(self.gyro_data[0], self.gyro_data[1], self.gyro_data[2])
        gx = self.gravity[0]
        gy = self.gravity[1]
        gz = self.gravity[2]
        self.gravity[0] = rotation[0][0] * gx + rotation[0][1] * gy + rotation[0][2] * gz
        self.gravity[1] = rotation[1][0] * gx + rotation[1][1] * gy + rotation[1][2] * gz
        self.gravity[2] = rotation[2][0] * gx + rotation[2][1] * gy + rotation[2][2] * gz 
        self.comp_acc[0] = self.acc_data[0] - self.gravity[0]
        self.comp_acc[1] = self.acc_data[1] - self.gravity[1]
        self.comp_acc[2] = self.acc_data[2] - self.gravity[2]

        # if it is in place
        if (self.direction == 2):
            # going forward
            if (self.comp_acc[0] >= 0.1):
                self.direction = 1
            # going backward
            elif (self.comp_acc[0] <= -0.1):
                self.direction = 0
        # if it is going forward
        if (self.direction == 1):
            # stop 
            if (self.comp_acc[0] <= -0.1):
                self.direction = 2
        # if it is going backward
        if (self.direction == 0):
            # stop
            if (self.comp_acc[0] >= 0.1):
                self.direction = 2

        #print("raw acc, gravity, comp acc, direction, gyro")
        #print(self.acc_data, self.gravity, self.comp_acc, self.direction, self.gyro_data)

        # if it is going forward
        if self.direction == 1:
            # rotation = self.calc_rotation_matrix(self.gyro_data[0], self.gyro_data[1], self.gyro_data[2])

            # calculate new velocities
            vx = self.velocity[0]
            vy = self.velocity[1]
            vz = self.velocity[2]
            self.update_mapping_plot()
            self.velocity[0] = rotation[0][0] * vx + rotation[0][1] * vy + rotation[0][2] * vz
            self.velocity[1] = rotation[1][0] * vx + rotation[1][1] * vy + rotation[1][2] * vz
            self.velocity[2] = rotation[2][0] * vx + rotation[2][1] * vy + rotation[2][2] * vz

            # calculate new positions
            delta_t = 0.1
            self.x_pos.append(self.x_pos[len(self.x_pos) - 1] + self.velocity[0] * delta_t)
            self.y_pos.append(self.y_pos[len(self.y_pos) - 1] + self.velocity[1] * delta_t)
            self.z_pos.append(self.z_pos[len(self.z_pos) - 1] + self.velocity[2] * delta_t)
            self.update_mapping_plot()

        # if it is going backwards
        elif self.direction == 0 and len(self.x_pos) > 1:
            try:
                self.x_pos.pop()
                self.y_pos.pop()
                self.z_pos.pop()
                self.update_mapping_plot()
            except:
                #print("no more positions to pop")
                pass

    
    # Function to calculate the rotation matrix with the gyro data
    def calc_rotation_matrix(self, omega_x, omega_y, omega_z):
        # constant because it only gets data each tenth of a second
        delta_t = 0.1
        # Calculate the sin and cosine of the angles
        cosx = np.cos(omega_x * delta_t)
        cosy = np.cos(omega_y * delta_t)
        cosz = np.cos(omega_z * delta_t)
        sinx = np.sin(omega_x * delta_t)
        siny = np.sin(omega_y * delta_t)
        sinz = np.sin(omega_z * delta_t)
        # Calculate the elements of the rotation matrix
        R11 = cosy * cosz
        R12 = sinx * siny * cosz - cosx * sinz
        R13 = cosx * siny * cosz + sinx * sinz
        R21 = cosy * sinz
        R22 = sinx * siny * sinz + cosx * cosz  
        R23 = cosx * siny * sinz - sinx * cosz
        R31 = -siny
        R32 = sinx * cosy
        R33 = cosx * cosy
        # Return the rotation matrix
        return [[R11, R12, R13], [R21, R22, R23], [R31, R32, R33]]


    # Update the plot that presents the mapping
    def update_mapping_plot(self):
        self.mapping_axes.clear()
        self.mapping_axes.set_xlabel("x (m)")
        self.mapping_axes.set_ylabel("y (m)")
        self.mapping_axes.set_zlabel("z (m)")
        tip = int((len(self.x_pos) / 100)*90)
        self.mapping_axes.plot(self.x_pos[0:tip], self.y_pos[0:tip], self.z_pos[0:tip], color='limegreen', label='body')
        self.mapping_axes.plot(self.x_pos[tip-1:], self.y_pos[tip-1:], self.z_pos[tip-1:], color='crimson', label='head')
        self.set_axes_equal()
        self.mapping_axes.legend()
        self.mapping_canvas.draw()


    # Auxiliary function to make all the axis the same size in the mapping plot
    def set_axes_equal(self):
        x_limits = self.mapping_axes.get_xlim3d()
        y_limits = self.mapping_axes.get_ylim3d()
        z_limits = self.mapping_axes.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = np.mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = np.mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = np.mean(z_limits)

        # The plot bounding box is a sphere in the sense of the infinity
        # norm, hence I call half the max range the plot radius.
        plot_radius = 0.5*max([x_range, y_range, z_range])

        self.mapping_axes.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        self.mapping_axes.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        self.mapping_axes.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

