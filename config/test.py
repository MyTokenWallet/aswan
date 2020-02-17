#!/usr/bin/env python3
# coding: utf-8

#  Redis that stores configuration information
REDIS_CONFIG = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 1,
    "password": "",
    "max_connections": 40,
    "socket_timeout": 1,
    "decode_responses": True
}

#  Redis as a hit log queue
LOG_REDIS_CONFIG = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 1,
    "password": "",
    "max_connections": 40,
    "socket_timeout": 1,
    "decode_responses": True
}

#  Redis to store reported data
REPORT_REDIS_CONFIG = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 1,
    "password": "",
    "max_connections": 40,
    "socket_timeout": 1,
    "decode_responses": True
}

# Store hit logs for mysql
LOG_MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'charset': 'utf8',
    'db': 'risk_control_test',
}

# Mongo that stores information such as Authority
SOC_MONGO_HOST = [
    "127.0.0.1:27017",
]

MONGO_DB = "risk_control_test"
