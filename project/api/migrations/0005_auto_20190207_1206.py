# Generated by Django 2.1.5 on 2019-02-07 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190207_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='legacy_chart',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]