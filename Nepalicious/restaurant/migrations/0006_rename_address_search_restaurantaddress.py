# Generated by Django 4.2.5 on 2024-03-24 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_remove_search_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='search',
            old_name='address',
            new_name='restaurantaddress',
        ),
    ]
