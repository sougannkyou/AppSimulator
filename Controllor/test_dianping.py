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

urls = [
    "http://www.dianping.com/shop/24981944",  # 936
    "http://www.dianping.com/shop/18385524",  #
    "http://www.dianping.com/shop/98535009",  # 深夜食堂
    "http://www.dianping.com/shop/72459852",  # 1061
]

keywords = [
    '匹夫涮肉城 黄村店',
    '鲜牛记潮汕牛肉火锅 亚运村店',
    '海底捞火锅(大屯北路店)'
]


class MySimulator(Simulator):
    def script(self):
        # self.start_web(urls[self._adb_idx], 3)
        # ret, x, y = self.find_element(comment='web打开APP', timeout=10)
        # if ret: ret = self.click_xy(x, y, timeout=2)
        ret = True
        x = -1
        y = -1

        ret, x, y = self.find_element(comment='APP图标', timeout=10)
        if ret: ret = self.click_xy(x, y, timeout=2)
        if ret: ret, x, y = self.find_element(comment='附近热搜', timeout=5)
        if ret: ret = self.click_xy(x, y, timeout=1)
        time.sleep(3)
        if ret: ret = self.input_cn(keywords[self._adb_idx], timeout=1)
        time.sleep(5)
        if ret: ret, x, y = self.find_element(comment='搜索', timeout=5)
        if ret: ret = self.click_xy(x, y + 30, timeout=1)

        ret, x, y = self.find_element(comment='APP打开结果OK', timeout=60)
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
            # "web打开APP": 'images/dianping/webOpenApp.png',
            # "APP打开结果OK": 'images/dianping/search_ready.png',
            "APP图标": 'images/dianping/app_icon.png',
            '附近热搜': 'images/dianping/search.png',
            '搜索': 'images/dianping/search_btn.png',
            "网友点评": 'images/dianping/wangyoudianping.png',
            "全部网友点评": 'images/dianping/wangyoudianping-all.png',
            "分享": 'images/dianping/share.png',
            "复制链接": 'images/dianping/copy_link.png',
            "打分": 'images/dianping/dafen.png',
        }
        mySimulator._DEBUG = False
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


# run()


if __name__ == "__main__":
    devices_cnt = 3
    pool = multiprocessing.Pool(processes=4)
    for idx in range(devices_cnt):
        pool.apply_async(run, (idx,))
    pool.close()
    pool.join()
    print("Sub-process(es) done.")
