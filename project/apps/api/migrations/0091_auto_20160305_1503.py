# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-05 23:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0090_auto_20160305_1458'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='arranger',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='arranger',
            name='chart',
        ),
        migrations.RemoveField(
            model_name='arranger',
            name='person',
        ),
        migrations.DeleteModel(
            name='Arranger',
        ),
    ]
