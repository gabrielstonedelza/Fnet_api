from django.urls import path
from . import views

urlpatterns = [
    #     post at bank
    path("post_at_bank/", views.post_at_bank),
    path("get_all_data_at_bank/", views.get_all_data_at_bank),
]