# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-06 19:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0056_auto_20160630_1506'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qiecard',
            old_name='major_ver',
            new_name='bridge_major_ver',
        ),
        migrations.RenameField(
            model_name='qiecard',
            old_name='minor_ver',
            new_name='bridge_minor_ver',
        ),
        migrations.RenameField(
            model_name='qiecard',
            old_name='other_ver',
            new_name='bridge_other_ver',
        ),
    ]
