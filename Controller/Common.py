import os
# import logging
from datetime import datetime
from Controller.setting import WORK_PATH
from Controller.DBLib import MongoDriver

MDB = MongoDriver()


def common_log(_DEBUG, taskId, func, prefix, msg):
    MDB.log(taskId, func, prefix, msg)
    if _DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
        print(datetime.now().strftime('%H:%M:%S') + ' [' + func + ']', prefix, msg)


def common_runscript_countdown():
    try:
        conf_path = WORK_PATH + '\cmd\\NoxResetCounter.conf'
        f = open(conf_path, 'r')
        cnt = f.readline()
        common_log(True, '', 'common_runscript_countdown', 'counter', cnt)
        if int(cnt) > 0:
            n = open(conf_path, 'w')
            n.write(str(int(cnt) - 1))
            n.close()
            os.system('%APPSIMULATOR_WORK_PATH%\cmd\StartScript.cmd')

    except Exception as e:
        common_log(True, '', 'common_runscript_countdown', 'error', e)
    finally:
        f.close()


if __name__ == "__main__":
    common_runscript_countdown()
