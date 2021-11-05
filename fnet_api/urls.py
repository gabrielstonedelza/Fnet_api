from django.urls import path
from . import views

urlpatterns = [
    path('twilio_details/', views.get_twilio),
    path('agent_requests/', views.get_agent_requests),
    path('agent_request_approval/<int:id>/', views.approve_request),
    path('register_customer/<str:username>/', views.register_customer),
    path('agent_deposit_request/<str:username>/', views.agent_deposit_request),
    path('customer_withdrawal/<str:username>/', views.customer_withdrawal),
    path('all_agents/', views.get_all_agents),
    path('all_customers/', views.get_all_customers),
    path('agent_customer_summary/<str:username>/', views.agent_customers_summary),
    path('agent_deposit_request_summary/<str:username>/', views.deposit_request_summary),
    path('agents_customers_withdrawal_summary/<str:username>/', views.customer_withdrawal_summary),
    path('payments/', views.get_payments),
    path('make_payments/<str:username>/', views.make_payments),
    path('approve_payments/<int:id>/', views.approve_payment),
    path('payment_summary/<str:username>/', views.payment_summary)

]
