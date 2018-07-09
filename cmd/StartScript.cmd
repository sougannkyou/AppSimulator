@ECHO OFF
timeout 10
cd %APPSIMULATOR_WORK_PATH%
set /P taskConf= 0<cmd\task.conf
echo <<< %taskConf% >>>
timeout 60
start "script" /HIGH python Controller/script_%taskConf%.py
timeout 10
@ECHO ON
exit


