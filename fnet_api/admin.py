from django.contrib import admin

from .models import FNetAdmin, Customer, AgentDepositRequests, CustomerWithdrawal, Payments,TwilioApi

admin.site.register(FNetAdmin)
admin.site.register(Customer)
admin.site.register(AgentDepositRequests)
admin.site.register(CustomerWithdrawal)
admin.site.register(Payments)
admin.site.register(TwilioApi)
