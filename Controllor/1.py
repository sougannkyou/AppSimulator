import aircv as ac
import ftplib
from MyADB import MyADB
from pprint import pprint
from simulatorADB import Simulator

ADB_BINARY_PATH = 'C:\\Nox\\bin\\adb.exe'

class MySimulator(Simulator):
    def script(self):
        pass

mySimulator = MySimulator(adb_path=ADB_BINARY_PATH, idx=0)
mySimulator._PIC_PATH = {
    "打分": 'images/dianping/dafen.png',
}
mySimulator._DEBUG = True
# if not ret: self.send2web('images/offline.jpeg')
# mySimulator.run(is_app_restart=False)

img_obj = ac.imread(mySimulator._PIC_PATH["打分"])
capture_name = "capture99.png"
mySimulator.get_capture(capture_name)
pos = ac.find_all_template(mySimulator._img_capture, img_obj)
pprint(pos)
