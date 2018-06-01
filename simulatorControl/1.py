try:
    import sys
    from MyADB3 import ADB
except ImportError as e:
    # should never be reached
    print("[f] Required module missing.", e.args[0])
    sys.exit(-1)


def main():
    adb = ADB(adb_binary_path='C:\\Nox\\bin\\adb.exe')
    print(adb.get_android_version())

    adb.wait_for_device()
    err, devices = adb.get_devices()

    if not devices:
        print("Unexpected error, may be you're a very fast guy?")
        return

    print("Selecting: %s" % devices[0])
    adb.set_target_device(devices[0])

    print("Executing 'ls' command")
    adb.shell_command('ls')

    print("Output:\n%s" % adb.get_output())


if __name__ == "__main__":
    main()
