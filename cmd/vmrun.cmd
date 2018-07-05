cd "C:\VMware\Workstation"

REM echo stop vm
REM vmrun.exe stop "C:\VMWare\VM\vm1\Windows 7 x64.vmx"
REM timeout 10

REM echo snapshot vm
REM vmrun.exe snapshot "c:\VMWare\VM\vm1\Windows 7 x64.vmx" vm1-snapshot
REM timeout 10

echo revert To Snapshot
vmrun.exe revertToSnapshot "c:\VMWare\VM\vm1\Windows 7 x64.vmx" snapshot-vm1
timeout 10

echo start vm
vmrun.exe start "c:\VMWare\VM\vm1\Windows 7 x64.vmx"
timeout 10

rem echo run Program in Guest
rem 基本不能用
rem vmrun.exe  -T ws -gu "zhxg" -gp "zhxg2018" runPrograminGuest "c:\VMWare\VM\vm1\Windows 7 x64.vmx" "C:\workspace\pyWorks\AppSimulator\cmd\script_douyin.cmd"