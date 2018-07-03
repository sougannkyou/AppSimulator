import os
import time
import win32con as WCON
import win32api
import win32gui
from PIL import ImageGrab
import cv2
import aircv as ac
import pyautogui
from ControllerGUI.setting import WORK_PATH


class VMSelenium(object):
    def __init__(self, nox_name):
        self._DEBUG = False
        self._UNLOCK_POS = {
            "step1": (133, 496),
            "step2": (132, 705),
            "step3": (343, 707)
        }
        self._PIC_PATH = {}
        self._CLICK_POS = {}
        self._capture_obj = None
        self.hwnd = win32gui.FindWindow(None, nox_name)
        self._work_path = WORK_PATH

    def _log(self, prefix, msg):
        if self._DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
            print('[SeleniumCV]', prefix, msg)

    def set_comment_to_pic(self, value):
        if isinstance(value, dict):
            self._PIC_PATH = value
        else:
            self._log('set_comment_to_pic error:', 'must be set a dictionary')

    def check_upgrade(self, img_capture, comment):
        img_obj = ac.imread(self._PIC_PATH[comment])
        pos = ac.find_template(img_capture, img_obj)
        if pos and pos['confidence'] > 0.9:
            self._log('版本更新提示', self._PIC_PATH[comment])
            self.click("跳过软件升级", 1)
            self.click("分享", 1)

    def click(self, comment, wait_times):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        win32gui.SetForegroundWindow(self.hwnd)
        # print(left, top, right, bottom)
        # print(right - left, bottom - top)
        (x, y) = self._CLICK_POS[comment]
        x = left + x
        y = top + y
        self._debug(x, y, wait_time=2)
        time.sleep(wait_times)
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(WCON.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(WCON.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(wait_times)
        self._log("click", comment)
        return True

    def click_xy(self, x, y, wait_times):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        win32gui.SetForegroundWindow(self.hwnd)
        # print(left, top, right, bottom)
        # print(right - left, bottom - top)
        _x = left + x
        _y = top + y
        self._debug(_x, _y, wait_time=2)
        time.sleep(wait_times)
        win32api.SetCursorPos((_x, _y))
        win32api.mouse_event(WCON.MOUSEEVENTF_LEFTDOWN, _x, _y, 0, 0)
        win32api.mouse_event(WCON.MOUSEEVENTF_LEFTUP, _x, _y, 0, 0)
        time.sleep(wait_times)
        self._log("click_xy", str(_x) + ' ' + str(_y))
        return True

    def _debug(self, x, y, wait_time):
        if not self._DEBUG:
            return

        cv2.circle(img=self._capture_obj, center=(int(x), int(y)), radius=30, color=(0, 0, 255), thickness=1)
        cv2.putText(img=self._capture_obj, text='click', org=(int(x) - 40, int(y) + 10),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=1)
        cv2.startWindowThread()
        cv2.imshow('Debugger', self._capture_obj)
        cv2.waitKey(wait_time * 1000)
        cv2.destroyAllWindows()
        cv2.waitKey(100)

    def get_capture(self, capture_name):
        pic = self._work_path + '\\ControllerCV\\images\\temp\\' + capture_name
        win32gui.SetForegroundWindow(self.hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        app_bg_box = (left, top, right, bottom)
        im = ImageGrab.grab(app_bg_box)
        im.save(pic)
        self._capture_obj = ac.imread(pic)

    def find_element(self, comment, timeout):
        capture_name = 'capture.png'
        img_obj = ac.imread(self._PIC_PATH[comment])
        while timeout > 0:
            self.get_capture(capture_name)
            pos = ac.find_template(self._capture_obj, img_obj)
            if pos and pos['confidence'] > 0.9:
                self._log('<<info>> 匹配到：', comment + ' ' + str(timeout) + 's')
                x, y = pos['result']
                return True, int(x), int(y)
            else:
                self._log('<<info>> 未匹配：', comment + ' ' + str(timeout) + 's')
                time.sleep(1)
                timeout -= 1
                # self.check_upgrade(img_capture, comment=u"跳过软件升级")

        return False, -1, -1

    def send_key(self, key_value, wait_times):
        win32gui.SetForegroundWindow(self.hwnd)
        # win32api.SetCursorPos([left + 10, top + 10])
        # win32api.mouse_event(WCON.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        # self._sleep(0.3)
        # win32api.mouse_event(WCON.MOUSEEVENTF_LEFTUP,0,0,0,0)
        # win32api.SendMessage(hwnd,WCON.WM_SETTEXT,None,'A')

        # 向窗口发送Enter键
        time.sleep(wait_times)
        win32api.keybd_event(key_value, 0, 0, 0)
        # self._sleep(0.5)
        win32api.keybd_event(key_value, 0, WCON.KEYEVENTF_KEYUP, 0)
        self._log('<<info>> 发送：', key_value + ' 键')
        time.sleep(wait_times)
        return True

    def quit_app(self, wait_times):
        time.sleep(wait_times)
        self.send_key(WCON.VK_ESCAPE, 1)
        self.send_key(WCON.VK_ESCAPE, 1)
        self.send_key(WCON.VK_ESCAPE, 1)
        self.send_key(WCON.VK_ESCAPE, 1)
        time.sleep(wait_times)
        return True

    def unlock(self, wait_times):
        ret, x, y = self.find_element(comment='锁屏', timeout=10)
        if not ret:
            return False
        else:
            win32gui.SetForegroundWindow(self.hwnd)
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            top += 20
            time.sleep(wait_times)

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
            time.sleep(wait_times)
            return True

    def _check_screen_lock(self, timeout):
        win32gui.SetForegroundWindow(self.hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        time.sleep(timeout)

        ret, x, y = self.find_element(comment='锁屏', timeout=10)
        if not ret:
            return False
        else:
            # _x = left + x
            # _y = top + y
            # pyautogui.moveTo(_x, _y)
            # pyautogui.dragTo(_x, _y - 400, 0.5, button='left')
            # self._sleep(timeout)

            ret, x, y = self.find_element(comment='锁屏图案', timeout=10)
            if not ret:
                return False
            else:
                screen_lock = ac.imread('images_yeshen/screen_lock.png')
                h = screen_lock.shape[0]
                d = screen_lock.shape[1]
                print(left, top, right, bottom, x, y, d, h)
                _x = left + x - d / 2
                _y = top + y - h / 2
                pyautogui.moveTo(_x, _y)
                pyautogui.mouseDown()

                _x = left + x - d
                _y = top + y + h
                pyautogui.moveTo(_x, _y, 1, pyautogui.easeInQuad)

                _x = left + x + d
                _y = top + y + h
                # pyautogui.dragTo(x, y, 0.5, button='left')
                pyautogui.moveTo(_x, _y, 1, pyautogui.easeInBounce)
                pyautogui.mouseUp()
                time.sleep(timeout)
                return True

    def run(self):
        if self.hwnd:
            ret = True
            # ret = self.unlock(wait_times=1)
            # if ret:
            #     ret = self.quit_app(wait_times=1)

            if ret:
                self.script()

    def script(self):
        pass  # overwrite


if __name__ == "__main__":
    pass
