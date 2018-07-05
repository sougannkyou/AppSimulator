REM taskkill /t /f /fi "WINDOWTITLE eq script"
C:\Nox\bin\Nox.exe -quit
timeout 10
start /HIGH C:\Nox\bin\Nox.exe
timeout 60
REM tasklist | findstr "Nox.exe"
cd %APPSIMULATOR_WORK_PATH%
set /P taskConf= 0<cmd\task.conf
echo %taskConf%
start "script" /HIGH python Controller/script_%taskConf%.py
timeout 10
exit


