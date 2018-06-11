# coding:utf-8
try:
    import sys
    from pprint import pprint
    import time
    import datetime
    import multiprocessing
    import win32gui
    from PIL import ImageGrab
    import cv2
    import aircv as ac
    import pyautogui
    from simulatorADB import Simulator
    from EmulatorNox import Emulator

except ImportError as e:
    print("[Script] ERROR:", e.args[0])
    sys.exit(-1)

ADB_BINARY_PATH = 'C:\\Nox\\bin\\adb.exe'

urls = [
    "https://m.toutiaocdn.cn/group/6565684301512311300/?iid=14592851837&app=news_article&timestamp=1528703355&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
    "http://m.toutiaocdn.cn/group/6563987941163532803/?iid=14592851837&app=news_article&timestamp=1528341722&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
    "https://m.toutiaocdn.cn/group/6565632060814262792/?iid=14592851837&app=news_article&timestamp=1528702278&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
    "http://m.toutiaocdn.cn/group/6563914570526622216/?iid=14592851837&app=news_article&timestamp=1528341946&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
    "http://m.toutiaocdn.cn/group/6563778505752969741/?iid=14592851837&app=news_article&timestamp=1528267671&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
    "http://m.toutiaocdn.cn/group/6563793627670118919/?iid=14592851837&app=news_article&timestamp=1528277350&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share",
]

comments = [
    "!?",
    "转发了2",
    "转发了3",
    "转发了4",
]


# def next_page(window_title, timeout):
#     # 10 400 -> 10 10
#     hwnd = win32gui.FindWindow(None, window_title)
#     if not hwnd:
#         return False
#
#     # win32gui.SetForegroundWindow(hwnd)
#     left, top, right, bottom = win32gui.GetWindowRect(hwnd)
#     top += 20
#     time.sleep(timeout)
#
#     (x, y) = (10, 400)
#     x = left + x
#     y = top + y
#     pyautogui.moveTo(x, y)
#     pyautogui.mouseDown()
#
#     (x, y) = (10, 10)
#     x = left + x
#     y = top + y
#     pyautogui.dragTo(x, y, 0.5, button='left')
#     # pyautogui.moveTo(x, y, 1, pyautogui.easeInQuad)
#
#     # pyautogui.mouseUp()
#     time.sleep(timeout)
#     return True


class MySimulator(Simulator):
    def script(self):
        ret = True
        x = -1
        y = -1
        page_cnt = 0
        self.start_web(urls[self._adb_idx], 5)
        ret, x, y = self.find_element(comment='打开APP', timeout=5)
        if ret:
            ret = self.click_xy(x, y, timeout=2)
        else:
            # ret = self.next_page(timeout=1)
            ret = self.next_page_browser(1)
            ret, x, y = self.find_element(comment='打开APP', timeout=10)
            if ret:
                ret = self.click_xy(x, y, timeout=2)
            else:
                # ret = self.next_page(timeout=1)
                ret = self.next_page_browser(1)
                ret, x, y = self.find_element(comment='打开APP', timeout=10)
                if ret: ret = self.click_xy(x, y, timeout=2)

        ret, x, y = self.find_element(comment='写评论', timeout=5)
        if ret: ret = self.click_xy(x, y, timeout=2)
        if ret: ret = self.input_cn(comments[self._adb_idx], timeout=1)
        time.sleep(5)
        if ret: ret, x, y = self.find_element(comment='发布', timeout=5)
        if ret: ret = self.click_xy(x, y, timeout=1)


##################################################################################
def run(idx):
    start = datetime.datetime.now()
    print("[Script" + str(idx) + "] run start.", start)
    try:
        mySimulator = MySimulator(adb_path=ADB_BINARY_PATH, idx=idx)
        mySimulator._PIC_PATH = {
            "打开APP": 'images/toutiao/jump2app.png',
            "写评论": 'images/toutiao/writeComment.png',
            "发布": 'images/toutiao/publish.png',
        }
        mySimulator._DEBUG = True
        mySimulator._adb._DEBUG = False
        # if not ret: self.send2web('images/offline.jpeg')
        mySimulator.set_gps(39.984727, 116.310050)  # 中关村
        mySimulator.run(is_app_restart=False)

        end = datetime.datetime.now()
        print("[Script" + str(idx) + "] run success. ", (end - start).seconds, "s")
        return True
    except Exception as e:
        end = datetime.datetime.now()
        print("[Script" + str(idx) + "] ERROR:", (end - start).seconds, e)
        return False


#################################################################################
if __name__ == "__main__":
    # tasks_cnt = int(sys.argv[1])
    tasks_cnt = 1
    # emulator = Emulator('dianping')
    # for i in range(1, 1 + tasks_cnt):
    #     print('launch_emulator nox-' + str(i))
    #     emulator.launch_emulator('nox-' + str(i), force=True)
    #
    # time.sleep(30)

    pool = multiprocessing.Pool(processes=4)
    for idx in range(tasks_cnt):
        pool.apply_async(run, (idx,))
    pool.close()
    pool.join()
    print("process done.")
