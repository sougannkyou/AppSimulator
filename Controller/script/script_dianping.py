import sys
import os
import time
from datetime import datetime

sys.path.append(os.getcwd())

from Controller.setting import *
from Controller.Common import *
from Controller.NoxConSelenium import NoxConSelenium
from Controller.ControllerManager import Manager


urls = [
    "http://www.dianping.com/shop/508130",
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


#################################################################################
class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)

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
        if ret: ret = self.click_xy(x, y, wait_time=3)
        if ret: ret = self.input_cn(keywords[0], wait_time=5)
        if ret: ret, x, y = self.find_element(comment='搜索', timeout=5)
        if ret: ret = self.click_xy(x, y + 30, wait_time=1)

        ret, x, y = self.find_element(comment='APP打开结果OK', timeout=60)
        find = False
        _pos_list = []
        for i in range(5):
            ret, x, y = self.find_element(comment='全部网友点评', timeout=5)
            if ret:
                find = True
                ret = self.click_xy(x, y, wait_time=1)
                break
            else:
                ret = self.v_scroll(from_y=710, to_y=10, wait_time=1)
        fail = 0
        while find and ret:
            if ret:
                ret, pos_list = self.find_elements(comment='分享', timeout=10)
                if pos_list == _pos_list:
                    fail += 1
                    if fail >= 5:
                        break
                else:
                    fail = 0
                _pos_list = pos_list
                for pos in pos_list:
                    (x, y) = pos
                    if ret: ret = self.click_xy(x, y, wait_time=1)
                    if ret: ret, x, y = self.find_element(comment='复制链接', timeout=10)
                    if ret: ret = self.click_xy_timer(x, y, wait_time=1)

            ret = self.v_scroll(from_y=710, to_y=10, wait_time=1)


##################################################################################
def main(task, mode):
    msg = ''
    error = ''
    start = datetime.now()
    common_log(True, task['taskId'], 'Script ' + task['docker_name'], 'start', task)

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


#################################################################################
if __name__ == "__main__":
    # APPSIMULATOR_MODE = MODE_SINGLE
    if APPSIMULATOR_MODE == MODE_SINGLE:
        taskId = -1
        timer_no = -1
    else:
        taskId = sys.argv[1]
        timer_no = int(sys.argv[2])

    task = {
        'taskId': taskId,
        'app_name': 'dianping',
        'docker_name': 'nox-' + str(taskId),
        'timer_no': timer_no
    }

    main(task=task, mode=APPSIMULATOR_MODE)
    print("Quit after 30 seconds.")
    time.sleep(30)
