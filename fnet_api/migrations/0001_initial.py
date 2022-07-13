# Generated by Django 3.2.9 on 2022-07-13 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teller_name', models.CharField(default='', max_length=100)),
                ('teller_phone', models.CharField(default='', max_length=100)),
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
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMobileMoneyAccountsStarted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physical', models.DecimalField(decimal_places=2, max_digits=19)),
                ('mtn_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('tigoairtel_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('vodafone_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('ecash_total', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMobileMoneyAccountsClosed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physical', models.DecimalField(decimal_places=2, max_digits=19)),
                ('mtn_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('tigoairtel_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('vodafone_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('ecash_total', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(blank=True, default='', max_length=100)),
                ('transaction_type', models.CharField(blank=True, default='', max_length=100)),
                ('notification_title', models.CharField(blank=True, max_length=200)),
                ('notification_message', models.TextField(blank=True)),
                ('read', models.CharField(choices=[('Read', 'Read'), ('Not Read', 'Not Read')], default='Not Read', max_length=20)),
                ('notification_trigger', models.CharField(blank=True, choices=[('Triggered', 'Triggered'), ('Not Triggered', 'Not Triggered')], default='Triggered', max_length=100)),
                ('customer', models.CharField(blank=True, default='', max_length=100)),
                ('customer_request_slug', models.CharField(blank=True, max_length=100)),
                ('cash_deposit_request_slug', models.CharField(blank=True, max_length=100)),
                ('bank_deposit_request_slug', models.CharField(blank=True, max_length=100)),
                ('payment_slug', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_receiving_notification', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode_of_payment1', models.CharField(blank=True, choices=[('Select mode of payment', 'Select mode of payment'), ('Bank Payment', 'Bank Payment'), ('Mtn', 'Mtn'), ('AirtelTigo', 'AirtelTigo'), ('Vodafone', 'Vodafone'), ('Momo pay', 'Momo pay'), ('Agent to Agent', 'Agent to Agent'), ('Cash left @', 'Cash left @'), ('Own Accounts', 'Own Accounts'), ('Company Accounts', 'Company Accounts')], max_length=30)),
                ('mode_of_payment2', models.CharField(blank=True, choices=[('Select mode of payment', 'Select mode of payment'), ('Bank Payment', 'Bank Payment'), ('Mtn', 'Mtn'), ('AirtelTigo', 'AirtelTigo'), ('Vodafone', 'Vodafone'), ('Momo pay', 'Momo pay'), ('Agent to Agent', 'Agent to Agent'), ('Cash left @', 'Cash left @'), ('Own Accounts', 'Own Accounts'), ('Company Accounts', 'Company Accounts')], max_length=30)),
                ('cash_at_location1', models.CharField(blank=True, choices=[('Please select cash at location', 'Please select cash at location'), ('Cash @ location', 'Cash @ location'), ('DVLA', 'DVLA'), ('HEAD OFFICE', 'HEAD OFFICE'), ('KEJETIA', 'KEJETIA'), ('ECOBANK', 'ECOBANK'), ('PAN AFRICA', 'PAN AFRICA')], default='', max_length=30)),
                ('cash_at_location2', models.CharField(blank=True, choices=[('Please select cash at location', 'Please select cash at location'), ('Cash @ location', 'Cash @ location'), ('DVLA', 'DVLA'), ('HEAD OFFICE', 'HEAD OFFICE'), ('KEJETIA', 'KEJETIA'), ('ECOBANK', 'ECOBANK'), ('PAN AFRICA', 'PAN AFRICA')], default='', max_length=30)),
                ('bank1', models.CharField(blank=True, choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB'), ('Atwima Rural Bank', 'Atwima Rural Bank'), ('Omnibsic Bank', 'Omnibsic Bank'), ('Stanbic Bank', 'Stanbic Bank'), ('Absa Bank', 'Absa Bank'), ('Universal Merchant Bank', 'Universal Merchant Bank'), ('Mtn', 'Mtn'), ('Vodafone', 'Vodafone'), ('Tigoairtel', 'Tigoairtel')], max_length=50)),
                ('bank2', models.CharField(blank=True, choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB'), ('Atwima Rural Bank', 'Atwima Rural Bank'), ('Omnibsic Bank', 'Omnibsic Bank'), ('Stanbic Bank', 'Stanbic Bank'), ('Absa Bank', 'Absa Bank'), ('Universal Merchant Bank', 'Universal Merchant Bank'), ('Mtn', 'Mtn'), ('Vodafone', 'Vodafone'), ('Tigoairtel', 'Tigoairtel')], max_length=50)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=19)),
                ('amount1', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('amount2', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('transaction_id1', models.CharField(blank=True, default='', max_length=30)),
                ('transaction_id2', models.CharField(blank=True, default='', max_length=30)),
                ('payment_action', models.CharField(choices=[('Select payment action', 'Select payment action'), ('Not Closed', 'Not Closed'), ('Close Payment', 'Close Payment')], default='Close Payment', max_length=50)),
                ('payment_status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MobileMoneyWithdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_phone', models.CharField(blank=True, max_length=30)),
                ('customer_name', models.CharField(blank=True, max_length=30)),
                ('network', models.CharField(blank=True, choices=[('Select Network', 'Select Network'), ('Mtn', 'Mtn'), ('AirtelTigo', 'AirtelTigo'), ('Vodafone', 'Vodafone')], default='Select Network', max_length=20)),
                ('type', models.CharField(blank=True, choices=[('MomoPay', 'MomoPay'), ('Cash Out', 'Cash Out'), ('Agent to Agent', 'Agent to Agent')], default='', max_length=30)),
                ('id_type', models.CharField(choices=[('Select Id Type', 'Select Id Type'), ('Ghana Card', 'Ghana Card'), ('Passport', 'Passport'), ('Drivers License', 'Drivers License'), ('Voters Id', 'Voters Id')], max_length=30)),
                ('id_number', models.CharField(max_length=20)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('charges', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('cash_out_commission', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('agent_commission', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('mtn_commission', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('date_of_withdrawal', models.DateField(auto_now_add=True)),
                ('time_of_withdrawal', models.TimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MobileMoneyDeposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_phone', models.CharField(blank=True, max_length=30)),
                ('customer_name', models.CharField(blank=True, max_length=30)),
                ('depositor_name', models.CharField(blank=True, default='', max_length=30)),
                ('depositor_number', models.CharField(blank=True, default='', max_length=30)),
                ('network', models.CharField(blank=True, choices=[('Select Network', 'Select Network'), ('Mtn', 'Mtn'), ('AirtelTigo', 'AirtelTigo'), ('Vodafone', 'Vodafone')], default='Select Network', max_length=20)),
                ('type', models.CharField(blank=True, choices=[('Regular', 'Regular'), ('Direct', 'Direct'), ('Agent to Agent', 'Agent to Agent')], max_length=20)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('charges', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('agent_commission', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('date_deposited', models.DateField(auto_now_add=True)),
                ('time_deposited', models.TimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_requesting', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExpensesRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('reason', models.TextField(default='')),
                ('request_status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('deposit_paid', models.CharField(blank=True, choices=[('Not Paid', 'Not Paid'), ('Paid', 'Paid')], default='Not Paid', max_length=20)),
                ('date_requested', models.DateField(auto_now_add=True)),
                ('time_requested', models.TimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_requesting_expense_cash', to=settings.AUTH_USER_MODEL)),
                ('guarantor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerWithdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=100)),
                ('bank', models.CharField(choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB'), ('Atwima Rural Bank', 'Atwima Rural Bank'), ('Omnibsic Bank', 'Omnibsic Bank'), ('Stanbic Bank', 'Stanbic Bank'), ('Absa Bank', 'Absa Bank'), ('Universal Merchant Bank', 'Universal Merchant Bank'), ('Mtn', 'Mtn'), ('Vodafone', 'Vodafone'), ('Tigoairtel', 'Tigoairtel')], default='GT Bank', max_length=100)),
                ('withdrawal_type', models.CharField(choices=[('Select Withdrawal Type', 'Select Withdrawal Type'), ('Cheque', 'Cheque'), ('Atm', 'Atm'), ('Phone', 'Phone')], default='Cheque', max_length=120)),
                ('id_type', models.CharField(choices=[('Select Id Type', 'Select Id Type'), ('Ghana Card', 'Ghana Card'), ('Passport', 'Passport'), ('Drivers License', 'Drivers License'), ('Voters Id', 'Voters Id')], max_length=20)),
                ('id_number', models.CharField(default='0', max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerRequestDeposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_phone', models.CharField(blank=True, max_length=20)),
                ('customer_name', models.CharField(blank=True, max_length=100)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('request_option', models.CharField(choices=[('Cash', 'Cash'), ('Mobile Money', 'Money Money'), ('Bank', 'Bank')], default='Physical Cash', max_length=100)),
                ('request_status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('date_requested', models.DateField(auto_now_add=True)),
                ('time_requested', models.TimeField(auto_now_add=True)),
                ('slug', models.SlugField(allow_unicode=True, default='', max_length=100)),
                ('agent', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=16)),
                ('account_name', models.CharField(max_length=100)),
                ('bank', models.CharField(choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB'), ('Atwima Rural Bank', 'Atwima Rural Bank'), ('Omnibsic Bank', 'Omnibsic Bank'), ('Stanbic Bank', 'Stanbic Bank'), ('Absa Bank', 'Absa Bank'), ('Universal Merchant Bank', 'Universal Merchant Bank'), ('Mtn', 'Mtn'), ('Vodafone', 'Vodafone'), ('Tigoairtel', 'Tigoairtel')], default='Access Bank', max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('digital_address', models.CharField(blank=True, max_length=25)),
                ('id_type', models.CharField(blank=True, choices=[('Select Id Type', 'Select Id Type'), ('Ghana Card', 'Ghana Card'), ('Passport', 'Passport'), ('Drivers License', 'Drivers License'), ('Voters Id', 'Voters Id')], default='Passport', max_length=50)),
                ('id_number', models.CharField(blank=True, default='', max_length=50)),
                ('phone', models.CharField(blank=True, max_length=15, unique=True)),
                ('date_of_birth', models.CharField(blank=True, max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CashAtPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19)),
                ('left_with', models.CharField(max_length=50)),
                ('left_with_phone', models.CharField(max_length=20)),
                ('reference_id', models.CharField(max_length=50)),
                ('date_paid', models.DateField(auto_now_add=True)),
                ('time_paid', models.TimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankDeposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(blank=True, max_length=20)),
                ('bank', models.CharField(blank=True, choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB'), ('Atwima Rural Bank', 'Atwima Rural Bank'), ('Omnibsic Bank', 'Omnibsic Bank'), ('Stanbic Bank', 'Stanbic Bank'), ('Absa Bank', 'Absa Bank'), ('Universal Merchant Bank', 'Universal Merchant Bank'), ('Mtn', 'Mtn'), ('Vodafone', 'Vodafone'), ('Tigoairtel', 'Tigoairtel')], default='', max_length=50)),
                ('account_number', models.TextField(blank=True, max_length=17)),
                ('account_name', models.CharField(blank=True, default='', max_length=100)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('depositor_name', models.CharField(blank=True, default='', max_length=50)),
                ('request_status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('deposit_paid', models.CharField(blank=True, choices=[('Not Paid', 'Not Paid'), ('Paid', 'Paid')], default='Not Paid', max_length=20)),
                ('date_requested', models.DateField(auto_now_add=True)),
                ('deposited_month', models.CharField(blank=True, default='', max_length=10)),
                ('deposited_year', models.CharField(blank=True, default='', max_length=10)),
                ('time_requested', models.TimeField(auto_now_add=True)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_requesting_bank', to=settings.AUTH_USER_MODEL)),
                ('guarantor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdminAccountsStartedWith',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physical_cash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('eCash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('date_started', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdminAccountsCompletedWith',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physical_cash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('eCash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('date_closed', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
