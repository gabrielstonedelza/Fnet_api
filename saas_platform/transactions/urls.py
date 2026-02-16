from django.urls import path
from . import views

app_name = "transactions"

urlpatterns = [
    path("", views.transactions, name="transaction-list"),
    path("<uuid:transaction_id>/", views.transaction_detail, name="transaction-detail"),

    # Create by channel
    path("bank-deposit/", views.create_bank_deposit, name="create-bank-deposit"),
    path("mobile-money/", views.create_momo_transaction, name="create-momo"),
    path("cash/", views.create_cash_transaction, name="create-cash"),

    # Approvals
    path("pending/", views.pending_approvals, name="pending-approvals"),
    path("<uuid:transaction_id>/approve/", views.approve_transaction, name="approve-transaction"),

    # Reversals
    path("<uuid:transaction_id>/reverse/", views.reverse_transaction, name="reverse-transaction"),

    # Expenses
    path("expenses/", views.expense_requests, name="expense-list-create"),
    path("expenses/<uuid:expense_id>/approve/", views.approve_expense, name="approve-expense"),

    # Daily closings
    path("daily-closings/", views.daily_closings, name="daily-closing-list-create"),
    path("daily-closings/<uuid:closing_id>/", views.daily_closing_detail, name="daily-closing-detail"),

    # Provider balances
    path("balances/", views.provider_balances, name="provider-balance-list"),
    path("balances/set/", views.set_provider_balance, name="set-provider-balance"),
    path("balances/initialize/", views.initialize_all_balances, name="initialize-all-balances"),
    path("balances/adjust/", views.adjust_provider_balance, name="adjust-provider-balance"),
]
