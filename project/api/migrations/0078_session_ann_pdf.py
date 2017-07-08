# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-08 20:20
from __future__ import unicode_literals

import api.fields
import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0077_appearance_var_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='ann_pdf',
            field=models.FileField(blank=True, max_length=255, null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to=api.fields.PathAndRename(prefix='announcements')),
        ),
    ]
