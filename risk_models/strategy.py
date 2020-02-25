#!/usr/bin/env python3
# coding: utf-8
from django.utils.translation import gettext_lazy as _
import re
import time
import math
import logging
from datetime import datetime
from functools import partial, wraps
from collections import defaultdict

import redis

from risk_models.menu import hit_menu
from builtin_funcs import BuiltInFuncs
from risk_models.source import FreqSource, UserSource
from clients import get_report_redis_client, get_config_redis_client

logger = logging.getLogger(__name__)


def partial_bind_uuid(f):
    @wraps(f)
    def inner(self, *args, **kwargs):
        partial_obj = f(self, *args, **kwargs)
        partial_obj.uuid = self.uuid
        partial_obj.name = self.name
        return partial_obj

    return inner


_used_strategies = set()


def register_strategy(cls):
    _used_strategies.add(cls)
    return cls


class Strategy(object):
    """Policy Base Class"""

    def __init__(self, d):
        #  Policy uuid
        self.uuid = d['uuid']
        #  PolicyName
        self.name = d['strategy_name']
        # Call count
        self.query_count = 0

    def get_thresholds(self):
        """Each Policy must have a threshold list, and Policy in the rule binds this threshold by default
        The threshold list returned here is actually a string list and does not have type conversion"""
        raise NotImplementedError(_("must be writen by subclass"))

    def build_strategy_name_from_thresholds(self, thresholds):
        """Each Policy must be able to reconstruct the PolicyName from the threshold list"""
        raise NotImplementedError(_("must be writen by subclass"))

    def get_callable(self):
        raise NotImplementedError(_("must be writen by subclass"))

    def get_callable_from_threshold_list(self, threshold_list):
        """This method returns a callable object based on a given threshold list.
        The callable object accepts a req_body as input, outputs a boolean value and a custom string"""
        raise NotImplementedError(_("must be writen by subclass"))

    def __unicode__(self):
        return "{}[{}]".format(self.name, self.uuid)

    def __repr__(self):
        return self.__unicode__()


@register_strategy
class BoolStrategy(Strategy):
    """ Bool Type """
    prefix = 'bool_strategy:*'

    def __init__(self, d):
        super(BoolStrategy, self).__init__(d)
        self.func_name = d['strategy_func']
        self.op_name = d['strategy_op']
        self.threshold = d['strategy_threshold']
        self.strategy_var = d['strategy_var']

    def get_thresholds(self):
        if not self.threshold:
            return []
        else:
            return [self.threshold]

    def build_strategy_name_from_thresholds(self, thresholds):
        if len(thresholds) == 1:
            threshold = str(thresholds[0])
            return re.sub(r'[\d.]+$', threshold, self.name)
        else:
            return self.name

    def get_callable(self):
        threshold = self.threshold or None
        return partial(BuiltInFuncs.run, builtin_func_name=self.func_name,
                       op_name=self.op_name, threshold=threshold)

    @partial_bind_uuid
    def get_callable_from_threshold_list(self, threshold_list):
        if not threshold_list:
            threshold = None
        else:
            threshold = threshold_list[0]
        return partial(BuiltInFuncs.run, builtin_func_name=self.func_name,
                       op_name=self.op_name, threshold=threshold)


@register_strategy
class FreqStrategy(Strategy):
    """ Time-time frequency control """
    prefix = 'freq_strategy:*'
    conn = get_report_redis_client()
    source_cls = FreqSource

    def __init__(self, d):
        super(FreqStrategy, self).__init__(d)
        self.threshold = d['strategy_limit']
        self.second_count = d['strategy_time']

        name = d['strategy_source']
        keys = [x.strip() for x in d['strategy_body'].split(',')]
        self.source = self.source_cls(name, keys)

    def get_thresholds(self):
        return [self.second_count, self.threshold]

    def build_strategy_name_from_thresholds(self, thresholds):
        strategy_time, threshold = thresholds
        tmp_str = re.sub(r'[\d]+s', strategy_time + 's', self.name)
        return re.sub(r'[\d]' + _('Times'), threshold, tmp_str)

    def get_callable(self):
        return self.query_with_history

    def _build_key_member_score_map(self, history_data):
        key_member_score_map = defaultdict(list)
        for data in history_data:
            keys, member, score = self.source.get_all(data)
            for key in keys:
                key_member_score_map[key].append((member, score))
        return key_member_score_map

    def query_with_history(self, req_body, history_data):
        zkeys = self.source.get_zkeys(req_body)
        #  Can't get built-in variables, default to let go
        if not zkeys:
            return False

        second_count = int(self.second_count)
        start = time.time() - second_count
        threshold = int(self.threshold)
        key_member_score_map = self._build_key_member_score_map(history_data)

        for zkey in zkeys:
            count = 0
            for (member, score) in key_member_score_map[zkey]:
                if int(score) >= start:
                    count += 1
            if count >= threshold:
                return True
        return False

    def query(self, req_body, threshold, second_count):
        self.query_count += 1
        #  If the request is illegal, leave it by default
        if not self.source.check_key(req_body):
            logger.error(_('invalid req_body(%s)'), req_body)
            return False

        zkeys = self.source.get_zkeys(req_body)
        #  Can't get built-in variables, default to let go
        if not zkeys:
            return False

        end = time.time()
        start = end - second_count

        for zkey in zkeys:
            count = 0
            #  计数
            try:
                count = self.conn.zcount(zkey, start, end) or 0
            except redis.RedisError:
                logger.error('zcount({}, {}, {}) failed'.format(zkey,
                                                                start, end))

            #  Return final judgment result, any hit returns hit
            if count >= threshold:
                return True

        #  All misses, returns hit
        return False

    @partial_bind_uuid
    def get_callable_from_threshold_list(self, threshold_list):
        second_count, threshold = threshold_list
        second_count, threshold = int(second_count), int(threshold)
        return partial(self.query, threshold=threshold,
                       second_count=second_count)


@register_strategy
class MenuStrategy(Strategy):
    """ ListType """
    prefix = 'strategy_menu:*'

    def __init__(self, d):
        super(MenuStrategy, self).__init__(d)
        self.op_name = d['menu_op']
        self.event = d['event']
        self.dimension = d['dimension']
        self.menu_type = d['menu_type']

    def get_thresholds(self):
        return []

    def get_callable(self):
        return self.get_callable_from_threshold_list()

    def build_strategy_name_from_thresholds(self, thresholds):
        return self.name

    @partial_bind_uuid
    def get_callable_from_threshold_list(self, *args):
        return partial(hit_menu,
                       op_name=self.op_name,
                       event=self.event,
                       dimension=self.dimension,
                       menu_type=self.menu_type)


@register_strategy
class UserStrategy(Strategy):
    """ Limited User Number """
    prefix = 'user_strategy:*'
    conn = get_report_redis_client()
    source_cls = UserSource

    def __init__(self, d):
        super(UserStrategy, self).__init__(d)
        self.threshold = d['strategy_limit']
        self.daily_count = d['strategy_day']

        name = d['strategy_source']
        keys = [x.strip() for x in d['strategy_body'].split(',')]
        self.source = self.source_cls(name, keys)

    def get_thresholds(self):
        return [self.daily_count, self.threshold]

    def build_strategy_name_from_thresholds(self, thresholds):
        strategy_day, threshold = thresholds
        tmp_str = self.name
        if "That day" in self.name:
            if int(strategy_day) > 1:
                tmp_str = re.sub(r'_("That day")', strategy_day + _("Default Day"),
                                 self.name)
        else:
            if strategy_day == "1":
                tmp_str = re.sub(r'[\d]' + _('Default Day'), 'That day', self.name)
            else:
                tmp_str = re.sub(r'[\d]' + _('Default Day'), strategy_day + _('Default Day'),
                                 self.name)
        return re.sub(r'[\d]' + _('Individual_User'), threshold + _('Individual_User'), tmp_str)

    def get_callable(self):
        return self.query_with_history

    def _build_key_member_score_map(self, history_data):
        key_member_score_map = defaultdict(list)
        for data in history_data:
            keys, member, score = self.source.get_all(data)
            for key in keys:
                key_member_score_map[key].append((member, score))
        return key_member_score_map

    def query_with_history(self, req_body, history_data):
        zkeys = self.source.get_zkeys(req_body)
        #  Can't get built-in variables, default to let go
        if not zkeys:
            return False

        daily_count = int(self.daily_count)
        now = datetime.now()
        seconds = (daily_count - 1) * 86400 + now.hour * 3600 + now.minute * 60 + now.second
        start = time.time() - seconds
        threshold = int(self.threshold)
        key_member_score_map = self._build_key_member_score_map(history_data)

        for zkey in zkeys:
            hit_users = set()
            for (member, score) in key_member_score_map[zkey]:
                if int(score) >= start:
                    user_id = member.split(':', 1)[0]
                    hit_users.add(user_id)
            hit_users.discard(req_body['user_id'])
            if len(hit_users) >= threshold:
                return True
        return False

    def query(self, req_body, threshold, daily_count):
        self.query_count += 1
        #  If the request is illegal, leave it by default
        if not self.source.check_key(req_body):
            logger.error(_('invalid req_body(%s)'), req_body)
            return False

        zkeys = self.source.get_zkeys(req_body)
        if not zkeys:
            return False

        cur_time = datetime.now()
        seconds = (daily_count - 1) * 86400 + cur_time.hour * 3600 + cur_time.minute * 60 + cur_time.second
        end = time.time()
        start = math.floor(end - seconds)
        for zkey in zkeys:
            count = 0
            #  Count
            try:
                records = self.conn.zrangebyscore(zkey, start, end) or []
                hit_users = {x.split(':', 1)[0] for x in records}
                hit_users.discard(req_body['user_id'])
                count = len(hit_users)
            except redis.RedisError:
                logger.error('zrangebyscore({}, {}, {}) failed'.format(zkey,
                                                                       start,
                                                                       end))

            if count >= threshold:
                return True
        return False

    @partial_bind_uuid
    def get_callable_from_threshold_list(self, threshold_list):
        daily_count, threshold = threshold_list
        daily_count, threshold = int(daily_count), int(threshold)
        return partial(self.query, daily_count=daily_count,
                       threshold=threshold)


class Strategys(object):
    def __init__(self, *args, **kwargs):
        self.uuid_strategy_map = {}
        self.load_strategys()

    def load_strategys(self):
        uuid_strategy_map = {}
        conn = get_config_redis_client()
        logger.info('start load strategys from db, current strategy: %s', self.uuid_strategy_map.keys())
        for strategy_cls in _used_strategies:
            try:
                for name in conn.scan_iter(match=strategy_cls.prefix):
                    d = conn.hgetall(name)
                    strategy = strategy_cls(d)
                    uuid_strategy_map[strategy.uuid] = strategy
            except redis.RedisError:
                logger.error('load strategys occur redis conn error')
                return
        self.uuid_strategy_map = uuid_strategy_map
        logger.info('load strategys success, current strategy: %s',
                    self.uuid_strategy_map.keys())

    def _get_strategy_or_raise(self, uuid_):
        strategy = self.uuid_strategy_map.get(uuid_)
        if not strategy:
            raise ValueError('uuid({}) is not a valid strategy uuid'.format(uuid_))
        return strategy

    def get_thresholds(self, uuid_):
        strategy = self._get_strategy_or_raise(uuid_)
        return strategy.get_thresholds()

    def get_all_strategy_uuid_and_name(self):
        return [(uuid_, strategy.name) for (uuid_, strategy)
                in self.uuid_strategy_map.items()]

    def get_strategy_name(self, uuid_):
        strategy = self._get_strategy_or_raise(uuid_)
        return strategy.name

    def build_strategy_name_from_thresholds(self, uuid_, thresholds):
        strategy = self._get_strategy_or_raise(uuid_)
        return strategy.build_strategy_name_from_thresholds(thresholds)

    def get_callable(self, uuid_, threshold_list):
        strategy = self._get_strategy_or_raise(uuid_)
        return strategy.get_callable_from_threshold_list(threshold_list)
