# Generated by Django 3.2.9 on 2022-04-25 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0027_alter_customerwithdrawal_id_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerwithdrawal',
            name='id_number',
            field=models.CharField(default='0', max_length=20),
        ),
    ]