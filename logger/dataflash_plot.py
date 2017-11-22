# -*- coding:utf-8 -*-

from dronekit.mavlink import MAVConnection
from PyQt5.QtWidgets import QFileDialog
from actions import wonf
from pymavlink import DFReader

@wonf
def read_data_flash_file(self):
	opt = QFileDialog.Options()
	# opt |= QFileDialog.DontUseNativeDialog
	fp, _ = QFileDialog.getOpenFileName(self, "选择日志文件", "", "PX4 DataFlash File (*.bin;*.BIN;*.log);;All Files (*)",
	                                    options=opt)
	print fp
	if not fp:
		return

	if fp.endswith('.log'):
		log = DFReader.DFReader_text(fp)
	else:
		log = DFReader.DFReader_binary(fp)
	while True:
		m = log.recv_msg()
		if m is None:
			break
		print(m)

@wonf
def read_data_flash_text(self, file):
	print "Log File..."

@wonf
def read_data_flash_binary(self, file):
	print "Bin File..."









