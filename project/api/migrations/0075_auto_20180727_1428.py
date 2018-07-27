# Generated by Django 2.0.7 on 2018-07-27 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0074_award_is_later'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='level',
            field=models.IntegerField(choices=[(10, 'Championship'), (30, 'Qualifier'), (40, 'Award'), (50, 'Deferred'), (60, 'Manual')]),
        ),
    ]
