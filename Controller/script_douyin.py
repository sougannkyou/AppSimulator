# coding:utf-8
import sys
import time
from datetime import datetime
from Controller.NoxConSelenium import NoxConSelenium


class MySelenium(NoxConSelenium):
    def __init__(self, task_info):
        super().__init__(task_info=task_info)

    def script(self):
        ret, x, y = self.find_element(comment=u'APP图标', timeout=10)  # unlock ok
        if ret: ret = self.click_xy(x, y, wait_time=2)
        while ret:  # 更新 -> 分享 -> 复制链接
            if ret: ret, x, y = self.find_element(comment=u'更新', timeout=10)
            if ret: ret = self.click_xy(x, y, wait_time=1)

            if ret: ret, x, y = self.find_element(comment=u'分享', timeout=10)
            if ret: ret = self.click_xy(x, y, wait_time=1)

            if ret:
                ret, x, y = self.find_element(comment=u'复制链接', timeout=10)
                if ret:
                    ret = self.click_xy_timer(x, y, wait_time=1)
                else:  # upgrade?
                    # ret = self.check_upgrade(timeout=2)
                    # if ret:
                    print(u"重试 click 分享 按钮 ...")
                    ret, x, y = self.find_element(comment=u'分享', timeout=10)
                    if ret: ret = self.click_xy(x, y, wait_time=1)

                    if ret: ret, x, y = self.find_element(comment=u'复制链接', timeout=10)
                    if ret: ret = self.click_xy(x, y, wait_time=1)


##################################################################################
def main(task):
    start = datetime.now()
    print("[Script " + docker_name + "] start at ", start, '\n', task)
    try:
        me = MySelenium(task_info=task)
        me.set_comment_to_pic({
            "锁屏": 'images/screen_lock.png',
            "锁屏图案": 'images/screen_lock_9point.png',
            "APP图标": 'images/douyin/app_icon.png',
            "更新": 'images/douyin/update.png',
            "分享": 'images/douyin/share.png',
            "复制链接": 'images/douyin/copylink.png',
            "跳过软件升级": 'images/douyin/ignore_upgrade.png',
        })

        # if not ret: self.send2web('images/offline.jpeg')
        me.run(is_app_restart=True)
        # me._DEBUG = True
        end = datetime.now()
        print("[Script " + docker_name + "] total times:", (end - start).seconds, "s")
        return True
    except Exception as e:
        end = datetime.now()
        print("[Script " + docker_name + "] total times:", (end - start).seconds, "s error:", e)
        return False


if __name__ == "__main__":
    docker_name = sys.argv[1]
    # docker_name = 'nox-3'
    main({
        'taskId': 3,
        'app_name': 'douyin',
        'docker_name': docker_name,
        'timer_no': 3
    })
    print("Close after 60 seconds.")
    time.sleep(60)
