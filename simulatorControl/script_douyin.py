# coding: utf-8
from pprint import pprint
import time
import win32con as WCON
import win32api
import win32gui
from PIL import ImageGrab
import cv2
import aircv as ac
import shutil
import pyautogui

DEBUG_ENV = False

PIC_PATH = {
    u"APP图标": 'images/app_ready.png',
    u"更新": 'images/update.png',
    u"分享": 'images/share.png',
    u"复制链接": 'images/copylink.png',
    u"跳过软件升级": 'images/is_upgrade.png',
    u"锁屏": 'images/screen_lock.png'
}

CLICK_POS = {
    u"APP图标": (38, 793),
    u"更新": (38, 793),
    u"分享": (451, 628),
    u"复制链接": (47, 720),
    u"跳过软件升级": (231, 590)  # 以后再说
}

UNLOCK_POS = {
    "step1": (133, 496),
    "step2": (132, 705),
    "step3": (343, 707)
}


def is_upgrade(img_capture, comment):
    img_obj = ac.imread(PIC_PATH[comment])
    pos = ac.find_template(img_capture, img_obj)
    if pos and pos['confidence'] > 0.9:
        print('版本更新提示', PIC_PATH[comment])
        click(hwnd, u"跳过软件升级", 1)
        click(hwnd, u"分享", 1)


def click(hwnd, comment, timeout):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    win32gui.SetForegroundWindow(hwnd)
    # print(left, top, right, bottom)
    # print(right - left, bottom - top)
    (x, y) = CLICK_POS[comment]
    x = left + x
    y = top + y
    time.sleep(timeout)
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(WCON.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(WCON.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(timeout)
    print("click", comment)
    return True


def _detect_obj(img, circle_center_pos, circle_radius, color, line_width):
    if DEBUG_ENV:
        cv2.circle(img, circle_center_pos, circle_radius, color, line_width)
        cv2.imshow('detect_obj', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def send2web(pic_path):
    shutil.copyfile('../static/AppSimulator/images/capture.png',
                    '../static/AppSimulator/images/capture_before.png')
    shutil.copyfile(pic_path, '../static/AppSimulator/images/capture.png')


def find_element(hwnd, comment, timeout):
    # 匹配element图像
    # pprint(pos)
    obj_pic_path = PIC_PATH[comment]
    while (timeout > 0):
        win32gui.SetForegroundWindow(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        app_bg_box = (left, top, right, bottom)
        im = ImageGrab.grab(app_bg_box)
        im.save('images/capture.png')
        send2web('images/capture.png')

        img_capture = ac.imread('images/capture.png')
        img_obj = ac.imread(obj_pic_path)
        pos = ac.find_template(img_capture, img_obj)
        if pos and pos['confidence'] > 0.9:
            print('匹配到', comment, timeout)
            x, y = pos['result']
            _detect_obj(img=img_capture, circle_center_pos=(int(x), int(y)), circle_radius=40, color=(0, 255, 0),
                        line_width=2)
            return True
        else:
            print('未匹配到', comment, timeout)
            time.sleep(1)
            timeout -= 1
            is_upgrade(img_capture, comment=u"跳过软件升级")

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
    # time.sleep(0.5)
    win32api.keybd_event(key_value, 0, WCON.KEYEVENTF_KEYUP, 0)
    print('发送', key_value, '键')
    time.sleep(timeout)
    return True


def app_quit(hwnd):
    send_key(hwnd, WCON.VK_ESCAPE, 1)
    send_key(hwnd, WCON.VK_ESCAPE, 1)
    send_key(hwnd, WCON.VK_ESCAPE, 1)
    send_key(hwnd, WCON.VK_ESCAPE, 1)


def unlock(hwnd, timeout):
    win32gui.SetForegroundWindow(hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    top += 20
    time.sleep(timeout)

    (x, y) = UNLOCK_POS['step1']
    x = left + x
    y = top + y
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()

    (x, y) = UNLOCK_POS['step2']
    x = left + x
    y = top + y
    # pyautogui.dragTo(x, y, 0.5, button='left')
    pyautogui.moveTo(x, y, 1, pyautogui.easeInQuad)

    (x, y) = UNLOCK_POS['step3']
    x = left + x
    y = top + y
    # pyautogui.dragTo(x, y, 0.5, button='left')
    pyautogui.moveTo(x, y, 1, pyautogui.easeInBounce)
    pyautogui.mouseUp()
    time.sleep(timeout)
    return True


def start(hwnd):
    ret = None
    if hwnd: ret = find_element(hwnd, comment='APP图标', timeout=10)  # unlock ok
    if ret: ret = click(hwnd, u"APP图标", timeout=2)
    while (ret):
        if ret: ret = find_element(hwnd, comment='更新', timeout=10)
        if ret: ret = click(hwnd, u"更新", timeout=1)

        if ret: ret = find_element(hwnd, comment='分享', timeout=10)
        if ret: ret = click(hwnd, u"分享", timeout=1)

        if ret: ret = find_element(hwnd, comment='复制链接', timeout=10)
        if ret: ret = click(hwnd, u"复制链接", timeout=1)


if __name__ == "__main__":
    ret = None
    # hwnd = win32gui.FindWindow("Qt5QWindowIcon", None)
    hwnd = win32gui.FindWindow(None, "douyin0")
    if hwnd: ret = find_element(hwnd, comment='锁屏', timeout=5)
    if ret: unlock(hwnd, 1)
    app_quit(hwnd)
    start(hwnd)
