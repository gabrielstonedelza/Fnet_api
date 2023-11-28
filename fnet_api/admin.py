from django.contrib import admin

from .models import (Customer, CustomerWithdrawal, MyPayments, AdminAccountsStartedWith,
                     AdminAccountsCompletedWith, CustomerAccounts, CashAtPayments, CustomerRequestDeposit,
                     Notifications, ExpensesRequest, BankDeposit, MobileMoneyDeposit, MobileMoneyWithdraw,
                     UserMobileMoneyAccountsStarted, UserMobileMoneyAccountsClosed, PaymentAtBank, OTP,
                     CustomerPaymentAtBank, AddedToApprovedPayment, AddedToApprovedDeposits, Reports, FnetGroupMessage,CashRequest,MyCashPayments,AddedToApprovedCashPayment,WithdrawalReference,AccountNumberWithPoints,Commercials,
                     FnetPrivateUserMessage, PrivateChatId, AddToCustomerPoints, AddToCustomerRedeemPoints,CustomerPoints,CustomerRequestRedeemPoints,
                     ReferCustomer, AddToBlockList,AgentAndOwnerAccounts,CashSupportRequest,CashSupport,CashSupportBalance)

admin.site.register(CustomerRequestRedeemPoints)
admin.site.register(CustomerPoints)
admin.site.register(CashSupportRequest)
admin.site.register(CashSupport)
admin.site.register(CashSupportBalance)
class AdminBankDepositRequest(admin.ModelAdmin):
    list_display = ['id', 'agent', 'customer', 'bank', 'customer', 'account_number', 'account_name','amount','request_status','deposit_paid','date_requested','user_location','user_local_district']

    class Meta:
        model = BankDeposit

class AdminAccountNumberWithPoints(admin.ModelAdmin):
    list_display = ['id', 'agent', 'account_number', 'account_name', 'customer', 'points', 'date_deposited','time_deposited','bank']
    search_fields = ['id', 'agent', 'customer','account_number', 'account_name','bank']

    class Meta:
        model = AccountNumberWithPoints

class AdminCustomerRequests(admin.ModelAdmin):
    list_display = ['id', 'agent', 'customer_phone', 'amount', 'bank', 'request_status', 'date_requested']
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


# class AdminBankDeposit(admin.ModelAdmin):
#     list_display = ['id', 'agent', 'customer', 'bank', 'account_number', 'account_name', 'amount', 'depositor_name',
#                     'request_status', 'deposit_paid', '']
#     search_fields = ['id', 'agent', ]
#
#     class Meta:
#         model = BankDeposit


class AdminMobileMoneyDeposit(admin.ModelAdmin):
    list_display = ['id', 'agent', 'customer_phone', 'depositor_name', 'depositor_number', 'network', 'type', 'amount',
                 'date_deposited']
    search_fields = ['id', 'agent', 'customer_phone']

    class Meta:
        model = MobileMoneyDeposit


class AdminMobileMoneyWithdraw(admin.ModelAdmin):
    list_display = ['id', 'agent', 'customer_phone', 'network', 'type', 'amount',]
    search_fields = ['id', 'agent', 'customer_phone']

    class Meta:
        model = MobileMoneyWithdraw


class AdminUserMobileMoneyAccountsStarted(admin.ModelAdmin):
    list_display = ['id', 'agent', 'physical', 'mtn_ecash', 'tigoairtel_ecash', 'vodafone_ecash',
                    'ecash_total', 'date_posted', ]
    search_fields = ['id', 'agent', ]

    class Meta:
        model = UserMobileMoneyAccountsStarted


class AdminUserMobileMoneyAccountsClosed(admin.ModelAdmin):
    list_display = ['id', 'agent', 'physical', 'mtn_ecash', 'tigoairtel_ecash', 'vodafone_ecash',
                    'ecash_total', 'date_posted', ]
    search_fields = ['id', 'agent', ]

    class Meta:
        model = UserMobileMoneyAccountsClosed


class AdminCustomerWithdrawal(admin.ModelAdmin):
    list_display = ['id', 'agent', 'customer', 'bank', 'withdrawal_type', 'id_type',
                    'id_number', 'amount', 'date_requested']
    search_fields = ['id', 'agent', ]

    class Meta:
        model = CustomerWithdrawal


class AdminMyPayments(admin.ModelAdmin):
    list_display = ['id', 'agent', 'mode_of_payment1', 'mode_of_payment2', 'cash_at_location1', 'cash_at_location2',
                    'bank1', 'bank2', 'amount', 'amount1', 'amount2', 'transaction_id1', 'transaction_id2',
                    'payment_action', 'payment_status', 'payment_month', 'date_created']
    search_fields = ['id', 'agent', ]

    class Meta:
        model = MyPayments


class AdminPaymentAtBank(admin.ModelAdmin):
    list_display = ['id', 'agent', 'teller_name', 'teller_phone', 'amount', 'total',
                    'd_200', 'd_100', 'd_50', 'd_20', 'd_10', 'd_5', 'd_2',
                    'd_1', 'date_added', ]
    search_fields = ['id', 'agent', ]

    class Meta:
        model = PaymentAtBank


admin.site.register(AccountNumberWithPoints,AdminAccountNumberWithPoints)
admin.site.register(AgentAndOwnerAccounts)
admin.site.register(Commercials)
admin.site.register(MyCashPayments)
admin.site.register(WithdrawalReference)
admin.site.register(AddedToApprovedCashPayment)
admin.site.register(ReferCustomer)
admin.site.register(CashRequest)
admin.site.register(AddToBlockList)
admin.site.register(AddToCustomerPoints)
admin.site.register(AddToCustomerRedeemPoints)
admin.site.register(Reports)
admin.site.register(PrivateChatId)
admin.site.register(FnetGroupMessage)
admin.site.register(FnetPrivateUserMessage)
admin.site.register(Customer, AdminCustomer)
admin.site.register(ExpensesRequest, AdminExpensesRequest)
admin.site.register(BankDeposit,AdminBankDepositRequest)
admin.site.register(MobileMoneyDeposit, AdminMobileMoneyDeposit)
admin.site.register(MobileMoneyWithdraw, AdminMobileMoneyWithdraw)
admin.site.register(CustomerWithdrawal, AdminCustomerWithdrawal)
admin.site.register(MyPayments, AdminMyPayments)
admin.site.register(AdminAccountsStartedWith)
admin.site.register(AdminAccountsCompletedWith)
admin.site.register(CustomerAccounts, AdminCustomerAccounts)
admin.site.register(CashAtPayments, AdminCashAtPayments)
admin.site.register(CustomerRequestDeposit, AdminCustomerRequests)
admin.site.register(Notifications)
admin.site.register(UserMobileMoneyAccountsStarted, AdminUserMobileMoneyAccountsStarted)
admin.site.register(UserMobileMoneyAccountsClosed, AdminUserMobileMoneyAccountsClosed)
admin.site.register(PaymentAtBank, AdminPaymentAtBank)
admin.site.register(OTP)
admin.site.register(CustomerPaymentAtBank)
admin.site.register(AddedToApprovedPayment)
admin.site.register(AddedToApprovedDeposits)