#!/usr/bin/env python3
# coding: utf-8

import json

from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from www.core.forms import BaseFilterForm, BaseForm
from risk_models.strategy import Strategys
from risk_models.rule import Rules
from www.rule.models import RuleModel

STATUS_CHOICES = (
    ('on', u"Enable"),
    ('off', u"Disable"),
)
CONTROL_CHOICES = (
    ('', u"Select Project"),
    ('pass', u"pass"),
    ('deny', u"deny"),
    ('log', u"log"),
    ('message', u"SMS verification"),
    ('picture', u"Picture verification"),
    ('number', u"Digital verification"),
    ('verify', u"Review")
)
CONTROL_MAP = {
    k: v for k, v in CONTROL_CHOICES if k
}


class RulesForm(BaseForm):
    title = forms.CharField(label=_(u"RuleName"))
    describe = forms.CharField(required=False, label=_(u"Rule description"),
                               widget=forms.Textarea)
    status = forms.ChoiceField(label=_(u"Status"), choices=STATUS_CHOICES)
    end_time = forms.DateTimeField()
    strategy = forms.ChoiceField(label=_("Policy"), required=False)
    control = forms.ChoiceField(label=_("Projectmanagement"), choices=CONTROL_CHOICES,
                                required=False)
    custom = forms.CharField(label=_(u"Customer service skills"), required=False,
                             widget=forms.Textarea(
                                 attrs={'placeholder': u'Customer service skills',
                                        'data-autoresize': '',
                                        'rows': '1',
                                        'cols': 'auto'}))
    strategys = forms.CharField(required=True)
    controls = forms.CharField(required=True)
    customs = forms.CharField()
    names = forms.CharField(required=True)
    weights = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(RulesForm, self).__init__(*args, **kwargs)
        strategy_choices = self._get_all_strategys()
        self.fields['strategy'].choices = strategy_choices
        self.strategy_names = strategy_choices

    @classmethod
    def _get_all_strategys(cls):
        return Strategys().get_all_strategy_uuid_and_name()

    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']
        if end_time <= timezone.now():
            raise forms.ValidationError(_(u"The end time should be greater than the current time"))
        return end_time

    def clean_weights(self):
        weights = self.cleaned_data['weights']
        seps = weights.split(',')
        for num in seps:
            if not num.isdigit():
                raise forms.ValidationError(_(u"Weight value is not a number"))
        return weights

    def _check_names(self, names, choices, sep=None):
        valid_names = set()
        for english, chinese in choices:
            if english:
                valid_names.add(english)
        if sep:
            all_names = []
            for name in names:
                for e in name.split(sep):
                    all_names.append(e)
            names = all_names
        return all([name in valid_names for name in names])

    def clean(self):
        cd = super(RulesForm, self).clean()

        # If there's already a problem, don't continue the verification.
        if self.errors:
            return cd

        strategys_list = cd['strategys'].split(',')
        controls = cd['controls'].split(',')
        customs = cd.get('customs', '').split(':::')
        names = cd['names'].split(':::')
        if not len(strategys_list) == len(controls) == len(customs) == len(
                names):
            self.errors['customs'] = [u'PolicyGroupName、Policy、Projectmanagement、Customer service does not match']
        if not self._check_names(strategys_list, self._get_all_strategys(),
                                 sep=';'):
            self.errors['strategys'] = [u'Illegal PolicyName']
        if not self._check_names(controls, CONTROL_CHOICES):
            self.errors['controls'] = [u'Illegal Projectmanagement Name']
        strategy_uuids = []
        for strategy in strategys_list:
            item = strategy.split(';')
            item.sort()
            strategy_uuids.append("".join(item))
        if len(set(strategy_uuids)) < len(strategy_uuids):
            self.errors['strategys'] = [u'Policy already exist']
        return cd

    def save(self, *args, **kwargs):
        cd = self.cleaned_data

        names = cd['names'].split(':::')
        controls = cd['controls'].split(',')
        strategys = cd['strategys'].split(',')
        customs = cd.get('customs', '').split(':::')
        weights = [int(x) for x in cd['weights'].split(',')]

        return RuleModel.create(creator_name=self.request.user.username,
                                title=cd['title'],
                                describe=cd['describe'], status=cd['status'],
                                end_time=cd['end_time'],
                                strategy_confs=zip(names, strategys, controls,
                                                   customs,
                                                   weights))


class RulesTestForm(BaseForm):
    req_body = forms.CharField(widget=forms.Textarea, label=_(u"RequestBody"))
    rule = forms.ChoiceField(label=_(u"RuleName"), widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(RulesTestForm, self).__init__(*args, **kwargs)
        self.fields['rule'].choices = self._build_rule_choices()

    @classmethod
    def _build_rule_choices(cls):
        return Rules().get_all_rule_uuid_and_name()

    def clean_req_body(self):
        req_body = self.cleaned_data.get('req_body', '')
        try:
            req_body = json.loads(req_body)
        except ValueError:
            raise forms.ValidationError(u"RequestBody Not legal json format")
        return req_body


class RulesFilterForm(BaseFilterForm):
    status = forms.ChoiceField(label=_(u"Status"),
                               choices=(('', 'All States'),) + STATUS_CHOICES,
                               required=False)
    rule_name = forms.CharField(label=_(u"RuleName(Fuzzy queries)"), required=False)
