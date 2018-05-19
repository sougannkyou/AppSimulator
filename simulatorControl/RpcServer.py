# coding=utf8
import os
import time,datetime
import win32gui
from PIL import ImageGrab
import shutil
from xmlrpc.server import SimpleXMLRPCServer
from simulator import Simulator

def runScript1():
    print("[rpc_server] runScript")
    # try:
    # mySimulator = MySimulator("douyin0")
    # mySimulator._PIC_PATH = {
    #     u"APP图标": 'images/app_ready.png',
    #     u"更新": 'images/update.png',
    #     u"分享": 'images/share.png',
    #     u"复制链接": 'images/copylink.png',
    #     u"跳过软件升级": 'images/is_upgrade.png',
    #     u"锁屏": 'images/screen_lock.png'
    # }
    #
    # mySimulator._CLICK_POS = {
    #     u"APP图标": (38, 793),
    #     u"更新": (38, 793),
    #     u"分享": (451, 628),
    #     u"复制链接": (47, 720),
    #     u"跳过软件升级": (231, 590)  # 以后再说
    # }
    # mySimulator.run()

    # except Exception as e:
    #     print("[rpc_server] runScript err", e)
    return True

def runScript():
    print("[rpc_server] runScript start:",datetime.datetime.now())
    try:
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

                    if ret:
                        ret = self.find_element(comment='复制链接', timeout=10)
                        if not ret:
                            print("重试 click 分享 按钮 ...")
                            ret = self.find_element(comment='分享', timeout=10)
                            if ret: ret = self.click(u"分享", timeout=1)

                    if ret: ret = self.click(u"复制链接", timeout=1)
                    if not ret: self.send2web('images/offline.jpeg')

        mySimulator = MySimulator("douyin0")
        mySimulator._PIC_PATH = {
            u"APP图标": 'images/app_ready.png',
            u"更新": 'images/update.png',
            u"分享": 'images/share.png',
            u"复制链接": 'images/copylink.png',
            u"跳过软件升级": 'images/is_upgrade.png',
            u"锁屏": 'images/screen_lock.png'
        }

        mySimulator._CLICK_POS = {
            u"APP图标": (38, 793),
            u"更新": (38, 793),
            u"分享": (451, 628),
            u"复制链接": (47, 720),
            u"跳过软件升级": (231, 590)  # 以后再说
        }
        mySimulator.run()
        print("[rpc_server] runScript end:", datetime.datetime.now())
        return True
    except Exception as e:
        print("[rpc_server] runScript error:", datetime.datetime.now() ,e)
        return False

def send2web(pic_path):
    try:
        shutil.copyfile('../static/AppSimulator/images/capture.png',
                        '../static/AppSimulator/images/capture_before.png')
        shutil.copyfile(pic_path, '../static/AppSimulator/images/capture.png')
    except Exception as e:
        print("[rpc_server] send2web err", e)


def run_captrue():
    print("[rpc_server] run_captrue")
    while (1):
        capture('douyin0')
        time.sleep(5)


def capture(app_name):
    hwnd = win32gui.FindWindow(None, app_name)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        app_bg_box = (left, top, right, bottom)
        im = ImageGrab.grab(app_bg_box)
        im.save('images/capture.png')
        send2web('images/capture.png')
    else:
        send2web('images/offline.jpeg')


def restartDevice(deviceId):
    print("[rpc_server] restartDevice")
    # print("Nox.exe -quit :", p.read())
    while (1):
        time.sleep(2)
        p = os.popen('tasklist | findstr Nox.exe')
        msg = p.read()
        print("[rpc_server] tasklist | findstr Nox.exe\n", msg)
        if len(msg) > 0:
            print("[rpc_server] 模拟器正在 运行 ...")
            os.popen("C:\\Nox\\bin\\Nox.exe -quit")
            # os.popen("taskkill /f /t /im Nox.exe")
            # os.popen("taskkill /f /t /im NoxVMSVC.exe")
            # os.popen("taskkill /f /t /im NoxVMHandle.exe")
        else:
            print("[rpc_server] 将重启模拟器 ...")
            p = os.popen("C:\\Nox\\bin\\Nox.exe")
            # msg = p.read() # 不能使用 会将命令阻塞
            break

    return True


def setDeviceGPS(deviceId, latitude, longitude):
    print(deviceId, latitude, longitude)  # 39.6099202570, 118.1799316404
    p = os.popen("[rpc_server] adb shell setprop persist.nox.gps.latitude " + latitude)
    print(p.read())

    p = os.popen("[rpc_server] adb shell setprop persist.nox.gps.longitude " + longitude)
    print(p.read())
    return True


######################################################################
# netstat -ano | findstr "8003"
server = SimpleXMLRPCServer(("0.0.0.0", 8003))
server.register_function(restartDevice, "restartDevice")
server.register_function(setDeviceGPS, 'setDeviceGPS')
server.register_function(runScript, "runScript")
# server.register_function(quitApp, "quitApp")
# run_captrue()
print("[rpc_server] start ...")
server.serve_forever()
