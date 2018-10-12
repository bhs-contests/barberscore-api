# Generated by Django 2.1.2 on 2018-10-08 13:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0130_complete_season'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('row', models.IntegerField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('district', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('season', models.IntegerField(blank=True, choices=[(1, 'Summer'), (2, 'Midwinter'), (3, 'Fall'), (4, 'Spring'), (9, 'Video')], null=True)),
                ('session_kind', models.IntegerField(blank=True, choices=[(32, 'Chorus'), (41, 'Quartet'), (42, 'Mixed')], null=True)),
                ('round_kind', models.IntegerField(blank=True, choices=[(1, 'Finals'), (2, 'Semi-Finals'), (3, 'Quarter-Finals')], null=True)),
                ('legacy_group', models.CharField(blank=True, max_length=255)),
                ('draw', models.IntegerField(blank=True, null=True)),
                ('num', models.IntegerField(blank=True, null=True)),
                ('legacy_chart', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]