#!/usr/bin/env python3
# coding: utf-8


from django.db import models
from django.db.models import Manager
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _


class AuditLogModel(models.Model):
    username = models.CharField(verbose_name=_("Username"), max_length=64,
                                blank=True)
    email = models.CharField(verbose_name=_("Mailbox"), max_length=128, blank=True)
    path = models.CharField(verbose_name=_("Request address"), max_length=128,
                            blank=True)
    status = models.CharField(verbose_name=_("Response_Code"), max_length=32,
                              blank=True)
    method = models.CharField(verbose_name=_("Request_Type"), max_length=32,
                              blank=True)
    req_body = models.TextField(verbose_name=_("Request_Parameter"), blank=True)
    time = models.DateTimeField(verbose_name=_('Operating_Time'), auto_now_add=True)

    class Meta:
        db_table = "user_audit_log"
        ordering = ('-time',)
        verbose_name = _('Audit log')

    def __unicode__(self):
        return self.username

    objects = Manager()


def get_hit_log_model(db_table):
    class CustomMetaClass(ModelBase):
        def __new__(cls, name, bases, attrs):
            model = super(CustomMetaClass, cls).__new__(cls, name, bases,attrs)
            model._meta.db_table = db_table
            model._meta.index_together = (
                ('time',),
                ('user_id',),
            )
            model.managed = False
            return model

    class HitLogModel(models.Model, metaclass=CustomMetaClass):
        time = models.DateTimeField(verbose_name=_('Hit time'))
        rule_id = models.IntegerField(verbose_name=_('Rule ID'))
        user_id = models.IntegerField(verbose_name=_('Hit User'))
        kwargs = models.CharField(max_length=128, null=False, default='', verbose_name=_('Extended parameter'))
        req_body = models.CharField(max_length=512, null=False, default='', verbose_name=_('Request_Parameter'))
        control = models.CharField(max_length=16, null=False, default='', verbose_name=_('Projectmanagement'))
        custom = models.CharField(max_length=50, null=False, default='', verbose_name=_('Strategy Group Explained'))
        group_name = models.CharField(max_length=256, null=False, default='',
                                      verbose_name=_('PolicyGroupNameCall'))
        group_uuid = models.CharField(max_length=36, null=False, default='',
                                      verbose_name=_('PolicyGroupUUID'))
        hit_number = models.PositiveSmallIntegerField(null=False, default=1, verbose_name=_('Hit order'))

        objects = Manager()

    return HitLogModel
