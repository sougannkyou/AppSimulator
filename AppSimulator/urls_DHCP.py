# coding=utf-8
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from .views import (
    DashBoardView, DevicesManagerView
)

from .restAPI import (
    HubXPathViewAPI, getDeviceCrawlCntAPI, getResultSampleAPI, getDevicesStatusAPI,
    setDeviceGPSAPI, restartDeviceAPI, startScriptAPI, stopScriptAPI, quitAppAPI, startProxyServerAPI,
    getDeviceCaptureAPI, getProxyServerInfoAPI,
    runTasksAPI,
)

cache_time_out = 60 * 3

urlpatterns = patterns('',
                       url(r'^dashboard/$', DashBoardView.as_view(), name='dashboard'),
                       url(r'^devices/$', DevicesManagerView.as_view(), name='devices'),
                       url(r'^getDeviceCrawlCntAPI/$', getDeviceCrawlCntAPI, name='getDeviceCrawlCntAPI'),
                       url(r'^getDevicesStatusAPI/$', getDevicesStatusAPI, name='getDevicesStatusAPI'),
                       url(r'^getResultSampleAPI/$', getResultSampleAPI, name='getResultSampleAPI'),
                       url(r'^startProxyServerAPI/$', startProxyServerAPI, name='startProxyServerAPI'),

                       url(r'^setDeviceGPSAPI/$', setDeviceGPSAPI, name='setDeviceGPSAPI'),
                       url(r'^restartDeviceAPI/$', restartDeviceAPI, name='restartDeviceAPI'),
                       url(r'^startScriptAPI/$', startScriptAPI, name='startScriptAPI'),
                       url(r'^stopScriptAPI/$', stopScriptAPI, name='stopScriptAPI'),
                       url(r'^quitAppAPI/$', quitAppAPI, name='quitAppAPI'),
                       url(r'^runTasksAPI/$', runTasksAPI, name='runTasksAPI'),

                       url(r'^getDeviceCaptureAPI/$', getDeviceCaptureAPI, name='getDeviceCaptureAPI'),
                       url(r'^getProxyServerInfoAPI/$', getProxyServerInfoAPI, name='getProxyServerInfoAPI'),
                       )
