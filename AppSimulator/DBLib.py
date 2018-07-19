# coding=utf-8
from pprint import pprint
from datetime import datetime, timedelta, time
import pymongo
import redis
from AppSimulator.setting import *
from AppSimulator.Common import common_log


# ------------------------ web server db lib ----------------------
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

    def get_vmware_shareLink_cnt(self, ip, app_name):
        key = 'devices:' + ip + ':' + app_name
        return self._conn.scard(key)

    def get_vmware_lastTime(self, ip, app_name):
        key = 'devices:' + ip + '_lastTime:' + app_name
        return self._conn.scard(key)


# ------------------------ web server db lib ----------------------
class MongoDriver(object):
    def __init__(self):
        self._client = pymongo.MongoClient(host=MONGODB_SERVER_IP, port=MONGODB_SERVER_PORT)
        self._db = self._client.AppSimulator
        self.deviceStatisticsInfo = self._db.deviceStatisticsInfo
        self.deviceConfig = self._db.deviceConfig
        self.rpcServer = self._db.rpcServer
        self.tasks = self._db.tasks
        self.logger = self._db.logger
        self.vmwares = self._db.vmwares
        self._DEBUG = False

    def get_taskId(self):
        taskId = 1
        m = self.tasks.aggregate([{"$group": {'_id': '', 'max_id': {"$max": "$taskId"}}}])
        for i in m:
            taskId = i['max_id'] + 1  # taskId自增

        return taskId

    def add_task(self, task):
        taskId = self.get_taskId()
        self.tasks.insert({
            "taskId": taskId,
            "orgTaskId": 0,
            "script": task['script'],
            "app_name": task['app_name'],
            "status": STATUS_WAIT,
            "live_cycle": task['live_cycle'],
            "rpc_server_ip": '',
            "start_time": int(datetime.now().timestamp()),
            "up_time": 0,
            "timer_no": 0,
            "dockerId": ''
        })
        return taskId

    def get_tasks(self, status=None):
        ret = []
        if status:
            l = self.tasks.find({'status': status}).sort([('_id', pymongo.DESCENDING)])
        else:
            l = self.tasks.find()

        for r in l:
            r.pop('_id')
            r.pop('dockerId')
            r['start_time'] = datetime.fromtimestamp(r['start_time']).strftime("%Y-%m-%d %H:%M:%S") \
                if r['start_time'] else ''
            r['end_time'] = datetime.fromtimestamp(r['end_time']).strftime("%Y-%m-%d %H:%M:%S") \
                if r['end_time'] else ''
            ret.append(r)

        return ret

    def set_task_server_ip(self, taskId, ip):
        self.tasks.update({'taskId': taskId}, {'$set': {'rpc_server_ip': ip}})

    def get_config_info(self, deviceId):
        info = self.deviceConfig.find_one({'deviceId': deviceId})
        if info:
            info.pop('_id')
        return info

    def get_rpc_servers(self, app_name=None):
        ret = []
        if app_name:
            l = self.rpcServer.find({'app_name': {'$in': [app_name]}})
        else:
            l = self.rpcServer.find()

        for r in l:
            r.pop('_id')
            ret.append(r)
        return ret

    def get_one_wait_task(self):
        task = self.tasks.find_one({'status': STATUS_WAIT, 'rpc_server_ip': ''})
        if task:
            task.pop('_id')

        return task

    def log_find_by_ip(self, ip=None):
        ret = []
        cond = {}
        if ip:
            cond = {'ip': ip}

        log_list = self.logger.find(cond)
        for log in log_list:
            log.pop('_id')
            ret.append(log)
        return ret

    def vm_find_by_host(self, host_ip=None):
        ret = []
        if host_ip:
            cond = {'host_ip': host_ip, 'status': {'$ne': 'disable'}}
        else:
            cond = {'status': {'$ne': 'disable'}}

        vmwares = self.vmwares.find(cond)
        for vm in vmwares:
            vm.pop('_id')
            vm['cnt'] = RedisDriver().get_vmware_shareLink_cnt(vm['ip'], vm['app_name'])
            vm['lastTime'] = RedisDriver().get_vmware_shareLink_cnt(vm['ip'], vm['app_name'])
            ret.append(vm)
        return ret


# ------------------------ server db lib ----------------------
if __name__ == '__main__':
    # from .setting import
    r = RedisDriver()
    pprint(r.get_crwal_cnt_by_device())

    info = {'device1': 10, 'device2': 20, 'device3': 30, 'device4': 40}
    db = MongoDriver()
    # db.update_device_statistics_info(info, SCOPE_TIMES)
    # pprint(db.get_devices_status())
