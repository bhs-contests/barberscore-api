# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-03 18:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0070_chart_tune'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='chart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='songs', to='api.Chart'),
        ),
    ]
