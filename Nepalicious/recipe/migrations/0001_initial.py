# Generated by Django 4.2.5 on 2024-03-06 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='addRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipeName', models.CharField(max_length=100)),
                ('recipeDescription', models.TextField()),
                ('cuisineType', models.CharField(choices=[('Thakali', 'Thakali'), ('Newari', 'PansPots'), ('Sherpa', 'knifes'), ('Tamang', 'electricAppliance'), ('Nepali ', 'cleaningAppliance')], max_length=100)),
                ('recipeIngredient', models.TextField()),
                ('recipeSteps', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='recipeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/recipe/recipeImage/')),
                ('addRecipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='recipe.addrecipe')),
            ],
        ),
    ]
