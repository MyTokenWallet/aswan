# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLogModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64, verbose_name=_('username'), blank=True)),
                ('email', models.CharField(max_length=128, verbose_name=_('email'), blank=True)),
                ('path', models.CharField(max_length=128, verbose_name=_('path'), blank=True)),
                ('status', models.CharField(max_length=32, verbose_name=_('status'), blank=True)),
                ('method', models.CharField(max_length=32, verbose_name=_('method'), blank=True)),
                ('req_body', models.TextField(verbose_name=_('req_body'), blank=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name=_('time'))),
            ],
            options={
                'ordering': ('-time',),
                'db_table': 'user_audit_log',
                'verbose_name': _('Audit_log'),
            },
        ),
    ]
