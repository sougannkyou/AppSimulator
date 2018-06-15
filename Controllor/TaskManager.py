# coding:utf-8
from datetime import datetime, timedelta
import pymongo

# MONGODB_SERVER = os.environ["MONGODB_SERVER_IP"]  # "172.16.252.174"
MONGODB_SERVER = "172.16.252.174"
# MONGODB_PORT = int(os.environ["MONGODB_SERVER_PORT"])
MONGODB_PORT = 27017


class TaskManager(object):
    def __init__(self):
        self._client = pymongo.MongoClient(host=MONGODB_SERVER, port=MONGODB_PORT)
        self._db = self._client.AppSimulator
        self.dockerConfig = self._db.dockerConfig
        self.tasksTrace = self._db.tasksTrace
        self.controllor = self._db.controllor

    def task_trace(self, task_id, app_name, docker_name, action):  # after docker start success
        self.tasksTrace.insert({
            'task_id': task_id,
            'app_name': app_name,
            'docker_name': docker_name,
            'time': int(datetime.now().timestamp()),
            'action': action,  # sharelink, start, stop, publish
        })

    def set_docker_info(self, docker_name, ip, port, task_id, app_name):
        self.dockerConfig.insert({
            'docker_name': docker_name,
            'ip': ip,
            'port': port,
            'task_id': task_id,
            'app_name': app_name,
        })

    def registor_rpc_server(self, controllor_info):
        self.controllor.update({'ip': controllor_info['ip']}, {"$set": controllor_info}, upsert=True)

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
