"""
SMS notification service for Merchant+.

Supports two Ghanaian SMS gateways:
  - Hubtel (primary)
  - Arkesel (fallback)

Used for:
  - Transaction alerts (large amounts, approvals)
  - 2FA codes (if SMS-based OTP is added later)
  - Security alerts (new login, password change)
  - Account notifications

Configuration via environment variables:
  SMS_PROVIDER=hubtel|arkesel
  SMS_API_KEY=your-api-key
  SMS_API_SECRET=your-api-secret  (Hubtel only)
  SMS_SENDER_ID=MerchantPlus
"""

import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def get_sms_config():
    """Get SMS configuration from Django settings."""
    return {
        "provider": getattr(settings, "SMS_PROVIDER", "hubtel"),
        "api_key": getattr(settings, "SMS_API_KEY", ""),
        "api_secret": getattr(settings, "SMS_API_SECRET", ""),
        "sender_id": getattr(settings, "SMS_SENDER_ID", "MerchantPlus"),
    }


def format_phone(phone: str) -> str:
    """
    Normalize a Ghanaian phone number to international format.
    Converts 0XX XXXX XXX → 233XX XXXX XXX
    """
    phone = phone.strip().replace(" ", "").replace("-", "")
    if phone.startswith("+"):
        phone = phone[1:]
    if phone.startswith("0"):
        phone = "233" + phone[1:]
    if not phone.startswith("233"):
        phone = "233" + phone
    return phone


def send_sms(to: str, message: str) -> bool:
    """
    Send an SMS via the configured provider.
    Returns True on success, False on failure.
    """
    config = get_sms_config()

    if not config["api_key"]:
        logger.warning("SMS not configured — SMS_API_KEY is empty. Message not sent to %s", to)
        return False

    to = format_phone(to)
    provider = config["provider"].lower()

    if provider == "arkesel":
        return _send_arkesel(to, message, config)
    else:
        return _send_hubtel(to, message, config)


def _send_hubtel(to: str, message: str, config: dict) -> bool:
    """
    Send SMS via Hubtel Programmable SMS API.
    Docs: https://developers.hubtel.com/docs/sms
    """
    url = "https://smsc.hubtel.com/v1/messages/send"

    try:
        resp = requests.get(
            url,
            params={
                "clientid": config["api_key"],
                "clientsecret": config["api_secret"],
                "from": config["sender_id"],
                "to": to,
                "content": message,
            },
            timeout=15,
        )

        if resp.status_code == 200 or resp.status_code == 201:
            logger.info("SMS sent via Hubtel to %s", to)
            return True
        else:
            logger.error(
                "Hubtel SMS failed: status=%s body=%s",
                resp.status_code,
                resp.text[:200],
            )
            return False
    except requests.RequestException as e:
        logger.error("Hubtel SMS request error: %s", e)
        return False


def _send_arkesel(to: str, message: str, config: dict) -> bool:
    """
    Send SMS via Arkesel SMS API.
    Docs: https://developers.arkesel.com/
    """
    url = "https://sms.arkesel.com/api/v2/sms/send"

    try:
        resp = requests.post(
            url,
            headers={
                "api-key": config["api_key"],
                "Content-Type": "application/json",
            },
            json={
                "sender": config["sender_id"],
                "message": message,
                "recipients": [to],
            },
            timeout=15,
        )

        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                logger.info("SMS sent via Arkesel to %s", to)
                return True
            else:
                logger.error("Arkesel SMS error: %s", data)
                return False
        else:
            logger.error(
                "Arkesel SMS failed: status=%s body=%s",
                resp.status_code,
                resp.text[:200],
            )
            return False
    except requests.RequestException as e:
        logger.error("Arkesel SMS request error: %s", e)
        return False


# -------------------------------------------------------------------------
# Pre-built notification messages
# -------------------------------------------------------------------------

def send_transaction_sms(phone: str, tx_data: dict) -> bool:
    """Notify about a transaction via SMS."""
    msg = (
        f"Merchant+ Alert\n"
        f"Ref: {tx_data['reference']}\n"
        f"Type: {tx_data['type']}\n"
        f"Amount: {tx_data['currency']} {tx_data['amount']}\n"
        f"Status: {tx_data['status']}"
    )
    return send_sms(phone, msg)


def send_security_sms(phone: str, event: str) -> bool:
    """Send a security alert SMS (password change, new login, etc)."""
    msg = (
        f"Merchant+ Security Alert\n"
        f"{event}\n"
        f"If this wasn't you, contact support immediately."
    )
    return send_sms(phone, msg)


def send_approval_sms(phone: str, reference: str, amount: str) -> bool:
    """Notify a manager that a transaction needs approval."""
    msg = (
        f"Merchant+ Approval Required\n"
        f"Transaction {reference} for GHS {amount} needs your approval. "
        f"Log in to your dashboard to review."
    )
    return send_sms(phone, msg)


def send_welcome_sms(phone: str, company_name: str) -> bool:
    """Welcome SMS for new team members."""
    msg = (
        f"Welcome to {company_name} on Merchant+! "
        f"Download the app or visit your dashboard to get started."
    )
    return send_sms(phone, msg)


def send_otp_sms(phone: str, code: str) -> bool:
    """Send a one-time verification code via SMS."""
    msg = f"Your Merchant+ verification code is: {code}. Valid for 5 minutes. Do not share this code."
    return send_sms(phone, msg)
