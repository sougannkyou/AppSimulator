# coding:utf-8
import sys
import time
from datetime import datetime
from Controller.NoxConSelenium import NoxConSelenium

urls = [
    "http://www.miaopai.com/show/6NWi1Bp5fx9GV0tdwCUGYWNzaQm9hVJe.htm",  # 936
]


class MySelenium(NoxConSelenium):
    def __init__(self, task_info):
        super().__init__(task_info)

    def script(self):
        try:
            ret, x, y = self.find_element(comment='app_icon', timeout=10)  # unlock ok
            if ret:
                ret = self.click_xy(x, y, wait_time=2)

            while ret:
                ret, pos_list = self.find_elements(comment='share', timeout=10)
                if ret:
                    for pos in pos_list:
                        (x, y) = pos
                        ret = self.click_xy(x, y, wait_time=2)
                        if ret:
                            ret, x, y = self.find_element(comment='copylink', timeout=10)
                            if ret:
                                ret = self.click_xy_timer(x, y, wait_time=1)
                            else:  # upgrade?
                                # ret = self.check_upgrade(timeout=2)
                                # if ret:
                                # print("重试 click 分享 按钮 ...")
                                ret, x, y = self.find_element(comment='share', timeout=10)
                                if ret: ret = self.click_xy(x, y, wait_time=1)

                                if ret: ret, x, y = self.find_element(comment='copylink', timeout=10)
                                if ret: ret = self.click_xy(x, y, wait_time=1)

                self.next_page(wait_time=5)

        except Exception as e:
            self._log('error:', e)


##################################################################################
def main(task):
    start = datetime.now()
    print("[Script " + task['docker_name'] + "] start at ", start, '\n', task)
    try:
        me = MySelenium(task_info=task)
        me.set_comment_to_pic({
            "app_icon": 'images/miaopai/app_icon.png',
            "update": 'images/miaopai/update.png',
            "share": 'images/miaopai/share.png',
            "copylink": 'images/miaopai/copylink.png',
            "ignore_upgrade": 'images/miaopai/ignore_upgrade.png',
        })
        # me._DEBUG = True
        me.run(is_app_restart=True)
        end = datetime.now()
        print("[Script " + task['docker_name'] + "] total times:", str((end - start).seconds) + "s")
        return True
    except Exception as e:
        end = datetime.now()
        print("[Script " + task['docker_name'] + "] total times:", str((end - start).seconds) + "s\nerror:", e)
        return False


if __name__ == "__main__":
    # taskId = sys.argv[1]
    taskId = 1
    task = {
        'taskId': taskId,
        'app_name': 'miaopai',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': 2
    }
    main(task)
    print("Close after 60 seconds.")
    time.sleep(60)
