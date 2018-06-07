import subprocess
from pprint import pprint


class Emulator(object):
    def __init__(self):
        self.EMULATOR_STATUS_RUNNING = 'running'
        self.EMULATOR_STATUS_IDLE = 'idle'
        self._emulator_cnt = 10

    def _make_cmd(self, cmd):
        return 'NoxConsole ' + cmd

    def emulator_quit(self, name):
        self._exec_emulator_cmd(self._make_cmd(" quit -name:" + name))

    def emulator_quit_all(self):
        self._exec_emulator_cmd(self._make_cmd('quitall'))

    def get_emulator_list(self, ):
        devices = []
        ret = self._exec_emulator_cmd(self._make_cmd('list'))
        if ret:
            for s in ret.split('\r\n'):  # 虚拟机名称，标题，顶层窗口句柄，工具栏窗口句柄，绑定窗口句柄，进程PID
                if s.startswith('nox') or s.startswith('Nox'):
                    id = s.split(',')[0]
                    name = s.split(',')[1]
                    status = self.EMULATOR_STATUS_IDLE if s.split(',')[-1] == '-1' else self.EMULATOR_STATUS_RUNNING
                    pid = s.split(',')[-1]
                    devices.append({'id': id, 'name': name, 'status': status, 'pid': pid})

        return devices

    def _exec_emulator_cmd(self, cmdline):
        _stdout = ''
        _stderr = ''
        try:
            print('[emulator_cmd] cmdline: ', cmdline)
            process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            (stdout, stderr) = process.communicate()
            _stdout = stdout.decode('utf8')
            _stderr = stderr.decode('utf8')
        except Exception as e:
            print('[emulator_cmd] Exception:', e)

        print('[emulator_cmd] stdout:', _stdout)
        if _stderr:
            print('[emulator_cmd] stderr:', _stderr)
            return ''
        else:
            return _stdout

    def remove_emulator(self, name):
        self.emulator_quit(name)
        self._exec_emulator_cmd(self._make_cmd("remove -name:" + name))

    def launch_emulator(self, name, force=False):
        found = False
        current_status = self.EMULATOR_STATUS_IDLE
        l = self.get_emulator_list()
        for e in l:
            if e['name'] == name:
                found = True
                current_status = e['status']

        if force:
            self.remove_emulator(name)
            self._exec_emulator_cmd(self._make_cmd("copy -name:" + name + " -from:nox-0"))
            self._exec_emulator_cmd(self._make_cmd('restore -name:' + name + ' -file:"c:\\Nox\\backup\\nox-0.npbk"'))
            self._exec_emulator_cmd(self._make_cmd("launch -name:" + name))
        else:
            if not found:
                self._exec_emulator_cmd(self._make_cmd("copy -name:" + name + " -from:nox-0"))
                self._exec_emulator_cmd(
                    self._make_cmd('restore -name:' + name + ' -file:"c:\\Nox\\backup\\nox-0.npbk"'))
                self._exec_emulator_cmd(self._make_cmd("launch -name:" + name))
            else:
                if current_status == self.EMULATOR_STATUS_IDLE:
                    self._exec_emulator_cmd(self._make_cmd("launch -name:" + name))
                else:  # EMULATOR_STATUS_RUNNING
                    pass


if __name__ == "__main__":
    emulator = Emulator()
    pprint(emulator.get_emulator_list())
    # emulator.removeEmulator('nox-3')
    emulator.launch_emulator(name='nox-3', force=True)
