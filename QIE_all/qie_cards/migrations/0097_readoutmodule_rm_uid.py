# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-20 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0096_auto_20160919_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='readoutmodule',
            name='rm_uid',
            field=models.CharField(blank=True, default='', max_length=48),
        ),
    ]
