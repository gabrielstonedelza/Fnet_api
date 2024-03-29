# Generated by Django 3.2.9 on 2023-11-28 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0068_auto_20231127_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15, unique=True)),
                ('points', models.DecimalField(blank=True, decimal_places=2, default='0.0', max_digits=19)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
