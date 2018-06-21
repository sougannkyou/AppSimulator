# coding=utf8
import os
import time
import psutil
import win32gui
from PIL import ImageGrab
import shutil
from xmlrpc.server import SimpleXMLRPCServer
from Controllor.setting import *
from Controllor.DBLib import MongoDriver

MDB = MongoDriver()


# ------------------------ docker rpc server ----------------------
def getRpcServerStatus():
    return "running"


def simulatorStatus():
    return "running"


def startScript():
    os.system('taskkill /f /t /fi "WINDOWTITLE eq script"')
    os.system('start /B start "script" cmd.exe @cmd /k python %RPCSERVER_HOME%script_douyin.py')
    return True


def startTask(app_name):
    os.system('taskkill /f /t /fi "WINDOWTITLE eq script"')
    os.system('start /B start "script" cmd.exe @cmd /k python %RPCSERVER_HOME%script_douyin.py')
    return True


def stopScript():
    os.system('taskkill /f /t /fi "WINDOWTITLE eq script"')
    return True


def send2web(pic_path):
    try:
        shutil.copyfile('../static/AppSimulator/images/capture.png',
                        '../static/AppSimulator/images/capture_before.png')
        shutil.copyfile(pic_path, '../static/AppSimulator/images/capture.png')
    except Exception as e:
        print("[rpc_server] send2web err", e)

    return True


def run_captrue():
    print("[rpc_server] run_captrue")
    while True:
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

    return True


def setDeviceGPS(deviceId, latitude, longitude):
    print(deviceId, latitude, longitude)  # 39.6099202570, 118.1799316404
    p = os.popen("[rpc_server] adb shell setprop persist.nox.gps.latitude " + latitude)
    print(p.read())

    p = os.popen("[rpc_server] adb shell setprop persist.nox.gps.longitude " + longitude)
    print(p.read())
    return True


def get_free_mem():
    mem = psutil.virtual_memory()
    ret = '%.1f' % (mem.free / GB)
    return ret


def _clean():
    os.system("c:\\Nox\\bin\\NoxConsole quitall")
    time.sleep(10)


def _backup_app():
    l = []
    for root, dirs, files in os.walk('C:\\Nox\\backup'):
        for file in files:
            if os.path.splitext(file)[1] == '.npbk':
                p = os.path.splitext(file)[0]
                l.append(p[4:])

    return l


def _registor():
    mem = psutil.virtual_memory()
    MDB.registor_rpc_server({
        'ip': os.getenv('APPSIMULATOR_IP'),
        'port': RPC_PORT,
        'app_name': _backup_app(),
        'mem_free': '%.1f' % (mem.free / GB),
        'mem_total': '%.1f' % (mem.total / GB),
    })
    return


def start_rpc_server():
    # netstat -ano | findstr "8003"
    _clean()
    server = SimpleXMLRPCServer(("0.0.0.0", RPC_PORT))
    server.register_function(restartDevice, "restartDevice")
    server.register_function(setDeviceGPS, 'setDeviceGPS')
    server.register_function(startScript, "startScript")
    server.register_function(stopScript, "stopScript")
    server.register_function(getRpcServerStatus, "getRpcServerStatus")
    server.register_function(simulatorStatus, "simulatorStatus")
    server.register_function(get_free_mem, "get_free_mem")
    _registor()
    print("[rpc_server] start ...")
    server.serve_forever()  # never stop
    print("[rpc_server] done.")


######################################################################
if __name__ == "__main__":
    start_rpc_server()
