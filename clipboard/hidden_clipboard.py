import win32con as WCON
import win32gui
import win32clipboard as WCB


class MyWindow():
    def __init__(self):
        wc = win32gui.WNDCLASS()  # 注册一个窗口类
        wc.lpszClassName = 'AppSharerLink'
        wc.hbrBackground = WCON.COLOR_BTNFACE + 1
        wc.lpfnWndProc = self.wndProc
        class_atom = win32gui.RegisterClass(wc)

        self.hwnd = win32gui.CreateWindow(  # 创建窗口
            class_atom, u'分享链接', WCON.WS_OVERLAPPEDWINDOW,
            WCON.CW_USEDEFAULT, WCON.CW_USEDEFAULT,
            WCON.CW_USEDEFAULT, WCON.CW_USEDEFAULT,
            0, 0, 0, None)

        # win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL) # 显示窗口

    def wndProc(self, hwnd, msg, wParam, lParam):  # 消息处理
        if msg == WCON.WM_DESTROY:
            win32gui.PostQuitMessage(0)

        if msg == WCON.WM_DRAWCLIPBOARD:  # 当剪切板更新的时候收到这个消息
            utxt = None
            btxt = None
            try:  # 有时候打不开会出异常
                WCB.OpenClipboard()
                if WCB.IsClipboardFormatAvailable(WCON.CF_UNICODETEXT):  # 判断是否有指定的内容
                    utxt = WCB.GetClipboardData(WCON.CF_UNICODETEXT)
                    # if utxt.find('http') != -1:
                    #     utxt = utxt[utxt.find('http'):]
                if WCB.IsClipboardFormatAvailable(WCON.CF_TEXT):
                    btxt = WCB.GetClipboardData(WCON.CF_TEXT)
                    # if btxt.find('http') != -1:
                    #     btxt = btxt[btxt.find('http'):]
                    WCB.CloseClipboard()
            except Exception as e:
                print("error:", e)
            # finally:

            ok = False  # 依次尝试打印Unicode和字节码,ok是打印成功标志位
            if utxt:
                try:
                    if utxt.find('http') != -1:
                        utxt = utxt[utxt.find('http'):]
                    print("UNICODE:", utxt)
                    ok = True
                except Exception as e:
                    print(u'UNICODE打印失败:', e)

            if btxt and not ok:
                try:
                    print("GBK:", btxt.decode('gbk'))
                except Exception as e:
                    print(u'GBK打印失败:', e)

        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)


if __name__ == '__main__':
    mw = MyWindow()
    WCB.SetClipboardViewer(mw.hwnd)  # 注册为剪切板监听窗口
    win32gui.PumpMessages()
