# Generated by Django 3.2.9 on 2023-04-13 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0046_alter_bankdeposit_app_version'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobilemoneywithdraw',
            name='id_number',
        ),
        migrations.RemoveField(
            model_name='mobilemoneywithdraw',
            name='id_type',
        ),
        migrations.AlterField(
            model_name='mobilemoneywithdraw',
            name='type',
            field=models.CharField(blank=True, choices=[('Cash Out', 'Cash Out'), ('Agent to Agent', 'Agent to Agent')], default='', max_length=30),
        ),
    ]
