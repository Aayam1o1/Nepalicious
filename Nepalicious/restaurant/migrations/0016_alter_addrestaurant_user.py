# Generated by Django 4.2.5 on 2024-04-10 05:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0015_rename_product_restaurantfeedback_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addrestaurant',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
