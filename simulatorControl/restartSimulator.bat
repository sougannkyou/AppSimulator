rem taskkill /t /f /fi "WINDOWTITLE eq taskeng.exe"
start /b start C:\Nox\bin\Nox.exe -quit
timeout 10
start /b start /HIGH C:\Nox\bin\Nox.exe
timeout 60
tasklist | findstr "Nox.exe"
cd %SIMULATOR_CONTROL_HOME%
start /b start /HIGH python script_douyin.py
rem C:\Nox\bin\Nox.exe -quit
timeout 10
exit

