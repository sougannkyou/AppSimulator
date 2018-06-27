# coding=utf-8
import os


PAGE_SIZE = 20

# ---------------------- db -----------------------------
REDIS_SERVER = 'redis://' + os.environ["REDIS_SERVER_IP"] + '/11'
REDIS_SERVER_RESULT = 'redis://' + os.environ["REDIS_SERVER_IP"] + '/10'

MONGODB_SERVER_IP = os.environ["MONGODB_SERVER_IP"]
MONGODB_SERVER_PORT = int(os.environ["MONGODB_SERVER_PORT"])

# ---------------------- status -----------------------------
STATUS_RPC_TIMEOUT = 'rpc_timeout'

STATUS_UNKOWN = 'unkown'

STATUS_WAIT = 'wait'

STATUS_DOCKER_RUNNING = 'docker_running'  # docker running(create and run) ...
STATUS_DOCKER_RUN_OK = 'docker_run_ok'
STATUS_DOCKER_RUN_NG = 'docker_run_ng'

STATUS_SCRIPT_RUNNING = 'script_running'  # script running ...
STATUS_SCRIPT_RUN_OK = 'script_run_ok'
STATUS_SCRIPT_RUN_NG = 'script_run_ng'
STATUS_SCRIPT_RUN_SUSPEND = 'script_run_suspend'  # task interrupt

# ---------------------- task -----------------------------
TASK_TYPE_ONCE = 'once'
TASK_TYPE_NEVER = 'never'

SCOPE_TIMES = 1 * 60

# ---------------------- rpc -----------------------------
RPC_SERVER_TIMEOUT = 5
RPC_DEBUG = False
