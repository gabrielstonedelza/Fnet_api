import json
from channels.generic.websocket import AsyncWebSocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs


class AdminDashboardConsumer(AsyncWebSocketConsumer):
    """
    WebSocket consumer for the admin dashboard.
    Admins connect and receive real-time updates for:
    - Transaction events (deposits, withdrawals, approvals)
    - Customer events (registrations, deletions)
    - Provider balance changes
    """

    async def connect(self):
        # Extract company_id from query string: ws://host/ws/admin/dashboard/?company_id=xxx&token=yyy
        query_params = parse_qs(self.scope["query_string"].decode())
        company_id = query_params.get("company_id", [None])[0]
        token_key = query_params.get("token", [None])[0]

        if not company_id or not token_key:
            await self.close()
            return

        # Authenticate via token
        user = await self._authenticate_token(token_key)
        if not user:
            await self.close()
            return

        # Verify user is admin+ in this company
        is_admin = await self._is_admin_or_above(user, company_id)
        if not is_admin:
            await self.close()
            return

        self.company_id = company_id
        self.group_name = f"admin_dashboard_{company_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Send initial state
        balances = await self._get_all_balances(company_id)
        await self.send(text_data=json.dumps({
            "type": "initial_state",
            "balances": balances,
        }))

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name, self.channel_name
            )

    async def receive(self, text_data):
        # Admin can request a balance refresh
        data = json.loads(text_data)
        if data.get("type") == "refresh_balances":
            balances = await self._get_all_balances(self.company_id)
            await self.send(text_data=json.dumps({
                "type": "balance_update",
                "balances": balances,
            }))

    # --- Group message handlers ---

    async def transaction_event(self, event):
        """Handle transaction broadcasts."""
        await self.send(text_data=json.dumps(event["data"]))

    async def customer_event(self, event):
        """Handle customer broadcasts."""
        await self.send(text_data=json.dumps(event["data"]))

    async def balance_event(self, event):
        """Handle provider balance broadcasts."""
        await self.send(text_data=json.dumps(event["data"]))

    # --- Database helpers ---

    @database_sync_to_async
    def _authenticate_token(self, token_key):
        from rest_framework.authtoken.models import Token
        try:
            token = Token.objects.select_related("user").get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def _is_admin_or_above(self, user, company_id):
        from accounts.models import Membership
        return Membership.objects.filter(
            user=user,
            company_id=company_id,
            role__in=["owner", "admin"],
            is_active=True,
        ).exists()

    @database_sync_to_async
    def _get_all_balances(self, company_id):
        from .models import ProviderBalance
        balances = ProviderBalance.objects.filter(
            company_id=company_id
        ).select_related("user").order_by("user__full_name", "provider")

        result = {}
        for b in balances:
            user_key = str(b.user_id)
            if user_key not in result:
                result[user_key] = {
                    "user_id": user_key,
                    "user_name": b.user.full_name,
                    "providers": {},
                }
            result[user_key]["providers"][b.provider] = {
                "balance": str(b.balance),
                "starting_balance": str(b.starting_balance),
            }
        return list(result.values())
