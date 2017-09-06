# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot, Qt, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog,QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from Ui_MainWindow import Ui_MainWindow
from pymavlink import mavutil
from dronekit import connect
from setting import px4_uploader
import time
import threading

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
        if self.serial_list:
            self.current_port = p0

    @pyqtSlot(QString)
    def on_cb_comm_rate_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.

        @param p0 DESCRIPTION
        @type QString
        """
        # TODO: not implemented yet
        if self.serial_list:
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
            return
        self.print_info(fp)
        fw_thread = threading.Thread(target=self.firmware_uploader,args=(fp,))
        fw_thread.setDaemon(True)
        fw_thread.start()

    def firmware_uploader(self, fp):
        if self.connection:
            self.print_info("Please unconnect apm!")
            return

        if not self.serial_list:
            count = 0
            while count < 30 and not self.serial_list:
                time.sleep(1)
                count += 1
                info = "Plugin flight controller board, remaining: %s s"%(30 - count)
                self.fw_upload_state.setText(info)
                self.combobox_port_update()
            if count >= 30:
                self.fw_upload_state.setText("Time Out!")
                fw_thread.join()
                return

        px4_uploader.px4_uploader(self,fp,self.current_port,self.current_baud)
        fw_thread.join()
        
    def print_info(self,str):
        self.tb_console.append(str)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
