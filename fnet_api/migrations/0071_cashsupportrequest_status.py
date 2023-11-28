# Generated by Django 3.2.9 on 2023-11-28 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0070_alter_customerpoints_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashsupportrequest',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=100),
        ),
    ]
