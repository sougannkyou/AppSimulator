# coding=utf-8
from pprint import pprint
import os, time
from datetime import datetime, timedelta
import pymongo
import redis
import json
from bson.objectid import ObjectId
import requests
from urllib.parse import urlparse, urlunparse

from setting import *


class RedisDriver(object):
    def __init__(self):
        self._conn = redis.StrictRedis.from_url(REDIS_SERVER)

    def get_result_sample(self):
        cnt = self._conn.llen('douyin_data')
        ret = self._conn.blrange('douyin_data', -1, -1)
        return ret

    def get_devices_ip_list(self, app_name):
        l = []
        for key in self._conn.keys():
            name = key.decode('utf-8')
            if name.startswith('devices:' + app_name + ':') and name.endswith('_org'):
                l.append(name.split(':')[2][:-4])
        print("get_devices_ip_list:", l)
        return l

    def get_crwal_cnt_by_device(self, app_name):
        keys = [x.decode('utf8') for x in self._conn.keys()]
        key_acquire_url_cnt = '0'
        key_get_url_cnt = '0'
        key_acquire_url = 'APP:' + app_name + ':count:acquire_url'
        key_get_url = 'APP:' + app_name + ':count:get_url'
        if key_acquire_url in keys:
            key_acquire_url_cnt = self._conn.get(key_acquire_url).decode('ascii')
        if key_acquire_url in keys:
            key_get_url_cnt = self._conn.get(key_get_url).decode('ascii')

        ret = {'cnt': key_acquire_url_cnt,  # douyin, miaopai
               'dedup_cnt': key_get_url_cnt,
               'statusList': []}
        ips = self.get_devices_ip_list(app_name)
        # {deviceId: 'device1', ip: '172.16.251.27', cnt: 0, dedup_cnt: 0, status: DEVICE_STATUS_UNKOWN},
        for ip in ips:
            ret['statusList'].append({
                'deviceId': ip,
                'ip': ip,
                'cnt': int(str(self._conn.scard("devices:" + app_name + ":" + ip + '_org'))),
                'dedup_cnt': 0,
                'status': STATUS_UNKOWN
            })

        return ret

    def get_device_history(self, device_id):
        return self._conn.scard(device_id)


class MongoDriver(object):
    def __init__(self):
        self._client = pymongo.MongoClient(host=MONGODB_SERVER_IP, port=MONGODB_SERVER_PORT)
        self._db = self._client.AppSimulator
        self.deviceStatisticsInfo = self._db.deviceStatisticsInfo
        self.deviceConfig = self._db.deviceConfig
        self.rpcServer = self._db.rpcServer
        self.tasks = self._db.tasks

    def _get_max_task_id(self):
        taskId = 1
        m = self.tasks.aggregate([{"$group": {'_id': '', 'max_id': {"$max": "$taskId"}}}])
        for i in m:
            taskId = i['max_id'] + 1  # taskId自增

        return taskId

    def add_task(self, task):
        taskId = self._get_max_task_id()
        self.tasks.insert({
            "taskId": taskId,
            "script": task['script'],
            "appName": task['appName'],
            "status": STATUS_WAIT,
            "docker": {
                "ip": "",
                "port": "",
                "name": "",
                "start": 0,
                "end": 0
            }})
        return taskId

    def get_tasks(self, status=None):
        ret = []
        if status:
            l = self.tasks.find({'status': status})
        else:
            l = self.tasks.find()

        for r in l:
            r.pop('_id')
            ret.append(r)

        return ret

    def get_config_info(self, deviceId):
        info = self.deviceConfig.find_one({'deviceId': deviceId})
        if info:
            info.pop('_id')
        return info

    def get_rpc_server(self, appName=None):
        ret = []
        if appName:
            l = self.rpcServer.find({'appName': {'$in': [appName]}})
        else:
            l = self.rpcServer.find()

        for r in l:
            r.pop('_id')
            ret.append(r)
        return ret

    def update_device_statistics_info(self, info, scope_times):  # 时间窗式记录采集量
        print("update_device_statistics_info start", info)
        old_time = int((datetime.now() - timedelta(seconds=scope_times)).timestamp())
        self.deviceStatisticsInfo.remove({'time': {'$lt': old_time}})
        now = int(datetime.now().timestamp())
        # ips = RedisDriver().get_devices_ip_list()
        # print("update_device_statistics_info ips:", ips)
        for m in info['statusList']:
            m['time'] = now
            # print("update_device_statistics_info:", m)
            self.deviceStatisticsInfo.insert(m)
            m.pop('_id')

    def get_devices_status(self, app_name):  # 时间窗
        devices_status = []
        ips = RedisDriver().get_devices_ip_list(app_name)
        print("get_devices_status ips")
        for ip in ips:
            status = {'deviceId': ip, 'ip': ip, 'cnt': 0, 'dedup_cnt': 0, 'status': STATUS_UNKOWN}
            l = []
            statistics = self.deviceStatisticsInfo.find({'deviceId': ip})
            for s in statistics:
                s.pop('_id')
                l.append(s['cnt'])

            if (len(l) > 0 and l[-1] > 0):
                status['cnt'] = l[-1]
                if (l[0] == l[-1]):
                    status['status'] = STATUS_SUSPEND
                else:
                    status['status'] = STATUS_RUNNING

            devices_status.append(status)

        # {deviceId: '172.16.251.27', ip: '172.16.251.27', cnt: 0, dedup_cnt: 0, status: DEVICE_STATUS_UNKOWN}
        # {deviceId: '172.16.251.28', ip: '172.16.251.28', cnt: 0, dedup_cnt: 0, status: DEVICE_STATUS_UNKOWN}
        return devices_status  # {'172.16.250.247':'running','172.16.250.252':'unkown'}


if __name__ == '__main__':
    # from .setting import
    r = RedisDriver()
    pprint(r.get_crwal_cnt_by_device())

    info = {'device1': 10, 'device2': 20, 'device3': 30, 'device4': 40}
    db = MongoDriver()
    # db.update_device_statistics_info(info, SCOPE_TIMES)
    # pprint(db.get_devices_status())
