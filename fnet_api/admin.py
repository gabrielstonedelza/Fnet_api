from django.contrib import admin

from .models import (Customer, CustomerWithdrawal, MyPayments, AdminAccountsStartedWith,
                     AdminAccountsCompletedWith, CustomerAccounts, CashAtPayments, CustomerRequestDeposit,
                     Notifications, ExpensesRequest, BankDeposit, MobileMoneyDeposit, MobileMoneyWithdraw,
                     UserMobileMoneyAccountsStarted, UserMobileMoneyAccountsClosed, PaymentAtBank, OTP,
                     CustomerPaymentAtBank, AddedToApprovedPayment, AddedToApprovedDeposits, Reports, FnetGroupMessage, FnetPrivateUserMessage, PrivateChatId, AddToCustomerPoints, AddToCustomerRedeemPoints, ReferCustomer, AddToBlockList)

admin.site.register(ReferCustomer)
admin.site.register(AddToBlockList)
admin.site.register(AddToCustomerPoints)
admin.site.register(AddToCustomerRedeemPoints)
admin.site.register(Reports)
admin.site.register(PrivateChatId)
admin.site.register(FnetGroupMessage)
admin.site.register(FnetPrivateUserMessage)
admin.site.register(Customer)
admin.site.register(ExpensesRequest)
admin.site.register(BankDeposit)
admin.site.register(MobileMoneyDeposit)
admin.site.register(MobileMoneyWithdraw)
admin.site.register(CustomerWithdrawal)
admin.site.register(MyPayments)
admin.site.register(AdminAccountsStartedWith)
admin.site.register(AdminAccountsCompletedWith)
admin.site.register(CustomerAccounts)
admin.site.register(CashAtPayments)
admin.site.register(CustomerRequestDeposit)
admin.site.register(Notifications)
admin.site.register(UserMobileMoneyAccountsStarted)
admin.site.register(UserMobileMoneyAccountsClosed)
admin.site.register(PaymentAtBank)
admin.site.register(OTP)
admin.site.register(CustomerPaymentAtBank)
admin.site.register(AddedToApprovedPayment)
admin.site.register(AddedToApprovedDeposits)
