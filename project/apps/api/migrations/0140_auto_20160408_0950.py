# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-08 16:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0139_remove_session_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='datet',
            new_name='date',
        ),
    ]
