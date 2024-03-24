# Generated by Django 4.2.5 on 2024-03-24 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0003_remove_search_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='user',
            field=models.ForeignKey(default=6.175889328063241e-05, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]