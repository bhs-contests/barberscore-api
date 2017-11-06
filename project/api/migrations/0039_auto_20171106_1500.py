# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 23:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_grantor_convention'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grantor',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grantors', to='api.Session'),
        ),
    ]
