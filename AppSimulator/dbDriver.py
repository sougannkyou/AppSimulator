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

    def get_result_sample(self):
        cnt = self._conn.llen('douyin_data')
        ret = self._conn.blrange('douyin_data', -1, -1)
        return ret

    def get_devices_ip_list(self):
        l = []
        for key in self._conn.keys():
            name = key.decode('utf-8')
            if name.startswith('devices:') and name.endswith('_org'):
                l.append(name[len('devices:'):-4])
        print("get_devices_ip_list:", l)
        return l

    def get_crwal_cnt_by_device(self):
        ret = {'cnt': self._conn.get('APP:iesdouyin:count:acquire_url').decode('ascii'),
               'dedup_cnt': self._conn.get('APP:iesdouyin:count:get_url').decode('ascii'),
               'statusList': []}
        ips = self.get_devices_ip_list()
        # {deviceId: 'device1', ip: '172.16.251.27', cnt: 0, dedup_cnt: 0, status: DEVICE_STATUS_UNKOWN},
        for ip in ips:
            ret['statusList'].append({
                'deviceId': ip,
                'ip': ip,
                'cnt': int(str(self._conn.scard("devices:" + ip + '_org'))),
                'dedup_cnt': 0,
                'status': DEVICE_STATUS_UNKOWN
            })

        return ret

    def get_device_history(self, device_id):
        return self._conn.scard(device_id)


class MongoDriver(object):
    def __init__(self):
        self._client = pymongo.MongoClient(host=MONGODB_SERVER, port=MONGODB_PORT)
        self._db = self._client.AppSimulator
        self.deviceStatisticsInfo = self._db.deviceStatisticsInfo
        self.deviceConfig = self._db.deviceConfig

    def get_config_info(self, deviceId):
        info = self.deviceConfig.find_one({'deviceId': deviceId})
        if info:
            info.pop('_id')
        return info

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

    def get_devices_status(self):  # 时间窗
        devices_status = []
        ips = RedisDriver().get_devices_ip_list()
        print("get_devices_status ips", ips)
        for ip in ips:
            status = {'deviceId': ip, 'ip': ip, 'cnt': 0, 'dedup_cnt': 0, 'status': DEVICE_STATUS_UNKOWN}
            l = []
            statistics = self.deviceStatisticsInfo.find({'deviceId': ip})
            for s in statistics:
                s.pop('_id')
                l.append(s['cnt'])

            if (len(l) > 0 and l[-1] > 0):
                status['cnt'] = l[-1]
                if (l[0] == l[-1]):
                    status['status'] = DEVICE_STATUS_SUSPEND
                else:
                    status['status'] = DEVICE_STATUS_RUNNING

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
