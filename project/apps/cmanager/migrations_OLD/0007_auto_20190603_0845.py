# Generated by Django 2.1.8 on 2019-06-03 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmanager', '0006_auto_20190526_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(10, 'Male'), (20, 'Female'), (30, 'Mixed')], help_text='\n            The gender to which the award is restricted.  If unselected, this award is open to all combinations.\n        ', null=True),
        ),
    ]