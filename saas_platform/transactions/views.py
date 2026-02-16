from decimal import Decimal
from django.utils import timezone
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    Transaction, BankDeposit, MobileMoneyTransaction,
    CashTransaction, ExpenseRequest, DailyClosing, ProviderBalance,
)
from .serializers import (
    TransactionSerializer,
    CreateBankDepositSerializer,
    CreateMoMoTransactionSerializer,
    CreateCashTransactionSerializer,
    ApproveTransactionSerializer,
    ReverseTransactionSerializer,
    ExpenseRequestSerializer,
    ExpenseRequestCreateSerializer,
    DailyClosingSerializer,
    ProviderBalanceSerializer,
    SetProviderBalanceSerializer,
    AdjustProviderBalanceSerializer,
)


def _calculate_fee(company, transaction_type, amount):
    settings = getattr(company, "settings", None)
    if not settings:
        return Decimal("0")
    if transaction_type == "deposit":
        return (settings.deposit_fee_percentage / 100) * amount
    elif transaction_type == "withdrawal":
        return (settings.withdrawal_fee_percentage / 100) * amount
    elif transaction_type == "transfer":
        return settings.transfer_fee_flat
    return Decimal("0")


def _needs_approval(company, amount):
    settings = getattr(company, "settings", None)
    if not settings:
        return False
    return amount >= settings.require_approval_above


# ---------------------------------------------------------------------------
# Transaction List
# ---------------------------------------------------------------------------
@api_view(["GET"])
def transactions(request):
    """List transactions. Supports filtering by status, type, channel, customer, date range."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    qs = Transaction.objects.filter(
        company=membership.company
    ).select_related(
        "initiated_by", "approved_by", "customer", "branch",
        "bank_deposit_detail", "momo_detail", "cash_detail",
    )

    if membership.role == "teller":
        qs = qs.filter(initiated_by=request.user)

    tx_status = request.query_params.get("status")
    if tx_status:
        qs = qs.filter(status=tx_status)

    tx_type = request.query_params.get("type")
    if tx_type:
        qs = qs.filter(transaction_type=tx_type)

    channel = request.query_params.get("channel")
    if channel:
        qs = qs.filter(channel=channel)

    customer_id = request.query_params.get("customer")
    if customer_id:
        qs = qs.filter(customer_id=customer_id)

    branch_id = request.query_params.get("branch")
    if branch_id:
        qs = qs.filter(branch_id=branch_id)

    date_from = request.query_params.get("date_from")
    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)

    date_to = request.query_params.get("date_to")
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)

    search = request.query_params.get("search")
    if search:
        qs = qs.filter(Q(reference__icontains=search) | Q(description__icontains=search))

    return Response(TransactionSerializer(qs[:200], many=True).data)


@api_view(["GET"])
def transaction_detail(request, transaction_id):
    """Get a single transaction with full details."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        tx = Transaction.objects.select_related(
            "initiated_by", "approved_by", "customer", "branch",
            "bank_deposit_detail", "momo_detail", "cash_detail",
        ).get(id=transaction_id, company=membership.company)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if membership.role == "teller" and tx.initiated_by != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    return Response(TransactionSerializer(tx).data)


# ---------------------------------------------------------------------------
# Create Transactions
# ---------------------------------------------------------------------------
@api_view(["POST"])
def create_bank_deposit(request):
    """Create a bank deposit transaction."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = CreateBankDepositSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    company = membership.company
    amount = Decimal(str(data["amount"]))
    fee = _calculate_fee(company, "deposit", amount)
    requires_approval = _needs_approval(company, amount)

    tx = Transaction.objects.create(
        company=company, branch=membership.branch,
        customer_id=data.get("customer"), initiated_by=request.user,
        transaction_type=Transaction.Type.DEPOSIT,
        channel=Transaction.Channel.BANK,
        status=Transaction.Status.PENDING if requires_approval else Transaction.Status.COMPLETED,
        amount=amount, fee=fee, net_amount=amount - fee,
        description=data.get("description", ""),
        requires_approval=requires_approval,
    )
    BankDeposit.objects.create(
        transaction=tx, bank_name=data["bank_name"],
        account_number=data["account_number"], account_name=data["account_name"],
        depositor_name=data["depositor_name"],
        slip_number=data.get("slip_number", ""),
    )
    return Response(TransactionSerializer(tx).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def create_momo_transaction(request):
    """Create a mobile money deposit or withdrawal."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if not membership.company.subscription_plan.has_mobile_money:
        return Response(
            {"error": "Mobile money is not available on your plan."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = CreateMoMoTransactionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    company = membership.company
    tx_type = data["transaction_type"]
    amount = Decimal(str(data["amount"]))
    fee = _calculate_fee(company, tx_type, amount)
    requires_approval = _needs_approval(company, amount)

    tx = Transaction.objects.create(
        company=company, branch=membership.branch,
        customer_id=data.get("customer"), initiated_by=request.user,
        transaction_type=tx_type, channel=Transaction.Channel.MOBILE_MONEY,
        status=Transaction.Status.PENDING if requires_approval else Transaction.Status.COMPLETED,
        amount=amount, fee=fee, net_amount=amount - fee,
        description=data.get("description", ""),
        requires_approval=requires_approval,
    )
    MobileMoneyTransaction.objects.create(
        transaction=tx, network=data["network"],
        service_type=data["service_type"],
        sender_number=data["sender_number"],
        receiver_number=data.get("receiver_number", ""),
        momo_reference=data.get("momo_reference", ""),
    )
    return Response(TransactionSerializer(tx).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def create_cash_transaction(request):
    """Create a cash deposit or withdrawal."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = CreateCashTransactionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    company = membership.company
    tx_type = data["transaction_type"]
    amount = Decimal(str(data["amount"]))
    fee = _calculate_fee(company, tx_type, amount)
    requires_approval = _needs_approval(company, amount)

    tx = Transaction.objects.create(
        company=company, branch=membership.branch,
        customer_id=data.get("customer"), initiated_by=request.user,
        transaction_type=tx_type, channel=Transaction.Channel.CASH,
        status=Transaction.Status.PENDING if requires_approval else Transaction.Status.COMPLETED,
        amount=amount, fee=fee, net_amount=amount - fee,
        description=data.get("description", ""),
        requires_approval=requires_approval,
    )
    CashTransaction.objects.create(
        transaction=tx,
        d_200=data.get("d_200", 0), d_100=data.get("d_100", 0),
        d_50=data.get("d_50", 0), d_20=data.get("d_20", 0),
        d_10=data.get("d_10", 0), d_5=data.get("d_5", 0),
        d_2=data.get("d_2", 0), d_1=data.get("d_1", 0),
    )
    return Response(TransactionSerializer(tx).data, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------------------------
# Approval Workflow
# ---------------------------------------------------------------------------
@api_view(["GET"])
def pending_approvals(request):
    """List transactions pending approval. Manager+ only."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin", "manager"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    qs = Transaction.objects.filter(
        company=membership.company, requires_approval=True,
        status=Transaction.Status.PENDING,
    ).select_related(
        "initiated_by", "customer", "branch",
        "bank_deposit_detail", "momo_detail", "cash_detail",
    )
    return Response(TransactionSerializer(qs, many=True).data)


@api_view(["POST"])
def approve_transaction(request, transaction_id):
    """Approve or reject a pending transaction. Manager+ only."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin", "manager"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        tx = Transaction.objects.get(
            id=transaction_id, company=membership.company,
            status=Transaction.Status.PENDING,
        )
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if tx.initiated_by == request.user:
        return Response(
            {"error": "Cannot approve your own transaction."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = ApproveTransactionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    action = serializer.validated_data["action"]

    if action == "approve":
        tx.status = Transaction.Status.COMPLETED
    else:
        tx.status = Transaction.Status.REJECTED
        tx.rejection_reason = serializer.validated_data.get("rejection_reason", "")

    tx.approved_by = request.user
    tx.approved_at = timezone.now()
    tx.save()
    return Response(TransactionSerializer(tx).data)


# ---------------------------------------------------------------------------
# Reversal
# ---------------------------------------------------------------------------
@api_view(["POST"])
def reverse_transaction(request, transaction_id):
    """Reverse a completed transaction. Admin+ only."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        tx = Transaction.objects.get(
            id=transaction_id, company=membership.company,
            status=Transaction.Status.COMPLETED,
        )
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ReverseTransactionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    reversal = Transaction.objects.create(
        company=tx.company, branch=tx.branch, customer=tx.customer,
        initiated_by=request.user,
        transaction_type=Transaction.Type.REVERSAL,
        channel=tx.channel, status=Transaction.Status.COMPLETED,
        amount=tx.amount, fee=Decimal("0"), net_amount=tx.amount,
        description=f"Reversal of {tx.reference}: {serializer.validated_data['reason']}",
        reversed_transaction=tx,
    )
    tx.status = Transaction.Status.REVERSED
    tx.save(update_fields=["status"])
    return Response(TransactionSerializer(reversal).data, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------------------------
# Expense Requests
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def expense_requests(request):
    """List or create expense requests."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        qs = ExpenseRequest.objects.filter(company=membership.company)
        if membership.role == "teller":
            qs = qs.filter(requested_by=request.user)
        return Response(ExpenseRequestSerializer(qs, many=True).data)

    serializer = ExpenseRequestCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    expense = ExpenseRequest.objects.create(
        company=membership.company, requested_by=request.user,
        amount=serializer.validated_data["amount"],
        reason=serializer.validated_data["reason"],
        receipt_image=serializer.validated_data.get("receipt_image"),
    )
    return Response(ExpenseRequestSerializer(expense).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def approve_expense(request, expense_id):
    """Approve or reject an expense. Manager+ only."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin", "manager"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        expense = ExpenseRequest.objects.get(
            id=expense_id, company=membership.company,
            status=ExpenseRequest.Status.PENDING,
        )
    except ExpenseRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    action = request.data.get("action")
    if action == "approve":
        expense.status = ExpenseRequest.Status.APPROVED
    elif action == "reject":
        expense.status = ExpenseRequest.Status.REJECTED
        expense.rejection_reason = request.data.get("rejection_reason", "")
    else:
        return Response(
            {"error": "Action must be 'approve' or 'reject'."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    expense.approved_by = request.user
    expense.approved_at = timezone.now()
    expense.save()
    return Response(ExpenseRequestSerializer(expense).data)


# ---------------------------------------------------------------------------
# Daily Closing
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def daily_closings(request):
    """List or create daily closings."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        qs = DailyClosing.objects.filter(company=membership.company)
        if membership.role == "teller":
            qs = qs.filter(closed_by=request.user)
        date_filter = request.query_params.get("date")
        if date_filter:
            qs = qs.filter(date=date_filter)
        return Response(DailyClosingSerializer(qs, many=True).data)

    serializer = DailyClosingSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(
        company=membership.company, closed_by=request.user,
        branch=membership.branch,
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH"])
def daily_closing_detail(request, closing_id):
    """Get or update a daily closing."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        closing = DailyClosing.objects.get(id=closing_id, company=membership.company)
    except DailyClosing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(DailyClosingSerializer(closing).data)

    if closing.closed_by != request.user and membership.role not in ("owner", "admin"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = DailyClosingSerializer(closing, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# ---------------------------------------------------------------------------
# Provider Balances
# ---------------------------------------------------------------------------
@api_view(["GET"])
def provider_balances(request):
    """List all provider balances for the company. Admin+ can see all users."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    qs = ProviderBalance.objects.filter(
        company=membership.company
    ).select_related("user")

    # Non-admins only see their own balances
    if membership.role not in ("owner", "admin"):
        qs = qs.filter(user=request.user)

    user_filter = request.query_params.get("user")
    if user_filter:
        qs = qs.filter(user_id=user_filter)

    provider_filter = request.query_params.get("provider")
    if provider_filter:
        qs = qs.filter(provider=provider_filter)

    return Response(ProviderBalanceSerializer(qs, many=True).data)


@api_view(["POST"])
def set_provider_balance(request):
    """Set starting balance for a user's provider. Admin+ only."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = SetProviderBalanceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    balance, created = ProviderBalance.objects.update_or_create(
        company=membership.company,
        user_id=data["user"],
        provider=data["provider"],
        defaults={
            "starting_balance": data["starting_balance"],
            "balance": data["starting_balance"],
        },
    )
    return Response(
        ProviderBalanceSerializer(balance).data,
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
    )


@api_view(["POST"])
def initialize_all_balances(request):
    """
    Set starting balances for ALL providers at once for a user. Admin+ only.
    Expects: { "user": "<uuid>", "balances": { "mtn": 1000, "vodafone": 500, ... } }
    """
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    user_id = request.data.get("user")
    balances = request.data.get("balances", {})
    if not user_id or not balances:
        return Response(
            {"error": "Provide 'user' and 'balances' fields."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    valid_providers = dict(ProviderBalance.Provider.choices)
    results = []
    for provider, amount in balances.items():
        if provider not in valid_providers:
            continue
        balance, _ = ProviderBalance.objects.update_or_create(
            company=membership.company,
            user_id=user_id,
            provider=provider,
            defaults={
                "starting_balance": Decimal(str(amount)),
                "balance": Decimal(str(amount)),
            },
        )
        results.append(balance)

    return Response(ProviderBalanceSerializer(results, many=True).data)


@api_view(["POST"])
def adjust_provider_balance(request):
    """
    Adjust a provider balance (add or subtract). Used when processing transactions.
    """
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = AdjustProviderBalanceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    try:
        balance = ProviderBalance.objects.get(
            company=membership.company,
            user=request.user,
            provider=data["provider"],
        )
    except ProviderBalance.DoesNotExist:
        return Response(
            {"error": f"No balance record found for provider '{data['provider']}'."},
            status=status.HTTP_404_NOT_FOUND,
        )

    amount = data["amount"]
    if data["operation"] == "add":
        balance.balance += amount
    else:
        if balance.balance < amount:
            return Response(
                {"error": "Insufficient balance."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance.balance -= amount

    balance.save()
    return Response(ProviderBalanceSerializer(balance).data)
