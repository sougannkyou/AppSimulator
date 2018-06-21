import socket
import xmlrpc.client
from AppSimulator.setting import *

_DEBUG = True

# ------------------------ server rpc lib ----------------------
def _log(prefix, msg):
    if _DEBUG:
        print(prefix, msg)


def _rpc_server(ip, port):
    return "http://" + ip + ":" + str(port)


def rpc_stop_script(ip, port, deviceId):
    _log('rpc_stop_script', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.stopScript()
    socket.setdefaulttimeout(None)
    _log('rpc_stop_script end:', ret)
    return ret


def rpc_start_script(ip, port, deviceId):
    _log('rpc_start_script', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.startScript()
    socket.setdefaulttimeout(None)
    _log('rpc_start_script end:', ret)
    return ret


def rpc_restart(ip, port, deviceId):
    _log('rpc_restart', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.restartDevice(deviceId)
    socket.setdefaulttimeout(None)
    _log('rpc_restart end:', ret)
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
    _log('rpc_get_status end:', ret)
    return ret


def rpc_set_gps(ip, port, deviceId, latitude, longitude):
    _log('rpc_set_gps', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.setDeviceGPS(deviceId, latitude, longitude)
    socket.setdefaulttimeout(None)
    _log('rpc_set_gps end:', ret)
    return ret


def rpc_get_free_mem(ip, port):
    _log('rpc_get_free_mem', 'start')
    socket.setdefaulttimeout(RPC_SERVER_TIMEOUT)
    with xmlrpc.client.ServerProxy(_rpc_server(ip, port)) as proxy:
        ret = proxy.get_free_mem()
    socket.setdefaulttimeout(None)
    _log('rpc_get_free_mem end:', ret)
    return float(ret)
