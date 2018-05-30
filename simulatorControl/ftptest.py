import ftplib

DEBUG_ENV = False


def ftp_upload(local_file, remote_dir, remote_file):
    host = '172.16.3.2'
    username = 'admin'
    password = 'zhxg@2018'

    f = ftplib.FTP(host)
    f.login(username, password)
    pwd_path = f.pwd()
    print("FTP当前路径:", pwd_path)

    bufsize = 1024  # 设置缓冲器大小
    fp = open(local_file, 'rb')
    # f.set_debuglevel(2)
    try:
        f.delete(remote_file)
        f.rmd(remote_dir)
    except Exception as e:
        print("ftp_upload:", e)

    f.mkd(remote_dir)
    f.storbinary('STOR ' + remote_dir + '/' + remote_file, fp, bufsize)
    f.set_debuglevel(0)
    fp.close()


if __name__ == "__main__":
    local_file = 'images/app_ready.png'
    remote_dir = '172.16.3.2'
    remote_file = 'app_ready.png'
    ftp_upload(local_file, remote_dir, remote_file)
