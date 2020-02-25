#!/usr/bin/env python3
# coding: utf-8

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Manager
from django.db.models.base import ModelBase


class AuditLogModel(models.Model):
    username = models.CharField(verbose_name="username", max_length=64, blank=True)
    email = models.CharField(verbose_name="email", max_length=128, blank=True)
    path = models.CharField(verbose_name="path", max_length=128, blank=True)
    status = models.CharField(verbose_name="status", max_length=32, blank=True)
    method = models.CharField(verbose_name="method", max_length=32, blank=True)
    req_body = models.TextField(verbose_name="req_body", blank=True)
    time = models.DateTimeField(verbose_name="Hit_time", auto_now_add=True)

    class Meta:
        db_table = "user_audit_log"
        ordering = ('-time',)
        verbose_name = _('Audit_log')

    def __unicode__(self):
        return self.username

    objects = Manager()


def get_hit_log_model(db_table):
    class CustomMetaClass(ModelBase):
        def __new__(mcs, name, bases, attrs):
            model = super(CustomMetaClass, mcs).__new__(mcs, name, bases, attrs)
            model._meta.db_table = db_table
            model._meta.index_together = (('time',), ('user_id',),)
            model.managed = False

            return model

    class HitLogModel(models.Model, metaclass=CustomMetaClass):
        time = models.DateTimeField(verbose_name=_('Hit_time'))
        rule_id = models.IntegerField(verbose_name=_('Rule_ID'))
        user_id = models.IntegerField(verbose_name=_('Hit_User'))

        kwargs = models.CharField(max_length=128, null=False, default='', verbose_name=_('Extended parameter'))
        req_body = models.CharField(max_length=512, null=False, default='', verbose_name=_('Request_Parameter'))
        control = models.CharField(max_length=16, null=False, default='', verbose_name=_('Projectmanagement'))
        custom = models.CharField(max_length=50, null=False, default='', verbose_name=_('Strategy Group Explained'))
        group_name = models.CharField(max_length=256, null=False, default='', verbose_name=_('PolicyGroupNameCall'))
        group_uuid = models.CharField(max_length=36, null=False, default='', verbose_name=_('PolicyGroupUUID'))
        hit_number = models.PositiveSmallIntegerField(null=False, default=1, verbose_name=_('Hit_Order'))

        objects = Manager()

    return HitLogModel
