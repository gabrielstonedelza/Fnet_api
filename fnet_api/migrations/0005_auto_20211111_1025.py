# Generated by Django 3.2.9 on 2021-11-11 10:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0004_alter_customer_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentdepositrequests',
            name='time_requested',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payments',
            name='time_created',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agentdepositrequests',
            name='date_requested',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
