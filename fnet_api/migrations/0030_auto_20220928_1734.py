# Generated by Django 3.2.9 on 2022-09-28 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0029_auto_20220928_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='points',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.0', max_digits=19),
        ),
        migrations.CreateModel(
            name='AddToCustomerRedeemPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_phone', models.CharField(blank=True, max_length=20)),
                ('points', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('redeem_option', models.CharField(choices=[('Cash', 'Cash'), ('Mobile Credit', 'Mobile Credit'), ('Melcom Coupon', 'Melcom Coupon')], default='Mobile Credit', max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fnet_api.customer')),
            ],
        ),
        migrations.CreateModel(
            name='AddToCustomerPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_phone', models.CharField(blank=True, max_length=20)),
                ('points', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fnet_api.customer')),
            ],
        ),
    ]
