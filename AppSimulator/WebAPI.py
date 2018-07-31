# coding=utf-8
import os
import sys
import psutil
from pprint import pprint
from io import StringIO
import bson.binary
import traceback
import requests
import re
from urllib.parse import urljoin
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_protect, csrf_exempt
# from rest_framework import filters, pagination, serializers
# from rest_framework.generics import ListAPIView
# from rest_framework.views import APIView
# from rest_framework.response import Response as restResponse
# from rest_framework import status

from AppSimulator.DBLib import MongoDriver, RedisDriver
from AppSimulator.RPCLib import *
from Controller.NoxConDocker import NoxConDocker

MDB = MongoDriver()
RDB = RedisDriver()


def getRpcServerStatus(deviceId):
    info = MDB.emulator_get_config_info(deviceId)
    # print('emulator_get_config_info', deviceId, info['ip'])

    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def startProxyServerAPI(request):
    if sys.platform == 'win32':
        os.system('taskkill /t /f /fi "WINDOWTITLE eq ProxyServer"')
        os.system('start "ProxyServer" node.exe %ANYPROXY_HOME%\main.js')

    output = JsonResponse({
        'ret': 'ok',
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getProxyServerStatusAPI(request):
    output = JsonResponse({
        'ret': 'ok',
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


# popen.system("tasklist /fi anyproxy")
def setDeviceGPSAPI(request):
    deviceId = request.POST.get('deviceId')  # 设备ID
    latitude = request.POST.get('latitude')  # 经度
    longitude = request.POST.get('longitude')  # 纬度

    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def restartDeviceAPI(request):
    deviceId = request.GET.get('deviceId')  # 设备ID

    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def quitAppAPI(request):
    deviceId = request.GET.get('deviceId')  # 设备ID

    # ret = True
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def startScriptAPI(request):
    deviceId = request.GET.get('deviceId')  # 设备ID
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def stopScriptAPI(request):
    deviceId = request.GET.get('deviceId')  # 设备ID
    ret = rpc_stop_script()
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def runTasksAPI(request):
    ret = True
    app_name = request.GET.get('app_name')  # 'dianping'
    tasks_cnt = request.GET.get('tasks_cnt')  # tasks

    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getDeviceCaptureAPI(request):
    # deviceId = request.POST.get('deviceId')  # 设备ID
    # try:
    #     hwnd = win32gui.FindWindow(None, "douyin0")
    #     print("getDeviceCaptureAPI start.", hwnd)
    #     win32gui.SetForegroundWindow(hwnd)
    #     left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    #     app_bg_box = (left, top, right, bottom)
    #     im = ImageGrab.grab(app_bg_box)
    #     im.save('capture.png')
    #     shutil.copyfile('capture.png', './static/AppSimulator/images/capture.png')
    # except Exception as e:
    #     print(e)
    # %errorlevel%
    output = JsonResponse({
        'ret': 'ok',
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getProxyServerInfoAPI(request):
    partition = psutil.disk_usage('/')
    mem_info = psutil.virtual_memory()
    output = JsonResponse({
        'hd_info': {
            'percent': partition.percent
        },
        'cpu_info': {
            'user': 0,
            'system': 0,
            'idle': 0,
            'percent': psutil.cpu_percent()
        },
        'mem_info': {
            'total': mem_info.total,
            'avaiable': mem_info.available,
            'percent': mem_info.percent,
            'used': mem_info.used,
            'free': mem_info.free
        },
        'ret': 'ok',
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getDeviceCrawlCntAPI(request):
    app_name = request.GET.get('app_name')
    info = RDB.get_crwal_cnt_by_device(app_name)
    print('getDeviceCrawlCntAPI:', info)
    MDB.update_device_statistics_info(info=info, scope_times=SCOPE_TIMES)
    print("getDeviceCrawlCntAPI end", info)
    # info.pop('dedup_cnt')
    output = JsonResponse({
        'ret': info,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getDevicesStatusAPI(request):
    app_name = request.GET.get('app_name')
    # ret = MDB.get_devices_status(app_name)  # {'device1':'running','device2':'unkown'}
    output = JsonResponse({
        'ret': [],
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getResultSampleAPI(request):
    ret = RDB.get_result_sample()
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


# ------- tasks ----------------------------------------------------------------
def addTaskAPI(request):
    app_name = request.POST.get('app_name')
    script = request.POST.get('script')
    live_cycle = request.POST.get('live_cycle')
    ret = MDB.emulator_add_task({'script': script, 'app_name': app_name, 'live_cycle': live_cycle})
    output = JsonResponse({
        'ret': ret
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getTasksAPI(request):
    # status = request.POST.get('status')
    # ret = MDB.emulator_get_tasks({'status': status})
    ret = MDB.emulator_get_tasks()
    output = JsonResponse({
        'ret': ret
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def runTasks():
    tasks = MDB.emulator_get_tasks(status=STATUS_WAIT)
    output = JsonResponse({
        'ret': tasks
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


# ------- vmware ----------------------------------------------------------------
def getVMwaresAPI(request):
    host_ip = request.GET.get('host_ip')
    ret = MDB.vm_find_by_host(host_ip)
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getVMwareActiveInfoAPI(request):
    host_ip = request.GET.get('host_ip')
    ret = MDB.vm_actioveInfo_by_host(host_ip)
    output = JsonResponse({
        'interval': ret['interval'],
        'cntList': ret['cntList'],
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


# ------- hosts ----------------------------------------------------------------
def getHostsAPI(request):
    host_type = request.GET.get('host_type')
    if host_type == 'emulator':
        ret = MDB.emulator_get_hosts()
    else:
        ret = MDB.vm_get_hosts()

    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getAllHostsAPI(request):
    ret = MDB.all_get_hosts()
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def addHostAPI(request):
    ip = request.POST.get('ip')
    host_type = request.POST.get('host_type')
    timer_max_cnt = request.POST.get('timer_max_cnt')
    mem_total = request.POST.get('mem_total')
    support_app_list = request.POST.get('support_app_list')

    host = {
        "ip": ip,
        "host_type": host_type,
        "support_app_list": support_app_list.split(','),
        "timer_max_cnt": int(timer_max_cnt),
        "mem_total": float(mem_total)
    }
    ret = MDB.emulator_add_host(host)
    output = JsonResponse({
        'ret': True if ret else False,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def emulatorShakeAPI(request):
    taskId = request.GET.get('taskId')
    cnt = request.GET.get('cnt')
    task = MDB.tasks_find_by_taskId(taskId)
    if task:
        docker = NoxConDocker(task_info=task)
        docker.shake(cnt)

    output = JsonResponse({
        'ret': True if task else False,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


# ------- logger ----------------------------------------------------------------
def getLoggerAPI(request):
    ip = request.GET.get('ip')
    ret = MDB.log_find_by_ip(ip)
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


if __name__ == "__main__":
    test()
