from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum, Count, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from transactions.models import Transaction, ExpenseRequest
from transactions.serializers import TransactionSerializer
from customers.models import Customer
from accounts.models import Membership
from .models import SavedReport
from .serializers import SavedReportSerializer


# ---------------------------------------------------------------------------
# Dashboard Summary
# ---------------------------------------------------------------------------
@api_view(["GET"])
def dashboard(request):
    """Main dashboard endpoint for company owners/admins."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin", "manager"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    company = membership.company
    today = timezone.now().date()

    today_txns = Transaction.objects.filter(company=company, created_at__date=today)

    total_transactions_today = today_txns.count()

    deposits_today = today_txns.filter(
        transaction_type="deposit", status="completed"
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

    withdrawals_today = today_txns.filter(
        transaction_type="withdrawal", status="completed"
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

    fees_today = today_txns.filter(
        status="completed"
    ).aggregate(total=Sum("fee"))["total"] or Decimal("0")

    pending_approvals = Transaction.objects.filter(
        company=company, requires_approval=True, status="pending"
    ).count()

    total_customers = Customer.objects.filter(company=company, status="active").count()
    total_active_users = Membership.objects.filter(company=company, is_active=True).count()

    by_channel = {}
    for row in today_txns.values("channel").annotate(count=Count("id")):
        by_channel[row["channel"]] = row["count"]

    by_status = {}
    for row in today_txns.values("status").annotate(count=Count("id")):
        by_status[row["status"]] = row["count"]

    recent = Transaction.objects.filter(
        company=company
    ).select_related("initiated_by", "customer", "branch").order_by("-created_at")[:10]

    first_of_month = today.replace(day=1)
    top_agents_qs = (
        Transaction.objects.filter(
            company=company, created_at__date__gte=first_of_month, status="completed",
        )
        .values("initiated_by__full_name", "initiated_by__id")
        .annotate(transaction_count=Count("id"), total_volume=Sum("amount"))
        .order_by("-total_volume")[:10]
    )
    top_agents = [
        {
            "user_id": str(row["initiated_by__id"]),
            "name": row["initiated_by__full_name"],
            "transaction_count": row["transaction_count"],
            "total_volume": str(row["total_volume"] or 0),
        }
        for row in top_agents_qs
    ]

    return Response({
        "total_transactions_today": total_transactions_today,
        "total_deposits_today": str(deposits_today),
        "total_withdrawals_today": str(withdrawals_today),
        "total_fees_today": str(fees_today),
        "pending_approvals": pending_approvals,
        "total_customers": total_customers,
        "total_active_users": total_active_users,
        "transactions_by_channel": by_channel,
        "transactions_by_status": by_status,
        "recent_transactions": TransactionSerializer(recent, many=True).data,
        "top_agents": top_agents,
    })


# ---------------------------------------------------------------------------
# Transaction Summary Report
# ---------------------------------------------------------------------------
@api_view(["GET"])
def transaction_summary(request):
    """Aggregated transaction report with filters."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin", "manager"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    company = membership.company
    qs = Transaction.objects.filter(company=company, status="completed")

    date_from = request.query_params.get("date_from", str(date.today() - timedelta(days=30)))
    date_to = request.query_params.get("date_to", str(date.today()))
    qs = qs.filter(created_at__date__gte=date_from, created_at__date__lte=date_to)

    branch = request.query_params.get("branch")
    if branch:
        qs = qs.filter(branch_id=branch)

    channel = request.query_params.get("channel")
    if channel:
        qs = qs.filter(channel=channel)

    tx_type = request.query_params.get("type")
    if tx_type:
        qs = qs.filter(transaction_type=tx_type)

    totals = qs.aggregate(
        total_count=Count("id"), total_amount=Sum("amount"),
        total_fees=Sum("fee"), total_net=Sum("net_amount"),
    )

    by_type = list(qs.values("transaction_type").annotate(
        count=Count("id"), total=Sum("amount"), fees=Sum("fee"),
    ))

    by_channel = list(qs.values("channel").annotate(
        count=Count("id"), total=Sum("amount"),
    ))

    daily = list(
        qs.values("created_at__date")
        .annotate(count=Count("id"), total=Sum("amount"))
        .order_by("created_at__date")
    )
    daily_trend = [
        {"date": str(row["created_at__date"]), "count": row["count"], "total": str(row["total"] or 0)}
        for row in daily
    ]

    return Response({
        "period": {"from": date_from, "to": date_to},
        "totals": {
            "count": totals["total_count"],
            "amount": str(totals["total_amount"] or 0),
            "fees": str(totals["total_fees"] or 0),
            "net": str(totals["total_net"] or 0),
        },
        "by_type": by_type,
        "by_channel": by_channel,
        "daily_trend": daily_trend,
    })


# ---------------------------------------------------------------------------
# Agent Performance Report
# ---------------------------------------------------------------------------
@api_view(["GET"])
def agent_performance(request):
    """Report on each agent's transaction volume and count."""
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
        .values("initiated_by__id", "initiated_by__full_name", "initiated_by__email")
        .annotate(
            total_transactions=Count("id"),
            total_deposits=Count("id", filter=Q(transaction_type="deposit")),
            total_withdrawals=Count("id", filter=Q(transaction_type="withdrawal")),
            deposit_volume=Sum("amount", filter=Q(transaction_type="deposit")),
            withdrawal_volume=Sum("amount", filter=Q(transaction_type="withdrawal")),
            total_volume=Sum("amount"),
            total_fees_generated=Sum("fee"),
        )
        .order_by("-total_volume")
    )

    result = [
        {
            "user_id": str(a["initiated_by__id"]),
            "name": a["initiated_by__full_name"],
            "email": a["initiated_by__email"],
            "total_transactions": a["total_transactions"],
            "total_deposits": a["total_deposits"],
            "total_withdrawals": a["total_withdrawals"],
            "deposit_volume": str(a["deposit_volume"] or 0),
            "withdrawal_volume": str(a["withdrawal_volume"] or 0),
            "total_volume": str(a["total_volume"] or 0),
            "total_fees_generated": str(a["total_fees_generated"] or 0),
        }
        for a in agents
    ]

    return Response({"period": {"from": date_from, "to": date_to}, "agents": result})


# ---------------------------------------------------------------------------
# Revenue Report
# ---------------------------------------------------------------------------
@api_view(["GET"])
def revenue_report(request):
    """Revenue from fees and commissions."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    company = membership.company
    date_from = request.query_params.get("date_from", str(date.today() - timedelta(days=30)))
    date_to = request.query_params.get("date_to", str(date.today()))

    qs = Transaction.objects.filter(
        company=company, status="completed",
        created_at__date__gte=date_from, created_at__date__lte=date_to,
    )

    total_fees = qs.aggregate(total=Sum("fee"))["total"] or Decimal("0")
    fees_by_channel = list(qs.values("channel").annotate(fees=Sum("fee")).order_by("-fees"))
    fees_by_type = list(qs.values("transaction_type").annotate(fees=Sum("fee")).order_by("-fees"))

    daily = list(
        qs.values("created_at__date").annotate(fees=Sum("fee")).order_by("created_at__date")
    )
    daily_trend = [
        {"date": str(row["created_at__date"]), "fees": str(row["fees"] or 0)}
        for row in daily
    ]

    expenses = ExpenseRequest.objects.filter(
        company=company, status__in=["approved", "paid"],
        created_at__date__gte=date_from, created_at__date__lte=date_to,
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

    return Response({
        "period": {"from": date_from, "to": date_to},
        "total_fees": str(total_fees),
        "total_expenses": str(expenses),
        "net_revenue": str(total_fees - expenses),
        "fees_by_channel": fees_by_channel,
        "fees_by_type": fees_by_type,
        "daily_trend": daily_trend,
    })


# ---------------------------------------------------------------------------
# Saved Reports
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def saved_reports(request):
    """List or create saved report configurations."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin", "manager"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        qs = SavedReport.objects.filter(company=membership.company)
        return Response(SavedReportSerializer(qs, many=True).data)

    serializer = SavedReportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(company=membership.company, created_by=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_saved_report(request, report_id):
    """Delete a saved report."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        report = SavedReport.objects.get(id=report_id, company=membership.company)
    except SavedReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if report.created_by != request.user and membership.role not in ("owner", "admin"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    report.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
