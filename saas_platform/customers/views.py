from django.db import models
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Customer, CustomerAccount
from .serializers import (
    CustomerSerializer,
    CustomerCreateSerializer,
    CustomerUpdateSerializer,
    CustomerAccountSerializer,
    CustomerKYCSerializer,
)


# ---------------------------------------------------------------------------
# Customer CRUD
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def customers(request):
    """List or register customers for the current company."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    company = membership.company

    if request.method == "GET":
        qs = Customer.objects.filter(company=company).select_related(
            "registered_by", "branch"
        )

        status_filter = request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)

        branch_filter = request.query_params.get("branch")
        if branch_filter:
            qs = qs.filter(branch_id=branch_filter)

        kyc_filter = request.query_params.get("kyc_status")
        if kyc_filter:
            qs = qs.filter(kyc_status=kyc_filter)

        search = request.query_params.get("search")
        if search:
            qs = qs.filter(
                models.Q(full_name__icontains=search)
                | models.Q(phone__icontains=search)
            )

        return Response(CustomerSerializer(qs, many=True).data)

    # POST - register new customer
    plan = company.subscription_plan
    current_count = Customer.objects.filter(company=company).count()
    if plan.max_customers and current_count >= plan.max_customers:
        return Response(
            {"error": f"Customer limit reached ({plan.max_customers}). Upgrade your plan."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = CustomerCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if Customer.objects.filter(
        company=company, phone=serializer.validated_data["phone"]
    ).exists():
        return Response(
            {"error": "A customer with this phone number already exists in your company."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    customer = serializer.save(
        company=company,
        registered_by=request.user,
        branch=membership.branch,
    )

    return Response(
        CustomerSerializer(customer).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "PATCH", "DELETE"])
def customer_detail(request, customer_id):
    """Retrieve, update, or delete a customer."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        customer = Customer.objects.get(id=customer_id, company=membership.company)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(CustomerSerializer(customer).data)

    if request.method == "PATCH":
        serializer = CustomerUpdateSerializer(
            customer, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CustomerSerializer(customer).data)

    if request.method == "DELETE":
        if membership.role not in ("owner", "admin"):
            return Response(
                {"error": "Only owners and admins can delete customers."},
                status=status.HTTP_403_FORBIDDEN,
            )
        customer.status = Customer.Status.INACTIVE
        customer.save(update_fields=["status"])
        return Response({"message": "Customer deactivated."})


@api_view(["GET"])
def customer_by_phone(request):
    """Look up a customer by phone number."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    phone = request.query_params.get("phone")
    if not phone:
        return Response(
            {"error": "Phone parameter is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        customer = Customer.objects.get(company=membership.company, phone=phone)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(CustomerSerializer(customer).data)


# ---------------------------------------------------------------------------
# KYC Verification
# ---------------------------------------------------------------------------
@api_view(["POST"])
def verify_kyc(request, customer_id):
    """Approve or reject a customer's KYC. Manager+ only."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin", "manager"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        customer = Customer.objects.get(id=customer_id, company=membership.company)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerKYCSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    customer.kyc_status = serializer.validated_data["kyc_status"]
    if customer.kyc_status == Customer.KYCStatus.VERIFIED:
        customer.kyc_verified_at = timezone.now()
        customer.kyc_verified_by = request.user
    customer.save()

    return Response(CustomerSerializer(customer).data)


# ---------------------------------------------------------------------------
# Customer Accounts
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def customer_accounts(request, customer_id):
    """List or add accounts for a customer."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        customer = Customer.objects.get(id=customer_id, company=membership.company)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        accounts = CustomerAccount.objects.filter(customer=customer)
        return Response(CustomerAccountSerializer(accounts, many=True).data)

    serializer = CustomerAccountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(customer=customer, company=membership.company)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_customer_account(request, customer_id, account_id):
    """Delete a customer's bank/mobile money account."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        account = CustomerAccount.objects.get(
            id=account_id,
            customer_id=customer_id,
            company=membership.company,
        )
    except CustomerAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    account.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
