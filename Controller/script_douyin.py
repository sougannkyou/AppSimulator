# coding:utf-8
import os
import sys

sys.path.append(os.getcwd())

import time
from datetime import datetime
from Controller.NoxConSelenium import NoxConSelenium


class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)

    def script(self):
        try:
            ret, x, y = self.find_element(comment='APP图标', timeout=10)  # unlock ok
            if ret: ret = self.click_xy(x, y, wait_time=2)

            while ret:  # 更新 -> 分享 -> 复制链接
                ret, x, y = self.find_element(comment='分享', timeout=10)
                if ret:
                    ret = self.click_xy(x, y, wait_time=1)
                    if ret:
                        ret, x, y = self.find_element(comment='复制链接', timeout=10)
                        if ret:
                            ret = self.click_xy_timer(x, y, wait_time=1)
                        else:  # upgrade?
                            # ret = self.check_upgrade(timeout=2)
                            # if ret:
                            print("重试 click 分享 按钮 ...")
                            ret, x, y = self.find_element(comment='分享', timeout=10)
                            if ret:
                                ret = self.click_xy(x, y, wait_time=1)
                                if ret:
                                    ret, x, y = self.find_element(comment='复制链接', timeout=10)
                                    if ret:
                                        ret = self.click_xy(x, y, wait_time=1)

                self.next_page(wait_time=5)

        except Exception as e:
            self._log('error:', e)


##################################################################################
def main(task_info, mode):
    start = datetime.now()
    print("[Script " + task_info['docker_name'] + "] start at ", start, '\n', task_info)
    try:
        me = MySelenium(task_info=task_info, mode=mode)
        me.set_comment_to_pic({
            "锁屏": 'images/screen_lock.png',
            "锁屏图案": 'images/screen_lock_9point.png',
            "APP图标": 'images/douyin/app_icon.png',
            "更新": 'images/douyin/update.png',
            "分享": 'images/douyin/share.png',
            "复制链接": 'images/douyin/copylink.png',
            "跳过软件升级": 'images/douyin/ignore_upgrade.png',
        })

        me.run()
        # me._DEBUG = True
        end = datetime.now()
        print("[Script " + task_info['docker_name'] + "] total times:", str((end - start).seconds) + "s")
        return True
    except Exception as e:
        end = datetime.now()
        print("[Script " + task_info['docker_name'] + "] total times:", str((end - start).seconds) + "s\nerror:", e)
        return False


if __name__ == "__main__":
    # taskId = sys.argv[1]
    taskId = 1
    task = {
        'taskId': taskId,
        'app_name': 'douyin',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': 1  # 5s
    }
    main(task_info=task, mode='single')
    print("Close after 60 seconds.")
    time.sleep(60)
