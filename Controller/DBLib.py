from pprint import pprint
from datetime import datetime, timedelta
from bson.objectid import ObjectId
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
        print("[DBLib]<<info>> get_devices_ip_list:", l)
        return l

    def get_vmware_shareLink_cnt(self, ip, app_name):
        key = 'devices:' + ip + ':' + app_name
        return self._conn.scard(key)


# ------------------------ docker db lib ----------------------
class MongoDriver(object):
    def __init__(self):
        self._client = pymongo.MongoClient(host=MONGODB_SERVER_IP, port=MONGODB_SERVER_PORT)
        self._db = self._client.AppSimulator
        self.activeInfo = self._db.activeInfo
        self.action = self._db.action
        self.deviceConfig = self._db.deviceConfig
        self.hosts = self._db.hosts
        self.tasks = self._db.tasks
        self.logger = self._db.logger
        self.dockers = self._db.dockers
        self.vmwares = self._db.vmwares
        self._DEBUG = False

    # def _log(self, prefix, msg):
    #     common_log(self._DEBUG, '[Controller DB]', prefix, msg)

    # ---------- log -----------------------
    def save_log(self, taskId, func, prefix, msg):
        try:
            self.logger.insert({
                'time': int(datetime.now().timestamp()),
                'ip': LOCAL_IP,
                'taskId': int(taskId) if taskId and isinstance(taskId, str) else taskId,
                'func': func,
                'prefix': prefix,
                'msg': msg.decode('gbk') if isinstance(msg, bytes) else msg
            })
        except Exception as e:
            print('[DBLib]<<error>> save log:\n', e)

    def save_action(self, taskId, action, msg):
        try:
            self.action.update(
                {'taskId': taskId, 'action': action},
                {"$set": {
                    'taskId': int(taskId) if taskId and isinstance(taskId, str) else taskId,
                    'action': action,
                    'msg': msg.decode('gbk') if isinstance(msg, bytes) else msg,
                    'cnt': 0,
                    'time': int(datetime.now().timestamp()),
                }},
                upsert=True)
        except Exception as e:
            print('[DBLib]<<error>> save action:\n', e)

    # ---------- tasks -----------------------
    def task_get_timer_no(self, host_ip):
        timer_no = -1
        used = set()
        tasks = self.tasks.find({'host_ip': host_ip, 'status': STATUS_SCRIPT_START_OK})
        for task in tasks:
            used.add(task['timer_no'])

        t = set(range(len(TIMER))) - set(used)
        if len(t) > 0:
            timer_no = t.pop()

        return timer_no

    def get_taskId(self):
        taskId = 100
        m = self.tasks.aggregate([{"$group": {'_id': '', 'max_id': {"$max": "$taskId"}}}])
        for i in m:
            taskId = int(i['max_id']) + 1  # taskId自增

        return taskId

    def host_register_service(self, controller_info):
        self.hosts.update({'ip': controller_info['ip']}, {"$set": controller_info}, upsert=True)

    def task_reset(self):
        # {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}
        # {'n': 0, 'nModified': 0, 'ok': 1.0, 'updatedExisting': False}
        info = self.tasks.update({'status': STATUS_DOCKER_RUN, 'host_ip': LOCAL_IP},
                                 {"$set": {'status': STATUS_WAIT}})
        return info['nModified']

    def task_get_one_for_run(self):
        cnt = self.tasks.find({'status': STATUS_DOCKER_RUN, 'host_ip': LOCAL_IP}).count()
        if cnt > 0:
            return None, '宿主机当前有' + str(cnt) + '个模拟器正在启动 ...'

        cnt = self.tasks.find({'status': STATUS_DOCKER_RUN, 'host_ip': LOCAL_IP}).count()
        if cnt > len(TIMER):
            return None, '超过 TIMER 个数.'

        task = self.tasks.find_one({  # 优先：复诊
            'status': STATUS_WAIT,
            'host_ip': LOCAL_IP, 'orgTaskId': {'$ne': 0}
        })
        if not task:  # 其次：挂自己号的
            task = self.tasks.find_one({
                'status': STATUS_WAIT,
                'host_ip': LOCAL_IP
            })
            if not task:  # 最后：没人管的
                task = self.tasks.find_one({
                    'status': STATUS_WAIT,
                    'host_ip': ''
                })

        if task:
            self.tasks.update({'_id': task['_id']}, {'$set': {'host_ip': LOCAL_IP}})
            return task, ''

        return None, ''

    def task_get_my_prepare_tasks_cnt(self):
        return self.tasks.find({'status': {'$in': [STATUS_WAIT]}, 'host_ip': LOCAL_IP}).count()

    def task_find_by_taskId(self, taskId):
        return self.tasks.find_one({'taskId': taskId})

    def task_clone(self, task):
        taskId = self.get_taskId()
        self.tasks.insert({
            "taskId": taskId,
            "orgTaskId": task['orgTaskId'] if task['orgTaskId'] != 0 else task['taskId'],  # 初始taskId
            "script": task['script'],
            "redis_key": task['redis_key'],
            "app_name": task['app_name'],
            "status": STATUS_WAIT,
            "live_cycle": task['live_cycle'],
            "schedule": task['schedule'],
            "host_ip": task['host_ip'],
            "start_time": int(datetime.now().timestamp()),
            "up_time": 0,
            "end_time": 0,
            "timer": task['timer'],
            "timer_no": 0,
            "docker_img_name": task['docker_img_name'],
            "description": task['description'],
            "dockerId": ''
        })
        return taskId

    def task_schedule(self):
        '''
        1）超过计划起始时间则马上启动
        2）等待任务空闲，不保证精确按照计划时间启动
        3）修改状态为wait，由任务管理监控来启动
        4）taskId不变，任务管理启动会将上次启动的任务及容器销毁，而后启动本次任务。
        '''
        cnt = 0
        now = int(datetime.now().timestamp())
        cond = {
            'schedule.start': {'$lte': now},
            'schedule.end': {'$gt': now},
            'host_ip': LOCAL_IP,
            'status': {'$ne': STATUS_WAIT}
        }
        tasks = self.tasks.find(cond)
        for task in tasks:
            start = task['schedule']['start']
            if start == 0:  # 未设定任务开始时间视为无效
                continue
            cycle = task['schedule']['cycle']
            run = task['schedule']['run_time']
            now_cycle, _ = divmod(now - start, cycle)
            run_cycle, _ = divmod(run - start, cycle)
            if not now_cycle <= run_cycle < now_cycle + 1:
                print('task_schedule set task-' + str(task['taskId']) + 'status to wait.')
                cnt += 1
                self.tasks.update({'_id': task['_id']}, {'$set': {
                    'schedule.run_time': now,
                    'status': STATUS_WAIT
                }})

        return cnt

    def task_change_status(self, task):
        now = int(datetime.now().timestamp())
        # 脚本运行完毕 docker创建完毕
        if task['status'] == STATUS_SCRIPT_RUN_OK or task['status'] == STATUS_SCRIPT_RUN_NG or \
                task['status'] == STATUS_DOCKER_RUN_OK or task['status'] == STATUS_DOCKER_RUN_NG:
            self.tasks.update({'_id': task['_id']}, {"$set": {
                'status': task['status'],
                'up_time': now,
                'end_time': now
            }})
        elif task['status'] == STATUS_WAIT:  # 重启Task
            self.tasks.update({'_id': task['_id']}, {"$set": {
                'status': task['status'],
                'host_ip': '',
                'start_time': now,
                'up_time': now,
                'end_time': 0
            }})
        else:
            self.tasks.update({'_id': task['_id']}, {"$set": {
                'status': task['status'],
                'up_time': now
            }})

    def task_bind_docker(self, task, docker_id):
        self.tasks.update({'_id': task['_id']}, {"$set": {
            'dockerId': docker_id
        }})

    def task_unbind_docker(self, task):
        self.tasks.update({'_id': task['_id']}, {"$set": {
            'dockerId': None
        }})

    # ---------- dockers -----------------------
    def docker_create(self, docker_obj):
        return self.dockers.insert({  # ObjectId('5b5031baf930a530c47275d2')
            'name': 'nox-{}'.format(docker_obj.get_taskId()),
            'taskId': docker_obj.get_taskId(),
            'app_name': docker_obj.get_app_name(),
            'error_msg': [],
            'host_ip': LOCAL_IP,
            'status': STATUS_DOCKER_RUN,
            'start_time': int(datetime.now().timestamp()),
            'up_time': 0,
            'end_time': 0
        })

    def docker_destroy(self, docker_obj):
        now = int(datetime.now().timestamp())
        ret = self.dockers.update(
            {'name': docker_obj.get_name()},
            {"$set": {
                'status': STATUS_DOCKER_RUN_NG if docker_obj.error_msg else STATUS_DOCKER_RUN_OK,
                'up_time': now,
                'end_time': now
            }})
        return ret['nModified'] == 1

    def docker_add_deadly_msg(self, docker_obj, error_msg):
        now = int(datetime.now().timestamp())
        self.dockers.update(
            {'name': docker_obj.get_name()},
            {"$push": {
                'error_msg': error_msg,
            }})
        ret = self.dockers.update(
            {'name': docker_obj.get_name()},
            {"$set": {
                'status': STATUS_DOCKER_RUN_NG,
                'up_time': now,
                'end_time': now
            }})
        return ret['nModified'] == 1

    # ---------- vmware -----------------------
    def vm_find_vm_by_host(self, host_ip=None):
        ret = []
        if host_ip:
            cond = {'host_ip': host_ip, 'status': {'$ne': 'disable'}}
        else:
            cond = {'status': {'$ne': 'disable'}}

        vmwares = self.vmwares.find(cond)
        for vm in vmwares:
            vm.pop('_id')
            ret.append(vm)
        return ret

    def vm_record_share_cnt(self, vm_info, scope_times):  # 时间窗记录采集量
        # self._log("vm_record_share_cnt\t", vm_info['ip'] + ':\t' + str(vm_info['cnt']))
        old_time = int((datetime.now() - timedelta(seconds=scope_times)).timestamp())
        self.activeInfo.remove({'time': {'$lte': old_time}})
        vm_info['time'] = int(datetime.now().timestamp())
        self.activeInfo.insert(vm_info)

    def vm_get_shareLink_cnt(self, ip):
        ret = []
        vmwares = self.activeInfo.find({'ip': ip}).sort([("time", 1)])
        for vm in vmwares:
            vm.pop('_id')
            ret.append(vm['cnt'])

        return ret

    def get_devices_status(self, app_name):  # 时间窗
        devices_status = []
        ips = RedisDriver().get_devices_ip_list(app_name)
        # self._log('get_devices_status', '')
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
                    status['status'] = STATUS_SCRIPT_SUSPEND
                else:
                    status['status'] = STATUS_SCRIPT_START_OK

            devices_status.append(status)

        # {deviceId: '172.16.251.27', ip: '172.16.251.27', cnt: 0, dedup_cnt: 0, status: DEVICE_STATUS_UNKOWN}
        # {deviceId: '172.16.251.28', ip: '172.16.251.28', cnt: 0, dedup_cnt: 0, status: DEVICE_STATUS_UNKOWN}
        return devices_status  # {'172.16.250.247':'running','172.16.250.252':'unkown'}


# ------------------------ docker db lib ----------------------
if __name__ == '__main__':
    # from .setting import
    host_ip = '172.16.2.113'  # 172.16.2.113
    info = {'device1': 10, 'device2': 20, 'device3': 30, 'device4': 40}
    db = MongoDriver()
    db._DEBUG = True
    # pprint(db.vm_find_vm_by_host(host_ip))
    # pprint(db.task_find_by_taskId(10))
    # db.update_device_statistics_info(info, SCOPE_TIMES)
    # pprint(db.task_get_timer_no(host_ip='172.16.250.199'))
    LOCAL_IP = '172.16.2.113'
    print(LOCAL_IP, db.task_reset())
