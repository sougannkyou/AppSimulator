# coding=utf-8
import datetime, time
import os, sys
import psutil
import json
import copy
from io import StringIO
import bson.binary
import traceback
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lxml.cssselect import CSSSelector
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

import win32gui
from PIL import ImageGrab
import shutil

from .dbDriver import MongoDriver, RedisDriver

from .setting import PAGE_SIZE

MDB = MongoDriver()
RDB = RedisDriver()


def setDeviceGPSAPI(request):
    deviceId = request.POST.get('deviceId')  # 设备ID
    latitude = request.POST.get('latitude')  # 经度
    longitude = request.POST.get('longitude')  # 纬度
    print(latitude, longitude)  # 39.6099202570, 118.1799316404
    p = os.popen("adb shell setprop persist.nox.gps.latitude " + latitude)
    print(p.read())

    p = os.popen("adb shell setprop persist.nox.gps.longitude " + longitude)
    print(p.read())
    output = JsonResponse({
        'ret': 'ok',
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def resetDeviceAPI(request):
    # deviceId = request.POST.get('deviceId')  # 设备ID
    print("resetDeviceAPI start.")
    p = os.popen("Nox -quit")
    print("Nox -quit", p.read())

    p = os.popen("tasklist | findstr 'Nox'")
    print("tasklist | findstr 'Nox'", p.read())

    time.sleep(5)
    p = os.popen("Nox")
    print("Nox", p.read())

    output = JsonResponse({
        'ret': 'ok',
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


def getMemoryInfo(request):
    cpu = {'user': 0, 'system': 0, 'idle': 0, 'percent': 0}
    mem = {'total': 0, 'avaiable': 0, 'percent': 0, 'used': 0, 'free': 0}
    mem_info = psutil.virtual_memory()
    mem['total'] = mem_info.total
    mem['available'] = mem_info.available
    mem['percent'] = mem_info.percent
    mem['used'] = mem_info.used
    mem['free'] = mem_info.free
    output = JsonResponse({
        'ret': 'ok',
    })
    return HttpResponse(output, content_type='application/json; charset=UTF-8')


def getDeviceInfoAPI(request):
    ret = RDB.get_device_info()
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
        info = MDB.get_hub_xpath_info(taskId, int(level))
        return info

    def _set_data(self, args):
        xgsjTaskId = int(args.get('xgsjTaskId')) if args.get('xgsjTaskId') else -1

        return ret, msg

    def _remove_data(self, args):
        taskId = args.get('taskId')
        hub_url = args.get('hub_url', '')

        ret = MDB.remove_hub_xpath_info(taskId)
        msg = '删除了一条信息。'
        return ret, msg

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
