# coding=utf-8
from pprint import pprint
from datetime import datetime, timedelta
import pymongo
import redis
from Controller.setting import *


# ------------------------ docker db lib ----------------------
class RedisDriver(object):
    def __init__(self):
        self._conn = redis.StrictRedis.from_url(REDIS_SERVER)

    def set_current_task(self):
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


# ------------------------ docker db lib ----------------------
class MongoDriver(object):
    def __init__(self):
        self._client = pymongo.MongoClient(host=MONGODB_SERVER_IP, port=MONGODB_SERVER_PORT)
        self._db = self._client.AppSimulator
        self.deviceStatisticsInfo = self._db.deviceStatisticsInfo
        self.deviceConfig = self._db.deviceConfig
        self.rpcServer = self._db.rpcServer
        self.tasks = self._db.tasks
        self.dockers = self._db.dockers
        self._DEBUG = False

    def _log(self, prefix, msg):
        if self._DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
            print('[Controller DB]', prefix, msg)

    def rpc_register_service(self, controller_info):
        self.rpcServer.update({'ip': controller_info['ip']}, {"$set": controller_info}, upsert=True)

    def task_get_one_for_run(self):
        cnt = self.tasks.find({'status': STATUS_DOCKER_RUN, 'rpc_server_ip': LOCAL_IP}).count()
        if cnt > 0:
            return None, '有' + str(cnt) + '个docker正在启动 ...'

        cnt = self.tasks.find({'status': STATUS_DOCKER_RUN, 'rpc_server_ip': LOCAL_IP}).count()
        if cnt > len(TIMER):
            return None, ''

        task = self.tasks.find_one({'status': STATUS_WAIT, 'rpc_server_ip': LOCAL_IP})
        return task, 'ok'

    def task_get_my_prepare_tasks_cnt(self):
        return self.tasks.find(
            {'status': {'$in': [STATUS_WAIT]}, 'rpc_server_ip': LOCAL_IP}).count()

    def task_change_status(self, task):
        self._log('task_change_status', task['status'])
        self.tasks.update({'_id': task['_id']}, {"$set": {'status': task['status']}})

    def task_set_docker(self, task, docker):
        self._log('task_set_docker', task)
        self.tasks.update({'_id': task['_id']}, {"$set": {'dockerId': docker['_id']}})

    def docker_create(self, task):
        id = self.dockers.insert({
            'docker_name': 'nox-' + str(task['taskId']),
            'ip': LOCAL_IP,
            'port': 0,
            'status': STATUS_DOCKER_RUN,
            'start_time': int(datetime.now().timestamp()),
            'end_time': 0
        })
        return id

    def docker_change_status(self, docker):
        self._log('docker_change_status', docker['status'])
        self.dockers.update({'_id': docker['_id']}, {"$set": {'status': docker['status']}})

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
