@ECHO OFF
SET vmrun=C:\VMware\Workstation\vmrun.exe
SET workspace=d:\VMware\VM
SET vmx=Windows 7 x64.vmx

FOR %%vm in (vm1,vm2,vm3,vm4,vm5) DO CALL :CAPTURESCREEN_VM %vm

GOTO :EOF
::--------------------------------------------------
:CAPTURESCREEN_VM
SET vmName=%1
ECHO vmrun.exe  -T ws -gu win7_64 -gp zhxg2018 captureScreen "%workspace%\%vmName%\%vmx%" "%APPSIMULATOR_WORK_PATH%\\static\\images\\AppSimulator\\images\\VM\"
GOTO :EOF

:END
ECHO ON