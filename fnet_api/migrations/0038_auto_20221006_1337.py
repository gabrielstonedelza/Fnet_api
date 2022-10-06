# Generated by Django 3.2.9 on 2022-10-06 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0037_addtoblocklist'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankdeposit',
            name='app_name',
            field=models.CharField(default='FNET', max_length=20),
        ),
        migrations.AddField(
            model_name='expensesrequest',
            name='app_name',
            field=models.CharField(default='FNET', max_length=20),
        ),
        migrations.AddField(
            model_name='mobilemoneydeposit',
            name='app_name',
            field=models.CharField(default='FNET', max_length=20),
        ),
        migrations.AddField(
            model_name='mobilemoneywithdraw',
            name='app_name',
            field=models.CharField(default='FNET', max_length=20),
        ),
        migrations.AddField(
            model_name='mypayments',
            name='app_name',
            field=models.CharField(default='FNET', max_length=20),
        ),
    ]
