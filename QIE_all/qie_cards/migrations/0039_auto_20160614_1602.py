# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0038_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qiecard',
            name='geo_loc',
        ),
        migrations.AddField(
            model_name='location',
            name='geo_loc',
            field=models.CharField(default='', max_length=30),
        ),
    ]
