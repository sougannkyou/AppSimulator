0） 电源计划 
 高性能
 关闭显示器时间：从不

1) 设置桥接
-----------------------------------------
[PC]
00:e0:4c:44:c2:40

[VM]
00:0c:29:79:08:7e
00:0c:29:04:ca:80
00:0c:29:f4:b2:63

00:0c:29:6E:c8:68   172.16.251.28   vm1
00:0c:29:0a:00:94   172.16.251.27   vm2
00:0c:29:f7:e3:2b   172.16.251.13   vm3
00:0c:29:3c:91:27   172.16.251.152  vm4
00:0c:29:e9:ca:4e
00:50:56:c0:00:01
------------------------------------------

2) 设置登录免密（netplwiz 命令）
win7_64/zhxg2018

3)环境变量
APPSIMULATOR_IP
APPSIMULATOR_WORK_PATH = c:\workspace\pyWorks\AppSimulator
MONGODB_SERVER_IP = 127.0.0.1
MONGODB_SERVER_PORT = 27017
REDIS_SERVER_IP = 127.0.0.1

4）pip install
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple psutil opencv-python Pillow aircv pypiwin32 protobuf grpcio grpcio-tools pyautogui