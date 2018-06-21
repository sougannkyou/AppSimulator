# coding=utf-8
import os

MONGODB_SERVER_IP = os.environ["MONGODB_SERVER_IP"]
MONGODB_SERVER_PORT = int(os.environ["MONGODB_SERVER_PORT"])

STATUS_RPC_TIMEOUT = 'rpc_timeout'
STATUS_UNKOWN = 'unkown'
STATUS_WAIT = 'wait'
STATUS_BUILD = 'build'
STATUS_RUNNING = 'running'
STATUS_SUSPEND = 'suspend'

SCOPE_TIMES = 1 * 60

RPC_SERVER_TIMEOUT = 5
