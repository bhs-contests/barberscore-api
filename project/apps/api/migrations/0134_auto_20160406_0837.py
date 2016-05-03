# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-06 15:37
from __future__ import unicode_literals

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0133_auto_20160405_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, b'New'), (20, b'Started'), (30, b'Finished'), (40, b'Drafted'), (45, b'Published'), (50, b'Final')], default=0),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, b'New'), (10, b'Eligible'), (20, b'Ineligible'), (30, b'Did Not Qualify'), (50, b'Qualified'), (60, b'Ranked'), (90, b'Final')], default=0),
        ),
    ]
