# coding:utf-8
import os
import time
import subprocess
import multiprocessing
from pprint import pprint
from datetime import datetime
import importlib
import importlib.util
import win32gui
from Controller.setting import *
from Controller.DBLib import MongoDriver, RedisDriver
from Controller.NoxConDocker import NoxConDocker
from Controller.NoxConSelenium import NoxConSelenium

_DEBUG = True


# ------------------------ task manager ----------------------
class Manager(object):
    def __init__(self):
        self._rds = RedisDriver()
        self._mdb = MongoDriver()
        self._mdb._DEBUG = False
        self._DEBUG = False
        self._work_path = WORK_PATH

    def _log(self, prefix, msg):
        if self._DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
            print('[' + datetime.now().strftime('%H:%M:%S') + ' Controller Manager]', prefix, msg)

    def _check(self):
        if not self._work_path:
            msg = '请设置: APPSIMULATOR_WORK_PATH'
            self._log('_check error', msg)
            return False, msg

    def run_script1(self, task_info):
        _stdout = ''
        _stderr = ''
        try:
            docker_name = 'nox-' + str(task_info['taskId'])
            # cmdline = 'START "task-' + str(task_info['taskId']) + '" '
            cmdline = 'python ' + self._work_path + '\Controller\\' + task_info['script']  # + ' ' + docker_name
            self._log('run_task', cmdline)
            time.sleep(1)
            process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # process.wait()
            (stdout, stderr) = process.communicate()
            _stdout = stdout.decode('utf8')
            _stderr = stderr.decode('utf8')
        except Exception as e:
            self._log('<<error>> run_script:', e)

        if _stderr:
            self._log('run_script stderr:\n', _stderr)
            return False
        else:
            self._log('run_script stdout:\n', _stdout)
            time.sleep(1)
            return True

    def run_script2(self, task, docker_name):
        try:
            script = 'Controller.' + task['script'][:-3]
            importlib.invalidate_caches()
            module = importlib.import_module(script)
            # importlib.reload(module)
            module.main(docker_name)
            self._log('<<info>> run_script ok', script)
            return True
        except Exception as e:
            self._log('run_script error:', e)
            return False

    def run_script(self, task_info):
        try:
            from pprint import pprint
            import os
            # cd _work_path (D:\workspace\pyWork\AppSimulator>)
            # python Controller\script_miaopai.py
            p = os.getcwd()
            import sys

            if p not in sys.path:
                print('append', p)
                sys.path.append(p)

            pprint(sys.path)
            docker_name = 'nox-' + str(task_info['taskId'])
            # cmd = 'python --version'
            cmd = 'START "task-' + str(task_info['taskId']) + '" '
            cmd += 'python ' + self._work_path + '\Controller\\' + task_info['script'] + ' ' + docker_name
            # cmd += ' >>' + self._work_path + '\Controller\log\\task-' + str(task['taskId']) + '.log 2>&1'
            self._log('<<info>> run_script cmd:\n', cmd)
            os.system(cmd)
            # print(os.popen(cmd).read())
            return True
        except Exception as e:
            self._log('run_script error:', e)
            return False

    def docker_run(self, task, docker, retry_cnt):
        docker.stop()
        self.check_docker_stop(docker, retry=True, wait_time=30)
        ret = docker.run(force=True)  # docker run: create and start
        if ret:
            ret = self.docker_run_check(task_info=task, timeout=60)
            if ret:
                ret = self.docker_run_success(docker=docker)
            else:
                ret = self.docker_run_error(task=task, docker=docker, retry_cnt=retry_cnt)

        return ret

    def docker_run_success(self, docker):
        self._log('<<info>> docker_run_success', docker.get_name())
        time.sleep(2)
        docker.shake(1)
        # docker.set_docker_name()
        # port = docker.get_port()
        return True

    def docker_run_error(self, task, docker, retry_cnt):
        self._log('<<info>> docker_run_error:', docker.get_name() + ' retry: ' + str(retry_cnt))
        retry_cnt -= 1
        if retry_cnt >= 0:
            return self.docker_run(task, docker, retry_cnt)

        return False

    def docker_run_check(self, task_info, timeout=60):
        driver = NoxConSelenium(task_info=task_info)
        driver.set_comment_to_pic({
            "APP图标": self._work_path + '\\Controller\\images\\' + task_info['app_name'] + '\\app_icon.png',
            "很抱歉": self._work_path + '\\Controller\\images\\im_sorry.png',
        })
        docker_name = 'nox-' + str(task_info['taskId'])
        ret = driver.wait_online(timeout=timeout)
        if ret:
            ret, x, y = driver.find_element(comment='很抱歉', timeout=10)  # 匹配到“很抱歉”字样
            if ret:
                self._log('<<info>> check_docker_run', task_info['docker_name'] + ' 匹配到“很抱歉”.')
                return False
            else:
                ret, x, y = driver.find_element(comment='APP图标', timeout=10)  # 可匹配到app图标
                if ret:
                    self._log('<<info>> check_docker_run', docker_name + ' 可匹配到app图标.')
                else:
                    self._log('<<info>> check_docker_run', docker_name + ' 未匹配到app图标.')

                return ret

    def check_docker_stop(self, docker, retry=False, wait_time=30):
        while wait_time > 0:
            hwnd = win32gui.FindWindow(None, docker.get_name())
            if hwnd:  # hwnd is 0 if not found
                time.sleep(1)
                self._log('<<info>> check_docker_stop', '正在等待 ' + docker.get_name() + ' 停止，剩余：' + str(wait_time) + 's')
                wait_time -= 1
            else:  # not found the window
                self._log('<<info>> check_docker_stop', '已停止：' + str(wait_time) + 's')
                break

        if retry and wait_time == 0:  # retry
            # docker._cmd_kill_task(self._docker_name)  # 不能强杀，会造成 ERR：1037
            docker.stop()

        time.sleep(10)
        return True

    def start_tasks(self):
        # 1)docker running -> 2)docker run ok(ng) -> 3)script running -> 4)script run ok(ng)
        while True:
            task, msg = self._mdb.task_get_one_for_run()
            if task:
                # 1)docker running
                task['status'] = STATUS_DOCKER_RUN
                self._mdb.task_change_status(task)
                docker = NoxConDocker(task_info=task)
                ret = self.docker_run(task=task, docker=docker, retry_cnt=2)
                # call NoxConDocker.__del__
                # docker = None

                status = STATUS_DOCKER_RUN_OK if ret else STATUS_DOCKER_RUN_NG

                # 2)docker run ok(ng)
                docker_info = {'_id': self._mdb.docker_create(task), 'status': status}
                self._mdb.docker_change_status(docker_info)
                task['status'] = status
                self._mdb.task_change_status(task)

                if ret:
                    self._mdb.task_set_docker(task, docker_info)  # bind docker to task
                    # 3)script running
                    ret = self.run_script(task_info=task)
                    task['status'] = STATUS_SCRIPT_START_OK if ret else STATUS_SCRIPT_START_NG

                    # 4)script run ok(ng)
                    self._mdb.task_change_status(task)

                # break
            else:
                self._log('<<info>> start_tasks', 'not found waiting task, retry after 60s.')
                time.sleep(1 * 60)

    def vm_draw_cardiogram(self, host_ip):
        while True:
            vmwares = self._mdb.vm_find_vm_by_host(host_ip)
            for vm in vmwares:
                cnt = self._rds.get_vmware_crwal_cnt(vm)
                vm['cnt'] = cnt
                vm['dedup_cnt'] = cnt
                self._mdb.vm_record_share_cnt(vm_info=vm, scope_times=10 * 60)

            if vmwares:
                self._log('vm_draw_cardiogram', 'vmware:' + str(len(vmwares)))
                time.sleep(60)
            else:
                self._log('vm_draw_cardiogram:', 'not found vmware.')
                break

    def vm_reset(self, vm_name):
        try:
            self._log('vm_reset start:', vm_name)
            work_path = os.getenv('APPSIMULATOR_WORK_PATH')
            cmd = work_path + '\cmd\VMReset.cmd ' + vm_name
            print('vm_reset', cmd)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # process.wait()
            (stdout, stderr) = process.communicate()
            _stdout = stdout.decode('utf8')
            _stderr = stderr.decode('utf8')
            print('stdout:', _stdout)
            print('stderr:', _stderr)
            self._log('vm_reset end:', vm_name)
            return True
        except Exception as e:
            self._log('vm_reset error:', e)
            return False

    def vm_check_active(self, host_ip):
        while True:
            vmwares = self._mdb.vm_find_vm_by_host(host_ip)
            for vm in vmwares:
                crwal_cnt_list = self._mdb.vm_get_crwal_cnt(vm['ip'])
                if len(crwal_cnt_list) >= CHECK_TIMES and crwal_cnt_list[-1] > 0:
                    self._log('vm_check_active ' + vm['ip'], crwal_cnt_list)
                    if crwal_cnt_list[0] == crwal_cnt_list[-1]:  # 无增长记录
                        self._log('vm_check_active', vm['ip'] + ': suspend tobe reset')
                        self.vm_reset(vm['name'])
                    else:
                        self._log('vm_check_active', vm['ip'] + ': running')

            time.sleep(CHECK_TIMES * 60)


# ------------------------------------------------------------------------------------------
def _log(prefix, msg):
    if _DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
        print('[' + datetime.now().strftime('%H:%M:%S') + ' Controller Process]', prefix, msg)


def start_tasks():
    pass


def draw_cardiogram(host_ip):
    _log('draw_cardiogram', 'start ...')
    manager = Manager()
    manager._DEBUG = True
    manager._mdb._DEBUG = True
    manager.vm_draw_cardiogram(host_ip)
    _log('draw_cardiogram', 'end.')


def check(host_ip):
    _log('check', 'start ...')
    manager = Manager()
    manager._DEBUG = True
    manager._mdb._DEBUG = True
    manager.vm_check_active(host_ip)
    _log('check', 'end.')


def main():
    _log('main', 'start ...')
    host_ip = os.getenv('APPSIMULATOR_IP')
    if not host_ip:
        _log('main', 'Undefined APPSIMULATOR_IP')
    else:
        numList = []
        p1 = multiprocessing.Process(target=draw_cardiogram, args=(host_ip,))
        numList.append(p1)
        p1.start()

        p2 = multiprocessing.Process(target=check, args=(host_ip,))
        numList.append(p2)
        p2.start()

        p1.join()
        _log('main', 'draw_cardiogram end.')
        p2.join()
        _log('main', 'check end.')

    _log('main', 'all end.')
    return


def test():
    # manager = Manager()
    # manager._DEBUG = True
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


# ------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
