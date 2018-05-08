# coding=utf-8
from pprint import pprint
import os, time, datetime
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

    def get_device_info(self):
        ret = {}
        for device_id in ['device1', 'device2', 'device3', 'device4']:
            ret[device_id] = self._conn.scard(device_id + '_org')
        return ret

    def get_device_history(self, device_id):
        return self._conn.scard(device_id)


class MongoDriver(object):
    def __init__(self):
        self.local_client = pymongo.MongoClient(host=MONGODB_SERVER, port=MONGODB_PORT)
        self.webspider = self.local_client.webspider
        self.entry_setting = self.webspider.entry_setting
        self.detail_xpath = self.webspider.detail_xpath
        self.hub_xpath = self.webspider.hub_xpath
        self.simulator = self.webspider.simulator

    def get_entry_info(self, taskId):
        info = self.entry_setting.find_one({'taskId': taskId})
        if info: info.pop('_id')
        return info


if __name__ == '__main__':
    # r = RedisDriver()
    db = MongoDriver()
    # a = "//div[@class='wrapper mt20 content']/div[@class='fl cola']/div[@class='haoklil']/div[@class='haoklil1']/dl/dd/span[@class='haoklil113']"
    # b = "//div[@class='wrapper mt20 content']/div[@class='fl cola']/div[@class='haoklil']/div[@class='haoklil1']/div[@class='haoklil11']/span/a"
    # print(db.extract(a, b))
    # pprint(db.get_channel_search_cnt(''))
