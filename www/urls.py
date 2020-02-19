#!/usr/bin/env python3
# coding: utf-8
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include(('risk_auth.urls','risk_auth'), namespace='risk_auth')),
    url(r'^permissions/', include(('permissions.urls','permissions'), namespace='permissions')),
    url(r'^strategy/', include(('strategy.urls', 'strategy'), namespace='strategy')),
    url(r'^menu/', include(('menu.urls', 'menus'), namespace='menus')),
    url(r'^rule/', include(('rule.urls', 'rule'), namespace='rule')),
    url(r'^config/', include(('bk_config.urls', 'config'), namespace='config')),
    url(r'^log_manage/', include(('log_manage.urls','log_manage'), namespace='log_manage')),
]

# This section should be removed when used on the line, and the dynamic separation should be
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    from django.views.defaults import (page_not_found, server_error,
                                       permission_denied)

    urlpatterns += [
        url(r'404/', page_not_found),
        url(r'500/', server_error),
        url(r'403/', permission_denied),
    ]
