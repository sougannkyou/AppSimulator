cd "C:\VMware\Workstation"

REM echo stop vm
REM vmrun.exe stop "C:\VM\device1\Windows 7 x64.vmx"
REM timeout 10

rem echo snapshot vm 
rem vmrun.exe snapshot "c:\VM\device1\Windows 7 x64.vmx" device1-snapshot
rem timeout 10

echo revertToSnapshot 
vmrun.exe revertToSnapshot "c:\VM\device1\Windows 7 x64.vmx" device1-snapshot
timeout 10

echo start vm
vmrun.exe start "c:\VM\device1\Windows 7 x64.vmx"
timeout 10

vmrun.exe  -T ws -gu "zhxg" -gp "zhxg2018" runPrograminGuest "c:\VMWare\device1\Windows 7 x64.vmx" "C:\workspace\AppSimulator\Controller\script_douyin.cmd"