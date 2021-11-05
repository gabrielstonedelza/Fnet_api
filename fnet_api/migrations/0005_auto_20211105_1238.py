# Generated by Django 3.2.9 on 2021-11-05 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0004_alter_customerwithdrawal_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwilioApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_sid', models.CharField(max_length=200)),
                ('twi_auth', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='payments',
            name='cash_at_location',
            field=models.CharField(blank=True, choices=[('Cash @ location', 'Cash @ location'), ('DVLA', 'DVLA'), ('HEAD OFFICE', 'HEAD OFFICE'), ('KEJETIA', 'KEJETIA'), ('ECOBANK', 'ECOBANK'), ('PAN AFRICA', 'PAN AFRICA')], max_length=30),
        ),
        migrations.AlterField(
            model_name='payments',
            name='mode_of_payment',
            field=models.CharField(blank=True, choices=[('Select mode of payment', 'Select mode of payment'), ('Bank Payment', 'Bank Payment'), ('Momo Payment', 'Momo Payment'), ('Momo pay Payment', 'Momo pay Payment'), ('Agent to Agent', 'Agent to Agent'), ('Bank Payment', 'Bank Payment'), ('Cash left @', 'Cash left @')], max_length=30),
        ),
    ]