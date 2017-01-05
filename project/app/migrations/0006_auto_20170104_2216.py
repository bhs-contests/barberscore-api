# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-05 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20170104_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='name',
            field=models.CharField(help_text=b'Award Name.', max_length=255),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(help_text=b'\n            Chapter Name.', max_length=255),
        ),
        migrations.AlterField(
            model_name='convention',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
