#!/usr/bin/env python3
# coding=utf-8

from django.utils.translation import gettext_lazy as _
from aswan.core.utils import get_sample_str

from aswan.strategy.forms import (MenuStrategyForm, BoolStrategyForm,
                                  UserStrategyForm, FreqStrategyForm)


def _create_new_strategy(form_cls, strategy_conf):
    form_obj = form_cls(data=strategy_conf)

    if form_obj.is_valid():
        # Created successfully
        new_strategy_uuid = form_obj.save()
        return True, new_strategy_uuid
    else:
        return False, ''


def create_menu_strategy(event_code, dimension, menu_type, menu_op,
                         strategy_name=None, strategy_desc=None):
    """
        New List strategy
    :param str|unicode event_code: Project uuid
    :param str|unicode dimension: Dimensions  user_id / ip / uid ...
    :param str|unicode menu_type: ListType  black, white, gray
    :param str|unicode menu_op: ActionCode In/not in (is/is_not)
    :param str|unicode strategy_name: PolicyName
    :param str|unicode strategy_desc: PolicyDescription
    """

    strategy_name = strategy_name or get_sample_str()
    strategy_desc = strategy_desc or get_sample_str()

    data = {
        'strategy_name': strategy_name,
        'strategy_desc': strategy_desc,
        'menu_op': menu_op,
        'event': event_code,
        'dimension': dimension,
        'menu_type': menu_type
    }

    success, strategy_uuid = _create_new_strategy(
        MenuStrategyForm, strategy_conf=data
    )

    assert success, _('create menu strategy fail.')

    return strategy_uuid


def create_bool_strategy(strategy_var, strategy_op, strategy_func,
                         strategy_threshold, strategy_name=None,
                         strategy_desc=None):
    """
        新建bool型策略
    :param str|unicode strategy_var: Built-in_Variables
    :param str|unicode strategy_op: ActionCode
    :param str|unicode strategy_func: Built-in_Functions
    :param str|unicode strategy_threshold: Threshold for policy
    :param str|unicode strategy_name: PolicyName
    :param str|unicode strategy_desc: PolicyDescription
    :return:
    """

    strategy_name = strategy_name or get_sample_str()
    strategy_desc = strategy_desc or get_sample_str()

    data = {
        'strategy_var': strategy_var,
        'strategy_op': strategy_op,
        'strategy_func': strategy_func,
        'strategy_threshold': strategy_threshold,
        'strategy_name': strategy_name,
        'strategy_desc': strategy_desc
    }

    success, strategy_uuid = _create_new_strategy(
        BoolStrategyForm, strategy_conf=data
    )
    assert success, _('create bool strategy fail.')
    return strategy_uuid


def create_user_strategy(strategy_source, strategy_body, strategy_day,
                         strategy_limit, strategy_name=None,
                         strategy_desc=None):
    """
        New User-limited number-based policy
    :param str|unicode strategy_source: Escalate data source key
    :param str|unicode strategy_body: Limit the principal eg:  ip, uid, user_id  etc...
    :param int strategy_day: Natural days
    :param int strategy_limit: Limit the number of Users
    :param str|unicode strategy_name: PolicyName
    :param str|unicode strategy_desc: PolicyDescription
    :return:
    """
    strategy_name = strategy_name or get_sample_str()
    strategy_desc = strategy_desc or get_sample_str()

    data = {
        'strategy_source': strategy_source,
        'strategy_body': strategy_body,
        'strategy_day': strategy_day,
        'strategy_limit': strategy_limit,
        'strategy_name': strategy_name,
        'strategy_desc': strategy_desc
    }

    success, strategy_uuid = _create_new_strategy(
        UserStrategyForm, strategy_conf=data
    )
    assert success, _('create bool strategy fail.')
    return strategy_uuid


def create_freq_strategy(strategy_source, strategy_body, strategy_time,
                         strategy_limit, strategy_name=None,
                         strategy_desc=None):
    """
        New time period frequency control strategy
        request: Request object, user information needs to be obtained from it, etc.
    :param str|unicode strategy_source: Escalate data source key
    :param str|unicode strategy_body: Limit the principal eg:  ip, uid, user_id  etc...
    :param int strategy_time:  Time period (in seconds)
    :param int strategy_limit: Limit the number of people
    :param str|unicode strategy_name: PolicyName
    :param str|unicode strategy_desc: PolicyDescription
    :return:
    """
    strategy_name = strategy_name or get_sample_str()
    strategy_desc = strategy_desc or get_sample_str()

    data = {
        'strategy_source': strategy_source,
        'strategy_body': strategy_body,
        'strategy_time': strategy_time,
        'strategy_limit': strategy_limit,
        'strategy_name': strategy_name,
        'strategy_desc': strategy_desc
    }
    success, strategy_uuid = _create_new_strategy(FreqStrategyForm,
                                                  strategy_conf=data)
    assert success, _('create freq strategy fail.')

    return strategy_uuid
