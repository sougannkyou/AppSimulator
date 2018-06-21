# coding:utf-8
import time
from Controllor.setting import *
from Controllor.DBLib import MongoDriver
from Controllor.NoxDocker import NoxDocker


# ------------------------ docker task manager ----------------------
class TaskManager(object):
    def __init__(self):
        self.driver = MongoDriver()

    def start_tasks(self, app_name):
        while True:
            task = self.driver.get_one_wait_task()  # STATUS_WAIT
            if task:
                task['status'] = STATUS_BUILDING
                self.driver.change_task_status(task)

                docker = NoxDocker(task['app_name'], 'nox-' + task['taskId'])
                ret = docker.build(force=True, retry_cnt=2, wait_time=30)
                task['status'] = STATUS_BUILD_OK if ret else STATUS_BUILD_NG
                self.driver.change_task_status(task)

                break
            else:
                time.sleep(1 * 60)

        return True
