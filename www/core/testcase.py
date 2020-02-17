#!/usr/bin/env python3
# coding: utf-8

import os

from django.test import TransactionTestCase
from django.utils.translation import gettext_lazy as _

from www.core.redis_client import get_redis_client
from www.core.pymongo_client import get_mongo_client

from www.permissions.init_data import create_user

__all__ = ['BaseTestCase']


def _get_test_mongo_client(db_name='test_risk_control'):
    return get_mongo_client(db_name)


class BaseTestCase(TransactionTestCase):
    username = 'test_superuser'
    password = 'test_test'
    email = 'test@immomo.com'

    def setUp(self):
        """Provide signed-in functionality for unit test methods"""
        super(BaseTestCase, self).setUp()
        self.client.login(username=self.username, password=self.password)

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        risk_env = os.environ.get('RISK_ENV')
        assert risk_env and risk_env == 'test', _('Note that this section can only be performed in a test environment')
        create_user(email=cls.email, username=cls.username,
                    password=cls.password, is_superuser=1)

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()

        # Clean up the test library
        db = get_mongo_client()
        db.client.drop_database(db.name)

        client = get_redis_client()
        client.flushdb()
