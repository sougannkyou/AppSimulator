@ECHO OFF
SET vmrun=C:\VMware\Workstation\vmrun.exe
SET workspace=D:\VMware\VM
SET vmx=Windows 7 x64.vmx
REM parameter vm1
SET vm=%1

IF NOT DEFINED vm (
    ECHO [error] please input vm name
    GOTO END
)

%vmrun% -T ws -gu win7_64 -gp zhxg2018 copyFileFromGuestToHost "%workspace%\%vm%\%vmx%" "C:\workspace\pyWorks\AppSimulator\cmd\NoxResetCounter.conf" "%workspace%\%vm%\NoxResetCounter.conf"

set /P NoxResetCounter= 0<%workspace%\%vm%\NoxResetCounter.conf
echo NoxResetCounter is %NoxResetCounter%

IF %NoxResetCounter% NEQ 0 GOTO END

ECHO [%DATE% %TIME%] stop %vm%
%vmrun% stop "%workspace%\%vm%\%vmx%"
timeout 10

ECHO [%DATE% %TIME%] start %vm%
%vmrun% start "%workspace%\%vm%\%vmx%"
timeout 10

:END
@ECHO ON
EXIT 0