# Generated by Django 3.2.9 on 2022-01-22 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0004_alter_mypayments_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerrequestdeposit',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19),
        ),
    ]
