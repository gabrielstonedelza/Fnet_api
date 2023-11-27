# Generated by Django 3.2.9 on 2023-11-26 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0064_alter_bankdeposit_user_local_district'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_phone', models.CharField(max_length=20)),
                ('customer_name', models.CharField(max_length=50)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('interest', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CashSupportBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_phone', models.CharField(max_length=20)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CashSupportRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_phone', models.CharField(max_length=20)),
                ('customer_name', models.CharField(max_length=50)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='customerrequestdeposit',
            name='request_option',
        ),
        migrations.AddField(
            model_name='customerrequestdeposit',
            name='bank',
            field=models.CharField(choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Adansi rural bank', 'Adansi rural bank'), ('Kwumawuman Bank', 'Kwumawuman Bank'), ('Pan Africa', 'Pan Africa'), ('SGSSB', 'SGSSB'), ('Atwima Rural Bank', 'Atwima Rural Bank'), ('Omnibsic Bank', 'Omnibsic Bank'), ('Omini bank', 'Omini bank'), ('Stanbic Bank', 'Stanbic Bank'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('Adehyeman Savings and loans', 'Adehyeman Savings and loans'), ('ARB Apex Bank Limited', 'ARB Apex Bank Limited'), ('Absa Bank', 'Absa Bank'), ('Agriculture Development bank', 'Agriculture Development bank'), ('Bank of Africa', 'Bank of Africa'), ('Bank of Ghana', 'Bank of Ghana'), ('Consolidated Bank Ghana', 'Consolidated Bank Ghana'), ('First Atlantic Bank', 'First Atlantic Bank'), ('First National Bank', 'First National Bank'), ('G-Money', 'G-Money'), ('GCB BanK LTD', 'GCB BanK LTD'), ('Ghana Pay', 'Ghana Pay'), ('GHL Bank Ltd', 'GHL Bank Ltd'), ('GT Bank', 'GT Bank'), ('National Investment Bank', 'National Investment Bank'), ('Opportunity International Savings And Loans', 'Opportunity International Savings And Loans'), ('Prudential Bank', 'Prudential Bank'), ('Republic Bank Ltd', 'Republic Bank Ltd'), ('Sahel Sahara Bank', 'Sahel Sahara Bank'), ('Sinapi Aba Savings and Loans', 'Sinapi Aba Savings and Loans'), ('Societe Generale Ghana Ltd', 'Societe Generale Ghana Ltd'), ('Standard Chartered', 'Standard Chartered'), ('universal Merchant Bank', 'universal Merchant Bank'), ('Zenith Bank', 'Zenith Bank'), ('Mtn', 'Mtn'), ('AirtelTigo', 'AirtelTigo'), ('Vodafone', 'Vodafone')], default='Cal Bank', max_length=100),
        ),
    ]