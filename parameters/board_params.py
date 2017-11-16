# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from actions import wonf

@wonf
def table_view_init(self):
	# 设置行背景交替色
	self.tv_params.setAlternatingRowColors(True);
	self.tv_params.setStyleSheet(
		"background-color: rgb(225, 225, 225);\nalternate-background-color: rgb(255, 255, 255);\ncolor: rgb(0,0,0);");

	self.table_view_model = QStandardItemModel(self.tv_params)

	# 设置表格属性：
	self.params_length = len(self.vehicle.parameters)
	self.table_view_model.setRowCount(self.params_length)
	self.table_view_model.setColumnCount(5)

	# 设置表头
	self.table_view_model.setHeaderData(0, Qt.Horizontal, "Name")
	self.table_view_model.setHeaderData(1, Qt.Horizontal, "Value")
	self.table_view_model.setHeaderData(2, Qt.Horizontal, "Unit")
	self.table_view_model.setHeaderData(3, Qt.Horizontal, "Limit")
	self.table_view_model.setHeaderData(4, Qt.Horizontal, "Description")
	# 设置表头背景色
	self.tv_params.horizontalHeader().setStyleSheet("QHeaderView.section{background-color:red}");

	# 隐藏侧边序号
	self.tv_params.verticalHeader().setHidden(True)

	self.tv_params.setModel(self.table_view_model)

	# 设置列宽
	# self.tv_params.setColumnWidth(0,200)
	# self.tv_params.setColumnWidth(1,100)
	# self.tv_params.setColumnWidth(2,100)
	# self.tv_params.setColumnWidth(3,150)
	# self.tv_params.setColumnWidth(4,360)

	# 下面代码让表格100填满窗口
	self.tv_params.horizontalHeader().setStretchLastSection(True)
	self.tv_params.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

	# 表头信息显示居左
	self.tv_params.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

	self.params_table_view_update()

	# 按参数字母排序
	self.tv_params.sortByColumn(0, Qt.AscendingOrder)

	self.tv_params.resizeColumnToContents(0)
	self.tv_params.resizeColumnToContents(1)

@wonf
def params_table_view_update(self):
	idx = 0
	EDITABLE_FLAG = Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled
	NOTEDITABLE_FLAG = Qt.ItemIsSelectable | Qt.ItemIsEnabled
	for key, value in self.vehicle.parameters.iteritems():
		# 填充内容
		self.table_view_model.setItem(idx, 0, QStandardItem(key))
		self.table_view_model.setItem(idx, 1, QStandardItem(str(value)))
		self.table_view_model.setItem(idx, 2, QStandardItem(""))
		self.table_view_model.setItem(idx, 3, QStandardItem(""))
		self.table_view_model.setItem(idx, 4, QStandardItem(""))

		# 设置第二列数据可编辑
		self.table_view_model.item(idx, 0).setFlags(NOTEDITABLE_FLAG)
		self.table_view_model.item(idx, 1).setFlags(EDITABLE_FLAG)
		self.table_view_model.item(idx, 2).setFlags(NOTEDITABLE_FLAG)
		self.table_view_model.item(idx, 3).setFlags(NOTEDITABLE_FLAG)
		self.table_view_model.item(idx, 4).setFlags(NOTEDITABLE_FLAG)

		idx += 1