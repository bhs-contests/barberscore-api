# Generated by Django 2.0.2 on 2018-02-06 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_auto_20180206_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='mos',
            field=models.IntegerField(blank=True, help_text='Estimated Men-on-Stage', null=True),
        ),
    ]