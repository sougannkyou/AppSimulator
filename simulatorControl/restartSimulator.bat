rem taskkill /t /f /fi "WINDOWTITLE eq taskeng.exe"
C:\Nox\bin\Nox.exe -quit
timeout 10
start /b /ABOVENORMAL C:\Nox\bin\Nox.exe
timeout 30
tasklist | findstr "Nox.exe"
cd %RPCSERVER_HOME%
python script_douyin.py
timeout 10
rem C:\Nox\bin\Nox.exe -quit
rem timeout 30000

