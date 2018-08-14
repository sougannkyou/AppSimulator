import os
# import logging
import subprocess
from datetime import datetime
from Controller.setting import WORK_PATH
from Controller.DBLib import MongoDriver

MDB = MongoDriver()


def common_log(_DEBUG, taskId, func, prefix, msg):
    MDB.log(taskId, func, prefix, msg)
    if _DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
        print(datetime.now().strftime('%H:%M:%S') + ' [' + func + ']', prefix, msg)


def common_exec_cmd(_DEBUG, cmdline):
    _stdout = ''
    _stderr = ''
    try:
        process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # process.wait()
        (stdout, stderr) = process.communicate()
        _stdout = stdout.decode('gbk')
        _stderr = stderr.decode('gbk')
    except Exception as e:
        common_log(_DEBUG, -1, 'common_exec_cmd', 'error', e)
    finally:
        common_log(_DEBUG, -1, 'common_exec_cmd success.\n', cmdline, _stdout)

    if _stderr:
        return ''
    else:
        return _stdout


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
    # common_runscript_countdown()
    _docker_name = 'nox-99'
    # _docker_name = 'nox-1'
    cmd = 'TASKLIST /FI "WINDOWTITLE eq ' + _docker_name + '"'
    ret = common_exec_cmd(True, cmd)
    print(ret.replace('\r\n', '') == '信息: 没有运行的任务匹配指定标准。')
