# Generated by Django 3.2.9 on 2022-09-30 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0033_remove_refercustomer_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refercustomer',
            name='name',
            field=models.CharField(blank=True, max_length=150, unique=True),
        ),
    ]