#!/usr/bin/env python3
# coding=utf8

from django.urls import reverse
from django.contrib.auth.models import User

from ..core.testcase import BaseTestCase


class TestRiskAuthView(BaseTestCase):
    login_uri = 'risk_auth:risk_login'
    logout_uri = 'risk_auth:risk_logout'

    def setUp(self):
        """ No login is required here """
        self.username = 'test_user'
        self.email = 'test@momo.com'
        self.password = 'test_password'

    def _test_login(self):
        # The request is not done in the wrong way.
        url = reverse(self.login_uri)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        # 参数不全
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)

        # Non-existent User
        response = self.client.post(url, data={'username': self.username,
                                               'password': self.password})
        self.assertEquals(response.status_code, 200)

        # Ordinary User
        User.objects.create_user(self.username, password=self.password)
        response = self.client.post(url, data={'username': self.username,
                                               'password': self.password})
        self.assertEquals(response.status_code, 302)

        # Request again after logging in
        response = self.client.post(url, data={'username': self.username,
                                               'password': self.password})
        self.assertEquals(response.status_code, 302)

        # Clean User
        User.objects.filter(username=self.username).delete()

        # Super User
        User.objects.create_superuser(self.username, password=self.password,
                                      email=self.email)
        response = self.client.post(url, data={'username': self.username,
                                               'password': self.password})
        self.assertEquals(response.status_code, 302)

    def _test_logout(self):
        url = reverse(self.logout_uri)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_view(self):
        self._test_login()
        self._test_logout()
