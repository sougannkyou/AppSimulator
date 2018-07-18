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

SET vmName=%1
IF NOT DEFINED vmName (
    ECHO [ERROR] please input vm name
    GOTO END
)

%VMRUN_EXE% stop "%workspace%\%vmName%\%VMX_FILE%"
ECHO [%DATE% %TIME%] STOP_VM %vmName% : %ERRORLEVEL%
GOTO :EOF
::--------------------------------------------------
:START_VM

SET vmName=%1
IF NOT DEFINED vmName (
    ECHO [ERROR] please input vm name
    GOTO END
)
%VMRUN_EXE% start "%workspace%\%vmName%\%VMX_FILE%"
ECHO [%DATE% %TIME%] START_VM %vmName% : %ERRORLEVEL%
GOTO :EOF
::--------------------------------------------------
:CLONE_VM
SET vmName=%1

IF NOT DEFINED vmName (
    ECHO [ERROR] please input vm name
    GOTO END
)
ECHO [%DATE% %TIME%] DELETE %vmName%
DEL /F /Q /S %workspace%\%vmName%
ECHO [%DATE% %TIME%] XCOPY %vmName%
XCOPY /Y %workspace%\%vmName%-org %workspace%\%vmName%
ECHO [%DATE% %TIME%] CLONE_VM %vmName% : %ERRORLEVEL%
GOTO :EOF
::--------------------------------------------------

:END
ECHO ON