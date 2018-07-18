@ECHO OFF
SET vmrun=C:\VMware\Workstation\vmrun.exe
SET workspace=d:\VMware\VM
SET vmx=Windows 7 x64.vmx

FOR %%vm in (vm1,vm2,vm3,vm4,vm5) DO CALL :STOP_VM %%vm
FOR %%vm in (vm1,vm2,vm3,vm4,vm5) DO CALL :START_VM %%vm

GOTO :EOF

::--------------------------------------------------
:STOP_VM
SET vmName=%1
ECHO vmrun.exe stop "%workspace%\%vmName%\%vmx%"
GOTO :EOF

::--------------------------------------------------
:START_VM
SET vmName=%1
ECHO vmrun.exe start "%workspace%\%vmName%\%vmx%"
GOTO :EOF

::--------------------------------------------------
:END
ECHO ON