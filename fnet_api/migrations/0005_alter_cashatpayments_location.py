# Generated by Django 3.2.9 on 2021-11-21 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0004_rename_bank_cashatpayments_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashatpayments',
            name='location',
            field=models.CharField(max_length=50),
        ),
    ]