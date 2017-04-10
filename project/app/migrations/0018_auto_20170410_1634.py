# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-08 18:57
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    Assignment = apps.get_model("app", "Assignment")
    assignments = Assignment.objects.all()

    for assignment in assignments:
        assignment.kind = 10
        assignment.save()


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20170410_1631'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
