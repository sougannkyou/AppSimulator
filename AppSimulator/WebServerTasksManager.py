# coding:utf-8
import time
from AppSimulator.RPCLib import can_add_task
from AppSimulator.DBLib import MongoDriver


# ------------------------ web server task manager ----------------------
class Manager(object):
    def __init__(self):
        self._mdb = MongoDriver()
        self._DEBUG = False

    def _log(self, prefix, msg):
        if self._DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
            print(prefix, msg)

    def start_tasks(self):
        while True:
            task = self._mdb.emulator_get_one_wait_task()
            if task:
                servers = self._mdb.get_rpc_servers(task['app_name'])
                for server in servers:
                    ret = can_add_task(server['ip'], server['port'])
                    self._log('<<info>> ' + server['ip'], ret)
                    if ret.lower() == 'yes':
                        self._mdb.emulator_set_task_server_ip(taskId=task['taskId'], ip=server['ip'])
                        break
            else:
                time.sleep(1 * 60)


if __name__ == "__main__":
    manager = Manager()
    manager.start_tasks()
