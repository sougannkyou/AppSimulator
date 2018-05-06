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


def _detect_obj(img, circle_center_pos, circle_radius, color, line_width):
    if DEBUG_ENV:
        cv2.circle(img, circle_center_pos, circle_radius, color, line_width)
        cv2.imshow('detect_obj', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def find_element(hwnd, element_pic_path, timeout):
    win32gui.SetForegroundWindow(hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # print(left, top, right, bottom)
    # print(right - left, bottom - top)

    app_bg_box = (left, top, right, bottom)
    im = ImageGrab.grab(app_bg_box)
    im.save('bg.png')

    imsrc = ac.imread('bg.png')
    imobj = ac.imread(element_pic_path)

    # 匹配element图像
    pos = ac.find_template(imsrc, imobj)
    pprint(pos)
    if pos['confidence'] > 0.9:
        print('能够匹配到element图像')
        x, y = pos['result']
        _detect_obj(img=imsrc, circle_center_pos=(int(x), int(y)), circle_radius=40, color=(0, 255, 0), line_width=2)
        return True
    else:
        print('未匹配到element图像')
        return False


def send_key(hwnd, key_value, timeout):
    win32gui.SetForegroundWindow(hwnd)
    # win32api.SetCursorPos([left + 10, top + 10])
    # win32api.mouse_event(WCON.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    # time.sleep(0.3)
    # win32api.mouse_event(WCON.MOUSEEVENTF_LEFTUP,0,0,0,0)
    # win32api.SendMessage(hwnd,WCON.WM_SETTEXT,None,'A')

    # 向窗口发送Enter键
    time.sleep(5)
    win32api.keybd_event(key_value, 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(key_value, 0, WCON.KEYEVENTF_KEYUP, 0)

    # 宏按键Enter的定义
    # size 480 800
    # click 38 783
    # delay 1000
    # click 447 617
    # delay 1000
    # click 47 700


if __name__ == "__main__":
    # hwnd = win32gui.FindWindow("Qt5QWindowIcon", None)
    hwnd = win32gui.FindWindow(None, "抖音0")
    # find_element('images/share.png')  # 查找分享按钮
    find_element(hwnd, element_pic_path='images/copylink.png', timeout=5000)  # 查找分享按钮
    send_key(hwnd, key_value=13, timeout=5000)  # Enter
