import sys
import os
import time
import psutil
import shutil
from pprint import pprint
import win32gui
import win32com.client

sys.path.append(os.getcwd())
from Controller.Common import *
from Controller.DBLib import MongoDriver


class NoxConDocker(object):
    def __init__(self, task_info):
        self._DEBUG = True
        self._taskId = task_info['taskId']
        self._local_ip = LOCAL_IP
        self._org_path = os.getcwd()
        self._work_path = WORK_PATH
        self._app_name = task_info['app_name']
        self._docker_name = 'nox-' + str(task_info['taskId'])
        self._taskId = task_info['taskId']
        self._mdb = MongoDriver()

    # def __del__(self):
    #     print('call NoxConDocker.__del__')
    #     os.chdir(self._org_path)

    def _log(self, prefix, msg):
        common_log(self._DEBUG, self._taskId, 'NoxDocker ' + self._docker_name, prefix, msg)

    def _check(self):
        msg = ''
        if not self._local_ip:
            msg = 'Must be set APPSIMULATOR_IP'
            self._log('_check error:', msg)
            return False, msg

        if not self._app_name:
            msg = 'Must be set app_name'
            self._log('_check error:', msg)
            return False, msg

        mem = psutil.virtual_memory()
        if mem.free < 1 * GB:  # < 1GB
            msg = 'Memory must be greater than 1GB.'
            self._log('_check error:', msg)
            return False, msg
        else:
            self._log('_check', 'Memory: %.1f' % (mem.free / GB) + ' GB')

        if not os.access(NOX_BACKUP_PATH + '\\nox-' + self._app_name + '.npbk', os.R_OK):
            msg = 'Not found nox-' + self._app_name + '.npbk'
            self._log('_check error', msg)
            return False, msg

        if len(self.ps(docker_name='nox-org')) == 0:
            msg = 'Not found nox-org.'
            self._log('_check error:', msg)
            return False, msg

        running_dockers = self.ps(docker_status=STATUS_DOCKER_RUN_OK)
        if len(running_dockers) >= len(TIMER):
            msg = 'The number of starts can not be greater than timer counter ' + str(len(TIMER))
            self._log('_check error:', msg)
            return False, msg
        else:
            self._log('_check ok', 'Running dockers: ' + str(len(running_dockers)))

        return True, msg

    def _make_cmd(self, cmd):
        os.chdir(NOX_BIN_PATH)
        return 'NoxConsole ' + cmd

    def _exec_nox_cmd(self, cmdline):
        _stdout = ''
        _stderr = ''
        try:
            self._log('<<nox_cmd>> ', cmdline)
            time.sleep(1)
            os.chdir(NOX_BIN_PATH)  # 防止 BignoxVMS 写入.py本地
            process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # process.wait()
            (stdout, stderr) = process.communicate()
            _stdout = stdout.decode('gbk')
            _stderr = stderr.decode('gbk')
        except Exception as e:
            self._log('_exec_nox_cmd error:', e)
        finally:
            os.chdir(self._org_path)  # 恢复路径

        self._log('stdout:\n', _stdout)
        if _stderr:
            self._log('stderr:\n', _stderr)
            return '<<<error>>>' + _stderr
        else:
            time.sleep(1)
            return _stdout

    def _cmd_kill_task(self, docker_name):
        dockers = self.ps(docker_name=docker_name, docker_status=STATUS_DOCKER_RUN_OK)
        for d in dockers:
            cmd = 'TASKKILL /F /T /PID ' + str(d['pid'])  # 不能强杀，会造成 ERR：1037
            common_exec_cmd(True, cmd)
            # os.system(cmd)

    def kill_task(self):
        # <<cmd>> taskkill /f /t /fi "WINDOWTITLE eq task-99"
        cmd = 'TASKKILL /F /T /FI "WINDOWTITLE eq task-' + str(self._taskId) + '"'
        common_exec_cmd(True, cmd)
        # os.system(cmd)

    def get_name(self):
        return self._docker_name

    def shake(self, cnt):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        hwnd = win32gui.FindWindow(None, self._docker_name)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)

        self._log('<<info>> shake', str(cnt) + ' times')
        for _ in range(cnt):
            self._exec_nox_cmd(self._make_cmd("action -name:" + self._docker_name + " -key:call.shake -value:null"))
        return True

    def quit(self, wait_time=2):
        self._log('<<info>> destroy', 'wait: ' + str(wait_time) + 's')
        time.sleep(wait_time)
        self._exec_nox_cmd(self._make_cmd("quit -name:" + self._docker_name))
        time.sleep(wait_time)
        stdout = common_exec_cmd(self._DEBUG, 'TASKLIST /FI "WINDOWTITLE eq ' + self._docker_name + '"')
        # win10 win7 cmd 提示信息
        return stdout.replace('\r\n', '') == '信息: 没有运行的任务匹配指定标准。'

    def stop(self, wait_time=2):
        self._log('<<info>> stop', 'wait: ' + str(wait_time) + 's')
        self.kill_task()  # kill 掉 cmd 启动的 python  script_xxx.py
        return self.quit(wait_time=wait_time)

    def stop_all(self):
        self._log('<<info>> stop_all', 'wait: 10s')
        time.sleep(2)
        self._exec_nox_cmd(self._make_cmd('quitall'))
        time.sleep(10)
        return True

    def ps(self, docker_name=None, docker_status=None):
        devices = []
        ret = self._exec_nox_cmd(self._make_cmd('list'))
        if ret:
            # 虚拟机名称，标题，顶层窗口句柄，工具栏窗口句柄，绑定窗口句柄，进程PID
            for s in ret.split('\r\n'):
                if s.startswith('nox') or s.startswith('Nox'):
                    status = STATUS_WAIT if s.split(',')[-1] == '-1' else STATUS_DOCKER_RUN_OK
                    name = s.split(',')[1]
                    id = s.split(',')[0]
                    pid = s.split(',')[-1]

                    if (docker_status is None or status == docker_status) and \
                            (docker_name is None or name == docker_name):
                        devices.append({'id': id, 'name': name, 'status': status, 'pid': pid})

        return devices

    def remove(self):
        self._log('remove', self._docker_name)
        time.sleep(2)
        self._exec_nox_cmd(self._make_cmd("remove -name:" + self._docker_name))
        time.sleep(2)
        return self._mdb.emulator_end(self._taskId)

    def pull(self, app_name):  # restore
        self._log('pull', self._docker_name + ' ' + app_name)
        time.sleep(1)
        ret = self._exec_nox_cmd(self._make_cmd(
            'restore -name:' + self._docker_name + ' -file:"' + NOX_BACKUP_PATH + '\\nox-' + app_name + '.npbk"'
        ))
        if ret.find('failed') > 0:
            return False
        else:
            time.sleep(5)
            return True

    def copy(self, org):
        self._log('copy', self._docker_name)
        self._exec_nox_cmd(self._make_cmd("copy -name:" + self._docker_name + " -from:" + org))
        return True

    def add(self):
        self._log('add', self._docker_name)
        time.sleep(2)
        ret = self._exec_nox_cmd(self._make_cmd("add -name:" + self._docker_name))
        # ret = self._exec_nox_cmd(self._make_cmd("add -name:" + self._docker_name + ' -systemtype:4')) # nox 6.2.1
        time.sleep(2)
        return False if ret.find('failed') != -1 or \
                        ret.find('not') != -1 or \
                        ret.find('system type err!') != -1 else True

    def create(self, force=False):
        poweron = self._work_path + '\\static\\AppSimulator\\images\\temp\\emulators\\poweron.png'
        static_capture_path = self._work_path + '\\static\\AppSimulator\\images\\temp\\emulators\\capture_' + self._docker_name + '.png'
        if os.access(static_capture_path, os.R_OK):
            shutil.copy(poweron, static_capture_path)

        ret, msg = self._check()
        if not ret:
            return False, msg

        dockers = self.ps(docker_name=self._docker_name)
        if len(dockers) > 1:
            pprint(dockers)
            msg = 'The number of docker found is more than 1.'
            self._log('create', msg)
            return False, msg

        if len(dockers) == 1:
            if dockers[0]['status'] == STATUS_DOCKER_RUN:
                ret = self.stop(wait_time=5)
                if not ret:
                    msg = 'failed!'
                    self._log('<<error>> stop', msg)
                    return False, msg

            ret = self.remove()
            if not ret:
                msg = 'failed!'
                self._log('<<error>> remove', msg)
                return False, msg

        # time.sleep(10)
        # self.copy('nox-org')
        ret = self.add()
        if not ret:
            msg = 'failed!'
            self._log('<<error>> add', msg)
            return False, msg

        ret = self.pull(self._app_name)
        if not ret:
            msg = 'failed!'
            self._log('<<error>> pull', msg)
            return False, msg

        return True, msg

    def start(self, timeout=2):
        time.sleep(timeout)
        stdout = self._exec_nox_cmd(self._make_cmd("launch -name:" + self._docker_name))
        time.sleep(timeout)
        return stdout.find('player is not exist!') == -1

    def run(self, force=False):  # run = create + start
        ret, msg = self.create(force)
        if ret:
            ret = self.start()

        return ret


# -------------------------------------------------------------------------------
def main(task_info):
    docker = NoxConDocker(task_info=task_info)
    docker._DEBUG = True
    return docker.run(force=True)


if __name__ == "__main__":
    # docker_name = sys.argv[1]
    docker_name = 'nox-2'
    task_info = {
        'taskId': 2,
        'app_name': 'miaopai',
        'docker_name': docker_name,
        'timer_no': 2
    }
    main(task_info)
    print("Close after 60 seconds.")
    time.sleep(60)
