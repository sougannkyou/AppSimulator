#!/usr/bin/env python
import os
import sys
from Controller.setting import APPSIMULATOR_MODE

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    from django.core.management import execute_from_command_line

    # if APPSIMULATOR_MODE == 'vmware':
    #     os.system('start "vmware" python Controller\\vm_start.py')
    # else:
    #     os.system('start "emulators" python Controller\\emulators_start.py')

    execute_from_command_line(sys.argv)
