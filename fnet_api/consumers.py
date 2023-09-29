import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import BankDeposit
from .serializers import BankDepositSerializer

class BankDepositConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Add the WebSocket connection to a group
        await self.channel_layer.group_add("bank_deposit_group", self.channel_name)

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard("bank_deposit_group", self.channel_name)

    async def send_bank_deposits(self, event):
        # Send bank deposit data to the WebSocket
        bank_deposits = await asyncio.to_thread(BankDeposit.objects.all)
        serializer = BankDepositSerializer(bank_deposits, many=True)
        await self.send(json.dumps(serializer.data))