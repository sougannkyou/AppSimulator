# coding=utf-8
import os

LOCAL_IP = os.getenv('APPSIMULATOR_IP')

MONGODB_SERVER_IP = os.environ["MONGODB_SERVER_IP"]
MONGODB_SERVER_PORT = int(os.environ["MONGODB_SERVER_PORT"])

STATUS_RPC_TIMEOUT = 'rpc_timeout'

STATUS_UNKOWN = 'unkown'

STATUS_WAIT = 'wait'  # wait

STATUS_BUILDING = 'building'  # docker building ...
STATUS_BUILD_OK = 'build_ok'
STATUS_BUILD_NG = 'build_ng'

STATUS_RUNNING = 'running'  # script running ...
STATUS_RUN_OK = 'run_ok'
STATUS_RUN_NG = 'run_ng'
STATUS_SUSPEND = 'suspend'  # task interrupt

SCOPE_TIMES = 1 * 60

RPC_PORT = 8003
GB = 1024 * 1024 * 1024

RPC_SERVER_TIMEOUT = 5
