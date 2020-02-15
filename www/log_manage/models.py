#!/usr/bin/env python3
# coding=utf8


from django.db import models
from django.db.models import Manager
from django.db.models.base import ModelBase
from django.utils.translation import ugettext_lazy as _


class AuditLogModel(models.Model):
    username = models.CharField(verbose_name=_(u"Username"), max_length=64,
                                blank=True)
    email = models.CharField(verbose_name=_(u"Mailbox"), max_length=128, blank=True)
    path = models.CharField(verbose_name=_(u"Request address"), max_length=128,
                            blank=True)
    status = models.CharField(verbose_name=_(u"Response_Code"), max_length=32,
                              blank=True)
    method = models.CharField(verbose_name=_(u"Request_Type"), max_length=32,
                              blank=True)
    req_body = models.TextField(verbose_name=_(u"Request_Parameter"), blank=True)
    time = models.DateTimeField(verbose_name=_(u'Operating_Time'), auto_now_add=True)

    class Meta:
        db_table = "user_audit_log"
        ordering = ('-time',)
        verbose_name = _(u'Audit log')

    def __unicode__(self):
        return self.username

    objects = Manager()


def get_hit_log_model(db_table):
    class CustomMetaClass(ModelBase):
        def __new__(cls, name, bases, attrs):
            model = super(CustomMetaClass, cls).__new__(cls, name, bases,
                                                        attrs)
            model._meta.db_table = db_table
            model._meta.index_together = (
                ('time',),
                ('user_id',),
            )
            model.managed = False
            return model

    class HitLogModel(models.Model, metaclass=CustomMetaClass):
        time = models.DateTimeField(verbose_name=_(u'Hit time'))
        rule_id = models.IntegerField(verbose_name=_(u'Rule ID'))
        user_id = models.IntegerField(verbose_name=_(u'Hit User'))
        kwargs = models.CharField(max_length=128, null=False, default='', verbose_name=_(u'Extended parameter'))
        req_body = models.CharField(max_length=512, null=False, default='', verbose_name=_(u'Request_Parameter'))
        control = models.CharField(max_length=16, null=False, default='', verbose_name=_(u'Projectmanagement'))
        custom = models.CharField(max_length=50, null=False, default='', verbose_name=_(u'策略Group解释'))
        group_name = models.CharField(max_length=256, null=False, default='',
                                      verbose_name=_(u'PolicyGroupNameCall'))
        group_uuid = models.CharField(max_length=36, null=False, default='',
                                      verbose_name=_(u'PolicyGroupUUID'))
        hit_number = models.PositiveSmallIntegerField(null=False, default=1, verbose_name=_(u'命中次序'))

        objects = Manager()

    return HitLogModel
