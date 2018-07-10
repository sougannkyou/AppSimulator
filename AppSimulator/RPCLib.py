import socket
import xmlrpc.client
from AppSimulator.setting import *
from AppSimulator.Common import common_log

RPC_DEBUG = True


# ------------------------ server rpc lib ----------------------
def _log(prefix, msg):
    common_log(RPC_DEBUG, 'Web server rpc', prefix, msg)


def _rpc_server(ip, port):
    return "http://" + ip + ":" + str(port)


def rpc_stop_script(ip, port, deviceId):
    _log('rpc_stop_script', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.stopScript()
    socket.setdefaulttimeout(None)
    _log('rpc_stop_script ret:', ret)
    return ret


def rpc_start_script(ip, port, deviceId):
    _log('rpc_start_script', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.startScript()
    socket.setdefaulttimeout(None)
    _log('rpc_start_script ret:', ret)
    return ret


def rpc_restart(ip, port, deviceId):
    _log('rpc_restart', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.restartDevice(deviceId)
    socket.setdefaulttimeout(None)
    _log('rpc_restart ret:', ret)
    return ret


def rpc_quit(ip, port, deviceId):
    _log('rpc_quit', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.quitApp()
    socket.setdefaulttimeout(None)
    _log('rpc_quit end:', ret)
    return ret


def rpc_get_status(ip, port):
    _log('rpc_get_status', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.getRpcServerStatus()
    socket.setdefaulttimeout(None)
    _log('rpc_get_status ret:', ret)
    return ret


def rpc_set_gps(ip, port, deviceId, latitude, longitude):
    _log('rpc_set_gps', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.setDeviceGPS(deviceId, latitude, longitude)
    socket.setdefaulttimeout(None)
    _log('rpc_set_gps ret:', ret)
    return ret


def can_add_task(ip, port):
    _log('can_add_task', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.can_add_task()
    socket.setdefaulttimeout(None)
    _log('can_add_task ret:', ret)
    return ret


def rpc_get_running_docker_cnt(ip, port):
    _log('get_running_docker_cnt', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.get_running_docker_cnt()
    socket.setdefaulttimeout(None)
    _log('get_running_docker_cnt ret:', ret)
    return int(ret)


if __name__ == '__main__':
    _ip = '172.16.253.232'
    _port = 8003
    can_add_task(_ip, _port)
