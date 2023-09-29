from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/new_bank_deposit/", consumers.BankDepositConsumer.as_asgi()),
]