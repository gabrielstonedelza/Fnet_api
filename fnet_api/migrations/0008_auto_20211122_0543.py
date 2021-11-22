# Generated by Django 3.2.9 on 2021-11-22 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnet_api', '0007_alter_agentdepositrequests_bank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentdepositrequests',
            name='bank',
            field=models.CharField(blank=True, choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='customeraccounts',
            name='bank',
            field=models.CharField(choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB')], default='Access Bank', max_length=100),
        ),
        migrations.AlterField(
            model_name='customerwithdrawal',
            name='bank',
            field=models.CharField(choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB')], default='GT Bank', max_length=100),
        ),
        migrations.AlterField(
            model_name='payments',
            name='bank',
            field=models.CharField(blank=True, choices=[('Select bank', 'Select bank'), ('Access Bank', 'Access Bank'), ('Cal Bank', 'Cal Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('Ecobank', 'Ecobank'), ('Pan Africa', 'Pan Africa'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('SGSSB', 'SGSSB')], max_length=50),
        ),
        migrations.AlterField(
            model_name='payments',
            name='cash_at_location',
            field=models.CharField(blank=True, choices=[('Please select cash at location', 'Please select cash at location'), ('Cash @ location', 'Cash @ location'), ('DVLA', 'DVLA'), ('HEAD OFFICE', 'HEAD OFFICE'), ('KEJETIA', 'KEJETIA'), ('ECOBANK', 'ECOBANK'), ('PAN AFRICA', 'PAN AFRICA')], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='payments',
            name='payment_action',
            field=models.CharField(choices=[('Select payment action', 'Select payment action'), ('Not Closed', 'Not Closed'), ('Close Payment', 'Close Payment')], default='Not Closed', max_length=50),
        ),
    ]
