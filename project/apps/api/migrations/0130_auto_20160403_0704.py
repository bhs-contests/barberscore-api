# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-03 14:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0129_remove_round_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='round',
            old_name='datetm',
            new_name='date',
        ),
    ]
