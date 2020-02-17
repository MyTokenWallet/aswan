#!/usr/bin/env python3
# coding: utf-8

from django.conf.urls import url
from django.urls import reverse_lazy, path
from django.views.generic import RedirectView

from www.bk_config.views import (
    ConfigSourceListView, ConfigSourceAjaxView, ConfigSourceCreateView,
    ConfigDestroyView
)

from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^$', RedirectView.as_view(url=reverse_lazy("config:source_list"), permanent=True), name="config_index"),
    url(r'^source/list/$', ConfigSourceListView.as_view(), name="source_list"),
    url(r'^source/ajax/$', ConfigSourceAjaxView.as_view(), name="source_ajax"),
    url(r'^source/create/$', ConfigSourceCreateView.as_view(), name="source_create"),
    url(r'^source/destroy/$', ConfigDestroyView.as_view(), name="source_destroy"),
]
