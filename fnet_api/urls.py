from django.urls import path
from . import views

urlpatterns = [
    path('admin_user/', views.get_admin),
    path('request_detail/<int:pk>/', views.expense_detail),

    path('register_customer/', views.register_customer),
    path('admin_register_customer/', views.admin_register_customer),
    path('customer_withdrawal/', views.customer_withdrawal),
    path('all_agents/', views.GetAllAgents.as_view()),
    path('all_customers/', views.GetAllCustomers.as_view()),
    path('customer_detail/<int:pk>/', views.customer_details),
    path('customer_details_by_phone/<str:phone>/', views.customer_details_by_phone),
    path('get_user_customers/<str:username>/', views.get_user_customers),
    path('agent_customer_summary/', views.agent_customers_summary),

    path('agents_customers_withdrawal_summary/', views.customer_withdrawal_summary),
    path('payments/', views.get_payments),
    path('get_all_payments/', views.get_all_payments),
    path('make_payments/', views.make_payments),
    path('approve_payments/<int:id>/', views.approve_payment),
    path('approve_cash_payment/<int:id>/', views.approve_cash_payment),
    path('delete_payment/<int:id>/', views.delete_payment),
    path('delete_cash_payment/<int:id>/', views.delete_cash_payment),
    path('payment_summary/', views.payment_summary),
    path('cash_payment_summary/', views.cash_payment_summary),
    path('get_agent/<str:username>/', views.get_agent),
    path('payment_detail/<int:pk>/', views.payment_detail),
    path('cash_payment_detail/<int:pk>/', views.cash_payment_detail),
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
    path('get_customer_accounts/', views.get_customer_accounts),
    path('customer_account_detail/<int:id>/', views.customer_account_detail),
    path('get_customer_account/<str:phone>/', views.get_customer_account),
    path('update_accounts/<int:id>/', views.update_accounts),
    path('admin_account_detail/<int:id>/', views.admin_account_detail),

    path("get_user_payments/", views.get_user_payments),
    path("get_payment_approved_total/", views.get_payment_approved_total),
    path('get_customer_accounts_by_bank/<str:customer_phone>/<str:bank>/', views.get_customer_accounts_by_bank),

    path("make_cash_at_payment/", views.make_bank_payment),
    path("add_withdraw_reference/", views.add_withdraw_reference),
    path("get_bank_payments/", views.get_user_bank_payments),
    # path("get_withdraw_reference/", views.get_user_withdraw_reference),

    path("delete_user/<int:pk>/", views.user_delete),
    path("delete_customer/<int:pk>/", views.customer_delete),
    path("delete_customer_request/<int:id>/", views.delete_customer_request),
    path("search_user_customers/", views.GetAllUserCustomers.as_view()),

    path('customer_request_deposit/', views.customer_deposit_request),
    path('get_your_customers_request/', views.get_your_customers_requests),
    path('get_customers_request/<str:phone>/', views.get_customers_requests),
    path('approve_customer_request/<int:id>/', views.approve_customer_request),
    path("get_customer_request_summary/<str:phone>/", views.get_customer_request_summary),
    path("customer_request_detail/<int:pk>/", views.customer_request_detail),

    path('add_user_flag/', views.add_flag),
    path('get_flags/', views.get_flags),

    #     newly added get request
    path('get_agent_cash_request_admin/', views.get_agent_expense_requests_admin),
    path('get_agent_bank_request_admin/', views.get_agent_bank_requests_admin),
    path('get_agent_cash_total_today_admin/<str:username>/', views.get_agents_expenses_for_today),
    path('get_agent_bank_total_today_admin/<str:username>/', views.get_agents_bank_for_today),
    path('get_user_momo_deposits/', views.get_user_mm_deposits),
    path('get_user_momo_withdraws/', views.get_user_mm_withdrawal),
    path('get_agents_momo_withdraws/<str:username>/', views.get_agents_mobile_money_withdraws),
    path('get_agents_momo_deposits/<str:username>/', views.get_agents_mobile_money_deposits),
    path("get_user_momo_accounts_started/", views.get_user_mobile_money_accounts_started),
    path("get_user_momo_accounts_closed/", views.get_user_mobile_money_accounts_closed),
    path("get_agent_momo_accounts_closed/<str:username>/", views.get_agents_mobile_money_accounts_closed),
    path("get_agent_momo_accounts_started/<str:username>/", views.get_agents_mobile_money_accounts_started),

    #     newly added post requests
    path('post_cash_deposit/', views.post_expenses_request),
    path('post_bank_deposit/', views.post_bank_deposit),
    path('post_momo_deposit/', views.post_momo_deposit),
    path('post_momo_withdraw/', views.post_momo_withdraw),
    path('post_momo_accounts_started/', views.post_momo_accounts_started),
    path('post_momo_accounts_closed/', views.post_momo_accounts_closed),

    path('approve_cash_deposit/<int:id>/', views.approve_expense_request),
    path('approve_bank_deposit/<int:id>/', views.approve_bank_deposit),
    path('delete_cash_deposit/<int:id>/', views.delete_expense_request),
    path('delete_bank_deposit/<int:id>/', views.delete_bank_request),

    path("cash_detail/<int:pk>/", views.expense_detail),
    path("bank_detail/<int:pk>/", views.bank_detail),

    path("momo_accounts_started_detail/<int:pk>/", views.momo_accounts_started_detail),

    path('update_customers_details/<int:id>/', views.update_customers_details),
    path('update_customers_accounts_details/<int:id>/', views.update_report),
    path('delete_customer_accounts/<int:id>/', views.delete_customer_accounts),
    path("customers_account_detail/<int:pk>/", views.customers_account_detail),
    path('search_customers_accounts/', views.GetAllCustomersAccounts.as_view()),
    path('update_momo_accounts/<int:id>/', views.update_momo_accounts),

    path('get_momo_deposit_customer/<str:phone>/', views.get_momo_deposit_customer_by_phone),
    path('get_momo_withdraw_customer/<str:phone>/', views.get_momo_withdraw_customer_by_phone),
    path('get_all_momo_deposit_customers/', views.get_all_momo_deposit_customers),
    path('get_all_momo_withdrawal_customers/', views.get_all_momo_withdraw_customers),
    path('get_cash_total_today/', views.get_expense_request_for_today),
    path('get_bank_total_today/', views.get_bank_deposits_for_today),
    path('get_deposit_commission/', views.get_deposit_commission),
    path('get_withdraw_commission/', views.get_withdraw_commission),
    path('get_agent_deposit_commission/<str:username>/', views.get_agents_deposit_commission),
    path('get_agent_withdraw_commission/<str:username>/', views.get_agents_withdraw_commission),
    path('search_agents_momo_deposit_transaction/', views.SearchAgentsMomoDepositTransactions.as_view()),
    path('search_agents_momo_withdraw_transaction/', views.SearchAgentsMomoWithdrawTransactions.as_view()),
    path('approve_bank_deposit_paid/<int:id>/', views.approve_bank_deposit_paid),
    path('approve_cash_deposit_paid/<int:id>/', views.approve_expense_request_paid),
    path('approve_cash_request_paid/<int:id>/', views.approve_cash_request_paid),
    path('get_unpaid_cash_deposits_for_today/', views.get_unpaid_expense_request_for_today),
    path('get_unpaid_bank_deposits_for_today/', views.get_unpaid_bank_deposits_for_today),

    #
    path("get_all_bank_deposits/", views.get_all_bank_deposits),
    path("get_all_cash_at_payments/", views.get_all_cash_at_payments),
    path("get_all_momo_deposit_made/", views.get_all_momo_deposit_made),
    path("get_all_momo_withdrawal_made/", views.get_all_momo_withdrawal_made),
    path("get_all_user_momo_accounts_started/", views.get_all_user_momo_accounts_started),
    path("get_all_user_momo_accounts_closed/", views.get_all_user_momo_accounts_closed),
    path("get_all_users/", views.get_all_users),
    path("get_cash_deposits_all/", views.get_expenses_request_all),
    path("get_bank_deposits_all/", views.get_bank_deposits_all),

    #
    path('get_user_notifications/', views.get_user_notifications),
    path('get_all_user_notifications/', views.get_all_user_notifications),
    path('get_all_read_user_notifications/', views.get_all_read_user_notifications),
    path('get_triggered_notifications/', views.get_triggered_notifications),
    path("read_notification/<int:id>/", views.read_notification),
    path("get_customer_transaction_summary/<str:phone>/", views.get_customer_transaction_summary),
    path("get_customer_accounts/<str:phone>/", views.get_customer_accounts),
    path("get_momo_withdraw_user/<str:phone>/", views.get_momo_withdraw_user),
    path('get_agents_bank_total_by_date/', views.get_agents_bank_total_by_date),
    path('get_customer_bank_withdrawal_summary/', views.get_customer_bank_withdrawal_summary),
    path('get_agents_cash_total_by_date/', views.get_agents_expense_request_total_by_date),
    path('user_total_payments/', views.user_total_payments),
    path('get_all_users_expenses_total/', views.get_all_users_expenses_total),

    #
    path('get_all_customer_accounts/', views.get_all_customer_accounts),
    path('get_all_customer_requests/', views.get_all_customer_requests),
    path('get_all_user_payments/', views.get_all_user_payments),
    path('notifications/', views.notifications),
    path('all_user_accounts_started/', views.all_user_accounts_started),
    path('all_user_accounts_closed/', views.all_user_accounts_closed),
    path("post_at_bank/", views.post_at_bank),
    path("get_all_data_at_bank/", views.get_all_data_at_bank),
    path("get_all_my_data_at_bank/", views.get_all_my_data_at_bank),
    path("bank_payment_detail/<int:pk>/", views.bank_payment_detail),

    #     OTP
    path("send_otp_to_customer_admin/", views.send_otp_to_customer_admin),
    path("get_admin_otp_notifications/", views.get_admin_otp_notifications),
    path("get_customer_otp_notifications/<str:phone_number>/", views.get_customer_otp_notifications),

    #     customer notifications
    path("get_all_customer_notifications/<str:phone_number>/", views.get_all_customer_notifications),
    path("get_customer_notifications/<str:phone_number>/", views.get_customer_notifications),
    path("get_all_customer_read_user_notifications/<str:phone_number>/",
         views.get_all_customer_read_user_notifications),
    path("get_customer_triggered_notifications/<str:phone_number>/", views.get_customer_triggered_notifications),
    path("read_customer_notification/<int:id>/", views.read_customer_notification),

    #     customer payment at bank
    path('post_customer_at_bank/', views.post_customer_at_bank),
    path('get_all_customer_data_at_bank/<str:customer>/', views.get_all_customer_data_at_bank),
    path('customer_bank_payment_detail/<int:pk>/', views.customer_bank_payment_detail),
    path('get_all_customers_data_at_bank/', views.get_all_customers_data_at_bank),

    #     admin notifications
    path("get_customer_bank_payment_notifications/", views.get_customer_bank_payment_notifications),
    path("get_customer_otp_notifications/", views.get_customer_otp_notifications),
    path("get_user_payments_notifications/", views.get_user_payments_notifications),
    path("get_user_cash_payments_notifications/", views.get_user_cash_payments_notifications),
    path("get_user_bank_requests_notifications/", views.get_user_bank_requests_notifications),
    path("get_user_report_notifications/", views.get_user_report_notifications),
    path("get_user_expenses_requests_notifications/", views.get_user_expenses_requests_notifications),
    path("get_customer_requests_notifications/", views.get_customer_requests_notifications),

    #     ADD TO APPROVED
    path("admin_add_to_approved_payment/", views.admin_add_to_approved_payment),
    path("admin_add_to_approved_bank_deposit/", views.admin_add_to_approved_bank_deposit),


    #     getting customers deposit transactions
    path("get_customers_deposit_transactions/", views.GetCustomersDepositTransactions.as_view()),
    path("GetCustomerDepositTransactions/<str:customer>/", views.GetCustomerDepositTransactions.as_view()),

    # momo deposits and withdraw summary
    path("get_user_mtn_deposits_summary/", views.get_user_mtn_deposits_summary),
    path("get_user_tigo_deposits_summary/", views.get_user_tigo_deposits_summary),
    path("get_user_vodafone_deposits_summary/", views.get_user_vodafone_deposits_summary),
    path("get_user_momo_agent_to_agent_summary/", views.get_user_momo_agent_to_agent_summary),
    path("get_user_mtn_withdrawal/", views.get_user_mtn_withdrawal),
    path("get_user_tigo_withdrawal/", views.get_user_tigo_withdrawal),
    path("get_user_vodafone_withdrawal/", views.get_user_vodafone_withdrawal),

    #     reports
    path("add_report/", views.add_report),
    path("report_detail/<int:id>/", views.report_detail),
    path("update_report/<int:id>/", views.update_report),
    path("get_all_my_reports/", views.get_all_my_reports),
    path("get_all_reports/", views.get_all_reports),
    path("get_user_reports/<str:username>/", views.get_user_reports),

    # private and group messages
    path("private_message_detail/<str:private_chat_id>/", views.private_message_detail),
    path("get_private_message/<int:user1>/<int:user2>/", views.get_private_message),
    path("send_private_message/", views.send_private_message),
    path("get_all_group_message/", views.get_all_group_message),
    path("send_group_message/", views.send_group_message),

    #   customer points
    path("get_customer_points/<str:customer_phone>/", views.get_customer_points),
    path("get_customer_redeemed_points/<str:customer_phone>/", views.get_customer_redeemed_points),
    path("get_all_redeemed_points/", views.get_all_redeemed_points),
    path("add_to_customer_redeemed_points/", views.add_to_customer_redeemed_points),

    #     customer referrals
    path("refer_customer/", views.refer_customer),
    path("get_all_customer_referrals/<str:referral>/", views.get_all_customer_referrals),
    path("referral_detail/<int:pk>/", views.referral_detail),
    path("update_referral/<int:id>/", views.update_referral),
    path("get_all_referrals/", views.get_all_referrals),
    path("get_all_was_referred_customers/", views.get_all_was_referred_customers),
    path("delete_notifications/", views.delete_notifications),

    #     delete momo_deposits and withdraws
    path("delete_momo_deposit_request/<int:id>/", views.delete_momo_deposit_request),
    path("delete_momo_withdraw_request/<int:id>/", views.delete_momo_withdraw_request),
    path("get_agents_unpaid_deposits/", views.get_agents_unpaid_deposits),
    path("get_agents_unpaid_cash_request_deposits/", views.get_agents_unpaid_cash_request_deposits),

    #     block listing
    path("add_to_blocked/", views.add_to_blocked),
    path("get_blocked_users/", views.get_blocked_users),
    path("remove_from_blocked/<int:id>/", views.remove_from_blocked),

    #     bank filters
    path("all_fidelity/", views.get_all_fidelity),
    path("all_cal/", views.get_all_cals),
#     users bank transactions
    path("get_agents_cal_bank/<str:username>/", views.get_agents_cal_bank),
    path("get_agents_fidelity_bank/<str:username>/", views.get_agents_fidelity_bank),
    path("get_agents_eco_bank/<str:username>/", views.get_agents_eco_bank),
    path("get_agents_access_bank/<str:username>/", views.get_agents_access_bank),
    path("get_agents_gt_bank/<str:username>/", views.get_agents_gt_bank),
    # bank transactions by date
    path("get_agents_bank_transactions_by_date/<str:username>/<str:d_month>/<str:d_year>/<str:bank>/", views.get_agents_bank_transactions_by_date),
    # path("get_agents_cal_bank_by_date/<str:username>/<str:d_month>/<str:d_year>/", views.get_agents_cal_bank_by_date),
    # path("get_agents_access_bank_by_date/<str:username>/<str:d_month>/<str:d_year>/", views.get_agents_access_bank_by_date),
    # path("get_agents_fidelity_bank_by_date/<str:username>/<str:d_month>/<str:d_year>/", views.get_agents_fidelity_bank_by_date),
    # path("get_agents_gt_bank_by_date/<str:username>/<str:d_month>/<str:d_year>/", views.get_agents_gt_bank_by_date),

#     admin update payment and request
    path("update_payment/<int:id>/", views.update_payment),
    path("update_bank_deposit/<int:id>/", views.update_bank_deposit),
    path("update_cash_requests/<int:id>/", views.update_cash_requests),

#     cash request
    path("add_cash_request/", views.post_cash_deposit),
    path("get_admin_user_cash_requests/", views.get_admin_user_cash_requests),
    path("get_admin_all_user_cash_requests/<str:username>/", views.get_admin_all_user_cash_requests),
    path("get_agent1_cash_request_all/", views.get_agent1_cash_request_all),
    path("get_agent2_cash_request_all/", views.get_agent2_cash_request_all),
    path("get_agent1_cash_requests_today/<str:username>/", views.get_agent1_cash_requests_today),
    path("get_agent2_cash_requests_today/<str:username>/", views.get_agent2_cash_requests_today),
    path("approve_cash_request/<int:id>/", views.approve_cash_request),
    path("cash_requests_detail/<int:pk>/", views.cash_requests_detail),

    path("get_all_user_cash_payments/", views.get_all_user_cash_payments),
    path("admin_add_to_approved_cash_payment/", views.admin_add_to_approved_cash_payment),
    path("get_agents_unpaid_cash_deposits/", views.get_agents_unpaid_cash_deposits),
    path('user_total_cash_payments/', views.user_total_cash_payments),
    path('get_cash_payment_approved_total/', views.get_cash_payment_approved_total),
    path('get_user_payments_cash/', views.get_user_payments_cash),
    path('make_cash_payments/', views.make_cash_payments),
    path('get_cash_payments/', views.get_cash_payments),
    path('get_all_my_cash_payments/', views.get_all_my_cash_payments),
    path('get_all_cash_payments_by_username/<str:username>/', views.get_all_cash_payments_by_username),
    path('get_all_cash_payments/', views.get_all_cash_payments),
    path('get_cash_requests_for_today/', views.get_cash_requests_for_today),

#     for collecting data

    path("get_all_customer_requests_deposits/", views.get_all_customer_requests_deposits),
    path("get_all_cash_at_payments/", views.get_all_cash_at_payments),
    path("get_all_fnet_customers/", views.get_all_fnet_customers),
    path("get_all_referred_customers/", views.get_all_referred_customers),
    path("get_all_add_to_customers_points/", views.get_all_add_to_customers_points),
    path("get_all_add_to_customers_redeemed_points/", views.get_all_add_to_customers_redeemed_points),
    path("get_all_customers_accounts_registered/", views.get_all_customers_accounts_registered),
    path("get_all_users_expenses/", views.get_all_users_expenses),
    path("get_all_users_bank_requests_deposits/", views.get_all_users_bank_requests_deposits),
    path("get_all_add_to_approved_requests_deposits/", views.get_all_add_to_approved_requests_deposits),
    path("get_all_users_mobile_money_deposit_requests_deposits/", views.get_all_users_mobile_money_deposit_requests_deposits),
    path("get_all_users_mobile_money_withdrawal_requests_deposits/", views.get_all_users_mobile_money_withdrawal_requests_deposits),
    path("get_all_users_mobile_money_accounts_started/", views.get_all_users_mobile_money_accounts_started),
    path("get_all_users_mobile_money_accounts_closed/", views.get_all_users_mobile_money_accounts_closed),
    path("get_all_customers_withdrawals/", views.get_all_customers_withdrawals),
    path("get_all_users_bank_payments/", views.get_all_users_bank_payments),
    path("get_all_added_to_approved_payments/", views.get_all_added_to_approved_payments),
    path("get_all_admin_accounts_started_with/", views.get_all_admin_accounts_started_with),
    path("get_all_admin_accounts_with_with/", views.get_all_admin_accounts_with_with),
    path("get_all_fnet_notifications/", views.get_all_fnet_notifications),
    path("get_all_users_payment_at_bank/", views.get_all_users_payment_at_bank),
    path("get_all_customers_payment_at_bank/", views.get_all_customers_payment_at_bank),
    path("get_all_users_reports/", views.get_all_users_reports),
    path("get_all_fnet_messages/", views.get_all_fnet_messages),
    path("get_all_fnet_messages_chat_id/", views.get_all_fnet_messages_chat_id),
    path("get_all_fnet_private_chat_messages/", views.get_all_fnet_private_chat_messages),
    path("get_all_users_blocked_lists/", views.get_all_users_blocked_lists),
    path("get_all_users_cash_request_deposits/", views.get_all_users_cash_request_deposits),
    path("get_all_users_cash_payments/", views.get_all_users_cash_payments),
    path("get_all_users_added_to_approved_cash_payments/", views.get_all_users_added_to_approved_cash_payments),

#     remove from database
    path("delete_all_customer_requests_deposits/", views.delete_all_customer_requests_deposits),
    path("authenticate_agent_phone/",views.authenticate_agent_phone),
    path("get_all_auth_phones/",views.get_all_auth_phones),
    path("get_all_auth_phone_agent_by_phone_id/<str:phone_id>/",views.get_all_auth_phone_agent_by_phone_id),
    path("get_auth_phone_by_username/<str:username>/",views.get_auth_phone_by_username),
    path("delete_auth_phone/<int:id>/",views.delete_auth_phone),

#     add account points
    path("add_account_points/", views.add_account_points),
    path("get_account_number_points_today/", views.get_account_number_points_today),
    path("get_account_number_points_week/", views.get_account_number_points_week),
    path("get_account_number_points_month/", views.get_account_number_points_month),
    path("get_my_account_number_points/", views.get_my_account_number_points),
    path("get_all_account_number_points/", views.get_all_account_number_points),
    path("get_user_account_points_by_username/<str:username>/", views.get_user_account_points_by_username),
]