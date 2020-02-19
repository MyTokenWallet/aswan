#!/usr/bin/env python3
"""
WSGI config for risk_control project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# FIX open base.py(PYMYSQL) and delete just line 36 and 37
import pymysql

pymysql.install_as_MySQLdb()


application = get_wsgi_application()
