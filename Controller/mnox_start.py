# coding:utf-8
import os
import sys

sys.path.append(os.getcwd())

import multiprocessing
from Controller.setting import *
from Controller.Common import common_log
from Controller.ControllerManager import Manager

_DEBUG = True


# ------------------------------------------------------------------------------------------
def _log(prefix, msg):
    common_log(_DEBUG, '', 'Multi Nox start', prefix, msg)


def mnox_test(vm):
    manager = Manager()
    manager._DEBUG = True
    manager._mdb._DEBUG = True
    # t = {
    #     'taskId': 2,
    #     'app_name': 'miaopai',
    #     'docker_name': 'nox-2',
    #     'timer_no': 2,
    #     'script': 'script_miaopai.py'
    # }
    # manager.run_script(task_info=t)
    # manager.start_tasks()
    # manager.vm_draw_cardiogram()
    # manager.vm_reset(vm_name='vm4')
    # host_ip = '172.16.253.37'
    return


def mnox_main():
    manager = Manager()
    manager._DEBUG = True
    manager.nox_run_tasks()


# ------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # mnox_test()
    mnox_main()
