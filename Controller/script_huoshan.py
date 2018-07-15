# coding:utf-8
import os
import sys

sys.path.append(os.getcwd())

import time
from datetime import datetime
from Controller.NoxConSelenium import NoxConSelenium
from Controller.Common import common_log, common_runscript_countdown

_DEBUG = False


class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)

    def script(self):
        try:
            ret, x, y = self.find_element(comment='APP图标', timeout=10)  # unlock ok
            if ret: ret = self.click_xy(x, y, wait_time=2)
            # ret, x, y = self.find_element(comment='选择一个视频', timeout=10)
            if ret: ret = self.click_xy(200, 200, wait_time=2)

            while ret:
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
    common_log(_DEBUG, 'Script ' + task['docker_name'], 'start', task)

    try:
        me = MySelenium(task_info=task, mode=mode)
        me.set_comment_to_pic({
            "选择一个视频": 'images/huoshan/clickone.png',
            "APP图标": 'images/huoshan/app_icon.png',
            "更新": 'images/huoshan/update.png',
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
        common_log(_DEBUG, 'Script ' + task['docker_name'] + 'end.',
                   msg + 'total times:' + str((end - start).seconds) + 's', error)
        # common_runscript_countdown()
        return


if __name__ == "__main__":
    _DEBUG = True
    # taskId = sys.argv[1]
    taskId = 3
    task = {
        'taskId': taskId,
        'app_name': 'huoshan',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': 3  # 11s
    }
    main(task=task, mode='single')
    print("Close after 30 seconds.")
    time.sleep(30)
