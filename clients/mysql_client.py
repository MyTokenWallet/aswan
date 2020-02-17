#!/usr/bin/env python3
# coding: utf-8
# FIX open base.py(PYMYSQL) and delete just line 36 and 37
import pymysql
pymysql.install_as_MySQLdb()

# for development import this:
# from config.develop import LOG_MYSQL_CONFIG

# for production import this
import config.product as conf

__all__ = ['get_log_mysql_client']


def get_log_mysql_client():
    return pymysql.connect(**conf.LOG_MYSQL_CONFIG)
