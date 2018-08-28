# coding:utf-8
import os
import sys
import time

sys.path.append(os.getcwd())

from Controller.Common import *
from Controller.setting import APPSIMULATOR_MODE
from Controller.NoxConSelenium import NoxConSelenium
from Controller.ControllerManager import Manager



#################################################################################
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
        if APPSIMULATOR_MODE == 'multi':  # multi nox mode
            m = Manager()
            m.nox_run_task_finally(taskId)

        common_log(True, task['taskId'], 'Script ' + task['docker_name'] + 'end.',
                   msg + 'total times:' + str((datetime.now() - start).seconds) + 's', error)
        return


#################################################################################
if __name__ == "__main__":
    # APPSIMULATOR_MODE = 'single'
    if APPSIMULATOR_MODE == 'single':
        taskId = -1
        timer_no = -1
    else:
        taskId = sys.argv[1]
        timer_no = int(sys.argv[2])

    task = {
        'taskId': taskId,
        'app_name': 'douyin',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': timer_no
    }

    main(task_info=task, mode=APPSIMULATOR_MODE)
    print("Quit after 30 seconds.")
    time.sleep(30)
