# Generated by Django 2.1.7 on 2019-03-29 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0099_auto_20190329_1056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appearance',
            name='competitor',
        ),
        migrations.AlterField(
            model_name='appearance',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appearances', to='api.Group'),
        ),
    ]
