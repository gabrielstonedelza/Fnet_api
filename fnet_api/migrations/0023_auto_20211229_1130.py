# Generated by Django 3.2.9 on 2021-12-29 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0022_auto_20211229_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankdeposit',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='cashatpayments',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='cashdeposit',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='customerrequestdeposit',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='customerwithdrawal',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='mobilemoneydeposit',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='mobilemoneywithdraw',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='payments',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='withdrawreference',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
    ]
