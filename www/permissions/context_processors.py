#!/usr/bin/env python3
# coding: utf-8

from www.permissions.middleware import PermissionsMiddleware


def menu_by_perms(request):
    if request.user.is_authenticated():
        return {
            'project_perms': PermissionsMiddleware.get_user_perms(request.user.email),
        }
    return {
        'project_perms': []
    }
