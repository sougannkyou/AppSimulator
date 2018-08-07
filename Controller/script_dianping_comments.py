# coding:utf-8
import os
import sys

sys.path.append(os.getcwd())
from PIL import Image
import cv2
import numpy as np
import aircv as ac
from datetime import datetime
import pytesseract

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

    def pic_to_ocr(self):
        # start = datetime.now()
        capture_name = 'capture_' + self._docker_name + '.png'
        capture_before_name = 'capture_' + self._docker_name + '_before.png'
        capture_path = self._work_path + '\\Controller\\images\\temp\\' + capture_name
        capture_before_path = self._work_path + '\\Controller\\images\\temp\\' + capture_before_name

        capture_name_new = 'capture_' + self._docker_name + '_new.png'
        capture_before_name_new = 'capture_' + self._docker_name + '_new_before.png'
        capture_path_new = self._work_path + '\\Controller\\images\\temp\\' + capture_name_new
        capture_before_path_new = self._work_path + '\\Controller\\images\\temp\\' + capture_before_name_new

        capture_concat_name = 'capture_' + self._docker_name + '_concat.png'
        capture_concat_name_new = 'capture_' + self._docker_name + '_concat_new.png'
        capture_concat_path = self._work_path + '\\Controller\\images\\temp\\' + capture_concat_name
        capture_concat_path_new = self._work_path + '\\Controller\\images\\temp\\' + capture_concat_name_new

        # border_path = self._work_path + '\\Controller\\images\\dianping\\border.png'
        border_path = self._work_path + '\\Controller\\images\\dianping\\border_128_128.png'

        # 前后页分别截图
        img = Image.open(capture_before_path)
        # img = img.crop((0, 0, 480, 750))
        img.save(capture_before_path_new)

        img = Image.open(capture_path)
        # img = img.crop((0, 75, 480, 750))
        img.save(capture_path_new)

        # 800 * 480
        img1 = cv2.imread(capture_before_path_new)
        img2 = cv2.imread(capture_path_new)

        # 纵向合成
        img_bg = np.vstack((img1, img2))
        cv2.imwrite(capture_concat_path, img_bg)

        # 照片图框 152 * 152
        img_border = ac.imread(border_path)

        h, w, _ = img_border.shape
        ret = ac.find_all_template(img_bg, img_border, threshold=0.5)
        l = []
        for r in ret:
            (x, y) = r['result']
            l.append(y)

        if l:
            min_y = min(l)
            print(min_y)

            # 合成图截图
            img = Image.open(capture_concat_path)
            img = img.crop((0, 180, 480, min_y - h / 2))
            img.save(capture_concat_path_new)

            image = Image.open(capture_concat_path_new)
            code = pytesseract.image_to_string(image, lang='chi_sim')
            print('-------------------\n', code)
        else:
            print('-------------------\n', 'not found photo')

    def script(self):
        ret = True
        x = -1
        y = -1
        page_cnt = 0
        # ret, x, y = self.find_element(comment='APP打开结果OK', timeout=60)
        # _pos_list = []
        # fail = 0
        # while ret:
        self.next_page(from_y=210, to_y=10, wait_time=1)

        ret, x, y = self.find_element(comment='全文', timeout=10)
        if ret:
            ret = self.click_xy(x, y, wait_time=1)
            self.get_capture()

        # nox_adb.exe shell input swipe 240 670 240 10 2000
        # nox_adb.exe shell screencap -p /sdcard/capture.png
        # nox_adb.exe pull /sdcard/capture.png c:\Nox\
        ret = self.next_page(from_y=670, to_y=10, wait_time=1)
        ret, x, y = self.find_element(comment='分页', timeout=10)
        if ret:
            self.pic_to_ocr()

        # self.back()
        # ret = self.next_page(wait_time=1)


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
            "全文": 'images/dianping/show_all.png',
            "分页": 'images/dianping/page_line.png',
            "star": 'images/dianping/star.png',
        })
        me._DEBUG = True
        me.run()
    except Exception as e:
        msg = '<<error>>'
        error = e
    finally:
        end = datetime.now()
        print(error)
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
