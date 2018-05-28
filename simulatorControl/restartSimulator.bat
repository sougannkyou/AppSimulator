rem taskkill /t /f /fi "WINDOWTITLE eq taskeng.exe"
C:\Nox\bin\Nox.exe -quit
timeout 10
start /b /HIGH C:\Nox\bin\Nox.exe
timeout 60
tasklist | findstr "Nox.exe"
cd %SIMULATOR_CONTROL_HOME%
start /b start /HIGH python script_douyin.py
timeout 10
rem C:\Nox\bin\Nox.exe -quit
rem timeout 30

