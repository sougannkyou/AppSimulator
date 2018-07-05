C:\Nox\bin\Nox.exe -quit
timeout 10
start /HIGH C:\Nox\bin\Nox.exe
timeout 90
REM tasklist | findstr "Nox.exe"
cd %APPSIMULATOR_WORK_PATH%
start "script" /HIGH python Controller/script_douyin.py
timeout 10
exit