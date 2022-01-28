from django.contrib import admin

from .models import (Customer, CustomerWithdrawal, MyPayments, AdminAccountsStartedWith,
                     AdminAccountsCompletedWith, CustomerAccounts, CashAtPayments, WithdrawReference, CustomerRequestDeposit, Notifications, CashDeposit, BankDeposit, MobileMoneyDeposit, MobileMoneyWithdraw, UserMobileMoneyAccountsStarted, UserMobileMoneyAccountsClosed)

admin.site.register(Customer)
admin.site.register(CashDeposit)
admin.site.register(BankDeposit)
admin.site.register(MobileMoneyDeposit)
admin.site.register(MobileMoneyWithdraw)
admin.site.register(CustomerWithdrawal)
admin.site.register(MyPayments)
admin.site.register(AdminAccountsStartedWith)
admin.site.register(AdminAccountsCompletedWith)
admin.site.register(CustomerAccounts)
admin.site.register(CashAtPayments)
admin.site.register(WithdrawReference)
admin.site.register(CustomerRequestDeposit)
admin.site.register(Notifications)
admin.site.register(UserMobileMoneyAccountsStarted)
admin.site.register(UserMobileMoneyAccountsClosed)

