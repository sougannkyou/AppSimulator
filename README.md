[PC]
zhxg/zhxg2018

-- 计划任务
  不要“使用最高权限运行”，否则kill不掉task 
  触发器：启动时，延迟30秒

-- 电源计划 
 高性能
 关闭显示器时间：从不

-- 设置桥接

[进入开发者模式]

[解锁]
使用 adb shell 的 rm /data/system/gesture.key  

[PC]
48:4D:7E:D9:B4:4D   172.16.2.109    (7500 + 8G + SSD-512G)  (pc@zhxg)

8c:ec:4b:90:9d:6d   172.16.2.110    (8400 + 16G + SSD-512G + 1T)
8c:ec:4b:92:72:6e   172.16.2.111    (8400 + 16G + SSD-512G + 1T)
48:4d:7e:ef:31:65   172.16.2.112    (7500 + 8G + SSD-256G)
48:4d:7e:d0:2f:c6   172.16.2.113    (6500 + 16G + SSD-1T)       (5 VM; 3 testerVM)


[VM] 使用桥接
00:0c:29:04:ca:80   172.16.2.101 
00:0c:29:f4:b2:63   172.16.2.102
00:0c:29:0a:00:94   172.16.2.104    tester-1
00:0c:29:f7:e3:2b   172.16.2.105    tester-2     
00:0c:29:3c:91:27   172.16.2.106    tester-3   
00:0c:29:e9:ca:4e   172.16.2.107         
00:50:56:c0:00:01   172.16.2.108   
00:0c:29:79:08:7e   172.16.2.100

00:e0:4c:44:c2:40
00:0c:29:6E:c8:68   

[快手账号]
13596415505
13514400711

------------------------------------------

[免密登录] VM-win7设置（netplwiz 命令）
win7_64/zhxg2018
vmrun -T ws -gu win7_64 -gp zhxg2018 captureScreen "c:\VMware\VM\vm1\Windows 7 x64.vmx" c:\vmware\vm\1.png

3)环境变量
APPSIMULATOR_IP = 172.16.2.XXX
APPSIMULATOR_MODE = [single|multi]
APPSIMULATOR_WORK_PATH = C:\workspace\pyWorks\AppSimulator
MONGODB_SERVER_IP = 172.16.2.109
MONGODB_SERVER_PORT = 27017
REDIS_SERVER_IP = 172.16.2.109

[FTP]  
ftp://172.16.253.37/
host = '172.16.253.37'
username = 'ControllerManager'
password = 'zhxg2018'
    
[python3 pip install]
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements_web.txt
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements_controller.txt
#pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple psutil pandas opencv-python==3.4.1.15 Pillow aircv pypiwin32 protobuf grpcio grpcio-tools pyautogui==0.9.36 matplotlib opencv-contrib-python

[数据结构]
[taskId]
{
    "_id" : "counter",
    "count" : 12
}

[tasks]
{
    "taskId" : 3,
    "orgTaskId":0,
    "script" : "script_douyin.py",
    "live_cycle": "once"/"never",
    "host_ip": "172.16.253.37",
    "app_name" : "douyin",
    "status" : "wait",  // unkown, wait, building, build_ok, build_ng, running, run_ok, run_ng
    "docker_type": "vmware"/"emulator",
    "timer_no": 3,
    "timer": "on|off",
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
    "host_ip" : "172.16.2.232",
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
mongodump -h 172.16.253.37:27017 -d AppSimulator -o c:\MongoDB\backup
mongorestore -h 192.168.31.82:27017 -d AppSimulator c:\MongoDB\backup\AppSimulator

[锁屏 4.4.2] 
adb shell rm /data/system/*.key

[adbkeyboard] 
adb shell pm uninstall com.android.adbkeyboard

[todo]
修改地域， 文本输入， 匹配杂乱背景，无明显标示无法切分

/static/AppSimulator/images/temp/emulators/capture_nox-1.png
static\AppSimulator\images\temp\emulators