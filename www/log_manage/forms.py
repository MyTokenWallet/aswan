#!/usr/bin/env python3
# coding=utf8

import logging
from datetime import datetime, timedelta, date

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..core.forms import BaseFilterForm
from ..log_manage.models import AuditLogModel
from risk_models.rule import Rules

logger = logging.getLogger(__name__)

CONTROL_CHOICES = (
    (u'all', u"Select Project"),
    ('pass', u"pass"),
    ('deny', u"deny"),
    ('log', u"log"),
    ('message', u"SMS verification"),
    ('picture', u"Picture verification"),
    ('number', u"Digital verification"),
    ('verify', u"Review")
)


class HitLogFilterForm(BaseFilterForm):
    start_day = forms.CharField(required=False)
    end_day = forms.CharField(required=False)
    rule_id = forms.ChoiceField(label=_(u"Rule name"), required=False)
    strategy_group = forms.ChoiceField(label=_(u"PolicyGroup Name"), required=False)

    def __init__(self, *args, **kwargs):
        super(HitLogFilterForm, self).__init__(*args, **kwargs)
        today = datetime.today().strftime('%Y/%m/%d')
        seven_day_before = (datetime.today() - timedelta(days=7)).strftime(
            '%Y/%m/%d')
        self.fields['start_day'].widget.attrs[
            'placeholder'] = u'开始日期:{}'.format(seven_day_before)
        self.fields['end_day'].widget.attrs['placeholder'] = u'截止日期:{}'.format(
            today)
        self.fields['strategy_group'].choices = self._get_all_strategy_groups()
        self.fields['rule_id'].choices = self._get_all_rule_id_and_names()

    def _get_all_strategy_groups(self):
        strategy_names = Rules(load_all=True).get_all_group_uuid_and_name()
        strategy_names.insert(0, ('', u'所有PolicyGroup'))
        return strategy_names

    def _get_all_rule_id_and_names(self):
        rule_id_and_names = Rules(load_all=True).get_all_rule_id_and_name()
        rule_id_and_names.insert(0, ('', u'所有规则'))
        return rule_id_and_names

    def clean_strategy_group(self):
        strategy_group = self.cleaned_data.get('strategy_group', '')
        if strategy_group:
            strategy_group = strategy_group.split('_')[1]
        return strategy_group

    def clean_start_day(self):
        start_day = self.cleaned_data.get('start_day', '')
        if start_day:
            try:
                start_day = datetime.strptime(start_day, '%Y/%m/%d')
                start_day = start_day.date()
            except ValueError:
                start_day = date.today() - timedelta(days=7)
        else:
            start_day = date.today() - timedelta(days=7)
        return start_day

    def clean_end_day(self):
        end_day = self.cleaned_data.get('end_day', '')
        if end_day:
            try:
                end_day = datetime.strptime(end_day, '%Y/%m/%d') + timedelta(
                    days=1)
                end_day = end_day.date()
            except ValueError:
                end_day = date.today() + timedelta(days=1)
        else:
            end_day = date.today() + timedelta(days=1)
        return end_day


class HitLogDetailFilterForm(HitLogFilterForm):
    #  required set to false to ensure that the initial open page does not prompt for an error
    control = forms.ChoiceField(choices=CONTROL_CHOICES, label=_(u"Projectmanagement"),
                                required=False)
    user_id = forms.CharField(label=_(u"UserID"), required=False)

    def __init__(self, *args, **kwargs):
        super(HitLogDetailFilterForm, self).__init__(*args, **kwargs)


class AuditLogForm(forms.ModelForm, BaseFilterForm):
    time__gt = forms.DateTimeField(label=_(u"开始时间"), required=False)
    time__lt = forms.DateTimeField(label=_(u"End Time"), required=False)

    class Meta:
        model = AuditLogModel
        fields = ('username', 'email', 'path', 'method', 'status')
