# coding:utf-8
try:
    import sys
    import time, datetime
    from PIL import ImageGrab
    import cv2
    import aircv as ac
    from MyADB3 import ADB
except ImportError as e:
    print("[error] Required module missing.", e.args[0])
    sys.exit(-1)


class Simulator(object):
    def __init__(self, adb_path):
        self._DEBUG = True
        self._PIC_PATH = {}
        self._adb = ADB(adb_path=adb_path)

        print("Waiting for device...")
        self._adb.wait_for_device()
        err, dev = self._adb.get_devices()
        if not dev:
            print("Unexpected error")

        for d in dev:
            print("[script] found device: ", d)

        self._adb.set_target_device(dev[0])

    def find_element(self, comment, timeout):
        while (timeout > 0):
            self._adb.adb_shell("screencap -p /sdcard/capture.png")
            self._adb.adb_cmd("pull /sdcard/capture.png")
            # print "\nOutput:%s" % _adb.get_output()

            img_capture = ac.imread('capture.png')
            img_obj = ac.imread(self._PIC_PATH[comment])
            pos = ac.find_template(img_capture, img_obj)
            if pos and pos['confidence'] > 0.9:
                print('found:%s %d', comment, timeout)
                x, y = pos['result']
                self._debug(img=img_capture, pos=(int(x), int(y)), timeout=2000)
                return True, x, y
            else:
                time.sleep(1)
                timeout -= 1
                print('not found: ', comment, timeout)
                self.check_upgrade()

    def _debug(self, img, pos, timeout):
        if self._DEBUG:
            # cv.Circle(img, center, radius, color, thickness=1, lineType=8, shift=0)
            cv2.circle(img=img, center=pos, radius=30, color=(0, 0, 255), thickness=2)
            cv2.startWindowThread()
            cv2.imshow('match', img)
            cv2.waitKey(timeout)
            cv2.destroyAllWindows()
            cv2.waitKey(100)

    def click_xy(self, x, y, timeout):
        time.sleep(timeout)
        self._adb.shell_command('input tap ' + str(x) + ' ' + str(y))
        time.sleep(timeout)
        return True

    def check_upgrade(self):
        ret, x, y = self.find_element(u"跳过软件升级", 10)
        if ret:
            print('提示版本更新.')
            self.click_xy(x, y, 2)
            # ret, x, y = self.find_element(u"分享", 10)
            # if ret:
            #     self.click_xy(x, y, 1)

    def reboot(self, timeout):
        self._adb.run_cmd('reboot')
        time.sleep(timeout)

    def app_quit(self, timeout):
        self._adb.shell_command('input keyevent 4')  # KEYCODE_BACK
        time.sleep(timeout)

    def unlock(self, timeout):
        self._adb.shell_command('rm /data/system/*.key')  # rm /data/system/*.key
        time.sleep(timeout)
        return True

    def script(self):
        pass

    def run(self):
        ret = self.unlock(timeout=1)
        if not ret:
            ret = self.app_quit(timeout=1)

        if ret: self.script()


def run():
    print("[script] start ...")
    start = datetime.datetime.now()
    try:
        class MySimulator(Simulator):
            def script(self):
                ret, x, y = self.find_element(comment=u'APP图标', timeout=10)  # unlock ok
                if ret: ret = self.click_xy(x, y, timeout=2)
                while (ret):
                    if ret: ret, x, y = self.find_element(comment=u'更新', timeout=10)
                    if ret: ret = self.click_xy(x, y, timeout=1)

                    if ret: ret, x, y = self.find_element(comment=u'分享', timeout=10)
                    if ret: ret = self.click_xy(x, y, timeout=1)

                    if ret:
                        ret, x, y = self.find_element(comment=u'复制链接', timeout=10)
                        if ret:
                            ret = self.click_xy(x, y, timeout=1)
                        else:
                            print(u"重试 click 分享 按钮 ...")
                            ret, x, y = self.find_element(comment=u'分享', timeout=10)
                            if ret: ret = self.click_xy(x, y, timeout=1)

                    # if not ret: self.send2web('images/offline.jpeg')

        mySimulator = MySimulator(adb_path='C:\\Nox\\bin\\adb.exe')
        # mySimulator = MySimulator(adb_path='C:\\adb\\adb.exe')
        mySimulator._PIC_PATH = {
            u"APP图标": 'images/app_ready.png',
            u"更新": 'images/update.png',
            u"分享": 'images/share.png',
            u"复制链接": 'images/copylink.png',
            # u"跳过软件升级": 'images/is_upgrade.png',
            u"跳过软件升级": 'images/ignore_upgrade.png',
            u"锁屏": 'images/screen_lock.png',
            u"锁屏图案": 'images/screen_lock_9point.png'
        }

        mySimulator.run()
        end = datetime.datetime.now()
        # print "[script] success. %d" % (end - start).seconds
        return True
    except Exception as e:
        end = datetime.datetime.now()
        print("[script] error:", e)
        return False


if __name__ == "__main__":
    run()
