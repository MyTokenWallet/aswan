#!/usr/bin/env python3
# coding: utf-8

import datetime

from bson import ObjectId
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django_tables2 import tables, columns


class UserPermissionTable(tables.Table):
    fullname = columns.Column(verbose_name=_('Name'), orderable=False)
    pk = columns.Column(verbose_name=_('email'), orderable=False)
    is_superuser = columns.BooleanColumn(null=False,
                                         verbose_name=_('SuperAdministrator'),
                                         orderable=False)
    entity_id = columns.Column(verbose_name=_('First sign-in time'))
    remark = columns.Column(verbose_name=_('Note'), orderable=False)

    @classmethod
    def render_fullname(cls, record):
        url = reverse('permissions:user_update')
        html = '<a href="{}?entity_id={}">{}</a>'.format(url, record.get(
            'entity_id', ''), record.get('fullname', record['pk']))
        return format_html(html)

    @classmethod
    def render_entity_id(cls, value):
        create_time = ObjectId(value).generation_time
        # utc to local time
        create_time += datetime.timedelta(hours=8)
        return create_time.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}


class GroupPermissionTable(tables.Table):
    desc = columns.Column(verbose_name=_('Sub_Group_Name'))
    pk = columns.Column(verbose_name=_('Unique_Identification'))
    entity_id = columns.Column(verbose_name=_('Creation_Time'))
    action = columns.TemplateColumn(str('x'), orderable=False,
                                    verbose_name=_('Confirm'))

    @classmethod
    def render_action(cls, record):
        url = reverse('permissions:group_update')
        html = (
            '''
            <a href="{1}?entity_id={0}"
               style="margin-right: 10px">Change Authority
            </a>
            <a data-entity_id={0}
               class="perms-group-delete">delete
            </a>
            '''
        ).format(record.get('entity_id', ''), url)
        return format_html(html)

    @classmethod
    def render_desc(cls, value, record):
        url = reverse('permissions:group_update')
        html = '<a href="{}?entity_id={}">{}</a>'.format(
            url, record.get('entity_id', ''), value,
        )
        return format_html(html)

    @classmethod
    def render_entity_id(cls, value):
        return UserPermissionTable.render_entity_id(value)

    class Meta:
        attrs = {'class': 'table table-hover'}


class UriGroupPermissionTable(tables.Table):
    desc = columns.Column(verbose_name=_('uriGroupNameCall'))
    pk = columns.Column(verbose_name=_('Unique_Identification'))
    uris = columns.Column(verbose_name=_('Uri_List'))
    entity_id = columns.Column(verbose_name=_('Creation_Time'))
    action = columns.TemplateColumn(str('x'), orderable=False,
                                    verbose_name=_('Confirm'))

    @classmethod
    def render_action(cls, record):
        url = reverse('permissions:uri_group_update')
        html = (
            '''
            <a href="{1}?entity_id={0}"
               style="margin-right: 10px">Change Authority
            </a>
            <a data-entity_id={0}
               class="perms-uri-group-delete">delete
            </a>
            '''
        ).format(record.get('entity_id', ''), url)
        return format_html(html)

    @classmethod
    def render_desc(cls, value, record):
        url = reverse('permissions:uri_group_update')
        html = '<a href="{}?entity_id={}">{}</a>'.format(
            url, record.get('entity_id', ''), value,
        )
        return format_html(html)

    @classmethod
    def render_uris(cls, record):
        html = (
            '<pre>{}</pre>'.format('\n'.join(record['uris']))
        )
        return format_html(html)

    @classmethod
    def render_entity_id(cls, value):
        return UserPermissionTable.render_entity_id(value)

    class Meta:
        attrs = {'class': 'table table-hover'}
