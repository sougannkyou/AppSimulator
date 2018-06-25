# coding:utf-8
import time
import subprocess
import importlib
import importlib.util
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
        if self._DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
            print('[Controller Manager]', prefix, msg)

    def _check(self):
        if not self._work_path:
            msg = '请设置: APPSIMULATOR_WORK_PATH'
            self._log('_check error', msg)
            return False, msg

    def run_script(self, task, docker_name):
        _stdout = ''
        _stderr = ''
        try:
            cmdline = 'python ' + task['script'] + ' ' + docker_name
            self._log('run_task', cmdline)
            time.sleep(1)
            process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # process.wait()
            (stdout, stderr) = process.communicate()
            _stdout = stdout.decode('utf8')
            _stderr = stderr.decode('utf8')
        except Exception as e:
            self._log('<<error>> run_script:', e)

        if _stderr:
            self._log('run_script stderr:\n', _stderr)
            return False
        else:
            self._log('run_script stdout:\n', _stdout)
            time.sleep(1)
            return True

    def __run_script(self, task, docker_name):
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

    def docker_run_success(self, docker):
        self._log('<<info>> docker_run_success', docker.get_name())
        time.sleep(5)
        # docker.shake(3)
        # docker.set_docker_name()
        # port = docker.get_port()
        return True

    def docker_run_error(self, docker, retry_cnt=0):
        self._log('<<info>> docker_run_error:', docker.get_name() + ' retry:' + str(retry_cnt))
        while retry_cnt > 0:
            ret, msg = docker.create(force=True)
            if ret:
                ret = docker.start(timeout=2)
                if ret:  # start success
                    return True
            else:
                retry_cnt -= 1
        else:
            docker.stop()
            self.check_docker_stop(docker, retry=True, wait_time=30)

        return False

    def check_docker_run(self, app_name, docker_name, timeout=60):
        driver = NoxConSelenium(app_name=app_name, docker_name=docker_name)
        driver.set_comment_to_pic({
            "APP图标": self._work_path + '\\Controller\\images\\' + app_name + '\\app_icon.png',
            "很抱歉": self._work_path + '\\Controller\\images\\im_sorry.png',
        })

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

    def check_docker_stop(self, docker, retry=False, wait_time=30):
        while wait_time > 0:
            hwnd = win32gui.FindWindow(None, docker.get_name())
            if hwnd:  # hwnd is 0 if not found
                time.sleep(1)
                self._log('<<info>> check_docker_stop', '正在等待 ' + docker.get_name() + ' 停止，剩余：' + str(wait_time) + 's')
                wait_time -= 1
            else:  # not found the window
                self._log('<<info>> check_docker_stop', '已停止：' + str(wait_time) + 's')
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

                # 1)docker running
                task['status'] = STATUS_DOCKER_RUNNING
                self.db.task_change_status(task)
                docker = NoxConDocker(app_name=task['app_name'], docker_name=docker_name)
                ret = docker.run(force=True)  # docker run: create and start
                if ret:
                    ret = self.check_docker_run(app_name=app_name, docker_name=docker_name, timeout=60)
                    if ret:
                        ret = self.docker_run_success(docker=docker)
                    else:
                        ret = self.docker_run_error(docker=docker, retry_cnt=2)

                docker = None  # NoxConDocker.__del__
                status = STATUS_DOCKER_RUN_OK if ret else STATUS_DOCKER_RUN_NG

                # 2)docker run ok(ng)
                docker_info = {'_id': self.db.docker_create(task), 'status': status}
                self.db.docker_change_status(docker_info)
                task['status'] = status
                self.db.task_change_status(task)

                if ret:
                    self.db.task_set_docker(task, docker_info)  # bind docker to task
                    # 3)script running
                    ret = self.run_script(task=task, docker_name=docker_name)
                    task['status'] = STATUS_SCRIPT_RUN_OK if ret else STATUS_SCRIPT_RUN_NG

                    # 4)script run ok(ng)
                    self.db.task_change_status(task)

                # break
            else:
                self._log('<<info>> start_tasks', 'not found wait task, sleep 60s.')
                time.sleep(1 * 60)


if __name__ == '__main__':
    manager = Manager()
    manager._DEBUG = True
    manager.start_tasks()
