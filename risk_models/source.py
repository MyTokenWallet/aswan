#!/usr/bin/env python3
# coding: utf-8
from django.utils.translation import gettext_lazy as _
import json
import time
import random
import logging
from collections import defaultdict
import builtins

import redis
import gevent

import config.base as conf
from clients import get_config_redis_client, get_report_redis_client

logger = logging.getLogger(__name__)

_used_source_cls_set = set()


def register_source_cls(cls):
    _used_source_cls_set.add(cls)
    return cls


class RawSource(object):
    name_keys_map = {}

    @classmethod
    def load_raw_source(cls):
        conn = get_config_redis_client()
        name_keys_map = {}

        try:
            d = conn.hgetall(conf.REDIS_SOURCE_MAP)
        except redis.RedisError:
            logger.exception(_('load raw sources error'))
            return

        for name, fields_str in d.items():
            fields = json.loads(fields_str)
            fields.pop('name_show', None)
            keys = {}
            for key_name, key_type in fields.items():
                if key_type in {'string', 'str'}:
                    key_type = 'str'
                try:
                    type_ = getattr(__builtins__, key_type)
                except AttributeError:
                    type_ = getattr(__builtins__, 'str')
                keys[key_name] = type_
            name_keys_map[name] = keys

        cls.name_keys_map = name_keys_map


class Source(object):
    """ Data source after automatic split, base class """
    prefix = None
    already_load_raw_source = False

    def __init__(self, name, keys, *args, **kwargs):
        """ name: Name: The name of the data source entered by the business side, keys: the desired key list """
        super(Source, self).__init__(*args, **kwargs)
        desired_key_list = name
        self.zkey_prefix = '_'.join(desired_key_list)
        if not self.already_load_raw_source:
            self.already_load_raw_source = True
            RawSource.load_raw_source()

        self.name = name
        self.key_type_map = {}
        for key in keys:
            self.key_type_map[key] = RawSource.name_keys_map[name][key]

        self.preserve_time = self.get_preserve_time()
        self.keys = sorted(keys)
        self.set_zkey_prefix()

    def set_zkey_prefix(self):
        lst = [self.name, self.__class__.__name__]
        lst.extend(self.keys)

    @staticmethod
    def get_preserve_time():
        return 3 * 24 * 3600

    def get_zkeys(self, data):
        keys = []
        for key_name in self.keys:
            if key_name in data:
                key = data[key_name]
                if key in ['', None]:
                    return []
                keys.append(key)
        return [u"{}:{}".format(self.zkey_prefix, '_'.join(keys))]

    def get_member(self, data):
        return str(int(time.time() * 1000))

    @staticmethod
    def get_score(data):
        return str(data['timestamp'])

    def get_all(self, data):
        return (self.get_zkeys(data),
                self.get_member(data),
                self.get_score(data))

    def check_key(self, data):
        for key_name, key_type in self.key_type_map.items():
            if key_name not in data:
                return False
            if not isinstance(data[key_name], key_type):
                return False
        return True

    def check_member(self, data):
        return True

    @staticmethod
    def check_timestamp(data):
        return 'timestamp' in data and isinstance(data['timestamp'], int)

    def check_all(self, data):
        return (self.check_key(data) and
                self.check_member(data) and
                self.check_timestamp(data))

    def __hash__(self):
        return hash(self.zkey_prefix)

    def __eq__(self, other):
        return self.zkey_prefix == other.zkey_prefix

    @classmethod
    def load(cls):
        name_sources_map = defaultdict(set)
        conn = get_config_redis_client()
        for name in conn.scan_iter(match=cls.prefix, count=100):
            d = conn.hgetall(name)
            source_name = d['strategy_source']
            keys = d['strategy_body'].split(',')
            name_sources_map[source_name].add(cls(source_name, keys))
        return name_sources_map

    def __str__(self):
        return self.name

    __repr__ = __str__


@register_source_cls
class FreqSource(Source):
    prefix = 'freq_strategy:*'


@register_source_cls
class UserSource(Source):
    prefix = 'user_strategy:*'

    def get_member(self, data):
        return _('{}:{}').format(data['user_id'], int(time.time() * 1000))

    def check_member(self, data):
        return 'user_id' in data and isinstance(data['user_id'], str)


class Sources(object):
    def __init__(self, auto_fresh=False):
        self.name_sources_map = defaultdict(set)
        self.conn = get_report_redis_client()
        if auto_fresh:
            gevent.spawn(self.refresh)

    def load_sources(self):
        name_sources_map = defaultdict(set)
        RawSource.load_raw_source()
        raw_name_source_map_lst = []
        try:
            for source_cls in _used_source_cls_set:
                raw_name_source_map_lst.append(source_cls.load())
        except redis.RedisError:
            return
        else:
            for raw_name_sources_map in raw_name_source_map_lst:
                for name, sources in raw_name_sources_map.items():
                    name_sources_map[name] |= sources
            self.name_sources_map = name_sources_map

    def refresh(self):
        while True:
            gevent.sleep(300 + random.randint(1, 60))
            logger.debug(_('start refresh sources'))
            try:
                self.load_sources()
            except Exception:
                logger.exception(_('refresh sources failed'))
            else:
                logger.debug(_('refresh sources success'))

    def get_source_or_raise(self, name):
        sources = self.name_sources_map.get(name)
        if not sources:
            raise ValueError(_('name({}) is not a source name').format(name))
        return sources

    def check_all(self, name, data):
        sources = self.get_source_or_raise(name)
        return all([source.check_all(data) for source in sources])

    def _write_one_record(self, zkey, score, member, preserve_time):
        pipeline = self.conn.pipeline()
        try:
            pipeline.zadd(zkey, score, member)
            pipeline.expire(zkey, preserve_time)
            # This is to reduce the pressure of redis storage, each time delete part of the old data, you can modify
            # the logic here
            pipeline.zremrangebyrank(zkey, 0, -128)
            pipeline.execute()
        except redis.RedisError:
            logger.error(
                f'pipeline execute error,'
                f'zkey --> {zkey},'
                f'score --> {score},'
                f'member --> {member},'
                f'preserve_time --> {preserve_time})')
            return False
        return True

    def write_all(self, name, data):
        sources = self.get_source_or_raise(name)
        coroutines = []
        for source in sources:
            zkeys, member, score = source.get_all(data)
            preserve_time = source.get_preserve_time()
            for zkey in zkeys:
                coroutines.append(
                    gevent.spawn(self._write_one_record, zkey, score, member,
                                 preserve_time)
                )
        results = gevent.joinall(coroutines)
        return all([r.value for r in results])
