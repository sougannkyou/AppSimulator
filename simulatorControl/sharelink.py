import time
import win32con as WCON
import win32api
import win32gui
import win32clipboard as WCB

# hwnd = win32gui.FindWindow("Qt5QWindowIcon", None)
for i in range(1, 100):
    print(i)
    hwnd = win32gui.FindWindow(None, "抖音0")
    print(hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    print(left, top, right, bottom)
    print(right - left, bottom - top)

    title = win32gui.GetWindowText(hwnd)
    clsname = win32gui.GetClassName(hwnd)
    print(title, clsname)


    win32gui.SetForegroundWindow(hwnd)

    # win32api.SetCursorPos([left + 10, top + 10])
    # win32api.mouse_event(WCON.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    # time.sleep(0.3)
    # win32api.mouse_event(WCON.MOUSEEVENTF_LEFTUP,0,0,0,0)
    # win32api.SendMessage(hwnd,WCON.WM_SETTEXT,None,'A')

    time.sleep(5)
    win32api.keybd_event(13, 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(13, 0, WCON.KEYEVENTF_KEYUP, 0)

# 宏按键Enter的定义
# size 480 800
# click 38 783
# delay 1000
# click 447 617
# delay 1000
# click 47 700

