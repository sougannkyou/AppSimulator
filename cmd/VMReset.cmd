@ECHO OFF
SET vmrun=C:\VMware\Workstation\vmrun.exe
SET workspace=C:\VMware\VM
SET vmx=Windows 7 x64.vmx
REM parameter vm1
SET vm=%1

IF NOT DEFINED vm (
    ECHO [error] please input vm name
    GOTO END
)

ECHO [%DATE% %TIME%] stop %vm%
%vmrun% stop "%workspace%\%vm%\%vmx%"
timeout 10

ECHO [%DATE% %TIME%] start %vm%
%vmrun% start "%workspace%\%vm%\%vmx%"
timeout 10

:END
@ECHO ON