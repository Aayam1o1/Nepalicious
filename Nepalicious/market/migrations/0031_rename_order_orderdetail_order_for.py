# Generated by Django 4.2.5 on 2024-04-01 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0030_alter_orderdetail_seller'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='order',
            new_name='order_for',
        ),
    ]