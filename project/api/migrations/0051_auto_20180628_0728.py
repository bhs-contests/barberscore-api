# Generated by Django 2.0.6 on 2018-06-28 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_auto_20180628_0634'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appearance',
            options={'ordering': ['-round__kind', 'num']},
        ),
    ]