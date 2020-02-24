#!/usr/bin/env python3
# coding: utf-8

import random

from django.contrib.auth.models import User

from aswan.permissions.permission import UserPermission


def create_user(email, username, password, is_superuser):
    """
        Create User, which is intended for testing, so simply delete rebuild
    :param email:
    :param username: Username (for login)
    :param password: Password
    :param is_superuser:
    """
    try:
        obj = User.objects.get(username=username)
        obj.delete()
    except User.DoesNotExist:
        pass

    User.objects.create_superuser(username=username,
                                  email=email,
                                  password=password)

    import string
    last_name = ''.join(random.sample(string.ascii_lowercase, 8))
    first_name = ''.join(random.sample(string.ascii_uppercase, 8))
    if not UserPermission.objects.get(email):
        UserPermission(
            email,
            fullname='{}{}'.format(last_name, first_name),
            is_superuser=is_superuser
        ).save()
