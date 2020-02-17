#!/usr/bin/env python3
# coding=utf8


import json
from datetime import datetime, timedelta

from django.urls import reverse

from www.core.testcase import BaseTestCase
from www.core.utils import get_sample_str
from www.log_manage.init_data import create_hit_table


class TestHitListDetailCase(BaseTestCase):

    def test_hit_detail_view(self):
        url = reverse('log_manage:hit_list_detail')

        # common
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        # With User
        data = {
            'user_id': 11
        }
        response = self.client.get(url, data)
        self.assertEquals(response.status_code, 200)

        # Table does not exist with time
        right = datetime.now()
        left = right - timedelta(days=1)
        data = {
            'user_id': 11,
            'start_day': left.strftime('%Y/%m/%d'),
            'end_day': right.strftime('%Y/%m/%d')
        }
        response = self.client.get(url, data=data)
        self.assertEquals(response.status_code, 200)

        # Table Exists and With Time
        create_hit_table(left)
        response = self.client.get(url, data=data)
        self.assertEquals(response.status_code, 200)

        # With the wrong time
        data = {
            'user_id': 11,
            'start_day': get_sample_str(8),
            'end_day': get_sample_str(8)
        }
        response = self.client.get(url, data=data)
        self.assertEquals(response.status_code, 200)


class TestRuleStrategyMapView(BaseTestCase):

    def test_view(self):
        url = reverse('log_manage:rule_strategy_map')

        # Argument incomplete
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        t = json.loads(response.content)

        self.assertEquals(t['state'], False)
        self.assertEquals(t['rules_num'], 0)

        # all
        for rule_id in {u'', u'All'}:
            data = {'rule_id': rule_id}
            response = self.client.get(url, data)
            self.assertEquals(response.status_code, 200)
            t = json.loads(response.content)

            self.assertEquals(t['state'], True)
            self.assertEquals(t['strategy_groups'], {})

        # Rule does not exist
        response = self.client.get(url, {'rule_id': 'no_exixts_rule_id'})
        self.assertEquals(response.status_code, 200)
        t = json.loads(response.content)

        self.assertEquals(t['state'], False)
        self.assertEquals(t['rules_num'], 0)

        # There are rules
        # todo


class TestAuditLogView(BaseTestCase):

    def test_view(self):
        url = reverse('log_manage:audit_logs')

        # No access
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        # Normal time
        right = datetime.now()
        left = right - timedelta(hours=1)
        data = {
            'time__gt': left.strftime('%Y-%m-%d %H:%M:%S'),
            'time__lt': right.strftime('%Y-%m-%d %H:%M:%S')
        }
        response = self.client.get(url, data=data)
        self.assertEquals(response.status_code, 200)

        # Less access
        data.pop('time__lt')
        response = self.client.get(url, data=data)
        self.assertEquals(response.status_code, 200)
