# Generated by Django 3.2.9 on 2023-04-13 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0048_auto_20230413_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobilemoneydeposit',
            name='reference',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='mobilemoneywithdraw',
            name='reference',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]