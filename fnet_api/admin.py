from django.contrib import admin

from .models import (Customer, CustomerWithdrawal, Payments, AdminAccountsStartedWith,
                     AdminAccountsCompletedWith, CustomerAccounts, CashAtPayments, WithdrawReference,CustomerRequestDeposit,UserFlags,CashDeposit,BankDeposit,MobileMoneyDeposit)

admin.site.register(Customer)
admin.site.register(CashDeposit)
admin.site.register(BankDeposit)
admin.site.register(MobileMoneyDeposit)
admin.site.register(CustomerWithdrawal)
admin.site.register(Payments)
admin.site.register(AdminAccountsStartedWith)
admin.site.register(AdminAccountsCompletedWith)
admin.site.register(CustomerAccounts)
admin.site.register(CashAtPayments)
admin.site.register(WithdrawReference)
admin.site.register(CustomerRequestDeposit)
admin.site.register(UserFlags)

