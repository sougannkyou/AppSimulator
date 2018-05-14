# coding=utf8
import os, time
from xmlrpc.server import SimpleXMLRPCServer


def resetDevice(deviceId):
    print("resetDeviceAPI start.", deviceId)
    p = os.popen("D:\\Nox\\bin\\Nox.exe -quit")
    print("Nox.exe -quit :", p.read())

    p = os.popen("tasklist | findstr 'Nox'")
    print("tasklist | findstr 'Nox' :", p.read())

    time.sleep(10)
    p = os.popen("D:\\Nox\\bin\\Nox.exe")
    print("Nox.exe :", p.read())
    return True


def setDeviceGPS(deviceId, latitude, longitude):
    print(deviceId, latitude, longitude)  # 39.6099202570, 118.1799316404
    p = os.popen("adb shell setprop persist.nox.gps.latitude " + latitude)
    print(p.read())

    p = os.popen("adb shell setprop persist.nox.gps.longitude " + longitude)
    print(p.read())
    return True

server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(resetDevice, "resetDevice")
server.register_function(setDeviceGPS, 'setDeviceGPS')
server.serve_forever()
