taskkill /t /f /fi "WINDOWTITLE eq script"
C:\Nox\bin\Nox.exe -quit
timeout 10
start /HIGH C:\Nox\bin\Nox.exe
timeout 90
tasklist | findstr "Nox.exe"
cd %SIMULATOR_CONTROL_HOME%
start "script" /HIGH python script_douyin.py
timeout 10
exit


