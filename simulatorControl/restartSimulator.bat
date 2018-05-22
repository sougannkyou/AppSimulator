C:\Nox\bin\Nox.exe -quit
timeout 10
start /b C:\Nox\bin\Nox.exe
timeout 30
cd %RPCSERVER_HOME%
python script_douyin.py
timeout 10
C:\Nox\bin\Nox.exe -quit
timeout 30

