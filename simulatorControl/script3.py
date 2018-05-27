from subprocess import check_output, CalledProcessError

try:
    adb_ouput = check_output(["adb", "devices"])
    print(adb_ouput)
except CalledProcessError as e:
    print(e.returncode)