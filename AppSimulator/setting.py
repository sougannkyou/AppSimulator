# coding=utf-8
import os

PAGE_SIZE = 20

REDIS_SERVER = 'redis://' + os.environ["REDIS_SERVER_IP"] + '/11'  # 'redis://172.16.55.155'
REDIS_SERVER_RESULT = 'redis://' + os.environ["REDIS_SERVER_IP"] + '/10'

MONGODB_SERVER_IP = os.environ["MONGODB_SERVER_IP"]  # "172.16.55.155"
MONGODB_SERVER_PORT = int(os.environ["MONGODB_SERVER_PORT"])

STATUS_RPC_TIMEOUT = 'rpc_timeout'
STATUS_UNKOWN = 'unkown'
STATUS_WAIT = 'wait'
STATUS_BUILD = 'build'  # build a docker
STATUS_RUNNING = 'running'  # docker build ok, run script
STATUS_SUSPEND = 'suspend'  # task interrupt
STATUS_SUCCESS = 'success'  # task run ok
STATUS_FAILURE = 'failure'  # task run failed

TASK_TYPE_ONCE = 'once'
TASK_TYPE_NEVER = 'never'

SCOPE_TIMES = 1 * 60

RPC_SERVER_TIMEOUT = 5
