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

# from .setting import MONGODB_SERVER, MONGODB_PORT

# LOCAL_DEBUG = False
#
# if LOCAL_DEBUG:  # os.name == 'nt':
#     MONGODB_SERVER = '127.0.0.1:37017'
#     MONGODB_PORT = 27017
#     REDIS_SERVER = 'redis://127.0.0.1:6379/2'
# else:
#     MONGODB_SERVER = '192.168.16.223:37017'
#     MONGODB_PORT = 37017
#     REDIS_SERVER = 'redis://192.168.16.223:6379/2'

REDIS_SERVER = 'redis://127.0.0.1/11'
REDIS_SERVER_RESULT = 'redis://127.0.0.1/10'
MONGODB_SERVER = '127.0.0.1'
MONGODB_PORT = 27017
DEVICE_LIST = ['device1', 'device2', 'device3', 'device4']


class RedisDriver(object):
    def __init__(self):
        self._conn = redis.StrictRedis.from_url(REDIS_SERVER)
        self._conn_result = redis.StrictRedis.from_url(REDIS_SERVER_RESULT)
        self.device1 = 'device1'
        self.device2 = 'device2'
        self.device3 = 'device3'
        self.device4 = 'device4'

    def get_result_sample(self):
        cnt = self._conn_result.llen('douyin_data')
        ret = self._conn_result.blrange('douyin_data', -1, -1)
        return ret

    def get_crwal_cnt_by_device(self):
        ret = {}
        for device_id in DEVICE_LIST:
            ret[device_id] = self._conn.scard(device_id + '_org')
        return ret

    def get_device_history(self, device_id):
        return self._conn.scard(device_id)


class MongoDriver(object):
    def __init__(self):
        self._client = pymongo.MongoClient(host=MONGODB_SERVER, port=MONGODB_PORT)
        self._db = self._client.AppSimulator
        self.deviceStatisticsInfo = self._db.deviceStatisticsInfo

    def get_device_list(self):
        return DEVICE_LIST

    def get_entry_info(self, taskId):
        info = self.deviceStatisticsInfo.find_one({'deviceId': taskId})
        if info: info.pop('_id')
        return info

    def set_device_statistics_info(self, info):
        now = int(datetime.now().timestamp())
        for device_id in DEVICE_LIST:
            self.deviceStatisticsInfo.insert({'deviceId': device_id, 'time': now, 'cnt': info[device_id]})

    def get_deactive_device_list(self):
        nonactive = []
        old_time = int((datetime.now() - timedelta(minutes=1)).timestamp())
        print(old_time)
        for device_id in DEVICE_LIST:
            l = []
            statistics = self.deviceStatisticsInfo.find({
                'deviceId': device_id,
                'time': {'$gt': old_time}
            })
            for s in statistics:
                s.pop('_id')
                l.append(s)

            if (len(l) > 0 and l[0]['cnt'] == l[-1]['cnt']):
                nonactive.append(device_id)

        return nonactive


if __name__ == '__main__':
    # r = RedisDriver()
    info = {'device1': 10, 'device2': 20, 'device3': 30, 'device4': 40}
    db = MongoDriver()
    db.set_device_statistics_info(info)
    db.get_deactive_device_list()
