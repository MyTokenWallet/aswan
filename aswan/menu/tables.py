#!/usr/bin/env python3
# coding: utf-8

from django.utils.translation import gettext_lazy as _
from django_tables2 import tables, columns
from aswan.core.pymongo_client import get_mongo_client
from aswan.core.columns import TruncateColumn
from aswan.menu.forms import MENU_TYPE_NAME_MAP


class EventTable(tables.Table):
    event_name = columns.Column(verbose_name=_("Project name"))
    action = columns.TemplateColumn("""
    <a class="event-destroy" data-uri="{% url 'menus:event_destroy' %}" data-id="{{ record.event_code }}">
    delete</a>
    """, orderable=False, verbose_name=_("action"))

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}


class BaseMenuTable(tables.Table):
    check_all = columns.TemplateColumn("""
        {% load reverse_tags %}
        <input class="menu-item" data-id="{{ record|mongo_id }}" type="checkbox" />
        """, orderable=False, verbose_name="")
    value = columns.Column(verbose_name=_("Value"))
    event_code = columns.Column(verbose_name=_("Project"))
    menu_type = columns.Column(verbose_name=_("ListType"))
    menu_status = columns.Column(verbose_name=_("Status"))
    menu_desc = TruncateColumn(verbose_name=_("Note"))
    end_time = columns.DateTimeColumn(format="Y-m-d H:i:s", verbose_name=_("EndTime"))
    create_time = columns.DateTimeColumn(format="Y-m-d H:i:s", verbose_name=_("UpdateTime"))
    creator = columns.Column(verbose_name=_("Operator"))

    def __init__(self, *args, **kwargs):
        super(BaseMenuTable, self).__init__(*args, **kwargs)
        self.deletable = True

    @staticmethod
    def render_menu_type(value):
        return MENU_TYPE_NAME_MAP.get(value, value)

    @staticmethod
    def render_event_code(value):
        db = get_mongo_client()
        res = db.menu_event.find_one({'event_code': value})
        if not res:
            return value
        return res.get('event_name', value)


class UseridTable(BaseMenuTable):
    value = columns.Column(verbose_name=_("UserID"))

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}


class IPTable(BaseMenuTable):
    value = columns.Column(verbose_name=_("IP_Address"))

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}


class UidTable(BaseMenuTable):
    value = columns.Column(verbose_name=_("Device_ID"))

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}


class PayTable(BaseMenuTable):
    value = columns.Column(verbose_name=_("Payment account number"))

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}


class PhoneTable(BaseMenuTable):
    value = columns.Column(verbose_name=_("CellPhoneNumber"))

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}
