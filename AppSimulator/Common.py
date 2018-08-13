from datetime import datetime


def times_format(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{h:0>2d}:{m:0>2d}:{s:0>2d}".format(h=hours, m=minutes, s=seconds)


def common_log(_DEBUG, func, prefix, msg):
    if _DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
        print(datetime.now().strftime('%H:%M:%S') + '[' + func + ']', prefix, msg)
