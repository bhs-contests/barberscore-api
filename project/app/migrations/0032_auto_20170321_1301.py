# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20170321_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='panel',
            field=models.IntegerField(blank=True, choices=[(1, 'Single'), (2, 'Double'), (3, 'Triple'), (4, 'Quadruple'), (5, 'Quintiple')], null=True),
        ),
    ]
