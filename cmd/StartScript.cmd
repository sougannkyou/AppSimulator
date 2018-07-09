@ECHO OFF
timeout 10
echo 退出模拟器
C:\Nox\bin\Nox.exe -quit
timeout 10
echo 启动模拟器
C:\Nox\bin\Nox.exe
timeout 10
cd %APPSIMULATOR_WORK_PATH%
set /P taskConf= 0<cmd\task.conf
echo 开始执行脚本 %taskConf%
timeout 60
start "script" /HIGH python Controller/script_%taskConf%.py
timeout 10
@ECHO ON
exit


