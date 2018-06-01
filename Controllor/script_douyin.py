# coding=utf8
import os
import datetime
from simulator_yeshen  import Simulator


def run():
    start = datetime.datetime.now()
    print("[script] run start ...", start)
    try:
        class MySimulator(Simulator):
            def script(self):
                ret = None
                if self.hwnd: ret = self.find_element(comment='APP图标', timeout=10)  # unlock ok
                if ret: ret = self.click(u"APP图标", timeout=2)
                while (ret):
                    if ret: ret = self.find_element(comment='更新', timeout=30)
                    if ret: ret = self.click(u"更新", timeout=1)

                    if ret: ret = self.find_element(comment='分享', timeout=10)
                    if ret: ret = self.click(u"分享", timeout=1)

                    if ret:
                        ret = self.find_element(comment='复制链接', timeout=10)
                        if not ret:
                            print("重试 click 分享 按钮 ...")
                            ret = self.find_element(comment='分享', timeout=10)
                            if ret: ret = self.click(u"分享", timeout=1)

                    if ret: ret = self.click(u"复制链接", timeout=1)
                    # if not ret: self.send2web('images_yeshen/offline.jpeg')

        mySimulator = MySimulator("simulator")
        mySimulator._PIC_PATH = {
            u"APP图标": 'images_yeshen/douyin/app_icon.png',
            u"更新": 'images_yeshen/douyin/update.png',
            u"分享": 'images_yeshen/douyin/share.png',
            u"复制链接": 'images_yeshen/douyin/copylink.png',
            u"跳过软件升级": 'images_yeshen/douyin/is_upgrade.png',
            u"锁屏": 'images_yeshen/screen_lock.png'
        }

        mySimulator._CLICK_POS = {
            u"APP图标": (38, 793),
            u"更新": (68, 793),
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
