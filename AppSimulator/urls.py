from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from AppSimulator.views import (
    DashBoardView, TasksView, VMwareView, LoggerView, HostsView, EmulatorsView, TasksStartView, DetectionView
)

from AppSimulator.WebAPI import (
    addTaskAPI, removeTaskAPI, getTasksAPI, getTasksCntAPI, getEmulatorsAPI, getHeatmapAPI, getHeatmapFamilyAPI,
    getDevicesStatusAPI,
    startProxyServerAPI,
    getProxyServerInfoAPI,
    runTasksAPI,
    getVMwaresAPI, getHostsAPI, getAllHostsAPI, getLogsAPI, getLogCntAPI, emulatorShakeAPI,
    uploadAPI
)

cache_time_out = 60 * 3

urlpatterns = patterns('',
                       url(r'^dashboard/$', DashBoardView.as_view(), name='dashboard'),
                       url(r'^tasks/$', TasksView.as_view(), name='tasks'),
                       url(r'^emulators/$', EmulatorsView.as_view(), name='emulators'),
                       url(r'^tasksStart/$', TasksStartView.as_view(), name='tasksStart'),
                       url(r'^detection/$', DetectionView.as_view(), name='detection'),
                       url(r'^hosts/$', HostsView.as_view(), name='hosts'),
                       url(r'^vmware/$', VMwareView.as_view(), name='vmware'),
                       url(r'^log/$', LoggerView.as_view(), name='log'),
                       url(r'^addTaskAPI/$', addTaskAPI, name='addTaskAPI'),
                       url(r'^removeTaskAPI/$', removeTaskAPI, name='removeTaskAPI'),
                       url(r'^getTasksAPI/$', getTasksAPI, name='getTasksAPI'),
                       url(r'^getTasksCntAPI/$', getTasksCntAPI, name='getTasksCntAPI'),

                       url(r'^getDevicesStatusAPI/$', getDevicesStatusAPI, name='getDevicesStatusAPI'),
                       url(r'^startProxyServerAPI/$', startProxyServerAPI, name='startProxyServerAPI'),

                       url(r'^runTasksAPI/$', runTasksAPI, name='runTasksAPI'),

                       url(r'^getProxyServerInfoAPI/$', getProxyServerInfoAPI, name='getProxyServerInfoAPI'),
                       # emulator
                       url(r'^emulatorShakeAPI/$', emulatorShakeAPI, name='emulatorShakeAPI'),
                       url(r'^getEmulatorsAPI/$', getEmulatorsAPI, name='getEmulatorsAPI '),
                       url(r'^getHeatmapAPI/$', getHeatmapAPI, name='getHeatmapAPI '),
                       url(r'^getHeatmapFamilyAPI/$', getHeatmapFamilyAPI, name='getHeatmapFamilyAPI '),
                       # vmware
                       url(r'^getVMwaresAPI/$', getVMwaresAPI, name='getVMwaresAPI'),
                       # hosts
                       url(r'^getHostsAPI/$', getHostsAPI, name='getHostsAPI'),
                       # all hosts
                       url(r'^getAllHostsAPI/$', getAllHostsAPI, name='getAllHostsAPI'),
                       # log
                       url(r'^getLogCntAPI/$', getLogCntAPI, name='getLogCntAPI'),
                       url(r'^getLogsAPI/$', getLogsAPI, name='getLogsAPI'),
                       # upload
                       url(r'^uploadAPI/$', uploadAPI, name='uploadAPI'),
                       )
