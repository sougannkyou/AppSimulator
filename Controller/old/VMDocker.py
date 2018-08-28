# coding:utf-8
import time
import psutil
import subprocess
from Controller.setting import *
from Controller.Common import common_log


class VMDocker(object):
    def __init__(self, task_info):
        self._DEBUG = True
        self._local_ip = ''
        self._app_name = task_info['app_name']
        self._vm_name = task_info['docker_name']
        self._taskId = task_info['taskId']

    def _log(self, prefix, msg):
        common_log(self._DEBUG, self._taskId, '[VM ' + self._vm_name + ']', prefix, msg)

    def run_check(self):
        msg = ''

        if not self._app_name:
            msg = 'Must be set app_name'
            self._log('_check error:', msg)
            return False, msg

        mem = psutil.virtual_memory()
        if mem.free < 2.5 * GB:  # < 2.5GB
            msg = 'Free memory must be greater than 2.5GB.'
            self._log('_check error:', msg)
            return False, msg
        else:
            self._log('_check', 'Memory: %.1f' % (mem.free / GB) + ' GB')

        running_dockers = self.ps()
        if len(running_dockers) >= VM_MAX:
            msg = 'The number of starts can not be greater ' + str(VM_MAX)
            self._log('_check error:', msg)
            return False, msg
        else:
            self._log('_check ok', 'Running VMware ' + str(len(running_dockers)))

        return True, msg

    def _make_cmd(self, cmd):
        return VMRUN_BINARY_PATH + ' ' + cmd

    def _make_cmd_login(self, cmd):
        return VMRUN_BINARY_PATH + ' -T ws -gu "win7_64" -gp "zhxg2018" ' + cmd

    def _exec_vmrun_cmd(self, cmdline):
        _stdout = ''
        _stderr = ''
        try:
            self._log('<<vmrun_cmd>> ', cmdline)
            time.sleep(1)
            process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # process.wait()
            (stdout, stderr) = process.communicate()
            _stdout = stdout.decode('gbk')
            _stderr = stderr.decode('gbk')
        except Exception as e:
            self._log('_exec_vmrun_cmd error:', e)
        finally:
            pass

        self._log('stdout:\n', _stdout)
        if _stderr:
            self._log('stderr:\n', _stderr)
            return ''
        else:
            time.sleep(1)
            return _stdout

    def get_local_ip(self):
        return self._exec_vmrun_cmd(self._make_cmd('getGuestIPAddress ' + self.get_vm_image_path(self._vm_name)))

    def get_vm_image_path(self, vm_name):
        if vm_name:
            return '"' + VM_IMAGES_PATH + '\\' + vm_name + '\\' + VMX_NAME + '"'
        else:
            return None

    def set_run_app(self, app_name):
        try:
            f = open(WORK_PATH + '\cmd\\app.conf', 'w')
            f.write(app_name)
            f.close()
            self._log('<<info>> set run app:', app_name)
        except Exception as e:
            self._log('set run app error:', e)
            return False

        guest_path = '"' + WORK_PATH + '\cmd\\app.conf"'
        host_path = '"C:\workspace\pyWorks\AppSimulator\cmd\\app.conf"'
        time.sleep(1)
        ret = self._exec_vmrun_cmd(self._make_cmd_login(
            'CopyFileFromHostToGuest ' + self.get_vm_image_path(self._vm_name) + ' ' + guest_path + ' ' + host_path
        ))
        time.sleep(1)
        if ret.lower().find('error') != -1:
            return False
        else:
            return True

    def stop(self, wait_time=2):
        self._log('<<info>> stop', 'wait: ' + str(wait_time) + 's')
        time.sleep(wait_time)
        self._exec_vmrun_cmd(self._make_cmd("stop " + self.get_vm_image_path(self._vm_name)))
        time.sleep(wait_time)
        return True

    def ps(self, docker_name=None):
        devices = []
        ret = self._exec_vmrun_cmd(self._make_cmd('list'))
        if ret:
            # Total running VMs: 0
            #  or
            # Total running VMs: 1
            # C:\VMware\VM\vm3\Windows 7 x64.vmx
            for s in ret.split('\r\n'):
                if s.startswith('nox') or s.startswith('Nox'):
                    status = STATUS_WAIT if s.split(',')[-1] == '-1' else STATUS_DOCKER_RUN_OK
                    name = s.split(',')[1]

                    if docker_name is None or name == docker_name:
                        devices.append({'name': name, 'status': STATUS_DOCKER_RUN_OK})

        return devices

    def start(self, wait_times=2):
        vm_path = '"' + VM_IMAGES_PATH + '\\' + self._vm_name + '\\' + VMX_NAME + '"'
        time.sleep(wait_times)
        self._exec_vmrun_cmd(self._make_cmd("start " + vm_path))
        time.sleep(wait_times)
        return True


def main(task_info):
    vm = VMDocker(task_info=task_info)
    vm._DEBUG = True
    vm.get_local_ip()
    print(vm.set_run_app('douyin'))
    # return docker.start(wait_times=2)


if __name__ == "__main__":
    # docker_name = sys.argv[1]
    vm_name = 'vm3'
    task = {
        'taskId': 11,
        'app_name': 'miaopai',
        'docker_name': vm_name,
        'timer_no': -1
    }
    main(task_info=task)
    print("Close after 60 seconds.")
    time.sleep(60)
