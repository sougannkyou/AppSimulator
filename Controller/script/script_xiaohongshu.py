# coding:utf-8
import sys
import time
import os

sys.path.append(os.getcwd())

from Controller.setting import APPSIMULATOR_MODE
from Controller.Common import *
from Controller.NoxConSelenium import NoxConSelenium
from Controller.ControllerManager import Manager


##################################################################################
class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)
        option = task_info.get("option", {"keyword": "玫琳凯"})
        self.keyword = option["keyword"]

    def script(self):
        try:
            # self.unlock(timeout=10)
            self.open_app()
            self.ignore_update()
            if not self.find_search_area():
                self._log("find_search_area", "failed.")
                return False
            if not self.search(self.keyword):
                self._log("search", "failed")
                return False
            if not self.sort():
                self._log("sort", "failed.")
                return False
            self.crawl(tries=3)
            return True
        except Exception as e:
            self._log('<<error>> script Exception:\n', str(e))
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

    def find_search_area(self):
        ret, x, y = self.find_element(comment='放大镜', timeout=2)
        if ret:
            self.click_xy(x, y, wait_time=5)
            return True
        else:
            return False

    def search(self, keyword):
        self.input_cn(keyword, wait_time=2)
        ret, x, y = self.find_element(comment="放大镜", timeout=2)
        if ret:
            self.click_xy(200, 90, wait_time=2)
            return True
        else:
            return False

    # 按时间排序
    def sort(self):
        ret, x, y = self.find_element(comment="综合排序", timeout=10)
        if not ret:
            self._log("find the rank button", "failed.")
            return False
        self.click_xy(x, y, wait_time=5)
        ret, x, y = self.find_element(comment="按时间排序", timeout=10)
        if not ret:
            return False
        self.click_xy(x, y, wait_time=5)
        return True

    # 判断是不是视频
    def is_video(self):
        ret, x, y = self.find_element(comment="视频+关注", timeout=5)
        if ret:
            return True
        else:
            return False

    # 判断是不是文章
    def is_article(self):
        ret, x, y = self.find_element(comment="文章+关注", timeout=5)
        if ret:
            return True
        else:
            return False

    # 视频详情信息需要点一下才能加载上
    def open_video_detail(self):
        x, y = 470, 700
        self.click_xy(x, y, wait_time=3)
        return True

    # 关闭视频详情
    def close_video_detail(self):
        ret, x, y = self.find_element(comment="关闭详情页", timeout=2)
        if ret:
            self.click_xy(x, y, wait_time=3)

    # 返回列表页
    def back_to_list_page(self):
        x, y = 20, 40
        self.click_xy(x, y, wait_time=2)

    # 采集详情
    def crawl_one(self, x, y, wait_time=5):
        self.click_xy(x, y, wait_time=wait_time)
        # ret, x, y = self.find_element(comment="返回列表页", timeout=10)
        # if not ret:
        #     self._log("crawl_one", "未匹配到返回图标")
        #     return False
        # 如果是视频，暂停视频！！！
        # x, y = 240, 300
        # self.click_xy(x, y, wait_time=2)
        # 判断是不是视频
        # ret, x, y = self.find_element(comment="视频", timeout=3)
        # if ret:
        if not self.is_article():
            self.open_video_detail()
            self.close_video_detail()
        self.back_to_list_page()
        return True

    # def crawl(self, tries=3):
    #     def crawl(_tries):
    #         if _tries <= 0:
    #             self._log("error", "fail to find element for too manay times.")
    #             return None
    #         ret, pos_list = self.find_elements(comment='定位视频', timeout=10)
    #         if ret:
    #             for x, y in pos_list:
    #                 ret = self.crawl_one(x, y, wait_time=5)
    #                 if ret:
    #                     _tries = tries
    #                 else:
    #                     _tries -= 1
    #         else:
    #             _tries -= 1
    #         self.next_page(wait_time=5)
    #         time.sleep(2)
    #         return crawl(_tries)
    #
    #     return crawl(tries)

    def crawl(self, tries=3):
        return self._crawl(tries)

    def _crawl(self, tries):
        _tries = tries
        for i in range(200):
            if _tries <= 0:
                self._log("error", "fail to find element for too manay times.")
                return None
            ret, pos_list = self.find_elements(comment='定位视频', timeout=10)
            if ret:
                for x, y in pos_list:
                    ret = self.crawl_one(x, y, wait_time=5)
                    if ret:
                        _tries = tries
                    else:
                        _tries -= 1
            else:
                _tries -= 1

            self.v_scroll(wait_time=5)
            time.sleep(2)


##################################################################################
def main(task, mode):
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
        # me._DEBUG = True
        me._DEBUG = False
        me.run()
    except Exception as e:
        msg = '<<error>> Exception:'
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
    if APPSIMULATOR_MODE == MODE_SINGLE:
        taskId = -1
        timer_no = -1
    else:
        taskId = sys.argv[1]
        timer_no = sys.argv[2]

    task = {
        'taskId': taskId,
        'app_name': 'xiaohongshu',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': timer_no,
        'option': {
            'keyword': "玫琳凯",
        },
    }

    main(task=task, mode=APPSIMULATOR_MODE)
    print("Quit after 30 seconds.")
    time.sleep(30)
