# coding:utf-8
import os
import sys

sys.path.append(os.getcwd())

import time
from Controller.setting import APPSIMULATOR_MODE
from Controller.Common import *
from Controller.NoxConDocker import NoxConDocker
from Controller.NoxConSelenium import NoxConSelenium
from Controller.ControllerManager import Manager

_DEBUG = False


class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)

    def script(self):
        try:
            ret, x, y = self.find_element(comment='APP图标', timeout=10)  # unlock ok
            if ret: self.click_xy(x, y, wait_time=20)
            ret, x, y = self.find_element(comment='忽略升级', timeout=10)
            if ret:
                self.click_xy(x, y, wait_time=2)

            ret = self.click_xy(200, 200, wait_time=10)  # 选择一个视频

            while ret:
                ret, x, y = self.find_element(comment='分享', timeout=10)
                if ret:
                    self.click_xy(x, y, wait_time=2)  # click 分享
                    if ret:
                        ret, x, y = self.find_element(comment='复制链接', timeout=10)
                        if ret:
                            self.click_xy(x, y, wait_time=1)
                        else:  # retry once
                            ret, x, y = self.find_element(comment='分享', timeout=10)
                            if ret:
                                self.click_xy(x, y, wait_time=2)  # click 分享
                                if ret:
                                    ret, x, y = self.find_element(comment='复制链接', timeout=10)
                                    if ret:
                                        self.click_xy(x, y, wait_time=1)
                else:
                    ret = self.find_element(comment='广告', timeout=10)
                    if ret:
                        ret = self.next_page_700(wait_time=5)

                self.next_page_700(wait_time=5)

        except Exception as e:
            self._log('error:', e)


##################################################################################
def main(task, mode):
    msg = ''
    error = ''
    start = datetime.now()
    common_log(_DEBUG, task['taskId'], 'Script ' + task['docker_name'], 'start', task)

    try:
        me = MySelenium(task_info=task, mode=mode)
        me.set_comment_to_pic({
            "选择一个视频": 'images/huoshan/clickone.png',
            "APP图标": 'images/huoshan/app_icon.png',
            "忽略升级": 'images/huoshan/ignore_upgrade.png',
            "广告": 'images/huoshan/ad.png',
            "分享": 'images/huoshan/share.png',
            "复制链接": 'images/huoshan/copylink.png',
        })
        # me._DEBUG = True
        me.run()
    except Exception as e:
        msg = '<<error>>'
        error = e
    finally:
        end = datetime.now()
        if APPSIMULATOR_MODE != 'vmware':  # multi nox console
            common_log(_DEBUG, task['taskId'], 'Script ' + task['docker_name'], 'multi nox console mode.', '')
            docker = NoxConDocker(task)
            docker.destroy()
            docker.remove()
            m = Manager()
            m.nox_run_task_complete(task['taskId'])
            time.sleep(10)

        common_log(_DEBUG, task['taskId'], 'Script ' + task['docker_name'] + 'end.',
                   msg + 'total times:' + str((end - start).seconds) + 's', error)
        return


if __name__ == "__main__":
    _DEBUG = True

    if APPSIMULATOR_MODE == 'vmware':
        taskId = 3
        mode = 'single'
    else:
        taskId = sys.argv[1]
        mode = 'multi'

    task = {
        'taskId': taskId,
        'app_name': 'huoshan',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': 2  # 5s
    }
    main(task=task, mode=mode)
    print("Close after 30 seconds.")
    time.sleep(30)
