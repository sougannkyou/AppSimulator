0） 电源计划 
 高性能
 关闭显示器时间：从不

1) 设置桥接
-----------------------------------------
[testerVM]    172.16.253.232    1141264951
[testerNox]   172.16.250.199    1136162364

[PC]
00:e0:4c:44:c2:40

[VM]
00:0c:29:79:08:7e
00:0c:29:04:ca:80
00:0c:29:f4:b2:63

00:0c:29:6E:c8:68   172.16.251.28   vm1     miaopai
00:0c:29:0a:00:94   172.16.251.27   vm2     miaopai
00:0c:29:f7:e3:2b   172.16.251.13   vm3     huoshan
00:0c:29:3c:91:27   172.16.251.152  vm4     huoshan
00:0c:29:e9:ca:4e   172.16.250.176  vm5     miaopai
00:50:56:c0:00:01

[Nox]
nox-1 

[快手]
13596415505
13514400711

------------------------------------------

2) VM-win7设置登录免密（netplwiz 命令）
win7_64/zhxg2018
vmrun -T ws -gu win7_64 -gp zhxg2018 captureScreen "c:\VMware\VM\vm1\Windows 7 x64.vmx" c:\vmware\vm\1.png

3)环境变量
APPSIMULATOR_IP = 172.16.253.232
APPSIMULATOR_MODE = nox
APPSIMULATOR_WORK_PATH = C:\workspace\pyWorks\AppSimulator
MONGODB_SERVER_IP = 172.16.253.37
MONGODB_SERVER_PORT = 27017
REDIS_SERVER_IP = 172.16.253.37

4) FTP  ftp://172.16.253.37/
    host = '172.16.253.37'
    username = 'ControllerManager'
    password = 'zhxg2018'
    
5）python3 pip install
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple psutil opencv-python==3.4.1.15 Pillow aircv pypiwin32 protobuf grpcio grpcio-tools pyautogui==0.9.36 matplotlib opencv-contrib-python

6)数据结构
[tasks]
{
    "taskId" : 222,
    "orgTaskId":0,
    "script" : "script_douyin.py",
    "live_cycle": "once"/"never",
    "host_ip": "172.16.253.232",
    "app_name" : "douyin",
    "status" : "wait",  // unkown, wait, building, build_ok, build_ng, running, run_ok, run_ng
    "docker_type": "vmware"/"emulator",
    "timer_no": 0,
    "dockerId": ObjectId("emulators") or ObjectId("vmwares"),
    "start_time" : 0,
    "up_time" : 0,
    "end_time" : 0,
}

[hosts]
{
    "ip" : "172.16.253.232",
    "host_type": "vmware" / "emulator",
    "support_app_list": ["huoshan", "douyin", "miaopai"],
    "timer_max_cnt": 10,
    "mem_total": 7.9
}

[emulators]
{
    "name" : "nox-222",
    "host_ip" : "172.16.253.232",
    "app_name" : "douyin",
    "status" : "docker_run_ok",
    "start_time" : 1529894656,
    "up_time" : 1529894656,
    "end_time" : 0
}

[vmwares]
{
    "name" : "vm3",
    "local_ip" : "172.16.251.13",
    "host_ip" : "172.16.253.232",
    "app_name" : "douyin",
    "status" : "wait",
    "start_time" : 0,
    "end_time" : 0
}

[mongodb]
mongodump -h 172.16.253.37:27017 -d AppSimulator -o c:\MongoDB\data