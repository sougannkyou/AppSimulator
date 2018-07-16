# coding=utf-8
import os

APPSIMULATOR_MODE = os.getenv('APPSIMULATOR_MODE')
LOCAL_IP = os.getenv('APPSIMULATOR_IP')
WORK_PATH = os.getenv('APPSIMULATOR_WORK_PATH')
SCOPE_TIMES = 1 * 60

GB = 1024 * 1024 * 1024

# ---------------------- db -----------------------------
MONGODB_SERVER_IP = os.environ["MONGODB_SERVER_IP"]
MONGODB_SERVER_PORT = int(os.environ["MONGODB_SERVER_PORT"])

REDIS_SERVER = 'redis://' + os.environ["REDIS_SERVER_IP"] + '/11'

# ---------------------- status -----------------------------
STATUS_RPC_TIMEOUT = 'rpc_timeout'

STATUS_UNKOWN = 'unkown'

STATUS_WAIT = 'wait'  # wait

STATUS_DOCKER_RUN = 'docker_run'  # docker running(create and run) ...
STATUS_DOCKER_RUN_OK = 'docker_run_ok'
STATUS_DOCKER_RUN_NG = 'docker_run_ng'

STATUS_SCRIPT_START = 'script_start'  # script running ...
STATUS_SCRIPT_START_OK = 'script_start_ok'
STATUS_SCRIPT_START_NG = 'script_start_ng'
STATUS_SCRIPT_SUSPEND = 'script_suspend'  # task interrupt

# ---------------------- rpc -----------------------------
RPC_SERVER_TIMEOUT = 30
RPC_PORT = 8003

# ---------------------- adb -----------------------------
NOX_BIN_PATH = 'C:\\Nox\\bin'
ADB_BINARY_PATH = NOX_BIN_PATH + '\\nox_adb.exe'
CONSOLE_BINARY_PATH = NOX_BIN_PATH + '\\NoxConsole.exe'
TIMER = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]

# ---------------------- VMware -----------------------------
VMRUN_BINARY_PATH = 'C:\\VMware\\Workstation\\vmrun.exe'
VM_IMAGES_PATH = 'C:\\VMware\\VM'
VMX_NAME = 'Windows 7 x64.vmx'
VM_MAX = 5

# ---------------------- ControllerManager -----------------------------
CHECK_TIMES = 10  # min
