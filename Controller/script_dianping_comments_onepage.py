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

<<<<<<< Updated upstream
        self.capture_name = 'capture_' + self._docker_name + '.png'
        self.capture_before_name = 'capture_' + self._docker_name + '_before.png'
        self.capture_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_name
        self.capture_before_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_before_name

        self.capture_cut_name = 'capture_' + self._docker_name + '_cut.png'
        self.capture_before_cut_name = 'capture_' + self._docker_name + '_before_cut.png'
        self.capture_cut_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_cut_name
        self.capture_before_cut_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_before_cut_name

        self.capture_comment_name = 'capture_' + self._docker_name + '_comment.png'
        self.capture_comment_cut_name = 'capture_' + self._docker_name + '_comment_cut.png'
        self.capture_comment_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_comment_name
        self.capture_comment_cut_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_comment_cut_name

        # border_path = self._work_path + '\\Controller\\images\\dianping\\border.png'
        self.border_path = self._work_path + '\\Controller\\images\\dianping\\border_128_128.png'
=======
    def pic_to_ocr(self, page_line=800):
        # start = datetime.now()
        temp_path = self._work_path + '\\Controller\\images\\temp\\'
        capture_name = 'capture_' + self._docker_name + '.png'
        capture_before_name = 'capture_' + self._docker_name + '_before.png'
        capture_path = temp_path + capture_name
        capture_before_path = temp_path + capture_before_name

        capture_name_new = 'capture_' + self._docker_name + '_new.png'
        capture_before_name_new = 'capture_' + self._docker_name + '_before_new.png'
        capture_path_new = temp_path + capture_name_new
        capture_before_path_new = temp_path + capture_before_name_new

        capture_concat_name = 'capture_' + self._docker_name + '_concat.png'
        capture_concat_name_new = 'capture_' + self._docker_name + '_concat_new.png'
        capture_concat_path = temp_path + capture_concat_name
        capture_concat_path_new = temp_path + capture_concat_name_new

        # border_path = self._work_path + '\\Controller\\images\\dianping\\border.png'
        border_path = self._work_path + '\\Controller\\images\\dianping\\border_128_128.png'

        # 前后页分别截图
        img = Image.open(capture_before_path)
        # img = img.crop((0, 0, 480, 750))
        img.save(capture_before_path_new)

        img = Image.open(capture_path)
        img = img.crop((0, 75, 480, page_line))
        img.save(capture_path_new)
        print('前后页分别截图')

        # 纵向合成 800 * 480
        img1 = cv2.imread(capture_before_path_new)
        img2 = cv2.imread(capture_path_new)
        img_bg = np.vstack((img1, img2))
        cv2.imwrite(capture_concat_path, img_bg)
        print('纵向合成')

        # 照片图框 152 * 152 or 128 * 128
        img_border = ac.imread(border_path)
>>>>>>> Stashed changes

    def get_photo_top_y(self, img_obj):
        # 照片图框 152 * 152 or 128 * 128
        img_border = ac.imread(self.border_path)
        h, w, _ = img_border.shape
        ret = ac.find_all_template(img_obj, img_border, threshold=0.5)
        l = []
        for r in ret:
            (x, y) = r['result']
            l.append(y)

        if l:
            ret = min(l)
        else:
            ret = -1

        return ret

    def pic_to_ocr(self, one_page, photo_top_y, page_line_y):
        # start = datetime.now()
        if one_page:
            y = 800
            img = Image.open(self.capture_path)
            if photo_top_y != -1:
                y = photo_top_y
            else:
                if page_line_y != -1:
                    y = page_line_y

            img = img.crop((0, 75, 480, y))
            img.save(self.capture_comment_cut_path)

        else:  # page_line_y is next page y
            # 前后页分别截图
            img = Image.open(self.capture_before_path)
            # img = img.crop((0, 0, 480, 750))
            img.save(self.capture_before_cut_path)

            img = Image.open(self.capture_path)
            img = img.crop((0, 75, 480, 800))
            img.save(self.capture_cut_path)

            # 800 * 480
            img1 = cv2.imread(self.capture_before_cut_path)
            img2 = cv2.imread(self.capture_cut_path)

            # 纵向合成
            img_concat = np.vstack((img1, img2))
            cv2.imwrite(self.capture_comment_path, img_concat)

            # 合成图截图
<<<<<<< Updated upstream
            img = Image.open(self.capture_comment_path)
            img = img.crop((0, 180, 480, min_y - h / 2))
            img.save(self.capture_comment_cut_path)
=======
            img = Image.open(capture_concat_path)
            img = img.crop((0, 0, 480, min_y - h / 2))
            img.save(capture_concat_path_new)
>>>>>>> Stashed changes

            image = Image.open(self.capture_comment_cut_path)
            code = pytesseract.image_to_string(image, lang='chi_sim')
<<<<<<< Updated upstream
            if code:
                print('-------------------\n', code)
            else:
                print('-------------------\n', 'not found comment')
=======
            code.replace('\r\n', '')
            print('-------------------\n', code)
        else:
            print('-------------------\n', 'not found concat photo')
>>>>>>> Stashed changes

    def script(self):
        # ret, x, y = self.find_element(comment='APP打开结果OK', timeout=60)
        # while ret:
        self.next_page(from_y=296, to_y=100, wait_time=1)

        ret, x, y = self.find_element(comment='展开全文', timeout=10)
        if ret:
            self.click_xy(x, y, wait_time=1)
            self.get_capture()

        # nox_adb.exe shell input swipe 240 670 240 10 2000
        # nox_adb.exe shell screencap -p /sdcard/capture.png
        # nox_adb.exe pull /sdcard/capture.png c:\Nox\
<<<<<<< Updated upstream
        ret, _, page_line_y = self.find_element(comment='分页线', timeout=10)
        if ret:
            img_obj = Image.open(self.capture_path)
            photo_top_y = self.get_photo_top_y(img_obj)
        else:
            ret = self.next_page(from_y=670, to_y=10, wait_time=1)
            self.get_capture()  # 更新截图
            img_obj = Image.open(self.capture_path)
            photo_top_y = self.get_photo_top_y(img_obj)
            if photo_top_y == -1:
                ret, _, page_line_y = self.find_element(comment='分页线', timeout=10)

        self.pic_to_ocr(one_page=ret, photo_top_y=photo_top_y, page_line_y=page_line_y)
=======
        ret = self.next_page(from_y=740, to_y=10, wait_time=1)
        ret, x, y = self.find_element(comment='分页', timeout=10)
        if ret:
            self.pic_to_ocr(page_line=y)
>>>>>>> Stashed changes

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
            "展开全文": 'images/dianping/show_all.png',
            "分页线": 'images/dianping/page_line.png',
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
    print("start")
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
