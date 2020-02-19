#!/usr/bin/env python3
import os
import sys

# FIX open base.py(PYMYSQL) and delete just line 36 and 37
import pymysql

pymysql.install_as_MySQLdb()

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
