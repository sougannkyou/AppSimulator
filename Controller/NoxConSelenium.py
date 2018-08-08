# coding:utf-8
import os
import time
from datetime import datetime
import shutil
import cv2
import aircv as ac
from ftplib import FTP
import win32gui
import pyautogui
from Controller.setting import *
from Controller.Common import common_log
from Controller.NoxConADB import NoxConADB


class NoxConSelenium(NoxConADB):
    '''
    可以使用Timer进行时分同步
    '''

    def __init__(self, task_info, mode):
        super().__init__(task_info, mode)
        self._DEBUG = False
        self._FTP_TRANSMISSION = False
        self._PIC_PATH = {  # set_comment_to_pic()
            "锁屏": 'images\\screen_lock.png',
            "很抱歉": 'images\\im_sorry.png',
            "锁屏图案": 'images\\screen_lock_9point.png',
        }
        self._work_path = WORK_PATH
        self._capture_obj = None
        if mode == 'single':
            self.hwnd = win32gui.FindWindow(None, '夜神模拟器')
        else:
            self.hwnd = None
        self._UNLOCK_POS = {
            "step1": (133, 496),
            "step2": (132, 705),
            "step3": (343, 707)
        }

    def _log(self, prefix, msg):
        common_log(self._DEBUG, self._taskId, 'NoxConSelenium ' + self._docker_name, prefix, msg)

    def set_comment_to_pic(self, value):
        if isinstance(value, dict):
            self._PIC_PATH.update(value)
        else:
            self._log('set_comment_to_pic error:', 'must be set a dictionary')

    def wait_online(self, timeout=10):
        return self.wait_for_device(timeout=timeout)

    def get(self, url, wait_time=5):
        # start android web browser
        self.adb_start_web(url)
        time.sleep(wait_time)
        return True

    def open_settings(self):
        # adb shell am start -n com.android.settings/.Settings
        self.adb_shell("am start -n com.android.settings/.Settings")
        return True

    def get_capture(self):
        capture_default_path = self._work_path + '\\Controller\\images\\temp\\default.png'
        capture_name = 'capture_' + self._docker_name + '.png'
        capture_before_name = 'capture_' + self._docker_name + '_before.png'
        capture_path = self._work_path + '\\Controller\\images\\temp\\' + capture_name
        capture_before_path = self._work_path + '\\Controller\\images\\temp\\' + capture_before_name
        static_capture_path = self._work_path + '\\static\\AppSimulator\\images\\temp\\emulators\\' + capture_name

        if not os.access(capture_before_path, os.R_OK):
            shutil.copy(capture_default_path, capture_before_path)

        if not os.access(capture_path, os.R_OK):
            shutil.copy(capture_default_path, capture_path)
        else:
            modify_t = os.stat(capture_path).st_mtime
            now = datetime.now().timestamp()
            if now - modify_t > 60:
                shutil.copy(capture_default_path, capture_path)
            else:
                shutil.copy(capture_path, capture_before_path)

        # emulator ==> pc temp  可能获取失败
        self.adb_shell("screencap -p /sdcard/" + capture_name)
        self.adb_cmd("pull /sdcard/" + capture_name + " " + self._work_path + '\\Controller\\images\\temp')

        self._capture_obj = ac.imread(capture_path)
        # pc temp ==> pc static
        shutil.copy(capture_path, static_capture_path)

    def find_element(self, comment, timeout, threshold=0.7):
        # True(False), x, y
        img_obj = ac.imread(self._work_path + '\\Controller\\' + self._PIC_PATH[comment])
        while timeout > 0:
            self.get_capture()
            from datetime import datetime
            # start = datetime.now()
            pos = ac.find_template(self._capture_obj, img_obj, threshold=threshold)
            # end = datetime.now()
            # print('find_template', (end - start).microseconds)
            if pos:
                self._log('<<info>> 匹配到：', comment + ' ' + str(timeout) + 's')
                x, y = pos['result']
                return True, x, y
            else:
                time.sleep(1)
                timeout -= 1
                self._log('<<info>> 未匹配：', comment + ' ' + str(timeout) + 's')

        return False, -1, -1

    def find_elements(self, comment, timeout, threshold=0.7):
        ret = []
        img_obj = ac.imread(self._work_path + '\\Controller\\' + self._PIC_PATH[comment])
        self.get_capture()

        while timeout > 0:
            pos_list = ac.find_all_template(self._capture_obj, img_obj, threshold=threshold)
            for pos in pos_list:
                (x, y) = pos['result']
                ret.append((int(x), int(y)))

            if len(ret) > 0:
                self._log('<<info>> 匹配到：' + comment, str(len(ret)) + '个')
                break
            else:
                time.sleep(1)
                timeout -= 1
                self.get_capture()
                self._log('<<info>> 未匹配：', comment + ' ' + str(timeout) + 's')

        return len(ret) > 0, ret

    def next_page_comments(self, wait_time):
        self._log('<<info>> next_page_comments', '翻页')
        # self .clear_cache()
        self.adb_shell("input swipe 300 750 300 350")
        time.sleep(wait_time)
        return True

    def next_page(self, from_x=240, from_y=700, to_x=240, to_y=10, wait_time=2):
        # 480 * 800
        self._log('<<info>> next_page', '翻页')
        # self .clear_cache()
        self.adb_shell("input swipe " + str(from_x) + " " + str(from_y) + " " + str(to_x) + " " + str(to_y) + " 2000")
        time.sleep(wait_time)
        return True

    def next_page_browser(self, wait_time=3):
        self._log('<<info>> next_page_browser', '浏览器翻页')
        # KEYCODE_PAGE_UP = 92
        self.adb_shell("input keyevent 93")  # KEYCODE_PAGE_DOWN = 93
        time.sleep(wait_time)
        return True

    def scroll(self, from_y=700, to_y=10, wait_time=1):
        cmd = "input swipe 240 " + str(int(from_y)) + " 240 " + str(int(to_y)) + " " + str(int((from_y - to_y) * 5))
        self._log('<<info>> scroll', cmd)
        self.adb_shell(cmd)
        time.sleep(wait_time)
        return True

    def _debug(self, x, y, wait_time):
        if not self._DEBUG:
            return

        cv2.circle(img=self._capture_obj, center=(int(x), int(y)), radius=30, color=(0, 255, 0), thickness=2)
        cv2.putText(img=self._capture_obj, text='Click', org=(int(x) - 38, int(y) + 10),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=1)
        cv2.startWindowThread()
        cv2.imshow('Debugger', self._capture_obj)
        cv2.waitKey(wait_time * 1000)
        cv2.destroyAllWindows()
        cv2.waitKey(100)

    def click_xy(self, x, y, wait_time):
        self._debug(x, y, wait_time=2)
        self.adb_shell('input tap ' + str(int(x)) + ' ' + str(int(y)))
        time.sleep(wait_time)
        return True

    def click_xy_timer(self, x, y, wait_time):
        self._debug(x, y, wait_time=2)
        self._timer_flg = True  # NoxConADB adb_cmd_before() on
        self.adb_shell('input tap ' + str(int(x)) + ' ' + str(int(y)))
        self._timer_flg = False  # NoxConADB adb_cmd_before() off
        time.sleep(wait_time)
        return True

    def input(self, text, wait_time):
        self._log('<<info>> input', text)
        self.adb_shell('input text ' + text)
        time.sleep(wait_time)
        return True

    def input_cn(self, text, wait_time=5):
        self._log('<<info>> input_cn', text)
        # adb shell am broadcast -a ADB_INPUT_TEXT --es msg '输入汉字'
        self.adb_shell("am broadcast -a ADB_INPUT_TEXT --es msg '" + text + "'")
        time.sleep(wait_time)
        return True

    def check_upgrade(self, timeout):
        ret, x, y = self.find_element("ignore_upgrade", timeout)
        if ret:
            self._log('<<info>> check_upgrade', 'ignore the upgrade.')
            self.click_xy(x, y, wait_time=2)

        return ret

    def reboot(self, wait_time):
        self.adb_cmd('reboot')
        time.sleep(wait_time)

    def back(self, wait_time=1):
        self._log('back', '')
        self.adb_shell('input keyevent 4')  # KEYCODE_BACK
        time.sleep(wait_time)
        return True

    def app_quit(self, wait_time):
        for i in range(4):
            self._log('app_quit', '')
            self.adb_shell('input keyevent 4')  # KEYCODE_BACK
            time.sleep(wait_time)
        return True

    def __unlock(self, wait_time):
        # self.adb_shell('rm /data/system/*.key')  # rm /data/system/*.key
        # time.sleep(wait_time)
        return True

    def unlock(self, timeout):
        ret, x, y = self.find_element(comment='锁屏', timeout=timeout)
        if not ret:
            return False
        else:
            win32gui.SetForegroundWindow(self.hwnd)
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            top += 20
            time.sleep(1)

            (x, y) = self._UNLOCK_POS['step1']
            x = left + x
            y = top + y
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()

            (x, y) = self._UNLOCK_POS['step2']
            x = left + x
            y = top + y
            # pyautogui.dragTo(x, y, 0.5, button='left')
            pyautogui.moveTo(x, y, 1, pyautogui.easeInQuad)

            (x, y) = self._UNLOCK_POS['step3']
            x = left + x
            y = top + y
            # pyautogui.dragTo(x, y, 0.5, button='left')
            pyautogui.moveTo(x, y, 1, pyautogui.easeInBounce)
            pyautogui.mouseUp()
            time.sleep(1)
            return True

    def ftp_upload(self, capture_name, capture_before_name, mode='mnox'):
        # Controller\images\temp\capture_nox-1.png ->
        # static\AppSimulator(ftp root)\images\temp\mnox(VM)\capture_nox-1.png
        bufsize = 1024  # 设置缓冲器大小
        # task = self._taskId
        if not self._FTP_TRANSMISSION:
            return

        ftp = FTP()
        ftp.connect(FTP_SERVER_IP, 21)
        ftp.login(FTP_USER_NAME, FTP_PASSWORD)
        pwd_path = ftp.pwd()
        self._log('FTP path:', pwd_path)

        fp = open(self._work_path + '\\Controller\\images\\temp\\' + capture_name, 'rb')
        if os.access(self._work_path + '\\Controller\\images\\temp\\' + capture_before_name, os.F_OK):
            fp_before = open(self._work_path + '\\Controller\\images\\temp\\' + capture_before_name, 'rb')
        else:
            fp_before = fp

        # f.set_debuglevel(2)
        if mode == 'vmware':
            remote_dir = 'images/temp/VM'
        else:
            remote_dir = 'images/temp/mnox'

        # try:
        #     ftp.delete(remote_dir + '/' + capture_name)
        #     ftp.delete(remote_dir + '/' + capture_before_name)
        #     ftp.rmd(remote_dir)
        # except Exception as e:
        #     self._log('ftp_upload error:', e)
        #     pass

        # ftp.mkd(remote_dir)
        ftp.storbinary('STOR ' + remote_dir + '/' + capture_name, fp, bufsize)
        ftp.storbinary('STOR ' + remote_dir + '/' + capture_before_name, fp_before, bufsize)
        ftp.set_debuglevel(0)
        ftp.quit()
        fp.close()

    def script(self):
        pass  # overwrite

    def run(self):
        # self.unlock(timeout=10)
        # self.get_new_phone()
        # if ret and is_app_restart:
        #     ret = self.app_quit(wait_time=1)

        self.script()


if __name__ == "__main__":
    task = {
        'taskId': 1,
        'app_name': 'miaopai',
        'docker_name': 'nox-' + str(1),
        'timer_no': 4  # 14s
    }
    me = NoxConSelenium(task, 'single')
    me._FTP_TRANSMISSION = True
    start = time.time()
    me.ftp_upload('capture_nox-1.png', 'capture_nox-1_before.png')
    end = time.time()
    print(end - start)
