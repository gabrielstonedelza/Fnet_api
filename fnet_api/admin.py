from django.contrib import admin

from .models import (Customer, AgentDepositRequests, CustomerWithdrawal, Payments,TwilioApi,AdminAccountsStartedWith,
AdminAccountsCompletedWith,CustomerAccounts,BankPayment,WithdrawFerence)

admin.site.register(Customer)
admin.site.register(AgentDepositRequests)
admin.site.register(CustomerWithdrawal)
admin.site.register(Payments)
admin.site.register(TwilioApi)
admin.site.register(AdminAccountsStartedWith)
admin.site.register(AdminAccountsCompletedWith)
admin.site.register(CustomerAccounts)
admin.site.register(BankPayment)
admin.site.register(WithdrawFerence)

