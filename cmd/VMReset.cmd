@ECHO ON
SET log=%APPSIMULATOR_WORK_PATH%\cmd\vmreset.log
SET vmrun=C:\VMware\Workstation\vmrun.exe
SET workspace=D:\VMware\VM
SET vmx=Windows 7 x64.vmx
SET vm=%1

IF NOT DEFINED vm (
    ECHO [error] please input vm name
    GOTO END
)

:: %vmrun% -T ws -gu win7_64 -gp zhxg2018 copyFileFromGuestToHost "%workspace%\%vm%\%vmx%" "C:\workspace\pyWorks\AppSimulator\cmd\NoxResetCounter.conf" "%workspace%\%vm%\NoxResetCounter.conf"

set /P NoxResetCounter= 0<%APPSIMULATOR_WORK_PATH%\cmd\NoxResetCounter.conf
echo NoxResetCounter is %NoxResetCounter%

REM IF %NoxResetCounter% NEQ 0 GOTO END

ECHO [%DATE% %TIME%] %vm%>>%log%
ECHO [%DATE% %TIME%] stop %vm%
%vmrun% stop "%workspace%\%vm%\%vmx%"
timeout 10

ECHO [%DATE% %TIME%] start %vm%
%vmrun% start "%workspace%\%vm%\%vmx%"
timeout 10


:END
@ECHO ON
timeout 20
EXIT /B %ERRORLEVEL%