#!/usr/bin/env python3
# coding: utf-8

from django.utils.translation import ugettext_lazy as _
from collections import defaultdict
from django_tables2 import tables, columns

from risk_models.rule import Rules
from aswan.permissions.permission import (UserPermission, GroupPermission,
                                          UriGroupPermission)
from aswan.rule.forms import CONTROL_MAP


class HitLogDetailTable(tables.Table):
    time = columns.Column(verbose_name=_('Hit_time'))
    rule_id = columns.Column(verbose_name=_('RuleName'), orderable=False)
    group_name = columns.Column(verbose_name=_('PolicyGroupNameCall'), orderable=False)
    user_id = columns.Column(verbose_name=_('UserID'), orderable=False)
    control = columns.Column(verbose_name=_('Projectmanagement'), orderable=False)
    req_body = columns.Column(verbose_name=_('RequestBody'), orderable=False)
    hit_number = columns.Column(verbose_name=_('Whether to hit for the first time'), orderable=False)

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}

    def __init__(self, *args, **kwargs):
        self.rules = Rules(load_all=True)

    def before_render(self, request):
        pass

    @staticmethod
    def render_time(value):
        return value.strftime('%Y-%m-%d %H:%M:%S')

    def render_rule_id(self, value):
        return self.rules.get_rule_name(str(value))

    @staticmethod
    def render_control(value):
        return CONTROL_MAP.get(value, value)

    @staticmethod
    def render_hit_number(value):
        return '-' if value == 0 else _('is') if value == 1 else _('Whether')

    @staticmethod
    def render_passed_users(value):
        return '-' if value == 0 else value


class AuditLogTable(tables.Table):
    username = columns.Column(verbose_name=_("Username"), orderable=False)
    email = columns.Column(verbose_name=_("Mailbox"), orderable=False)
    role = columns.Column(verbose_name=_("Role"), empty_values=(),
                          orderable=False)
    path = columns.Column(verbose_name=_("Request_Address"), orderable=False)
    Confirm = columns.Column(verbose_name=_("ActionType"), empty_values=(),
                             orderable=False)
    method = columns.Column(verbose_name=_("How to request"), orderable=False)
    status = columns.Column(verbose_name=_("Response_Code"), orderable=False)
    req_body = columns.TemplateColumn("""
    <div style="max-width: 600px;">
        {% if record.req_body|length > 128 %}
            <a data-toggle="modal" data-target="#req_body_{{ record.id }}">
                View
            </a>
            <div class="modal inmodal" id="req_body_{{ record.id }}" tabindex="-1" role="dialog"  aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content animated fadeIn">
                        <div class="modal-header">
                            <h2>Request_Parameter</h2>
                        </div>
                        <div class="modal-body">
                        {{ record.req_body }}
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-white" data-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        {% else %}
            {{ record.req_body }}
        {% endif %}
    </div>
    """, orderable=False, verbose_name=_("Request_Parameter"))
    time = columns.DateTimeColumn(verbose_name=_("Hit_time"),
                                  format="Y-m-d H:i:s")

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}

    def __init__(self, *args, **kwargs):
        self.pk_user_map = self.pk_user_map
        self.group_name_desc_map = self.group_name_desc_map
        self.uri_desc_map = self.uri_desc_map

    @staticmethod
    def before_render(request):
        pk_user_map = {}
        for d in UserPermission.objects.all_fields():
            pk = d.get('pk')
            if pk:
                pk_user_map[pk] = d

        group_name_desc_map = {}
        for d in GroupPermission.objects.all_fields():
            name = d.get('name')
            if name:
                group_name_desc_map[name] = d.get('desc', '')

        uri_descs_map = defaultdict(list)
        for d in UriGroupPermission.objects.all_fields():
            uris = d.get('uris', [])
            for uri in uris:
                desc = d.get('desc', '')
                uri_descs_map[uri].append(desc)

        uri_desc_map = {}
        for uri, descs in uri_descs_map.items():
            rw = None
            r = None
            for desc in descs:
                if desc.endswith(_('-Write')):
                    rw = desc
                if desc.endswith(_('-Read')):
                    r = desc
            if rw and r:
                uri_desc_map[uri] = r
            elif rw and not r:
                uri_desc_map[uri] = rw.rstrip(_('-Write')) + _('-Write')
            else:
                uri_desc_map[uri] = descs[0]

    def render_role(self, value, record):
        user = self.pk_user_map.get(record.email)
        if not user:
            return _('Unknown')

        if user.get('is_superuser'):
            return _('Super_Administrator')

        groups = user.get('groups', [])
        descs = [self.group_name_desc_map.get(name, '') for name in groups]
        return ', '.join(descs)

    def render_operation(self, value, record):
        return self.uri_desc_map.get(record.path, '')
