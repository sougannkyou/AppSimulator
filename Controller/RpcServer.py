# coding=utf8
import os
import time
import psutil
import win32gui
from PIL import ImageGrab
import shutil
from xmlrpc.server import SimpleXMLRPCServer
from Controller.setting import *
from Controller.Common import common_log
from Controller.DBLib import MongoDriver
from Controller.NoxConDocker import NoxConDocker

RPC_SERVER_DEBUG = True
MDB = MongoDriver()


# ------------------------ docker rpc server ----------------------
def _rpc_log(prefix, msg):
    common_log(RPC_SERVER_DEBUG, '[RpcServer]', prefix, msg)


def reset_vm(docker_name):
    os.system('%APPSIMULATOR_WORK_PATH%\cmd\VMReset.cmd ' + docker_name)
    return True


def set_app_name_to_vm(docker_name, app_name):
    # docker_name: vm1 vm2 vm3
    os.system(
        'vmrun.exe  -T ws -gu "zhxg" -gp "zhxg2018" CopyFileFromHostToGuest "c:\VMWare\VM\\vm1\Windows 7 x64.vmx"  %APPSIMULATOR_WORK_PATH%"\cmd\\app.conf"')
    os.system('vmrun.exe reset "c:\VMWare\VM\\' + docker_name + '\Windows 7 x64.vmx"')
    return True


def start_script():
    os.system('taskkill /f /t /fi "WINDOWTITLE eq script"')
    os.system('start /B start "script" cmd.exe @cmd /k python %RPCSERVER_HOME%script_douyin.py')
    return True


def start_task(app_name):
    os.system('taskkill /f /t /fi "WINDOWTITLE eq script"')
    os.system('start /B start "script" cmd.exe @cmd /k python %RPCSERVER_HOME%script_douyin.py')
    return True


def stop_script():
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


def restart_device(deviceId):
    print("[rpc_server] restartDevice")
    # print("Nox.exe -quit :", p.read())

    return True


def set_device_gps(deviceId, latitude, longitude):
    print(deviceId, latitude, longitude)  # 39.6099202570, 118.1799316404
    p = os.popen("[rpc_server] adb shell setprop persist.nox.gps.latitude " + latitude)
    print(p.read())

    p = os.popen("[rpc_server] adb shell setprop persist.nox.gps.longitude " + longitude)
    print(p.read())
    return True


def _get_free_mem():
    _rpc_log('_get_free_mem', 'start')
    mem = psutil.virtual_memory()
    # STATUS_WAIT or STATUS_BUILDING
    mem_free = mem.free - MDB.task_get_my_prepare_tasks_cnt() * GB
    ret = '%.1f' % (mem_free / GB)
    _rpc_log('_get_free_mem ret: ', ret + " GB")
    return float(ret)


def _get_running_docker_cnt():
    _rpc_log('_get_running_docker_cnt', 'start')
    docker = NoxConDocker({'taskId': 0, 'app_name': 'miaopai', 'docker_name': '', 'timer_no': 0})
    dockers = docker.ps(docker_name=None, docker_status=STATUS_DOCKER_RUN_OK)
    ret = len(dockers)
    _rpc_log('_get_running_docker_cnt ret: ', str(ret))
    return ret


def can_add_task():
    _rpc_log('can_add_task', 'start')
    ret = 'yes'
    if _get_free_mem() < 1.0:
        ret = '剩余内存小于1GB'

    if _get_running_docker_cnt() >= len(TIMER):
        ret = '启动docker不能大于' + str(len(TIMER)) + '个'

    _rpc_log('can_add_task ret: ', ret)
    return ret


def _clean():
    os.system("c:\\Nox\\bin\\NoxConsole quitall")
    time.sleep(10)


def nox_backup_app_list():
    l = []
    for root, dirs, files in os.walk('C:\\Nox\\backup'):
        for file in files:
            if os.path.splitext(file)[1] == '.npbk':
                p = os.path.splitext(file)[0]  # nox-dianping.npbk
                l.append(p[4:])

    return l


def _register_service():
    _rpc_log('_register', 'start')
    mem = psutil.virtual_memory()
    info = {
        'ip': LOCAL_IP,
        'port': RPC_PORT,
        'support_app_list': nox_backup_app_list(),
        'mem_free': '%.1f' % (mem.free / GB),
        'mem_total': '%.1f' % (mem.total / GB),
        'timer_max_cnt': len(TIMER)
    }
    MDB.host_register_service(info)
    _rpc_log('_register', 'end')
    return


def start_rpc_server():
    # netstat -ano | findstr "8003"
    _clean()
    server = SimpleXMLRPCServer(("0.0.0.0", RPC_PORT))
    server.register_function(restart_device, "restart_device")
    server.register_function(set_device_gps, 'set_device_gps')
    server.register_function(start_script, "start_script")
    server.register_function(stop_script, "stop_script")
    server.register_function(can_add_task, "can_add_task")
    server.register_function(reset_vm, "reset_vm")
    _register_service()
    _rpc_log("start", "...")
    server.serve_forever()  # never stop
    _rpc_log("end", "")


######################################################################
if __name__ == "__main__":
    RPC_SERVER_DEBUG = True
    # can_add_task()
    start_rpc_server()
