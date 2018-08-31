import os
import time
import compileall

# import py_compile
# py_compile.compile('./NoxConADB.py')

compileall.compile_dir('./', maxlevels=0)

time.sleep(5)

for root, dirs, files in os.walk("./__pycache__", topdown=False):
    for name in files:
        if name.find('NoxConSelenium') != -1 or name.find('compile') != -1:
            os.remove(os.path.join(root, name))
        else:
            os.rename(os.path.join(root, name), os.path.join(root, name).replace('cpython-36.', ''))
