# coding=utf-8
import datetime, time
import os, sys
import psutil
import xmlrpc.client
import json
import copy
from io import StringIO
import bson.binary
import traceback
import requests
import re
from urllib.parse import urljoin
import subprocess
from pprint import pprint
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework import filters, pagination, serializers
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response as restResponse
from rest_framework import status
import socket

from .dbDriver import MongoDriver, RedisDriver
from .setting import *

MDB = MongoDriver()
RDB = RedisDriver()


def getRpcServerStatus(deviceId):
    info = MDB.get_config_info(deviceId)
    # print('get_config_info', deviceId, info['ip'])
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy("http://" + info['ip'] + ":" + str(RPC_PORT)) as proxy:
        ret = proxy.getRpcServerStatus()
    socket.setdefaulttimeout(None)

    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def startProxyServerAPI(request):
    if (sys.platform == 'win32'):
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
    print(deviceId, latitude, longitude)
    with xmlrpc.client.ServerProxy(RPC_CLIENT) as proxy:
        ret = proxy.setDeviceGPS(deviceId, latitude, longitude)

    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def restartDeviceAPI(request):
    deviceId = request.GET.get('deviceId')  # 设备ID

    with xmlrpc.client.ServerProxy(RPC_CLIENT) as proxy:
        ret = proxy.restartDevice(deviceId)

    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def quitAppAPI(request):
    deviceId = request.GET.get('deviceId')  # 设备ID
    with xmlrpc.client.ServerProxy(RPC_CLIENT) as proxy:
        ret = proxy.quitApp()
    # ret = True
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def startScriptAPI(request):
    deviceId = request.GET.get('deviceId')  # 设备ID
    with xmlrpc.client.ServerProxy(RPC_CLIENT) as proxy:
        ret = proxy.startScript()
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def stopScriptAPI(request):
    deviceId = request.GET.get('deviceId')  # 设备ID
    with xmlrpc.client.ServerProxy(RPC_CLIENT) as proxy:
        ret = proxy.stopScript()
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
    app_name = request.GET.get('appName')
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
    app_name = request.GET.get('appName')
    ret = MDB.get_devices_status(app_name)  # {'device1':'running','device2':'unkown'}
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getResultSampleAPI(request):
    ret = RDB.get_result_sample()
    output = JsonResponse({
        'ret': ret,
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


class HubXPathViewAPI(APIView):
    def _get_data(self, args):
        taskId = args.get('taskId')
        level = args.get('level')
        return 0

    def _set_data(self, args):
        return 0

    def _remove_data(self, args):
        taskId = args.get('taskId')
        hub_url = args.get('hub_url', '')

        msg = '删除了一条信息。'
        return 0

    def get(self, request, *args, **kwargs):
        ret = self._get_data(request.GET)
        output = JsonResponse(ret)
        return HttpResponse(output, content_type='application/json; charset=UTF-8')

    def post(self, request, *args, **kwargs):
        ret, msg = self._set_data(request.POST)
        # if 'upserted' in ret:
        #     ret.pop('upserted')  # 含有objectId 无法json编码
        output = JsonResponse({'ret': ret, 'msg': msg})
        return HttpResponse(output, content_type='application/json; charset=UTF-8')

    def put(self, request, *args, **kwargs):  # print('put:', request.POST)
        ret, msg = self._set_data(request.POST)
        output = JsonResponse({'ret': ret, 'msg': msg})
        return HttpResponse(output, content_type='application/json; charset=UTF-8')

    def delete(self, request, *args, **kwargs):
        if request.POST:
            ret, msg = self._remove_data(request.POST)
        else:
            ret, msg = self._remove_data(request.query_params)
        output = JsonResponse({'ret': ret, 'msg': msg})
        return HttpResponse(output, content_type='application/json; charset=UTF-8')
