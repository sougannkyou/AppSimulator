REM taskkill /t /f /fi "WINDOWTITLE eq script"
C:\Nox\bin\Nox.exe -quit
timeout 10
start /HIGH C:\Nox\bin\Nox.exe
timeout 90

REM NoxConsole quitall
REM NoxConsole list
REM FOR %%i IN (1,2,3,4,5,6,7,8,9,10) do NoxConsole remove -name:nox-%%i && timeout 5
REM FOR %%i IN (1,2,3,4,5,6,7,8,9,10) do NoxConsole copy -name:nox-%%i -from:org && timeout 20
REM FOR %%i IN (1,2,3,4,5,6,7,8,9,10) do NoxConsole restore -name:nox-%%i -file:"C:\Nox\backup\nox-dianping.npbk" && timeout 20

REM tasklist | findstr "Nox.exe"
cd %APPSIMULATOR_WORK_PATH%
start "script" /HIGH python Controller/script_douyin.py
timeout 10
exit


