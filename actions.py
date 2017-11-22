# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot, Qt, QEvent
from PyQt5.QtWidgets import QMainWindow,\
                            QFileDialog,\
                            QMessageBox,\
                            QButtonGroup, \
                            QComboBox


from Ui_MainWindow import Ui_MainWindow
from pymavlink import mavutil
from dronekit import connect
# from tools.sql_tool import *
# import os
# import time

# import csv

try:
    from PyQt5.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = type("")

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.initialise()

    def initialise(self):
        self.side_view_init()
        self.combobox_init()
        self.current_window_init()

        self.connection = False

    def current_window_init(self):
        self.gv_setter.setStyleSheet("border-image: url(:/side_btn/LightGCS_image/setter_pressed.png);")
        self.btns_flag = 1
        self.stw_mainwindow.setCurrentIndex(0)
        self.stw_setter_sub.setCurrentIndex(0)

    def side_view_init(self):
        # flag for main window btns:
        # 0 for none
        # 1 for first
        # 2 for second
        # ...
        self.btns_flag = 0

        # register event filter for all btns
        gv_btns = [self.gv_setter,  self.gv_monitor, self.gv_logger,  self.gv_params,  self.gv_exts]
        gv_btns_images = [(1, "border-image: url(:/side_btn/LightGCS_image/setter.png);", \
                                            "border-image: url(:/side_btn/LightGCS_image/setter_on.png);" , \
                                            "border-image: url(:/side_btn/LightGCS_image/setter_pressed.png);"), \
                                        (2,  "border-image: url(:/side_btn/LightGCS_image/monitor.png);", \
                                            "border-image: url(:/side_btn/LightGCS_image/monitor_on.png);" , \
                                            "border-image: url(:/side_btn/LightGCS_image/monitor_pressed.png);"), \
                                        (3,  "border-image: url(:/side_btn/LightGCS_image/logger.png);", \
                                            "border-image: url(:/side_btn/LightGCS_image/logger_on.png);",  \
                                            "border-image: url(:/side_btn/LightGCS_image/logger_pressed.png);"),\
                                        (4, "border-image: url(:/side_btn/LightGCS_image/params.png);", \
                                            "border-image: url(:/side_btn/LightGCS_image/params_on.png);" , \
                                            "border-image: url(:/side_btn/LightGCS_image/params_pressed.png);"), \
                                        (5, "border-image: url(:/side_btn/LightGCS_image/exts.png);", \
                                            "border-image: url(:/side_btn/LightGCS_image/exts_on.png);" , \
                                            "border-image: url(:/side_btn/LightGCS_image/exts_pressed.png);")
                                        ]
        self.gv_btns_res = dict(zip(gv_btns,  gv_btns_images))

        # register group view icon event filter
        for item in self.gv_btns_res.keys():
            item.installEventFilter(self)

        # main window: setter view event
        self.gv_setter_init()
        self.gv_logger.mousePressEvent = self.on_logger_mouseClicked
        self.gv_monitor.mousePressEvent = self.on_monitor_mouseClicked
        self.gv_params.mousePressEvent = self.on_params_mouseClicked
        self.gv_exts.mousePressEvent = self.on_exts_mouseClicked


    def gv_setter_init(self):
        """
        add push button here
        """
        self.gv_setter.mousePressEvent = self.on_setter_mouseClicked
        self.setter_btns = [self.pb_firmware,\
                            self.pb_frame,\
                            self.pb_accel,\
                            self.pb_compass,\
                            self.pb_radio,\
                            self.pb_flt_mode,\
                            self.pb_pid,\
                            self.pb_peripheral]
        self.setter_btn_clicked(self.pb_firmware)

    def setter_btn_clicked(self,obj):
        self.setter_btn_reset()
        obj.setStyleSheet("background-color: rgb(0,170,0)")
        idx = self.setter_btns.index(obj)
        self.stw_setter_sub.setCurrentIndex(idx)

    def setter_btn_reset(self):
        for item in self.setter_btns:
            item.setStyleSheet("background-color: rgb(225, 225, 225);\ncolor: rgb(0, 0, 0);")

    def combobox_init(self):
        self.combobox_port_init()
        self.combobox_baudrate_init()

        self.motor_db_combobox_init()

    def find_ports(self):
        self.preferred_list=['*FTDI*',"*Arduino_Mega_2560*", "*3D_Robotics*", "*USB to UART*", '*PX4*', '*FMU*']
        self.serial_list = mavutil.auto_detect_serial(self.preferred_list)
        if self.serial_list:
            pass
        else:
            self.serial_list = mavutil.auto_detect_serial()
            for port in self.serial_list:
                # print port.__dict__
                if 'Virtual' in port.description:
                    self.serial_list.remove(port)

        try:
            self.serial_list_device = []
            for item in self.serial_list:
                self.serial_list_device.append(item.device)
        except Exception as e:
            pass

    def combobox_port_update(self):
        self.cb_comm_name.clear()
        self.find_ports()
        if self.serial_list_device:
            self.cb_comm_name.addItems(self.serial_list_device)
            if len(self.serial_list_device) == 1:
                self.cb_comm_name.setCurrentText(self.serial_list_device[0])
        else:
            self.cb_comm_name.addItem("No FMU PORT")
            self.cb_comm_name.setCurrentText("No FMU PORT")


    def combobox_port_init(self):
        # register com port event filter
        self.cb_comm_name.installEventFilter(self)
        self.combobox_port_update()

    def combobox_baudrate_init(self):
        self.serial_baud = ["1200", "2400", "4800", "9600", "38400", "57600", "111100", "115200", "500000", "921600", "1500000"]
        self.cb_comm_rate.addItems(self.serial_baud)
        self.cb_comm_rate.setCurrentIndex(7)

    def eventFilter(self, obj, e):
        if obj in self.gv_btns_res.keys():
            values = self.gv_btns_res.get(obj)
            if not self.btns_flag == values[0]:
                if e.type() == QEvent.Enter:
                    obj.setStyleSheet(values[2]) # e.g. setter_on.png
                    return True
                elif e.type() == QEvent.Leave:
                    obj.setStyleSheet(values[1]) # e.g. setter.png
                    return True

        if obj == self.cb_comm_name:
            if e.type() == QEvent.MouseButtonPress:
                self.combobox_port_update()
                return False

        if obj in self.motorCbs:
            if e.type() == QEvent.MouseButtonPress:
                self.motor_data_combobox_update(obj)
                return False
        return False

    def reset_gv_btns_icon(self):
        for item, values in self.gv_btns_res.items():
            item.setStyleSheet(values[1])

    def on_mouse_pressed_gv_btns(self, obj, e):
        if Qt.LeftButton== e.button():
            self.reset_gv_btns_icon()
            values = self.gv_btns_res.get(obj)
            self.btns_flag = values[0]
            obj.setStyleSheet(values[3])
            self.stw_mainwindow.setCurrentIndex(self.btns_flag-1)

    def on_setter_mouseClicked(self, e):
        self.on_mouse_pressed_gv_btns(self.gv_setter, e)

    def on_logger_mouseClicked(self, e):
        self.on_mouse_pressed_gv_btns(self.gv_logger, e)
#        self.stw_mainwindow.setCurrentIndex(1)

    @pyqtSlot()
    def on_pb_read_log_clicked(self):
        self.read_data_flash_file()

    def on_monitor_mouseClicked(self, e):
        self.on_mouse_pressed_gv_btns(self.gv_monitor, e)

    def on_params_mouseClicked(self, e):
        self.on_mouse_pressed_gv_btns(self.gv_params, e)

    def on_exts_mouseClicked(self, e):
        self.on_mouse_pressed_gv_btns(self.gv_exts, e)
        self.exts_window_init()

    @pyqtSlot()
    def on_pb_params_table_clicked(self):
        self.stw_params_sub.setCurrentIndex(0)
        if not self.connection:
            return
        self.table_view_init()

    @pyqtSlot(QString)
    def on_cb_comm_name_currentIndexChanged(self, p0):
        self.current_port = p0

    @pyqtSlot(QString)
    def on_cb_comm_rate_currentIndexChanged(self, p0):
        self.current_baud = int(p0)

    def pb_connection_reset(self):
        self.pb_connection.setText("未连接")
        self.pb_connection.setStyleSheet("background-color: rgb(204, 204, 102);\ncolor: rgb(0,0,0)")

    @pyqtSlot()
    def on_pb_connection_clicked(self):
        if not self.serial_list:
            self.tb_console.append(self.cb_comm_name.currentText()+" No Valid FMU!")
            # print self.cb_comm_name.currentText()
            return False
        port = self.cb_comm_name.currentText()
        if not port in self.serial_list_device:
            return False

        if not self.connection:
            try:
                self.vehicle = connect(port,  wait_ready=True, status_printer = self.tb_console.append, baud=int(self.cb_comm_rate.currentText()))
            except Exception as e:
                self.vehicle = None
                # print str(e)

            if self.vehicle:
                self.connection = True
                self.pb_connection.setText("已连接")
                self.pb_connection.setStyleSheet("background-color: rgb(51, 153, 51);")
            else:
                self.pb_connection_reset()
        else:
            self.pb_connection_reset()
            self.connection = False
            self.vehicle.close()

    @pyqtSlot()
    def on_pb_firmware_clicked(self):
        """
        Upload mav firmware to flight board
        """
        self.setter_btn_clicked(self.pb_firmware)

    @pyqtSlot()
    def on_pb_frame_clicked(self):
        """
        Set mav frame class or type
        """
        self.setter_btn_clicked(self.pb_frame)

    @pyqtSlot()
    def on_pb_accel_clicked(self):
        """
        enter accelerator calibrating window
        """
        self.setter_btn_clicked(self.pb_accel)

    @pyqtSlot()
    def on_pb_compass_clicked(self):
        """
        enter compass calibrating window
        """
        self.setter_btn_clicked(self.pb_compass)

    @pyqtSlot()
    def on_pb_radio_clicked(self):
        """
        enter rc calibrating window
        """
        self.setter_btn_clicked(self.pb_radio)

    @pyqtSlot()
    def on_pb_flt_mode_clicked(self):
        """
        enter flight mode setting window
        """
        self.setter_btn_clicked(self.pb_flt_mode)

    @pyqtSlot()
    def on_pb_pid_clicked(self):
        """
        enter pid params window
        """
        self.setter_btn_clicked(self.pb_pid)

    @pyqtSlot()
    def on_pb_copter_pid_screen_clicked(self):
        """
        read fixedwing pid params
        """
        pass

        # import setting.pid_params
    @pyqtSlot()
    def on_pb_fixedwing_pid_screen_clicked(self):
        """
        read fixedwing pid params
        """
        if not self.connection:
            return

        from setting import pid_params
        pid_params.fwPID(self.vehicle.parameters, self.f_pid)

    @pyqtSlot()
    def on_pb_peripheral_clicked(self):
        """
        Slot documentation goes here.
        """
        self.setter_btn_clicked(self.pb_peripheral)

    @pyqtSlot()
    def on_pb_custom_fw_clicked(self):
        self.custom_fw_select_event()

    def exts_window_init(self):
        self.ext_btns_init()

    def ext_btns_init(self):
        self.ext_btns = QButtonGroup(self)
        self.ext_btns.setExclusive(True)

        # 附加功能选项按顺序添加到此列表
        ext_btns_list = [self.rb_xrotor_calc,self.rb_fixedwing_calc,self.rb_tiltrotor_calc,self.rb_rotor_database,self.rb_foc_esc]

        for i in range(len(ext_btns_list)):
            self.ext_btns.addButton(ext_btns_list[i])
            self.ext_btns.setId(ext_btns_list[i],i)

        self.ext_btns.buttonClicked.connect(self.ext_btns_update)

        self.rb_xrotor_calc.setChecked(True)
        self.stw_exts_sub.setCurrentIndex(0)
        self.xrotor_params_init()

    def ext_btns_update(self, button):
        id = self.ext_btns.checkedId()
        self.stw_exts_sub.setCurrentIndex(id)

        if id == 0 and not "xrotor_initialised" in self.__dict__:
            self.xrotor_params_init()
        elif id == 1 and not "fixed_wing_initialised" in self.__dict__:
            self.fixed_wing_params_init()
        elif id == 2 and not "tilt_rotor_initialised" in self.__dict__:
            self.tilt_rotor_params_init()
        elif id == 3 and not "motor_db_initialised" in self.__dict__:
            self.motor_db_init()
        elif id == 4 and not "foc_esc_initialised" in self.__dict__:

            pass
        else:
            pass

    @pyqtSlot()
    def on_pb_xrotor_calc_clicked(self):
        self.copter_estimator()

    @pyqtSlot()
    def on_pb_xrotor_reset_clicked(self):
        """
        Slot documentation goes here.
        """
        for i in range(len(self.xrotor_params)):
            if isinstance(self.xrotor_params[i],QComboBox):
                self.xrotor_params[i].setCurrentText("")
            else:
                self.xrotor_params[i].setText("")


    def fixed_wing_params_init(self):
        """
        固定翼机评估部分
        """
        self.fixed_wing_initialised = True


    def tilt_rotor_params_init(self):
        """
        倾旋翼机评估部分
        """
        self.tilt_rotor_initialised = True

    @pyqtSlot()
    def on_pb_motor_db_doc_select_clicked(self):
        """
        Slot documentation goes here.
        """
        self.motor_dir = QFileDialog.getExistingDirectory(self, "选择电机测试数据目录", \
                                                    "",\
                                                    QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        self.label_motor_db_path.setText(self.motor_dir)

    @pyqtSlot()
    def on_pb_motor_db_file_read_clicked(self):
        self.motor_db_file_read_event()

    @pyqtSlot()
    def on_pb_motor_db_file_insert_clicked(self):
        self.motor_db_file_insert_event()


    @pyqtSlot()
    def on_pb_motor_db_file_remove_clicked(self):
        self.motor_db_file_remove_event()


    @pyqtSlot()
    def on_pb_csv_template_clicked(self):
        self.csv_template_event()

    @pyqtSlot()
    def on_pb_motor_db_insert_confirm_clicked(self):
        self.motor_db_insert_confirm_event()

    @pyqtSlot(QString)
    def on_cb_motor_db_productor_currentTextChanged(self, p0):
        self.motorCbValues[0] = p0

    @pyqtSlot(QString)
    def on_cb_motor_db_type_currentTextChanged(self, p0):
        self.motorCbValues[1] = p0

    @pyqtSlot(QString)
    def on_cb_motor_db_kv_currentTextChanged(self, p0):
        self.motorCbValues[2] = p0

    @pyqtSlot(QString)
    def on_cb_motor_db_propeller_currentTextChanged(self, p0):
        self.motorCbValues[3] = p0

    @pyqtSlot(QString)
    def on_cb_motor_db_volt_currentTextChanged(self, p0):
        self.motorCbValues[4] = p0

    @pyqtSlot()
    def on_pb_motor_data_sql_clicked(self):
        self.motor_data_sql_event()

    @pyqtSlot()
    def on_pb_motor_table_show_clicked(self):
        self.motor_table_show_event()

    @pyqtSlot()
    def on_pb_motor_db_update_clicked(self):
        self.motor_table_view_model.database().transaction() #开始事务操作
        if self.motor_table_view_model.submitAll():
           self.motor_table_view_model.database().commit() #提交
        else:
           self.motor_table_view_model.database().rollback() #回滚
           QMessageBox.warning(self, "tableModel",\
                                     "数据库错误: {}".format(self.motor_table_view_model.lastError().text()))

    @pyqtSlot()
    def on_pb_motor_db_insert_row_clicked(self):
        pass

    @pyqtSlot()
    def on_pb_motor_db_delete_row_clicked(self):
        pass

def wonf(f):
    """
    referrence to waf conf decorator
    Decorator: attach new functions to MainWindow class
    :param f: method to bind
    :return:
    """
    def fun(*k,**kw):
        return f(*k,**kw)

    fun.__name__ = f.__name__
    setattr(MainWindow, f.__name__, fun)
    return f



import setting
import monitor
import logger
import parameters
import tools


