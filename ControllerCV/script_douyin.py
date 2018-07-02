# coding=utf8
import os
from datetime import datetime
from ControllerCV.GUISelenium import GUISelenium


class MySelenium(GUISelenium):
    def __init__(self):
        super().__init__()

    def script(self):
        try:
            ret = None
            if self.hwnd: ret = self.find_element(comment='APP图标', timeout=10)  # unlock ok
            if ret: ret = self.click(u"APP图标", wait_times=2)
            while ret:
                if ret: ret = self.find_element(comment='更新', timeout=30)
                if ret: ret = self.click(u"更新", wait_times=1)

                if ret: ret = self.find_element(comment='分享', timeout=10)
                if ret: ret = self.click(u"分享", wait_times=1)

                if ret:
                    ret = self.find_element(comment='复制链接', timeout=10)
                    if not ret:
                        print("重试 click 分享 按钮 ...")
                        ret = self.find_element(comment='分享', timeout=10)
                        if ret: ret = self.click(u"分享", wait_times=1)

                if ret: ret = self.click(u"复制链接", wait_times=1)

        except Exception as e:
            self._log('error:', e)


def main():
    start = datetime.now()
    print("[Script] start at ", start)
    try:
        me = MySelenium()
        me.set_comment_to_pic({
            "锁屏": 'images/screen_lock.png',
            "APP图标": 'images/douyin/app_icon.png',
            "更新": 'images/douyin/update.png',
            "分享": 'images/douyin/share.png',
            "复制链接": 'images/douyin/copylink.png',
            "跳过软件升级": 'images/douyin/is_upgrade.png',
        })

        me._CLICK_POS = {
            "APP图标": (38, 793),
            "更新": (68, 793),
            "分享": (451, 628),
            "复制链接": (47, 720),
            "跳过软件升级": (231, 590)  # 以后再说
        }
        me.run()
        # me._DEBUG = True
        end = datetime.now()
        print("[Script] total times:", str((end - start).seconds) + "s")
        return True
    except Exception as e:
        end = datetime.now()
        print("[Script] total times:", str((end - start).seconds) + "s\nerror:", e)
        return False


if __name__ == "__main__":
    main()
