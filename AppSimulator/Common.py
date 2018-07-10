from datetime import datetime


def common_log(_DEBUG, func, prefix, msg):
    if _DEBUG or prefix.find('error') != -1 or prefix.find('<<info>>') != -1:
        print(datetime.now().strftime('%H:%M:%S') + '[' + func + ']', prefix, msg)
