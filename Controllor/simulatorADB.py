# coding:utf-8
try:
    import sys
    import time, datetime, random
    from pprint import pprint
    from PIL import ImageGrab
    import cv2
    import aircv as ac
    from MyADB import MyADB
except ImportError as e:
    print("[Simulator] ERROR:", e.args[0])
    sys.exit(-1)


class Simulator(object):
    def __init__(self, adb_path, idx):
        self._DEBUG = False
        self._PIC_PATH = {}
        self._img_capture = None
        self._adb = MyADB(adb_binary_path=adb_path)
        self._adb_idx = idx

        self._adb.wait_for_device()
        (err_msg, devices) = self._adb.get_devices()
        print('[Simulator-' + str(self._adb_idx) + '] get_devices:', err_msg)
        pprint(devices)

        if not err_msg:
            self._adb.set_target_device(devices[idx])

    def find_element(self, comment, timeout):
        capture_name = "capture" + str(self._adb_idx) + ".png"

        # self._adb.adb_shell("screencap -p /sdcard/" + capture_name)
        # self._adb.adb_cmd("pull /sdcard/" + capture_name)
        # self._img_capture = ac.imread(capture_name)
        # img_obj = ac.imread(self._PIC_PATH[u"跳过软件升级"])
        # pos = ac.find_template(self._img_capture, img_obj)
        # if pos and pos['confidence'] > 0.9:
        #     print('[Simulator' + str(self._adb_idx) + '] 跳过软件升级.')
        #     x, y = pos['result']
        #     self.click_xy(x, y, timeout=1)

        while (timeout > 0):
            self._adb.adb_shell("screencap -p /sdcard/" + capture_name)
            self._adb.adb_cmd("pull /sdcard/" + capture_name)
            # print "\nOutput:%s" % _adb.get_output()
            self._img_capture = ac.imread(capture_name)
            img_obj = ac.imread(self._PIC_PATH[comment])
            pos = ac.find_template(self._img_capture, img_obj)
            if pos and pos['confidence'] > 0.9:
                print('[Simulator-' + str(self._adb_idx) + '] 匹配到:', comment, str(timeout) + 's')
                x, y = pos['result']
                return True, x, y
            else:
                time.sleep(1)
                timeout = timeout - 1
                print('[Simulator-' + str(self._adb_idx) + '] 未匹配: ', comment, str(timeout) + 's')

        return False, -1, -1

    def _debug(self, pos, timeout):
        if self._DEBUG:
            # cv.Circle(img, center, radius, color, thickness=1, lineType=8, shift=0)
            cv2.circle(img=self._img_capture, center=pos, radius=30, color=(0, 0, 255), thickness=2)
            cv2.startWindowThread()
            cv2.imshow('match', self._img_capture)
            cv2.waitKey(timeout)
            cv2.destroyAllWindows()
            cv2.waitKey(100)

    def click_xy(self, x, y, timeout):
        self._debug(pos=(int(x), int(y)), timeout=2000)
        self._adb.adb_shell('input tap ' + str(int(x)) + ' ' + str(int(y)))
        time.sleep(timeout)
        return True

    def check_upgrade(self, timeout):
        ret, x, y = self.find_element(u"跳过软件升级", timeout)
        if ret:
            print('[Simulator-' + str(self._adb_idx) + '] 提示版本更新.')
            self.click_xy(x, y, 2)

        return ret

    def reboot(self, timeout):
        self._adb.adb_cmd('reboot')
        time.sleep(timeout)

    def app_quit(self, timeout):
        for i in range(4):
            print('[Simulator-' + str(self._adb_idx) + '] app_quit')
            self._adb.adb_shell('input keyevent 4')  # KEYCODE_BACK
            time.sleep(timeout)
        return True

    def unlock(self, timeout):
        self._adb.adb_shell('rm /data/system/*.key')  # rm /data/system/*.key
        time.sleep(timeout)
        return True

    def get_new_phone(self, timeout):
        ret = self._adb.get_new_phone()
        time.sleep(timeout)
        return ret

    def script(self):
        pass

    def run(self):
        ret = self.unlock(timeout=1)
        self.get_new_phone(timeout=1)
        if ret:
            ret = self.app_quit(timeout=1)

        if ret:
            self.script()
