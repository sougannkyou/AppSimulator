import time,datetime
from simulator import Simulator

def runScript(deviceId):
    print("[rpc_server] runScript start:",datetime.datetime.now())
    try:
        class MySimulator(Simulator):
            def script(self):
                ret = None
                if self.hwnd: ret = self.find_element(comment='APP图标', timeout=10)  # unlock ok
                if ret: ret = self.click(u"APP图标", timeout=2)
                while (ret):
                    if ret: ret = self.find_element(comment='更新', timeout=10)
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
                    if not ret: self.send2web('images/offline.jpeg')

        mySimulator = MySimulator("douyin0")
        mySimulator._PIC_PATH = {
            u"APP图标": 'images/app_ready.png',
            u"更新": 'images/update.png',
            u"分享": 'images/share.png',
            u"复制链接": 'images/copylink.png',
            u"跳过软件升级": 'images/is_upgrade.png',
            u"锁屏": 'images/screen_lock.png'
        }

        mySimulator._CLICK_POS = {
            u"APP图标": (38, 793),
            u"更新": (38, 793),
            u"分享": (451, 628),
            u"复制链接": (47, 720),
            u"跳过软件升级": (231, 590)  # 以后再说
        }
        mySimulator.run()
        print("[rpc_server] runScript end:", datetime.datetime.now())
        return True
    except Exception as e:
        print("[rpc_server] runScript error:", datetime.datetime.now() ,e)
        return False

if __name__ == "__main__":
    # while(1):
    #     time.sleep(20)
    runScript('')
