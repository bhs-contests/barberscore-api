# Generated by Django 2.1.7 on 2019-03-25 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_auto_20190324_2047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appearance',
            name='is_private',
        ),
    ]