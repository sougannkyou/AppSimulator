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
        ret = True
        x = -1
        y = -1
        page_cnt = 0
        ret, x, y = self.find_element(comment='APP打开结果OK', timeout=60)
        _pos_list = []
        fail = 0
        while ret:
            ret, x, y = self.find_element(comment='打分', timeout=10)
            if ret: ret = self.click_xy(x, y, wait_time=1)
            ret = self.find_element(comment='star', timeout=5)
            if not ret:
                ret = self.next_page(from_y=710, to_y=10, wait_time=1)


##################################################################################
def main(task, mode):
    msg = ''
    error = ''
    start = datetime.now()
    common_log(_DEBUG, task['taskId'], 'Script ' + task['docker_name'], 'start', task)

    try:
        me = MySelenium(task_info=task, mode=mode)
        me.set_comment_to_pic({
            "web打开APP": 'images/dianping/webOpenApp.png',
            "APP打开结果OK": 'images/dianping/search_ready.png',
            "APP图标": 'images/dianping/app_icon.png',
            '附近热搜': 'images/dianping/search.png',
            '搜索': 'images/dianping/search_btn.png',
            "网友点评": 'images/dianping/wangyoudianping.png',
            "全部网友点评": 'images/dianping/wangyoudianping-all.png',
            "分享": 'images/dianping/share.png',
            "复制链接": 'images/dianping/copy_link.png',
            "打分": 'images/dianping/dafen.png',
            "star": 'images/dianping/star.png',
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


#################################################################################
if __name__ == "__main__":
    _DEBUG = True

    if APPSIMULATOR_MODE == 'vmware':
        taskId = -1
        timer_no = -1
        mode = 'single'
    else:
        taskId = sys.argv[1]
        timer_no = int(sys.argv[2])
        mode = 'multi'

    task = {
        'taskId': taskId,
        'app_name': 'dianping',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': timer_no
    }

    main(task=task, mode=mode)
    print("Close after 30 seconds.")
    time.sleep(30)
