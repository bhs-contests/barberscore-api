# Generated by Django 2.1.8 on 2019-06-04 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmanager', '0012_auto_20190604_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignments', to='bhs.Person'),
        ),
    ]