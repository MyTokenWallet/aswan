#!/usr/bin/env python3
import os
import sys

# FIX open base.py(PYMYSQL) and delete just line 36 and 37
import pymysql

pymysql.install_as_MySQLdb()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
