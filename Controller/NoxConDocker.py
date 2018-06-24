# coding:utf-8
import os
import time
import psutil
import win32gui
import subprocess
import aircv as ac
from PIL import ImageGrab
from Controller.setting import *


class NoxConDocker(object):
    def __init__(self, app_name, docker_name):
        self.DOCKERS_MAX_CNT = 10
        self._DEBUG = True
        self._ip = os.getenv('APPSIMULATOR_IP')
        self._app_name = app_name
        self._docker_name = docker_name
        self._work_path = os.getenv('APPSIMULATOR_WORK_PATH')

        self._PIC_PATH = {
            "APP图标": self._work_path + '\\Controller\\images\\' + self._app_name + '\\app_icon.png',
            "很抱歉": self._work_path + '\\Controller\\images\\im_sorry.png',
        }

        os.chdir('c:\\Nox\\bin')  # 防止 BignoxVMS 写入py本地

    def _log(self, prefix, msg):
        if self._DEBUG:
            print('[NoxDocker] ', prefix, msg)

    def _check(self):
        msg = ''
        if not self._ip:
            msg = 'ip 不能为空，请设置：APPSIMULATOR_IP'
            self._log('_check', msg)
            return False, msg

        if not self._app_name:
            msg = 'app_name 不能为空.'
            self._log('_check', msg)
            return False, msg

        if not self._work_path:
            msg = '请设置: APPSIMULATOR_WORK_PATH'
            self._log('_check', msg)
            return False, msg

        mem = psutil.virtual_memory()
        if mem.free < 1 * GB:  # < 1GB
            msg = '内存剩余必须大于 1GB.'
            self._log('_check', msg)
            return False, msg
        else:
            self._log('_check', 'memory: %.1f' % (mem.free / GB) + ' GB')

        if not os.access('c:\\Nox\\backup\\nox-' + self._app_name + '.npbk', os.R_OK):
            msg = '未找到 nox-' + self._app_name + '.npbk'
            self._log('_check', msg)
            return False, msg

        if len(self.ps(docker_name='nox-org')) == 0:
            msg = '未找到 nox-org.'
            self._log('_check', msg)
            return False, msg

        running_dockers = self.ps(docker_status=STATUS_RUNNING)
        if len(running_dockers) >= self.DOCKERS_MAX_CNT:
            msg = '启动数量不能大于 ' + str(self.DOCKERS_MAX_CNT)
            self._log('_check', msg)
            return False, msg
        else:
            self._log('_check', '当前运行中的docker数: ' + str(len(running_dockers)))

        return True, msg

    def _make_cmd(self, cmd):
        os.chdir('c:\\Nox\\bin')
        return 'NoxConsole ' + cmd

    def _exec_nox_cmd(self, cmdline):
        _stdout = ''
        _stderr = ''
        try:
            self._log('cmdline:', cmdline)
            time.sleep(1)
            process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # process.wait()
            (stdout, stderr) = process.communicate()
            _stdout = stdout.decode('utf8')
            _stderr = stderr.decode('utf8')
        except Exception as e:
            self._log('exception:', e)

        self._log('stdout:\n', _stdout)
        if _stderr:
            self._log('stderr:\n', _stderr)
            return ''
        else:
            time.sleep(1)
            return _stdout

    def _cmd_kill_task(self, docker_name):
        dockers = self.ps(docker_name=docker_name, docker_status=STATUS_RUNNING)
        for d in dockers:
            cmd = 'TASKKILL /F /T /PID ' + str(d['pid'])  # 不能强杀，会造成 ERR：1037
            self._log('_cmd_kill_task', cmd)
            os.system(cmd)

    def get_port(self):
        self._log('shake', '获取adb端口')
        ret = self._exec_nox_cmd(self._make_cmd(
            'adb -name:' + self._docker_name + ' -command:"get-serialno"'
        ))
        return ret.replace('\r', '').replace('\n', '').replace('127.0.0.1:', '')

    def shake(self, cnt):
        self._log('shake', '振动提示 ...')
        for i in range(cnt):
            self._exec_nox_cmd(self._make_cmd("action -name:" + self._docker_name + " -key:call.shake -value:null"))
        return True

    def set_docker_name(self):
        self._log('shake', '设置docker名称为:' + self._docker_name)
        self._exec_nox_cmd(self._make_cmd(
            'adb -name:' + self._docker_name + ' -command:" shell setprop persist.nox.docker_name ' + self._docker_name + '"'
        ))
        return True

    def stop(self, retry=False, wait_time=30):
        self._exec_nox_cmd(self._make_cmd("quit -name:" + self._docker_name))
        while wait_time > 0:
            hwnd = win32gui.FindWindow(None, self._docker_name)
            if hwnd:  # hwnd is 0 if not found
                time.sleep(1)
                self._log('stop', '正在等待 ' + self._docker_name + ' 停止，剩余：' + str(wait_time) + 's')
                wait_time -= 1
            else:
                break

        if retry and wait_time == 0:  # retry
            self._exec_nox_cmd(self._make_cmd("quit -name:" + self._docker_name))

        time.sleep(10)
        # self._cmd_kill_task(self._docker_name)  # 不能强杀，会造成 ERR：1037
        return True

    def stop_all(self):
        self._exec_nox_cmd(self._make_cmd('quitall'))
        time.sleep(10)
        return True

    def ps(self, docker_name=None, docker_status=None):
        devices = []
        ret = self._exec_nox_cmd(self._make_cmd('list'))
        # self._log('ps\n', ret)
        if ret:
            # 虚拟机名称，标题，顶层窗口句柄，工具栏窗口句柄，绑定窗口句柄，进程PID
            for s in ret.split('\r\n'):
                if s.startswith('nox') or s.startswith('Nox'):
                    status = STATUS_WAIT if s.split(',')[-1] == '-1' else STATUS_RUNNING
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
        return True

    def pull(self, app_name):  # restore
        self._log('pull', self._docker_name + ' ' + app_name)
        time.sleep(1)
        ret = self._exec_nox_cmd(self._make_cmd(
            'restore -name:' + self._docker_name + ' -file:"c:\\Nox\\backup\\nox-' + app_name + '.npbk"'
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
        time.sleep(2)
        return False if ret.find('failed') > 0 or ret.find('not') > 0 else True

    def create(self, force=False):
        ret, msg = self._check()
        if not ret:
            return False, msg

        dockers = self.ps(docker_name=self._docker_name)
        if len(dockers) > 1:
            msg = '找到的 docker 数大于1个.'
            self._log('create', msg)
            return False, msg

        if len(dockers) == 1:
            if dockers[0]['status'] == STATUS_RUNNING:
                self.stop(retry=False, wait_time=30)

            ret = self.remove()
            if not ret:
                msg = 'remove failed!'
                return False, msg

        # time.sleep(10)
        # self.copy('nox-org')
        ret = self.add()
        if not ret:
            msg = 'add failed!'
            return False, msg

        ret = self.pull(self._app_name)
        if not ret:
            msg = 'pull failed!'
            return False, msg

        return True, msg

    def find_element(self, hwnd, comment, timeout):
        self._log('find_element', '尝试在 ' + str(timeout) + 's内匹配: ' + comment)
        time.sleep(3)
        while timeout > 0:
            win32gui.SetForegroundWindow(hwnd)
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            app_bg_box = (left, top, right, bottom)

            im = ImageGrab.grab(app_bg_box)
            im.save(self._work_path + '\\Controller\\images\\start.png')

            img_capture = ac.imread(self._work_path + '\\Controller\\images\\start.png')
            img_obj = ac.imread(self._PIC_PATH[comment])
            pos = ac.find_template(img_capture, img_obj)
            if pos and pos['confidence'] > 0.9:
                self._log('find_element', '已匹配到:' + comment + ' ' + str(timeout) + 's')
                return True
            else:
                time.sleep(1)
                timeout = timeout - 1
                self._log('find_element', '未匹配到:' + comment + ', 重试剩余: ' + str(timeout) + 's')

        return False

    def start(self, wait_time=30):
        self._exec_nox_cmd(self._make_cmd("launch -name:" + self._docker_name))
        while wait_time > 0:
            hwnd = win32gui.FindWindow(None, self._docker_name)
            if hwnd:
                self._log('start', self._docker_name + ' ok.')
                ret = self.find_element(hwnd, '很抱歉', 30)  # 匹配“很抱歉”字样
                if ret:
                    return False
                else:
                    return self.find_element(hwnd, 'APP图标', 30)  # 可匹配到app图标

            else:  # hwnd is 0 if not found
                time.sleep(1)
                wait_time -= 1
                self._log('start', '等待 ' + self._docker_name + ' 窗口创建，剩余：' + str(wait_time) + 's')

        return False

    def on_success(self):
        time.sleep(10)
        self.shake(3)
        self.set_docker_name()
        port = self.get_port()
        return True

    def on_error(self, retry_cnt=0):
        while retry_cnt > 0:
            ret, msg = self.create(force=True)
            if ret:
                ret = self.start(wait_time=30)
                if ret:  # start success
                    return True
            else:
                retry_cnt -= 1
        else:
            self.stop()

        return False

    def build(self, force=False, retry_cnt=2, wait_time=30):  # run = create and start
        ret, msg = self.create(force)
        if ret:
            ret = self.start(wait_time=wait_time)
            if ret:  # start success
                ret = self.on_success()
            else:
                ret = self.on_error(retry_cnt=retry_cnt)

            # else:  # retry
            #     ret = self.start(wait_time=time_out)
            #     if ret:
            #         time.sleep(10)  # wait 10s
            #     else:

        return ret


def build(app_name, docker_name):
    docker = NoxConDocker(app_name=app_name, docker_name=docker_name)
    docker._DEBUG = True
    return docker.build(force=True, retry_cnt=2, wait_time=30)
    # docker.stop_all()


if __name__ == "__main__":
    # tasks_cnt = 3
    complete_cnt = 0
    os.chdir('c:\\Nox\\bin')
    # pool = multiprocessing.Pool(processes=4)
    # for docker_name in ['nox-3', 'nox-4', 'nox-5']:  # range(tasks_cnt):
    # # for docker_name in ['nox-3']:  # range(tasks_cnt):
    #     pool.apply_async(run, (docker_name,))
    # pool.close()
    # pool.join()

    # for docker_name in ['nox-11', 'nox-12', 'nox-13', 'nox-14', 'nox-15']:
    for docker_name in ['nox-21', 'nox-22', 'nox-23', 'nox-24', 'nox-25', 'nox-26', 'nox-27']:
        # for docker_name in ['nox-31', 'nox-32', 'nox-33']:
        # for docker_name in ['nox-41', 'nox-42', 'nox-43']:
        # for docker_name in ['nox-11']:
        if build('toutiao', docker_name):  # run = create and start
            complete_cnt += 1

    print("start success:", str(complete_cnt))
