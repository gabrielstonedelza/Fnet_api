# Generated by Django 3.2.9 on 2022-10-07 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0039_auto_20221006_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankdeposit',
            name='app_name',
        ),
        migrations.RemoveField(
            model_name='expensesrequest',
            name='app_name',
        ),
        migrations.RemoveField(
            model_name='mobilemoneydeposit',
            name='app_name',
        ),
        migrations.RemoveField(
            model_name='mobilemoneywithdraw',
            name='app_name',
        ),
        migrations.RemoveField(
            model_name='mypayments',
            name='app_name',
        ),
    ]
