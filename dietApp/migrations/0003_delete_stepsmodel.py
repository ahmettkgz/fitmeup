# Generated by Django 4.2.3 on 2023-08-17 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dietApp', '0002_category_recipe_stepsmodel_delete_recipepost'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StepsModel',
        ),
    ]
