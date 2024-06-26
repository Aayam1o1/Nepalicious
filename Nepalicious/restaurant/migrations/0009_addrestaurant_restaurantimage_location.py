# Generated by Django 4.2.5 on 2024-03-26 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0008_search_latitude_search_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='addRestaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurantDescription', models.TextField()),
                ('restaurantType', models.CharField(choices=[('Thakali', 'Thakali'), ('Newari', 'Newari'), ('Sherpa', 'Sherpa'), ('Tamang', 'Tamang'), ('Nepali ', 'Nepali')], max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='restaurantImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/recipe/restaurantImage/')),
                ('addRecipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='restaurant.addrestaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.addrestaurant')),
            ],
        ),
    ]
