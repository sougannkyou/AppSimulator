import pyadb3

adb = pyadb3.ADB()
adb.run_shell_cmd('ls -l /')
print(adb.get_output().decode())