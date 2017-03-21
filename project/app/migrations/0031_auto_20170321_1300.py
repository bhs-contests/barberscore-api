# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_auto_20170320_0436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='convention',
        ),
        migrations.RemoveField(
            model_name='host',
            name='entity',
        ),
        migrations.RemoveField(
            model_name='host',
            name='session',
        ),
        migrations.RemoveField(
            model_name='convention',
            name='participants',
        ),
        migrations.RemoveField(
            model_name='session',
            name='participants',
        ),
        migrations.AlterField(
            model_name='convention',
            name='panel',
            field=models.IntegerField(blank=True, choices=[(0, 'Unknown'), (1, 'Single'), (2, 'Double'), (3, 'Triple'), (4, 'Quadruple'), (5, 'Quintiple')], default=0, null=True),
        ),
        migrations.DeleteModel(
            name='Host',
        ),
    ]
