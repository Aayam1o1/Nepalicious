# Generated by Django 4.2.5 on 2024-04-04 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_addrecipe_recipeproducttags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addrecipe',
            name='recipeProductTags',
            field=models.TextField(),
        ),
    ]
