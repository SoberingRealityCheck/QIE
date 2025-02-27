# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-29 23:25
from __future__ import unicode_literals

from django.db import migrations, models
import qie_cards.models


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0073_auto_20160729_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qieshuntparams',
            name='cal_range',
        ),
        migrations.RemoveField(
            model_name='qieshuntparams',
            name='cap_ID',
        ),
        migrations.RemoveField(
            model_name='qieshuntparams',
            name='date',
        ),
        migrations.RemoveField(
            model_name='qieshuntparams',
            name='offset',
        ),
        migrations.RemoveField(
            model_name='qieshuntparams',
            name='qie',
        ),
        migrations.RemoveField(
            model_name='qieshuntparams',
            name='serial',
        ),
        migrations.RemoveField(
            model_name='qieshuntparams',
            name='shunt',
        ),
        migrations.RemoveField(
            model_name='qieshuntparams',
            name='slope',
        ),
        migrations.AddField(
            model_name='qieshuntparams',
            name='plots',
            field=models.FileField(default='default.png', upload_to=qie_cards.models.logs_location),
        ),
    ]
