from django.shortcuts import render, get_object_or_404
from .serializers import (CustomerSerializer, AgentDepositRequestSerializer, \
    CustomerWithdrawalSerializer, PaymentsSerializer, TwilioSerializer, AdminAccountsStartedSerializer, \
    AdminAccountsCompletedSerializer,CustomerAccountsSerializer,BankPaymentSerializer,WithdrawSerializer)

from .models import (Customer, AgentDepositRequests, CustomerWithdrawal, Payments, TwilioApi, \
    AdminAccountsStartedWith, AdminAccountsCompletedWith,CustomerAccounts,BankPayment, WithdrawReference)

from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from users.models import User
from users.serializers import UsersSerializer
from rest_framework import filters
from datetime import datetime, date, time

from fnet_api import serializers


@api_view(['GET'])
def get_twilio(request):
    twilio_details = TwilioApi.objects.all().order_by('-date_created')
    serializer = TwilioSerializer(twilio_details, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agent_requests(request):
    all_agents_requests = AgentDepositRequests.objects.filter(request_status="Pending").order_by('-date_requested')
    serializer = AgentDepositRequestSerializer(all_agents_requests, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_customer_account(request):
    serializer = CustomerAccountsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customer_accounts(request):
    customer_accounts = CustomerAccounts.objects.all().order_by('-date_added')
    serializer = CustomerAccountsSerializer(customer_accounts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def customer_account_detail(request,id):
    c_detail = CustomerAccounts.objects.filter(id=id).order_by('-date_added')
    serializer = CustomerAccountsSerializer(c_detail,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customer_account(request,phone):
    c_detail = CustomerAccounts.objects.filter(phone=phone).order_by('-date_added')
    serializer = CustomerAccountsSerializer(c_detail,many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def approve_request(request, id):
    agent_request = get_object_or_404(AgentDepositRequests, id=id)
    serializer = AgentDepositRequestSerializer(agent_request, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_deposit_request(request):
    serializer = AgentDepositRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def update_accounts(request,id):
    account = get_object_or_404(AdminAccountsStartedWith,id=id)
    serializer = AdminAccountsStartedSerializer(account, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def request_detail(request, pk):
    drequest = AgentDepositRequests.objects.get(pk=pk)
    serializer = AgentDepositRequestSerializer(drequest, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def payment_detail(request, pk):
    dpayment = Payments.objects.get(pk=pk)
    serializer = PaymentsSerializer(dpayment, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def customer_details(request, pk):
    customer = Customer.objects.get(pk=pk)
    serializer = CustomerSerializer(customer, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def customer_withdrawal(request):
    serializer = CustomerWithdrawalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agent(request, username):
    agent = User.objects.filter(username=username)
    serializer = UsersSerializer(agent, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_admin(request):
    admin_user = User.objects.filter(pk=1)
    serializer = UsersSerializer(admin_user, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def agent_customers_summary(request):
    user = get_object_or_404(User, username=request.user.username)
    customers = Customer.objects.filter(agent=user).order_by('-date_created')
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def deposit_request_summary(request):
    user = get_object_or_404(User, username=request.user.username)
    depo_requests = AgentDepositRequests.objects.filter(agent=user).order_by('-date_requested')
    serializer = AgentDepositRequestSerializer(depo_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def customer_withdrawal_summary(request):
    user = get_object_or_404(User, username=request.user.username)
    c_withdrawals = CustomerWithdrawal.objects.filter(agent=user).order_by('-date_requested')
    serializer = CustomerWithdrawalSerializer(c_withdrawals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_summary(request):
    user = get_object_or_404(User, username=request.user.username)
    my_payments = Payments.objects.filter(agent=user).order_by('-date_created')
    serializer = PaymentsSerializer(my_payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_payments(request):
    my_date = datetime.today()
    payments = Payments.objects.filter(payment_status="Pending").order_by('-date_created')
    serializer = PaymentsSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def make_payments(request):
    serializer = PaymentsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def approve_payment(request, id):
    payment = get_object_or_404(Payments, id=id)
    serializer = PaymentsSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_customer(request, name):
    customer = Customer.objects.filter(name=name)
    serializer = CustomerSerializer(customer, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_customers(request):
    user = get_object_or_404(User, username=request.user.username)
    u_customers = Customer.objects.filter(agent=user).order_by('-date_created')
    serializer = CustomerSerializer(u_customers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user_customers(request, username):
    user = get_object_or_404(User, username=username)
    u_customers = Customer.objects.filter(agent=user).order_by('-date_created')
    serializer = CustomerSerializer(u_customers, many=True)
    return Response(serializer.data)


class GetAllCustomers(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Customer.objects.all().order_by('-date_created')
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GetAllAgents(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.exclude(id=1).order_by('-date_joined')
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def admin_accounts_started(request):
    admin_user = User.objects.get(pk=1)
    serializer = AdminAccountsStartedSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=admin_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def admin_account_detail(request,id):
    account = get_object_or_404(AdminAccountsStartedWith, id=id)
    serializer = AdminAccountsStartedSerializer(account,many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def admin_accounts_completed(request):
    admin_user = User.objects.get(pk=1)
    serializer = AdminAccountsCompletedSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=admin_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def admin_accounts_started_lists(request):
    admin_user = User.objects.get(pk=1)
    admin_accounts = AdminAccountsStartedWith.objects.filter(user=admin_user).order_by('-date_started')
    serializer = AdminAccountsStartedSerializer(admin_accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def admin_accounts_completed_lists(request):
    admin_user = User.objects.get(pk=1)
    admin_accounts = AdminAccountsCompletedWith.objects.filter(user=admin_user).order_by('-date_closed')
    serializer = AdminAccountsCompletedSerializer(admin_accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_transaction_requests(request, username):
    my_date = datetime.today()
    user = get_object_or_404(User, username=username)
    all_user_requests = AgentDepositRequests.objects.filter(agent=user).filter(date_requested=f"{my_date.date()}").order_by('-date_requested')
    serializer = AgentDepositRequestSerializer(all_user_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_transaction_payments(request, username):
    my_date = datetime.today()
    user = get_object_or_404(User, username=username)
    all_user_payments = Payments.objects.filter(agent=user).filter(date_created=f"{my_date.date()}").order_by('-date_created')
    serializer = PaymentsSerializer(all_user_payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_transaction_withdrawals(request, username):
    my_date = datetime.today()
    user = get_object_or_404(User, username=username)
    all_user_withdrawals = CustomerWithdrawal.objects.filter(agent=user).filter(date_requested=f"{my_date.date()}").order_by('-date_requested')
    serializer = CustomerWithdrawalSerializer(all_user_withdrawals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_deposit_total(request):
    my_date = datetime.today()
    deposit_today = AgentDepositRequests.objects.filter(agent=request.user).filter(date_requested=my_date.date()).order_by('-date_requested')
    serializer = AgentDepositRequestSerializer(deposit_today,many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_payment_total(request):
    my_date = datetime.today()
    payement_today = Payments.objects.filter(agent=request.user).filter(date_created=my_date.date()).order_by('-date_created')
    serializer = PaymentsSerializer(payement_today,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def make_bank_payment(request):
    serializer = BankPaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_withdraw_reference(request):
    serializer = WithdrawSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_bank_payments(request):
    bank_payments = BankPayment.objects.filter(agent=request.user).order_by('-date_paid')
    serializer = BankPaymentSerializer(bank_payments,many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_withdraw_reference(request):
    withdraw_reference = WithdrawReference.objects.filter(agent=request.user).order_by('-date_withdrew')
    serializer = WithdrawSerializer(withdraw_reference,many=True)
    return Response(serializer.data)