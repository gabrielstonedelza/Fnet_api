from django.contrib import admin

from .models import (Customer, AgentDepositRequests, CustomerWithdrawal, Payments, TwilioApi, AdminAccountsStartedWith,
                     AdminAccountsCompletedWith, CustomerAccounts, CashAtPayments, WithdrawReference,CustomerRequestDeposit,UserFlags)

admin.site.register(Customer)
admin.site.register(AgentDepositRequests)
admin.site.register(CustomerWithdrawal)
admin.site.register(Payments)
admin.site.register(TwilioApi)
admin.site.register(AdminAccountsStartedWith)
admin.site.register(AdminAccountsCompletedWith)
admin.site.register(CustomerAccounts)
admin.site.register(CashAtPayments)
admin.site.register(WithdrawReference)
admin.site.register(CustomerRequestDeposit)
admin.site.register(UserFlags)

