# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 16:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0083_auto_20170710_0920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='office',
            old_name='is_drcj',
            new_name='is_convention_manager',
        ),
    ]
