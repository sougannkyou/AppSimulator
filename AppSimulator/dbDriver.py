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

from .setting import *


class RedisDriver(object):
    def __init__(self):
        self._conn = redis.StrictRedis.from_url(REDIS_SERVER)
        self._conn_result = redis.StrictRedis.from_url(REDIS_SERVER_RESULT)

    def get_result_sample(self):
        cnt = self._conn_result.llen('douyin_data')
        ret = self._conn_result.blrange('douyin_data', -1, -1)
        return ret

    def get_crwal_cnt_by_device(self):
        ret = {'devices': {'dedup_cnt': self._conn_result.zcard('dedup_douyin_id')}}
        devices = MongoDriver().get_device_list()
        for device in devices:
            ret[device['deviceId']] = {'cnt': self._conn.scard(device['deviceId'] + '_org')}

        return ret

    def get_device_history(self, device_id):
        return self._conn.scard(device_id)


class MongoDriver(object):
    def __init__(self):
        self._client = pymongo.MongoClient(host=MONGODB_SERVER, port=MONGODB_PORT)
        self._db = self._client.AppSimulator
        self.deviceStatisticsInfo = self._db.deviceStatisticsInfo
        self.deviceConfig = self._db.deviceConfig

    def get_device_list(self):
        devices_list = []
        l = self.deviceConfig.find()
        for r in l:
            devices_list.append({'deviceId': r['deviceId'], 'ip': r['ip']})

        return devices_list

    def get_config_info(self, deviceId):
        info = self.deviceConfig.find_one({'deviceId': deviceId})
        if info: info.pop('_id')
        return info

    def update_device_statistics_info(self, info, scope_times):  # 时间窗式记录采集量
        old_time = int((datetime.now() - timedelta(seconds=scope_times)).timestamp())
        self.deviceStatisticsInfo.remove({'time': {'$lt': old_time}})
        now = int(datetime.now().timestamp())
        for device in self.get_device_list():
            self.deviceStatisticsInfo.insert({
                'deviceId': device['deviceId'], 'time': now, 'cnt': info[device['deviceId']]['cnt']
            })

    def get_devices_status(self):  # 时间窗
        devices_status = {}
        for device in self.get_device_list():
            l = []
            devices_status[device['deviceId']] = DEVICE_STATUS_UNKOWN
            statistics = self.deviceStatisticsInfo.find({'deviceId': device['deviceId']})
            for s in statistics:
                s.pop('_id')
                l.append(s['cnt'])

            if (len(l) > 0 and l[-1] > 0):
                if (l[0] == l[-1]):
                    devices_status[device['deviceId']] = DEVICE_STATUS_SUSPEND
                else:
                    devices_status[device['deviceId']] = DEVICE_STATUS_RUNNING

        return devices_status  # {'device1':'running','device2':'unkown'}


if __name__ == '__main__':
    # r = RedisDriver()
    info = {'device1': 10, 'device2': 20, 'device3': 30, 'device4': 40}
    db = MongoDriver()
    db.update_device_statistics_info(info, SCOPE_TIMES)
    pprint(db.get_devices_status())
