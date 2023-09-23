from django.urls import path
from . import views

urlpatterns = [
    path("close_accounts/",views.close_accounts),
    path("get_my_closed_accounts/",views.get_my_closed_accounts),
    path("update_account_closed_details/<int:pk>/", views.update_account_closed_details),
    path("delete_account/<int:id>/",views.delete_account),
]