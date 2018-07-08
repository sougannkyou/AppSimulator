REM taskkill /t /f /fi "WINDOWTITLE eq script"
REM C:\Nox\bin\Nox.exe -quit
REM timeout 10
REM start /HIGH C:\Nox\bin\Nox.exe
set /P taskConf= 0<cmd\task.conf
echo %taskConf%
timeout 60
REM tasklist | findstr "Nox.exe"
cd %APPSIMULATOR_WORK_PATH%
start "script" /HIGH python Controller/script_%taskConf%.py
timeout 10
exit


