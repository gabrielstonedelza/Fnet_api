# Generated by Django 3.2.9 on 2022-09-26 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0027_fnetprivateusermessage_issender'),
    ]

    operations = [
        migrations.AddField(
            model_name='fnetprivateusermessage',
            name='isReceiver',
            field=models.BooleanField(default=False),
        ),
    ]
