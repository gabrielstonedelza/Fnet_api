from rest_framework import serializers
from .models import (
    Transaction, BankDeposit, MobileMoneyTransaction,
    CashTransaction, ExpenseRequest, DailyClosing, ProviderBalance,
)


class BankDepositDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDeposit
        fields = [
            "bank_name", "account_number", "account_name",
            "depositor_name", "slip_number", "slip_image",
        ]


class MoMoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileMoneyTransaction
        fields = [
            "network", "service_type",
            "sender_number", "receiver_number", "momo_reference",
        ]


class CashDetailSerializer(serializers.ModelSerializer):
    denomination_total = serializers.DecimalField(
        max_digits=14, decimal_places=2, read_only=True
    )

    class Meta:
        model = CashTransaction
        fields = [
            "d_200", "d_100", "d_50", "d_20", "d_10", "d_5", "d_2", "d_1",
            "denomination_total",
        ]


class TransactionSerializer(serializers.ModelSerializer):
    initiated_by_name = serializers.CharField(
        source="initiated_by.full_name", read_only=True
    )
    approved_by_name = serializers.CharField(
        source="approved_by.full_name", read_only=True, default=None
    )
    customer_name = serializers.CharField(
        source="customer.full_name", read_only=True, default=None
    )
    branch_name = serializers.CharField(
        source="branch.name", read_only=True, default=None
    )
    bank_deposit_detail = BankDepositDetailSerializer(read_only=True)
    momo_detail = MoMoDetailSerializer(read_only=True)
    cash_detail = CashDetailSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id", "reference", "company", "branch", "branch_name",
            "customer", "customer_name",
            "initiated_by", "initiated_by_name",
            "transaction_type", "channel", "status",
            "amount", "fee", "net_amount", "currency",
            "description", "internal_notes",
            "requires_approval", "approved_by", "approved_by_name",
            "approved_at", "rejection_reason",
            "reversed_transaction",
            "bank_deposit_detail", "momo_detail", "cash_detail",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "reference", "company", "initiated_by",
            "fee", "net_amount",
            "requires_approval", "approved_by", "approved_at",
            "reversed_transaction",
            "created_at", "updated_at",
        ]


class CreateBankDepositSerializer(serializers.Serializer):
    customer = serializers.UUIDField(required=False, allow_null=True)
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)
    bank_name = serializers.CharField(max_length=100)
    account_number = serializers.CharField(max_length=50)
    account_name = serializers.CharField(max_length=255)
    depositor_name = serializers.CharField(max_length=255)
    slip_number = serializers.CharField(max_length=50, required=False, allow_blank=True)


class CreateMoMoTransactionSerializer(serializers.Serializer):
    customer = serializers.UUIDField(required=False, allow_null=True)
    transaction_type = serializers.ChoiceField(
        choices=[("deposit", "Deposit"), ("withdrawal", "Withdrawal")]
    )
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)
    network = serializers.ChoiceField(choices=MobileMoneyTransaction.Network.choices)
    service_type = serializers.ChoiceField(
        choices=MobileMoneyTransaction.ServiceType.choices
    )
    sender_number = serializers.CharField(max_length=20)
    receiver_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    momo_reference = serializers.CharField(max_length=50, required=False, allow_blank=True)


class CreateCashTransactionSerializer(serializers.Serializer):
    customer = serializers.UUIDField(required=False, allow_null=True)
    transaction_type = serializers.ChoiceField(
        choices=[("deposit", "Deposit"), ("withdrawal", "Withdrawal")]
    )
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)
    d_200 = serializers.IntegerField(default=0)
    d_100 = serializers.IntegerField(default=0)
    d_50 = serializers.IntegerField(default=0)
    d_20 = serializers.IntegerField(default=0)
    d_10 = serializers.IntegerField(default=0)
    d_5 = serializers.IntegerField(default=0)
    d_2 = serializers.IntegerField(default=0)
    d_1 = serializers.IntegerField(default=0)


class ApproveTransactionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=[("approve", "Approve"), ("reject", "Reject")])
    rejection_reason = serializers.CharField(required=False, allow_blank=True)


class ReverseTransactionSerializer(serializers.Serializer):
    reason = serializers.CharField()


class ExpenseRequestSerializer(serializers.ModelSerializer):
    requested_by_name = serializers.CharField(
        source="requested_by.full_name", read_only=True
    )
    approved_by_name = serializers.CharField(
        source="approved_by.full_name", read_only=True, default=None
    )

    class Meta:
        model = ExpenseRequest
        fields = [
            "id", "company",
            "requested_by", "requested_by_name",
            "amount", "reason", "status",
            "approved_by", "approved_by_name", "approved_at",
            "rejection_reason", "receipt_image",
            "created_at",
        ]
        read_only_fields = [
            "id", "company", "requested_by", "status",
            "approved_by", "approved_at", "created_at",
        ]


class ExpenseRequestCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    reason = serializers.CharField()
    receipt_image = serializers.ImageField(required=False)


class DailyClosingSerializer(serializers.ModelSerializer):
    closed_by_name = serializers.CharField(
        source="closed_by.full_name", read_only=True
    )
    branch_name = serializers.CharField(
        source="branch.name", read_only=True, default=None
    )

    class Meta:
        model = DailyClosing
        fields = [
            "id", "company", "branch", "branch_name",
            "closed_by", "closed_by_name", "date",
            "physical_cash", "mtn_ecash", "vodafone_ecash",
            "airteltigo_ecash", "total_ecash",
            "overage", "shortage", "notes",
            "created_at",
        ]
        read_only_fields = ["id", "company", "closed_by", "created_at"]


class ProviderBalanceSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    provider_display = serializers.CharField(
        source="get_provider_display", read_only=True
    )

    class Meta:
        model = ProviderBalance
        fields = [
            "id", "company", "user", "user_name",
            "provider", "provider_display",
            "starting_balance", "balance",
            "last_updated", "created_at",
        ]
        read_only_fields = ["id", "company", "last_updated", "created_at"]


class SetProviderBalanceSerializer(serializers.Serializer):
    """Used by admins to set starting balances for a user."""
    user = serializers.UUIDField()
    provider = serializers.ChoiceField(choices=ProviderBalance.Provider.choices)
    starting_balance = serializers.DecimalField(max_digits=14, decimal_places=2)


class AdjustProviderBalanceSerializer(serializers.Serializer):
    """Used to adjust a provider balance (deposit adds, withdrawal subtracts)."""
    provider = serializers.ChoiceField(choices=ProviderBalance.Provider.choices)
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    operation = serializers.ChoiceField(choices=[("add", "Add"), ("subtract", "Subtract")])
