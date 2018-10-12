# coding=utf-8
import os

PAGE_SIZE = 20

# ---------------------- db -----------------------------
REDIS_SERVER = os.environ["REDIS_SERVER_IP"]
# REDIS_SERVER_RESULT = os.environ["REDIS_SERVER_IP"]
REDIS_SERVER_RESULT = '192.168.174.130'

MONGODB_SERVER_IP = os.environ["MONGODB_SERVER_IP"]
MONGODB_SERVER_PORT = int(os.environ["MONGODB_SERVER_PORT"])

# ---------------------- status -----------------------------
STATUS_RPC_TIMEOUT = 'rpc_timeout'

STATUS_UNKOWN = 'unkown'

STATUS_WAIT = 'wait'

STATUS_DOCKER_RUN = 'docker_run'  # docker running(create and run) ...
STATUS_DOCKER_RUN_OK = 'docker_run_ok'
STATUS_DOCKER_RUN_NG = 'docker_run_ng'

STATUS_SCRIPT_START = 'script_start'  # script running ...
STATUS_SCRIPT_START_OK = 'script_start_ok'
STATUS_SCRIPT_START_NG = 'script_start_ng'
STATUS_SCRIPT_SUSPEND = 'script_suspend'  # task interrupt

# ---------------------- task -----------------------------
TASK_TYPE_ONCE = 'once'
TASK_TYPE_NEVER = 'never'

SCOPE_TIMES = 1 * 60

# ---------------------- rpc -----------------------------
RPC_SERVER_TIMEOUT = 30
RPC_DEBUG = False

TIMER = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]
