# Generated by Django 2.1.1 on 2018-10-01 16:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0119_round_legacy_sa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(-10, 'Inactive'), (0, 'New'), (10, 'Active')], default=0)),
                ('num', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('legacy_name', models.CharField(blank=True, max_length=255, null=True)),
                ('contest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outcomes', to='api.Contest')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outcomes', to='api.Round')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]