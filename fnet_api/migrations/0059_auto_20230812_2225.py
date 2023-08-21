# Generated by Django 3.2.9 on 2023-08-12 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0058_auto_20230725_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypayments',
            name='bank1',
            field=models.CharField(blank=True, choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Adansi rural bank', 'Adansi rural bank'), ('Kwumawuman Bank', 'Kwumawuman Bank'), ('Pan Africa', 'Pan Africa'), ('SGSSB', 'SGSSB'), ('Atwima Rural Bank', 'Atwima Rural Bank'), ('Omnibsic Bank', 'Omnibsic Bank'), ('Omini bank', 'Omini bank'), ('Stanbic Bank', 'Stanbic Bank'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('Adehyeman Savings and loans', 'Adehyeman Savings and loans'), ('ARB Apex Bank Limited', 'ARB Apex Bank Limited'), ('Absa Bank', 'Absa Bank'), ('Agriculture Development bank', 'Agriculture Development bank'), ('Bank of Africa', 'Bank of Africa'), ('Bank of Ghana', 'Bank of Ghana'), ('Consolidated Bank Ghana', 'Consolidated Bank Ghana'), ('First Atlantic Bank', 'First Atlantic Bank'), ('First National Bank', 'First National Bank'), ('G-Money', 'G-Money'), ('GCB BanK LTD', 'GCB BanK LTD'), ('Ghana Pay', 'Ghana Pay'), ('GHL Bank Ltd', 'GHL Bank Ltd'), ('GT Bank', 'GT Bank'), ('National Investment Bank', 'National Investment Bank'), ('Opportunity International Savings And Loans', 'Opportunity International Savings And Loans'), ('Prudential Bank', 'Prudential Bank'), ('Republic Bank Ltd', 'Republic Bank Ltd'), ('Sahel Sahara Bank', 'Sahel Sahara Bank'), ('Sinapi Aba Savings and Loans', 'Sinapi Aba Savings and Loans'), ('Societe Generale Ghana Ltd', 'Societe Generale Ghana Ltd'), ('Standard Chartered', 'Standard Chartered'), ('universal Merchant Bank', 'universal Merchant Bank'), ('Zenith Bank', 'Zenith Bank'), ('Mtn', 'Mtn'), ('AirtelTigo', 'AirtelTigo'), ('Vodafone', 'Vodafone')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='mypayments',
            name='mode_of_payment2',
            field=models.CharField(blank=True, choices=[('Select mode of payment', 'Select mode of payment'), ('Bank Payment', 'Bank Payment'), ('Mtn', 'Mtn'), ('AirtelTigo', 'AirtelTigo'), ('Vodafone', 'Vodafone'), ('Momo pay', 'Momo pay'), ('Agent to Agent', 'Agent to Agent'), ('Cash left @', 'Cash left @'), ('Own Accounts', 'Own Accounts'), ('Company Accounts', 'Company Accounts')], default='', max_length=30),
        ),
    ]