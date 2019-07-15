from inspect import getsourcefile
import os.path as path
import sys


current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
parent_path = current_dir[:current_dir.rfind(path.sep)]
sys.path.insert(0, parent_path)

