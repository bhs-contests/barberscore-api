# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 06:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_session_num_rounds'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='office',
            name='long_name',
        ),
    ]