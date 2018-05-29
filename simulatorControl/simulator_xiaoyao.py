import os, time
import win32con as WCON
import win32api
import win32gui
from PIL import ImageGrab
import cv2
import aircv as ac
import shutil
import pyautogui

DEBUG_ENV = False


class Simulator(object):
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

    def check_upgrade(self, img_capture, comment):
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

    def click_xy(self, x, y, timeout):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        win32gui.SetForegroundWindow(self.hwnd)
        # print(left, top, right, bottom)
        # print(right - left, bottom - top)
        _x = left + x
        _y = top + y
        self._sleep(timeout)
        win32api.SetCursorPos((_x, _y))
        win32api.mouse_event(WCON.MOUSEEVENTF_LEFTDOWN, _x, _y, 0, 0)
        win32api.mouse_event(WCON.MOUSEEVENTF_LEFTUP, _x, _y, 0, 0)
        self._sleep(timeout)
        print("click", _x, _y)
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
        # APPSIMULATOR_IMAGES_HOME = os.environ["APPSIMULATOR_IMAGES_HOME"]
        try:
            shutil.copyfile('Z:/images/capture.png',
                            'Z:/images/capture_before.png')
        except Exception as e:
            print("send2web error:", e)
            pass

        shutil.copyfile(pic_path, 'Z:/images/capture.png')
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
            # self.send2web('images/capture.png')

            img_capture = ac.imread('images/capture.png')
            img_obj = ac.imread(obj_pic_path)
            pos = ac.find_template(img_capture, img_obj)
            if pos and pos['confidence'] > 0.9:
                print('匹配到', comment, timeout)
                x, y = pos['result']
                self._detect_obj(img=img_capture, circle_center_pos=(int(x), int(y)), circle_radius=40,
                                 color=(0, 255, 0),
                                 line_width=2)
                return True, int(x), int(y)
            else:
                print('未匹配到', comment, timeout)
                self._sleep(1)
                timeout -= 1
                self.check_upgrade(img_capture, comment=u"跳过软件升级")

        return False, -1, -1

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

    def check_screen_lock(self, timeout):
        win32gui.SetForegroundWindow(self.hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self._sleep(timeout)

        ret, x, y = self.find_element(comment='锁屏', timeout=10)
        if not ret:
            return False
        else:
            _x = left + x
            _y = top + y
            pyautogui.moveTo(_x, _y)
            pyautogui.dragTo(_x, _y - 400, 0.5, button='left')
            self._sleep(timeout)

            ret, x, y = self.find_element(comment='锁屏图案', timeout=10)
            if not ret:
                return False
            else:
                screen_lock = ac.imread('images_xiaoyao/screen_lock.png')
                h = screen_lock.shape[0]
                d = screen_lock.shape[1]
                _x = left + x - d
                _y = top + y - h
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
                self._sleep(timeout)
                return True

    def run(self):
        ret = None
        # hwnd = win32gui.FindWindow("Qt5QWindowIcon", None)
        if self.hwnd:
            ret = self.check_screen_lock(timeout=1)
            if not ret:
                ret = self.app_quit()
            if ret: self.script()

    def script(self):
        pass


if __name__ == "__main__":
    pass
