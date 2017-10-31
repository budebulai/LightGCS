# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot, Qt, QEvent
from PyQt5.QtWidgets import QApplication, \
                            QMainWindow,\
                            QFileDialog,\
                            QHeaderView, \
                            QMessageBox,\
                            QButtonGroup, \
                            QComboBox

from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtSql import QSqlTableModel,QSqlDatabase
from Ui_MainWindow import Ui_MainWindow
from pymavlink import mavutil
from dronekit import connect
from setting.px4_uploader import firmware,uploader
from ext_tools.sql_tool import *
import os
import time
import threading
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
        self.gv_setter.mousePressEvent = self.on_setter_mouseClicked
        self.setter_btns = [self.pb_firmware,self.pb_frame,self.pb_accel,self.pb_compass,self.pb_radio,self.pb_flt_mode,self.pb_pid]
        self.setter_btn_clicked(self.pb_firmware)

    def setter_btn_clicked(self,obj):
        self.setter_btn_reset()
        obj.setStyleSheet("background-color: rgb(0,170,0)")
        idx = self.setter_btns.index(obj)
        self.stw_setter_sub.setCurrentIndex(idx)

    def setter_btn_reset(self):
        for item in self.setter_btns:
            item.setStyleSheet("background-color: rgb(225,225,225)")

    def combobox_init(self):
        self.combobox_port_init()
        self.combobox_baudrate_init()

        self.motor_db_combobox_init()


    def find_ports(self):
        self.preferred_list=['*FTDI*',"*Arduino_Mega_2560*", "*3D_Robotics*", "*USB to UART*", '*PX4*', '*FMU*']
        self.serial_list = mavutil.auto_detect_serial(self.preferred_list)
        if self.serial_list:
            self.serial_list_device = []
            for item in self.serial_list:
                self.serial_list_device.append(item.device)

    def combobox_port_update(self):
        self.cb_comm_name.clear()
        self.find_ports()
        if self.serial_list:
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

    def on_monitor_mouseClicked(self, e):
        self.on_mouse_pressed_gv_btns(self.gv_monitor, e)

    def on_params_mouseClicked(self, e):
        self.on_mouse_pressed_gv_btns(self.gv_params, e)

    def on_exts_mouseClicked(self, e):
        self.on_mouse_pressed_gv_btns(self.gv_exts, e)
        self.exts_window_init()

    @pyqtSlot()
    def on_pb_params_table_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.stw_params_sub.setCurrentIndex(0)
        if not self.connection:
            return
        self.table_view_init()

    def table_view_init(self):

        #设置行背景交替色
        self.tv_params.setAlternatingRowColors(True);
        self.tv_params.setStyleSheet("{background-color: rgb(255, 255, 255);" "alternate-background-color: rgb(225, 225, 225);}");

        self.table_view_model = QStandardItemModel(self.tv_params)

        #设置表格属性：
        self.params_length = len(self.vehicle.parameters)
        self.table_view_model.setRowCount(self.params_length)
        self.table_view_model.setColumnCount(5)

        #设置表头
        self.table_view_model.setHeaderData(0,Qt.Horizontal,"Name")
        self.table_view_model.setHeaderData(1,Qt.Horizontal,"Value")
        self.table_view_model.setHeaderData(2,Qt.Horizontal,"Unit")
        self.table_view_model.setHeaderData(3,Qt.Horizontal,"Limit")
        self.table_view_model.setHeaderData(4,Qt.Horizontal,"Description")
        #设置表头背景色
        self.tv_params.horizontalHeader().setStyleSheet("QHeaderView.section{background-color:red}");

        #隐藏侧边序号
        self.tv_params.verticalHeader().setHidden(True)

        self.tv_params.setModel(self.table_view_model)

        #设置列宽
        # self.tv_params.setColumnWidth(0,200)
        # self.tv_params.setColumnWidth(1,100)
        # self.tv_params.setColumnWidth(2,100)
        # self.tv_params.setColumnWidth(3,150)
        # self.tv_params.setColumnWidth(4,360)

        #下面代码让表格100填满窗口
        self.tv_params.horizontalHeader().setStretchLastSection(True)
        self.tv_params.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #表头信息显示居左
        self.tv_params.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        self.params_table_view_update()

        #按参数字母排序
        self.tv_params.sortByColumn(0, Qt.AscendingOrder)

        self.tv_params.resizeColumnToContents(0)
        self.tv_params.resizeColumnToContents(1)

    def params_table_view_update(self):

        idx = 0
        EDITABLE_FLAG = Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled
        NOTEDITABLE_FLAG = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        for key, value in self.vehicle.parameters.iteritems():
            #填充内容
            self.table_view_model.setItem(idx,0,QStandardItem(key))
            self.table_view_model.setItem(idx,1,QStandardItem(str(value)))
            self.table_view_model.setItem(idx,2,QStandardItem(""))
            self.table_view_model.setItem(idx,3,QStandardItem(""))
            self.table_view_model.setItem(idx,4,QStandardItem(""))

            #设置第二列数据可编辑
            self.table_view_model.item(idx,0).setFlags(NOTEDITABLE_FLAG)
            self.table_view_model.item(idx,1).setFlags(EDITABLE_FLAG)
            self.table_view_model.item(idx,2).setFlags(NOTEDITABLE_FLAG)
            self.table_view_model.item(idx,3).setFlags(NOTEDITABLE_FLAG)
            self.table_view_model.item(idx,4).setFlags(NOTEDITABLE_FLAG)

            idx += 1

    @pyqtSlot(QString)
    def on_cb_comm_name_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.

        @param p0 DESCRIPTION
        @type QString
        """
        # TODO: not implemented yet
        self.current_port = p0

    @pyqtSlot(QString)
    def on_cb_comm_rate_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.

        @param p0 DESCRIPTION
        @type QString
        """
        # TODO: not implemented yet
        self.current_baud = int(p0)

    def pb_connection_reset(self):
        self.pb_connection.setText("CONNECT")
        self.pb_connection.setStyleSheet("background-color: rgb(204, 255, 102)")

    @pyqtSlot()
    def on_pb_connection_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if not self.serial_list:
            self.print_info(self.cb_comm_name.currentText())
#            print self.cb_comm_name.currentText()
            return False
        port = self.cb_comm_name.currentText()
        if not port in self.serial_list_device:
            return False

        if not self.connection:
            self.vehicle = connect(port,  baud=int(self.cb_comm_rate.currentText()), wait_ready=True, status_printer = self.tb_console.append)

            if self.vehicle:
                self.connection = True
                self.pb_connection.setText("CONNECTED")
                self.pb_connection.setStyleSheet("background-color: rgb(51, 153, 51)")
            else:
                self.pb_connection_reset()
        else:
            self.pb_connection_reset()
            self.connection = False
            self.vehicle.close()

    @pyqtSlot()
    def on_pb_firmware_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.setter_btn_clicked(self.pb_firmware)

    @pyqtSlot()
    def on_pb_frame_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.setter_btn_clicked(self.pb_frame)

    @pyqtSlot()
    def on_pb_accel_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.setter_btn_clicked(self.pb_accel)

    @pyqtSlot()
    def on_pb_compass_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.setter_btn_clicked(self.pb_compass)

    @pyqtSlot()
    def on_pb_radio_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.setter_btn_clicked(self.pb_radio)

    @pyqtSlot()
    def on_pb_flt_mode_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.setter_btn_clicked(self.pb_flt_mode)

    @pyqtSlot()
    def on_pb_pid_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.setter_btn_clicked(self.pb_pid)

    @pyqtSlot()
    def on_pb_custom_fw_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        opt = QFileDialog.Options()
        # opt |= QFileDialog.DontUseNativeDialog
        fp, _ = QFileDialog.getOpenFileName(self, "选择固件", "", "APM Firmware Files (*.px4;*.elf);;All Files (*)", options = opt)

        if not fp:
            self.upload_state_update("No Valid Firmware!")
            return
        #运行一次，防止飞控强制断开，如断开USB线
        self.upload_complete = False
        self.combobox_port_update()
        fw_thread = threading.Thread(target=self.firmware_uploader,args=(fp,))
        fw_thread.setDaemon(True)
        fw_thread.start()

        if self.upload_complete:
            fw_thread.join()

    def firmware_uploader(self,fp):
        if self.connection:
            self.upload_state_update("Please unconnect apm!")
            return

        if not self.serial_list:
            count = 0
            while count < 30 and not self.serial_list:
                time.sleep(1)
                count += 1
                info = "Plugin flight controller board, remaining: %s s"%(30 - count)
                self.upload_state_update(info)
                self.combobox_port_update()
            if count >= 30:
                self.upload_state_update("Time Out!")
                return

        self.upload_state_update(fp)
        # self.print_info(fp)
        # Load the firmware file
        fw = firmware(fp)
        self.upload_state_update(fw.description)
        count = 0
        while count < 60:
            # Spin waiting for a device to show up
            try:
                baud = 115200
                for port in self.serial_list_device:
                    self.print_info("try open port: %s, baud:%s"%(port,str(baud)))
                    # create an uploader attached to the port
                    try:
                        # Windows, don't open POSIX ports
                        up = uploader(port, baud)
                    except Exception:
                        # open failed, rate-limit our attempts
                        self.print_info("Open port failed! Unplug and re-plug the USB connector.")
                        time.sleep(0.05)
                        continue

                    # port is open, try talking to it
                    try:
                        # identify the bootloader
                        up.identify()
                    except Exception:
                        # most probably a timeout talking to the port, no bootloader, try to reboot the board
                        self.print_info("attempting reboot on %s..." % port)
                        self.print_info("if the board does not respond, unplug and re-plug the USB connector.")
                        up.send_reboot()
                        # wait for the reboot, without we might run into Serial I/O Error 5
                        time.sleep(0.5)
                        # always close the port
                        up.close()
                        continue

                    try:
                        if (up.bl_rev < uploader.BL_REV_MIN) or (up.bl_rev > uploader.BL_REV_MAX):
                            msg = "Unsupported bootloader protocol %d" % uploader.INFO_BL_REV
                            raise RuntimeError(msg)
                        # Make sure we are doing the right thing
                        elif up.board_type != fw.property('board_id'):
                            msg = "Firmware not suitable for this board (board_type=%u board_id=%u)" % (up.board_type, fw.property('board_id'))
                            raise RuntimeError(msg)
                        elif up.fw_maxsize < fw.property('image_size'):
                            msg = "Firmware image is too large for this board"
                            raise RuntimeError(msg)
                        # elif 板载固件hash值与欲烧录的固件hash值一致，返回，不重复下载
                    except RuntimeError as e:
                            time.sleep(0.05)
                            up.close()
                            self.upload_state_update("WARNING:"+str(e))
                            self.upload_complete = True
                            return

                    up.detect()

                    self.upload_state_update("Found board %s, bootloader rev %x on %s" % (up.otp_id.decode('Latin-1'), up.bl_rev, port))
                    # self.print_info("Found board %x,%x bootloader rev %x on %s" % (up.board_type, up.board_rev, up.bl_rev, port))
                    start = time.time()
                    try:
                        label = "Erase Flash"
                        # ok, we have a bootloader, try flashing it
                        up.erase()
                        # erase is very slow, give it 20s
                        deadline = time.time() + 20.0
                        while time.time() < deadline:
                            #Draw progress bar (erase usually takes about 9 seconds to complete)
                            # stucked often
                            estimatedTimeRemaining = deadline - time.time()
                            if estimatedTimeRemaining >= 9.0:
                                self.drawProgressBar(label, 20.0-estimatedTimeRemaining, 9.0)
                            else:
                                label = "timeout: %d seconds" % int(deadline-time.time())
                                self.drawProgressBar(label, 10.0, 10.0)
                            if up.trySync():
                                label = "Erase Done. Programing..."
                                self.drawProgressBar(label, 10.0, 10.0)
                                break
                        else:
                            raise RuntimeError("timed out waiting for erase")

                    except RuntimeError as ex:
                        # print the error
                        self.upload_state_update("ERROR: %s" % str(ex))
                        up.close()
                        continue
                    except IOError:
                        up.close()
                        continue

                    try:
                        up.program(fw)
                        label = "Program Done. Verifing..."
                        self.drawProgressBar(label, 100, 100)

                        if up.bl_rev == 2:
                            up.verify_v2(fw)
                        else:
                            up.verify_v3(fw)
                        label = "Done"
                        self.drawProgressBar(label, 100, 100)
                        sec = time.time() - start

                    except RuntimeError as ex:
                        # print the error
                        self.upload_state_update("ERROR: %s" % str(ex))
                        up.close()
                    except IOError:
                        up.close()
                    finally:
                        up.reboot()
                        # always close the port
                        up.close()
                        print "time for uploading firmware : %f s"%(sec)
                        self.upload_complete = True
                        return

            # CTRL+C aborts the upload/spin-lock by interrupt mechanics
            except KeyboardInterrupt:
                print("Upload aborted by user.")
                self.upload_complete = True
                return False
            # px4_uploader.px4_uploader(self,fp,self.serial_list_device,self.current_baud)
            # Delay retries to < 20 Hz to prevent spin-lock from hogging the CPU
            time.sleep(0.05)
            count += 1
        self.upload_state_update("Time Out")
        self.upload_complete = True


    def print_info(self,str):
        self.tb_console.append(str)

    def upload_state_update(self,str):
        self.fw_upload_state.setText(str)

    def drawProgressBar(self,label,progress,maxVal):
        if maxVal < progress:
            progress = maxVal

        percent = int(float(progress) / float(maxVal) * 100)
        self.fw_upload_state.setText(label)
        self.fw_progressbar.setValue(percent)

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

        if id == 1 and not "fixed_wing_initialised" in self.__dict__:
            self.fixed_wing_params_init()
        elif id == 2 and not "tilt_rotor_initialised" in self.__dict__:
            self.tilt_rotor_params_init()
        elif id == 3 and not "motor_db_initialised" in self.__dict__:
            self.motor_db_init()
        elif id == 4 and not "foc_esc_initialised" in self.__dict__:

            pass
        else:
            pass

    def xrotor_estimate(self, params):
        from ext_tools import xrotor_estimator
        xrotor_estimator.xrotor_estimate(params)

    @pyqtSlot()
    def on_pb_xrotor_calc_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # get params
        param_values = []
        for i in range(len(self.xrotor_params)):
            if isinstance(self.xrotor_params[i],QComboBox):
                param_values.append(self.xrotor_params[i].currentText())
            else:
                param_values.append(self.xrotor_params[i].text())
        params = dict(zip(self.xrotor_params_key, param_values))

        if self.check_xrotor_params(params):
            xrotor_estimate_thread = threading.Thread(target=self.xrotor_estimate,args=(params,))
            xrotor_estimate_thread.setDaemon(True)
            xrotor_estimate_thread.start()
        else:
            """
            StandardButton QMessageBox::critical(
                QWidget *parent,
                const QString &title,
                const QString &text,
                StandardButtons buttons = Ok,
                StandardButton defaultButton = NoButton)
            """
            mb_text = "You have selected parameters below"
            for key,value in params.items():
                key += ":\t"+str(value)
                mb_text += "\n"+key
            QMessageBox.critical(self, "Parameters Invalid", mb_text)

    def check_xrotor_params(self, params):
        if not (params["weight"] and params["frame"] and params["motor"] and params["propeller"]):
            print "saf"
            return False
        try:
            "convert string weight to int"
            params["weight"] = int(params["weight"])
            assert params["weight"] > 0

            for i in range(len(self.xrotor_params_key)):
                if isinstance(self.xrotor_params[i],QComboBox):
                    continue
                if params[self.xrotor_params_key[i]]:
                    params[self.xrotor_params_key[i]] = float(params[self.xrotor_params_key[i]])
                    if self.xrotor_params_key[i] == "temperature":
                        continue
                    assert params[self.xrotor_params_key[i]] > 0

        except Exception:
            return False
        return True

    def xrotor_params_init(self):
        """
        Init xrotor groupbox all QCombobox
        """
        # db table init
        create_table_motorList()
        create_table_motorData()
        create_table_motorInfo()
        create_table_propellerInfo()

        self.xrotor_params = [self.le_weight,\
                              self.cb_copter_frame,\
                              self.le_uav_axisDist,\
                              self.le_flight_height,\
                              self.le_ground_temperature,\
                              self.cb_motor_type,\
                              self.cb_prop_type,\
                              self.cb_volt,\
                              self.le_battery_capacity,\
                              self.le_capacity_residual]
        self.xrotor_params_key = ["weight",\
                                  "frame",\
                                  "axisDist",\
                                  "height",\
                                  "temperature",\
                                  "motor",\
                                  "propeller",\
                                  "voltage",\
                                  "capacity",\
                                  "residual"]

        self.cb_copter_frame.clear()
        self.cb_copter_frame.addItems(["","Quad","Hexa","Octo"])

        params = {"table":"motorData"}
        params["fields"] = ["Motor","Propeller"]
        ret = table_query(params)

        motors = set([item[0] for item in ret if item[0]])
        propellers = set([str(item[1]) for item in ret if item[1]])

        self.cb_motor_type.clear()
        self.cb_motor_type.addItem("")
        self.cb_motor_type.addItems(motors)
        self.cb_prop_type.clear()
        self.cb_prop_type.addItem("")
        self.cb_prop_type.addItems(propellers)

        volt_list = [""]
        for i in range(2,13):
            item = "{}S--{:.1f}V".format(i,i*3.7)
            volt_list.append(item)
        self.cb_volt.clear()
        self.cb_volt.addItems(volt_list)

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

    """
    固定翼机评估部分
    """
    def fixed_wing_params_init(self):
        self.fixed_wing_initialised = True
        pass

    """
    倾旋翼机评估部分
    """
    def tilt_rotor_params_init(self):
        self.tilt_rotor_initialised = True
        pass

    """
    电机数据库部分
    """
    def motor_db_combobox_init(self):
        self.motorCbs = (self.cb_motor_db_productor,\
                    self.cb_motor_db_type,\
                    self.cb_motor_db_kv,\
                    self.cb_motor_db_propeller,\
                    self.cb_motor_db_volt)

        for item in self.motorCbs:
            item.installEventFilter(self)

        self.motorCbKeys = ("Producer","Type","KV","Propeller","Voltage")

        self.motorCbValues = [str(cb.currentText()) for cb in self.motorCbs]

    def motor_db_init(self):
        tables = [item for items in show_tables() for item in items]
        self.cb_motor_tables.clear()
        self.cb_motor_tables.addItems(tables)
        self.cb_motor_tables.setCurrentIndex(0)

        self.motor_table_view_model = self.create_sql_table_model()
        self.motor_table_view_init(self.tv_motor_tables)
        self.motor_table_view_init(self.tv_motor_data)
        self.motor_db_initialised = True

    def motor_data_combobox_update(self,obj):
        """
        self.motorCbs = (self.cb_motor_db_productor,\
                    self.cb_motor_db_type,\
                    self.cb_motor_db_kv,\
                    self.cb_motor_db_propeller,\
                    self.cb_motor_db_volt)
        self.motorCbKeys = ("Producer","Type","KV","Propeller","Voltage")

        self.motorCbValues = [str(cb.currentText()) for cb in self.motorCbs]
        """
        motorInfoCondition = []
        motorDataCondition = []
        idx = self.motorCbs.index(obj)
        for i in range(len(self.motorCbs)):
            if not self.motorCbValues[i]:
                continue
            if i > 2:
                motorDataCondition.append("{}={}".format(self.motorCbKeys[i],self.motorCbValues[i]))
            else:
                motorInfoCondition.append("{}='{}'".format(self.motorCbKeys[i],self.motorCbValues[i]))

        params = {"table":"motorInfo"}
        params["fields"] = ["Motor","Producer","Type","KV"]
        params["condition"] = " AND ".join(motorInfoCondition)
        values = table_query(params)
        motors = set([str(item[0]) for item in values if item[0]])

        if idx >= 3: # Propeller ---> motorData
            params = {"table":"motorData"}
            params["fields"] = ["Motor","Propeller","Voltage"]
            if len(motors) == 1:
                motorDataCondition.append("Motor = '{}'".format(list(motors)[0]))
            else:
                motorDataCondition.append("Motor IN {}".format(tuple(motors)))
            params["condition"] = " AND ".join(motorDataCondition)

            values = table_query(params)
            items = set([str(item[idx-2]) for item in values if item[idx-2]])
        else:
            items = set([str(item[idx+1]) for item in values if item[idx+1]])

        obj.clear()
        obj.addItem("")
        obj.addItems(items)

    def create_sql_table_model(self):
        db_file = os.path.split(os.path.realpath(__file__))[0] + "\\ext_tools\\rotor_db\\motors.db"
        db = QSqlDatabase.addDatabase("QSQLITE", "motorDB")
        db.setDatabaseName(db_file)
        db.open()

        model = QSqlTableModel(self.tv_motor_tables,db)
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        return model

    def motor_table_view_init(self,table_view):
        #设置行背景交替色
        table_view.setAlternatingRowColors(True);
        table_view.setStyleSheet("{background-color: rgb(255, 255, 255);" "alternate-background-color: rgb(225, 225, 225);}");
        #隐藏侧边序号
        table_view.verticalHeader().setHidden(True)
        table_view.setModel(self.motor_table_view_model)

        #下面代码让表格100填满窗口
        # table_view.horizontalHeader().setStretchLastSection(True)
        # table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #表头信息显示居左
        # table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

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
        """
        self.motor_dir如果未定义，则使用默认目录：
        ...\LightGCS\ext_tools\rotor_db\
        否则为选定目录
        左侧窗口显示目录中的.csv文件
        右侧窗口显示motors.db库中motorList表内容
        若左侧目录中.csv文件已存在于motorList表中，则只在右侧显示
        """

        # 查询表内容
        """
        params = {"table":tablename, "fields":["ID","name",...], "conditions":xxx}
        """
        params = {"table":"motorList"}
        db_motor_list = table_query(params)
        self.motor_list = set()
        for items in db_motor_list:
            for item in items:
                self.motor_list.add(item)

        if not "motor_dir" in self.__dict__:
            self.motor_dir = os.path.split(os.path.realpath(__file__))[0] + "\\ext_tools\\rotor_db"

        self.csv_files = set()
        files = os.listdir(self.motor_dir)
        for file in files:
            if os.path.isfile(os.path.join(self.motor_dir,file)):
                f = os.path.splitext(file)
                if f[1] == ".csv":
                    self.csv_files.add(f[0])
        self.csv_files_show = self.csv_files - self.motor_list

        self.lw_motor_test_files.clear()
        self.lw_motor_db_files.clear()
        self.lw_motor_test_files.addItems(self.csv_files_show)
        self.lw_motor_db_files.addItems(self.motor_list)
        self.label_motor_db_path.setText(self.motor_dir)

    @pyqtSlot()
    def on_pb_motor_db_file_insert_clicked(self):
        """
        Slot documentation goes here.
        """
        selItems = self.lw_motor_test_files.selectedItems()
        itemSet = set()
        for item in selItems:
            itemSet.add(item.text())

        self.motor_list |= itemSet
        self.csv_files_show = self.csv_files - self.motor_list

        self.lw_motor_test_files.clear()
        self.lw_motor_test_files.addItems(self.csv_files_show)

        self.lw_motor_db_files.clear()
        self.lw_motor_db_files.addItems(self.motor_list)

        def insert_motorItems(itemSet):
            import pandas as pd
            for item in itemSet:
                csv_file = os.path.join(self.motor_dir,"{}.csv".format(item))
                with open(csv_file, 'rb') as f:
                    #lines = csv.reader(f)
                    lines = pd.read_csv(f)
                    # 清除含有NAN的列
                    lines = lines.dropna(axis=1)
                    # 将long转为int
                    columns = list(lines.columns)
                    for column in columns:
                        if lines[column].dtypes == long:
                            lines[column] = lines[column].astype("int")

                    params = {"table":"motorData"}
                    params["fields"] = columns
                    params["values"] = lines.values
                    insert_items(params)

                    params = {}
                    params["fields"] = ["Motor"]
                    params["values"] = [str(item)]

                    params["table"] = "motorList"
                    insert_items(params)

                    params["table"] = "motorInfo"
                    insert_items(params)

            params = {}
            params["fields"] = ["Propeller"]

            params["table"] = "motorData"
            params["values"] = set(table_query(params))

            params["table"] = "propellerInfo"
            insert_items(params)

            self.label_db_dml_status.setText("添加成功！")

        insert_items_thread = threading.Thread(target=insert_motorItems,args=(itemSet,))
        insert_items_thread.setDaemon(True)
        insert_items_thread.start()

    @pyqtSlot()
    def on_pb_motor_db_file_remove_clicked(self):
        """
        Slot documentation goes here.
        """
        selItems = self.lw_motor_db_files.selectedItems()
        itemSet = set()
        for item in selItems:
            itemSet.add(item.text())

        self.motor_list -= itemSet
        self.csv_files_show = self.csv_files - self.motor_list

        self.lw_motor_test_files.clear()
        self.lw_motor_test_files.addItems(self.csv_files_show)

        self.lw_motor_db_files.clear()
        self.lw_motor_db_files.addItems(self.motor_list)

        for item in itemSet:
            params = {}
            params["condition"] = "Motor = '{}'".format(str(item))

            params["table"] = "motorData"
            delete_items(params)

            params["table"] = "motorList"
            delete_items(params)

            params["table"] = "motorInfo"
            delete_items(params)

        self.label_db_dml_status.setText("删除成功！")

    @pyqtSlot()
    def on_pb_csv_template_clicked(self):
        """
        save a motor test file template, csv file
        """
        if not "motor_dir" in self.__dict__:
            self.motor_dir = os.path.split(os.path.realpath(__file__))[0] + "\\ext_tools\\rotor_db"
        file = QFileDialog.getSaveFileName(self, "电机测试数据CSV模板", \
                                                    self.motor_dir,\
                                                    "CSV File (*.csv)")

        if file:
            """
            print file
            (u'E:/DATAANALYSE/PYTHON/PYQT/LightGCS/ext_tools/rotor_db/adfasfs.csv', u'CSV File (*.csv)')
            """
            import csv
            with open(file[0],'wb') as f:
                fileName = os.path.split(file[0])[1]
                fileName = os.path.splitext(fileName)[0]
                fields = ["Motor",\
                          "Voltage",\
                          "Propeller",\
                          "Throttle",\
                          "Amps",\
                          "Watts",\
                          "Thrust",\
                          "RPM",\
                          "Moment",\
                          "Efficiency"]
                writer = csv.DictWriter(f,fieldnames=fields)
                writer.writeheader()
                """
                T-motor lite版电机参数表
                """
                for i in range(40,71,2):
                    writer.writerow({"Motor":fileName,"Voltage":48,"Throttle":"{}%".format(i)})
                writer.writerow({"Motor":fileName,"Voltage":48,"Throttle":"75%"})
                for i in range(80,101,10):
                    writer.writerow({"Motor":fileName,"Voltage":48,"Throttle":"{}%".format(i)})

    @pyqtSlot()
    def on_pb_motor_db_insert_confirm_clicked(self):
        """
        params = {"table":tablename, "fields":["ID","name",...], "values":[[],[],...]}
        """
        drop_table_motorList()
        drop_table_motorData()
        drop_table_motorInfo()
        drop_table_propellerInfo()

        create_table_motorList()
        create_table_motorData()
        create_table_motorInfo()
        create_table_propellerInfo()

        self.label_db_dml_status.setText("清除完成！")

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
        motorInfoCondition = []
        motorDataCondition = []
        for i in range(len(self.motorCbs)):
            if not self.motorCbValues[i]:
                continue
            if i > 2:
                motorDataCondition.append("{}={}".format(self.motorCbKeys[i],self.motorCbValues[i]))
            else:
                motorInfoCondition.append("{}='{}'".format(self.motorCbKeys[i],self.motorCbValues[i]))

        params = {"table":"motorInfo"}
        params["fields"] = ["Motor"]
        params["condition"] = " AND ".join(motorInfoCondition)
        values = table_query(params)

        motors = set([str(item[0]) for item in values if item[0]])
        if len(motors) == 1:
            motorDataCondition.append("Motor = '{}'".format(list(motors)[0]))
        else:
            motorDataCondition.append("Motor IN {}".format(tuple(motors)))

        params = {"table":"motorData"}
        params["condition"] = " AND ".join(motorDataCondition)

        self.motor_table_show(params)

    @pyqtSlot()
    def on_pb_motor_table_show_clicked(self):
        tableName = {"table":self.cb_motor_tables.currentText()}
        self.motor_table_show(tableName)

    def motor_table_show(self,params):
        """
        params = {"table":tableName, "condition":"xxx"}
        """
        tableName = params["table"]
        condition = params.get("condition","")
        self.motor_table_view_model.setTable(tableName)
        self.motor_table_view_model.setFilter(condition)
        self.motor_table_view_model.select()

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

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
