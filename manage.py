#!/usr/bin/env python
import os
import sys

from AppSimulator.setting import DEVICE_LIST
from AppSimulator.dbDriver import MongoDriver

MDB = MongoDriver()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

    DEVICE_LIST = MDB.get_device_list()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
