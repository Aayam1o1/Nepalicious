# Generated by Django 4.2.5 on 2024-04-04 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_likedislikerecipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='addrecipe',
            name='recipeProductTags',
            field=models.CharField(choices=[('spicesFood', 'SpicesFood'), ('pansPots', 'PansPots'), ('knifes', 'knifes'), ('electricAppliance', 'electricAppliance'), ('cleaningAppliance', 'cleaningAppliance')], default=0.0004940711462450593, max_length=100),
            preserve_default=False,
        ),
    ]
