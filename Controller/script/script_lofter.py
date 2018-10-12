import sys
import os
import time
from datetime import datetime

sys.path.append(os.getcwd())

from Controller.setting import *
from Controller.Common import *
from Controller.NoxConSelenium import NoxConSelenium
from Controller.ControllerManager import Manager


#################################################################################
class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)

    def script(self):
        try:
            ret, x, y = self.find_element(comment='APP图标', timeout=10)  # unlock ok
            if ret:
                ret = self.click_xy(x, y, wait_time=5)

            self.h_scroll(from_x=450, from_y=650, to_x=10, to_y=650)
            scroll_num = 1
            while ret:
                ret, pos_list = self.find_elements(comment='分享', timeout=10, threshold=0.90)
                if ret:
                    scroll_num = 1
                    for pos in pos_list:
                        (x, y) = pos
                        ret = self.click_xy(x, y, wait_time=2)  # click 分享
                        if ret:
                            ret, x, y = self.find_element(comment='复制链接', timeout=10)
                            if ret:
                                ret = self.click_xy(x, y, wait_time=1)
                                # ret = self.click_xy(x, y, wait_time=1)
                            else:  # upgrade?
                                # ret = self.check_upgrade(timeout=2)
                                # if ret:
                                # print("重试 click 分享 按钮 ...")
                                ret, x, y = self.find_element(comment='分享', timeout=10)
                                if ret: ret = self.click_xy(x, y, wait_time=1)

                                if ret: ret, x, y = self.find_element(comment='复制链接', timeout=10)
                                if ret: ret = self.click_xy(x, y, wait_time=1)
                                # if ret: ret = self.click_xy(x, y, wait_time=1)
                    self.v_scroll()
                else:
                    ret = True
                    self.v_scroll()
                    scroll_num += 1
                    if scroll_num >= 3:
                        ret = False


        except Exception as e:
            self._log('<<error>>', e)


##################################################################################
def main(task, mode):
    msg = ''
    error = ''
    start = datetime.now()
    common_log(True, task['taskId'], 'Script ' + task['docker_name'], 'start', task)
    try:
        me = MySelenium(task_info=task, mode=mode)
        me.set_comment_to_pic({
            "APP图标": 'images/lofter/app_icon.png',
            # "更新": 'images/lofter/update.png',
            "分享": 'images/lofter/share.png',
            "复制链接": 'images/lofter/copylink.png',
            # "跳过软件升级": 'images/lofter/ignore_upgrade.png',
        })
        me._DEBUG = True
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
    APPSIMULATOR_MODE = 'single'
    if APPSIMULATOR_MODE == 'single':
        taskId = -1
        timer_no = -1
        redis_key = 'test'
    else:
        taskId = sys.argv[1]
        timer_no = int(sys.argv[2])
        redis_key = sys.argv[3]

    task = {
        'taskId': taskId,
        'app_name': 'miaopai',
        'redis_key': redis_key,
        'docker_name': 'nox-' + str(taskId),
        'timer_no': timer_no
    }

    main(task=task, mode=APPSIMULATOR_MODE)
    print("Quit after 30 seconds.")
    time.sleep(30)
