# Generated by Django 4.2.3 on 2023-08-16 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaryApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterentry',
            name='glasses',
            field=models.IntegerField(default=0, help_text='Enter the number of glasses of water'),
        ),
    ]
