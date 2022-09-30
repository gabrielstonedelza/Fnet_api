# Generated by Django 3.2.9 on 2022-09-30 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fnet_api', '0031_auto_20220929_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='referral',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.CharField(blank=True, choices=[('Was Referred', 'Was Referred'), ('User Registration', 'User Registration')], default='User Registration', max_length=100),
        ),
        migrations.CreateModel(
            name='ReferCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('digital_address', models.CharField(blank=True, max_length=25)),
                ('id_type', models.CharField(blank=True, choices=[('Select Id Type', 'Select Id Type'), ('Ghana Card', 'Ghana Card'), ('Passport', 'Passport'), ('Drivers License', 'Drivers License'), ('Voters Id', 'Voters Id')], default='Passport', max_length=50)),
                ('id_number', models.CharField(blank=True, default='', max_length=50)),
                ('phone', models.CharField(blank=True, max_length=15, unique=True)),
                ('referral', models.CharField(blank=True, default='', max_length=200)),
                ('status', models.CharField(blank=True, choices=[('Was Referred', 'Was Referred'), ('User Registration', 'User Registration')], default='Was Referred', max_length=100)),
                ('date_of_birth', models.CharField(blank=True, max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('administrator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='referral_administrator', to=settings.AUTH_USER_MODEL)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]