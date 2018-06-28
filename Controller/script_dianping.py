# coding:utf-8
import sys
import time
from datetime import datetime
from Controller.NoxConSelenium import NoxConSelenium
from Controller.NoxConDocker import NoxConDocker

urls = [
    "http://www.dianping.com/shop/93643555",
]

keywords = [
    '九本しんいち居酒屋(亚运村店)',
    '匹夫涮肉城 黄村店',
    '鲜牛记潮汕牛肉火锅 亚运村店',
    '海底捞火锅(大屯北路店)',
    '小吊梨汤(新奥店)',
    '盘古七星酒店聚福园自助餐厅',
    '丰茂烤串l羊肉现穿才好吃(金泉美食宫店)',
    '初色海鲜姿造自助火锅(时代名门商场店)',
    '鱼图腾·好吃的鱼头泡饼(亚运村店)',
    '金鼎轩·南北菜(亚运村店)',
]


class MySelenium(NoxConSelenium):
    def script(self):
        ret = True
        x = -1
        y = -1
        page_cnt = 0
        self.get(urls[0], 3)
        ret, x, y = self.find_element(comment='web打开APP', timeout=10)
        if ret: ret = self.click_xy(x, y, wait_time=2)
        if ret: ret, x, y = self.find_element(comment='APP图标', timeout=10)
        if ret: ret = self.click_xy(x, y, wait_time=2)
        if ret: ret, x, y = self.find_element(comment='附近热搜', timeout=5)
        if ret: ret = self.click_xy(x, y, wait_time=1)
        time.sleep(3)
        if ret: ret = self.input_cn(keywords[0], timeout=1)
        time.sleep(5)
        if ret: ret, x, y = self.find_element(comment='搜索', timeout=5)
        if ret: ret = self.click_xy(x, y + 30, wait_time=1)

        ret, x, y = self.find_element(comment='APP打开结果OK', timeout=60)
        find = False
        pos_list = []
        for i in range(5):
            ret, x, y = self.find_element(comment='全部网友点评', timeout=5)
            if ret:
                find = True
                ret = self.click_xy(x, y, wait_time=1)
                break
            else:
                ret = self.next_page(wait_time=1)

        while find and ret:
            if ret:
                ret, pos_list = self.find_elements(comment='打分', timeout=10)
                if not ret:
                    ret = self.next_page(wait_time=1)
                    print('next_page:', page_cnt)

            for pos in pos_list:
                (x, y) = pos
                if ret: ret = self.click_xy(x, y, wait_time=1)
                if ret:
                    ret, x, y = self.find_element(comment='分享', timeout=10)
                else:
                    (x, y) = pos
                    if ret: ret = self.click_xy(x, y, wait_time=1)
                    if ret: ret, x, y = self.find_element(comment='分享', timeout=10)

                if ret: ret = self.click_xy(x, y, wait_time=1)
                if ret: ret, x, y = self.find_element(comment='复制链接', timeout=10)
                if ret: ret = self.click_xy(x, y, wait_time=1)
                if ret: ret = self.back(wait_time=1)

            if ret: ret = self.next_page(wait_time=1)


##################################################################################
def main(task):
    start = datetime.now()
    print("[Script " + task['docker_name'] + "] run start.", start)
    try:
        me = MySelenium(task_info=task)
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
        })
        me.set_gps(39.984727, 116.310050)  # 中关村
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
    # taskId = sys.argv[1]
    taskId = 1
    task = {
        'taskId': taskId,
        'app_name': 'dianping',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': 2
    }
    main(task)
    print("Close after 60 seconds.")
    time.sleep(60)
