import sys
import os
import time
from datetime import datetime

sys.path.append(os.getcwd())

from Controller.setting import *
from Controller.Common import *
from Controller.NoxConSelenium import NoxConSelenium
from Controller.ControllerManager import Manager


##################################################################################
class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)

    def script(self):
        try:
            self.open_app()
            self.ignore_update()
            self.crawl()
            return True
        except Exception as e:
            self._log('error:', str(e))
            return False

    def open_app(self):
        ret, x, y = self.find_element(comment='APP图标', timeout=10)  # unlock ok
        if ret:
            self.click_xy(x, y, wait_time=20)
            return True
        else:
            self._log("error", "app not found.")
            return False

    def ignore_update(self):
        ret, x, y = self.find_element(comment='忽略升级', timeout=5)
        if ret:
            self.click_xy(x, y, wait_time=2)
        return True

    # 采集详情
    def crawl_one(self):
        pass

    # 采集
    def crawl(self):
        pass


##################################################################################
def main(task, mode, debug=False):
    msg = ''
    error = ''
    start = datetime.now()
    common_log(True, task['taskId'], 'Script ' + task['docker_name'], 'start', task)

    try:
        me = MySelenium(task_info=task, mode=mode)
        me.set_comment_to_pic({
            "定位视频": 'images/{}/click_one.png'.format(task["app_name"]),
            "APP图标": 'images/{}/app_icon.png'.format(task["app_name"]),
            "忽略升级": 'images/{}/ignore_upgrade.png'.format(task["app_name"]),
            "放大镜": 'images/{}/search.png'.format(task["app_name"]),
            "综合排序": 'images/{}/rank.png'.format(task["app_name"]),
            "按时间排序": 'images/{}/rule.png'.format(task["app_name"]),
            "关闭详情页": 'images/{}/close_detail.png'.format(task["app_name"]),
            "视频+关注": 'images/{}/video_follow.png'.format(task["app_name"]),
            "文章+关注": 'images/{}/article_follow.png'.format(task["app_name"]),
        })
        me._DEBUG = debug
        me.run()
    except Exception as e:
        msg = '<<error>>'
        error = e
    finally:
        if APPSIMULATOR_MODE == MODE_MULTI:  # multi nox mode
            m = Manager()
            m.nox_run_task_finally(taskId)

        common_log(True, task['taskId'], 'Script ' + task['docker_name'] + 'end.',
                   msg + 'total times:' + str((datetime.now() - start).seconds) + 's', error)
        return


#################################################################################
if __name__ == "__main__":
    # APPSIMULATOR_MODE = MODE_SINGLE
    if APPSIMULATOR_MODE == MODE_SINGLE:
        taskId = -1
        timer_no = -1
    else:
        taskId = sys.argv[1]
        timer_no = int(sys.argv[2])

    task = {
        'taskId': taskId,
        'app_name': 'xiaohongshu',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': timer_no,
        'option': {
            'keyword': "",
            'channel': "",
        },
    }

    main(task=task, mode=APPSIMULATOR_MODE, debug=True)
    print("Quit after 30 seconds.")
    time.sleep(30)
