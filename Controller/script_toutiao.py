# coding:utf-8
import os
import sys
import time

sys.path.append(os.getcwd())

from Controller.setting import APPSIMULATOR_MODE
from Controller.Common import *
from Controller.NoxConSelenium import NoxConSelenium
from Controller.ControllerManager import Manager

urls = [
    "https://m.toutiaocdn.cn/group/6565684301512311300/?iid=14592851837&app=news_article&timestamp=1528703355&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
    "http://m.toutiaocdn.cn/group/6563987941163532803/?iid=14592851837&app=news_article&timestamp=1528341722&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
    "https://m.toutiaocdn.cn/group/6565632060814262792/?iid=14592851837&app=news_article&timestamp=1528702278&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
    "http://m.toutiaocdn.cn/group/6563914570526622216/?iid=14592851837&app=news_article&timestamp=1528341946&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
    "http://m.toutiaocdn.cn/group/6563778505752969741/?iid=14592851837&app=news_article&timestamp=1528267671&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
    "http://m.toutiaocdn.cn/group/6563793627670118919/?iid=14592851837&app=news_article&timestamp=1528277350&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
]

comments = [
    "转发1",
    "转发2",
    "转发3",
    "转发4",
    "转发5",
    "转发6",
]

#################################################################################
class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)

    def script(self):
        self.get(url=urls[0], wait_time=5)
        self.next_page_browser(3)
        ret, x, y = self.find_element(comment='jump2app', timeout=5)
        if ret:
            ret = self.click_xy(x, y, wait_time=2)
        else:
            # ret = self.next_page(timeout=1)
            ret = self.next_page_browser(1)
            ret, x, y = self.find_element(comment='jump2app', timeout=10)
            if ret:
                ret = self.click_xy(x, y, wait_time=2)
            else:
                # ret = self.next_page(timeout=1)
                ret = self.next_page_browser(1)
                ret, x, y = self.find_element(comment='jump2app', timeout=10)
                if ret: ret = self.click_xy(x, y, wait_time=2)

        ret, x, y = self.find_element(comment='writeComment', timeout=5)
        if ret: ret = self.click_xy(x, y, wait_time=2)
        if ret: ret = self.input_cn(comments[0], wait_time=1)
        time.sleep(5)
        if ret: ret, x, y = self.find_element(comment='publish', timeout=5)
        if ret: ret = self.click_xy(x, y, wait_time=1)
        # self.task_trace()


##################################################################################
def main(task_info, mode):
    msg = ''
    error = ''
    start = datetime.now()
    common_log(_DEBUG, task['taskId'], 'Script ' + task['docker_name'], 'start', task)
    try:
        me = MySelenium(task_info=task_info, mode=mode)
        me.set_comment_to_pic({
            "jump2app": 'images/toutiao/jump2app.png',
            "writeComment": 'images/toutiao/writeComment.png',
            "publish": 'images/toutiao/publish.png',
        })
        me._DEBUG = True
        # me.set_gps(39.984727, 116.310050)  # 中关村
        me.run()

        end = datetime.now()
        print("[Script " + task_info['docker_name'] + "] total times:", str((end - start).seconds) + "s")
    except Exception as e:
        msg = '<<error>>'
        error = e
    finally:
        if APPSIMULATOR_MODE != 'vmware':  # multi nox mode
            m = Manager()
            m.nox_run_task_finally(taskId)

        common_log(True, task['taskId'], 'Script ' + task['docker_name'] + 'end.',
                   msg + 'total times:' + str((datetime.now() - start).seconds) + 's', error)
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
        'app_name': 'toutiao',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': timer_no
    }

    main(task_info=task, mode='single')
    print("Close after 30 seconds.")
    time.sleep(30)
