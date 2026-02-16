"""
Utility to broadcast real-time events to admin dashboard WebSocket consumers.
"""

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def broadcast_to_company(company_id, event_type, data):
    """
    Send a message to all connected admin dashboards for a company.

    Args:
        company_id: The company UUID (will be stringified)
        event_type: One of 'transaction_event', 'customer_event', 'balance_event'
        data: Dict payload to send to the frontend
    """
    channel_layer = get_channel_layer()
    group_name = f"admin_dashboard_{company_id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": event_type,
            "data": data,
        },
    )
