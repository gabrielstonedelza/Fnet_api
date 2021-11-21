# Generated by Django 3.2.9 on 2021-11-21 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminAccountsCompletedWith',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physical_cash', models.IntegerField()),
                ('eCash', models.IntegerField()),
                ('date_closed', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdminAccountsStartedWith',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physical_cash', models.IntegerField(blank=True)),
                ('eCash', models.IntegerField(blank=True)),
                ('date_started', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AgentDepositRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(blank=True, max_length=30)),
                ('bank', models.CharField(blank=True, choices=[('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB')], max_length=50)),
                ('amount', models.CharField(blank=True, max_length=500)),
                ('request_option', models.CharField(choices=[('Physical Cash', 'Physical Cash'), ('Mtn Ecash', 'Mtn Ecash'), ('Vodafone Ecash', 'Vodafone Ecash'), ('AirtelTigo Ecash', 'AirtelTigo Ecash'), ('Ecobank Ecash', 'Ecobank Ecash'), ('Calbank Ecash', 'Calbank Ecash'), ('Fidelity Ecash', 'Fidelity Ecash')], default='Physical Cash', max_length=100)),
                ('request_status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('date_requested', models.DateField(auto_now_add=True)),
                ('time_requested', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BankPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(choices=[('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB')], max_length=50)),
                ('amount', models.CharField(max_length=50)),
                ('left_with', models.CharField(max_length=50)),
                ('left_with_phone', models.CharField(max_length=20)),
                ('reference_id', models.CharField(max_length=50)),
                ('date_paid', models.DateField(auto_now_add=True)),
                ('time_paid', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('location', models.CharField(max_length=100)),
                ('digital_address', models.CharField(max_length=15)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('date_of_birth', models.CharField(max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=16)),
                ('bank', models.CharField(choices=[('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB')], default='Access Bank', max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerWithdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=100)),
                ('bank', models.CharField(choices=[('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB')], default='GT Bank', max_length=100)),
                ('amount', models.CharField(max_length=500)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode_of_payment', models.CharField(blank=True, choices=[('Select mode of payment', 'Select mode of payment'), ('Bank Payment', 'Bank Payment'), ('Mtn', 'Mtn'), ('AirtelTigo', 'AirtelTigo'), ('Vodafone', 'Vodafone'), ('Momo pay', 'Momo pay'), ('Agent to Agent', 'Agent to Agent'), ('Cash left @', 'Cash left @')], max_length=30)),
                ('cash_at_location', models.CharField(blank=True, choices=[('Cash @ location', 'Cash @ location'), ('DVLA', 'DVLA'), ('HEAD OFFICE', 'HEAD OFFICE'), ('KEJETIA', 'KEJETIA'), ('ECOBANK', 'ECOBANK'), ('PAN AFRICA', 'PAN AFRICA')], max_length=30)),
                ('bank', models.CharField(blank=True, choices=[('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB')], max_length=50)),
                ('amount', models.CharField(blank=True, max_length=500)),
                ('reference', models.CharField(blank=True, max_length=30)),
                ('payment_action', models.CharField(choices=[('Select payment action', 'Select payment action'), ('Close Payment', 'Close Payment')], default='Not Closed', max_length=50)),
                ('payment_status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TwilioApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_sid', models.CharField(max_length=200)),
                ('twi_auth', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WithdrawReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=50)),
                ('customer_phone', models.CharField(max_length=20)),
                ('reference_id', models.CharField(max_length=50)),
                ('date_withdrew', models.DateField(auto_now_add=True)),
                ('time_withdrew', models.TimeField(auto_now_add=True)),
            ],
        ),
    ]
