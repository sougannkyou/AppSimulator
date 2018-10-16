# coding=utf-8
import os
import sys
import psutil
import json
from pprint import pprint

from backend.settings import STATIC_ROOT
from datetime import datetime
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

from aip import AipImageClassify

from AppSimulator.Common import *
from AppSimulator.DBLib import MongoDriver, RedisDriver
from Controller.NoxConDocker import NoxConDocker

MDB = MongoDriver()
RDB = RedisDriver()

APP_ID = '14131380'
API_KEY = 'KyCbH0iKqkr1usuRAQR5CSga'
SECRET_KEY = 'IkS88smDf5Ab8OGvobIsDzM2x9zWRB7g'


def startProxyServerAPI(request):
    if sys.platform == 'win32':
        os.system('taskkill /t /f /fi "WINDOWTITLE eq ProxyServer"')
        os.system('start "ProxyServer" node.exe %ANYPROXY_HOME%\main.js')

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


def runTasksAPI(request):
    ret = True
    app_name = request.GET.get('app_name')  # 'dianping'
    tasks_cnt = request.GET.get('tasks_cnt')  # tasks

    output = JsonResponse({
        'ret': ret,
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


def getDevicesStatusAPI(request):
    app_name = request.GET.get('app_name')
    # ret = MDB.get_devices_status(app_name)  # {'device1':'running','device2':'unkown'}
    output = JsonResponse({
        'ret': [],
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


# ------- tasks ----------------------------------------------------------------
def addTaskAPI(request):
    app_name = request.POST.get('app_name')
    script = request.POST.get('script')
    redis_key = request.POST.get('redis_key')
    ip = request.POST.get('ip')
    live_cycle = request.POST.get('live_cycle', 'once')
    schedule_start = request.POST.get('schedule_start')
    schedule_end = request.POST.get('schedule_end')
    schedule_cycle = request.POST.get('schedule_cycle', '')
    timer = request.POST.get('timer', 'off')
    docker_img_name = request.POST.get('docker_img_name')
    description = request.POST.get('description')

    ret = MDB.emulator_add_task({
        'script': script,
        'redis_key': redis_key,
        'ip': ip,
        'app_name': app_name,
        'live_cycle': live_cycle,
        'schedule': {
            'start': string2timestamp(schedule_start) if schedule_start else 0,
            'end': string2timestamp(schedule_end) if schedule_end else 9999999999,
            'run_time': string2timestamp(schedule_start) if schedule_start else 0,
            'cycle': int(schedule_cycle) * 60 if schedule_cycle else 24 * 60 * 60,
        },
        'timer': timer,  # on off
        'docker_img_name': docker_img_name,
        'description': description
    })
    output = JsonResponse({
        'ret': ret
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def removeTaskAPI(request):
    taskId = request.POST.get('taskId')
    ret = MDB.emulator_remove_task(int(taskId))
    output = JsonResponse({
        'ret': ret
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')

def resetTaskAPI(request):
    taskId = request.POST.get('taskId')
    ret = MDB.emulator_reset_task(int(taskId))
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


def getTasksCntAPI(request):
    host_ip = request.GET.get('host_ip', '')
    ret = MDB.emulator_get_tasks_cnt(host_ip)
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


def getHeatmapAPI(request):
    ret = []
    taskIdList = json.loads(request.GET.get('taskIdList', '[]'))
    day = request.GET.get('day', datetime.now().strftime('%Y-%m-%d'))
    for i in range(len(taskIdList)):
        ret += MDB.emulator_get_start_by_day(i, taskIdList[i], day)

    ret1 = [
        [0, 0, 5], [0, 1, 1], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0], [0, 6, 0], [0, 7, 0], [0, 8, 0], [0, 9, 0],
        [0, 10, 0], [0, 11, 2], [0, 12, 4], [0, 13, 1], [0, 14, 1], [0, 15, 3], [0, 16, 4], [0, 17, 6], [0, 18, 4],
        [0, 19, 4], [0, 20, 3], [0, 21, 3], [0, 22, 2], [0, 23, 5],
        [1, 0, 7], [1, 1, 0], [1, 2, 0], [1, 3, 0], [1, 4, 0], [1, 5, 0], [1, 6, 0], [1, 7, 0], [1, 8, 0], [1, 9, 0],
        [1, 10, 5], [1, 11, 2], [1, 12, 2], [1, 13, 6], [1, 14, 9], [1, 15, 11], [1, 16, 6], [1, 17, 7], [1, 18, 8],
        [1, 19, 12], [1, 20, 5], [1, 21, 5], [1, 22, 7], [1, 23, 2],
        [2, 0, 1], [2, 1, 1], [2, 2, 0], [2, 3, 0], [2, 4, 0], [2, 5, 0], [2, 6, 0], [2, 7, 0], [2, 8, 0], [2, 9, 0],
        [2, 10, 3], [2, 11, 2], [2, 12, 1], [2, 13, 9], [2, 14, 8], [2, 15, 10], [2, 16, 6], [2, 17, 5], [2, 18, 5],
        [2, 19, 5], [2, 20, 7], [2, 21, 4], [2, 22, 2], [2, 23, 4],
        [3, 0, 7], [3, 1, 3], [3, 2, 0], [3, 3, 0], [3, 4, 0], [3, 5, 0], [3, 6, 0], [3, 7, 0], [3, 8, 1], [3, 9, 0],
        [3, 10, 5], [3, 11, 4], [3, 12, 7], [3, 13, 14], [3, 14, 13], [3, 15, 12], [3, 16, 9], [3, 17, 5], [3, 18, 5],
        [3, 19, 10], [3, 20, 6], [3, 21, 4], [3, 22, 4], [3, 23, 1],
        [4, 0, 1], [4, 1, 3], [4, 2, 0], [4, 3, 0], [4, 4, 0], [4, 5, 1], [4, 6, 0], [4, 7, 0], [4, 8, 0], [4, 9, 2],
        [4, 10, 4], [4, 11, 4], [4, 12, 2], [4, 13, 4], [4, 14, 4], [4, 15, 14], [4, 16, 12], [4, 17, 1], [4, 18, 8],
        [4, 19, 5], [4, 20, 3], [4, 21, 7], [4, 22, 3], [4, 23, 0],
        [5, 0, 2], [5, 1, 1], [5, 2, 0], [5, 3, 3], [5, 4, 0], [5, 5, 0], [5, 6, 0], [5, 7, 0], [5, 8, 2], [5, 9, 0],
        [5, 10, 4], [5, 11, 1], [5, 12, 5], [5, 13, 10], [5, 14, 5], [5, 15, 7], [5, 16, 11], [5, 17, 6], [5, 18, 0],
        [5, 19, 5], [5, 20, 3], [5, 21, 4], [5, 22, 2], [5, 23, 0],
        [6, 0, 1], [6, 1, 0], [6, 2, 0], [6, 3, 0], [6, 4, 0], [6, 5, 0], [6, 6, 0], [6, 7, 0], [6, 8, 0], [6, 9, 0],
        [6, 10, 1], [6, 11, 0], [6, 12, 2], [6, 13, 1], [6, 14, 3], [6, 15, 4], [6, 16, 0], [6, 17, 0], [6, 18, 0],
        [6, 19, 0], [6, 20, 1], [6, 21, 2], [6, 22, 2], [6, 23, 6]
    ]

    # pprint(ret)
    output = JsonResponse({
        'ret': ret
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getHeatmapFamilyAPI(request):
    taskId = int(request.GET.get('taskId', -1))
    ret = [
        ['times', 'crawlCnt', 'taskId'],
        [80, 5, 'task-10'],
        [60, 7, 'task-11'],
        [40, 12, 'task-12'],
        [80, 79, 'task-13'],
        [20, 91, 'task-14'],
        [100, 20, 'task-15']
    ]
    parent = MDB.tasks.find_one({'taskId': taskId})
    if parent:
        children = MDB.tasks.find({'orgTaskId': taskId})
        for c in children:
            score = spend_time_score(seconds=(c['up_time'] - c['start_time']))
            crawl_cnt = RDB.get_crawl_cnt_by_taskId(c['host_ip'], 'task-{}'.format(taskId))
            ret.append([score, crawl_cnt, taskId])

    output = JsonResponse({
        'ret': ret
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


# ------- emulators ------------------------------------------------------------
def getEmulatorsAPI(request):
    emulators = MDB.emulator_get_emulators(host_ip='')
    output = JsonResponse({
        'ret': emulators
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
    taskId = int(request.GET.get('taskId'))
    cnt = int(request.GET.get('cnt'))
    task = MDB.tasks_find_by_taskId(taskId)
    if task:
        docker = NoxConDocker(task_info=task)
        docker.docker_shake(cnt)

    output = JsonResponse({
        'ret': True if task else False,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


# ------- logger ----------------------------------------------------------------
def getLogsAPI(request):
    ip = request.GET.get('ip')
    log_filter = json.loads(request.GET.get('log_filter', {}))
    ret = MDB.log_find_by_ip(ip, log_filter)
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getLogCntAPI(request):
    ip = request.GET.get('ip')
    ret = MDB.log_cnt(ip)
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


# --------- img upload ------------------------------------------------
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


def detection(file_path):
    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
    image = get_file_content(file_path)
    client.carDetect(image)
    ret = client.carDetect(image, {'top_num': 10, 'baike_num': 5})  # 带参数调用车辆识别
    pprint(ret)
    return ret


def uploadAPI(request):
    ret = {'img_src': 'error.png'}
    try:
        img_src = str(int(datetime.now().timestamp() * 1000000))
        file_obj = request.FILES.get('file')
        fixed = file_obj.name[file_obj.name.find('.'):]
        img_path = os.path.join(STATIC_ROOT, 'upload', img_src + fixed)
        ret = {'img_src': '/static/upload/{}{}'.format(img_src, fixed)}
        print(img_path)
        f = open(img_path, 'wb')
        # print(file_obj, type(file_obj))
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        ret.update(detection(img_path))
    except Exception as e:
        ret = {'img_src': 'error.png'}
        print('error:', e)
    finally:
        return HttpResponse(JsonResponse(ret), content_type='application/json; charset=UTF-8')


if __name__ == "__main__":
    pass
