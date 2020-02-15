#!/usr/bin/env python3
# coding=utf8

from lru import lru_cache_function
from pymongo import MongoClient

from config.base import (MONGO_POOL_SIZE, MONGO_MAX_IDLE_TIME,
                    MONGO_MAX_WAITING_TIME, MONGO_SOCKET_TIMEOUT)

from config.product import (SOC_MONGO_HOST, MONGO_DB)


@lru_cache_function(max_size=1, expiration=24 * 3600)
def _get_mongo_pool():
    _POOL_TEMP = MongoClient(host=SOC_MONGO_HOST, maxPoolSize=MONGO_POOL_SIZE,
                             connect=False,
                             socketKeepAlive=True,
                             maxIdleTimeMS=MONGO_MAX_IDLE_TIME,
                             waitQueueTimeoutMS=MONGO_MAX_WAITING_TIME,
                             socketTimeoutMS=MONGO_SOCKET_TIMEOUT)
    # _POOL_TEMP[MONGO_AUTH_DB].authenticate(MONGO_USER, MONGO_PWD)
    return _POOL_TEMP


def get_mongo_client(db_name=MONGO_DB):
    pool = _get_mongo_pool()
    return pool[db_name]
