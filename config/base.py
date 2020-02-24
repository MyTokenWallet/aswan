#!/usr/bin/env python3
# coding: utf-8
from django.utils.translation import ugettext_lazy as _
import importlib
import os

# Log output directory
LOG_HOME = './output'

# www Home
BASE_DIR = './www'

# Hit log queue name
HIT_LOG_QUEUE_NAME = 'hit_log_queue'

# Service configuration items
RISK_SERVER_HOST = '127.0.0.1'
RISK_SERVER_PORT = 50000

#  Store sourcemap's redis key
REDIS_SOURCE_MAP = 'CONFIG_SOURCE_MAP'

# mongodb
MONGO_POOL_SIZE = 20  # one additional to monitoring the server’s state
MONGO_MAX_IDLE_TIME = 1 * 60 * 1000  # Maximum idle time 1 minute
MONGO_SOCKET_TIMEOUT = 1 * 1000  # socket time-out, 1 second
MONGO_MAX_WAITING_TIME = 100  # Maximum wait time, 100ms
MONGO_READ_PREFERENCE = "secondaryPreferred"

MONGO_AUTH_DB = "risk_control"
MONGO_USER = "risk_control_user"
MONGO_PWD = "risk_control_pwd"

risk_env = os.environ.get('RISK_ENV', 'develop')

# If the profile does not exist, it cannot be started directly
try:
    importlib.import_module('.' + risk_env, 'config')
    exec('from config.{risk_env} import *'.format(risk_env=risk_env))
except Exception:
    raise AssertionError(
        _('The project should set correct RISK_ENV environment var.'))
