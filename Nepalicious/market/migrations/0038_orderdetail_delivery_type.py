# Generated by Django 4.2.5 on 2024-04-16 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0037_addproducts_isdeleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='delivery_type',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]