from django.urls import path
from . import views

urlpatterns = [
    path('admin_user/', views.get_admin),
    path('twilio_details/', views.get_twilio),
    path('agent_requests/', views.get_agent_requests),
    path('request_detail/<int:pk>/', views.request_detail),
    path('agent_request_approval/<int:id>/', views.approve_request),
    path('register_customer/', views.register_customer),
    path('agent_deposit_request/', views.user_deposit_request),
    path('customer_withdrawal/', views.customer_withdrawal),
    path('all_agents/', views.GetAllAgents.as_view()),
    path('all_customers/', views.GetAllCustomers.as_view()),
    path('agent_customer_summary/', views.agent_customers_summary),
    path('agent_deposit_request_summary/', views.deposit_request_summary),
    path('agents_customers_withdrawal_summary/', views.customer_withdrawal_summary),
    path('payments/', views.get_payments),
    path('make_payments/', views.make_payments),
    path('approve_payments/<int:id>/', views.approve_payment),
    path('payment_summary/', views.payment_summary),
    path('get_agent/<str:username>/', views.get_agent),
    path('payment_detail/<int:pk>/', views.payment_detail),
    path('get_customer/<str:name>/', views.get_customer),
    path('admin_accounts_started/', views.admin_accounts_started),
    path('admin_accounts_completed/', views.admin_accounts_completed),
    path('admin_accounts_started_lists/', views.admin_accounts_started_lists),
    path('admin_accounts_started_lists/', views.admin_accounts_completed_lists),
    path('user_customers/', views.user_customers),
    path('user_transaction_requests/<str:username>/', views.user_transaction_requests),
    path('user_transaction_payments/<str:username>/', views.user_transaction_payments),
    path('user_transaction_withdrawals/<str:username>/', views.user_transaction_withdrawals),


]
