# coding=utf-8
from pprint import pprint
import os, time
from datetime import datetime, timedelta
import pymongo

from AppSimulator.setting import *


# ------------------------ docker db lib ----------------------
class MongoDriver(object):
    def __init__(self):
        self._client = pymongo.MongoClient(host=MONGODB_SERVER_IP, port=MONGODB_SERVER_PORT)
        self._db = self._client.AppSimulator
        self.deviceStatisticsInfo = self._db.deviceStatisticsInfo
        self.deviceConfig = self._db.deviceConfig
        self.rpcServer = self._db.rpcServer
        self.tasks = self._db.tasks

    def registor_rpc_server(self, controllor_info):
        self.rpcServer.update({'ip': controllor_info['ip']}, {"$set": controllor_info}, upsert=True)

    def get_one_wait_task(self):
        while True:
            l = self.tasks.find({'status': STATUS_RUNNING})
            if not l:
                task = self.tasks.find_one({'status': STATUS_WAIT, 'docker.ip': ''})
                task.pop('_id')
                return task
            else:
                time.sleep(1 * 60)


# ------------------------ docker db lib ----------------------
if __name__ == '__main__':
    # from .setting import
    info = {'device1': 10, 'device2': 20, 'device3': 30, 'device4': 40}
    db = MongoDriver()
    # db.update_device_statistics_info(info, SCOPE_TIMES)
    # pprint(db.get_devices_status())
