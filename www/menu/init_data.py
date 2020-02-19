#!/usr/bin/env python3
# coding: utf-8

from django.utils.translation import gettext as _
import uuid
from datetime import datetime, timedelta

from www.core.pymongo_client import get_mongo_client
from www.core.redis_client import get_redis_client
from www.core.utils import get_sample_str
from risk_models.menu import build_redis_key


def create_menu_event(event_code=None, event_name=None):
    db = get_mongo_client()
    payload = dict(
        event_code=event_code or str(uuid.uuid4()),
        event_name=event_name or get_sample_str(length=8)
    )
    db['menu_event'].insert_one(payload)
    return payload


def add_element_to_menu(event_code, menu_type, dimension, element,
                        end_time=None, menu_desc=None):
    """
        Add elements to the list
    :param str|unicode event_code: List item code
    :param str|unicode menu_type: ListType  black white gray
    :param str|unicode dimension: List dimensions user_id / ip / ...
    :param str|unicode element: Elements placed on the list
    :param datetime end_time: Failure time
    :param str|unicode menu_desc: Note
    :return:
    """
    end_time = (end_time or datetime.now() + timedelta(hours=1))
    menu_desc = menu_desc or get_sample_str(15)
    payload = dict(
        end_time=end_time,
        menu_desc=menu_desc,
        menu_status=_("Valid"),
        create_time=datetime.now(),
        creator='test',
        value=element,
        event_code=event_code,
        dimension=dimension,
        menu_type=menu_type
    )
    db = get_mongo_client()
    insert_result = db['menus'].insert_one(payload)

    redis_client = get_redis_client()
    redis_key = build_redis_key(event_code, dimension=dimension,
                                menu_type=menu_type)
    if redis_key:
        redis_client.sadd(redis_key, element)

    return str(insert_result.inserted_id)
