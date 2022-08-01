# Generated by Django 3.2.9 on 2022-08-01 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0009_auto_20220801_1134'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPaymentAtBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=100)),
                ('agent_name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('d_200', models.IntegerField(blank=True, default=0)),
                ('d_100', models.IntegerField(blank=True, default=0)),
                ('d_50', models.IntegerField(blank=True, default=0)),
                ('d_20', models.IntegerField(blank=True, default=0)),
                ('d_10', models.IntegerField(blank=True, default=0)),
                ('d_5', models.IntegerField(blank=True, default=0)),
                ('d_2', models.IntegerField(blank=True, default=0)),
                ('d_1', models.IntegerField(blank=True, default=0)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('time_added', models.TimeField(auto_now_add=True)),
            ],
        ),
    ]
