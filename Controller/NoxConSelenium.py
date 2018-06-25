# coding:utf-8
import os
import time
import cv2
import aircv as ac
import ftplib
from Controller.NoxConADB import NoxConADB


class NoxConSelenium(object):
    def __init__(self, app_name, docker_name):
        self._DEBUG = False
        self._FTP_TRANSMISSION = False
        self._PIC_PATH = {}  # overwrite
        self._img_capture = None
        self._docker_name = docker_name
        self._app_name = app_name
        self._work_path = os.getenv('APPSIMULATOR_WORK_PATH')
        self._ip = os.getenv('APPSIMULATOR_IP')
        self._adb = NoxConADB(docker_name=docker_name)
        self._adb_port = None

    def _log(self, prefix, msg):
        if self._DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
            print('[NoxConSelenium ' + self._docker_name + ']', prefix, msg)

    def set_comment_to_pic(self, value):
        if isinstance(value, dict):
            self._PIC_PATH = value
        else:
            self._log('set_comment_to_pic error:', 'must be set a dictionary')

    def wait_online(self, timeout=10):
        return self._adb.wait_for_device(timeout=timeout)

    def get(self, url, timeout):
        # start android web browser
        self._adb.start_web(url)
        time.sleep(timeout)
        return True

    def set_gps(self, latitude, longitude):
        return self._adb.set_gps(latitude, longitude)

    def open_settings(self):
        # adb shell am start -n com.android.settings/.Settings
        self._adb.adb_shell("am start -n com.android.settings/.Settings")
        return True

    def find_element(self, comment, timeout):
        # True(False), x, y
        capture_name = "capture_" + self._docker_name + ".png"
        img_obj = ac.imread(self._PIC_PATH[comment])
        while timeout > 0:
            self.get_capture(capture_name)
            pos = ac.find_template(self._img_capture, img_obj)
            if pos and pos['confidence'] > 0.9:
                self._log('<<info>> 匹配到:', comment + ' ' + str(timeout) + 's')
                x, y = pos['result']
                return True, x, y
            else:
                time.sleep(1)
                timeout = timeout - 1
                self._log('<<info>> 未匹配到:', comment + ' ' + str(timeout) + 's')

        return False, -1, -1

    def get_capture(self, capture_name):
        self._adb.adb_shell("screencap -p /sdcard/" + capture_name)
        self._adb.adb_cmd("pull /sdcard/" + capture_name)
        self._img_capture = ac.imread(capture_name)
        self.ftp_upload(local_file=capture_name, remote_dir='172.16.253.36', remote_file=capture_name)

    def find_elements(self, comment, timeout):
        pos_list = []
        capture_name = "capture_" + self._docker_name + ".png"
        img_obj = ac.imread(self._PIC_PATH[comment])
        self.get_capture(capture_name)

        while timeout > 0:
            pos_list = ac.find_all_template(self._img_capture, img_obj)
            for pos in pos_list:
                if pos['confidence'] > 0.9:
                    (x, y) = pos['result']
                    pos_list.append((int(x), int(y)))

            # pprint(pos_list)
            if len(pos_list) > 0:
                self._log('<<info>>匹配到:', str(len(pos_list)) + '件 ' + comment + ' ' + str(timeout) + 's')
                break
            else:
                self._log('<<info>>未匹配:', comment + ' ' + str(timeout) + 's')
                self.get_capture(capture_name)

            timeout = timeout - 1

        return len(pos_list) > 0, pos_list

    def next_page(self, timeout):
        self._log('<<info>> next_page', '翻页')
        self._adb.adb_shell("input swipe 10 400 10 10")
        time.sleep(timeout)
        return True

    def next_page_browser(self, timeout):
        self._log('<<info>> next_page_browser', '浏览器翻页')
        # KEYCODE_PAGE_UP = 92
        self._adb.adb_shell("input keyevent 93")  # KEYCODE_PAGE_DOWN = 93
        time.sleep(timeout)
        return True

    def _debug(self, x, y, timeout):
        if not self._DEBUG:
            return

        cv2.circle(img=self._img_capture, center=(int(x), int(y)), radius=30, color=(0, 0, 255), thickness=1)
        cv2.putText(img=self._img_capture, text='click', org=(int(x) - 40, int(y) + 10),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=1)
        cv2.startWindowThread()
        cv2.imshow('Debugger', self._img_capture)
        cv2.waitKey(timeout * 1000)
        cv2.destroyAllWindows()
        cv2.waitKey(100)

    def click_xy(self, x, y, timeout):
        self._debug(x, y, timeout=2)
        self._adb.adb_shell('input tap ' + str(int(x)) + ' ' + str(int(y)))
        time.sleep(timeout)
        return True

    def input(self, text, timeout):
        self._log('<<info>> input', text)
        self._adb.adb_shell('input text ' + text)
        time.sleep(timeout)
        return True

    def input_cn(self, text, timeout):
        self._log('<<info>> input_cn', text)
        # adb shell am broadcast -a ADB_INPUT_TEXT --es msg '输入汉字'
        self._adb.adb_shell("am broadcast -a ADB_INPUT_TEXT --es msg '" + text + "'")
        time.sleep(timeout)
        return True

    def check_upgrade(self, timeout):
        ret, x, y = self.find_element(u"跳过软件升级", timeout)
        if ret:
            self._log('<<info>> check_upgrade', '版本更新提示 .')
            self.click_xy(x, y, 2)

        return ret

    def reboot(self, timeout):
        self._adb.adb_cmd('reboot')
        time.sleep(timeout)

    def back(self, timeout):
        self._log('back', '')
        self._adb.adb_shell('input keyevent 4')  # KEYCODE_BACK
        time.sleep(timeout)
        return True

    def app_quit(self, timeout):
        for i in range(4):
            self._log('app_quit', '')
            self._adb.adb_shell('input keyevent 4')  # KEYCODE_BACK
            time.sleep(timeout)
        return True

    def unlock(self, timeout):
        self._adb.adb_shell('rm /data/system/*.key')  # rm /data/system/*.key
        time.sleep(timeout)
        return True

    def get_new_phone(self, timeout=1):
        ret = self._adb.get_new_phone()
        time.sleep(timeout)
        return ret

    def ftp_upload(self, local_file, remote_dir, remote_file):
        if not self._FTP_TRANSMISSION: return

        ftp_server_ip = '172.16.3.2'
        username = 'admin'
        password = 'zhxg@2018'

        f = ftplib.FTP(ftp_server_ip)
        f.login(username, password)
        pwd_path = f.pwd()
        self._log('FTP当前路径:', pwd_path)

        bufsize = 1024  # 设置缓冲器大小
        fp = open(local_file, 'rb')
        before_local_file = local_file[:-len('.png')] + '_before.png'
        fp_before = open(before_local_file, 'rb')
        # f.set_debuglevel(2)
        try:
            f.delete(remote_dir + '/' + remote_file)
            f.delete(remote_dir + '/' + remote_file + "_before")
            f.rmd(remote_dir)
        except Exception as e:
            self._log('ftp_upload error:', e)
            pass

        f.mkd(remote_dir)
        f.storbinary('STOR ' + remote_dir + '/' + remote_file, fp, bufsize)
        f.storbinary('STOR ' + remote_dir + '/' + remote_file + "_before", fp_before, bufsize)
        f.set_debuglevel(0)
        fp.close()

    def script(self):
        pass

    def run(self, is_app_restart):
        ret = self.unlock(timeout=1)
        self.get_new_phone(timeout=1)
        if ret and is_app_restart:
            ret = self.app_quit(timeout=1)

        if ret:
            self.script()
