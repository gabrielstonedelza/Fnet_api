from django.contrib import admin

from .models import (Customer, CustomerWithdrawal, MyPayments, AdminAccountsStartedWith,
                     AdminAccountsCompletedWith, CustomerAccounts, CashAtPayments, CustomerRequestDeposit,
                     Notifications, ExpensesRequest, BankDeposit, MobileMoneyDeposit, MobileMoneyWithdraw,
                     UserMobileMoneyAccountsStarted, UserMobileMoneyAccountsClosed, PaymentAtBank, OTP,
                     CustomerPaymentAtBank, AddedToApprovedPayment, AddedToApprovedDeposits, Reports, FnetGroupMessage,
                     FnetPrivateUserMessage, PrivateChatId, AddToCustomerPoints, AddToCustomerRedeemPoints,
                     ReferCustomer, AddToBlockList)


class AdminCustomerRequests(admin.ModelAdmin):
    list_display = ['id', 'agent', 'customer_phone', 'amount', 'request_option', 'request_status', 'date_requested']
    search_fields = ['id', 'agent', 'customer_phone']

    class Meta:
        model = CustomerRequestDeposit


class AdminCashAtPayments(admin.ModelAdmin):
    list_display = ['id', 'agent', 'location', 'amount', 'left_with', 'left_with_phone', 'reference_id', 'date_paid',
                    'time_paid']
    search_fields = ['id', 'agent', 'left_with_phone']

    class Meta:
        model = CashAtPayments


class AdminCustomer(admin.ModelAdmin):
    list_display = ['id', 'agent', 'location', 'name', 'digital_address', 'id_type', 'id_number', 'phone',
                    'points', 'date_of_birth']
    search_fields = ['id', 'agent', 'name', 'phone']

    class Meta:
        model = Customer


class AdminCustomerAccounts(admin.ModelAdmin):
    list_display = ['id', 'agent', 'account_number', 'account_name', 'bank', 'phone', 'date_added', ]
    search_fields = ['id', 'agent', 'account_number', 'phone', 'account_name']

    class Meta:
        model = CustomerAccounts


class AdminExpensesRequest(admin.ModelAdmin):
    list_display = ['id', 'agent', 'amount', 'reason', 'request_status', 'deposit_paid', 'date_requested', ]
    search_fields = ['id', 'agent', ]

    class Meta:
        model = ExpensesRequest


admin.site.register(ReferCustomer)
admin.site.register(AddToBlockList)
admin.site.register(AddToCustomerPoints)
admin.site.register(AddToCustomerRedeemPoints)
admin.site.register(Reports)
admin.site.register(PrivateChatId)
admin.site.register(FnetGroupMessage)
admin.site.register(FnetPrivateUserMessage)
admin.site.register(Customer, AdminCustomer)
admin.site.register(ExpensesRequest, AdminExpensesRequest)
admin.site.register(BankDeposit)
admin.site.register(MobileMoneyDeposit)
admin.site.register(MobileMoneyWithdraw)
admin.site.register(CustomerWithdrawal)
admin.site.register(MyPayments)
admin.site.register(AdminAccountsStartedWith)
admin.site.register(AdminAccountsCompletedWith)
admin.site.register(CustomerAccounts, AdminCustomerAccounts)
admin.site.register(CashAtPayments, AdminCashAtPayments)
admin.site.register(CustomerRequestDeposit, AdminCustomerRequests)
admin.site.register(Notifications)
admin.site.register(UserMobileMoneyAccountsStarted)
admin.site.register(UserMobileMoneyAccountsClosed)
admin.site.register(PaymentAtBank)
admin.site.register(OTP)
admin.site.register(CustomerPaymentAtBank)
admin.site.register(AddedToApprovedPayment)
admin.site.register(AddedToApprovedDeposits)
