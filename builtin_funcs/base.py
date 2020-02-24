#!/usr/bin/env python3
# coding: utf-8

import logging
from functools import wraps
import operator

from risk_models.exceptions import BuiltInFuncNotExistError

logger = logging.getLogger(__name__)
logging.basicConfig()


class BuiltInFuncs(object):
    name_callable = {}
    name_args_type = {}
    name_supported_ops = {}

    op_map = {
        'lt': operator.lt,
        'le': operator.le,
        'eq': operator.eq,
        'ne': operator.ne,
        'ge': operator.ge,
        'gt': operator.gt,
        'is': operator.is_,
        'is_not': operator.is_not
    }

    def __init__(self, desc, threshold_trans_func, run_func):
        self.desc = desc
        self.threshold_trans_func = threshold_trans_func
        self.run_func = run_func

    @classmethod
    def register(cls, desc, args_type_tuple, supported_ops,
                 threshold_trans_func=None, func_code=None):
        """
            Register the built-in function
        :param func_code:
        :param str|unicode desc: Function description (name)
        :param tuple args_type_tuple: The parameters required by the function
        :param tuple|list supported_ops: Operators supported by built-in function results
        :param callable threshold_trans_func: Threshold conversion function
        :return:
        """

        def outer(func):
            obj = cls(desc=desc, threshold_trans_func=threshold_trans_func,
                      run_func=func)

            code = func_code or func.__name__
            cls.name_callable[code] = obj
            cls.name_args_type[code] = args_type_tuple
            cls.name_supported_ops[code] = supported_ops

            @wraps(func)
            def inner(*args, **kwargs):
                return func(*args, **kwargs)

            return inner

        return outer

    @classmethod
    def check_args(cls, name, req_body):
        """
            Check Request parameter Is it legal (to meet the needs of the built-in function)
        :param str|unicode name: Built-in function code
        :param dict req_body: Request_Parameter
        :return:
        """
        args_type_tuple = cls.name_args_type[name]
        for k, type_ in args_type_tuple:
            value = req_body.get(k)
            if value is None or not isinstance(req_body[k], type_):
                return False
        return True

    @classmethod
    def get_required_args(cls, name):
        """
            Get the key required for built-in functions
        :param str|unicode name: Function code
        :return:
        """
        args_type_tuple = cls.name_args_type[name]
        return [k1 for (k1, k2) in args_type_tuple]

    def trans_result(self, rv, op_name, threshold):
        """
            Conversion of results, resulting in true/False identification whether or not the hit
        :param bool|None rv: Built-in function return value
        :param str|unicode op_name: Operator
        :param object threshold: Thresholds
        :return:
        """
        #  If you want to ignore op code forever pass then set rv as None
        if rv is None:
            return False

        if op_name in {'is', 'is_not'}:
            threshold = True
        elif self.threshold_trans_func:
            threshold = self.threshold_trans_func(threshold)

        method = self.op_map.get(op_name, None)
        return method(rv, threshold) if method else False

    def __call__(self, req_body, op_name, threshold, **kwargs):
        if not self.check_args(self.run_func.__name__, req_body):
            logger.error('run %s with invalid req_body(%s)', self, req_body)
            return False

        rv = self.run_func(req_body, **kwargs)
        return self.trans_result(rv, op_name, threshold)

    def __repr__(self):
        return self.desc

    @classmethod
    def run(cls, req_body, builtin_func_name, op_name, threshold=None,
            **kwargs):
        obj = cls.name_callable.get(builtin_func_name)
        if obj is None:
            raise BuiltInFuncNotExistError(
                '{} does not exist'.format(builtin_func_name)
            )
        return obj(req_body, op_name, threshold, **kwargs)
