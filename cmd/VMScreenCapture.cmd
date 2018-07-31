SET vmrun=C:\VMware\Workstation\vmrun.exe
SET workspace=C:\VMware\VM
SET vmx=Windows 7 x64.vmx

FOR /L %%i in (1,1,1000000) DO CALL :VM_LOOP
GOTO :EOF
::--------------------------------------------------
:VM_LOOP
FOR /L %%i in (1,1,2) DO CALL :VM_SCREEN_CAPTURE %%i
TIMEOUT 1
GOTO :EOF
::--------------------------------------------------
:VM_SCREEN_CAPTURE
@ECHO OFF
SET vmName=vm%1
SET current="%APPSIMULATOR_WORK_PATH%\static\AppSimulator\images\temp\vmwares\capture_%vmName%.png"
::SET before="%APPSIMULATOR_WORK_PATH%\static\AppSimulator\images\VM\capture_%vmName%_before.png"
::MOVE %current% %before%
%vmrun%  -T ws -gu win7_64 -gp zhxg2018 captureScreen "%workspace%\%vmName%\%vmx%" %current%
ECHO ON