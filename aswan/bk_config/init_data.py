#!/usr/bin/env python3
# coding: utf-8

import json

from aswan.core.utils import get_sample_str
from aswan.core.redis_client import get_redis_client


def create_data_source(source_key=None, source_name=None, fields=None):
    source_key = source_key or get_sample_str(8)
    source_name = source_name or get_sample_str(8)
    fields = fields or ['user_id', 'uid']

    # Currently only used in testing, for simplicity, type is not configurable
    content = {field: 'string' for field in fields}
    content['name_show'] = source_name

    map_key = 'CONFIG_SOURCE_MAP'
    client = get_redis_client()
    client.hset(map_key, source_key, json.dumps(content))
    return source_key
