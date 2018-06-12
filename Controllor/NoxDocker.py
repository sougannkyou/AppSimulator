# coding:utf-8
import os
import time
import psutil
import win32gui
import subprocess
import multiprocessing
from pprint import pprint

GB = 1024 * 1024 * 1024


class NoxDocker(object):
    def __init__(self, app_name):
        self.STATUS_RUNNING = 'running'
        self.STATUS_IDLE = 'idle'
        self.DOCKERS_MAX_CNT = 10
        self._DEBUG = True
        self._app_name = app_name

    def _log(self, prefix, info):
        if self._DEBUG:
            print('[NoxDocker] ', prefix, info)

    def _check(self):
        msg = ''
        if not self._app_name:
            msg = 'app_name is None'
            self._log('_check', msg)
            return False, msg

        if not os.access('c:\\Nox\\backup\\nox-' + self._app_name + '.npbk', os.R_OK):
            msg = 'not found: ' + self._app_name + '.npbk'
            self._log('_check', msg)
            return False, msg

        mem = psutil.virtual_memory()
        if mem.free < 0.5 * GB:  # < 1GB
            msg = 'memory less than 1GB.'
            self._log('_check', msg)
            return False, msg

        if len(self.ps(docker_name='nox-org')) == 0:
            msg = 'not found the nox-org.'
            self._log('_check', msg)
            return False, msg

        if len(self.ps(docker_status=self.STATUS_RUNNING)) >= self.DOCKERS_MAX_CNT:
            msg = 'over the DOCKERS_MAX_CNT.'
            self._log('_check', msg)
            return False, msg

        return True, msg

    def _make_cmd(self, cmd):
        return 'C:\\Nox\\bin\\NoxConsole.exe ' + cmd

    def _exec_nox_cmd(self, cmdline):
        _stdout = ''
        _stderr = ''
        try:
            self._log('_exec_nox_cmd', cmdline)
            process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # process.wait()
            (stdout, stderr) = process.communicate()
            _stdout = stdout.decode('utf8')
            _stderr = stderr.decode('utf8')
        except Exception as e:
            self._log('_exec_nox_cmd Exception:', e)

        self._log('_exec_nox_cmd stdout:\n', _stdout)
        if _stderr:
            self._log('_exec_nox_cmd stderr:\n', _stderr)
            return ''
        else:
            return _stdout

    def stop(self, docker_name, wait_time=30):
        self._exec_nox_cmd(self._make_cmd("quit -name:" + docker_name))
        while wait_time > 0:
            hwnd = win32gui.FindWindow(None, docker_name)
            if hwnd:  # hwnd is 0 if not found
                time.sleep(1)
                self._log('stop', 'wait for stop ' + docker_name + ' ' + str(wait_time) + 's')
                wait_time -= 1
            else:
                break

        if wait_time == 0:  # retry
            self._exec_nox_cmd(self._make_cmd("quit -name:" + docker_name))

        return True

    def stop_all(self):
        self._exec_nox_cmd(self._make_cmd('quitall'))
        return True

    def ps(self, docker_name=None, docker_status=None):
        devices = []
        ret = self._exec_nox_cmd(self._make_cmd('list'))
        # self._log('ps\n', ret)
        if ret:
            # 虚拟机名称，标题，顶层窗口句柄，工具栏窗口句柄，绑定窗口句柄，进程PID
            for s in ret.split('\r\n'):
                if s.startswith('nox') or s.startswith('Nox'):
                    status = self.STATUS_IDLE if s.split(',')[-1] == '-1' else self.STATUS_RUNNING
                    name = s.split(',')[1]
                    id = s.split(',')[0]
                    pid = s.split(',')[-1]

                    if (docker_status is None or status == docker_status) and \
                            (docker_name is None or name == docker_name):
                        devices.append({'id': id, 'name': name, 'status': status, 'pid': pid})

        return devices

    def remove(self, docker_name):
        self._log('remove', docker_name)
        self._exec_nox_cmd(self._make_cmd("remove -name:" + docker_name))
        return True

    def pull(self, docker_name, app_name):  # restore
        self._log('pull', docker_name + ' ' + app_name)
        self._exec_nox_cmd(self._make_cmd(
            'restore -name:' + docker_name + ' -file:"c:\\Nox\\backup\\nox-' + app_name + '.npbk"'
        ))
        return True

    def copy(self, docker_name, org):
        self._log('copy', docker_name)
        self._exec_nox_cmd(self._make_cmd("copy -name:" + docker_name + " -from:" + org))
        return True

    def create(self, docker_name, force=False):
        ret, msg = self._check()
        if not ret:
            return False, msg

        dockers = self.ps(docker_name=docker_name)
        if len(dockers) > 1:
            msg = 'found docker more than 1.'
            self._log('create', msg)
            return False, msg

        if len(dockers) == 0:
            self.copy(docker_name, 'nox-org')

        if len(dockers) == 1:
            if dockers[0]['status'] == self.STATUS_RUNNING:
                self.stop(docker_name, 30)
                self.remove(dockers[0]['name'])
                self.copy(docker_name, 'nox-org')

        if force:
            self.pull(docker_name, self._app_name)

        return True, msg

    def start(self, docker_name, wait_time=30):
        self._exec_nox_cmd(self._make_cmd("launch -name:" + docker_name))
        while wait_time > 0:
            hwnd = win32gui.FindWindow(None, docker_name)
            if hwnd:
                self._log('start', docker_name + ' ok.')
                return True
            else:  # hwnd is 0 if not found
                time.sleep(1)
                wait_time -= 1
                self._log('start', 'wait for start ' + docker_name + ' ' + str(wait_time) + 's')

        return False

    def run(self, docker_name=None, force=False, time_out=30):  # run = create and start
        self.create(docker_name, force)
        self.start(docker_name, wait_time=time_out)


def run(docker_name):
    docker = NoxDocker(app_name='toutiao')
    docker._DEBUG = True
    docker.run(docker_name=docker_name, force=True, time_out=30)


if __name__ == "__main__":
    # tasks_cnt = 3
    os.chdir('c:\\Nox\\bin')
    # pool = multiprocessing.Pool(processes=4)
    # for docker_name in ['nox-3', 'nox-4', 'nox-5']:  # range(tasks_cnt):
    # # for docker_name in ['nox-3']:  # range(tasks_cnt):
    #     pool.apply_async(run, (docker_name,))
    # pool.close()
    # pool.join()

    for docker_name in ['nox-3', 'nox-4', 'nox-5']:
    # for docker_name in ['nox-6', 'nox-7', 'nox-8']:
        run(docker_name)

    print("process done.")
