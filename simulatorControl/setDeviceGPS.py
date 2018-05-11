import os


def setDeviceGPS(deviceId, latitude, longitude):
    print(latitude, longitude)  # 39.6099202570, 118.1799316404
    p = os.popen("adb shell setprop persist.nox.gps.latitude " + latitude)
    print(p.read())

    p = os.popen("adb shell setprop persist.nox.gps.longitude " + longitude)
    print(p.read())
