# Generated by Django 4.2.5 on 2024-03-27 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_alter_restaurantimage_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurantimage',
            old_name='addRecipe',
            new_name='addRestaurant',
        ),
    ]