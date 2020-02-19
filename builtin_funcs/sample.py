#!/usr/bin/env python3
# coding: utf-8
from django.utils.translation import gettext as _
from builtin_funcs import BuiltInFuncs


@BuiltInFuncs.register(desc=_('Abnormal User'),
                       args_type_tuple=(('user_id', str),),
                       supported_ops=('is', 'is_not'))
def is_abnormal(req_body):
    user_id = req_body['user_id']
    user_key = user_id[-1]

    # Special User, go straight to let go
    if user_key == '0':
        return None

    if user_key in {'1', '2', '3', '4'}:
        # If the criteria for the determination are met, the hit is considered to be
        return True
    else:
        # Otherwise, no hit
        return False


@BuiltInFuncs.register(desc=_('Number of historical logins'),
                       args_type_tuple=(('user_id', str),),
                       supported_ops=('gt', 'ge', 'lt', 'le', 'eq', 'neq'),
                       threshold_trans_func=int
                       )
def user_login_count(req_body):
    user_id = req_body['user_id']
    user_key = user_id[-1]

    # Unacquired value / Special User Direct Pass
    if user_key == '0':
        return None

    # Get user values on this dimension by various methods (http, hard-coded, rpc, etc.)
    if user_id[-1] in {'1', '2', '3', '4'}:
        return 40
    else:
        return 200
