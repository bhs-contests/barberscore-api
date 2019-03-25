# Generated by Django 2.1.7 on 2019-03-14 22:53

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_auto_20190314_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(-10, 'Inactive'), (0, 'New'), (10, 'Active')], default=10, help_text='DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.'),
        ),
    ]