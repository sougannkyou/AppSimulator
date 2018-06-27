# coding:utf-8
import time
from datetime import datetime
import re
import random
import subprocess

CONSOLE_BINARY_PATH = 'C:\\Nox\\bin\\NoxConsole.exe'
TIMER = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27]


class NoxConADB(object):
    REBOOT_RECOVERY = 1
    REBOOT_BOOTLOADER = 2

    DEFAULT_TCP_HOST = "localhost"
    DEFAULT_TCP_PORT = 62001  # 5555

    def __init__(self, docker_name):
        self._DEBUG = False
        self._stdout = None
        self._stderr = None
        self._devices = None
        self.__target = None
        self._console_binary = CONSOLE_BINARY_PATH
        self._docker_name = docker_name

    def _log(self, prefix, msg):
        if self._DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
            print('[NoxConADB]', prefix, msg)

    def _clean(self):
        self._stdout = None
        self._stderr = None

    def _get_phone_number(self):
        num = '186'
        for i in range(8):
            num += str(random.randrange(0, 9))
        return num

    def _luhn_residue(self, digits):
        return sum(sum(divmod(int(d) * (1 + i % 2), 10)) for i, d in enumerate(digits[::-1])) % 10

    def _get_imei(self, N):
        part = ''.join(str(random.randrange(0, 9)) for _ in range(N - 1))
        res = self._luhn_residue('{}{}'.format(part, 0))
        return '{}{}'.format(part, -res % 10)

    def get_docker_name(self):
        ret = self.adb_shell("getprop persist.nox.docker_name")
        if ret:
            self._docker_name = ret.replace('\r\r\n', '')

        return self._docker_name

    def get_new_phone(self):
        imei = self._get_imei(15)
        phone_number = self._get_phone_number()
        self.adb_shell("setprop persist.nox.modem.imei " + imei)
        # "adb shell setprop persist.nox.modem.imsi 460000000000000"
        self.adb_shell("setprop persist.nox.modem.phonumber " + phone_number)
        # "adb shell setprop persist.nox.modem.serial 89860000000000000000"
        return True

    def get_android_version(self):
        self._clean()
        self.adb_shell("getprop ro.build.version.release")
        return self._stdout.decode('utf8')

    def set_gps(self, latitude, longitude):
        self.adb_shell("setprop persist.nox.gps.latitude " + str(latitude))
        self.adb_shell("setprop persist.nox.gps.longitude " + str(longitude))
        return True

    def start_web(self, url):
        # adb shell am start -a android.intent.action.VIEW -d http://testerhome.com
        self.adb_shell("am start -a android.intent.action.VIEW -d " + url)
        return True

    def get_stdout(self):
        return self._stdout

    def get_stderr(self):
        return self._stderr

    def get_new_error(self):
        """
        Was failed the last command?
        """
        if self._stdout is None and self._stderr is not None:
            return True
        return False

    def _make_command(self, cmd):
        # NoxConsole.exe adb -name:nox-22 -command:"version"
        cmd_str = self._console_binary + ' adb -name:' + self._docker_name + ' -command:"' + cmd + '"'
        return cmd_str

    def adb_cmd(self, cmd, timer_no=0):
        self._clean()
        try:
            cmdline = self._make_command(cmd)
            self._log('[adb_cmd]<<info>>', cmdline)
            if timer_no:
                time.sleep(30 + TIMER[timer_no] - datetime.now().second % 30)

            process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            (stdout, stderr) = process.communicate()
            self._stdout = stdout.decode('utf8').replace('\r', '').replace('\n', '')
            self._stderr = stderr.decode('utf8').replace('\r', '').replace('\n', '')
        except Exception as e:
            self._log('[adb_cmd] error:', e)

        return

    def adb_shell(self, cmd, timer_no=0):
        self._clean()
        self.adb_cmd('shell ' + cmd, timer_no)
        return self._stdout

    def get_adb_version(self):
        ret = None
        self.adb_cmd("version")
        try:
            if self._stdout.find('device not exist') == -1:
                ret = self._stdout
                self._log('<<info>> get_adb_version ok:\n', ret)
        except Exception as e:
            self._log('get_adb_version error:', e)
        return ret

    def wait_for_device(self, timeout=30):
        """
        Block until device is online
        adb wait-for-device
        """
        ver = None
        while timeout > 0:
            ver = self.get_adb_version()
            if ver and ver.startswith('Android Debug Bridge'):
                self._log('<<info>> wait_for_device:', 'ok')
                break
            else:
                self._log('<<info>> wait_for_device:', str(timeout) + 's')
                timeout -= 5
                time.sleep(5)

        return True if ver else False

    def check_path(self):
        """
        Intuitive way to verify the ADB path
        """
        if self.get_adb_version() is None:
            return False
        return True

    def start_server(self):
        self._clean()
        self.adb_cmd('start-server')
        return self._stdout

    def kill_server(self):
        """
        Kills ADB server
        adb kill-server
        """
        self._clean()
        self.adb_cmd('kill-server')

    def restart_server(self):
        """
        Restarts ADB server
        """
        self.kill_server()
        return self.start_server()

    def restore_file(self, file_name):
        """
        Restore device contents from the <file> backup archive
        adb restore <file>
        """
        self._clean()
        self.adb_cmd('restore %s' % file_name)
        return self._stdout

    def get_adb_help(self):
        self._clean()
        self.adb_cmd('help')
        return self._stdout

    def get_target_device(self):
        """
        Returns the selected device to work with
        """
        return self.__target

    def get_state(self):
        """
        adb get-state
        设备状态:
            device：设备正常连接
            offline：连接出现异常，设备无响应
            unknown：没有连接设备
        """
        self._clean()
        self.adb_cmd('get-state')
        return self._stdout

    def get_serialno(self):
        """
        Get serialno from target device
        adb get-serialno
        """
        self._clean()
        self.adb_cmd('get-serialno')
        return self._stdout

    def reboot_device(self, mode):
        """
        Reboot the target device
        adb reboot recovery/bootloader
        """
        self._clean()
        if not mode in (self.REBOOT_RECOVERY, self.REBOOT_BOOTLOADER):
            self._stderr = "mode must be REBOOT_RECOVERY/REBOOT_BOOTLOADER"
            return self._stdout

        self.adb_cmd("reboot %s" % "recovery" if mode == self.REBOOT_RECOVERY else "bootloader")
        return self._stdout

    def set_adb_root(self, mode):
        """
        restarts the adbd daemon with root permissions
        adb root
        """
        self._clean()
        self.adb_cmd('root')
        return self._stdout

    def set_system_rw(self):
        """
        Mounts /system as rw
        adb remount
        """
        self._clean()
        self.adb_cmd("remount")
        return self._stdout

    def get_remote_file(self, remote, local):
        """
        Pulls a remote file
        adb pull remote local
        """
        self._clean()
        self.adb_cmd('pull \"%s\" \"%s\"' % (remote, local))
        if "bytes in" in self._stderr:
            self._stdout = self._stderr
            self._stderr = None
        return self._stdout

    def push_to_device(self, local, remote):
        """
        Push a local file
        adb push local remote
        """
        self._clean()
        self.adb_cmd('push \"%s\" \"%s\"' % (local, remote))
        return self._stdout

    def listen_usb(self):
        """
        Restarts the adbd daemon listening on USB
        adb usb
        """
        self._clean()
        self.adb_cmd("usb")
        return self._stdout

    def listen_tcp(self, port=DEFAULT_TCP_PORT):
        """
        Restarts the adbd daemon listening on the specified port
        adb tcpip <port>
        """
        self._clean()
        self.adb_cmd("tcpip %s" % port)
        return self._stdout

    def get_bugreport(self):
        """
        Return all information from the device that should be included in a bug report
        adb bugreport
        """
        self._clean()
        self.adb_cmd("bugreport")
        return self._stdout

    def get_jdwp(self):
        """
        List PIDs of processes hosting a JDWP transport
        adb jdwp
        """
        self._clean()
        self.adb_cmd("jdwp")
        return self._stdout

    def get_logcat(self, lcfilter=""):
        """
        View device log
        adb logcat <filter>
        """
        self._clean()
        self.adb_cmd("logcat %s" % lcfilter)
        return self._stdout

    def run_emulator(self, cmd=""):
        """
        Run emulator console command
        """
        self._clean()
        self.adb_cmd("emu %s" % cmd)
        return self._stdout

    def connect_remote(self, host=DEFAULT_TCP_HOST, port=DEFAULT_TCP_PORT):
        """
        Connect to a device via TCP/IP
        adb connect host:port
        """
        self._clean()
        self.adb_cmd("connect %s:%s" % (host, port))
        return self._stdout

    def disconnect_remote(self, host=DEFAULT_TCP_HOST, port=DEFAULT_TCP_PORT):
        """
        Disconnect from a TCP/IP device
        adb disconnect host:port
        """
        self._clean()
        self.adb_cmd("disconnect %s:%s" % (host, port))
        return self._stdout

    def ppp_over_usb(self, tty=None, params=""):
        """
        Run PPP over USB
        adb ppp <tty> <params>
        """
        self._clean()
        if tty is None:
            return self._stdout

        cmd = "ppp %s" % tty
        if params != "":
            cmd += " %s" % params

        self.adb_cmd(cmd)
        return self._stdout

    def sync_directory(self, directory=""):
        """
        Copy host->device only if changed (-l means list but don't copy)
        adb sync <dir>
        """
        self._clean()
        self.adb_cmd("sync %s" % directory)
        return self._stdout

    def forward_socket(self, local=None, remote=None):
        """
        Forward socket connections
        adb forward <local> <remote>
        """
        self._clean()
        if local is None or remote is None:
            return self._stdout
        self.adb_cmd("forward %s %s" % (local, remote))
        return self._stdout

    def uninstall(self, package=None, keepdata=False):
        """
        Remove this app package from the device
        adb uninstall [-k] package
        """
        self._clean()
        if package is None:
            return self._stdout
        cmd = "uninstall %s" % (package if keepdata is True else "-k %s" % package)
        self.adb_cmd(cmd)
        return self._stdout

    def install(self, fwdlock=False, reinstall=False, sdcard=False, pkgapp=None):
        """
        Push this package file to the device and install it
        adb install [-l] [-r] [-s] <file>
        -l -> forward-lock the app
        -r -> reinstall the app, keeping its data
        -s -> install on sdcard instead of internal storage
        """

        self._clean()
        if pkgapp is None:
            return self._stdout

        cmd = "install "
        if fwdlock is True:
            cmd += "-l "
        if reinstall is True:
            cmd += "-r "
        if sdcard is True:
            cmd += "-s "

        self.adb_cmd("%s %s" % (cmd, pkgapp))
        return self._stdout

    def find_binary(self, name=None):
        """
        Look for a binary file on the device
        """
        self.adb_shell("which %s" % name)

        if self._stdout is None:  # not found
            self._stderr = "'%s' was not found" % name
        elif self._stdout.strip() == "which: not found":  # which binary not available
            self._stdout = None
            self._stderr = "which binary not found"
        else:
            self._stdout = self._stdout.strip()

        return self._stdout

    def get_screen_size(self):
        """
        获取手机屏幕大小
        """
        size_str = self.adb_shell('wm size')
        m = re.search(r'(\d+)x(\d+)', size_str)
        if m:
            return "{height}x{width}".format(height=m.group(2), width=m.group(1))
        return "1920x1080"


if __name__ == "__main__":
    my = NoxConADB('nox-1')
    my._DEBUG = True

    print(my.get_adb_version())
    print(my.get_serialno())
    print(my.adb_shell('input keyevent 4'))
