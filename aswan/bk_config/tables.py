#!/usr/bin/env python3
# coding: utf-8

from django.utils.translation import ugettext_lazy as _
from django_tables2 import tables, columns


class ConfigSourceTable(tables.Table):
    name_key = columns.Column(verbose_name=_("ConfigurationNameKey"), orderable=False)
    name_show = columns.Column(verbose_name=_("ConfigurationName"), orderable=False)
    content = columns.Column(verbose_name=_("Content"), orderable=False)
    action = columns.TemplateColumn("""
        {% load reverse_tags %}
        <a class="source-destroy" data-uri="{% url 'config:source_destroy' %}"
           data-name_key="{{ record.name_key }}">delete
        </a>
        """, orderable=False, verbose_name=_("Confirm"))

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}
