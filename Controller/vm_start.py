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
    common_log(_DEBUG, '', 'VM start', prefix, msg)


def vm_draw_cardiogram(host_ip):
    _log('vm_draw_cardiogram', 'start ...')
    manager = Manager()
    manager._DEBUG = True
    manager._mdb._DEBUG = True
    manager.vm_draw_cardiogram(host_ip)
    _log('vm_draw_cardiogram', 'end.')


def vm_check_active(host_ip):
    _log('vm_check_active', 'start ...')
    manager = Manager()
    manager._DEBUG = True
    manager._mdb._DEBUG = True
    manager.vm_check_active(host_ip)
    _log('vm_check_active', 'end.')


def vm_test(vm):
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
    manager.vm_reset(vm)  # vm3 vm4
    return


def vm_main():
    host_ip = os.getenv('APPSIMULATOR_IP')
    if not host_ip:
        _log('vm_main', 'Undefined APPSIMULATOR_IP')
    else:
        _log('vm_main', host_ip + ' start ...')
        numList = []
        p1 = multiprocessing.Process(target=vm_draw_cardiogram, args=(host_ip,))
        numList.append(p1)
        p1.start()

        p2 = multiprocessing.Process(target=vm_check_active, args=(host_ip,))
        numList.append(p2)
        p2.start()

        p1.join()
        _log('vm_main', 'draw_cardiogram end.')
        p2.join()
        _log('vm_main', 'check end.')

    _log('vm_main', host_ip + ' all end.')
    return


# ------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # vm_test()
    vm_main()
