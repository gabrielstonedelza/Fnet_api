from django.urls import path
from . import views

urlpatterns = [
    path("close_accounts/",views.close_accounts),
    path("get_my_closed_accounts/",views.get_my_closed_accounts),
    path("update_my_accounts_detail/<int:pk>/",views.update_my_accounts_detail),
    path("delete_account/<int:id>/",views.delete_account),
]