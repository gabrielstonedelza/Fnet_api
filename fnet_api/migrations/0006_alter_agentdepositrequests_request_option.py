# Generated by Django 3.2.9 on 2021-12-07 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0005_auto_20211207_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentdepositrequests',
            name='request_option',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Mobile Money', 'Mobile Money'), ('Banks', 'Banks')], default='Cash', max_length=100),
        ),
    ]