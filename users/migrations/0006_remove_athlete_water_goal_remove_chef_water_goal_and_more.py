# Generated by Django 4.2.3 on 2023-08-17 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_athlete_water_goal_chef_water_goal_other_water_goal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='athlete',
            name='water_goal',
        ),
        migrations.RemoveField(
            model_name='chef',
            name='water_goal',
        ),
        migrations.RemoveField(
            model_name='other',
            name='water_goal',
        ),
    ]
