# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 23:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20170410_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='category',
            field=models.IntegerField(blank=True, choices=[(5, 'DRCJ'), (10, 'CA'), (20, 'ACA'), (30, 'Music'), (40, 'Performance'), (50, 'Singing')], null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='kind',
            field=models.IntegerField(choices=[(10, 'Official'), (20, 'Practice'), (30, 'Composite')]),
        ),
    ]
