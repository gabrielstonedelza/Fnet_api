from django.urls import path
from . import views

urlpatterns = [
    path('admin_user/', views.get_admin),
    path('request_detail/<int:pk>/', views.cash_detail),

    path('register_customer/', views.register_customer),
    path('customer_withdrawal/', views.customer_withdrawal),
    path('all_agents/', views.GetAllAgents.as_view()),
    path('all_customers/', views.GetAllCustomers.as_view()),
    path('customer_detail/<int:pk>/', views.customer_details),
    path('get_user_customers/<str:username>/', views.get_user_customers),
    path('agent_customer_summary/', views.agent_customers_summary),

    path('agents_customers_withdrawal_summary/', views.customer_withdrawal_summary),
    path('payments/', views.get_payments),
    path('make_payments/', views.make_payments),
    path('approve_payments/<int:id>/', views.approve_payment),
    path('payment_summary/', views.payment_summary),
    path('get_agent/<str:username>/', views.get_agent),
    path('payment_detail/<int:pk>/', views.payment_detail),
    path('get_customer/<str:name>/', views.get_customer),
    path('get_customer_by_phone/<str:phone>/', views.get_customer_by_phone),
    path('admin_accounts_started/', views.admin_accounts_started),
    path('admin_accounts_completed/', views.admin_accounts_completed),
    path('admin_accounts_started_lists/', views.admin_accounts_started_lists),
    path('admin_accounts_completed_lists/', views.admin_accounts_completed_lists),
    path('user_customers/', views.user_customers),
    path('user_transaction_payments/<str:username>/', views.user_transaction_payments),
    path('user_transaction_withdrawals/<str:username>/', views.user_transaction_withdrawals),

    path('register_customer_accounts/', views.register_customer_account),
    path('get_customer_accounts/',views.get_customer_accounts),
    path('customer_account_detail/<int:id>/',views.customer_account_detail),
    path('get_customer_account/<str:phone>/',views.get_customer_account),
    path('update_accounts/<int:id>/',views.update_accounts),
    path('admin_account_detail/<int:id>/',views.admin_account_detail),

    path("get_payment_total/",views.get_payment_total),
    path("get_payment_approved_total/",views.get_payment_approved_total),
    path('get_customer_accounts_by_bank/<str:customer_phone>/<str:bank>/',views.get_customer_accounts_by_bank),

    path("make_cash_at_payment/", views.make_bank_payment),
    path("add_withdraw_reference/", views.add_withdraw_reference),
    path("get_bank_payments/",views.get_user_bank_payments),
    path("get_withdraw_reference/",views.get_user_withdraw_reference),

    path("delete_user/<int:pk>/", views.user_delete),
    path("delete_customer/<int:pk>/", views.customer_delete),
    path("delete_customer_request/<int:id>/", views.delete_customer_request),
    path("search_user_customers/",views.GetAllUserCustomers.as_view()),

    path('customer_request_deposit/', views.customer_deposit_request),
    path('get_your_customers_request/', views.get_your_customers_requests),
    path('get_customers_request/<str:phone>/',views.get_customers_requests),
    path('approve_customer_request/<int:id>/',views.approve_customer_request),
    path("get_customer_request_summary/<str:phone>/", views.get_customer_request_summary),
    path("customer_request_detail/<int:pk>/",views.customer_request_detail),

    path('add_user_flag/',views.add_flag),
    path('get_flags/',views.get_flags),

#     newly added get request
    path('get_agent_cash_request_admin/',views.get_agent_cash_requests_admin),
    path('get_agent_bank_request_admin/',views.get_agent_bank_requests_admin),
    path('get_agent_cash_total_today_admin/<str:username>/',views.get_agents_cash_for_today),
    path('get_agent_bank_total_today_admin/<str:username>/',views.get_agents_bank_for_today),
    path('get_user_momo_deposits/',views.get_user_mm_deposits),
    path('get_user_momo_withdraws/',views.get_user_mm_withdrawal),
    path('get_agents_momo_withdraws/<str:username>/',views.get_agents_mobile_money_withdraws),
    path('get_agents_momo_deposits/<str:username>/',views.get_agents_mobile_money_deposits),
    path("get_user_momo_accounts_started/",views.get_user_mobile_money_accounts_started),
    path("get_user_momo_accounts_closed/",views.get_user_mobile_money_accounts_closed),
    path("get_agent_momo_accounts_closed/<str:username>/",views.get_agents_mobile_money_accounts_closed),
    path("get_agent_momo_accounts_started/<str:username>/",views.get_agents_mobile_money_accounts_started),

#     newly added post requests
    path('post_cash_deposit/',views.post_cash_deposit),
    path('post_bank_deposit/',views.post_bank_deposit),
    path('post_momo_deposit/',views.post_momo_deposit),
    path('post_momo_withdraw/',views.post_momo_withdraw),
    path('post_momo_accounts_started/',views.post_momo_accounts_started),
    path('post_momo_accounts_closed/',views.post_momo_accounts_closed),

    path('approve_cash_deposit/<int:id>/',views.approve_cash_deposit),
    path('approve_bank_deposit/<int:id>/',views.approve_bank_deposit),
    path('delete_cash_deposit/<int:id>/',views.delete_cash_request),
    path('delete_bank_deposit/<int:id>/',views.delete_bank_request),

    path("cash_detail/<int:pk>/",views.cash_detail),
    path("bank_detail/<int:pk>/",views.bank_detail),
    path("momo_accounts_started_detail/<int:pk>/",views.momo_accounts_started_detail),

    path('update_customers_details/<int:id>/',views.update_customers_details),
    path('update_momo_accounts/<int:id>/',views.update_momo_accounts),

    path('get_momo_deposit_customer/<str:phone>/',views.get_momo_deposit_customer_by_phone),
    path('get_momo_withdraw_customer/<str:phone>/',views.get_momo_withdraw_customer_by_phone),
    path('get_all_momo_deposit_customers/', views.get_all_momo_deposit_customers),
    path('get_all_momo_withdrawal_customers/', views.get_all_momo_withdraw_customers),
    path('get_cash_total_today/',views.get_cash_deposits_for_today),
    path('get_bank_total_today/',views.get_bank_deposits_for_today),
    path('get_deposit_commission/',views.get_deposit_commission),
    path('get_withdraw_commission/',views.get_withdraw_commission),
    path('get_agent_deposit_commission/<str:username>/',views.get_agents_deposit_commission),
    path('get_agent_withdraw_commission/<str:username>/',views.get_agents_withdraw_commission),
    path('search_agents_momo_deposit_transaction/', views.SearchAgentsMomoDepositTransactions.as_view()),
    path('search_agents_momo_withdraw_transaction/', views.SearchAgentsMomoWithdrawTransactions.as_view()),
    path('approve_bank_deposit_paid/<int:id>/', views.approve_bank_deposit_paid),
    path('approve_cash_deposit_paid/<int:id>/', views.approve_cash_deposit_paid),
    path('get_unpaid_cash_deposits_for_today/', views.get_unpaid_cash_deposits_for_today),
    path('get_unpaid_bank_deposits_for_today/', views.get_unpaid_bank_deposits_for_today),

#
    path("get_all_bank_deposits/",views.get_all_bank_deposits)


]
