import sys
import os
import subprocess
from datetime import datetime

sys.path.append(os.getcwd())

# import logging
# -----------------colorama常量---------------------------
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL
from colorama import init, Fore, Back, Style

init(autoreset=True)

from Controller.setting import *
from Controller.DBLib import MongoDriver

MDB = MongoDriver()


class ColorLog(object):
    #  前景色:红色  背景色:默认
    def red(self, s):
        return Fore.RED + str(s) + Fore.RESET

    #  前景色:绿色  背景色:默认
    def green(self, s):
        return Fore.GREEN + str(s) + Fore.RESET

    #  前景色:黄色  背景色:默认
    def yellow(self, s):
        return Fore.YELLOW + str(s) + Fore.RESET

    #  前景色:蓝色  背景色:默认
    def blue(self, s):
        return Fore.BLUE + str(s) + Fore.RESET

    #  前景色:洋红色  背景色:默认
    def magenta(self, s):
        return Fore.MAGENTA + str(s) + Fore.RESET

    #  前景色:青色  背景色:默认
    def cyan(self, s):
        return Fore.CYAN + str(s) + Fore.RESET

    #  前景色:白色  背景色:默认
    def white(self, s):
        return Fore.WHITE + str(s) + Fore.RESET

    #  前景色:黑色  背景色:默认
    def black(self, s):
        return Fore.BLACK

    #  前景色:白色  背景色:绿色
    def white_green(self, s):
        return Fore.WHITE + Back.GREEN + str(s) + Fore.RESET + Back.RESET


def common_log(_DEBUG, taskId, func, prefix, msg):
    if APPSIMULATOR_MODE == MODE_MULTI:
        MDB.log(taskId, func, prefix, msg)

    if _DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
        print("{} [{}]".format(datetime.now().strftime('%H:%M:%S'), func), prefix, msg)


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
        common_log(_DEBUG, -1, '<<<error>>> common_exec_cmd', 'Exception', e)
    finally:
        common_log(_DEBUG, -1, 'common_exec_cmd', cmdline, _stdout)

    if _stderr:
        return ''
    else:
        return _stdout


def __common_runscript_countdown():
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
    # color = Colored()
    # print(color.red('I am red!'))
    # print(color.green('I am gree!'))
    # print(color.yellow('I am yellow!'))
    # print(color.blue('I am blue!'))
    # print(color.magenta('I am magenta!'))
    # print(color.cyan('I am cyan!'))
    # print(color.white('I am white!'))
    # print(color.white_green('I am white green!'))

    # common_runscript_countdown()
    _docker_name = 'nox-99'
    # _docker_name = 'nox-1'
    cmd = 'TASKLIST /FI "WINDOWTITLE eq ' + _docker_name + '"'
    ret = common_exec_cmd(True, cmd)
    print(ret.replace('\r\n', '') == '信息: 没有运行的任务匹配指定标准。')
