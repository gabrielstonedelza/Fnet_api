# Generated by Django 3.2.9 on 2022-01-28 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0012_alter_notifications_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='customer',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
