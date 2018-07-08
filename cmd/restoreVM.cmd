ECHO OFF
ECHO [%DATE% %TIME%] stop vm
C:\VMware\Workstation\vmrun.exe stop "d:\VM\vm-1\Windows 7 x64.vmx"
ECHO [%DATE% %TIME%] delete vm
DEL /F /Q /S D:\VM\vm-1
ECHO [%DATE% %TIME%] copy vm
XCOPY /Y D:\VM\vm-1-org D:\VM\vm-1
ECHO [%DATE% %TIME%] start vm
C:\VMware\Workstation\vmrun.exe start "d:\VM\vm-1\Windows 7 x64.vmx"
ECHO ON