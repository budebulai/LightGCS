# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from actions import MainWindow

if __name__ == "__main__":
	import sys

	app = QApplication(sys.argv)
	ui = MainWindow()
	ui.show()
	sys.exit(app.exec_())