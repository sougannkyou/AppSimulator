# coding:utf-8
import os
from datetime import datetime
import ftplib

DEBUG_ENV = False

# FTP_PORT = 14147
FTP_PORT = 21


def ftp_upload(local_file, remote_dir, remote_file):
    host = os.getenv('APPSIMULATOR_IP')
    username = 'ControllerManager'
    password = 'zhxg2018'
    start = datetime.now()
    f = ftplib.FTP(host)
    f.port = FTP_PORT
    f.login(username, password)
    f.cwd('images/VM/vm1')
    print("FTP当前路径:", f.pwd())
    # print('size:', f.size('capture3.png'))
    # try:
    #     f.rename('capture2.png', 'capture3.png')
    # except Exception as e:
    #     print("rename:", e)
    # try:
    #     f.rename('capture1.png', 'capture2.png')
    # except Exception as e:
    #     print("rename:", e)
    # try:
    #     f.rename('capture.png', 'capture1.png')
    # except Exception as e:
    #     print("rename:", e)

    bufsize = 200 * 1024  # 设置缓冲器大小
    fp = open(local_file, 'rb')
    # f.set_debuglevel(2)
    # try:
    #     f.delete(remote_file)
    #     f.rmd(remote_dir)
    # except Exception as e:
    #     print("ftp_upload:", e)

    # f.mkd(remote_dir)
    f.storbinary('STOR ' + remote_file, fp, bufsize)
    end = datetime.now()
    print('times', (end - start).seconds)
    f.set_debuglevel(0)
    fp.close()


if __name__ == "__main__":
    local_file = 'images/temp/capture_nox-1.png'
    remote_dir = os.getenv('APPSIMULATOR_IP')
    remote_file = 'capture.png'
    ftp_upload(local_file, remote_dir, remote_file)
