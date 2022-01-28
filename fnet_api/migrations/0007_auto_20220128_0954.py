# Generated by Django 3.2.9 on 2022-01-28 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fnet_api', '0006_alter_mypayments_agent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_title', models.CharField(max_length=200)),
                ('notification_message', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('customer', models.CharField(blank='', default='', max_length=100)),
                ('customer_request_slug', models.CharField(blank=True, max_length=100)),
                ('cash_deposit_request_slug', models.CharField(blank=True, max_length=100)),
                ('bank_deposit_request_slug', models.CharField(blank=True, max_length=100)),
                ('payment_slug', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User_receiving_notification', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userflags',
            name='user',
        ),
        migrations.AddField(
            model_name='bankdeposit',
            name='slug',
            field=models.SlugField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='cashdeposit',
            name='slug',
            field=models.SlugField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='customerrequestdeposit',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='mypayments',
            name='slug',
            field=models.SlugField(default='', max_length=100),
        ),
        migrations.DeleteModel(
            name='MomoRequest',
        ),
        migrations.DeleteModel(
            name='UserFlags',
        ),
    ]
