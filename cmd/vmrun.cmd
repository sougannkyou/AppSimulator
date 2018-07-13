cd "C:\VMware\Workstation"

REM echo stop vm
REM vmrun.exe stop "C:\VMWare\VM\vm1\Windows 7 x64.vmx"
REM timeout 10

REM echo snapshot vm
REM vmrun.exe snapshot "c:\VMWare\VM\vm1\Windows 7 x64.vmx" vm1-snapshot
REM timeout 10

rem echo revert To Snapshot
rem vmrun.exe revertToSnapshot "c:\VMWare\VM\vm1\Windows 7 x64.vmx" snapshot-vm1
rem timeout 10

rem vmrun.exe getGuestIPAddress "C:\VMware\VM\device1\Windows 7 x64.vmx"

rem vmrun.exe  -T ws -gu "zhxg" -gp "zhxg2018" CopyFileFromHostToGuest "c:\VMWare\VM\vm1\Windows 7 x64.vmx"  %APPSIMULATOR_WORK_PATH%"\cmd\app.conf"
echo start vm
vmrun.exe reset "c:\VMWare\VM\vm1\Windows 7 x64.vmx"
timeout 10

rem echo run Program in Guest
rem 基本不能用
rem vmrun.exe  -T ws -gu "zhxg" -gp "zhxg2018" runPrograminGuest "c:\VMWare\VM\vm1\Windows 7 x64.vmx" "C:\workspace\pyWorks\AppSimulator\cmd\script_douyin.cmd"