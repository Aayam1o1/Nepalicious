# Generated by Django 4.2.5 on 2024-04-06 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_usersdetail_restaurant_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersdetail',
            name='hasBlockedUser',
            field=models.BooleanField(default=False),
        ),
    ]
