# Generated by Django 3.2.9 on 2021-11-05 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0003_alter_agentdepositrequests_guarantor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerwithdrawal',
            name='customer',
            field=models.CharField(max_length=100),
        ),
    ]