"""
CSV and PDF export for Merchant+ reports.

Endpoints:
  GET /api/v1/reports/export/transactions/  → CSV download
  GET /api/v1/reports/export/agents/        → CSV download
"""

import csv
import io
from datetime import date, timedelta
from decimal import Decimal

from django.http import HttpResponse
from django.db.models import Sum, Count, Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from transactions.models import Transaction
from accounts.models import Membership


@api_view(["GET"])
def export_transactions_csv(request):
    """Export transactions as CSV. Manager+ only."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin", "manager"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    company = membership.company
    date_from = request.query_params.get("date_from", str(date.today() - timedelta(days=30)))
    date_to = request.query_params.get("date_to", str(date.today()))

    qs = Transaction.objects.filter(
        company=company,
        created_at__date__gte=date_from,
        created_at__date__lte=date_to,
    ).select_related(
        "initiated_by", "customer", "branch",
        "bank_deposit_detail", "momo_detail",
    ).order_by("-created_at")

    tx_status = request.query_params.get("status")
    if tx_status:
        qs = qs.filter(status=tx_status)

    tx_type = request.query_params.get("type")
    if tx_type:
        qs = qs.filter(transaction_type=tx_type)

    channel = request.query_params.get("channel")
    if channel:
        qs = qs.filter(channel=channel)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="transactions_{date_from}_to_{date_to}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow([
        "Reference", "Date", "Type", "Channel", "Status",
        "Amount", "Fee", "Net Amount", "Currency",
        "Customer", "Initiated By", "Branch", "Description",
    ])

    for tx in qs[:5000]:
        writer.writerow([
            tx.reference,
            tx.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            tx.transaction_type,
            tx.channel,
            tx.status,
            str(tx.amount),
            str(tx.fee),
            str(tx.net_amount),
            tx.currency,
            tx.customer.full_name if tx.customer else "Walk-in",
            tx.initiated_by.full_name if tx.initiated_by else "System",
            tx.branch.name if tx.branch else "-",
            tx.description[:100],
        ])

    return response


@api_view(["GET"])
def export_agents_csv(request):
    """Export agent performance report as CSV. Manager+ only."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin", "manager"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    company = membership.company
    date_from = request.query_params.get("date_from", str(date.today() - timedelta(days=30)))
    date_to = request.query_params.get("date_to", str(date.today()))

    agents = (
        Transaction.objects.filter(
            company=company, status="completed",
            created_at__date__gte=date_from, created_at__date__lte=date_to,
        )
        .values("initiated_by__full_name", "initiated_by__email")
        .annotate(
            total_transactions=Count("id"),
            total_deposits=Count("id", filter=Q(transaction_type="deposit")),
            total_withdrawals=Count("id", filter=Q(transaction_type="withdrawal")),
            deposit_volume=Sum("amount", filter=Q(transaction_type="deposit")),
            withdrawal_volume=Sum("amount", filter=Q(transaction_type="withdrawal")),
            total_volume=Sum("amount"),
            total_fees=Sum("fee"),
        )
        .order_by("-total_volume")
    )

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="agent_performance_{date_from}_to_{date_to}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow([
        "Agent Name", "Email", "Total Transactions",
        "Deposits", "Withdrawals", "Deposit Volume (GHS)",
        "Withdrawal Volume (GHS)", "Total Volume (GHS)", "Fees Generated (GHS)",
    ])

    for a in agents:
        writer.writerow([
            a["initiated_by__full_name"],
            a["initiated_by__email"],
            a["total_transactions"],
            a["total_deposits"],
            a["total_withdrawals"],
            str(a["deposit_volume"] or 0),
            str(a["withdrawal_volume"] or 0),
            str(a["total_volume"] or 0),
            str(a["total_fees"] or 0),
        ])

    return response
