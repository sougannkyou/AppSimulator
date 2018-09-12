import time
from datetime import datetime


def now_timestamp():
    return int(datetime.now().timestamp())


def seconds_format(seconds):
    if isinstance(seconds, int) and seconds > 0:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{h:0>2d}:{m:0>2d}:{s:0>2d}".format(h=hours, m=minutes, s=seconds)
    elif seconds == 0:
        return '0'
    else:
        return 'N/A'


def spend_time_score(seconds):
    if seconds <= 2 * 60:  # 2min
        score = 100
    elif seconds <= 5 * 60:  # 5min
        score = 80
    elif seconds <= 30 * 60:  # 30min
        score = 60
    elif seconds <= 2 * 60 * 60:  # 2h
        score = 40
    elif seconds <= 12 * 60 * 60:  # 12h
        score = 20
    else:  # >12h
        score = 0

    return score


def string2timestamp(s, format_str="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(datetime.strptime(s, format_str).timetuple()))


def timestamp2string(t, format_str="%Y-%m-%d %H:%M:%S"):
    if isinstance(t, int) and t > 0 and t != 9999999999:
        return datetime.fromtimestamp(t).strftime(format_str)
    else:
        return ''


def common_log(_DEBUG, func, prefix, msg):
    if _DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
        print(datetime.now().strftime('%H:%M:%S') + '[' + func + ']', prefix, msg)
