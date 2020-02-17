#!/usr/bin/env python3
# coding: utf-8

from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django_tables2 import tables, columns


class RulesTable(tables.Table):
    id = columns.Column(verbose_name=_(u"Rule ID"), orderable=False)
    title = columns.Column(verbose_name=_(u"RuleName"), orderable=False)
    status = columns.Column(verbose_name=_(u"Status"), orderable=False)
    update_time = columns.Column(verbose_name=_(u"UpdateTime"), orderable=False)
    user = columns.Column(verbose_name=_(u"Update"), orderable=False)
    action = columns.TemplateColumn("""
    <span class="action-button">
        <a class="rules-on" data-uri="{% url 'rule:change' %}" data-id="{{ record.uuid }}" data-title="{{ record.title }}" data-status="{{ record.status }}">Enable</a>
    </span>
    <span class="action-button">
        <a class="rules-off" data-uri="{% url 'rule:change' %}" data-id="{{ record.uuid }}" data-title="{{ record.title }}" data-status="{{ record.status }}">Disable</a>
    </span>
    <span class="action-button">
        <a class="rules-detail" data-uri="{% url 'rule:detail' %}" data-id="{{ record.uuid }}" >Details</a>
    </span>
    <span class="action-button">
        <a class="rules-edit" data-uri="{% url 'rule:edit' %}" data-id="{{ record.uuid }}" >Edit</a>
    </span>
    """, orderable=False, verbose_name=_(u"Confirm"))

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}

    def render_update_time(self, value):
        return datetime.fromtimestamp(int(value))

    def render_status(self, value):
        return u"Enable" if value == 'on' else u"Disable"
