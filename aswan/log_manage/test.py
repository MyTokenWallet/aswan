#!/usr/bin/env python3
# coding: utf-8


import json
from datetime import datetime, timedelta

from django.urls import reverse

from aswan.core.testcase import BaseTestCase
from aswan.core.utils import get_sample_str
from django.db import connection

from aswan.log_manage.models import get_hit_log_model


class TestHitListDetailCase(BaseTestCase):

    @staticmethod
    def create_hit_table(date_obj):
        table_name = 'hit_log_{}'.format(date_obj.strftime('%Y%m%d'))

        model_cls = get_hit_log_model(db_table=table_name)
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model_cls)

    def test_hit_detail_view(self):
        url = reverse('log_manage:hit_list_detail')

        # common
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # With User
        data = {
            'user_id': 11
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)

        # Table does not exist with time
        right = datetime.now()
        left = right - timedelta(days=1)
        data = {
            'user_id': 11,
            'start_day': left.strftime('%Y/%m/%d'),
            'end_day': right.strftime('%Y/%m/%d')
        }
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, 200)

        # Table Exists and With Time
        self.create_hit_table(left)
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, 200)

        # With the wrong time
        data = {
            'user_id': 11,
            'start_day': get_sample_str(8),
            'end_day': get_sample_str(8)
        }
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, 200)

    def strftime(self, param):
        pass


class TestRuleStrategyMapView(BaseTestCase):

    def test_view(self):
        url = reverse('log_manage:rule_strategy_map')

        # Argument incomplete
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        t = json.loads(response.content)

        self.assertEqual(t['state'], False)
        self.assertEqual(t['rules_num'], 0)

        # all
        for rule_id in {'', 'All'}:
            data = {'rule_id': rule_id}
            response = self.client.get(url, data)
            self.assertEqual(response.status_code, 200)
            t = json.loads(response.content)

            self.assertEqual(t['state'], True)
            self.assertEqual(t['strategy_groups'], {})

        # Rule does not exist
        response = self.client.get(url, {'rule_id': 'no_exixts_rule_id'})
        self.assertEqual(response.status_code, 200)
        t = json.loads(response.content)

        self.assertEqual(t['state'], False)
        self.assertEqual(t['rules_num'], 0)

        # There are rules
        # todo


class TestAuditLogView(BaseTestCase):

    def test_view(self):
        url = reverse('log_manage:audit_logs')

        # No access
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Normal time
        right = datetime.now()
        left = right - timedelta(hours=1)
        data = {
            'time__gt': left.strftime('%Y-%m-%d %H:%M:%S'),
            'time__lt': right.strftime('%Y-%m-%d %H:%M:%S')
        }
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, 200)

        # Less access
        data.pop('time__lt')
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, 200)
