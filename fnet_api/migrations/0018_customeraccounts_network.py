# Generated by Django 3.2.9 on 2022-09-20 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0017_remove_reports_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeraccounts',
            name='network',
            field=models.CharField(blank=True, choices=[('Select Network', 'Select Network'), ('Mtn', 'Mtn'), ('Tigo', 'Tigo'), ('AirtelTigo', 'AirtelTigo'), ('Vodafone', 'Vodafone')], default='Select Network', max_length=20),
        ),
    ]
