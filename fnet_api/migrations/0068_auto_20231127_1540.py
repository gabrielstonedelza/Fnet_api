# Generated by Django 3.2.9 on 2023-11-27 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0067_commercials_default_youtube_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashsupport',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.0', max_digits=19),
        ),
        migrations.AlterField(
            model_name='cashsupport',
            name='interest',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.0', max_digits=19),
        ),
    ]