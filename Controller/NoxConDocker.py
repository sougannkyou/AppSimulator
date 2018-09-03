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
        self.start_retry_cnt = 3
        self.error_msg = ''  # 启动诊断信息
        self._taskId = task_info['taskId']
        self._task_info = task_info
        self._local_ip = LOCAL_IP
        self._org_path = os.getcwd()
        self._work_path = WORK_PATH
        self._app_name = task_info['app_name']
        self._docker_id = None
        self._docker_name = 'nox-{}'.format(task_info['taskId'])
        self._docker_img_name = task_info['docker_img_name']
        self._mdb = MongoDriver()

    # def __del__(self):
    #     print('call NoxConDocker.__del__')
    #     os.chdir(self._org_path)

    def _check(self):
        msg = ''
        self.error_msg = ''
        if not self._local_ip:
            self.error_msg = '必须设定环境变量 APPSIMULATOR_IP'

        if not self._app_name:
            self.error_msg = '必须设定App名字'

        mem = psutil.virtual_memory()
        if mem.free < 1 * GB:  # < 1GB
            self.error_msg = '剩余内存需大于 1GB.'
        else:
            msg = 'Memory: {:.1f} GB'.format(mem.free / GB)

        if not os.access('{}\\{}'.format(NOX_BACKUP_PATH, self._docker_img_name), os.R_OK):
            self.error_msg = '未找到镜像文件: {}'.format(self._docker_img_name)

        if len(self.ps(docker_name='nox-org')) == 0:
            self.error_msg = '未找到 nox-org.'

        running_dockers = self.ps(docker_status=STATUS_DOCKER_RUN_OK)
        if len(running_dockers) >= len(TIMER):
            self.error_msg = '启动数量不能大于 TIMER 设定数量：{}'.format(len(TIMER))
        else:
            msg = '正在运行的模拟器数: {}'.format(len(running_dockers))

        if self.error_msg:
            self._log('<<error>> _check', self.error_msg)
            self.start_retry_cnt = -1  # 不满足启动条件
            return False
        else:
            self._log('_check', msg)
            return True

    def _make_cmd(self, cmd):
        os.chdir(NOX_BIN_PATH)
        return 'NoxConsole ' + cmd

    def _exec_nox_cmd(self, cmdline):
        _stdout = ''
        _stderr = ''
        try:
            self._log('[nox_cmd] cmdline:\n\t', cmdline)
            time.sleep(1)
            os.chdir(NOX_BIN_PATH)  # 防止 BignoxVMS 写入.py本地
            process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # process.wait()
            (stdout, stderr) = process.communicate()
            _stdout = stdout.decode('gbk')
            _stderr = stderr.decode('gbk')
        except Exception as e:
            self._log('<<error>> _exec_nox_cmd Exception:\n', e)
        finally:
            os.chdir(self._org_path)  # 恢复路径

        self._log('<<info>>[nox_cmd] stdout:\n', _stdout)
        if _stderr:
            self._log('<<info>>[nox_cmd] stderr:\n', _stderr)
            return 'error: {}'.format(_stderr)
        else:
            time.sleep(1)
            return _stdout

    def _cmd_kill_task(self, docker_name):
        dockers = self.ps(docker_name=docker_name, docker_status=STATUS_DOCKER_RUN_OK)
        for d in dockers:
            cmd = 'TASKKILL /F /T /PID {}'.format(d['pid'])  # 不能强杀，会造成 ERR：1037
            common_exec_cmd(True, cmd)
            # os.system(cmd)

    def kill_task(self):
        # <<cmd>> taskkill /f /t /fi "WINDOWTITLE eq task-99"
        cmd = 'TASKKILL /F /T /FI "WINDOWTITLE eq task-{}"'.format(self._taskId)
        common_exec_cmd(True, cmd)
        # os.system(cmd)

    def shake(self, cnt):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        hwnd = win32gui.FindWindow(None, self._docker_name)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)

        self._log('<<info>> shake', str(cnt) + ' times')
        for _ in range(cnt):
            self._exec_nox_cmd(self._make_cmd(
                "action -name:{} -key:call.shake -value:null".format(self._docker_name)
            ))
        return True

    def rmi(self, kill_script=False, wait_time=2):  # remove docker image
        self._log('<<info>> rmi', '退出并删除模拟器')
        # if kill_script:  # kill 掉 cmd 启动的 python script_xxx.py
        #     self.kill_task()

        time.sleep(wait_time)
        self._exec_nox_cmd(self._make_cmd("quit -name:{}".format(self._docker_name)))
        time.sleep(wait_time)

        # 确保窗体关闭
        # stdout = common_exec_cmd(self._DEBUG, 'TASKLIST /FI "WINDOWTITLE eq {}"'.format(self._docker_name))
        # if stdout.replace('\r\n', '') == '信息: 没有运行的任务匹配指定标准。':  # win10 win7 cmd 提示信息
        #     return self.remove()
        # else:
        #     return False
        return self.remove()

    def rmi_all(self):
        self._log('<<info>> rmi_all', 'wait: 10s')
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

                    if (docker_status is None or status == docker_status) and (
                            docker_name is None or name == docker_name):
                        devices.append({'id': id, 'name': name, 'status': status, 'pid': pid})

        return devices

    def pull(self):  # restore
        self._log('pull', self._docker_img_name)
        time.sleep(1)
        ret = self._exec_nox_cmd(self._make_cmd(
            'restore -name:{} -file:"{}\\{}"'.format(self._docker_name, NOX_BACKUP_PATH, self._docker_img_name)
        ))
        if ret.find('failed') > 0:
            return False
        else:
            time.sleep(5)
            return True

    def copy(self, org, wait_time=10):
        self._log('copy', self._docker_name)
        time.sleep(wait_time)
        self._exec_nox_cmd(self._make_cmd("copy -name:{} -from:{}".format(self._docker_name, org)))
        return True

    def add(self):
        self._log('add', self._docker_name)
        time.sleep(2)
        self._docker_id = self._mdb.docker_create(docker_obj=self)
        self._mdb.task_bind_docker(self._task_info, self._docker_id)  # bind docker to task
        ret = self._exec_nox_cmd(self._make_cmd("add -name:" + self._docker_name))
        # ret = self._exec_nox_cmd(self._make_cmd("add -name:" + self._docker_name + ' -systemtype:4')) # nox 6.2.1
        time.sleep(2)
        return False if ret.find('failed') != -1 or \
                        ret.find('not') != -1 or \
                        ret.find('system type err!') != -1 else True  # nox 6.2.1

    def remove(self):
        self._log('remove', self._docker_name)
        time.sleep(2)
        self._exec_nox_cmd(self._make_cmd("remove -name:{}".format(self._docker_name)))
        self._mdb.docker_destroy(docker_obj=self)
        self._mdb.task_unbind_docker(self._task_info)  # unbind task
        time.sleep(2)
        return True

    def create(self):
        poweron = self._work_path + '\\static\\AppSimulator\\images\\temp\\emulators\\poweron.png'
        static_capture_path = '{}\\static\\AppSimulator\\images\\temp\\emulators\\capture_{}.png'.format(
            self._work_path, self._docker_name)
        if os.access(static_capture_path, os.R_OK):
            shutil.copy(poweron, static_capture_path)

        ret = self._check()
        if not ret:
            return False

        dockers = self.ps(docker_name=self._docker_name)
        if len(dockers) > 1:
            pprint(dockers)
            self.error_msg = '找到不止 1 个模拟器'
            self._log('<<error>> create', self.error_msg)
            return False

        if len(dockers) == 1:
            # if dockers[0]['status'] == STATUS_DOCKER_RUN:
            ret = self.rmi(kill_script=True, wait_time=5)
            if not ret:
                self.error_msg = 'failed!'
                self._log('<<error>> stop', self.error_msg)
                return False

        # self.copy('nox-org')  # copy命令不稳定
        ret = self.add()
        if not ret:
            self.error_msg = 'add failed!'
            self._log('<<error>> add', self.error_msg)
            return False

        ret = self.pull()
        if not ret:
            self.error_msg = 'pull failed!'
            self._log('<<error>> pull', self.error_msg)
            return False

        return True

    def start(self, timeout=2):
        time.sleep(timeout)
        stdout = self._exec_nox_cmd(self._make_cmd("launch -name:" + self._docker_name))
        time.sleep(timeout)
        if stdout.find('player is not exist!') == -1:
            return True
        else:
            self.error_msg = 'launch failed!'
            return False

    def run(self):  # run = create + start
        ret = self.create()
        if ret:
            ret = self.start()

        return ret

    def get_name(self):
        return self._docker_name

    def get_docker_id(self):
        return self._docker_id

    def get_taskId(self):
        return self._taskId

    def get_app_name(self):
        return self._app_name

    def _log(self, prefix, msg):
        common_log(self._DEBUG, self._taskId, 'NoxDocker ' + self._docker_name, prefix, msg)


# -------------------------------------------------------------------------------
def main(task_info):
    docker = NoxConDocker(task_info=task_info)
    docker._DEBUG = True
    return docker.run()


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
