@ECHO OFF
::--------------------------------------------------
SET VMRUN_EXE=C:\VMware\Workstation\vmrun.exe
SET workspace=D:\VMware\VM
SET VMX_FILE=Windows 7 x64.vmx
::---- main ----------------------------------------
FOR %%vm in (vm1,vm2,vm3,vm4,vm5) do CALL :STOP_VM %%vm

CALL :KILL_VM

FOR %%vm in (vm1,vm2,vm3,vm4,vm5) do CALL :CLONE_VM %%vm

FOR %%vm in (vm1,vm2,vm3,vm4,vm5) do CALL :START_VM %%vm

GOTO :EOF
::--------------------------------------------------
:KILL_VM
TASKKILL /F /IM "VMware.exe"
ECHO [%DATE% %TIME%] TASKKILL %ERRORLEVEL%
GOTO :EOF
::--------------------------------------------------
:STOP_VM

SET vm=%1
IF NOT DEFINED vm (
    ECHO [ERROR] please input vm name
    GOTO END
)

%VMRUN_EXE% stop "%workspace%\%vm%\%VMX_FILE%"
ECHO [%DATE% %TIME%] STOP_VM %vm% : %ERRORLEVEL%
GOTO :EOF
::--------------------------------------------------
:START_VM

SET vm=%1
IF NOT DEFINED vm (
    ECHO [ERROR] please input vm name
    GOTO END
)
%VMRUN_EXE% start "%workspace%\%vm%\%VMX_FILE%"
ECHO [%DATE% %TIME%] START_VM %vm% : %ERRORLEVEL%
GOTO :EOF
::--------------------------------------------------
:CLONE_VM
SET vm=%1

IF NOT DEFINED vm (
    ECHO [ERROR] please input vm name
    GOTO END
)
ECHO [%DATE% %TIME%] DELETE %vm%
DEL /F /Q /S %workspace%\%vm%
ECHO [%DATE% %TIME%] XCOPY %vm%
XCOPY /Y %workspace%\%vm%-org %workspace%\%vm%
ECHO [%DATE% %TIME%] CLONE_VM %vm% : %ERRORLEVEL%
GOTO :EOF
::--------------------------------------------------

:END
ECHO ON