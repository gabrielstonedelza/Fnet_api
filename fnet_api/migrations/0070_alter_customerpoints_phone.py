# Generated by Django 3.2.9 on 2023-11-28 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0069_customerpoints'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerpoints',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]