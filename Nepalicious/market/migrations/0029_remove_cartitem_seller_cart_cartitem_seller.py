# Generated by Django 4.2.5 on 2024-03-31 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0028_remove_cartitem_seller_cartitem_seller_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='seller_cart',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='seller',
            field=models.ForeignKey(default=0.00510540184453228, on_delete=django.db.models.deletion.CASCADE, related_name='seller_cart_items', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]