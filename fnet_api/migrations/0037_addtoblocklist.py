# Generated by Django 3.2.9 on 2022-10-06 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fnet_api', '0036_auto_20221001_0653'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddToBlockList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_blocked', models.DateTimeField(auto_now_add=True)),
                ('administrator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_being_blocked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]