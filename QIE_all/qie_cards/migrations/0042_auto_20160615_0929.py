# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 14:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0041_auto_20160615_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='date_received',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 15, 14, 29, 41, 94239, tzinfo=utc), verbose_name='date received'),
        ),
    ]
