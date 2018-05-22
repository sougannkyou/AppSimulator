C:\Nox\bin\Nox.exe -quit
timeout 10
start /b C:\Nox\bin\Nox.exe
timeout 30
taskkill /f /t /fi "WINDOWTITLE eq script"
timeout 10
cd %RPCSERVER_HOME%
python script_douyin.py
