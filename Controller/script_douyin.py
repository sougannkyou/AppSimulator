# coding:utf-8
import os
import sys

sys.path.append(os.getcwd())

import time
from Controller.Common import *
from Controller.setting import APPSIMULATOR_MODE
from Controller.NoxConDocker import NoxConDocker
from Controller.NoxConSelenium import NoxConSelenium
from Controller.ControllerManager import Manager

_DEBUG = False

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
            self.next_page_comments(wait_time=5)
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
