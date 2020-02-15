#!/usr/bin/env python3
# coding=utf8

import pymysql

# for development import this:
# from config.develop import LOG_MYSQL_CONFIG

# for production import this
import config.product as conf

__all__ = ['get_log_mysql_client']


def get_log_mysql_client():
    return pymysql.connect(**conf.LOG_MYSQL_CONFIG)
