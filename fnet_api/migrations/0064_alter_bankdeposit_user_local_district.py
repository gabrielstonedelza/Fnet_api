# Generated by Django 3.2.9 on 2023-08-24 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0063_bankdeposit_user_local_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankdeposit',
            name='user_local_district',
            field=models.CharField(max_length=255),
        ),
    ]
