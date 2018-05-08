# coding: utf-8
from pprint import pprint
import time
import win32con as WCON
import win32api
import win32gui
import win32clipboard as WCB
from PIL import ImageGrab
import cv2
import aircv as ac

DEBUG_ENV = False

KEY_VALUE_0 = 48
KEY_VALUE_1 = 49
KEY_VALUE_2 = 50
KEY_VALUE_3 = 51


def _detect_obj(img, circle_center_pos, circle_radius, color, line_width):
    if DEBUG_ENV:
        cv2.circle(img, circle_center_pos, circle_radius, color, line_width)
        cv2.imshow('detect_obj', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def find_element(hwnd, element_pic_path, timeout):
    # 匹配element图像
    # pprint(pos)
    while (timeout > 0):
        win32gui.SetForegroundWindow(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        # print(left, top, right, bottom)
        # print(right - left, bottom - top)
        app_bg_box = (left, top, right, bottom)
        im = ImageGrab.grab(app_bg_box)
        im.save('images/capture.png')

        imsrc = ac.imread('images/capture.png')
        imobj = ac.imread(element_pic_path)
        pos = ac.find_template(imsrc, imobj)
        if pos and pos['confidence'] > 0.9:
            print('匹配到', element_pic_path, timeout)
            x, y = pos['result']
            _detect_obj(img=imsrc, circle_center_pos=(int(x), int(y)), circle_radius=40, color=(0, 255, 0),
                        line_width=2)
            return True
        else:
            time.sleep(1)
            timeout -= 1
            print('未匹配到', element_pic_path, timeout)

    return False


def send_key(hwnd, key_value, timeout):
    win32gui.SetForegroundWindow(hwnd)
    # win32api.SetCursorPos([left + 10, top + 10])
    # win32api.mouse_event(WCON.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    # time.sleep(0.3)
    # win32api.mouse_event(WCON.MOUSEEVENTF_LEFTUP,0,0,0,0)
    # win32api.SendMessage(hwnd,WCON.WM_SETTEXT,None,'A')

    # 向窗口发送Enter键
    time.sleep(timeout)
    win32api.keybd_event(key_value, 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(key_value, 0, WCON.KEYEVENTF_KEYUP, 0)
    print('发送', key_value, '键')
    time.sleep(timeout)
    return True
    # 宏按键Enter的定义
    # size 480 800
    # click 38 783
    # delay 1000
    # click 447 617
    # delay 1000
    # click 47 700


def script(hwnd):
    print(hwnd)
    time.sleep(2)
    win32api.keybd_event(KEY_VALUE_1, 0, 0, 0)
    win32api.keybd_event(KEY_VALUE_1, 0, WCON.KEYEVENTF_KEYUP, 0)
    print('发送', KEY_VALUE_1, '键')
    time.sleep(2)


if __name__ == "__main__":
    # hwnd = win32gui.FindWindow("Qt5QWindowIcon", None)
    hwnd = win32gui.FindWindow(None, "手机2")
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(2)
    win32api.keybd_event(KEY_VALUE_1, 0, 0, 0)
    win32api.keybd_event(KEY_VALUE_1, 0, WCON.KEYEVENTF_KEYUP, 0)