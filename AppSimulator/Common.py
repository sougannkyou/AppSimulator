import time
from datetime import datetime


def now_timestamp():
    return int(datetime.now().timestamp())


def seconds_format(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{h:0>2d}:{m:0>2d}:{s:0>2d}".format(h=hours, m=minutes, s=seconds)


def string2timestamp(s, format_str="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(datetime.strptime(s, format_str).timetuple()))


def timestamp2string(t, format_str="%Y-%m-%d %H:%M:%S"):
    return datetime.fromtimestamp(t).strftime(format_str)


def common_log(_DEBUG, func, prefix, msg):
    if _DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
        print(datetime.now().strftime('%H:%M:%S') + '[' + func + ']', prefix, msg)
