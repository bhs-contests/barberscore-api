# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 21:48
from __future__ import unicode_literals

import api.fields
import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0059_auto_20170625_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='scoresheet',
        ),
        migrations.AlterField(
            model_name='session',
            name='ss',
            field=models.FileField(blank=True, null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to=api.fields.PathAndRename(prefix='scoresheet')),
        ),
    ]
