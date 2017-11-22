# -*- coding: utf-8 -*-

from actions import wonf
from sql_tool import *
from PyQt5.QtSql import QSqlTableModel,QSqlDatabase
from PyQt5.QtWidgets import QFileDialog
import threading
"""
 电机数据库部分
 """

@wonf
def motor_db_combobox_init(self):
	self.motorCbs = (self.cb_motor_db_productor, \
	                 self.cb_motor_db_type, \
	                 self.cb_motor_db_kv, \
	                 self.cb_motor_db_propeller, \
	                 self.cb_motor_db_volt)

	for item in self.motorCbs:
		item.installEventFilter(self)

	self.motorCbKeys = ("Producer", "Type", "KV", "Propeller", "Voltage")

	self.motorCbValues = [str(cb.currentText()) for cb in self.motorCbs]

@wonf
def motor_db_file_read_event(self):
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
	params = {"table": "motorList"}
	db_motor_list = table_query(params)
	self.motor_list = set()
	for items in db_motor_list:
		for item in items:
			self.motor_list.add(item)

	if not "motor_dir" in self.__dict__:
		self.motor_dir = os.path.split(os.path.realpath(__file__))[0] + "\\rotor_db"

	self.csv_files = set()
	files = os.listdir(self.motor_dir)
	for file in files:
		if os.path.isfile(os.path.join(self.motor_dir, file)):
			f = os.path.splitext(file)
			if f[1] == ".csv":
				self.csv_files.add(f[0])
	self.csv_files_show = self.csv_files - self.motor_list

	self.lw_motor_test_files.clear()
	self.lw_motor_db_files.clear()
	self.lw_motor_test_files.addItems(self.csv_files_show)
	self.lw_motor_db_files.addItems(self.motor_list)
	self.label_motor_db_path.setText(self.motor_dir)

@wonf
def motor_db_file_insert_event(self):
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
			csv_file = os.path.join(self.motor_dir, "{}.csv".format(item))
			with open(csv_file, 'rb') as f:
				# lines = csv.reader(f)
				lines = pd.read_csv(f)
				# 清除含有NAN的列
				lines = lines.dropna(axis=1)
				# 将long转为int
				columns = list(lines.columns)
				for column in columns:
					if lines[column].dtypes == long:
						lines[column] = lines[column].astype("int")

				params = {"table": "motorData"}
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

	insert_items_thread = threading.Thread(target=insert_motorItems, args=(itemSet,))
	insert_items_thread.setDaemon(True)
	insert_items_thread.start()

@wonf
def motor_db_file_remove_event(self):
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

@wonf
def motor_db_init(self):
	tables = [item for items in show_tables() for item in items]
	self.cb_motor_tables.clear()
	self.cb_motor_tables.addItems(tables)
	self.cb_motor_tables.setCurrentIndex(0)

	self.motor_table_view_model = self.create_sql_table_model()
	self.motor_table_view_init(self.tv_motor_tables)
	self.motor_table_view_init(self.tv_motor_data)
	self.motor_db_initialised = True

@wonf
def motor_table_show(self, params):
	"""
	params = {"table":tableName, "condition":"xxx"}
	"""
	tableName = params["table"]
	condition = params.get("condition", "")
	self.motor_table_view_model.setTable(tableName)
	self.motor_table_view_model.setFilter(condition)
	self.motor_table_view_model.select()

@wonf
def motor_table_show_event(self):
	tableName = {"table": self.cb_motor_tables.currentText()}
	self.motor_table_show(tableName)

@wonf
def csv_template_event(self):
	"""
	        save a motor test file template, csv file
	        """
	if not "motor_dir" in self.__dict__:
		self.motor_dir = os.path.split(os.path.realpath(__file__))[0] + "\\rotor_db"
	file = QFileDialog.getSaveFileName(self, "电机测试数据CSV模板", \
	                                   self.motor_dir, \
	                                   "CSV File (*.csv)")

	if file:
		"""
		print file
		(u'E:/DATAANALYSE/PYTHON/PYQT/LightGCS/tools/rotor_db/adfasfs.csv', u'CSV File (*.csv)')
		"""
		import csv
		with open(file[0], 'wb') as f:
			fileName = os.path.split(file[0])[1]
			fileName = os.path.splitext(fileName)[0]
			fields = ["Motor", \
			          "Voltage", \
			          "Propeller", \
			          "Throttle", \
			          "Amps", \
			          "Watts", \
			          "Thrust", \
			          "RPM", \
			          "Moment", \
			          "Efficiency"]
			writer = csv.DictWriter(f, fieldnames=fields)
			writer.writeheader()
			"""
			T-motor lite版电机参数表
			"""
			for i in range(40, 71, 2):
				writer.writerow({"Motor": fileName, "Voltage": 48, "Throttle": "{}%".format(i)})
			writer.writerow({"Motor": fileName, "Voltage": 48, "Throttle": "75%"})
			for i in range(80, 101, 10):
				writer.writerow({"Motor": fileName, "Voltage": 48, "Throttle": "{}%".format(i)})

@wonf
def motor_db_insert_confirm_event(self):
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

@wonf
def motor_data_sql_event(self):
	motorInfoCondition = []
	motorDataCondition = []
	for i in range(len(self.motorCbs)):
		if not self.motorCbValues[i]:
			continue
		if i > 2:
			motorDataCondition.append("{}={}".format(self.motorCbKeys[i], self.motorCbValues[i]))
		else:
			motorInfoCondition.append("{}='{}'".format(self.motorCbKeys[i], self.motorCbValues[i]))

	params = {"table": "motorInfo"}
	params["fields"] = ["Motor"]
	params["condition"] = " AND ".join(motorInfoCondition)
	values = table_query(params)

	motors = set([str(item[0]) for item in values if item[0]])
	if len(motors) == 1:
		motorDataCondition.append("Motor = '{}'".format(list(motors)[0]))
	else:
		motorDataCondition.append("Motor IN {}".format(tuple(motors)))

	params = {"table": "motorData"}
	params["condition"] = " AND ".join(motorDataCondition)

	self.motor_table_show(params)

@wonf
def motor_data_combobox_update(self, obj):
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
			motorDataCondition.append("{}={}".format(self.motorCbKeys[i], self.motorCbValues[i]))
		else:
			motorInfoCondition.append("{}='{}'".format(self.motorCbKeys[i], self.motorCbValues[i]))

	params = {"table": "motorInfo"}
	params["fields"] = ["Motor", "Producer", "Type", "KV"]
	params["condition"] = " AND ".join(motorInfoCondition)
	values = table_query(params)
	motors = set([str(item[0]) for item in values if item[0]])

	if idx >= 3:  # Propeller ---> motorData
		params = {"table": "motorData"}
		params["fields"] = ["Motor", "Propeller", "Voltage"]
		if len(motors) == 1:
			motorDataCondition.append("Motor = '{}'".format(list(motors)[0]))
		else:
			motorDataCondition.append("Motor IN {}".format(tuple(motors)))
		params["condition"] = " AND ".join(motorDataCondition)

		values = table_query(params)
		items = set([str(item[idx - 2]) for item in values if item[idx - 2]])
	else:
		items = set([str(item[idx + 1]) for item in values if item[idx + 1]])

	obj.clear()
	obj.addItem("")
	obj.addItems(items)

@wonf
def create_sql_table_model(self):
	db_file = os.path.split(os.path.realpath(__file__))[0] + "\\rotor_db\\motors.db"
	db = QSqlDatabase.addDatabase("QSQLITE", "motorDB")
	db.setDatabaseName(db_file)
	db.open()

	model = QSqlTableModel(self.tv_motor_tables, db)
	model.setEditStrategy(QSqlTableModel.OnManualSubmit)
	return model

@wonf
def motor_table_view_init(self, table_view):
	# 设置行背景交替色
	table_view.setAlternatingRowColors(True);
	table_view.setStyleSheet("background-color: rgb(255, 255, 255);\nalternate-background-color: rgb(225, 225, 225);");
	# 隐藏侧边序号
	table_view.verticalHeader().setHidden(True)
	table_view.setModel(self.motor_table_view_model)

	# 下面代码让表格100填满窗口
	# table_view.horizontalHeader().setStretchLastSection(True)
	# table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

	# 表头信息显示居左
	# table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)