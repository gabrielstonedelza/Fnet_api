# Generated by Django 3.2.9 on 2021-11-05 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0006_remove_customer_bank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_of_birth',
            field=models.CharField(max_length=15),
        ),
    ]