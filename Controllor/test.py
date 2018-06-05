# coding:utf-8
try:
    import sys
    import time, datetime
    import multiprocessing
    from simulatorADB import Simulator
except ImportError as e:
    print("[Script] ERROR:", e.args[0])
    sys.exit(-1)

ADB_BINARY_PATH = 'C:\\Nox\\bin\\adb.exe'


class MySimulator(Simulator):
    def script(self):
        ret, x, y = self.find_element(comment=u'APP图标', timeout=10)  # unlock ok
        if ret: ret = self.click_xy(x, y, timeout=2)
        while (ret):  # 更新 -> 分享 -> 复制链接
            if ret: ret, x, y = self.find_element(comment=u'更新', timeout=10)
            if ret: ret = self.click_xy(x, y, timeout=1)

            if ret: ret, x, y = self.find_element(comment=u'分享', timeout=10)
            if ret: ret = self.click_xy(x, y, timeout=1)

            if ret:
                ret, x, y = self.find_element(comment=u'复制链接', timeout=10)
                if ret:
                    ret = self.click_xy(x, y, timeout=1)
                else:  # upgrade?
                    # ret = self.check_upgrade(timeout=2)
                    # if ret:
                    print(u"重试 click 分享 按钮 ...")
                    ret, x, y = self.find_element(comment=u'分享', timeout=10)
                    if ret: ret = self.click_xy(x, y, timeout=1)

                    if ret: ret, x, y = self.find_element(comment=u'复制链接', timeout=10)
                    if ret: ret = self.click_xy(x, y, timeout=1)


##################################################################################
def run(idx):
    start = datetime.datetime.now()
    print("[Script" + str(idx) + "] run start.", start)
    try:
        mySimulator = MySimulator(adb_path=ADB_BINARY_PATH, idx=idx)
        mySimulator._PIC_PATH = {
            u"锁屏": 'images/screen_lock.png',
            u"锁屏图案": 'images/screen_lock_9point.png',
            u"APP图标": 'images/douyin/app_icon.png',
            u"更新": 'images/douyin/update.png',
            u"分享": 'images/douyin/share.png',
            u"复制链接": 'images/douyin/copylink.png',
            u"跳过软件升级": 'images/douyin/ignore_upgrade.png',
        }

        # if not ret: self.send2web('images/offline.jpeg')
        mySimulator.run(is_app_restart=True)

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
    for idx in range(2):
        pool.apply_async(run, (idx,))
    pool.close()
    pool.join()
    print("Sub-process(es) done.")
