cd "C:\VMware\Workstation"

REM echo stop vm
REM vmrun.exe stop "C:\VMWare\VM\device1\Windows 7 x64.vmx"
REM timeout 10

rem echo snapshot vm 
rem vmrun.exe snapshot "c:\VMWare\VM\device1\Windows 7 x64.vmx" device1-snapshot
rem timeout 10

echo revertToSnapshot 
vmrun.exe revertToSnapshot "c:\VMWare\VM\device1\Windows 7 x64.vmx" snapshot-device1
timeout 10

echo start vm
vmrun.exe start "c:\VMWare\VM\device1\Windows 7 x64.vmx"
timeout 10

vmrun.exe  -T ws -gu "zhxg" -gp "zhxg2018" runPrograminGuest "c:\VMWare\VM\device1\Windows 7 x64.vmx" "C:\workspace\pyWorks\AppSimulator\Controller\script_douyin.cmd"