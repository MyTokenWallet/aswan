#!/usr/bin/env python3
# coding: utf-8

from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django_tables2 import tables, columns


class RulesTable(tables.Table):
    id = columns.Column(verbose_name=_("Rule_ID"), orderable=False)
    title = columns.Column(verbose_name=_("RuleName"), orderable=False)
    status = columns.Column(verbose_name=_("Status"), orderable=False)
    update_time = columns.Column(verbose_name=_("UpdateTime"), orderable=False)
    user = columns.Column(verbose_name=_("Updater"), orderable=False)
    action = columns.TemplateColumn("""
    <span class="action-button">
        <a class="rules-on" data-uri="{% url 'rule:change' %}" data-id="{{ record.uuid }}" 
        data-title="{{ record.title }}" data-status="{{ record.status }}">Enable</a>
    </span>
    <span class="action-button">
        <a class="rules-off" data-uri="{% url 'rule:change' %}" data-id="{{ record.uuid }}" 
        data-title="{{ record.title }}" data-status="{{ record.status }}">Disable</a>
    </span>
    <span class="action-button">
        <a class="rules-detail" data-uri="{% url 'rule:detail' %}" 
        data-id="{{ record.uuid }}" >Details</a>
    </span>
    <span class="action-button">
        <a class="rules-edit" data-uri="{% url 'rule:edit' %}" 
        data-id="{{ record.uuid }}" >Edit</a>
    </span>
    """, orderable=False, verbose_name=_("Confirm"))

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}

    @staticmethod
    def render_update_time(value):
        return datetime.fromtimestamp(int(value))

    @staticmethod
    def render_status(value):
        return _("Enable") if value == 'on' else _("Disable")
