# Generated by Django 3.2.9 on 2021-12-07 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0009_agentdepositrequests_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentdepositrequests',
            name='account_number',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]