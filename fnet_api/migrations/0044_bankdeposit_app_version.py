# Generated by Django 3.2.9 on 2023-03-30 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0043_auto_20230323_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankdeposit',
            name='app_version',
            field=models.CharField(default='1', max_length=10),
        ),
    ]
