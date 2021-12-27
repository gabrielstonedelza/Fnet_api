# Generated by Django 3.2.9 on 2021-12-27 20:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fnet_api', '0017_alter_agentdepositrequests_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankDeposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(blank=True, max_length=20)),
                ('bank', models.CharField(blank=True, choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB')], default='', max_length=50)),
                ('account_number', models.TextField(blank=True, max_length=17)),
                ('account_name', models.CharField(blank=True, default='', max_length=100)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('request_status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('date_requested', models.DateField(auto_now_add=True)),
                ('time_requested', models.TimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_requesting_bank', to=settings.AUTH_USER_MODEL)),
                ('guarantor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CashDeposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(blank=True, max_length=20)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('request_status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('date_requested', models.DateField(auto_now_add=True)),
                ('time_requested', models.TimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_requesting_cash', to=settings.AUTH_USER_MODEL)),
                ('guarantor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MobileMoneyDeposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(blank=True, max_length=30)),
                ('network', models.CharField(blank=True, choices=[('Select Network', 'Select Network'), ('Mtn', 'Mtn'), ('AirtelTigo', 'AirtelTigo'), ('Vodafone', 'Vodafone')], default='Select Network', max_length=20)),
                ('type', models.CharField(blank=True, choices=[('Regular', 'Regular'), ('Direct', 'Direct'), ('Agent to Agent', 'Agent to Agent')], max_length=20)),
                ('action', models.CharField(choices=[('Deposit', 'Deposit'), ('Withdraw', 'Withdraw')], max_length=20)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('request_status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('date_requested', models.DateField(auto_now_add=True)),
                ('time_requested', models.TimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_requesting', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMobileMoneyAccountsClosed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mtn_physical', models.DecimalField(decimal_places=2, max_digits=19)),
                ('tigoairtel_physical', models.DecimalField(decimal_places=2, max_digits=19)),
                ('vodafone_physical', models.DecimalField(decimal_places=2, max_digits=19)),
                ('mtn_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('tigoairtel_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('vodafone_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('physical_total', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('ecash_total', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMobileMoneyAccountsStarted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mtn_physical', models.DecimalField(decimal_places=2, max_digits=19)),
                ('tigoairtel_physical', models.DecimalField(decimal_places=2, max_digits=19)),
                ('vodafone_physical', models.DecimalField(decimal_places=2, max_digits=19)),
                ('mtn_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('tigoairtel_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('vodafone_ecash', models.DecimalField(decimal_places=2, max_digits=19)),
                ('physical_total', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('ecash_total', models.DecimalField(blank=True, decimal_places=2, max_digits=19)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='agentdepositrequests',
            name='agent',
        ),
        migrations.RemoveField(
            model_name='agentdepositrequests',
            name='guarantor',
        ),
        migrations.DeleteModel(
            name='TwilioApi',
        ),
        migrations.AddField(
            model_name='customerwithdrawal',
            name='id_number',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customerwithdrawal',
            name='id_type',
            field=models.CharField(choices=[('Ghana Card', 'Ghana Card'), ('Passport', 'Passport'), ('Drivers License', 'Drivers License'), ('Voters Id', 'Voters Id')], default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customerwithdrawal',
            name='type',
            field=models.CharField(choices=[('MomoPay', 'MomoPay'), ('Cash Out', 'Cash Out'), ('Agent to Agent', 'Agent to Agent')], default='Passport', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customerrequestdeposit',
            name='request_option',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Mobile Money', 'Money Money'), ('Bank', 'Bank')], default='Physical Cash', max_length=100),
        ),
        migrations.DeleteModel(
            name='AgentDepositRequests',
        ),
    ]
