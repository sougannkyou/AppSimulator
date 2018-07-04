cd "C:\Program Files (x86)\VMware\VMware Workstation"

echo stop vm 
vmrun.exe stop "C:\VM\device1\Windows 7 x64.vmx"
timeout 10

echo snapshot vm 
vmrun.exe snapshot "c:\VM\device1\Windows 7 x64.vmx" device1-snapshot
timeout 10

rem echo revertToSnapshot 
rem vmrun.exe revertToSnapshot "c:\VM\device1\Windows 7 x64.vmx" device1-snapshot
rem timeout 10

rem echo start vm
rem vmrun.exe start "c:\VM\device1\Windows 7 x64.vmx"
rem timeout 10