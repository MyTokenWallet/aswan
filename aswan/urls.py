#!/usr/bin/env python3
# coding: utf-8
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from django.views.i18n import JavaScriptCatalog

from aswan import settings as base
from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include(('aswan.risk_auth.urls', 'risk_auth'), namespace='risk_auth')),
    url(r'^permissions/', include(('aswan.permissions.urls', 'permissions'), namespace='permissions')),
    url(r'^strategy/', include(('aswan.strategy.urls', 'strategy'), namespace='strategy')),
    url(r'^menu/', include(('aswan.menu.urls', 'menus'), namespace='menus')),
    url(r'^rule/', include(('aswan.rule.urls', 'rule'), namespace='rule')),
    url(r'^config/', include(('aswan.bk_config.urls', 'config'), namespace='config')),
    url(r'^log_manage/', include(('aswan.log_manage.urls', 'log_manage'), namespace='log_manage')),
]

urlpatterns += i18n_patterns(
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
)

# This section should be removed when used on the line, and the dynamic separation should be
# urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)
# urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)

if not settings.DEBUG:
    from django.views.defaults import (page_not_found, server_error, permission_denied)

    urlpatterns += [
        url(r'404/', page_not_found),
        url(r'500/', server_error),
        url(r'403/', permission_denied),
    ]

if not settings.configured:
    settings.configure(base, DEBUG=True)
