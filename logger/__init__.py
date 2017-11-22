# -*- coding:utf-8 -*-

import dataflash_plot


# exclude_exts = [".bin", ".pyc", ".txt", ".BIN", ".params"]
# try:
# 	import os
# 	import sys
# 	path = os.path.dirname(os.path.abspath(__file__))
# 	files = os.listdir(path)
# 	for item in files:
# 		name,ext = os.path.splitext(item)
# 		if ext in exclude_exts:
# 			continue
# 		if "__init__" == name:
# 			continue
# 		print name,item,type(item)
# 		__import__(name, globals(), locals(), [], -1)
# 		print sys.modules[name]
# except Exception:
# 	pass