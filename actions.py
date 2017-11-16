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

from PyQt5.QtSql import QSqlTableModel,QSqlDatabase
from Ui_MainWindow import Ui_MainWindow
from pymavlink import mavutil
from dronekit import connect
# from tools.sql_tool import *
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

    @pyqtSlot()
    def on_pb_read_log_clicked(self):
        self.read_data_flash_log()

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

    # def table_view_init(self):
    #
    #     #设置行背景交替色
    #     self.tv_params.setAlternatingRowColors(True);
    #     self.tv_params.setStyleSheet("background-color: rgb(225, 225, 225);\nalternate-background-color: rgb(255, 255, 255);\ncolor: rgb(0,0,0);");
    #
    #     self.table_view_model = QStandardItemModel(self.tv_params)
    #
    #     #设置表格属性：
    #     self.params_length = len(self.vehicle.parameters)
    #     self.table_view_model.setRowCount(self.params_length)
    #     self.table_view_model.setColumnCount(5)
    #
    #     #设置表头
    #     self.table_view_model.setHeaderData(0,Qt.Horizontal,"Name")
    #     self.table_view_model.setHeaderData(1,Qt.Horizontal,"Value")
    #     self.table_view_model.setHeaderData(2,Qt.Horizontal,"Unit")
    #     self.table_view_model.setHeaderData(3,Qt.Horizontal,"Limit")
    #     self.table_view_model.setHeaderData(4,Qt.Horizontal,"Description")
    #     #设置表头背景色
    #     self.tv_params.horizontalHeader().setStyleSheet("QHeaderView.section{background-color:red}");
    #
    #     #隐藏侧边序号
    #     self.tv_params.verticalHeader().setHidden(True)
    #
    #     self.tv_params.setModel(self.table_view_model)
    #
    #     #设置列宽
    #     # self.tv_params.setColumnWidth(0,200)
    #     # self.tv_params.setColumnWidth(1,100)
    #     # self.tv_params.setColumnWidth(2,100)
    #     # self.tv_params.setColumnWidth(3,150)
    #     # self.tv_params.setColumnWidth(4,360)
    #
    #     #下面代码让表格100填满窗口
    #     self.tv_params.horizontalHeader().setStretchLastSection(True)
    #     self.tv_params.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    #
    #     #表头信息显示居左
    #     self.tv_params.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
    #
    #     self.params_table_view_update()
    #
    #     #按参数字母排序
    #     self.tv_params.sortByColumn(0, Qt.AscendingOrder)
    #
    #     self.tv_params.resizeColumnToContents(0)
    #     self.tv_params.resizeColumnToContents(1)
    #
    # def params_table_view_update(self):
    #
    #     idx = 0
    #     EDITABLE_FLAG = Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled
    #     NOTEDITABLE_FLAG = Qt.ItemIsSelectable | Qt.ItemIsEnabled
    #     for key, value in self.vehicle.parameters.iteritems():
    #         #填充内容
    #         self.table_view_model.setItem(idx,0,QStandardItem(key))
    #         self.table_view_model.setItem(idx,1,QStandardItem(str(value)))
    #         self.table_view_model.setItem(idx,2,QStandardItem(""))
    #         self.table_view_model.setItem(idx,3,QStandardItem(""))
    #         self.table_view_model.setItem(idx,4,QStandardItem(""))
    #
    #         #设置第二列数据可编辑
    #         self.table_view_model.item(idx,0).setFlags(NOTEDITABLE_FLAG)
    #         self.table_view_model.item(idx,1).setFlags(EDITABLE_FLAG)
    #         self.table_view_model.item(idx,2).setFlags(NOTEDITABLE_FLAG)
    #         self.table_view_model.item(idx,3).setFlags(NOTEDITABLE_FLAG)
    #         self.table_view_model.item(idx,4).setFlags(NOTEDITABLE_FLAG)
    #
    #         idx += 1

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
        self.pb_connection.setText("未连接")
        self.pb_connection.setStyleSheet("background-color: rgb(204, 204, 102);\ncolor: rgb(0,0,0)")

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
            try:
                self.vehicle = connect(port,  wait_ready=True, status_printer = self.tb_console.append, baud=int(self.cb_comm_rate.currentText()))
            except Exception as e:
                self.vehicle = None
                print str(e)

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
        Slot documentation goes here.
        """
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
        enter accelebrator calibrating window
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
        db_file = os.path.split(os.path.realpath(__file__))[0] + "\\tools\\rotor_db\\motors.db"
        db = QSqlDatabase.addDatabase("QSQLITE", "motorDB")
        db.setDatabaseName(db_file)
        db.open()

        model = QSqlTableModel(self.tv_motor_tables,db)
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        return model

    def motor_table_view_init(self,table_view):
        #设置行背景交替色
        table_view.setAlternatingRowColors(True);
        table_view.setStyleSheet("background-color: rgb(255, 255, 255);\nalternate-background-color: rgb(225, 225, 225);");
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
        ...\LightGCS\tools\rotor_db\
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
            self.motor_dir = os.path.split(os.path.realpath(__file__))[0] + "\\tools\\rotor_db"

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
            self.motor_dir = os.path.split(os.path.realpath(__file__))[0] + "\\tools\\rotor_db"
        file = QFileDialog.getSaveFileName(self, "电机测试数据CSV模板", \
                                                    self.motor_dir,\
                                                    "CSV File (*.csv)")

        if file:
            """
            print file
            (u'E:/DATAANALYSE/PYTHON/PYQT/LightGCS/tools/rotor_db/adfasfs.csv', u'CSV File (*.csv)')
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
        # drop_table_motorInfo()
        # drop_table_propellerInfo()

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


