# coding=utf-8
import re
from pprint import pprint
from datetime import datetime, timedelta, time
import pymongo
from pymongo import ReturnDocument
import redis
from AppSimulator.setting import *
from AppSimulator.Common import *


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
        self.taskId = self._db.taskId
        self.logger = self._db.logger
        self.hosts = self._db.hosts
        self.vmwares = self._db.vmwares
        self.dockers = self._db.dockers
        self.activeInfo = self._db.activeInfo
        self._DEBUG = False

    # -------------  logger -----------------------------------------------------------------
    def log_find_by_ip(self, ip=None, log_filter=None):
        # log_filter = {'module': {'adb': True, 'docker': False, 'manager': True, 'selenium': True}}
        ret = []
        cond = {}
        if ip:
            cond['ip'] = ip

        if log_filter:
            func_list = []
            if not log_filter['module']['manager']:
                func_list.append({'func': {'$not': re.compile('Manager')}})
            if not log_filter['module']['selenium']:
                func_list.append({'func': {'$not': re.compile('NoxConSelenium')}})
            if not log_filter['module']['docker']:
                func_list.append({'func': {'$not': re.compile('NoxDocker')}})
            if not log_filter['module']['adb']:
                func_list.append({'func': {'$not': re.compile('adb')}})

            if func_list:
                cond['$and'] = func_list

        print('<<<<<<log_find_by_ip>>>>>>')
        # db.logger.find({$and: [{'func':{'$not': /NoxConSelenium/}},{'func':{'$not': /NoxDocker/}}]})
        pprint(cond)
        log_list = self.logger.find(cond).sort('time', pymongo.ASCENDING).skip(0).limit(200)
        for log in log_list:
            log.pop('_id')
            log['time'] = timestamp2string(log['time'], "%m-%d %H:%M:%S") if log['time'] else ''
            log['msg'] = log['msg'].decode('gbk') if isinstance(log['msg'], bytes) else log['msg']
            ret.append(log)
        return ret

    def log_cnt(self, ip=None):
        cond = {}
        if ip:
            cond = {'ip': ip}

        return self.logger.find(cond).count()

    # -------------  tasks -----------------------------------------------------------------
    def tasks_find_by_host(self, host_ip=None):
        ret = []
        if host_ip:
            cond = {'host_ip': host_ip, 'status': {'$ne': 'disable'}}
        else:
            cond = {'status': {'$ne': 'disable'}}

        tasks = self.tasks.find(cond)
        for task in tasks:
            task.pop('_id')
            task.pop('dockerId')
            pre = 'http://' + task['host_ip'] + ':8000/static/AppSimulator/images/'
            task['app_icon'] = pre + 'app/' + task['app_name'] + '/app_icon.png'
            task['timer_no'] = TIMER[task['timer_no'] if task else 0]
            task['spend_times'] = seconds_format(seconds=(task['up_time'] - task['start_time'])) \
                if task['up_time'] > 0 else '00:00:00'
            task['capture'] = pre + 'temp/emulators/capture_nox-' + str(task['taskId']) + '.png'
            ret.append(task)
        return ret

    def tasks_find_by_taskId(self, taskId):
        return self.tasks.find_one({'taskId': taskId})

    # -------------  emulators ---------------------------------
    def emulator_get_hosts(self):
        hosts = []
        l = self.hosts.find({'host_type': 'emulator'})
        for h in l:
            h.pop('_id')
            h['tasks'] = self.tasks_find_by_host(h['ip'])
            hosts.append(h)
        return hosts

    def emulator_add_host(self, host):
        h = self.hosts.find_one({'ip': 'ip'})
        if h:
            return None
        else:
            return self.hosts.insert(host)

    def emulator_get_task(self, taskId):
        if taskId:
            return self.tasks.find_one({'taskId': taskId})
        else:
            return None

    def string2timestamp(self, s, format_str="%Y-%m-%d %H:%M:%S"):
        return int(time.mktime(datetime.strptime(s, format_str).timetuple()))

    def emulator_get_start_by_day(self, index, taskId, day):
        ret = []
        children = [taskId]
        for t in self.tasks.find({"orgTaskId": taskId}):
            children.append(t['taskId'])

        for h in range(24):
            t = self.string2timestamp('{} {}:00:00'.format(day, h))
            cnt = self.dockers.find({"taskId": {"$in": children}, 'start_time': {'$gt': t, '$lt': t + 3600}}).count()
            ret.append([index, h, cnt])

        return ret

    def emulator_find_by_host(self, host_ip=None):
        ret = []
        if host_ip:
            cond = {'host_ip': host_ip, 'status': {'$ne': 'disable'}}
        else:
            cond = {'status': {'$ne': 'disable'}}

        dockers = self.dockers.find(cond)
        for d in dockers:
            d.pop('_id')
            pre = 'http://' + d['host_ip'] + ':8000/static/AppSimulator/images/'
            d['app_icon'] = pre + 'app/' + d['app_name'] + '/app_icon.png'
            taskId = d['taskId'] if 'taskId' in d else None
            task = self.emulator_get_task(taskId)
            d['timer'] = TIMER[task['timer_no'] if task else 0]
            d['capture'] = pre + 'temp/emulators/capture_' + d['name'] + '.png'
            # emu['capture_before'] = pre + 'temp/emulators/capture_' + emu['name'] + '_before.png'
            ret.append(d)
        return ret

    def emulator_get_taskId(self):
        counter = self.taskId.find_one_and_update(
            {'_id': 'counter'},
            {'$inc': {'count': 1}},
            return_document=ReturnDocument.AFTER  # 返回修改后的内容
        )
        return counter['count']

    def emulator_add_task(self, task):
        taskId = self.emulator_get_taskId()
        self.tasks.insert({
            "taskId": taskId,
            "orgTaskId": 0,
            "script": task['script'],
            "app_name": task['app_name'],
            "status": STATUS_WAIT,
            "live_cycle": task['live_cycle'],
            "schedule": task['schedule'],
            "docker_img_name": task['docker_img_name'],
            "description": task['description'],
            "timer": task['timer'],
            "timer_no": -1 if task['timer'] == 'off' else 0,
            "host_ip": task['ip'],
            "start_time": int(datetime.now().timestamp()),
            "up_time": 0,
            "end_time": 0,
            "dockerId": ''
        })
        return taskId

    def emulator_remove_task(self, taskId):
        self.tasks.remove({
            "taskId": taskId
        })
        return True

    def emulator_get_one_wait_task(self):
        task = self.tasks.find_one({'status': STATUS_WAIT, 'host_ip': ''})
        if task:
            task.pop('_id')

        return task

    def emulator_get_tasks(self, status=None):
        ret = []
        if status:
            l = self.tasks.find({'status': status}).sort([('_id', pymongo.DESCENDING)])
        else:
            l = self.tasks.find()

        for r in l:
            r.pop('_id')
            if 'dockerId' in r:
                r.pop('dockerId')

            r['spend_time'] = seconds_format(seconds=(r['up_time'] - r['start_time']))
            r['start_time'] = timestamp2string(r['start_time'], "%m-%d %H:%M:%S")
            r['end_time'] = timestamp2string(r['end_time'], "%m-%d %H:%M:%S")
            r['schedule']['start'] = timestamp2string(r['schedule']['start'], "%m-%d %H:%M:%S")
            r['schedule']['end'] = timestamp2string(r['schedule']['end'], "%m-%d %H:%M:%S")
            r['schedule']['run_time'] = timestamp2string(r['schedule']['run_time'], "%m-%d %H:%M:%S")
            r['schedule']['cycle'] = int(r['schedule']['cycle'] / 60)
            ret.append(r)

        return ret

    def emulator_get_tasks_cnt(self, host_ip=None):
        cond = {}
        if host_ip:
            cond = {'host_ip': host_ip}

        return self.tasks.find(cond).count()

    def emulator_get_emulators(self, host_ip=None):
        ret = []
        cond = {}
        # cond = {'status': STATUS_WAIT, 'host_ip': host_ip}
        dockers = self.dockers.find(cond)
        for docker in dockers:
            docker.pop('_id')
            docker['spend_times'] = seconds_format(seconds=(docker['end_time'] - docker['start_time'])) \
                if docker['end_time'] > 0 else 'N/A'
            docker['start_time'] = timestamp2string(docker['start_time'], "%m-%d %H:%M:%S")
            docker['end_time'] = timestamp2string(docker['end_time'], "%m-%d %H:%M:%S")
            docker['up_time'] = timestamp2string(docker['up_time'], "%m-%d %H:%M:%S")
            docker['error_msg'] = ';'.join(docker['error_msg']) if docker['error_msg'] else '-'

            ret.append(docker)
        return ret

    def emulator_set_task_server_ip(self, taskId, ip):
        self.tasks.update({'taskId': taskId}, {'$set': {'host_ip': ip}})

    def emulator_get_config_info(self, deviceId):
        info = self.deviceConfig.find_one({'deviceId': deviceId})
        if info:
            info.pop('_id')
        return info

    # ----------------- all -------------------------------------------------------------
    def all_get_hosts(self):
        ret = []
        for h in self.hosts.find():
            h.pop('_id')
            h['timer_max_cnt'] = '-' if h['host_type'] == 'vmware' else h['timer_max_cnt']
            ret.append(h)
        return ret

    # ----------------- vmwares -------------------------------------------------------------
    def vm_get_hosts(self):
        hosts = []
        l = self.hosts.find({'host_type': 'vmware'})
        for h in l:
            h.pop('_id')
            h['vmwares'] = self.vm_find_by_host(host_ip=h['ip'])
            hosts.append(h)
        return hosts

    def vm_find_by_host(self, host_ip=None):
        ret = []
        if host_ip:
            cond = {'host_ip': host_ip, 'status': {'$ne': 'disable'}}
        else:
            cond = {'status': {'$ne': 'disable'}}

        vmwares = self.vmwares.find(cond)
        for vm in vmwares:
            vm.pop('_id')
            pre = 'http://' + vm['host_ip'] + ':8000/static/AppSimulator/images/temp/vmwares/'
            vm['capture'] = pre + 'capture_' + vm['name'] + '.png'
            vm['capture_before'] = pre + '/capture_' + vm['name'] + '_before.png'
            # vm['cnt'] = RedisDriver().get_vmware_shareLink_cnt(vm['ip'], vm['app_name'])
            # vm['lastTime'] = RedisDriver().get_vmware_shareLink_cnt(vm['ip'], vm['app_name'])
            # vm[]
            ret.append(vm)
        return ret

    def vm_get_cardiogram_by_host(self, host_ip=None):
        ret = []
        if host_ip:
            cond = {'host_ip': host_ip, 'status': {'$ne': 'disable'}}
        else:
            cond = {'status': {'$ne': 'disable'}}

        vmwares = self.vmwares.find(cond)
        for vm in vmwares:
            vm.pop('_id')
            vm['lastTime'] = RedisDriver().get_vmware_shareLink_cnt(vm['ip'], vm['app_name'])
            ret.append(vm)
        return ret

    def vm_actioveInfo_by_host(self, host_ip=None):
        ret = {
            'interval': [],
            'cntList': []
        }
        if host_ip:
            cond = {'host_ip': host_ip, 'status': {'$ne': 'disable'}}
        else:
            cond = {'status': {'$ne': 'disable'}}

        info_list = self.activeInfo.find(cond)
        for info in info_list:
            t = timestamp2string(info['time'], "%Y-%m-%d %H:%M:%S") if info['time'] else ''
            ret['interval'].append(t)
            ret['cntList'].append(info['cnt'])
        return ret


# ------------------------ server db lib ----------------------
if __name__ == '__main__':
    # from .setting import
    # r = RedisDriver()
    # pprint(r.get_crwal_cnt_by_device())

    info = {'device1': 10, 'device2': 20, 'device3': 30, 'device4': 40}
    db = MongoDriver()
    # db.update_device_statistics_info(info, SCOPE_TIMES)
    pprint(db.emulator_get_start_by_day(22, '2018-09-03'))
