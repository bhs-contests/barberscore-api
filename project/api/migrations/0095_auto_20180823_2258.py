# Generated by Django 2.0.8 on 2018-08-24 05:58

import api.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0094_auto_20180822_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=api.fields.LowerEmailField(help_text='\n            The contact email of the resource.', max_length=254, unique=True),
        ),
    ]