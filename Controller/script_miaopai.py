# coding:utf-8
import time
from datetime import datetime
from Controller.NoxConSelenium import NoxConSelenium

urls = [
    "http://www.miaopai.com/show/6NWi1Bp5fx9GV0tdwCUGYWNzaQm9hVJe.htm",  # 936
]


class MySelenium(NoxConSelenium):
    def script(self):
        # self.get(urls[0], 5)
        # ret, x, y = self.find_element(comment='web打开APP', timeout=10)
        # if ret: ret = self.click_xy(x, y, timeout=2)
        try:
            ret, x, y = self.find_element(comment='app_icon', timeout=10)  # unlock ok
            if ret:
                ret = self.click_xy(x, y, timeout=2)

            while ret:
                ret, pos_list = self.find_elements(comment='share', timeout=10)
                if ret:
                    for pos in pos_list:
                        (x, y) = pos
                        ret = self.click_xy(x, y, timeout=2)
                        if ret:
                            ret, x, y = self.find_element(comment='copylink', timeout=10)
                            if ret:
                                ret = self.click_xy(x, y, timeout=1, time_recoder=True)
                            else:  # upgrade?
                                # ret = self.check_upgrade(timeout=2)
                                # if ret:
                                # print(u"重试 click 分享 按钮 ...")
                                ret, x, y = self.find_element(comment='share', timeout=10)
                                if ret: ret = self.click_xy(x, y, timeout=1)

                                if ret: ret, x, y = self.find_element(comment='copylink', timeout=10)
                                if ret: ret = self.click_xy(x, y, timeout=1)

                self.next_page(timeout=5)

        except Exception as e:
            self._log('error:', e)


##################################################################################
def main(docker_name):
    start = datetime.now()
    print("[Script " + docker_name + "] start at ", start)
    try:
        me = MySelenium(docker_name=docker_name, app_name='miaopai')
        me.set_comment_to_pic({
            "app_icon": 'images/miaopai/app_icon.png',
            "update": 'images/miaopai/update.png',
            "share": 'images/miaopai/share.png',
            "copylink": 'images/miaopai/copylink.png',
            "ignore_upgrade": 'images/miaopai/ignore_upgrade.png',
        })
        # me._DEBUG = True
        me.run(is_app_restart=True)
        end = datetime.now()
        print("[Script " + docker_name + "] total times:", (end - start).seconds, "s")
        return True
    except Exception as e:
        end = datetime.now()
        print("[Script " + docker_name + "] total times:", (end - start).seconds, "s error:", e)
        return False


if __name__ == "__main__":
    # docker_name = sys.argv[1]
    docker_name = 'nox-2'
    main(docker_name)
    print("Close after 60 seconds.")
    time.sleep(60)
