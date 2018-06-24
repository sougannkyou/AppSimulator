# coding=utf-8
import os

LOCAL_IP = os.getenv('APPSIMULATOR_IP')

MONGODB_SERVER_IP = os.environ["MONGODB_SERVER_IP"]
MONGODB_SERVER_PORT = int(os.environ["MONGODB_SERVER_PORT"])

STATUS_RPC_TIMEOUT = 'rpc_timeout'

STATUS_UNKOWN = 'unkown'

STATUS_WAIT = 'wait'  # wait

STATUS_DOCKER_RUNNING = 'docker_running'  # docker running(create and run) ...
STATUS_DOCKER_RUN_OK = 'docker_run_ok'
STATUS_DOCKER_RUN_NG = 'docker_run_ng'

STATUS_SCRIPT_RUNNING = 'script_running'  # script running ...
STATUS_SCRIPT_RUN_OK = 'script_run_ok'
STATUS_SCRIPT_RUN_NG = 'script_run_ng'
STATUS_SCRIPT_RUN_SUSPEND = 'script_run_suspend'  # task interrupt

SCOPE_TIMES = 1 * 60

RPC_PORT = 8003
GB = 1024 * 1024 * 1024

RPC_SERVER_TIMEOUT = 5
