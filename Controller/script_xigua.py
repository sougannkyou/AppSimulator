# coding:utf-8
import os
import sys

# sys.path.append(os.getcwd())
# sys.path.append('C:\Python\Python35\Lib\site-packages\cv2')
# print(sys.path)

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
            if ret:
                self.click_xy(x, y, wait_time=20)
            else:
                self._log("error", "app not found.")
                return None
            # ret, x, y = self.find_element(comment='忽略升级', timeout=10)
            # if ret:
            #     self.click_xy(x, y, wait_time=2)
            self.crawl(tries=5)
        except Exception as e:
            self._log('error:', e)

    def crawl(self, tries=3):
        def crawl(_tries):
            if _tries <= 0:
                self._log("error", "fail to find element for too manay times.")
                return None
            ret, poses = self.find_elements(comment='分享', timeout=10)
            if ret:
                for x, y in poses:
                    self.click_xy(x, y, wait_time=2)  # click 分享
                    ret, x, y = self.find_element(comment='复制链接', timeout=10)
                    if ret:
                        self.click_xy(x, y, wait_time=1)
                        _tries = tries
                    else:
                        _tries -= 1
            else:
                _tries -= 1
            self.next_page_700(wait_time=5)
            return crawl(_tries)

        return crawl(tries)


##################################################################################
def main(task, mode):
    msg = ''
    error = ''
    start = datetime.now()
    common_log(_DEBUG, task['taskId'], 'Script ' + task['docker_name'], 'start', task)

    try:
        me = MySelenium(task_info=task, mode=mode)
        me.set_comment_to_pic({
            "APP图标": 'images/{}/app_icon.png'.format(task["app_name"]),
            "广告": 'images/{}/ad.png'.format(task["app_name"]),
            "分享": 'images/{}/share.png'.format(task["app_name"]),
            "复制链接": 'images/{}/copylink.png'.format(task["app_name"]),
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
            docker.quit()
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
        taskId = 4
        mode = 'single'
    else:
        taskId = sys.argv[1]
        mode = 'multi'

    task = {
        'taskId': taskId,
        'app_name': 'xigua',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': 2  # 5s
    }
    main(task=task, mode=mode)
    print("Close after 30 seconds.")
    time.sleep(30)