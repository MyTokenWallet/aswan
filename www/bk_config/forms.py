#!/usr/bin/env python3
# coding: utf-8
from django.utils.translation import gettext_lazy as _
import re
import json
from django import forms
from www.core.forms import BaseFilterForm, BaseForm
from www.core.redis_client import get_redis_client


class SourceMapForm(BaseForm):
    name_key = forms.CharField(
        min_length=2, max_length=32,
        widget=forms.TextInput(attrs={"placeholder": _("Configure key [alphanumeric underline]")})
    )
    name_show = forms.CharField(
        min_length=2, max_length=32,
        widget=forms.TextInput(attrs={"placeholder": _("Configuration name [Enter a description of]")})
    )
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            "rows": "8", "cols": "27", "placeholder": """{% trans "Configure content (json format))" %}:
{
    "user_id": "string",
    "uid": "string",
    "ip": "string"
}"""
        }))

    name_key_pattern = r"^[a-zA-Z\d_]+$"
    map_key = 'CONFIG_SOURCE_MAP'

    def clean_name_key(self):
        name_key = self.cleaned_data['name_key']
        if not re.match(self.name_key_pattern, name_key):
            raise forms.ValidationError(_("Incorrect input with some special characters"))

        client = get_redis_client()
        if client.hget(self.map_key, name_key):
            raise forms.ValidationError(_("The data source already exists"))

        return name_key

    def clean_content(self):
        content = self.cleaned_data['content']
        try:
            content = json.loads(content)
        except ValueError:
            raise forms.ValidationError(_("Wrong input，json resolution failed"))
        if not content.keys():
            raise forms.ValidationError(_("This field is required"))
        return content

    def save(self):
        client = get_redis_client()
        cd = self.cleaned_data
        name_key = cd['name_key']
        name_show = cd['name_show']
        content = cd['content']
        content.update(name_show=name_show)
        client.hset(self.map_key, name_key, json.dumps(content))
        return name_key


class SourceFilterForm(BaseFilterForm):
    name = forms.CharField(required=False, label=_(_("Data source name")))
