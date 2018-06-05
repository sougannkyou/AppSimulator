# coding:utf-8
try:
    import sys
    from pprint import pprint
    import time
    import datetime
    import multiprocessing
    from simulatorADB import Simulator
except ImportError as e:
    print("[Script] ERROR:", e.args[0])
    sys.exit(-1)

ADB_BINARY_PATH = 'C:\\Nox\\bin\\adb.exe'


class MySimulator(Simulator):
    def script(self):
        url = "http://www.dianping.com/shop/98535009"
        self.start_web(url, 3)
        ret, x, y = self.find_element(comment='web打开APP', timeout=10)
        if ret: ret = self.click_xy(x, y, timeout=2)
        ret, x, y = self.find_element(comment='APP打开结果OK', timeout=60)
        # return
        # ret, x, y = self.find_element(comment='APP图标', timeout=10)
        # if ret: ret = self.click_xy(x, y, timeout=2)
        # if ret: ret, x, y = self.find_element(comment='美食', timeout=5)
        # if ret: ret = self.click_xy(x, y, timeout=1)
        # if ret: ret, x, y = self.find_element(comment='查找', timeout=5)
        # if ret: ret = self.click_xy(x, y, timeout=1)
        # if ret: ret, x, y = self.find_element(comment='查找', timeout=5)
        # if ret: ret = self.input('深夜食堂', timeout=1)
        # if ret: ret, x, y = self.find_element(comment='搜索', timeout=5)
        # if ret: ret = self.click_xy(x, y, timeout=1)
        find = False
        pos_list = []
        for i in range(5):
            ret, x, y = self.find_element(comment='全部网友点评', timeout=5)
            if ret:
                find = True
                ret = self.click_xy(x, y, timeout=1)
                break
            else:
                ret = self.next_page(timeout=1)

        while find and ret:
            if ret:
                ret, pos_list = self.find_elements(comment='打分', timeout=10)
                if not ret:
                    ret = self.next_page(timeout=1)

            for pos in pos_list:
                (x, y) = pos
                if ret: ret = self.click_xy(x, y, timeout=1)
                if ret: ret, x, y = self.find_element(comment='分享', timeout=10)
                if ret: ret = self.click_xy(x, y, timeout=1)
                if ret: ret, x, y = self.find_element(comment='复制链接', timeout=10)
                if ret: ret = self.click_xy(x, y, timeout=1)
                if ret: ret = self.back(timeout=1)

            if ret: ret = self.next_page(timeout=1)


##################################################################################
def run(idx):
    start = datetime.datetime.now()
    print("[Script" + str(idx) + "] run start.", start)
    try:
        mySimulator = MySimulator(adb_path=ADB_BINARY_PATH, idx=idx)
        mySimulator._PIC_PATH = {
            "锁屏": 'images/screen_lock.png',
            "锁屏图案": 'images/screen_lock_9point.png',
            "web打开APP": 'images/dianping/webOpenApp.png',
            "APP打开结果OK": 'images/dianping/search_ready.png',
            "APP图标": 'images/dianping/app_icon.png',
            '美食': 'images/dianping/meishi.png',
            '查找': 'images/dianping/search.png',
            '搜索': 'images/dianping/search_btn.png',
            "网友点评": 'images/dianping/wangyoudianping.png',
            "全部网友点评": 'images/dianping/wangyoudianping-all.png',
            "分享": 'images/dianping/share.png',
            "复制链接": 'images/dianping/copy_link.png',
            "打分": 'images/dianping/dafen.png',
        }
        mySimulator._DEBUG = True
        # if not ret: self.send2web('images/offline.jpeg')
        mySimulator.set_gps(39.984727, 116.310050)
        mySimulator.run(is_app_restart=False)

        end = datetime.datetime.now()
        print("[Script" + str(idx) + "] run success. ", (end - start).seconds, "s")
        return True
    except Exception as e:
        end = datetime.datetime.now()
        print("[Script" + str(idx) + "] ERROR:", (end - start).seconds, e)
        return False


# run()


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)
    for idx in range(1):
        pool.apply_async(run, (idx,))
    pool.close()
    pool.join()
    print("Sub-process(es) done.")
