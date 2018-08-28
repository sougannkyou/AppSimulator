import sys
import os
import time
import subprocess
import psutil
import importlib
import importlib.util
import win32gui

sys.path.append(os.getcwd())

from Controller.setting import *
from Controller.Common import common_log
from Controller.DBLib import MongoDriver, RedisDriver
from Controller.NoxConDocker import NoxConDocker
from Controller.NoxConSelenium import NoxConSelenium

_DEBUG = True


# ------------------------ manager ----------------------
class Manager(object):
    def __init__(self):
        self._rds = RedisDriver()
        self._mdb = MongoDriver()
        self._mdb._DEBUG = False
        self._DEBUG = False
        self._work_path = WORK_PATH

    def _log(self, prefix, msg):
        common_log(self._DEBUG, '', 'Manager', prefix, msg)

    # ----------------------- hosts ------------------------------------------------------
    def host_support_app_list(self):
        app_list = []
        for root, dirs, files in os.walk(NOX_BACKUP_PATH):
            for file in files:
                if os.path.splitext(file)[1] == '.npbk':
                    p = os.path.splitext(file)[0]  # nox-dianping.npbk
                    app_list.append(p[4:])

        return app_list

    def host_register_service(self, host_type='emulator'):
        mem = psutil.virtual_memory()
        info = {
            'ip': LOCAL_IP,
            'host_type': host_type,  # 'emulator' or 'vmware'
            'support_app_list': self.host_support_app_list(),
            'mem_free': '%.1f' % (mem.free / GB),
            'mem_total': '%.1f' % (mem.total / GB),
            'timer_max_cnt': len(TIMER)
        }
        self._mdb.host_register_service(info)
        return

    # ---------------------- nox -------------------------------------------------------------
    def _nox_check(self):
        if not self._work_path:
            msg = '请设置: APPSIMULATOR_WORK_PATH'
            self._log('_check error', msg)
            return False, msg

    def nox_run_script1(self, task_info):
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
            _stdout = stdout.decode('gbk')
            _stderr = stderr.decode('gbk')
        except Exception as e:
            self._log('<<error>> run_script:', e)

        if _stderr:
            self._log('run_script stderr:\n', _stderr)
            return False
        else:
            self._log('run_script stdout:\n', _stdout)
            time.sleep(1)
            return True

    def nox_run_script2(self, task, docker_name):
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

    def nox_run_script(self, task_info):
        org_path = os.getcwd()
        os.chdir(self._work_path)
        try:
            timer_no = self._mdb.task_get_timer_no(host_ip=LOCAL_IP)  # Index of TIMER, start 0
            if timer_no == -1:
                self._log('error', 'not fond timer_no')
                return False, 'timer_no'

            ##################################################################################################
            cmd = 'START "task-' + str(task_info['taskId']) + '" ' + \
                  'python ' + self._work_path + '\Controller\\script\\' + task_info['script'] + ' ' + \
                  str(task_info['taskId']) + ' ' + str(timer_no)
            self._log('<<info>> run_script cmd:\n', cmd)
            os.system(cmd)
            ##################################################################################################
            os.chdir(org_path)
            return True, ''
        except Exception as e:
            os.chdir(org_path)
            self._log('run_script error:', e)
            return False, e

    def nox_start(self, task, docker, retry_cnt):
        docker.stop()
        self.nox_check_stop(docker, retry=True, wait_time=30)
        ret = docker.run(force=True)  # docker run: create and start
        if ret:
            ret = self.nox_start_check(task_info=task, timeout=60)  # 可匹配到app图标?
            if ret:
                ret = self.nox_start_success(docker=docker)
            else:
                ret = self.nox_start_error(task=task, docker=docker, retry_cnt=retry_cnt)

        return ret

    def nox_start_success(self, docker):
        self._log('<<info>> docker_run_success', docker.get_name())
        time.sleep(2)
        docker.shake(1)
        # docker.set_docker_name()
        # port = docker.get_port()
        return True

    def nox_start_error(self, task, docker, retry_cnt):
        self._log('<<info>> docker_run_error:', docker.get_name() + ' retry: ' + str(retry_cnt))
        retry_cnt -= 1
        if retry_cnt >= 0:
            return self.nox_start(task, docker, retry_cnt)

        return False

    def nox_start_check(self, task_info, timeout=60):
        driver = NoxConSelenium(task_info=task_info, mode=MODE_MULTI)
        driver.set_comment_to_pic({
            "APP图标": 'images/' + task_info['app_name'] + '/app_icon.png',
        })
        docker_name = 'nox-' + str(task_info['taskId'])
        ret = driver.wait_online(timeout=timeout)
        if ret:
            ret, x, y = driver.find_element(comment='很抱歉', timeout=10)  # 匹配到“很抱歉”字样
            if ret:
                self._log('<<info>> check_docker_run', docker_name + ' 匹配到“很抱歉”.')
                return False
            else:
                ret, x, y = driver.find_element(comment='APP图标', timeout=10)  # 可匹配到app图标
                if ret:
                    self._log('<<info>> check_docker_run', docker_name + ' 可匹配到app图标.')
                else:
                    self._log('<<info>> check_docker_run', docker_name + ' 未匹配到app图标.')

                return ret

    def nox_check_stop(self, docker, retry=False, wait_time=30):
        while wait_time > 0:
            hwnd = win32gui.FindWindow(None, docker.get_name())
            if hwnd:  # hwnd is 0 if not found
                time.sleep(1)
                self._log('<<info>> check_docker_stop', '正在等待 ' + docker.get_name() + ' 停止，剩余：' + str(wait_time) + 's')
                wait_time -= 1
            else:  # not found the window
                self._log('<<info>> check_docker_stop', docker.get_name() + '已停止 ' + str(wait_time) + 's')
                break

        if retry and wait_time == 0:  # retry
            # docker._cmd_kill_task(self._docker_name)  # 不能强杀，会造成 ERR：1037
            docker.stop()

        time.sleep(10)
        return True

    def nox_run_task_finally(self, taskId):
        task = self._mdb.task_find_by_taskId(int(taskId))

        docker = NoxConDocker(task)
        docker.quit()
        docker.remove()

        task['status'] = STATUS_SCRIPT_RUN_OK
        self._mdb.task_change_status(task)
        if task['live_cycle'] == LIVE_CYCLE_NEVER:
            self._log('<<info>> nox_run_task_complete', 'clone')
            self._mdb.task_clone(task)

    def nox_schedule(self):
        return self._mdb.task_schedule()

    def nox_run_tasks(self):
        # 1)docker running -> 2)docker run ok(ng) -> 3)script run ok(ng)
        while True:
            task, msg = self._mdb.task_get_one_for_run()
            if task:
                # 1) docker run
                task['status'] = STATUS_DOCKER_RUN
                self._mdb.task_change_status(task)
                self._mdb.task_change_status(task)
                docker = NoxConDocker(task_info=task)
                ret = self.nox_start(task=task, docker=docker, retry_cnt=2)

                # 2) docker run ok(ng)
                status = STATUS_DOCKER_RUN_OK if ret else STATUS_DOCKER_RUN_NG
                docker_info = {'_id': self._mdb.emulator_create(task), 'status': status}
                self._mdb.emulator_change_status(docker_info)
                task['status'] = status
                self._mdb.task_change_status(task)

                if ret:  # docker run ok
                    # 3) script run ok(ng)
                    self._mdb.task_set_docker(task, docker_info)  # bind docker to task
                    ###############################################
                    ret, msg = self.nox_run_script(task_info=task)
                    ###############################################
                    if ret:
                        task['status'] = STATUS_SCRIPT_START_OK
                    elif msg == 'timer_no':  # not found timer_no
                        task['status'] = STATUS_WAIT
                    else:
                        task['status'] = STATUS_SCRIPT_START_NG

                    self._mdb.task_change_status(task)
            else:
                cnt = self.nox_schedule()
                if cnt:
                    self._log('<<info>> run_schedule', 'reset {} task to wait status.'.format(cnt))

                self._log('<<info>> start_tasks', 'not found waiting task, retry after 60s.')
                time.sleep(1 * 60)

    # --------------------------- vmwares --------------------------------------------------------
    def vm_draw_cardiogram(self, host_ip):
        while True:
            vmwares = self._mdb.vm_find_vm_by_host(host_ip)
            for vm in vmwares:
                cnt = self._rds.get_vmware_shareLink_cnt(vm['ip'], vm['app_name'])
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
            self._log('vm_reset <<cmd>>', cmd)
            os.system('start "VMReset" ' + cmd)
            self._log('vm_reset end:', vm_name)
            return True
        except Exception as e:
            self._log('vm_reset error:', e)
            return False

    def vm_check_active(self, host_ip):
        while True:
            vmwares = self._mdb.vm_find_vm_by_host(host_ip)
            for vm in vmwares:
                shareLink_cnt_list = self._mdb.vm_get_shareLink_cnt(vm['ip'])
                if len(shareLink_cnt_list) >= CHECK_TIMES and shareLink_cnt_list[-1] > 0:
                    self._log('vm_check_active ' + vm['ip'], shareLink_cnt_list)
                    if shareLink_cnt_list[0] == shareLink_cnt_list[-1]:  # 无增长记录
                        self._log('vm_check_active', vm['ip'] + ': suspend tobe reset')
                        self.vm_reset(vm['name'])
                    else:
                        self._log('vm_check_active', vm['ip'] + ': running')

            time.sleep(CHECK_TIMES * 60)
