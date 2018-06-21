# coding=utf-8
from pprint import pprint
import time
from datetime import datetime, timedelta
import pymongo
from Controllor.setting import *


# ------------------------ docker db lib ----------------------
class MongoDriver(object):
    def __init__(self):
        self._client = pymongo.MongoClient(host=MONGODB_SERVER_IP, port=MONGODB_SERVER_PORT)
        self._db = self._client.AppSimulator
        self.deviceStatisticsInfo = self._db.deviceStatisticsInfo
        self.deviceConfig = self._db.deviceConfig
        self.rpcServer = self._db.rpcServer
        self.tasks = self._db.tasks
        self.tasksTrace = self._db.tasksTrace

    # def task_trace(self, task_id, app_name, docker_name, action):  # after docker start success
    #     self.tasksTrace.insert({
    #         'task_id': task_id,
    #         'app_name': app_name,
    #         'docker_name': docker_name,
    #         'time': int(datetime.now().timestamp()),
    #         'action': action,  # sharelink, start, stop, publish
    #     })
    #
    # def set_docker_info(self, docker_name, ip, port, task_id, app_name):
    #     self.dockerConfig.insert({
    #         'docker_name': docker_name,
    #         'ip': ip,
    #         'port': port,
    #         'task_id': task_id,
    #         'app_name': app_name,
    #     })

    def registor_rpc_server(self, controllor_info):
        self.rpcServer.update({'ip': controllor_info['ip']}, {"$set": controllor_info}, upsert=True)

    def get_one_wait_task(self):
        return self.tasks.find_one({'status': STATUS_WAIT, 'rpc_server_ip': LOCAL_IP})

    def change_task_status(self, task):
        self.tasks.update({'_id': task['_id']}, {"$set": {'status': task['status']}})

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


# ------------------------ docker db lib ----------------------
if __name__ == '__main__':
    # from .setting import
    info = {'device1': 10, 'device2': 20, 'device3': 30, 'device4': 40}
    db = MongoDriver()
    # db.update_device_statistics_info(info, SCOPE_TIMES)
    # pprint(db.get_devices_status())
