# Generated by Django 4.2.3 on 2023-08-17 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athletesQuotesApp', '0003_alter_athletequote_inspiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athletequote',
            name='inspiration',
            field=models.CharField(max_length=350),
        ),
    ]
