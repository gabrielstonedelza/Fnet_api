from django.contrib import admin

from .models import FNetAdmin, Customer, AgentDepositRequests, CustomerWithdrawal, Payments

admin.site.register(FNetAdmin)
admin.site.register(Customer)
admin.site.register(AgentDepositRequests)
admin.site.register(CustomerWithdrawal)
admin.site.register(Payments)
