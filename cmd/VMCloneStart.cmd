@ECHO OFF
SET vmrun=C:\VMware\Workstation\vmrun.exe
SET workspace=d:\VM
SET vmx=Windows 7 x64.vmx
REM parameter vm1
SET vm=%1

IF NOT DEFINED vm (
    ECHO [error] please input vm name
    GOTO END
)

ECHO [%DATE% %TIME%] stop %vm%
%vmrun% stop "%workspace%\%vm%\%vmx%"

ECHO [%DATE% %TIME%] delete %vm%
DEL /F /Q /S %workspace%\%vm%

ECHO [%DATE% %TIME%] copy %vm%
XCOPY /Y %workspace%\%vm%-org %workspace%\%vm%

ECHO [%DATE% %TIME%] start %vm%
%vmrun% start "%workspace%\%vm%\%vmx%"

:END
@ECHO ON