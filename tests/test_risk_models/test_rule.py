#!/usr/bin/env python3
# coding: utf-8

import unittest

# FIX open base.py(PYMYSQL) and delete just line 36 and 37
import pymysql

# use MySQLdb driver
pymysql.install_as_MySQLdb()  # noqa

import django

from risk_models.rule import calculate_rule
from aswan.core.utils import get_sample_str
from aswan.menu.init_data import create_menu_event, add_element_to_menu
from aswan.strategy.init_data import create_bool_strategy, create_menu_strategy
from aswan.rule.init_data import create_rule

# init django settings
django.setup()  # noqa


class TestRule(unittest.TestCase):

    def setUp(self):
        super(TestRule, self).setUp()
        self.event_code = create_menu_event()['event_code']
        self.menu_uuid = create_menu_strategy(event_code=self.event_code,
                                              dimension='user_id',
                                              menu_type='black', menu_op='is')

        self.bool_uuid = create_bool_strategy(strategy_var='user_id',
                                              strategy_op='is',
                                              strategy_func='is_abnormal',
                                              strategy_threshold='')

        strategy_confs = [
            [get_sample_str(), self.menu_uuid, 'deny', get_sample_str(),
             '100'],
            [get_sample_str(), self.bool_uuid, 'log', get_sample_str(), '90'],
        ]
        self.rule_id, self.rule_uuid = create_rule(strategy_confs)

    def test_rule(self):
        req_body = {'user_id': '111'}

        # Hit bool-type strategy
        control, weight = calculate_rule(id_=self.rule_id, req_body=req_body)
        self.assertEqual(control, 'log')
        self.assertEqual(weight, 90)

        # Hit List strategy
        add_element_to_menu(event_code=self.event_code, menu_type='black', dimension='user_id', element='111')
        control, weight = calculate_rule(id_=self.rule_id, req_body=req_body)
        self.assertEqual(control, 'deny')
        self.assertEqual(weight, 100)


if __name__ == '__main__':
    unittest.main()
