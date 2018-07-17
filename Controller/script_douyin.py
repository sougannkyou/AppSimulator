# coding:utf-8
import os
import sys

sys.path.append(os.getcwd())

import time
from Controller.Common import *
from Controller.setting import APPSIMULATOR_MODE
from Controller.NoxConDocker import NoxConDocker
from Controller.NoxConSelenium import NoxConSelenium

_DEBUG = False


class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)

    def script(self):
        ret, x, y = self.find_element(comment='APP图标', timeout=10)  # unlock ok
        if ret: ret = self.click_xy(x, y, wait_time=2)

        while ret:  # 更新 -> 分享 -> 复制链接
            ret, x, y = self.find_element(comment='分享', timeout=10)
            if ret:
                self.click_xy(x, y, wait_time=1)
                ret, x, y = self.find_element(comment='复制链接', timeout=10)
                if ret:
                    self.click_xy_timer(x, y, wait_time=1)
            else:
                ret, x, y = self.find_element(comment='跳过软件升级', timeout=10)
                if ret:
                    self.click_xy(x, y, wait_time=1)
                    self.next_page(wait_time=5)

            self.next_page(wait_time=5)


##################################################################################
def main(task_info, mode):
    msg = ''
    error = ''
    start = datetime.now()
    print("[Script " + task_info['docker_name'] + "] start at ", start, '\n', task_info)
    try:
        me = MySelenium(task_info=task_info, mode=mode)
        me.set_comment_to_pic({
            "APP图标": 'images/douyin/app_icon.png',
            "更新": 'images/douyin/update.png',
            "分享": 'images/douyin/share.png',
            "复制链接": 'images/douyin/copylink.png',
            "跳过软件升级": 'images/douyin/ignore_upgrade.png',
        })
        # me._DEBUG = True
        me.run()
    except Exception as e:
        msg = '<<error>>'
        error = e
    finally:
        end = datetime.now()
        common_log(_DEBUG, 'Script ' + task['docker_name'] + 'end.',
                   msg + 'total times:' + str((end - start).seconds) + 's', error)
        if APPSIMULATOR_MODE != 'vmware':
            docker = NoxConDocker(task)
            docker.destroy()
            docker.remove()
        return


if __name__ == "__main__":
    _DEBUG = True

    if APPSIMULATOR_MODE == 'vmware':
        taskId = 1
        mode = 'single'
    else:
        taskId = sys.argv[1]
        mode = 'multi'

    task = {
        'taskId': taskId,
        'app_name': 'douyin',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': 1  # 5s
    }
    main(task_info=task, mode=mode)
    print("Close after 30 seconds.")
    time.sleep(30)
