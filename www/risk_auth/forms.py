#!/usr/bin/env python3
# coding: utf-8

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm


class AuthenticationForm(BaseAuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    error_messages = {
        'invalid_login': _(
            u"Please enter a correct Username and password and please note that they are case sensitive."),
        'inactive': _("This account is inactive.")
    }
