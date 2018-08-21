# coding:utf-8
import os
import sys
import signal

sys.path.append(os.getcwd())

import time
from Controller.setting import APPSIMULATOR_MODE
from Controller.Common import *
from Controller.NoxConSelenium import NoxConSelenium
from Controller.ControllerManager import Manager

_DEBUG = False
taskId = -1
timer_no = -1
mode = 'single'


##################################################################################
def task_finally():
    if APPSIMULATOR_MODE == 'vmware':
        return

    m = Manager()
    m.nox_run_task_complete(taskId)
    print("task finally wait 30 seconds.")
    time.sleep(30)


def signal_int_handler(signal, frame):
    print(taskId, 'You pressed Ctrl+C!')
    task_finally()
    return


def signal_kill_handler(signal, frame):
    print(taskId, 'be killed!')
    task_finally()
    return


signal.signal(signal.SIGINT, signal_int_handler)
signal.signal(signal.SIGKILL, signal_kill_handler)


##################################################################################
class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)

    def script(self):
        try:
            ret, x, y = self.find_element(comment='APP图标', timeout=10)  # unlock ok
            if ret:
                ret = self.click_xy(x, y, wait_time=2)

            while ret:
                ret, pos_list = self.find_elements(comment='分享', timeout=10)
                if ret:
                    for pos in pos_list:
                        (x, y) = pos
                        ret = self.click_xy(x, y, wait_time=2)  # click 分享
                        if ret:
                            ret, x, y = self.find_element(comment='复制链接', timeout=10)
                            if ret:
                                ret = self.click_xy_timer(x, y, wait_time=1)
                                # ret = self.click_xy(x, y, wait_time=1)
                            else:  # upgrade?
                                # ret = self.check_upgrade(timeout=2)
                                # if ret:
                                # print("重试 click 分享 按钮 ...")
                                ret, x, y = self.find_element(comment='分享', timeout=10)
                                if ret: ret = self.click_xy(x, y, wait_time=1)

                                if ret: ret, x, y = self.find_element(comment='复制链接', timeout=10)
                                if ret: ret = self.click_xy_timer(x, y, wait_time=1)
                                # if ret: ret = self.click_xy(x, y, wait_time=1)

                self.next_page()

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
            "APP图标": 'images/miaopai/app_icon.png',
            "更新": 'images/miaopai/update.png',
            "分享": 'images/miaopai/share.png',
            "复制链接": 'images/miaopai/copylink.png',
            "跳过软件升级": 'images/miaopai/ignore_upgrade.png',
        })
        # me._DEBUG = True
        me.run()
    except Exception as e:
        msg = '<<error>>'
        error = e
    finally:
        task_finally()
        end = datetime.now()
        common_log(_DEBUG, task['taskId'], 'Script ' + task['docker_name'] + 'end.',
                   msg + 'total times:' + str((end - start).seconds) + 's', error)
        return


if __name__ == "__main__":
    _DEBUG = True

    # signal.signal(signal.SIGINT, signal_int_handler)

    # APPSIMULATOR_MODE = 'vmware'

    if APPSIMULATOR_MODE != 'vmware':
        taskId = sys.argv[1]
        timer_no = int(sys.argv[2])
        mode = 'multi'

    task = {
        'taskId': taskId,
        'app_name': 'miaopai',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': timer_no
    }

    main(task=task, mode=mode)
    print("Quit after 30 seconds.")
    time.sleep(30)
