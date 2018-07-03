# coding=utf8
import os
from datetime import datetime
from ControllerGUI.VMSelenium import VMSelenium


class MySelenium(VMSelenium):
    def __init__(self, nox_name):
        super().__init__(nox_name)

    def script(self):
        try:
            ret = False
            x = -1
            y = -1
            if self.hwnd: ret, x, y = self.find_element(comment='APP图标', timeout=10)  # unlock ok
            if ret: ret = self.click_xy(x, y, wait_times=2)
            while ret:
                if ret: ret, x, y = self.find_element(comment='更新', timeout=30)
                if ret: ret = self.click_xy(x, y, wait_times=1)

                if ret: ret, x, y = self.find_element(comment='分享', timeout=10)
                if ret: ret = self.click_xy(x, y, wait_times=1)

                if ret:
                    ret, x, y = self.find_element(comment='复制链接', timeout=10)
                    if ret:
                        ret = self.click_xy(x, y, wait_times=1)
                    else:
                        print("重试 click 分享 按钮 ...")
                        ret, x, y = self.find_element(comment='分享', timeout=10)
                        if ret: ret = self.click_xy(x, y, wait_times=1)
                        # if ret: ret = self.click("复制链接", wait_times=1)

        except Exception as e:
            self._log('[Script] error:', e)


def main(nox_name):
    start = datetime.now()
    print("[Script] start at ", start)
    try:
        me = MySelenium(nox_name)
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
    main('nox-1')
