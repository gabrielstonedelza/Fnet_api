from rest_framework import serializers
from .models import Customer, CustomerAccount


class CustomerSerializer(serializers.ModelSerializer):
    registered_by_name = serializers.CharField(
        source="registered_by.full_name", read_only=True
    )
    branch_name = serializers.CharField(
        source="branch.name", read_only=True, default=None
    )
    account_count = serializers.SerializerMethodField()
    transaction_count = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            "id", "company", "registered_by", "registered_by_name",
            "branch", "branch_name",
            "full_name", "phone", "email", "date_of_birth",
            "address", "city", "digital_address", "photo",
            "id_type", "id_number", "id_document_front", "id_document_back",
            "kyc_status", "kyc_verified_at",
            "status", "loyalty_points",
            "referred_by", "notes",
            "account_count", "transaction_count",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "company", "registered_by",
            "kyc_status", "kyc_verified_at",
            "loyalty_points", "created_at", "updated_at",
        ]

    def get_account_count(self, obj):
        return obj.accounts.count()

    def get_transaction_count(self, obj):
        return obj.transactions.count() if hasattr(obj, "transactions") else 0


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "full_name", "phone", "email", "date_of_birth",
            "address", "city", "digital_address", "photo",
            "id_type", "id_number", "id_document_front", "id_document_back",
            "branch", "referred_by", "notes",
        ]


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "full_name", "phone", "email", "date_of_birth",
            "address", "city", "digital_address", "photo",
            "id_type", "id_number", "id_document_front", "id_document_back",
            "notes", "status",
        ]


class CustomerAccountSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source="customer.full_name", read_only=True
    )

    class Meta:
        model = CustomerAccount
        fields = [
            "id", "customer", "customer_name",
            "account_type", "account_number", "account_name",
            "bank_or_network", "is_primary", "is_verified",
            "created_at",
        ]
        read_only_fields = ["id", "company", "is_verified", "created_at"]


class CustomerKYCSerializer(serializers.Serializer):
    kyc_status = serializers.ChoiceField(choices=Customer.KYCStatus.choices)
