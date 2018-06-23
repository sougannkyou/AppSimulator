# coding:utf-8
import time
from AppSimulator.RPCLib import rpc_get_free_mem
from AppSimulator.DBLib import MongoDriver


# ------------------------ web server task manager ----------------------
class TaskManager(object):
    def __init__(self):
        self._db = MongoDriver()

    def start_tasks(self):
        while True:
            task = self._db.get_one_wait_task()
            if task:
                servers = self._db.get_rpc_servers(task['app_name'])
                for server in servers:
                    ret = rpc_get_free_mem(server['ip'], server['port'])
                    if ret > 1.0:  # free memory > 1GB
                        self._db.set_task_server_ip(taskId=task['taskId'], ip=server['ip'])
                        break
            else:
                time.sleep(1 * 60)
