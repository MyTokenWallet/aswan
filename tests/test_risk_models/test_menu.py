#!/usr/bin/env python3
# coding: utf-8

import unittest
# FIX open base.py(PYMYSQL) and delete just line 36 and 37
import pymysql

# user MySQLdb driver
pymysql.install_as_MySQLdb()  # noqa

from risk_models.menu import hit_menu
from aswan.menu.init_data import create_menu_event, add_element_to_menu


class TestBaseFunction(unittest.TestCase):

    def test_hit_menu(self):
        event_code = create_menu_event()['event_code']
        sp_element = '111111'

        dimension = 'user_id'
        menu_type = 'black'
        add_element_to_menu(event_code=event_code, menu_type=menu_type, dimension=dimension, element=sp_element)
        req_body = {'user_id': sp_element}

        self.assertEqual(
            hit_menu(req_body, 'is', event_code, dimension=dimension, menu_type=menu_type), True)

        self.assertEqual(
            hit_menu(req_body, 'is_not', event_code, dimension=dimension, menu_type=menu_type), False)

        self.assertEqual(
            hit_menu(req_body, 'is', '', dimension=dimension, menu_type=menu_type), False)

        req_body['user_id'] = 'error_user_id'
        self.assertEqual(
            hit_menu(req_body, 'is', event_code, dimension=dimension, menu_type=menu_type), False)

        req_body.clear()
        self.assertEqual(
            hit_menu(req_body, 'is', event_code, dimension=dimension, menu_type=menu_type), False)


if __name__ == '__main__':
    unittest.main()
