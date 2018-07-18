@ECHO OFF
SET vmrun=C:\VMware\Workstation\vmrun.exe
SET workspace=d:\VMware\VM
SET vmx=Windows 7 x64.vmx

FOR %%i in (vm1,vm2,vm3,vm4,vm5) do  CALL STOP_VM %%i

TASKKILL /F /IM "VMware.exe"
ECHO TASKKILL ret %ERRORLEVEL%

FOR %%i in (vm1,vm2,vm3,vm4,vm5) do  CALL CLONE_VM %%i

FOR %%i in (vm1,vm2,vm3,vm4,vm5) do  CALL START_VM %%i

::--------------------------------------------------
:STOP_VM

SET vm=vm%1

IF NOT DEFINED vm (
    ECHO [error] please input vm name
    GOTO END
)

ECHO [%DATE% %TIME%] stop %vm%
%vmrun% stop "%workspace%\%vm%\%vmx%"
ECHO STOP_VM %ERRORLEVEL%
GOTO :EOF

::--------------------------------------------------
:START_VM
SET vm=vm%1

IF NOT DEFINED vm (
    ECHO [error] please input vm name
    GOTO END
)
ECHO [%DATE% %TIME%] start %vm%
%vmrun% start "%workspace%\%vm%\%vmx%"
ECHO START_VM %ERRORLEVEL%
GOTO :EOF

::--------------------------------------------------
:CLONE_VM

SET vm=vm%1

IF NOT DEFINED vm (
    ECHO [error] please input vm name
    GOTO END
)

ECHO [%DATE% %TIME%] delete %vm%
DEL /F /Q /S %workspace%\%vm%

ECHO [%DATE% %TIME%] copy %vm%
XCOPY /Y %workspace%\%vm%-org %workspace%\%vm%

ECHO CLONE_VM %ERRORLEVEL%
GOTO :EOF
::--------------------------------------------------

:END
ECHO ON