# coding:utf-8
import time
import subprocess
import importlib
import importlib.util
import aircv as ac
from PIL import ImageGrab
import win32gui
from Controller.setting import *
from Controller.DBLib import MongoDriver
from Controller.NoxConDocker import NoxConDocker
from Controller.NoxConSelenium import NoxConSelenium


# ------------------------ docker task manager ----------------------
class Manager(object):
    def __init__(self):
        self.db = MongoDriver()
        self.db._DEBUG = True
        self._DEBUG = False
        self._work_path = os.getenv('APPSIMULATOR_WORK_PATH')

    def _log(self, prefix, msg):
        if self._DEBUG or prefix.find('error') > 0:
            print('[Docker Manager]', prefix, msg)

    def _check(self):
        if not self._work_path:
            msg = '请设置: APPSIMULATOR_WORK_PATH'
            self._log('_check error', msg)
            return False, msg

    def run_task(self, task):
        _stdout = ''
        _stderr = ''
        try:
            cmdline = 'python ' + task['script']
            self._log('run_task', cmdline)
            time.sleep(1)
            process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # process.wait()
            (stdout, stderr) = process.communicate()
            _stdout = stdout.decode('utf8')
            _stderr = stderr.decode('utf8')
        except Exception as e:
            self._log('run_task exception:', e)

        if _stderr:
            self._log('run_task stderr:\n', _stderr)
            return False
        else:
            self._log('run_task stdout:\n', _stdout)
            time.sleep(1)
            return True

    def run_script(self, task):
        # module_spec = importlib.util.find_spec(task['script'])
        # if module_spec:
        #     module = importlib.util.module_from_spec(module_spec)
        #     module_spec.loader.exec_module(module)
        try:
            module = importlib.import_module('Controller.' + task['script'][:-3])
            module.main()
            self._log('run_script ok', '')
            return True
        except Exception as e:
            self._log('run_script error:', e)
            return False

    # def _find_element(self, hwnd, comment, timeout):
    #     self._PIC_PATH = {
    #         "APP图标": self._work_path + '\\Controller\\images\\' + self._app_name + '\\app_icon.png',
    #         "很抱歉": self._work_path + '\\Controller\\images\\im_sorry.png',
    #     }
    #
    #     self._log('find_element', '尝试在 ' + str(timeout) + 's内匹配: ' + comment)
    #     time.sleep(3)
    #     while timeout > 0:
    #         win32gui.SetForegroundWindow(hwnd)
    #         left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    #         app_bg_box = (left, top, right, bottom)
    #
    #         im = ImageGrab.grab(app_bg_box)
    #         im.save(self._work_path + '\\Controller\\images\\start.png')
    #
    #         img_capture = ac.imread(self._work_path + '\\Controller\\images\\start.png')
    #         img_obj = ac.imread(self._PIC_PATH[comment])
    #         pos = ac.find_template(img_capture, img_obj)
    #         if pos and pos['confidence'] > 0.9:
    #             self._log('find_element', '已匹配到:' + comment + ' ' + str(timeout) + 's')
    #             return True
    #         else:
    #             time.sleep(1)
    #             timeout = timeout - 1
    #             self._log('find_element', '未匹配到:' + comment + ', 重试剩余: ' + str(timeout) + 's')
    #
    #     return False

    def on_success(self, docker):
        time.sleep(10)
        docker.shake(3)
        docker.set_docker_name()
        # port = docker.get_port()
        return True

    def on_error(self, docker, retry_cnt=0):
        while retry_cnt > 0:
            ret, msg = docker.create(force=True)
            if ret:
                ret = docker.start(wait_time=30)
                if ret:  # start success
                    return True
            else:
                retry_cnt -= 1
        else:
            docker.stop()
            self.check_docker_stop(docker, retry=True, wait_time=30)

        return False

    def check_docker_run(self, app_name, docker_name, wait_time=30):
        driver = NoxConSelenium(app_name=app_name, docker_name=docker_name)
        # driver._DEBUG = True
        driver._PIC_PATH = {
            "APP图标": self._work_path + '\\Controller\\images\\' + app_name + '\\app_icon.png',
            "很抱歉": self._work_path + '\\Controller\\images\\im_sorry.png',
        }

        while wait_time > 0:
            ret = driver.pre_check()
            if ret:
                self._log('check_docker_run', docker_name + ' ok.')
                ret = driver.find_element(comment='很抱歉', timeout=30)  # 匹配“很抱歉”字样
                if ret:
                    return False
                else:
                    return driver.find_element(comment='APP图标', timeout=30)  # 可匹配到app图标

            else:  # hwnd is 0 if not found
                time.sleep(1)
                wait_time -= 1
                self._log('check_docker_run', '等待 ' + docker_name + ' 窗口创建，剩余：' + str(wait_time) + 's')

    def check_docker_stop(self, docker, retry=False, wait_time=30):
        while wait_time > 0:
            hwnd = win32gui.FindWindow(None, docker.get_name())
            if hwnd:  # hwnd is 0 if not found
                time.sleep(1)
                self._log('check_docker_stop', '正在等待 ' + docker.get_name() + ' 停止，剩余：' + str(wait_time) + 's')
                wait_time -= 1
            else:  # not found the window
                self._log('check_docker_stop', '已停止：' + str(wait_time) + 's')
                break

        if retry and wait_time == 0:  # retry
            # docker._cmd_kill_task(self._docker_name)  # 不能强杀，会造成 ERR：1037
            docker.stop()

        time.sleep(10)
        return True

    def start_tasks(self):
        # 1)docker running -> 2)docker run ok(ng) -> 3)script running -> 4)script run ok(ng)
        while True:
            task = self.db.task_get_one_for_run()
            if task:
                docker_name = 'nox-' + str(task['taskId'])
                app_name = task['app_name']

                task['status'] = STATUS_DOCKER_RUNNING
                self.db.task_change_status(task)
                # 1)docker running
                docker = NoxConDocker(app_name=task['app_name'], docker_name=docker_name)
                docker.run(force=True)  # docker run: create and start
                ret = self.check_docker_run(docker_name, app_name, wait_time=30)
                if ret:
                    ret = self.on_success(docker=docker)
                else:
                    ret = self.on_error(docker=docker, retry_cnt=2)

                status = STATUS_DOCKER_RUN_OK if ret else STATUS_DOCKER_RUN_NG

                # 2)docker run ok(ng)
                docker_info = {'_id': self.db.docker_create(task), 'status': status}
                self.db.docker_change_status(docker_info)
                task['status'] = status
                self.db.task_change_status(task)

                if ret:
                    self.db.task_set_docker(task, docker_info)  # bind docker to task
                    # 3)script running
                    ret = self.run_script(task)
                    task['status'] = STATUS_SCRIPT_RUN_OK if ret else STATUS_SCRIPT_RUN_NG

                    # 4)script run ok(ng)
                    self.db.task_change_status(task)

                # break
            else:
                time.sleep(1 * 60)


if __name__ == '__main__':
    manager = Manager()
    manager._DEBUG = True
    manager.start_tasks()
