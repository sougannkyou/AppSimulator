import aircv as ac
import cv2
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
pos_list = ac.find_all_template(mySimulator._img_capture, img_obj)
pprint(pos_list)

img = None
for pos in pos_list:
    if pos['confidence'] > 0.9:
        (x, y) = pos['result']
        img = cv2.circle(img=mySimulator._img_capture, center=(int(x), int(y)), radius=10, color=(0, 0, 0), thickness=10)
        cv2.startWindowThread()
        cv2.imshow('Debugger', img)
        cv2.waitKey(5000)

# cv2.destroyAllWindows()
# cv2.waitKey(5000)
