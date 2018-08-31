# coding=utf-8
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from AppSimulator.views import (
    DashBoardView, TasksView, VMwareView, LoggerView, HostsView, EmulatorsView
)

from AppSimulator.WebAPI import (
    addTaskAPI, removeTaskAPI, getTasksAPI,
    getDeviceCrawlCntAPI, getResultSampleAPI, getDevicesStatusAPI,
    setDeviceGPSAPI, restartDeviceAPI, startScriptAPI, stopScriptAPI, quitAppAPI, startProxyServerAPI,
    getDeviceCaptureAPI, getProxyServerInfoAPI,
    runTasksAPI,
    getVMwaresAPI, getHostsAPI, getAllHostsAPI, getLoggerAPI, emulatorShakeAPI
)

cache_time_out = 60 * 3

urlpatterns = patterns('',
                       url(r'^dashboard/$', DashBoardView.as_view(), name='dashboard'),
                       url(r'^tasks/$', TasksView.as_view(), name='tasks'),
                       url(r'^emulators/$', EmulatorsView.as_view(), name='emulators'),
                       url(r'^hosts/$', HostsView.as_view(), name='hosts'),
                       url(r'^vmware/$', VMwareView.as_view(), name='vmware'),
                       url(r'^logger/$', LoggerView.as_view(), name='logger'),
                       url(r'^addTaskAPI/$', addTaskAPI, name='addTaskAPI'),
                       url(r'^removeTaskAPI/$', removeTaskAPI, name='removeTaskAPI'),
                       url(r'^getTasksAPI/$', getTasksAPI, name='getTasksAPI'),

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
                       # emulator
                       url(r'^emulatorShakeAPI/$', emulatorShakeAPI, name='emulatorShakeAPI'),
                       # vmware
                       url(r'^getVMwaresAPI/$', getVMwaresAPI, name='getVMwaresAPI'),
                       # hosts
                       url(r'^getHostsAPI/$', getHostsAPI, name='getHostsAPI'),
                       # all hosts
                       url(r'^getAllHostsAPI/$', getAllHostsAPI, name='getAllHostsAPI'),
                       # logger
                       url(r'^getLoggerAPI/$', getLoggerAPI, name='getLoggerAPI'),
                       )
