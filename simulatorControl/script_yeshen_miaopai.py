# coding=utf8
import datetime
from simulator_yeshen import Simulator


def run():
    start = datetime.datetime.now()
    print("[script] run start ...", start)
    try:
        class MySimulator(Simulator):
            DEBUG_ENV = False

            def script(self):
                ret = None
                x = -1
                y = -1
                if self.hwnd: ret, x, y = self.find_element(comment='APP图标', timeout=10)  # unlock ok
                if ret: ret = self.click_xy(x, y, timeout=2)
                while (ret):
                    if ret: ret, x, y = self.find_element(comment='更新', timeout=30)
                    if ret: ret = self.click_xy(x, y, timeout=1)

                    if ret: ret, x, y = self.find_element(comment='分享', timeout=10)
                    if ret: ret = self.click_xy(x, y, timeout=1)

                    if ret:
                        ret, x, y = self.find_element(comment='复制链接', timeout=10)
                        if ret:
                            ret = self.click_xy(x, y, timeout=1)
                        else:
                            print("重试 click 分享 按钮 ...")
                            ret, x, y = self.find_element(comment='分享', timeout=10)
                            if ret: ret = self.click_xy(x, y, timeout=1)

                    # if not ret: self.send2web('images/offline.jpeg')

        mySimulator = MySimulator("simulator")
        mySimulator._PIC_PATH = {
            u"锁屏": 'images_yeshen/screen_lock.png',
            u"锁屏图案": 'images_yeshen/screen_lock_6_1.png',
            u"APP图标": 'images_yeshen/miaopai/app_icon.png',
            u"更新": 'images_yeshen/miaopai/update.png',
            u"分享": 'images_yeshen/miaopai/share.png',
            u"复制链接": 'images_yeshen/miaopai/copylink.png',
            u"跳过软件升级": 'images_yeshen/miaopai/is_upgrade.png',
        }

        mySimulator._CLICK_POS = {
            u"APP图标": (38, 793),
            u"更新": (38, 793),
            u"分享": (451, 628),
            u"复制链接": (47, 720),
            u"跳过软件升级": (231, 590)  # 以后再说
        }

        mySimulator.run()
        end = datetime.datetime.now()
        print("[script] run script success.", (end - start).seconds)
        return True
    except Exception as e:
        end = datetime.datetime.now()
        print("[script] run script error:", (end - start).seconds, e)
        return False


if __name__ == "__main__":
    run()
