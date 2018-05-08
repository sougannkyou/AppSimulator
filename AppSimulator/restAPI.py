# coding=utf-8
import datetime, time
import os, sys
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

from .dbDriver import MongoDriver, RedisDriver
from lxml import etree

from .setting import PAGE_SIZE

MDB = MongoDriver()
RDB = RedisDriver()

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

