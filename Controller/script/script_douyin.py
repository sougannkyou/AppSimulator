# coding:utf-8
import sys
import time
import os

sys.path.append(os.getcwd())

from Controller.Common import *
from Controller.setting import APPSIMULATOR_MODE
from Controller.NoxConSelenium import NoxConSelenium
from Controller.ControllerManager import Manager

# comments
url = "https://www.iesdouyin.com/share/video/6578652904150797581/?region=CN&mid=6576897816944184072&titleType=title&utm_source=copy_link&utm_campaign=client_share&utm_medium=android&app=aweme&iid=38787387499&timestamp=1532499011"


class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)

    def script(self):
        ret = self.get(url, wait_time=2)  # unlock ok

        ret, x, y = self.find_element(comment='跳转APP', timeout=10)  # unlock ok
        if ret: ret = self.click_xy(x, y, wait_time=2)

        ret, x, y = self.find_element(comment='评论', timeout=10)  # unlock ok
        if ret: ret = self.click_xy(x, y, wait_time=2)

        page_cnt = 0
        while ret:  # 更新 -> 分享 -> 复制链接
            print('page_cnt', page_cnt)
            self.v_scroll(wait_time=5)
            page_cnt += 1


##################################################################################
def main(task_info, mode):
    msg = ''
    error = ''
    start = datetime.now()
    print("[Script " + task_info['docker_name'] + "] start at ", start, '\n', task_info)
    try:
        me = MySelenium(task_info=task_info, mode=mode)
        me.set_comment_to_pic({
            "跳转APP": 'images/douyin/jump2app.png',
            "APP图标": 'images/douyin/app_icon.png',
            "评论": 'images/douyin/comments.png',
            "更新": 'images/douyin/update.png',
            "分享": 'images/douyin/share.png',
            "复制链接": 'images/douyin/copylink.png',
            "跳过软件升级": 'images/douyin/ignore_upgrade.png',
        })
        me._DEBUG = True
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


if __name__ == "__main__":
    _DEBUG = True

    if APPSIMULATOR_MODE == MODE_SINGLE:
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
    print("Close after 30 seconds.")
    time.sleep(30)
