from django.contrib import admin
from .models import (
    Transaction, BankDeposit, MobileMoneyTransaction,
    CashTransaction, ExpenseRequest, DailyClosing,
)


class BankDepositInline(admin.StackedInline):
    model = BankDeposit
    extra = 0


class MoMoInline(admin.StackedInline):
    model = MobileMoneyTransaction
    extra = 0


class CashInline(admin.StackedInline):
    model = CashTransaction
    extra = 0


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "reference", "transaction_type", "channel", "status",
        "amount", "fee", "currency", "company",
        "initiated_by", "created_at",
    ]
    list_filter = ["transaction_type", "channel", "status", "company"]
    search_fields = ["reference", "description"]
    raw_id_fields = ["company", "branch", "customer", "initiated_by", "approved_by"]
    readonly_fields = ["id", "reference", "created_at", "updated_at"]
    inlines = [BankDepositInline, MoMoInline, CashInline]


@admin.register(ExpenseRequest)
class ExpenseRequestAdmin(admin.ModelAdmin):
    list_display = ["requested_by", "amount", "status", "company", "created_at"]
    list_filter = ["status", "company"]
    search_fields = ["reason", "requested_by__full_name"]


@admin.register(DailyClosing)
class DailyClosingAdmin(admin.ModelAdmin):
    list_display = [
        "date", "closed_by", "company", "branch",
        "physical_cash", "total_ecash", "overage", "shortage",
    ]
    list_filter = ["company", "branch"]
    search_fields = ["closed_by__full_name"]
