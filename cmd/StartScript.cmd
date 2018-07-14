@ECHO ON
cd %APPSIMULATOR_WORK_PATH%

timeout 5
set /P NoxResetCounter= 0<cmd\NoxResetCounter.conf
echo NoxResetCounter is %NoxResetCounter%

REM if %NoxResetCounter% EQU 0 goto END

start C:\Nox\bin\Nox.exe -quit

timeout 20
start C:\Nox\bin\Nox.exe

timeout 10
set /P appName= 0<cmd\app.conf
echo %appName%

timeout 60
start "script" /HIGH python Controller/script_%appName%.py

:END
timeout 10
@ECHO ON
EXIT 0


