# coding:utf-8
import sys
import time
from datetime import datetime
from Controller.NoxConSelenium import NoxConSelenium

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


class MySelenium(NoxConSelenium):
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
        if ret: ret = self.input_cn(comments[0], timeout=1)
        time.sleep(5)
        if ret: ret, x, y = self.find_element(comment='publish', timeout=5)
        if ret: ret = self.click_xy(x, y, wait_time=1)
        # self.task_trace()


##################################################################################
def main(task):
    start = datetime.now()
    print("[Script " + task['docker_name'] + "] start at ", start)
    try:
        me = MySelenium(task_info=task)
        me.set_comment_to_pic({
            "jump2app": 'images/toutiao/jump2app.png',
            "writeComment": 'images/toutiao/writeComment.png',
            "publish": 'images/toutiao/publish.png',
        })
        me._DEBUG = True
        # me.set_gps(39.984727, 116.310050)  # 中关村
        me.run(is_app_restart=False)

        end = datetime.now()
        print("[Script " + task['docker_name'] + "] total times:", str((end - start).seconds) + "s")
        return True
    except Exception as e:
        end = datetime.now()
        print("[Script " + task['docker_name'] + "] total times:", str((end - start).seconds) + "s\nerror:", e)
        return False


#################################################################################
if __name__ == "__main__":
    # docker_name = sys.argv[1]
    # taskId = sys.argv[1]
    taskId = 2
    task = {
        'taskId': taskId,
        'app_name': 'miaopai',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': 2
    }
    main(task)
    print("Close after 60 seconds.")
    time.sleep(60)

