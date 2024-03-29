# Generated by Django 3.2.9 on 2023-03-23 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fnet_api', '0042_auto_20230308_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankdeposit',
            name='request_status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='cashrequest',
            name='request_status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='customerrequestdeposit',
            name='request_status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='expensesrequest',
            name='request_status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='mycashpayments',
            name='payment_status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='mypayments',
            name='payment_status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
        migrations.CreateModel(
            name='WithdrawalReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=19)),
                ('customer_name', models.CharField(max_length=255)),
                ('reference', models.CharField(max_length=255)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
