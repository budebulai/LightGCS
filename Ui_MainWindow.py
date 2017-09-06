# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\DATAANALYSE\PYTHON\PYQT\LightGCS\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 800)
        MainWindow.setMouseTracking(True)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gv_setter = QtWidgets.QGraphicsView(self.centralWidget)
        self.gv_setter.setGeometry(QtCore.QRect(0, 0, 60, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gv_setter.sizePolicy().hasHeightForWidth())
        self.gv_setter.setSizePolicy(sizePolicy)
        self.gv_setter.setMouseTracking(True)
        self.gv_setter.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gv_setter.setStyleSheet("border-image: url(:/side_btn/LightGCS_image/setter.png);")
        self.gv_setter.setObjectName("gv_setter")
        self.gv_logger = QtWidgets.QGraphicsView(self.centralWidget)
        self.gv_logger.setGeometry(QtCore.QRect(120, 0, 60, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gv_logger.sizePolicy().hasHeightForWidth())
        self.gv_logger.setSizePolicy(sizePolicy)
        self.gv_logger.setMouseTracking(True)
        self.gv_logger.setStyleSheet("border-image: url(:/side_btn/LightGCS_image/logger.png);")
        self.gv_logger.setObjectName("gv_logger")
        self.gv_monitor = QtWidgets.QGraphicsView(self.centralWidget)
        self.gv_monitor.setGeometry(QtCore.QRect(60, 0, 60, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gv_monitor.sizePolicy().hasHeightForWidth())
        self.gv_monitor.setSizePolicy(sizePolicy)
        self.gv_monitor.setMouseTracking(True)
        self.gv_monitor.setStyleSheet("border-image: url(:/side_btn/LightGCS_image/monitor.png);")
        self.gv_monitor.setObjectName("gv_monitor")
        self.gv_params = QtWidgets.QGraphicsView(self.centralWidget)
        self.gv_params.setGeometry(QtCore.QRect(180, 0, 60, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gv_params.sizePolicy().hasHeightForWidth())
        self.gv_params.setSizePolicy(sizePolicy)
        self.gv_params.setMouseTracking(True)
        self.gv_params.setStyleSheet("border-image: url(:/side_btn/LightGCS_image/params.png);")
        self.gv_params.setObjectName("gv_params")
        self.gv_exts = QtWidgets.QGraphicsView(self.centralWidget)
        self.gv_exts.setGeometry(QtCore.QRect(240, 0, 60, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gv_exts.sizePolicy().hasHeightForWidth())
        self.gv_exts.setSizePolicy(sizePolicy)
        self.gv_exts.setMouseTracking(True)
        self.gv_exts.setStyleSheet("border-image: url(:/side_btn/LightGCS_image/exts.png);")
        self.gv_exts.setObjectName("gv_exts")
        self.gv_about = QtWidgets.QGraphicsView(self.centralWidget)
        self.gv_about.setGeometry(QtCore.QRect(300, 0, 60, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gv_about.sizePolicy().hasHeightForWidth())
        self.gv_about.setSizePolicy(sizePolicy)
        self.gv_about.setStyleSheet("border-image: url(:/side_btn/LightGCS_image/about.png);")
        self.gv_about.setObjectName("gv_about")
        self.stw_mainwindow = QtWidgets.QStackedWidget(self.centralWidget)
        self.stw_mainwindow.setGeometry(QtCore.QRect(3, 59, 1021, 711))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.stw_mainwindow.sizePolicy().hasHeightForWidth())
        self.stw_mainwindow.setSizePolicy(sizePolicy)
        self.stw_mainwindow.setObjectName("stw_mainwindow")
        self.stw_setter = QtWidgets.QWidget()
        self.stw_setter.setObjectName("stw_setter")
        self.tb_console = QtWidgets.QTextBrowser(self.stw_setter)
        self.tb_console.setEnabled(True)
        self.tb_console.setGeometry(QtCore.QRect(0, 340, 265, 371))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tb_console.sizePolicy().hasHeightForWidth())
        self.tb_console.setSizePolicy(sizePolicy)
        self.tb_console.setReadOnly(False)
        self.tb_console.setObjectName("tb_console")
        self.gb_setting = QtWidgets.QGroupBox(self.stw_setter)
        self.gb_setting.setGeometry(QtCore.QRect(0, 10, 261, 321))
        self.gb_setting.setObjectName("gb_setting")
        self.pb_accel = QtWidgets.QPushButton(self.gb_setting)
        self.pb_accel.setGeometry(QtCore.QRect(20, 110, 211, 35))
        self.pb_accel.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.pb_accel.setObjectName("pb_accel")
        self.pb_compass = QtWidgets.QPushButton(self.gb_setting)
        self.pb_compass.setGeometry(QtCore.QRect(20, 150, 211, 35))
        self.pb_compass.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.pb_compass.setObjectName("pb_compass")
        self.pb_radio = QtWidgets.QPushButton(self.gb_setting)
        self.pb_radio.setGeometry(QtCore.QRect(20, 190, 211, 35))
        self.pb_radio.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.pb_radio.setObjectName("pb_radio")
        self.pb_flt_mode = QtWidgets.QPushButton(self.gb_setting)
        self.pb_flt_mode.setGeometry(QtCore.QRect(20, 230, 211, 35))
        self.pb_flt_mode.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.pb_flt_mode.setObjectName("pb_flt_mode")
        self.pb_pid = QtWidgets.QPushButton(self.gb_setting)
        self.pb_pid.setGeometry(QtCore.QRect(20, 270, 211, 35))
        self.pb_pid.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.pb_pid.setObjectName("pb_pid")
        self.pb_firmware = QtWidgets.QPushButton(self.gb_setting)
        self.pb_firmware.setGeometry(QtCore.QRect(20, 30, 211, 35))
        self.pb_firmware.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.pb_firmware.setObjectName("pb_firmware")
        self.pb_frame = QtWidgets.QPushButton(self.gb_setting)
        self.pb_frame.setGeometry(QtCore.QRect(20, 70, 211, 35))
        self.pb_frame.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.pb_frame.setObjectName("pb_frame")
        self.stw_setter_sub = QtWidgets.QStackedWidget(self.stw_setter)
        self.stw_setter_sub.setGeometry(QtCore.QRect(280, 20, 731, 691))
        self.stw_setter_sub.setStyleSheet("")
        self.stw_setter_sub.setObjectName("stw_setter_sub")
        self.fw = QtWidgets.QWidget()
        self.fw.setObjectName("fw")
        self.fw_progressbar = QtWidgets.QProgressBar(self.fw)
        self.fw_progressbar.setGeometry(QtCore.QRect(10, 590, 721, 23))
        self.fw_progressbar.setProperty("value", 0)
        self.fw_progressbar.setObjectName("fw_progressbar")
        self.fw_upload_state = QtWidgets.QLabel(self.fw)
        self.fw_upload_state.setGeometry(QtCore.QRect(10, 550, 701, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fw_upload_state.setFont(font)
        self.fw_upload_state.setObjectName("fw_upload_state")
        self.gb_fw_online = QtWidgets.QGroupBox(self.fw)
        self.gb_fw_online.setGeometry(QtCore.QRect(0, 0, 751, 391))
        self.gb_fw_online.setObjectName("gb_fw_online")
        self.gv_wired_copter = QtWidgets.QGraphicsView(self.gb_fw_online)
        self.gv_wired_copter.setGeometry(QtCore.QRect(10, 30, 231, 161))
        self.gv_wired_copter.setObjectName("gv_wired_copter")
        self.gv_copter = QtWidgets.QGraphicsView(self.gb_fw_online)
        self.gv_copter.setGeometry(QtCore.QRect(10, 210, 231, 161))
        self.gv_copter.setObjectName("gv_copter")
        self.gv_wired_copter_3 = QtWidgets.QGraphicsView(self.gb_fw_online)
        self.gv_wired_copter_3.setGeometry(QtCore.QRect(510, 30, 221, 161))
        self.gv_wired_copter_3.setObjectName("gv_wired_copter_3")
        self.gv_wired_copter_4 = QtWidgets.QGraphicsView(self.gb_fw_online)
        self.gv_wired_copter_4.setGeometry(QtCore.QRect(510, 210, 221, 161))
        self.gv_wired_copter_4.setObjectName("gv_wired_copter_4")
        self.gv_fixed_wing = QtWidgets.QGraphicsView(self.gb_fw_online)
        self.gv_fixed_wing.setGeometry(QtCore.QRect(260, 30, 231, 161))
        self.gv_fixed_wing.setObjectName("gv_fixed_wing")
        self.gv_tiltrotor = QtWidgets.QGraphicsView(self.gb_fw_online)
        self.gv_tiltrotor.setGeometry(QtCore.QRect(260, 210, 231, 161))
        self.gv_tiltrotor.setObjectName("gv_tiltrotor")
        self.gb_fw_load = QtWidgets.QGroupBox(self.fw)
        self.gb_fw_load.setGeometry(QtCore.QRect(0, 400, 751, 91))
        self.gb_fw_load.setObjectName("gb_fw_load")
        self.comboBox = QtWidgets.QComboBox(self.gb_fw_load)
        self.comboBox.setGeometry(QtCore.QRect(90, 30, 271, 41))
        self.comboBox.setObjectName("comboBox")
        self.pb_custom_fw = QtWidgets.QPushButton(self.gb_fw_load)
        self.pb_custom_fw.setGeometry(QtCore.QRect(520, 20, 201, 61))
        self.pb_custom_fw.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.pb_custom_fw.setObjectName("pb_custom_fw")
        self.label_3 = QtWidgets.QLabel(self.gb_fw_load)
        self.label_3.setGeometry(QtCore.QRect(20, 40, 61, 31))
        self.label_3.setObjectName("label_3")
        self.stw_setter_sub.addWidget(self.fw)
        self.frame = QtWidgets.QWidget()
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(140, 200, 291, 121))
        self.label.setObjectName("label")
        self.stw_setter_sub.addWidget(self.frame)
        self.accel = QtWidgets.QWidget()
        self.accel.setObjectName("accel")
        self.textEdit_5 = QtWidgets.QTextEdit(self.accel)
        self.textEdit_5.setGeometry(QtCore.QRect(150, 200, 351, 87))
        self.textEdit_5.setObjectName("textEdit_5")
        self.stw_setter_sub.addWidget(self.accel)
        self.compass = QtWidgets.QWidget()
        self.compass.setObjectName("compass")
        self.textEdit_6 = QtWidgets.QTextEdit(self.compass)
        self.textEdit_6.setGeometry(QtCore.QRect(150, 230, 361, 87))
        self.textEdit_6.setObjectName("textEdit_6")
        self.stw_setter_sub.addWidget(self.compass)
        self.rc = QtWidgets.QWidget()
        self.rc.setObjectName("rc")
        self.textEdit_7 = QtWidgets.QTextEdit(self.rc)
        self.textEdit_7.setGeometry(QtCore.QRect(200, 220, 321, 87))
        self.textEdit_7.setObjectName("textEdit_7")
        self.stw_setter_sub.addWidget(self.rc)
        self.fltMode = QtWidgets.QWidget()
        self.fltMode.setObjectName("fltMode")
        self.textEdit_9 = QtWidgets.QTextEdit(self.fltMode)
        self.textEdit_9.setGeometry(QtCore.QRect(180, 210, 291, 87))
        self.textEdit_9.setObjectName("textEdit_9")
        self.stw_setter_sub.addWidget(self.fltMode)
        self.pid = QtWidgets.QWidget()
        self.pid.setObjectName("pid")
        self.textEdit_8 = QtWidgets.QTextEdit(self.pid)
        self.textEdit_8.setGeometry(QtCore.QRect(170, 220, 301, 87))
        self.textEdit_8.setObjectName("textEdit_8")
        self.stw_setter_sub.addWidget(self.pid)
        self.stw_mainwindow.addWidget(self.stw_setter)
        self.stw_status = QtWidgets.QWidget()
        self.stw_status.setObjectName("stw_status")
        self.textEdit_2 = QtWidgets.QTextEdit(self.stw_status)
        self.textEdit_2.setGeometry(QtCore.QRect(240, 280, 421, 87))
        self.textEdit_2.setObjectName("textEdit_2")
        self.stw_mainwindow.addWidget(self.stw_status)
        self.stw_logger = QtWidgets.QWidget()
        self.stw_logger.setObjectName("stw_logger")
        self.textEdit = QtWidgets.QTextEdit(self.stw_logger)
        self.textEdit.setGeometry(QtCore.QRect(250, 280, 421, 87))
        self.textEdit.setObjectName("textEdit")
        self.stw_mainwindow.addWidget(self.stw_logger)
        self.stw_params = QtWidgets.QWidget()
        self.stw_params.setObjectName("stw_params")
        self.pb_params_read = QtWidgets.QPushButton(self.stw_params)
        self.pb_params_read.setGeometry(QtCore.QRect(0, 390, 81, 51))
        self.pb_params_read.setObjectName("pb_params_read")
        self.pb_params_tree = QtWidgets.QPushButton(self.stw_params)
        self.pb_params_tree.setGeometry(QtCore.QRect(0, 240, 81, 51))
        self.pb_params_tree.setObjectName("pb_params_tree")
        self.pb_params_set = QtWidgets.QPushButton(self.stw_params)
        self.pb_params_set.setGeometry(QtCore.QRect(0, 290, 81, 51))
        self.pb_params_set.setObjectName("pb_params_set")
        self.pb_params_save = QtWidgets.QPushButton(self.stw_params)
        self.pb_params_save.setGeometry(QtCore.QRect(0, 340, 81, 51))
        self.pb_params_save.setObjectName("pb_params_save")
        self.stw_params_sub = QtWidgets.QStackedWidget(self.stw_params)
        self.stw_params_sub.setGeometry(QtCore.QRect(80, 20, 931, 691))
        self.stw_params_sub.setObjectName("stw_params_sub")
        self.stw_params_table = QtWidgets.QWidget()
        self.stw_params_table.setObjectName("stw_params_table")
        self.tv_params = QtWidgets.QTableView(self.stw_params_table)
        self.tv_params.setGeometry(QtCore.QRect(0, 0, 930, 690))
        self.tv_params.setAutoFillBackground(True)
        self.tv_params.setStyleSheet("")
        self.tv_params.setSortingEnabled(False)
        self.tv_params.setObjectName("tv_params")
        self.tv_params.horizontalHeader().setHighlightSections(False)
        self.tv_params.horizontalHeader().setSortIndicatorShown(False)
        self.tv_params.horizontalHeader().setStretchLastSection(False)
        self.stw_params_sub.addWidget(self.stw_params_table)
        self.stw_params_tree = QtWidgets.QWidget()
        self.stw_params_tree.setObjectName("stw_params_tree")
        self.label_2 = QtWidgets.QLabel(self.stw_params_tree)
        self.label_2.setGeometry(QtCore.QRect(420, 640, 91, 16))
        self.label_2.setObjectName("label_2")
        self.stw_params_sub.addWidget(self.stw_params_tree)
        self.pb_params_table = QtWidgets.QPushButton(self.stw_params)
        self.pb_params_table.setGeometry(QtCore.QRect(0, 190, 81, 51))
        self.pb_params_table.setObjectName("pb_params_table")
        self.stw_mainwindow.addWidget(self.stw_params)
        self.stw_exts = QtWidgets.QWidget()
        self.stw_exts.setObjectName("stw_exts")
        self.textEdit_4 = QtWidgets.QTextEdit(self.stw_exts)
        self.textEdit_4.setGeometry(QtCore.QRect(300, 290, 421, 87))
        self.textEdit_4.setObjectName("textEdit_4")
        self.stw_mainwindow.addWidget(self.stw_exts)
        self.cb_comm_name = QtWidgets.QComboBox(self.centralWidget)
        self.cb_comm_name.setGeometry(QtCore.QRect(780, 0, 135, 30))
        self.cb_comm_name.setObjectName("cb_comm_name")
        self.cb_comm_rate = QtWidgets.QComboBox(self.centralWidget)
        self.cb_comm_rate.setGeometry(QtCore.QRect(780, 35, 135, 30))
        self.cb_comm_rate.setObjectName("cb_comm_rate")
        self.pb_connection = QtWidgets.QPushButton(self.centralWidget)
        self.pb_connection.setGeometry(QtCore.QRect(920, 0, 101, 66))
        self.pb_connection.setStyleSheet("background-color: rgb(204, 255, 102);")
        self.pb_connection.setObjectName("pb_connection")
        self.label_mode = QtWidgets.QLabel(self.centralWidget)
        self.label_mode.setGeometry(QtCore.QRect(370, 10, 181, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_mode.sizePolicy().hasHeightForWidth())
        self.label_mode.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_mode.setFont(font)
        self.label_mode.setStyleSheet("color: rgb(85, 0, 255);")
        self.label_mode.setText("")
        self.label_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mode.setObjectName("label_mode")
        self.label_armed = QtWidgets.QLabel(self.centralWidget)
        self.label_armed.setGeometry(QtCore.QRect(560, 10, 181, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_armed.sizePolicy().hasHeightForWidth())
        self.label_armed.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_armed.setFont(font)
        self.label_armed.setStyleSheet("color: rgb(85, 0, 255);")
        self.label_armed.setText("")
        self.label_armed.setAlignment(QtCore.Qt.AlignCenter)
        self.label_armed.setObjectName("label_armed")
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.stw_mainwindow.setCurrentIndex(3)
        self.stw_setter_sub.setCurrentIndex(0)
        self.stw_params_sub.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LightGCS"))
        self.gb_setting.setTitle(_translate("MainWindow", "CALIBRATING"))
        self.pb_accel.setText(_translate("MainWindow", "Accelerator"))
        self.pb_compass.setText(_translate("MainWindow", "Magnetic"))
        self.pb_radio.setText(_translate("MainWindow", "Radio Controller"))
        self.pb_flt_mode.setText(_translate("MainWindow", "Flight Mode"))
        self.pb_pid.setText(_translate("MainWindow", "PID"))
        self.pb_firmware.setText(_translate("MainWindow", "Firmware"))
        self.pb_frame.setText(_translate("MainWindow", "Frame Type"))
        self.fw_upload_state.setText(_translate("MainWindow", "Firmware Upload Status"))
        self.gb_fw_online.setTitle(_translate("MainWindow", "Firmware Online"))
        self.gb_fw_load.setTitle(_translate("MainWindow", "Firmware Local"))
        self.pb_custom_fw.setText(_translate("MainWindow", "Custom Firmware"))
        self.label_3.setText(_translate("MainWindow", "本地固件"))
        self.label.setText(_translate("MainWindow", "Frame Type"))
        self.textEdit_5.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">加速度计校准</p></body></html>"))
        self.textEdit_6.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">罗盘校准</p></body></html>"))
        self.textEdit_7.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">遥控校准</p></body></html>"))
        self.textEdit_9.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">飞行模式设置</p></body></html>"))
        self.textEdit_8.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">PID调节</p></body></html>"))
        self.textEdit_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">飞机状态监控窗</p></body></html>"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">日志分析窗</p></body></html>"))
        self.pb_params_read.setText(_translate("MainWindow", "读取参数"))
        self.pb_params_tree.setText(_translate("MainWindow", "分组显示"))
        self.pb_params_set.setText(_translate("MainWindow", "写入参数"))
        self.pb_params_save.setText(_translate("MainWindow", "保存参数"))
        self.label_2.setText(_translate("MainWindow", "Tree View"))
        self.pb_params_table.setText(_translate("MainWindow", "列表显示"))
        self.textEdit_4.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">附加功能窗</p></body></html>"))
        self.pb_connection.setText(_translate("MainWindow", "CONNECT"))

import LightGCS_image_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

