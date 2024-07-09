# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 14:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0039_auto_20160614_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='date_recieved',
        ),
        migrations.AddField(
            model_name='location',
            name='date_received',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 15, 14, 16, 53, 121255, tzinfo=utc), verbose_name='date received'),
        ),
        migrations.AlterField(
            model_name='location',
            name='geo_loc',
            field=models.CharField(default='', max_length=30, verbose_name='Location'),
        ),
    ]
