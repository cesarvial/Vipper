# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vipper_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from WebcamCapture import WebcamCapture

class VipperInterface(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 396)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 801, 371))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_webcam = QtWidgets.QWidget()
        self.tab_webcam.setObjectName("tab_webcam")
        self.btn_forward = QtWidgets.QPushButton(self.tab_webcam)
        self.btn_forward.setGeometry(QtCore.QRect(510, 230, 91, 31))
        self.btn_forward.setObjectName("btn_forward")
        self.btn_backward = QtWidgets.QPushButton(self.tab_webcam)
        self.btn_backward.setGeometry(QtCore.QRect(510, 270, 91, 31))
        self.btn_backward.setObjectName("btn_backward")
        self.title_temp = QtWidgets.QLabel(self.tab_webcam)
        self.title_temp.setGeometry(QtCore.QRect(520, 40, 111, 21))
        self.title_temp.setObjectName("title_temp")
        self.btn_microphone = QtWidgets.QPushButton(self.tab_webcam)
        self.btn_microphone.setGeometry(QtCore.QRect(630, 230, 131, 71))
        self.btn_microphone.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.btn_microphone.setIconSize(QtCore.QSize(16, 16))
        self.btn_microphone.setObjectName("btn_microphone")
        self.vipper_info_box = QtWidgets.QListView(self.tab_webcam)
        self.vipper_info_box.setGeometry(QtCore.QRect(510, 31, 251, 181))
        self.vipper_info_box.setObjectName("vipper_info_box")
        self.title_gas = QtWidgets.QLabel(self.tab_webcam)
        self.title_gas.setGeometry(QtCore.QRect(520, 90, 131, 21))
        self.title_gas.setObjectName("title_gas")
        self.placeholder_webcam = QtWidgets.QLabel(self.tab_webcam)
        self.placeholder_webcam.setGeometry(QtCore.QRect(30, 30, 441, 271))
        self.placeholder_webcam.setText("")
        self.placeholder_webcam.setPixmap(QtGui.QPixmap(":/preview/WhatsApp Image 2023-04-27 at 14.46.14.jpeg"))
        self.placeholder_webcam.setScaledContents(True)
        self.placeholder_webcam.setObjectName("placeholder_webcam")
        self.info_temp = QtWidgets.QLabel(self.tab_webcam)
        self.info_temp.setGeometry(QtCore.QRect(520, 60, 71, 21))
        self.info_temp.setObjectName("info_temp")
        self.info_gas = QtWidgets.QLabel(self.tab_webcam)
        self.info_gas.setGeometry(QtCore.QRect(520, 110, 71, 21))
        self.info_gas.setObjectName("info_gas")
        self.webcam_frame = QtWidgets.QFrame(self.tab_webcam)
        self.webcam_frame.setGeometry(QtCore.QRect(30, 30, 441, 271))
        self.webcam_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.webcam_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.webcam_frame.setObjectName("webcam_frame")
        self.btn_forward.raise_()
        self.btn_backward.raise_()
        self.btn_microphone.raise_()
        self.vipper_info_box.raise_()
        self.title_temp.raise_()
        self.title_gas.raise_()
        self.placeholder_webcam.raise_()
        self.info_temp.raise_()
        self.info_gas.raise_()
        self.webcam_frame.raise_()
        self.tabWidget.addTab(self.tab_webcam, "")
        self.tab_mapping = QtWidgets.QWidget()
        self.tab_mapping.setObjectName("tab_mapping")
        self.placeholder_mapping = QtWidgets.QLabel(self.tab_mapping)
        self.placeholder_mapping.setGeometry(QtCore.QRect(30, 29, 441, 271))
        self.placeholder_mapping.setText("")
        self.placeholder_mapping.setPixmap(QtGui.QPixmap(":/preview/WhatsApp Image 2023-04-27 at 14.46.55.jpeg"))
        self.placeholder_mapping.setScaledContents(True)
        self.placeholder_mapping.setObjectName("placeholder_mapping")
        self.btn_forward_m = QtWidgets.QPushButton(self.tab_mapping)
        self.btn_forward_m.setGeometry(QtCore.QRect(510, 230, 91, 31))
        self.btn_forward_m.setObjectName("btn_forward_m")
        self.btn_backward_m = QtWidgets.QPushButton(self.tab_mapping)
        self.btn_backward_m.setGeometry(QtCore.QRect(510, 270, 91, 31))
        self.btn_backward_m.setObjectName("btn_backward_m")
        self.btn_microphone_m = QtWidgets.QPushButton(self.tab_mapping)
        self.btn_microphone_m.setGeometry(QtCore.QRect(630, 230, 131, 71))
        self.btn_microphone_m.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.btn_microphone_m.setIconSize(QtCore.QSize(16, 16))
        self.btn_microphone_m.setObjectName("btn_microphone_m")
        self.vipper_info_box_m = QtWidgets.QListView(self.tab_mapping)
        self.vipper_info_box_m.setGeometry(QtCore.QRect(510, 31, 251, 181))
        self.vipper_info_box_m.setObjectName("vipper_info_box_m")
        self.info_gas_m = QtWidgets.QLabel(self.tab_mapping)
        self.info_gas_m.setGeometry(QtCore.QRect(520, 110, 71, 21))
        self.info_gas_m.setObjectName("info_gas_m")
        self.info_temp_m = QtWidgets.QLabel(self.tab_mapping)
        self.info_temp_m.setGeometry(QtCore.QRect(520, 60, 71, 21))
        self.info_temp_m.setObjectName("info_temp_m")
        self.title_temp_m = QtWidgets.QLabel(self.tab_mapping)
        self.title_temp_m.setGeometry(QtCore.QRect(520, 40, 111, 21))
        self.title_temp_m.setObjectName("title_temp_m")
        self.title_gas_m = QtWidgets.QLabel(self.tab_mapping)
        self.title_gas_m.setGeometry(QtCore.QRect(520, 90, 131, 21))
        self.title_gas_m.setObjectName("title_gas_m")
        self.mapping_frame = QtWidgets.QFrame(self.tab_mapping)
        self.mapping_frame.setGeometry(QtCore.QRect(40, 40, 441, 271))
        self.mapping_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mapping_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mapping_frame.setObjectName("mapping_frame")
        self.btn_forward_m.raise_()
        self.btn_backward_m.raise_()
        self.btn_microphone_m.raise_()
        self.vipper_info_box_m.raise_()
        self.info_gas_m.raise_()
        self.info_temp_m.raise_()
        self.title_temp_m.raise_()
        self.title_gas_m.raise_()
        self.mapping_frame.raise_()
        self.placeholder_mapping.raise_()
        self.tabWidget.addTab(self.tab_mapping, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuMenu.addAction(self.actionSettings)
        self.menuMenu.addAction(self.actionExit)
        self.menubar.addAction(self.menuMenu.menuAction())

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
        self.btn_microphone.setText(_translate("MainWindow", "🎙"))
        self.btn_microphone.setShortcut(_translate("MainWindow", "Space"))
        self.title_gas.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Dangerous Gas</span></p></body></html>"))
        self.info_temp.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#1f1f55;\">20º</span></p></body></html>"))
        self.info_gas.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">detected</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_webcam), _translate("MainWindow", "Camera"))
        self.btn_forward_m.setText(_translate("MainWindow", "Forward"))
        self.btn_forward_m.setShortcut(_translate("MainWindow", "Up"))
        self.btn_backward_m.setText(_translate("MainWindow", "Backward"))
        self.btn_backward_m.setShortcut(_translate("MainWindow", "Down"))
        self.btn_microphone_m.setText(_translate("MainWindow", "🎙"))
        self.btn_microphone_m.setShortcut(_translate("MainWindow", "Space"))
        self.info_gas_m.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; color:#ff0000;\">detected</span></p></body></html>"))
        self.info_temp_m.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#1f1f55;\">20º</span></p></body></html>"))
        self.title_temp_m.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Temp ºC</span></p></body></html>"))
        self.title_gas_m.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Dangerous Gas</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mapping), _translate("MainWindow", "Mapping"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
