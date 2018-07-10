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

    def get_vmware_crwal_cnt(self, wm):
        key = 'devices:' + wm['ip'] + ':' + wm['app_name']
        return self._conn.scard(key)


# ------------------------ docker db lib ----------------------
class MongoDriver(object):
    def __init__(self):
        self._client = pymongo.MongoClient(host=MONGODB_SERVER_IP, port=MONGODB_SERVER_PORT)
        self._db = self._client.AppSimulator
        self.activeInfo = self._db.activeInfo
        self.deviceConfig = self._db.deviceConfig
        self.rpcServer = self._db.rpcServer
        self.tasks = self._db.tasks
        self.dockers = self._db.dockers
        self.vmwares = self._db.vmwares
        self._DEBUG = False

    def _log(self, prefix, msg):
        if self._DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
            print('[' + datetime.now().strftime('%H:%M:%S') + ' Controller DB]', prefix, msg)

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

    def vm_find_vm_by_host(self, host_ip):
        ret = []
        vmwares = self.vmwares.find({'host_ip': host_ip, 'status': {'$ne': 'disable'}})
        for vm in vmwares:
            vm.pop('_id')
            ret.append(vm)
        return ret

    def vm_record_share_cnt(self, vm_info, scope_times):  # 时间窗式记录采集量
        self._log("vm_record_share_cnt\t", vm_info['ip'] + ':\t' + str(vm_info['cnt']))
        old_time = int((datetime.now() - timedelta(seconds=scope_times)).timestamp())
        self.activeInfo.remove({'time': {'$lte': old_time}})
        vm_info['time'] = int(datetime.now().timestamp())
        self.activeInfo.insert(vm_info)

    def vm_get_crwal_cnt(self, ip):
        ret = []
        vmwares = self.activeInfo.find({'ip': ip}).sort([("time", 1)])
        for vm in vmwares:
            vm.pop('_id')
            ret.append(vm['cnt'])

        return ret

    def get_devices_status(self, app_name):  # 时间窗
        devices_status = []
        ips = RedisDriver().get_devices_ip_list(app_name)
        self._log('get_devices_status', '')
        for ip in ips:
            status = {'deviceId': ip, 'ip': ip, 'cnt': 0, 'dedup_cnt': 0, 'status': STATUS_UNKOWN}
            l = []
            statistics = self.activeInfo.find({'deviceId': ip})
            for s in statistics:
                s.pop('_id')
                l.append(s['cnt'])

            if len(l) > 0 and l[-1] > 0:
                status['cnt'] = l[-1]
                if l[0] == l[-1]:
                    status['status'] = STATUS_SCRIPT_RUN_SUSPEND
                else:
                    status['status'] = STATUS_SCRIPT_RUNNING

            devices_status.append(status)

        # {deviceId: '172.16.251.27', ip: '172.16.251.27', cnt: 0, dedup_cnt: 0, status: DEVICE_STATUS_UNKOWN}
        # {deviceId: '172.16.251.28', ip: '172.16.251.28', cnt: 0, dedup_cnt: 0, status: DEVICE_STATUS_UNKOWN}
        return devices_status  # {'172.16.250.247':'running','172.16.250.252':'unkown'}


# ------------------------ docker db lib ----------------------
if __name__ == '__main__':
    # from .setting import
    host_ip = '172.16.253.37'
    info = {'device1': 10, 'device2': 20, 'device3': 30, 'device4': 40}
    db = MongoDriver()
    db._DEBUG = True
    pprint(db.vm_find_vm_by_host(host_ip))
    # db.update_device_statistics_info(info, SCOPE_TIMES)
    # pprint(db.get_devices_status())
