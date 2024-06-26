# Generated by Django 4.2.5 on 2024-04-05 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0035_alter_orderdetail_is_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='is_completed',
            field=models.CharField(choices=[('Delivery Canceled', 'Delivery Canceled'), ('Delivery Completed', 'Delivery Completed'), ('Delivery Pending', 'Delivery Pending')], default='Delivery Pending', max_length=120),
        ),
    ]
