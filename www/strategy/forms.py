#!/usr/bin/env python3
# coding: utf-8
import copy
import uuid
import json

from functools import reduce
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from builtin_funcs import BuiltInFuncs
from www.core.redis_client import get_redis_client
from www.core.forms import BaseForm, BaseFilterForm
from www.core.pymongo_client import get_mongo_client

OP_CHOICES = (
    ('is', u'Yes (use, already)'),
    ('is_not', u'Not (not used, not yet)'),
    ('lt', u'Less than...'),
    ('le', u'Less than or equal to...'),
    ('eq', u'Equals...'),
    ('ne', u'Not equal'),
    ('ge', u'Greater than or equal to...'),
    ('gt', u'Greater than...'),
)

FUNC_CHOICES = tuple(
    [(k, str(v)) for k, v in BuiltInFuncs.name_callable.items()]
)
VAR_CHOICES = (
    ('user_id', u'Account_ID'),
    ('phone', u'CellPhoneNumber'),
    ('uid', u'CurrentDevice_ID'),
    ('ip', u'Current_IP'),
    ('reg_ip', u'SignUpFrom_IP'),
    ('reg_uid', u'RegisterDevice_ID'),
)

DIM_CHOICES_MENU = (
    ('user_id', u'Account_ID'),
    ('phone', u'CellPhoneNumber'),
    ('ip', u'Current_IP'),
    ('reg_ip', u'SignUpFrom_IP'),
    ('uid', u'CurrentDevice_ID'),
    ('reg_uid', u'RegisterDevice_ID'),
)
OP_CHOICES_MENU = (
    ('is', u'is'),
    ('is_not', u'is_not'),
)
TYPE_CHOICES_MENU = (
    (u'black', u'Blacklist'),
    (u'white', u'White List'),
    (u'gray', u'Grey List')
)

OP_MAP = dict(OP_CHOICES)
FUNC_MAP = dict(FUNC_CHOICES)
VAR_MAP = dict(VAR_CHOICES)
DIM_MAP_MENU = dict(DIM_CHOICES_MENU)
TYPE_MAP_MENU = dict(TYPE_CHOICES_MENU)
OP_MAP_MENU = dict(OP_CHOICES_MENU)

FREQ_STRATEGY_UNIQ_SET_KEYS = (
    'strategy_source', 'strategy_body', 'strategy_time', 'strategy_limit')
USER_STRATEGY_UNIQ_SET_KEYS = (
    'strategy_source', 'strategy_body', 'strategy_day', 'strategy_limit')


class BoolStrategyForm(BaseForm):
    strategy_name = forms.CharField(label=_(u"PolicyName"))
    strategy_desc = forms.CharField(required=False, label=_(u"PolicyDescription"))
    strategy_var = forms.ChoiceField(label=_(u"Built-in variables"), choices=VAR_CHOICES)
    strategy_op = forms.ChoiceField(label=_(u"ActionCode"), choices=OP_CHOICES)
    strategy_func = forms.ChoiceField(label=_(u"Built-in functions"), choices=FUNC_CHOICES)
    strategy_threshold = forms.CharField(label=_(u"Thresholds"), required=False)

    def __init__(self, *args, **kwargs):
        self.values_sign = None
        super(BoolStrategyForm, self).__init__(*args, **kwargs)

    def save(self):
        client = get_redis_client()
        uuid_ = str(uuid.uuid4())
        name = 'bool_strategy:{}'.format(uuid_)
        payload = {}
        for key in ('strategy_name', 'strategy_desc', 'strategy_var',
                    'strategy_op', 'strategy_func', 'strategy_threshold'):
            payload[key] = self.cleaned_data.get(key, '')
        payload['uuid'] = uuid_
        client.hmset(name, payload)
        client.sadd(settings.STRATEGY_SIGN_KEY, self.values_sign)
        return uuid_

    def is_exists(self, cleaned_data):
        client = get_redis_client()
        temp = copy.deepcopy(cleaned_data)
        temp.pop("strategy_desc", None)
        temp.pop("strategy_name", None)
        keys = sorted(temp.keys())
        values_sign = "".join([temp[x] for x in keys])
        exists = client.sismember(settings.STRATEGY_SIGN_KEY, values_sign)
        self.values_sign = values_sign
        if exists in (0, '0'):
            return False
        return True

    @staticmethod
    def _get_display_names(names):
        display_names = []
        for english_name, display_name in VAR_CHOICES:
            for name in names:
                if name == english_name:
                    display_names.append(display_name)
        return ','.join(display_names)

    def clean(self):
        cd = self.cleaned_data
        op_name = cd['strategy_op']
        threshold = cd['strategy_threshold']
        func_name = cd['strategy_func']
        var_name = cd['strategy_var']
        supported_ops = BuiltInFuncs.name_supported_ops[func_name]
        required_args = BuiltInFuncs.get_required_args(func_name)

        if self.is_exists(cd):
            self.errors['strategy_name'] = [u"This record already exists, do not add it repeatedly"]

        if var_name not in required_args:
            self.errors['strategy_var'] = [u'The built-in variables supported by the function are'.format(
                func_name,
                self._get_display_names(required_args)
            )]

        if op_name not in supported_ops:
            self.errors['strategy_op'] = [u'This ActionCode is not supported by the function'.format(func_name)]
        if op_name in ('is', 'is_not') and threshold:
            self.errors['strategy_op'] = [u'[{}]The ActionCode does not accept the threshold'.format(op_name)]

        if op_name in {'lt', 'le', 'eq', 'ne', 'ge', 'gt'}:
            if not threshold:
                self.errors['strategy_threshold'] = [
                    u'ActionCode{}Thresholds must be included'.format(op_name)]
        return cd


class BoolStrategyTestForm(BaseForm):
    req_body = forms.CharField(widget=forms.Textarea, label=_(u"RequestBody"))
    strategy = forms.ChoiceField(label=_(u"Strategy"), widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(BoolStrategyTestForm, self).__init__(*args, **kwargs)
        self.fields['strategy'].choices = self._build_strategy_choices()

    @classmethod
    def _build_strategy_choices(cls):
        client = get_redis_client()
        choices = []
        for name in client.scan_iter(match="bool_strategy:*"):
            d = client.hgetall(name)
            if 'uuid' in d and 'strategy_name' in d:
                choices.append((d['uuid'], d['strategy_name']))
        choices.sort()
        return choices

    def clean_req_body(self):
        req_body = self.cleaned_data.get('req_body', '')
        try:
            req_body = json.loads(req_body)
        except ValueError:
            raise forms.ValidationError(u"RequestBody Not legal json format")
        return req_body


class FreqStrategyTestForm(BoolStrategyTestForm):
    history_data = forms.CharField(widget=forms.Textarea, label=_(u"Historical data"),
                                   required=False)

    def clean_history_data(self):
        history_data = self.cleaned_data.get('history_data') or None
        if history_data:
            try:
                history_data = json.loads(history_data)
            except ValueError:
                raise forms.ValidationError(u"Historical data Not legal json format")
        return history_data

    @classmethod
    def _build_strategy_choices(cls):
        client = get_redis_client()
        choices = []
        for name in client.scan_iter(match="freq_strategy:*"):
            d = client.hgetall(name)
            if 'uuid' in d and 'strategy_name' in d:
                choices.append((d['uuid'], d['strategy_name']))
        # choices.insert(0, ("", u"Please choose a PolicyName"))
        return choices


class FreqStrategyForm(BaseForm):
    strategy_name = forms.CharField(label=_(u"PolicyName"))
    strategy_desc = forms.CharField(required=False, label=_(u"PolicyDescription"))
    strategy_source = forms.CharField(label=_(u"DataSources"))
    strategy_body = forms.CharField(label=_(u"BodyName"), required=True,
                                    help_text=u"Example: The same account with the same IP address to grab the red envelope limit 1 time, check: UserID,Current_IP")
    strategy_time = forms.CharField(label=_(u"Period (in seconds))"),
                                    help_text=u"Supports both 86400 and 24 x 60 x 60 input formats.")
    strategy_limit = forms.IntegerField(min_value=1, label=_(u"Maximum"),
                                        initial=1)

    def __init__(self, *args, **kwargs):
        self.values_sign = None
        super(FreqStrategyForm, self).__init__(*args, **kwargs)

    def clean_strategy_time(self):
        strategy_time = self.cleaned_data.get("strategy_time", '')
        if "*" in strategy_time:
            args = strategy_time.split("*")
            try:
                for a in args:
                    assert int(a) > 0
                strategy_time = reduce(lambda x, y: x * y, map(int, args))
                assert strategy_time > 0
            except (ValueError, AssertionError):
                raise forms.ValidationError(u"The parameters are illegal and only support positive integers and")
        else:
            try:
                strategy_time = int(strategy_time)
                assert strategy_time > 0
            except (ValueError, AssertionError):
                raise forms.ValidationError(u"The parameters are illegal and only support positive integers and")
        return strategy_time

    def clean(self):
        client = get_redis_client()
        cd = self.cleaned_data
        source_key = cd['strategy_source']
        strategy_body_str = cd['strategy_body']
        valid_bodys = json.loads(client.hget('CONFIG_SOURCE_MAP', source_key))
        for strategy_body in strategy_body_str.split(','):
            if strategy_body not in valid_bodys:
                self.errors['strategy_body'] = [u"The data source is not{}。".format(strategy_body)]
                return

        fields = [str(cd.get(x, "")) for x in FREQ_STRATEGY_UNIQ_SET_KEYS]
        if not all(fields):
            return
        values_sign = ":".join(fields)
        if client.sismember(settings.STRATEGY_SIGN_KEY, values_sign):
            self.errors['strategy_name'] = [u"This record already exists, do not add it repeatedly"]
        self.values_sign = values_sign

    def save(self):
        client = get_redis_client()
        uuid_ = str(uuid.uuid4())
        name = 'freq_strategy:{}'.format(uuid_)
        payload = {}
        for key in ('strategy_name', 'strategy_desc', 'strategy_time',
                    'strategy_body', 'strategy_limit', 'strategy_source'):
            payload[key] = self.cleaned_data.get(key, '')
        payload['uuid'] = uuid_
        client.hmset(name, payload)
        client.sadd(settings.STRATEGY_SIGN_KEY, self.values_sign)
        return uuid_


class UserStrategyForm(BaseForm):
    strategy_name = forms.CharField(label=_(u"PolicyName"))
    strategy_desc = forms.CharField(required=False, label=_(u"PolicyDescription"))
    strategy_source = forms.CharField(label=_(u"DataSources"))
    strategy_body = forms.CharField(label=_(u"BodyName"),
                                    help_text=u"Example: Same device on the same day only 5 User gifts plus blessing value, check: current device")
    strategy_day = forms.IntegerField(min_value=1, label=_(u"Default days (in units): Individual)"),
                                      initial=1)
    strategy_limit = forms.IntegerField(min_value=1, label=_(u"Limit the number of Users"),
                                        initial=1)

    def __init__(self, *args, **kwargs):
        self.values_sign = None
        super(UserStrategyForm, self).__init__(*args, **kwargs)

    def clean_strategy_day(self):
        strategy_day = self.cleaned_data.get("strategy_day", '')
        try:
            strategy_day = int(strategy_day)
            assert strategy_day >= 0
        except(ValueError, AssertionError):
            raise forms.ValidationError(
                u"The argument is not legal, please enter an integer greater than or equal to 0")
        return strategy_day

    def clean(self):
        client = get_redis_client()
        cd = self.cleaned_data
        source_key = cd['strategy_source']
        strategy_body_str = cd.get('strategy_body', '')
        valid_bodys = json.loads(client.hget('CONFIG_SOURCE_MAP', source_key))
        for strategy_body in strategy_body_str.split(','):
            if strategy_body not in valid_bodys:
                self.errors['strategy_body'] = [
                    u"The data source is not{}。".format(strategy_body)]
                return

        fields = [str(cd.get(x, "")) for x in USER_STRATEGY_UNIQ_SET_KEYS]
        if not all(fields):
            return
        values_sign = ":".join(fields)
        client = get_redis_client()
        if client.sismember(settings.STRATEGY_SIGN_KEY, values_sign):
            self.errors['strategy_name'] = [u"This record already exists, do not add it repeatedly"]
        self.values_sign = values_sign

    def save(self, *args, **kwargs):
        client = get_redis_client()
        uuid_ = str(uuid.uuid4())
        name = 'user_strategy:{}'.format(uuid_)
        payload = {}
        for key in ('strategy_name', 'strategy_desc', 'strategy_day',
                    'strategy_body', 'strategy_limit', 'strategy_source'):
            payload[key] = self.cleaned_data.get(key, '')
        payload['uuid'] = uuid_
        client.hmset(name, payload)
        client.sadd(settings.STRATEGY_SIGN_KEY, self.values_sign)
        return uuid_


class UserStrategyTestForm(BoolStrategyTestForm):
    history_data = forms.CharField(widget=forms.Textarea, label=_(u"Historical data"),
                                   required=False)

    def clean_history_data(self):
        history_data = self.cleaned_data.get('history_data') or None
        if history_data:
            try:
                history_data = json.loads(history_data)
            except ValueError:
                raise forms.ValidationError(u"Historical data Not legal json format")
        return history_data

    @classmethod
    def _build_strategy_choices(cls):
        client = get_redis_client()
        choices = []
        for name in client.scan_iter(match="user_strategy:*"):
            d = client.hgetall(name)
            if 'uuid' in d and 'strategy_name' in d:
                choices.append((d['uuid'], d['strategy_name']))
        return choices


class MenuStrategyForm(BaseForm):
    dimension = forms.ChoiceField(label=_(u"Dimensions"), choices=DIM_CHOICES_MENU)
    menu_op = forms.ChoiceField(label=_(u"ActionCode"), choices=OP_CHOICES_MENU)
    event = forms.ChoiceField(label=_(u"Project"))
    menu_type = forms.ChoiceField(label=_(u"ListType"),
                                  choices=TYPE_CHOICES_MENU)  # It's a built-in function.
    strategy_name = forms.CharField(label=_(u"PolicyName"))
    strategy_desc = forms.CharField(required=False, label=_(u"PolicyDescription"))

    def __init__(self, *args, **kwargs):
        super(MenuStrategyForm, self).__init__(*args, **kwargs)
        self.fields['event'].choices = self._build_event_choices()
        self.values_sign = None

    @classmethod
    def _build_event_choices(cls):
        db = get_mongo_client()
        choices = [(x["event_code"], x["event_name"]) for x in
                   db['menu_event'].find()]
        return choices

    def clean(self):
        cd = self.cleaned_data
        if self.is_exists(cd):
            self.errors['strategy_name'] = [u"This record already exists, do not add it repeatedly"]

    def save(self, *args, **kwargs):
        client = get_redis_client()
        uuid_ = str(uuid.uuid4())
        name = 'strategy_menu:{}'.format(uuid_)
        payload = {'uuid': uuid_}
        for key in (
                'strategy_name', 'strategy_desc', 'menu_op', 'event',
                'dimension',
                'menu_type'):
            payload[key] = self.cleaned_data.get(key, '')

        client.hmset(name, payload)
        client.sadd(settings.STRATEGY_SIGN_KEY, self.values_sign)
        return uuid_

    def is_exists(self, cleaned_data):
        client = get_redis_client()
        temp = copy.deepcopy(cleaned_data)
        temp.pop("strategy_desc", None)
        temp.pop("strategy_name", None)
        keys = sorted(temp.keys())
        values_sign = "".join([temp[x] for x in keys])
        exists = client.sismember(settings.STRATEGY_SIGN_KEY, values_sign)
        self.values_sign = values_sign
        if exists in (0, '0'):
            return False
        return True


class MenuStrategyTestForm(BaseForm):
    req_body = forms.CharField(widget=forms.Textarea, label=_(u"RequestBody"))
    strategy = forms.ChoiceField(label=_(u"Strategy"), widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(MenuStrategyTestForm, self).__init__(*args, **kwargs)
        self.fields['strategy'].choices = self._build_strategy_choices()

    @classmethod
    def _build_strategy_choices(cls):
        client = get_redis_client()
        choices = []
        for name in client.scan_iter(match="strategy_menu:*"):
            d = client.hgetall(name)
            if 'uuid' in d and 'strategy_name' in d:
                choices.append((d['uuid'], d['strategy_name']))
        choices.sort()
        return choices

    def clean_req_body(self):
        req_body = self.cleaned_data.get('req_body', '')
        try:
            req_body = json.loads(req_body)
        except ValueError:
            raise forms.ValidationError(u"RequestBody Not legal json format")
        return req_body


class StrategyFilterForm(BaseFilterForm):
    filter_name = forms.CharField(label=_(u"PolicyName"), required=False)
