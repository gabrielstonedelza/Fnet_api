# Generated by Django 3.2.9 on 2021-11-11 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0009_auto_20211111_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='deposit_request',
            field=models.ForeignKey(default='20000', on_delete=django.db.models.deletion.CASCADE, related_name='deposit_requests', to='fnet_api.agentdepositrequests'),
        ),
    ]
