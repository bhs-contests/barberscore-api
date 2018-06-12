# Generated by Django 2.0.6 on 2018-06-12 14:07

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20180609_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, 'New'), (10, 'Built'), (20, 'Started'), (25, 'Reviewed'), (27, 'Verified'), (30, 'Finished')], default=0, help_text='DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.'),
        ),
    ]
