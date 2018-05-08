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

MOUSE_CLICK_POS_1 = (38, 783)  # 点击“更新”按钮
MOUSE_CLICK_POS_2 = (447, 617)  # 点击“分享”按钮
MOUSE_CLICK_POS_3 = (47, 700)  # 点击“复制链接”按钮


def click(hwnd, pos):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # print(left, top, right, bottom)
    # print(right - left, bottom - top)
    (x, y) = pos
    x = left + x
    y = top + y
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(WCON.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(WCON.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


# hwnd = win32gui.FindWindow("Qt5QWindowIcon", None)
hwnd = win32gui.FindWindow(None, "抖音0")
click(hwnd, MOUSE_CLICK_POS_1)

# click 38 783
# delay 1000
# click 447 617
# delay 1000
# click 47 700
