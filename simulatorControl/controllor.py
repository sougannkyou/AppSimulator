# coding=utf8
import os, time
import time
import win32con as WCON
import win32api
import win32gui
from PIL import ImageGrab
import cv2
import aircv as ac
import shutil
import pyautogui
from xmlrpc.server import SimpleXMLRPCServer

DEBUG_ENV = False


class Simulator:
    def __init__(self, app_name):
        self._UNLOCK_POS = {
            "step1": (133, 496),
            "step2": (132, 705),
            "step3": (343, 707)
        }
        self._PIC_PATH = {}
        self._CLICK_POS = {}
        self.is_proxy_active = True
        self.hwnd = win32gui.FindWindow(None, app_name)

    def is_upgrade(self, img_capture, comment):
        img_obj = ac.imread(self._PIC_PATH[comment])
        pos = ac.find_template(img_capture, img_obj)
        if pos and pos['confidence'] > 0.9:
            print('版本更新提示', self._PIC_PATH[comment])
            self.click(u"跳过软件升级", 1)
            self.click(u"分享", 1)

    def click(self, comment, timeout):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        win32gui.SetForegroundWindow(self.hwnd)
        # print(left, top, right, bottom)
        # print(right - left, bottom - top)
        (x, y) = self._CLICK_POS[comment]
        x = left + x
        y = top + y
        self._sleep(timeout)
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(WCON.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(WCON.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        self._sleep(timeout)
        print("click", comment)
        return True

    def set_proxy(self):
        self.is_proxy_active = False

    def proxy_change_status_stop(self):
        self.is_proxy_active = False

    def proxy_change_status_run(self):
        self.is_proxy_active = True

    def _sleep(self, times):
        while (not self.is_proxy_active):
            print("wait for proxy server active ...")
            time.sleep(1)
        else:
            time.sleep(times)

    def _detect_obj(self, img, circle_center_pos, circle_radius, color, line_width):
        if DEBUG_ENV:
            cv2.circle(img, circle_center_pos, circle_radius, color, line_width)
            cv2.imshow('detect_obj', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def send2web(self, pic_path):
        shutil.copyfile('../static/AppSimulator/images/capture.png',
                        '../static/AppSimulator/images/capture_before.png')
        shutil.copyfile(pic_path, '../static/AppSimulator/images/capture.png')
        return True

    def find_element(self, comment, timeout):
        # 匹配element图像
        # pprint(pos)
        obj_pic_path = self._PIC_PATH[comment]
        while (timeout > 0):
            win32gui.SetForegroundWindow(self.hwnd)
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            app_bg_box = (left, top, right, bottom)
            im = ImageGrab.grab(app_bg_box)
            im.save('images/capture.png')
            self.send2web('images/capture.png')

            img_capture = ac.imread('images/capture.png')
            img_obj = ac.imread(obj_pic_path)
            pos = ac.find_template(img_capture, img_obj)
            if pos and pos['confidence'] > 0.9:
                print('匹配到', comment, timeout)
                x, y = pos['result']
                self._detect_obj(img=img_capture, circle_center_pos=(int(x), int(y)), circle_radius=40,
                                 color=(0, 255, 0),
                                 line_width=2)
                return True
            else:
                print('未匹配到', comment, timeout)
                self._sleep(1)
                timeout -= 1
                self.is_upgrade(img_capture, comment=u"跳过软件升级")

        return False

    def send_key(self, key_value, timeout):
        win32gui.SetForegroundWindow(self.hwnd)
        # win32api.SetCursorPos([left + 10, top + 10])
        # win32api.mouse_event(WCON.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        # self._sleep(0.3)
        # win32api.mouse_event(WCON.MOUSEEVENTF_LEFTUP,0,0,0,0)
        # win32api.SendMessage(hwnd,WCON.WM_SETTEXT,None,'A')

        # 向窗口发送Enter键
        self._sleep(timeout)
        win32api.keybd_event(key_value, 0, 0, 0)
        # self._sleep(0.5)
        win32api.keybd_event(key_value, 0, WCON.KEYEVENTF_KEYUP, 0)
        print('发送', key_value, '键')
        self._sleep(timeout)
        return True

    def app_quit(self):
        self.send_key(WCON.VK_ESCAPE, 1)
        self.send_key(WCON.VK_ESCAPE, 1)
        self.send_key(WCON.VK_ESCAPE, 1)
        self.send_key(WCON.VK_ESCAPE, 1)
        return True

    def unlock(self, timeout):
        win32gui.SetForegroundWindow(self.hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        top += 20
        self._sleep(timeout)

        (x, y) = self._UNLOCK_POS['step1']
        x = left + x
        y = top + y
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()

        (x, y) = self._UNLOCK_POS['step2']
        x = left + x
        y = top + y
        # pyautogui.dragTo(x, y, 0.5, button='left')
        pyautogui.moveTo(x, y, 1, pyautogui.easeInQuad)

        (x, y) = self._UNLOCK_POS['step3']
        x = left + x
        y = top + y
        # pyautogui.dragTo(x, y, 0.5, button='left')
        pyautogui.moveTo(x, y, 1, pyautogui.easeInBounce)
        pyautogui.mouseUp()
        self._sleep(timeout)
        return True

    def run(self):
        ret = None
        # hwnd = win32gui.FindWindow("Qt5QWindowIcon", None)
        if self.hwnd: ret = self.find_element(comment='锁屏', timeout=5)
        if ret: ret = self.unlock(1)
        if ret: ret = self.app_quit()
        if ret: self.script()

    def script(self):
        pass


class MySimulator(Simulator):
    def script(self):
        ret = None
        if self.hwnd: ret = self.find_element(comment='APP图标', timeout=10)  # unlock ok
        if ret: ret = self.click(u"APP图标", timeout=2)
        while (ret):
            if ret: ret = self.find_element(comment='更新', timeout=10)
            if ret: ret = self.click(u"更新", timeout=1)

            if ret: ret = self.find_element(comment='分享', timeout=10)
            if ret: ret = self.click(u"分享", timeout=1)

            if ret: ret = self.find_element(comment='复制链接', timeout=10)
            if ret: ret = self.click(u"复制链接", timeout=1)
            if not ret: self.send2web('images/offline.png')


me = None


def run():
    me = MySimulator("douyin0")
    me._PIC_PATH = {
        u"APP图标": 'images/app_ready.png',
        u"更新": 'images/update.png',
        u"分享": 'images/share.png',
        u"复制链接": 'images/copylink.png',
        u"跳过软件升级": 'images/is_upgrade.png',
        u"锁屏": 'images/screen_lock.png'
    }

    me._CLICK_POS = {
        u"APP图标": (38, 793),
        u"更新": (38, 793),
        u"分享": (451, 628),
        u"复制链接": (47, 720),
        u"跳过软件升级": (231, 590)  # 以后再说
    }
    me.run()
    return me


def proxy_change_status_stop():
    me.is_proxy_active = False


def proxy_change_status_run():
    me.is_proxy_active = True


def resetDevice(deviceId):
    print("resetDeviceAPI start.", deviceId)
    p = os.popen("D:\\Nox\\bin\\Nox.exe -quit")
    print("Nox.exe -quit :", p.read())

    p = os.popen("tasklist | findstr 'Nox'")
    print("tasklist | findstr 'Nox' :", p.read())

    time.sleep(10)
    p = os.popen("D:\\Nox\\bin\\Nox.exe")
    print("Nox.exe :", p.read())
    return True


def setDeviceGPS(deviceId, latitude, longitude):
    print(deviceId, latitude, longitude)  # 39.6099202570, 118.1799316404
    p = os.popen("adb shell setprop persist.nox.gps.latitude " + latitude)
    print(p.read())

    p = os.popen("adb shell setprop persist.nox.gps.longitude " + longitude)
    print(p.read())
    return True


######################################################################
server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(run, "run")
server.register_function(run, "run")
server.register_function(run, "run")
server.register_function(resetDevice, "resetDevice")
server.register_function(setDeviceGPS, 'setDeviceGPS')
server.serve_forever()
