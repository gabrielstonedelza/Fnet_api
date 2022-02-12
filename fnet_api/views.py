from django.shortcuts import render, get_object_or_404
from .serializers import (CustomerSerializer, BankDepositSerializer, ExpenseRequestSerializer,
                          MobileMoneyDepositSerializer,
                          CustomerWithdrawalSerializer, PaymentsSerializer, AdminAccountsStartedSerializer, \
                          AdminAccountsCompletedSerializer, CustomerAccountsSerializer, CashAtPaymentSerializer,
                          WithdrawSerializer, CustomerDepositRequestSerializer, NotificationSerializer,
                          UserMobileMoneyAccountsClosedSerializer, UserMobileMoneyAccountsStartedSerializer,
                          MobileMoneyWithdrawalSerializer)

from .models import (Customer, BankDeposit, ExpensesRequest, MobileMoneyDeposit, CustomerWithdrawal, MyPayments,
                     AdminAccountsStartedWith, AdminAccountsCompletedWith, CustomerAccounts, CashAtPayments,
                     WithdrawReference, CustomerRequestDeposit, UserMobileMoneyAccountsStarted,
                     UserMobileMoneyAccountsClosed, MobileMoneyWithdraw, Notifications)
from drf_multiple_model.views import ObjectMultipleModelAPIView

from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from users.models import User
from users.serializers import UsersSerializer
from rest_framework import filters
from datetime import datetime, date, time

from fnet_api import serializers


# get all pending deposits for admin
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agent_expense_requests_admin(request):
    all_agents_expenses = ExpensesRequest.objects.filter(request_status="Pending").order_by('-date_requested')
    serializer = ExpenseRequestSerializer(all_agents_expenses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agent_bank_requests_admin(request):
    all_agents_bank = BankDeposit.objects.filter(request_status="Pending").order_by('-date_requested')
    serializer = BankDepositSerializer(all_agents_bank, many=True)
    return Response(serializer.data)


# get users deposits for the day for admin
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_expenses_for_today(request, username):
    user = get_object_or_404(User, username=username)
    all_agents_expenses = ExpensesRequest.objects.filter(agent=user).filter(request_status="Approved").order_by(
        '-date_requested')
    serializer = ExpenseRequestSerializer(all_agents_expenses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_bank_for_today(request, username):
    user = get_object_or_404(User, username=username)
    all_agents_bank = BankDeposit.objects.filter(agent=user).filter(request_status="Approved").order_by(
        '-date_requested')
    serializer = BankDepositSerializer(all_agents_bank, many=True)
    return Response(serializer.data)


# get mobile money transactions for user
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_mm_deposits(request):
    momo_deposits = MobileMoneyDeposit.objects.filter(agent=request.user).order_by('-date_deposited')
    serializer = MobileMoneyDepositSerializer(momo_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_mm_withdrawal(request):
    momo_deposits = MobileMoneyWithdraw.objects.filter(agent=request.user).order_by('-date_of_withdrawal')
    serializer = MobileMoneyWithdrawalSerializer(momo_deposits, many=True)
    return Response(serializer.data)


# get mobile money transaction for admin
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_mobile_money_withdraws(request, username):
    user = get_object_or_404(User, username=username)
    momo_deposits = MobileMoneyWithdraw.objects.filter(agent=user).order_by(
        '-date_of_withdrawal')
    serializer = MobileMoneyWithdrawalSerializer(momo_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_mobile_money_deposits(request, username):
    user = get_object_or_404(User, username=username)
    momo_deposits = MobileMoneyDeposit.objects.filter(agent=user).order_by(
        '-date_deposited')
    serializer = MobileMoneyDepositSerializer(momo_deposits, many=True)
    return Response(serializer.data)


# get users mobile money accounts
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_mobile_money_accounts_started(request):
    momo_started = UserMobileMoneyAccountsStarted.objects.filter(agent=request.user).order_by('-date_posted')
    serializer = UserMobileMoneyAccountsStartedSerializer(momo_started, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_mobile_money_accounts_closed(request):
    momo_started = UserMobileMoneyAccountsClosed.objects.filter(agent=request.user).order_by('-date_posted')
    serializer = UserMobileMoneyAccountsClosedSerializer(momo_started, many=True)
    return Response(serializer.data)


# get users mobile money accounts for admin
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_mobile_money_accounts_started(request, username):
    user = get_object_or_404(User, username=username)
    momo_accounts_started = UserMobileMoneyAccountsStarted.objects.filter(agent=user).order_by(
        '-date_posted')
    serializer = UserMobileMoneyAccountsStartedSerializer(momo_accounts_started, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_mobile_money_accounts_closed(request, username):
    user = get_object_or_404(User, username=username)
    momo_accounts_started = UserMobileMoneyAccountsClosed.objects.filter(agent=user).order_by(
        '-date_posted')
    serializer = UserMobileMoneyAccountsClosedSerializer(momo_accounts_started, many=True)
    return Response(serializer.data)


# post users cash deposit
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_expenses_request(request):
    serializer = ExpenseRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# post users bank deposit
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_bank_deposit(request):
    serializer = BankDepositSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# post users mobile money deposit
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_momo_deposit(request):
    serializer = MobileMoneyDepositSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_momo_withdraw(request):
    serializer = MobileMoneyWithdrawalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# post users mobile money accounts started
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_momo_accounts_started(request):
    serializer = UserMobileMoneyAccountsStartedSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def update_momo_accounts(request, id):
    account = get_object_or_404(UserMobileMoneyAccountsStarted, id=id)
    serializer = UserMobileMoneyAccountsStartedSerializer(account, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# post users mobile money accounts closed
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_momo_accounts_closed(request):
    serializer = UserMobileMoneyAccountsClosedSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# register customers accounts
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
def get_customer_accounts_by_bank(request, customer_phone, bank):
    customer_accounts = CustomerAccounts.objects.filter(phone=customer_phone).filter(bank=bank).order_by('-date_added')
    serializer = CustomerAccountsSerializer(customer_accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def customer_account_detail(request, id):
    c_detail = CustomerAccounts.objects.filter(id=id).order_by('-date_added')
    serializer = CustomerAccountsSerializer(c_detail, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customer_account(request, phone):
    c_detail = CustomerAccounts.objects.filter(phone=phone).order_by('-date_added')
    serializer = CustomerAccountsSerializer(c_detail, many=True)
    return Response(serializer.data)


# approve users cash deposit
@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def approve_expense_request(request, id):
    agent_request = get_object_or_404(ExpensesRequest, id=id)
    serializer = ExpenseRequestSerializer(agent_request, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def delete_expense_request(request, id):
    try:
        user_request = get_object_or_404(ExpensesRequest, id=id)
        user_request.delete()
    except User_Request.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)


# approve users bank deposit
@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def approve_bank_deposit(request, id):
    agent_request = get_object_or_404(BankDeposit, id=id)
    serializer = BankDepositSerializer(agent_request, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def delete_bank_request(request, id):
    try:
        user_request = get_object_or_404(BankDeposit, id=id)
        user_request.delete()
    except User_Request.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def update_accounts(request, id):
    account = get_object_or_404(AdminAccountsStartedWith, id=id)
    serializer = AdminAccountsStartedSerializer(account, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get cash deposit detail
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def expense_detail(request, pk):
    c_detail = ExpensesRequest.objects.get(pk=pk)
    serializer = ExpenseRequestSerializer(c_detail, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def momo_accounts_started_detail(request, pk):
    momo_started_detail = UserMobileMoneyAccountsStarted.objects.get(pk=pk)
    serializer = UserMobileMoneyAccountsStartedSerializer(momo_started_detail, many=False)
    return Response(serializer.data)


# get cash bank detail
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def bank_detail(request, pk):
    b_detail = BankDeposit.objects.get(pk=pk)
    serializer = BankDepositSerializer(b_detail, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def payment_detail(request, pk):
    dpayment = MyPayments.objects.get(pk=pk)
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
def customer_withdrawal_summary(request):
    user = get_object_or_404(User, username=request.user.username)
    c_withdrawals = CustomerWithdrawal.objects.filter(agent=user).order_by('-date_requested')
    serializer = CustomerWithdrawalSerializer(c_withdrawals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_summary(request):
    user = get_object_or_404(User, username=request.user.username)
    my_payments = MyPayments.objects.filter(agent=user).order_by('-date_created')
    serializer = PaymentsSerializer(my_payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_payments(request):
    my_date = datetime.today()
    payments = MyPayments.objects.filter(payment_status="Pending").order_by('-date_created')
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
    payment = get_object_or_404(MyPayments, id=id)
    serializer = PaymentsSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def delete_payment(request, id):
    try:
        user_payment = get_object_or_404(MyPayments, id=id)
        user_payment.delete()
    except User_Payment.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_customer(request, name):
    customer = Customer.objects.filter(name=name)
    serializer = CustomerSerializer(customer, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customer_by_phone(request, phone):
    customer = Customer.objects.filter(phone=phone)
    serializer = CustomerSerializer(customer, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_momo_deposit_customer_by_phone(request, phone):
    customer = MobileMoneyDeposit.objects.filter(customer_phone=phone)
    serializer = MobileMoneyDepositSerializer(customer, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_momo_withdraw_customer_by_phone(request, phone):
    customer = MobileMoneyWithdraw.objects.filter(customer_phone=phone)
    serializer = MobileMoneyWithdrawalSerializer(customer, many=True)
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


class GetAllUserCustomers(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone']

    def get_queryset(self):
        agent = self.request.user
        return Customer.objects.filter(agent=agent)


class GetAllCustomers(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Customer.objects.all().order_by('-date_created')
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone']


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
def admin_account_detail(request, id):
    account = get_object_or_404(AdminAccountsStartedWith, id=id)
    serializer = AdminAccountsStartedSerializer(account, many=False)
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
def user_transaction_payments(request, username):
    user = get_object_or_404(User, username=username)
    all_user_payments = MyPayments.objects.filter(agent=user).filter(payment_status="Approved").order_by(
        '-date_created')
    serializer = PaymentsSerializer(all_user_payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_transaction_withdrawals(request, username):
    user = get_object_or_404(User, username=username)
    all_user_withdrawals = CustomerWithdrawal.objects.filter(agent=user).order_by('-date_requested')
    serializer = CustomerWithdrawalSerializer(all_user_withdrawals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_payments(request):
    payment_today = MyPayments.objects.filter(agent=request.user).order_by('-date_created')
    serializer = PaymentsSerializer(payment_today, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_payment_approved_total(request):
    payment_today = MyPayments.objects.filter(agent=request.user).filter(payment_status="Approved").order_by(
        '-date_created')
    serializer = PaymentsSerializer(payment_today, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def make_bank_payment(request):
    serializer = CashAtPaymentSerializer(data=request.data)
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
    bank_payments = CashAtPayments.objects.filter(agent=request.user).order_by('-date_paid')
    serializer = CashAtPaymentSerializer(bank_payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_withdraw_reference(request):
    withdraw_reference = WithdrawReference.objects.filter(agent=request.user).order_by('-date_withdrew')
    serializer = WithdrawSerializer(withdraw_reference, many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def user_delete(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.delete()
    except User.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def customer_delete(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        customer.delete()
    except Customer.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def approve_customer_request(request, id):
    customer_request = get_object_or_404(CustomerRequestDeposit, id=id)
    serializer = CustomerDepositRequestSerializer(customer_request, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def delete_customer_request(request, id):
    try:
        customer_request = get_object_or_404(CustomerRequestDeposit, id=id)
        customer_request.delete()
    except Customer_Request.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customers_requests(request, phone):
    all_customer_requests = CustomerRequestDeposit.objects.filter(customer_phone=phone).order_by('-date_requested')
    serializer = CustomerDepositRequestSerializer(all_customer_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_your_customers_requests(request):
    your_customers_requests = CustomerRequestDeposit.objects.filter(request_status="Pending").order_by(
        '-date_requested')
    serializer = CustomerDepositRequestSerializer(your_customers_requests, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def customer_deposit_request(request):
    serializer = CustomerDepositRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customer_request_summary(request, phone):
    request_summary = CustomerRequestDeposit.objects.filter(customer_phone=phone).order_by('-date_requested')
    serializer = CustomerDepositRequestSerializer(request_summary, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customer_transaction_summary(request, phone):
    transaction_summary = BankDeposit.objects.filter(customer=phone).order_by('-date_requested')
    serializer = BankDepositSerializer(transaction_summary, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customer_accounts(request, phone):
    customer_accounts = CustomerAccounts.objects.filter(phone=phone).order_by('-date_added')
    serializer = CustomerAccountsSerializer(customer_accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def customer_request_detail(request, pk):
    c_request = CustomerRequestDeposit.objects.get(pk=pk)
    serializer = CustomerDepositRequestSerializer(c_request, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def add_flag(request):
    serializer = UserFlagsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_flags(request):
    flags = UserFlags.objects.all().order_by('-date_added')
    serializer = UserFlagsSerializer(flags, many=True)
    return Response(serializer.data)


# update customer details
@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def update_customers_details(request, id):
    customer = get_object_or_404(Customer, id=id)
    serializer = CustomerSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get all momo deposit users
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_momo_deposit_customers(request):
    momo_customers = MobileMoneyDeposit.objects.all().order_by('-date_deposited')
    serializer = MobileMoneyDepositSerializer(momo_customers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_momo_withdraw_customers(request):
    momo_customers = MobileMoneyWithdraw.objects.all().order_by('-date_of_withdrawal')
    serializer = MobileMoneyWithdrawalSerializer(momo_customers, many=True)
    return Response(serializer.data)


# get cash and bank request for the day
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_expense_request_for_today(request):
    your_expense_requests = ExpensesRequest.objects.filter(agent=request.user).filter(deposit_paid="Not Paid").order_by(
        '-date_requested')
    serializer = ExpenseRequestSerializer(your_expense_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_expenses_request_all(request):
    your_expense_requests = ExpensesRequest.objects.filter(agent=request.user).order_by('-date_requested')
    serializer = ExpenseRequestSerializer(your_expense_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_bank_deposits_all(request):
    your_bank_requests = BankDeposit.objects.filter(agent=request.user).order_by('-date_requested')
    serializer = BankDepositSerializer(your_bank_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_bank_deposits_for_today(request):
    your_bank_requests = BankDeposit.objects.filter(agent=request.user).filter(deposit_paid="Paid").order_by(
        '-date_requested')
    serializer = BankDepositSerializer(your_bank_requests, many=True)
    return Response(serializer.data)


# get uses commission
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_deposit_commission(request):
    my_date = datetime.today()
    your_commission = MobileMoneyDeposit.objects.filter(agent=request.user).filter(
        date_deposited=my_date.date()).order_by(
        '-date_deposited')
    serializer = MobileMoneyDepositSerializer(your_commission, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_withdraw_commission(request):
    my_date = datetime.today()
    your_commission = MobileMoneyWithdraw.objects.filter(agent=request.user).filter(
        date_of_withdrawal=my_date.date()).order_by(
        '-date_of_withdrawal')
    serializer = MobileMoneyWithdrawalSerializer(your_commission, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_deposit_commission(request, username):
    user = get_object_or_404(User, username=username)
    my_date = datetime.today()
    your_commission = MobileMoneyDeposit.objects.filter(agent=user).filter(
        date_deposited=my_date.date()).order_by('-date_deposited')
    serializer = MobileMoneyDepositSerializer(your_commission, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_withdraw_commission(request, username):
    user = get_object_or_404(User, username=username)
    my_date = datetime.today()
    your_commission = MobileMoneyWithdraw.objects.filter(agent=user).filter(
        date_of_withdrawal=my_date.date()).order_by(
        '-date_of_withdrawal')
    serializer = MobileMoneyWithdrawalSerializer(your_commission, many=True)
    return Response(serializer.data)


# search agent commission based on date
class SearchAgentsMomoDepositTransactions(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MobileMoneyDeposit.objects.all().order_by('-date_deposited')
    serializer_class = MobileMoneyDepositSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['date_deposited', 'agent__username', 'customer_phone']


class SearchAgentsMomoWithdrawTransactions(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MobileMoneyWithdraw.objects.all().order_by('-date_of_withdrawal')
    serializer_class = MobileMoneyWithdrawalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['date_of_withdrawal', 'agent__username', 'customer_phone']


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def approve_bank_deposit_paid(request, id):
    bank_deposit = get_object_or_404(BankDeposit, id=id)
    serializer = BankDepositSerializer(bank_deposit, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def approve_expense_request_paid(request, id):
    expense_request = get_object_or_404(ExpensesRequest, id=id)
    serializer = ExpenseRequestSerializer(expense_request, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_unpaid_expense_request_for_today(request):
    your_expense_requests = ExpensesRequest.objects.filter(agent=request.user).filter(deposit_paid="Not Paid").filter(
        request_status="Approved").order_by('-date_requested')
    serializer = ExpenseRequestSerializer(your_expense_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_unpaid_bank_deposits_for_today(request):
    your_bank_requests = BankDeposit.objects.filter(agent=request.user).filter(deposit_paid="Not Paid").filter(
        request_status="Approved").order_by('-date_requested')
    serializer = BankDepositSerializer(your_bank_requests, many=True)
    return Response(serializer.data)


# for local data
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_bank_deposits(request):
    bank_deposits = BankDeposit.objects.all().order_by('-date_requested')
    serializer = BankDepositSerializer(bank_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_cash_at_payments(request):
    bank_deposits = CashAtPayments.objects.all().order_by('-date_paid')
    serializer = CashAtPaymentSerializer(bank_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_momo_deposit_made(request):
    bank_deposits = MobileMoneyDeposit.objects.all().order_by('-date_deposited')
    serializer = MobileMoneyDepositSerializer(bank_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_momo_withdrawal_made(request):
    bank_deposits = MobileMoneyWithdraw.objects.all().order_by('-date_of_withdrawal')
    serializer = MobileMoneyWithdrawalSerializer(bank_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_user_momo_accounts_started(request):
    bank_deposits = UserMobileMoneyAccountsStarted.objects.all().order_by('-date_posted')
    serializer = UserMobileMoneyAccountsStartedSerializer(bank_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_user_momo_accounts_closed(request):
    bank_deposits = UserMobileMoneyAccountsClosed.objects.all().order_by('-date_posted')
    serializer = UserMobileMoneyAccountsClosedSerializer(bank_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_users(request):
    bank_deposits = User.objects.all()
    serializer = UsersSerializer(bank_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_user_notifications(request):
    notifications = Notifications.objects.filter(user2=request.user).order_by('-date_created')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_notifications(request):
    notifications = Notifications.objects.filter(user2=request.user).filter(read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_triggered_notifications(request):
    notifications = Notifications.objects.filter(user2=request.user).filter(notification_trigger="Triggered").filter(
        read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def read_notification(request, id):
    notification = get_object_or_404(Notifications, id=id)
    serializer = NotificationSerializer(notification, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_agents_bank_total_by_date(request):
    all_agents_bank = BankDeposit.objects.filter(agent=request.user).filter(request_status="Approved").order_by(
        '-date_requested')
    serializer = BankDepositSerializer(all_agents_bank, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_agents_expense_request_total_by_date(request):
    all_agents_expenses = ExpensesRequest.objects.filter(agent=request.user).filter(request_status="Approved").order_by(
        '-date_requested')
    serializer = BankDepositSerializer(all_agents_expenses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_total_payments(request):
    all_user_payments = MyPayments.objects.filter(agent=request.user).filter(payment_status="Approved").order_by(
        '-date_created')
    serializer = PaymentsSerializer(all_user_payments, many=True)
    return Response(serializer.data)
