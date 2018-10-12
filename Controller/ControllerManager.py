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
            self._log('<<error>> _check', msg)
            return False, msg

    def __nox_run_script(self, task_info):
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
            self._log('<<error>> run_script Exception:\n', e)

        if _stderr:
            self._log('<<error>> run_script stderr:\n', _stderr)
            return False
        else:
            self._log('run_script stdout:\n', _stdout)
            time.sleep(1)
            return True

    def ___nox_run_script(self, task, docker_name):
        try:
            script = 'Controller.' + task['script'][:-3]
            importlib.invalidate_caches()
            module = importlib.import_module(script)
            # importlib.reload(module)
            module.main(docker_name)
            self._log('<<info>> run_script ok', script)
            return True
        except Exception as e:
            self._log('<<error>> run_script Exception:\n', e)
            return False

    def nox_run_script(self, task_info):
        org_path = os.getcwd()
        os.chdir(self._work_path)
        try:
            if task_info['timer'] == TIMER_ON:  # 从系统获取timer_no(Index of TIMER, start 0)
                timer_no = self._mdb.task_get_timer_no(host_ip=LOCAL_IP)
                if timer_no == -1:
                    self._log('<<error>> nox_run_script', 'not fond timer_no')
                    return False, 'timer_no'
            else:  # timer:off 不使用timer功能
                timer_no = -1

            ##################################################################################################
            cmd = 'START "task-{}" python {}\Controller\\script\\{} {} {}'.format(
                task_info['taskId'], self._work_path, task_info['script'], task_info['taskId'], timer_no
            )
            self._log('<<info>> run_script cmd:\n', cmd)
            os.system(cmd)
            ##################################################################################################
            os.chdir(org_path)
            return True, ''
        except Exception as e:
            os.chdir(org_path)
            self._log('<<error>> run_script Exception:\n', e)
            return False, e

    def nox_start(self, task, docker):
        docker.docker_rmi(kill_script=True)
        self.nox_stop_confirm(docker, retry=True, wait_time=30)

        ret = docker.docker_run()  # docker.docker_run = docker.docker_create(precheck) + docker.docker_start
        if ret:
            ret = self.nox_start_confirm(task_info=task, docker=docker, timeout=60)

        if ret:
            ret = self.nox_start_success(docker=docker)
        else:
            ret = self.nox_start_error(task=task, docker=docker)

        return ret

    def nox_start_success(self, docker):
        self._log('<<info>> nox_start_success', docker.get_name())
        docker.docker_shake(1)
        # docker.set_docker_name()
        # port = docker.get_port()
        return True

    def nox_start_error(self, task, docker):
        self._log('<<info>> nox_start_error', 'start_retry_cnt: {}'.format(docker.start_retry_cnt))
        if docker.start_retry_cnt == -1:  # _check error 不满足启动条件
            return False

        docker.start_retry_cnt -= 1
        if docker.start_retry_cnt > 0:  # 模拟器启动失败则重试
            self._log('<<info>> nox_start_error', '\n<< 将再尝试 {} 次 重启 {} >>\n'.format(
                docker.start_retry_cnt, docker.get_name()
            ))
            return self.nox_start(task, docker)
        else:
            docker.docker_rmi(kill_script=True)

        return False

    def nox_start_confirm(self, task_info, docker, timeout=60):  # 进一步确认可匹配到app图标，以确保启动成功.
        driver = NoxConSelenium(task_info=task_info, mode=MODE_MULTI)
        driver.set_comment_to_pic({
            "APP图标": 'images/{}/app_icon.png'.format(task_info['app_name']),
        })
        ret = driver.wait_online(timeout=timeout)
        if ret:
            ret, x, y = driver.find_element(comment='很抱歉', timeout=10)  # 匹配到“很抱歉”字样
            if ret:
                msg = '匹配到“很抱歉”'
                docker.add_deadly_msg('nox_start_confirm', msg)
                self._log('<<info>> nox_start_confirm', '{} {}'.format(docker.get_name(), msg))
                return False
            else:
                ret, x, y = driver.find_element(comment='APP图标', timeout=10)  # 可匹配到app图标
                if ret:
                    msg = '可匹配到app图标'
                else:
                    msg = '未匹配到app图标'
                    docker.add_deadly_msg('nox_start_confirm', msg)

                self._log('<<info>> nox_start_confirm', '{} {}'.format(docker.get_name(), msg))
                return ret

    def nox_stop_confirm(self, docker, retry=False, wait_time=30):  # 进一步确认窗体消失，以确保停止成功
        while wait_time > 0:
            hwnd = win32gui.FindWindow(None, docker.get_name())
            if hwnd:  # hwnd is 0 if not found
                time.sleep(1)
                self._log('<<info>> nox_stop_confirm', '正在等待 {} 停止，剩余：{} 秒.'.format(
                    docker.get_name(), wait_time
                ))
                wait_time -= 1
            else:  # not found the window
                self._log('<<info>> nox_stop_confirm', '{} 已停止，剩余：{} 秒.'.format(
                    docker.get_name(), wait_time
                ))
                break

        if retry and wait_time == 0:  # 不能强杀，会造成模拟器 ERR：1037
            # docker._cmd_kill_task
            docker.docker_rmi(kill_script=True)

        time.sleep(10)
        return True

    def nox_run_task_finally(self, taskId):
        task = self._mdb.task_find_by_taskId(int(taskId))

        docker = NoxConDocker(task)
        docker.docker_rmi(kill_script=True)

        task['status'] = STATUS_SCRIPT_RUN_OK
        self._mdb.task_change_status(task)
        if task['live_cycle'] == LIVE_CYCLE_NEVER:
            self._log('<<info>> nox_run_task_finally', 'reset Task status to wait.')
            self._mdb.task_clone(task)

    def nox_schedule(self):
        return self._mdb.task_schedule()

    def nox_run_tasks(self):
        # 1)docker running -> 2)docker run ok(ng) -> 3)script run ok(ng)
        while True:
            task, msg = self._mdb.task_get_one_for_run()
            if task:
                # 1) 模拟器启动
                task['status'] = STATUS_DOCKER_RUN
                self._mdb.task_change_status(task)

                #    模拟器启动失败则重试3次
                docker = NoxConDocker(task_info=task)
                ret = self.nox_start(task=task, docker=docker)

                # 2) 模拟器启动：成功/失败
                task['status'] = STATUS_DOCKER_RUN_OK if ret else STATUS_DOCKER_RUN_NG
                self._mdb.task_change_status(task)

                if ret:  # 3) 脚本启动：成功/失败
                    ###############################################
                    ret, msg = self.nox_run_script(task_info=task)
                    ###############################################
                    if ret:
                        task['status'] = STATUS_SCRIPT_START_OK
                    elif msg == 'timer_no':  # 系统无法获取可用 timer_no
                        task['status'] = STATUS_WAIT
                    else:
                        task['status'] = STATUS_SCRIPT_START_NG

                    self._mdb.task_change_status(task)
            else:
                ###############################################
                cnt = self.nox_schedule()
                if cnt:
                    self._log('<<info>> run_schedule', 'reset {} tasks to wait status.'.format(cnt))
                ###############################################
                if msg:
                    self._log('<<info>> start_tasks', msg)
                else:
                    self._log('<<ignore>> start_tasks', 'not found waiting task, retry after 60s.')
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
            self._log('<<error>> vm_reset Exception:\n', e)
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
