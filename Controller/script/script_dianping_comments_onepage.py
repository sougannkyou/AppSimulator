# coding:utf-8
import sys
import time
from pprint import pprint
from PIL import Image
import cv2
import numpy as np
import aircv as ac
import pytesseract

from Controller.setting import *
from Controller.Common import *
from Controller.NoxConSelenium import NoxConSelenium
from Controller.ControllerManager import Manager

navigator_bar_h = 74
author_area_h = 58  # 评论人顶端区域高度
category_area_h = 75  # 顶端分类：全部，好评，，，  高度
border_size = 128


#################################################################################
class MySelenium(NoxConSelenium):
    def __init__(self, task_info, mode):
        super().__init__(task_info=task_info, mode=mode)

        self.capture_name = 'capture_' + self._docker_name + '.png'
        self.capture_before_name = 'capture_' + self._docker_name + '_before.png'
        self.capture_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_name
        self.capture_before_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_before_name

        self.capture_cut_name = 'capture_' + self._docker_name + '_cut.png'
        self.capture_before_cut_name = 'capture_' + self._docker_name + '_before_cut.png'
        self.capture_cut_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_cut_name
        self.capture_before_cut_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_before_cut_name

        self.capture_concat_name = 'capture_' + self._docker_name + '_concat.png'
        self.capture_concat_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_concat_name

        self.capture_comment_name = 'capture_' + self._docker_name + '_comment.png'
        self.capture_comment_cut_name = 'capture_' + self._docker_name + '_comment_cut.png'
        self.capture_comment_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_comment_name
        self.capture_comment_cut_path = self._work_path + '\\Controller\\images\\temp\\' + self.capture_comment_cut_name

        # border_path = self._work_path + '\\Controller\\images\\dianping\\border.png'
        self.border_path = self._work_path + '\\Controller\\images\\dianping\\border_128_128.png'
        self.page_line_path = self._work_path + '\\Controller\\images\\dianping\\page_line.png'
        self.dafen_path = self._work_path + '\\Controller\\images\\dianping\\dafen.png'

    def get_photo_top_y(self, img_path):
        img_obj = ac.imread(img_path)
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

    def get_page_line_y(self, img_path):
        l = []
        img_obj = cv2.imread(img_path)
        img_border = cv2.imread(self.page_line_path)  # 分页线
        ret = ac.find_all_template(img_obj, img_border, threshold=0.95)
        for r in ret:
            (x, y) = r['result']
            l.append(y)
        if l:
            ret = min(l)
        else:
            ret = -1

        return ret

    def get_comment_top_y(self, img_path):
        l = []
        img_obj = cv2.imread(img_path)
        img_border = cv2.imread(self.dafen_path)  # 打分
        ret = ac.find_all_template(img_obj, img_border, threshold=0.8)
        pprint(ret)
        for r in ret:
            (x, y) = r['result']
            l.append(y)

        if l:
            ret = min(l) + 5
        else:
            ret = -1

        print("打分 y:", ret)
        return ret

    def alignment_page(self, is_first=False):
        # 跳过分类区
        if is_first:
            self.scroll(from_y=140, to_y=10, wait_time=1)
        else:
            line_y = self.get_page_line_y(self.capture_path)
            print('alignment_page', is_first, line_y)
            if line_y != -1:
                self.scroll(from_y=line_y + 10, to_y=navigator_bar_h, wait_time=1)
            else:
                self.goto_next_page()
                # self.alignment_page(is_first=False)

    def concat(self):
        '''
            前后页截图 合成 滚屏效果
        '''
        img_before = Image.open(self.capture_before_path)
        # img_before = img_before.crop((0, 0, SCREEN_WIDTH, 750))
        img_before.save(self.capture_before_cut_path)

        img_current = Image.open(self.capture_path)
        img_current = img_current.crop((0, category_area_h, SCREEN_WIDTH, SCREEN_HEIGHT))  # 切掉导航栏
        img_current.save(self.capture_cut_path)

        # 800 * 480
        img_before = cv2.imread(self.capture_before_cut_path)
        img_current = cv2.imread(self.capture_cut_path)

        # 纵向合成
        img_concat = np.vstack((img_before, img_current))
        cv2.imwrite(self.capture_concat_path, img_concat)

    def cut_comment(self):
        page_line_y = self.get_page_line_y(self.capture_concat_path)
        img = Image.open(self.capture_concat_path)
        if page_line_y != -1:
            img = img.crop((0, 0, SCREEN_WIDTH, page_line_y))

        img.save(self.capture_comment_path)

    def one_page_cut(self, page_line_y):
        '''
            return: self.capture_comment_cut_path
        '''
        cut_y = page_line_y
        photo_top_y = self.get_photo_top_y(self.capture_path)
        if photo_top_y != -1:
            cut_y = photo_top_y - border_size / 2

        img = Image.open(self.capture_path)
        comment_top_y = self.get_comment_top_y(img_path=self.capture_comment_path)
        if comment_top_y == -1:
            img = img.crop((0, navigator_bar_h + author_area_h, SCREEN_WIDTH, cut_y))
        else:
            img = img.crop((0, comment_top_y, SCREEN_WIDTH, cut_y))
        img.save(self.capture_comment_cut_path)

    def two_page_cut(self):
        '''
            return: self.capture_comment_cut_path
        '''
        cut_y = -1
        self.concat()  # 拼接两张图
        self.cut_comment()

        photo_top_y = self.get_photo_top_y(self.capture_comment_path)
        if photo_top_y != -1:
            cut_y = photo_top_y - border_size / 2
        else:
            page_line_y = self.get_page_line_y(self.capture_comment_cut_path)
            if page_line_y != -1:
                cut_y = page_line_y

        img = Image.open(self.capture_comment_path)
        if cut_y != -1:
            comment_top_y = self.get_comment_top_y(img_path=self.capture_comment_path)
            if comment_top_y == -1:
                img = img.crop((0, navigator_bar_h + author_area_h, SCREEN_WIDTH, cut_y))
            else:
                img = img.crop((0, comment_top_y, SCREEN_WIDTH, cut_y))

        img.save(self.capture_comment_cut_path)

    def goto_next_page(self):
        # from_y=SCREEN_HEIGHT(800) 无效
        self.scroll(from_y=SCREEN_HEIGHT - 1, to_y=60, wait_time=1)

    def ocr(self):
        start = datetime.now()
        image = Image.open(self.capture_comment_cut_path)
        code = pytesseract.image_to_string(image, lang='chi_sim')
        print('--------------------------------------------------------------------------\n')
        if code:
            print(code.replace('\n\n', '\n'))
        else:
            print('not found comment')
        print('--------------------------------------------------------------------------\n')
        end = datetime.now()
        print('ocr times:', (end - start).seconds, 's')

    def script(self):
        self.get_capture()
        self.alignment_page(is_first=False)
        ret, x, y = self.find_element(comment='展开全文', timeout=1)
        if ret:
            self.click_xy(x, y, wait_time=1)
            self.get_capture()

        # nox_adb.exe shell input swipe 240 670 240 10 2000
        # nox_adb.exe shell screencap -p /sdcard/capture.png
        # nox_adb.exe pull /sdcard/capture.png c:\Nox\

        is_one_page, _, page_line_y = self.find_element(comment='分页线', timeout=1, threshold=0.95)
        if is_one_page:
            self.one_page_cut(page_line_y)
        else:
            self.goto_next_page()
            self.get_capture()  # 更新截图
            self.two_page_cut()

        self.ocr()
        # self.back()


##################################################################################
def main(task_info, mode):
    msg = ''
    error = ''
    start = datetime.now()
    # common_log(True, task['taskId'], 'Script ' + task['docker_name'], 'start', task)
    try:
        me = MySelenium(task_info=task_info, mode=mode)
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
        if APPSIMULATOR_MODE != 'vmware':  # multi nox mode
            m = Manager()
            m.nox_run_task_finally(taskId)

        common_log(True, task['taskId'], 'Script ' + task['docker_name'] + 'end.',
                   msg + 'total times:' + str((datetime.now() - start).seconds) + 's', error)
        return


#################################################################################
if __name__ == "__main__":
    # APPSIMULATOR_MODE = 'vmware'
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

    main(task_info=task, mode=mode)
    print("Close after 30 seconds.")
    time.sleep(30)
