# Generated by Django 2.1.8 on 2019-06-04 18:09

import apps.cmanager.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmanager', '0011_auto_20190604_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='kinds',
            field=apps.cmanager.fields.DivisionsField(base_field=models.IntegerField(choices=[(32, 'Chorus'), (41, 'Quartet'), (42, 'Mixed'), (43, 'Senior'), (44, 'Youth'), (45, 'Unknown'), (46, 'VLQ')]), blank=True, default=list, help_text='The session kind(s) created at build time.', size=None),
        ),
        migrations.AlterField(
            model_name='convention',
            name='season',
            field=models.IntegerField(choices=[(3, 'Fall'), (4, 'Spring')]),
        ),
    ]
