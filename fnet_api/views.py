from django.shortcuts import render, get_object_or_404
from .serializers import (CustomerSerializer, BankDepositSerializer, ExpenseRequestSerializer,
                          MobileMoneyDepositSerializer,WithdrawalReferenceSerializer,
                          CustomerWithdrawalSerializer, PaymentsSerializer, AdminAccountsStartedSerializer, \
                          AdminAccountsCompletedSerializer, CustomerAccountsSerializer, CashAtPaymentSerializer,
                          ReportsSerializer, FnetGroupMessageSerializer, FnetPrivateUserMessageSerializer,
                          CustomerDepositRequestSerializer, NotificationSerializer,
                          UserMobileMoneyAccountsClosedSerializer, UserMobileMoneyAccountsStartedSerializer,
                          MobileMoneyWithdrawalSerializer, PaymentAtBankSerializer, OTPSerializer,
                          CustomerPaymentAtBankSerializer, AddedToApprovedPaymentSerializer,
                          AddedToApprovedBankDepositsSerializer, PrivateChatIdSerializer, AddToCustomerPointsSerializer,CashRequestSerializer,CashPaymentsSerializer,AddedToApprovedCashPaymentSerializer,
                          AddToCustomerRedeemPointsSerializer, ReferCustomerSerializer, AdminCustomerSerializer,
                          AddToBlockListSerializer)

from .models import (Customer, BankDeposit, ExpensesRequest, MobileMoneyDeposit, CustomerWithdrawal, MyPayments,
                     AdminAccountsStartedWith, AdminAccountsCompletedWith, CustomerAccounts, CashAtPayments,
                     CustomerRequestDeposit, UserMobileMoneyAccountsStarted, OTP, FnetGroupMessage,
                     FnetPrivateUserMessage,WithdrawalReference,
                     UserMobileMoneyAccountsClosed, MobileMoneyWithdraw, Notifications, PaymentAtBank,
                     CustomerPaymentAtBank, AddedToApprovedPayment, AddedToApprovedDeposits, Reports, PrivateChatId,CashRequest,MyCashPayments,AddedToApprovedCashPayment,
                     AddToCustomerPoints, AddToCustomerRedeemPoints, ReferCustomer, AddToBlockList
                     )
from drf_multiple_model.views import ObjectMultipleModelAPIView

from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from users.models import User
from users.serializers import UsersSerializer
from rest_framework import filters
from datetime import datetime, date, time

from fnet_api import serializers
from django.utils import timezone

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def admin_add_to_approved_cash_payment(request):
    serializer = AdminAddToCashPaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def admin_add_to_approved_payment(request):
    serializer = AddedToApprovedPaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def admin_add_to_approved_bank_deposit(request):
    serializer = AddedToApprovedBankDepositsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def customers_account_detail(request, pk):
    account_detail = CustomerAccounts.objects.get(pk=pk)
    serializer = CustomerAccountsSerializer(account_detail, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_otp_to_customer_admin(request):
    serializer = OTPSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_admin_otp_notifications(request):
    otp_notifications = Notifications.objects.filter(notification_to_guarantor=1).order_by('-date_created')
    serializer = NotificationSerializer(otp_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_customer_otp_notifications(request, phone_number):
    otp_notifications = Notifications.objects.filter(notification_to_customer=phone_number).order_by('-date_created')
    serializer = NotificationSerializer(otp_notifications, many=True)
    return Response(serializer.data)


class GetAllCustomersAccounts(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CustomerAccounts.objects.all().order_by('-date_added')
    serializer_class = CustomerAccountsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['account_name', 'phone', 'account_number']


# not to be used now
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_customers_accounts(request, number):
    customers_accounts = CustomerAccounts.objects.filter(phone=number).order_by('-date_added')
    serializer = CustomerAccountsSerializer(customers_accounts, many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def delete_customer_accounts(request, pk):
    try:
        customer_account = CustomerAccounts.objects.get(pk=pk)
        customer_account.delete()
    except Customer.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def update_customers_accounts_details(request, id):
    customer = get_object_or_404(CustomerAccounts, id=id)
    serializer = CustomerAccountsSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_at_bank(request):
    serializer = PaymentAtBankSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_data_at_bank(request):
    all_agents_bank_payment = PaymentAtBank.objects.all().order_by('-date_added')
    serializer = PaymentAtBankSerializer(all_agents_bank_payment, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def bank_payment_detail(request, pk):
    de_bank_payment = PaymentAtBank.objects.get(pk=pk)
    serializer = PaymentAtBankSerializer(de_bank_payment, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_my_data_at_bank(request):
    all_my_bank_payment = PaymentAtBank.objects.filter(agent=request.user).order_by('-date_added')
    serializer = PaymentAtBankSerializer(all_my_bank_payment, many=True)
    return Response(serializer.data)


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


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def admin_register_customer(request):
    serializer = AdminCustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
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


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def customer_details_by_phone(request, phone):
    customer = get_object_or_404(Customer, phone=phone)
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

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_payments(request):
    payments = MyPayments.objects.all().order_by('-date_created')
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

# admin update payment
@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def update_payment(request, id):
    payment = get_object_or_404(MyPayments, id=id)
    serializer = PaymentsSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def update_bank_deposit(request, id):
    deposit = get_object_or_404(BankDeposit, id=id)
    serializer = BankDepositSerializer(deposit, data=request.data)
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
    user = get_object_or_404(User, id=request.user.id)
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


# class GetAllAgents(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = User.objects.exclude(id=request.user.id).order_by('-date_joined')
#     serializer_class = UsersSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['username']


class GetAllAgents(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def get_queryset(self):
        agent = self.request.user
        return User.objects.exclude(id=agent.id).order_by('-date_joined')


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
    my_date = datetime.today()
    de_date = my_date.date()
    payment_today = MyPayments.objects.filter(agent=request.user).filter(payment_status="Approved").filter(
        payment_month=de_date.month).filter(payment_year=de_date.year).order_by(
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


# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def add_withdraw_reference(request):
#     serializer = WithdrawSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(agent=request.user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_bank_payments(request):
    bank_payments = CashAtPayments.objects.filter(agent=request.user).order_by('-date_paid')
    serializer = CashAtPaymentSerializer(bank_payments, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def get_user_withdraw_reference(request):
#     withdraw_reference = WithdrawReference.objects.filter(agent=request.user).order_by('-date_added')
#     serializer = WithdrawSerializer(withdraw_reference, many=True)
#     return Response(serializer.data)


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
    request_summary = CustomerRequestDeposit.objects.filter(customer_phone=phone).filter(
        request_status="Approved").order_by('-date_requested')
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
def get_momo_withdraw_user(request, phone):
    user = MobileMoneyWithdraw.objects.filter(phone=phone).order_by('-date_of_withdrawal')
    serializer = MobileMoneyWithdrawalSerializer(user, many=True)
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
    my_date = datetime.today()
    de_date = my_date.date()
    your_bank_requests = BankDeposit.objects.filter(agent=request.user).filter(
        deposited_month=de_date.month).filter(deposited_year=de_date.year).filter(deposit_paid="Not Paid").order_by(
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
    search_fields = ['date_deposited', 'agent__username']


class SearchAgentsMomoWithdrawTransactions(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MobileMoneyWithdraw.objects.all().order_by('-date_of_withdrawal')
    serializer_class = MobileMoneyWithdrawalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['date_of_withdrawal', 'agent__username', ]


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
    all_momo_withdrawal = MobileMoneyWithdraw.objects.all().order_by('-date_of_withdrawal')
    serializer = MobileMoneyWithdrawalSerializer(all_momo_withdrawal, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_users_expenses_total(request):
    all_expenses = ExpensesRequest.objects.all().order_by('-date_requested')
    serializer = ExpenseRequestSerializer(all_expenses, many=True)
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
def get_all_read_user_notifications(request):
    notifications = Notifications.objects.filter(user2=request.user).filter(read="Read").order_by('-date_created')
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


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_customer_accounts(request):
    customer_accounts = CustomerAccounts.objects.all().order_by('-date_added')
    serializer = CustomerAccountsSerializer(customer_accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_customer_requests(request):
    customer_request = CustomerRequestDeposit.objects.all().order_by('-date_requested')
    serializer = CustomerDepositRequestSerializer(customer_request, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_user_payments(request):
    user_payments = MyPayments.objects.all().order_by('-date_created')
    serializer = PaymentsSerializer(user_payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def notifications(request):
    notifications_alerts = Notifications.objects.all().order_by('-date_created')
    serializer = NotificationSerializer(notifications_alerts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def all_user_accounts_started(request):
    user_accounts = UserMobileMoneyAccountsStarted.objects.all().order_by('-date_posted')
    serializer = UserMobileMoneyAccountsStartedSerializer(user_accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def all_user_accounts_closed(request):
    user_accounts = UserMobileMoneyAccountsClosed.objects.all().order_by('-date_posted')
    serializer = UserMobileMoneyAccountsClosedSerializer(user_accounts, many=True)
    return Response(serializer.data)


# customer notifications
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_customer_notifications(request, phone_number):
    customer_notifications = Notifications.objects.filter(notification_to_customer=phone_number).order_by(
        '-date_created')
    serializer = NotificationSerializer(customer_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customer_notifications(request, phone_number):
    customer_notifications = Notifications.objects.filter(notification_to_customer=phone_number).filter(
        read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(customer_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_customer_read_user_notifications(request, phone_number):
    customer_notifications = Notifications.objects.filter(notification_to_customer=phone_number).filter(
        read="Read").order_by('-date_created')
    serializer = NotificationSerializer(customer_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customer_triggered_notifications(request, phone_number):
    customer_notifications = Notifications.objects.filter(notification_to_customer=phone).filter(
        notification_trigger="Triggered").filter(
        read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(customer_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def read_customer_notification(request, id):
    notification = get_object_or_404(Notifications, id=id)
    serializer = NotificationSerializer(notification, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# requests
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customers_bank_deposits(request, phone_number):
    all_customer_deposits = BankDeposit.objects.filter(customer=phone_number).filter(
        request_status="Approved").order_by(
        '-date_requested')
    serializer = BankDepositSerializer(all_customer_deposits, many=True)
    return Response(serializer.data)


# customer bank payments
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def post_customer_at_bank(request):
    serializer = CustomerPaymentAtBankSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_customer_data_at_bank(request, customer):
    all_agents_bank_payment = CustomerPaymentAtBank.objects.filter(customer=customer).order_by('-date_added')
    serializer = CustomerPaymentAtBankSerializer(all_agents_bank_payment, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def customer_bank_payment_detail(request, pk):
    de_bank_payment = CustomerPaymentAtBank.objects.get(pk=pk)
    serializer = CustomerPaymentAtBankSerializer(de_bank_payment, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_customers_data_at_bank(request):
    all_customer_bank_payment = CustomerPaymentAtBank.objects.all().order_by('-date_added')
    serializer = CustomerPaymentAtBankSerializer(all_customer_bank_payment, many=True)
    return Response(serializer.data)


# get notifications by type
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_customer_bank_payment_notifications(request):
    customer_bank_notifications = Notifications.objects.filter(user2=request.user).filter(
        transaction_type="Customer Bank Payment").filter(read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(customer_bank_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_customer_otp_notifications(request):
    customer_bank_notifications = Notifications.objects.filter(user2=request.user).filter(
        transaction_type="OTP").filter(read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(customer_bank_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_payments_notifications(request):
    customer_bank_notifications = Notifications.objects.filter(user2=request.user).filter(
        transaction_type="Payment").filter(read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(customer_bank_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_bank_requests_notifications(request):
    customer_bank_notifications = Notifications.objects.filter(user2=request.user).filter(
        transaction_type="Bank").filter(read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(customer_bank_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_report_notifications(request):
    customer_bank_notifications = Notifications.objects.filter(user2=request.user).filter(
        transaction_type="New Report").filter(read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(customer_bank_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_expenses_requests_notifications(request):
    customer_bank_notifications = Notifications.objects.filter(user2=request.user).filter(
        transaction_type="Cash").filter(read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(customer_bank_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_customer_requests_notifications(request):
    customer_bank_notifications = Notifications.objects.filter(user2=request.user).filter(
        transaction_type="Customer").filter(read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(customer_bank_notifications, many=True)
    return Response(serializer.data)


# get customers deposit transactions
class GetCustomersDepositTransactions(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = BankDeposit.objects.all().order_by('-date_requested')
    serializer_class = BankDepositSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['customer', 'date_requested', ]


class GetCustomerDepositTransactions(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BankDepositSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['date_requested', ]

    def get_queryset(self):
        customer = self.kwargs['customer']
        return BankDeposit.objects.filter(customer=customer).order_by('-date_requested')


# get users all summaries
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


# get momo transactions by network
# deposits
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_mtn_deposits_summary(request):
    momo_deposits = MobileMoneyDeposit.objects.filter(agent=request.user).filter(network="Mtn").order_by(
        '-date_deposited')
    serializer = MobileMoneyDepositSerializer(momo_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_tigo_deposits_summary(request):
    momo_deposits = MobileMoneyDeposit.objects.filter(agent=request.user).filter(network="Tigo").order_by(
        '-date_deposited')
    serializer = MobileMoneyDepositSerializer(momo_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_vodafone_deposits_summary(request):
    momo_deposits = MobileMoneyDeposit.objects.filter(agent=request.user).filter(network="Vodafone").order_by(
        '-date_deposited')
    serializer = MobileMoneyDepositSerializer(momo_deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_momo_agent_to_agent_summary(request):
    momo_deposits = MobileMoneyDeposit.objects.filter(agent=request.user).filter(type="Agent to Agent").order_by(
        '-date_deposited')
    serializer = MobileMoneyDepositSerializer(momo_deposits, many=True)
    return Response(serializer.data)


# get momo transactions by network
# withdraws
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_mtn_withdrawal(request):
    mtn_withdraw = MobileMoneyWithdraw.objects.filter(agent=request.user).filter(network="Mtn").order_by(
        '-date_of_withdrawal')
    serializer = MobileMoneyWithdrawalSerializer(mtn_withdraw, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_tigo_withdrawal(request):
    tigo_withdraw = MobileMoneyWithdraw.objects.filter(agent=request.user).filter(network="Tigo").order_by(
        '-date_of_withdrawal')
    serializer = MobileMoneyWithdrawalSerializer(tigo_withdraw, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_vodafone_withdrawal(request):
    vodafone_withdraw = MobileMoneyWithdraw.objects.filter(agent=request.user).filter(network="Vodafone").order_by(
        '-date_of_withdrawal')
    serializer = MobileMoneyWithdrawalSerializer(vodafone_withdraw, many=True)
    return Response(serializer.data)


# reports by users and admin
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_report(request):
    serializer = ReportsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def report_detail(request, id):
    report = get_object_or_404(Reports, id=id)
    if report:
        report.read = True
        report.save()
    serializer = ReportsSerializer(report, many=False)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_report(request, id):
    report = get_object_or_404(Reports, id=id)
    serializer = ReportsSerializer(report, data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_my_reports(request):
    reports = Reports.objects.filter(user=request.user).order_by('-date_reported')
    serializer = ReportsSerializer(reports, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_reports(request):
    reports = Reports.objects.all().order_by('-date_reported')
    serializer = ReportsSerializer(reports, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user_reports(request, username):
    user = get_object_or_404(User, username=username)
    report = Reports.objects.filter(user=user).order_by('-date_reported')
    serializer = ReportsSerializer(report, many=True)
    return Response(serializer.data)


# private and public messages
# group message post and get request
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_group_message(request):
    serializer = FnetGroupMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_group_message(request):
    messages = FnetGroupMessage.objects.all().order_by('-timestamp')
    serializer = FnetGroupMessageSerializer(messages, many=True)
    return Response(serializer.data)


# private messages
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_private_message(request):
    serializer = FnetPrivateUserMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_private_message(request, user1, user2):
    all_messages = []
    messages1 = FnetPrivateUserMessage.objects.filter(sender=user1, receiver=user2).order_by('-timestamp')
    messages2 = FnetPrivateUserMessage.objects.filter(sender=user2, receiver=user1).order_by('-timestamp')
    for i in messages1:
        all_messages.append(i)

    for m in messages2:
        all_messages.append(m)
    serializer = FnetPrivateUserMessageSerializer(all_messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def private_message_detail(request, user1, user2):
    message = FnetPrivateUserMessage.objects.get(sender=user1, receiver=user2)
    if message:
        message.read = True
        message.save()
    serializer = FnetPrivateUserMessageSerializer(message, many=False)
    return Response(serializer.data)


# customer points
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_customer_points(request):
    serializer = AddToCustomerPointsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def add_to_customer_redeemed_points(request):
    serializer = AddToCustomerRedeemPointsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customer_redeemed_points(request, customer_phone):
    redeemedPoints = AddToCustomerRedeemPoints.objects.filter(customer_phone=customer_phone).order_by('-date_created')
    serializer = AddToCustomerRedeemPointsSerializer(redeemedPoints, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_redeemed_points(request):
    redeemedPoints = AddToCustomerRedeemPoints.objects.all().order_by('-date_created')
    serializer = AddToCustomerRedeemPointsSerializer(redeemedPoints, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_customer_points(request, customer_phone):
    points = Customer.objects.filter(phone=customer_phone).order_by('-date_created')
    serializer = CustomerSerializer(points, many=True)
    return Response(serializer.data)


# customer referral
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def refer_customer(request):
    serializer = ReferCustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get customer referrals
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_customer_referrals(request, referral):
    referrals = ReferCustomer.objects.filter(referral=referral).order_by('-date_created')
    serializer = ReferCustomerSerializer(referrals, many=True)
    return Response(serializer.data)


# referral detail
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def referral_detail(request, pk):
    referral = get_object_or_404(ReferCustomer, pk=pk)
    serializer = ReferCustomerSerializer(referral, many=False)
    return Response(serializer.data)


# get all referrals for
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_referrals(request, ):
    referrals = ReferCustomer.objects.all().order_by('-date_created')
    serializer = ReferCustomerSerializer(referrals, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def update_referral(request, id):
    referral = get_object_or_404(ReferCustomer, id=id)
    serializer = ReferCustomerSerializer(referral, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_was_referred_customers(request, ):
    referrals = Customer.objects.filter(status="Was Referred").order_by('-date_created')
    serializer = CustomerSerializer(referrals, many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def delete_notifications(request, ):
    try:
        all_notifications = Notifications.objects.all()
        for i in all_notifications:
            i.delete()
    except All_Notifications.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)


# delete momo deposit and withdraws
@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def delete_momo_deposit_request(request, id):
    try:
        momo_request = get_object_or_404(MobileMoneyDeposit, id=id)
        momo_request.delete()
    except Momo_Request.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def delete_momo_withdraw_request(request, id):
    try:
        momo_request = get_object_or_404(MobileMoneyWithdraw, id=id)
        momo_request.delete()
    except Momo_Request.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_unpaid_deposits(request):
    deposits = BankDeposit.objects.filter(deposit_paid="Not Paid").order_by('-date_requested')
    serializer = BankDepositSerializer(deposits, many=True)
    return Response(serializer.data)


# block list
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def add_to_blocked(request):
    serializer = AddToBlockListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def remove_from_blocked(request, id):
    try:
        user_blocked = get_object_or_404(AddToBlockList, id=id)
        user_blocked.delete()
    except User_Blocked.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_blocked_users(request):
    users = AddToBlockList.objects.all().order_by('-date_blocked')
    serializer = AddToBlockListSerializer(users, many=True)
    return Response(serializer.data)


# fetching banks
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_fidelity(request):
    fidelity_bank = BankDeposit.objects.filter(bank="Fidelity Bank").order_by('-date_requested')
    serializer = BankDepositSerializer(fidelity_bank, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_cals(request):
    cals = BankDeposit.objects.filter(bank="Cal Bank").order_by('-date_requested')
    serializer = BankDepositSerializer(cals, many=True)
    return Response(serializer.data)

# getting users fidelity,ecobank and calbank transactions
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_cal_bank(request, username):
    user = get_object_or_404(User, username=username)
    bank = BankDeposit.objects.filter(agent=user).filter(bank="Cal Bank").order_by(
        '-date_requested')
    serializer = BankDepositSerializer(bank, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_fidelity_bank(request, username):
    user = get_object_or_404(User, username=username)
    bank = BankDeposit.objects.filter(agent=user).filter(bank="Fidelity Bank").order_by(
        '-date_requested')
    serializer = BankDepositSerializer(bank, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_eco_bank(request, username):
    user = get_object_or_404(User, username=username)
    bank = BankDeposit.objects.filter(agent=user).filter(bank="Ecobank").order_by(
        '-date_requested')
    serializer = BankDepositSerializer(bank, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_access_bank(request, username):
    user = get_object_or_404(User, username=username)
    bank = BankDeposit.objects.filter(agent=user).filter(bank="Access Bank").order_by(
        '-date_requested')
    serializer = BankDepositSerializer(bank, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_gt_bank(request, username):
    user = get_object_or_404(User, username=username)
    bank = BankDeposit.objects.filter(agent=user).filter(bank="GT Bank").order_by(
        '-date_requested')
    serializer = BankDepositSerializer(bank, many=True)
    return Response(serializer.data)


# search user bank transactions by dates and year
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_bank_transactions_by_date(request, username, d_month, d_year, bank):
    user = get_object_or_404(User, username=username)
    bank = BankDeposit.objects.filter(agent=user).filter(bank=bank).filter(deposited_month=d_month).filter(deposited_year=d_year).filter(request_status="Approved")
    serializer = BankDepositSerializer(bank, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_fidelity_bank_by_date(request, username, d_month, d_year):
    user = get_object_or_404(User, username=username)
    bank = BankDeposit.objects.filter(agent=user).filter(bank="Fidelity Bank").filter(deposited_month=d_month).filter(deposited_year=d_year).order_by('-date_requested')
    serializer = BankDepositSerializer(bank, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_access_bank_by_date(request, username, d_month, d_year):
    user = get_object_or_404(User, username=username)
    bank = BankDeposit.objects.filter(agent=user).filter(bank="Access Bank").filter(deposited_month=d_month).filter(deposited_year=d_year).filter(request_status="Approved")
    serializer = BankDepositSerializer(bank, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_cal_bank_by_date(request, username, d_month, d_year):
    user = get_object_or_404(User, username=username)
    bank = BankDeposit.objects.filter(agent=user).filter(bank="Cal Bank").filter(deposited_month=d_month).filter(deposited_year=d_year).filter(request_status="Approved")
    serializer = BankDepositSerializer(bank, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_gt_bank_by_date(request, username, d_month, d_year):
    user = get_object_or_404(User, username=username)
    bank = BankDeposit.objects.filter(agent=user).filter(bank="GT Bank").filter(deposited_month=d_month).filter(deposited_year=d_year).filter(request_status="Approved")
    serializer = BankDepositSerializer(bank, many=True)
    return Response(serializer.data)


# cash request
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_cash_deposit(request):
    serializer = CashRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_admin_user_cash_requests(request):
    all_agents_cash_requests = CashRequest.objects.filter(request_status="Pending").order_by('-date_requested')
    serializer = CashRequestSerializer(all_agents_cash_requests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_admin_all_user_cash_requests(request,username):
    user = get_object_or_404(User, username=username)
    all_agents_cash_requests = CashRequest.objects.filter(agent1=user).filter(request_status="Approved").order_by('-date_requested')
    serializer = CashRequestSerializer(all_agents_cash_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agent1_cash_requests_today(request, username):
    user = get_object_or_404(User, username=username)
    all_agents_cash_requests = CashRequest.objects.filter(agent1=user).filter(request_status="Approved").order_by(
        '-date_requested')
    serializer = CashRequestSerializer(all_agents_cash_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agent2_cash_requests_today(request, username):
    user = get_object_or_404(User, username=username)
    all_agents_cash_requests = CashRequest.objects.filter(agent2=user).filter(request_status="Approved").order_by(
        '-date_requested')
    serializer = CashRequestSerializer(all_agents_cash_requests, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def approve_cash_request(request, id):
    agent_request = get_object_or_404(CashRequest, id=id)
    serializer = CashRequestSerializer(agent_request, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def cash_requests_detail(request, pk):
    c_detail = CashRequest.objects.get(pk=pk)
    serializer = CashRequestSerializer(c_detail, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_agent1_cash_request_all(request):
    your_cash_requests = CashRequest.objects.filter(agent1=request.user).order_by('-date_requested')
    serializer = CashRequestSerializer(your_cash_requests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_agent2_cash_request_all(request):
    your_cash_requests = CashRequest.objects.filter(agent2=request.user).order_by('-date_requested')
    serializer = CashRequestSerializer(your_cash_requests, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def update_cash_requests(request, id):
    cash_request = get_object_or_404(CashRequest, id=id)
    serializer = CashRequestSerializer(cash_request, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_user_cash_payments(request):
    user_payments = MyCashPayments.objects.all().order_by('-date_created')
    serializer = CashPaymentSerializerPaymentsSerializer(user_payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_unpaid_cash_deposits(request):
    deposits = CashRequest.objects.filter(agent1=request.user).filter(request_paid="Not Paid").order_by('-date_requested')
    serializer = CashRequestSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_cash_payments_notifications(request):
    customer_bank_notifications = Notifications.objects.filter(user2=request.user).filter(
        transaction_type="Cash Payment").filter(read="Not Read").order_by('-date_created')
    serializer = NotificationSerializer(customer_bank_notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_total_cash_payments(request):
    all_user_payments = MyCashPaymentsPayments.objects.filter(agent=request.user).filter(payment_status="Approved").order_by(
        '-date_created')
    serializer = CashPaymentsSerializerPaymentsSerializer(all_user_payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_cash_payment_approved_total(request):
    my_date = datetime.today()
    de_date = my_date.date()
    payment_today = MyCashPayments.objects.filter(agent=request.user).filter(payment_status="Approved").filter(
        payment_month=de_date.month).filter(payment_year=de_date.year).order_by(
        '-date_created')
    serializer = CashPaymentsSerializer(payment_today, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_payments_cash(request):
    payment_today = MyCashPayments.objects.filter(agent=request.user).order_by('-date_created')
    serializer = CashPaymentsSerializer(payment_today, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def make_cash_payments(request):
    serializer = CashPaymentsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_cash_payments(request):
    my_date = datetime.today()
    payments = MyCashPayments.objects.filter(payment_status="Pending").order_by('-date_created')
    serializer = CashPaymentsSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_cash_payments(request):
    payments = MyCashPayments.objects.all().order_by('-date_created')
    serializer = CashPaymentsSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def approve_cash_request_paid(request, id):
    cash_request = get_object_or_404(CashRequest, id=id)
    serializer = CashRequestSerializer(cash_request, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def cash_payment_summary(request):
    user = get_object_or_404(User, username=request.user.username)
    my_payments = MyCashPayments.objects.filter(agent=user).order_by('-date_created')
    serializer = CashPaymentsSerializer(my_payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_cash_requests_for_today(request):
    my_date = datetime.today()
    de_date = my_date.date()
    your_cash_requests = CashRequests.objects.filter(agent=request.user).filter(
        deposited_month=de_date.month).filter(deposited_year=de_date.year).filter(request_paid="Not Paid").order_by(
        '-date_requested')
    serializer = CashRequestSerializer(your_cash_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def cash_payment_detail(request, pk):
    dpayment = MyCashPayments.objects.get(pk=pk)
    serializer = CashPaymentsSerializer(dpayment, many=False)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def approve_cash_payment(request, id):
    payment = get_object_or_404(MyCashPayments, id=id)
    serializer = CashPaymentsSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes([permissions.AllowAny])
def delete_cash_payment(request, id):
    try:
        user_payment = get_object_or_404(MyCashPayments, id=id)
        user_payment.delete()
    except User_Payment.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)

# for saving data
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_customer_requests_deposits(request):
    today_year = timezone.now().year
  
    request_deposits = CustomerRequestDeposit.objects.all().order_by("-date_requested")
    for notification in request_deposits:
        if notification.date_requested.year != today_year:
            notification.delete()
    
    serializer = CustomerDepositRequestSerializer(request_deposits, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_cash_at_payments(request):
    payments = CashAtPayments.objects.all().order_by("-date_paid")
    serializer = CashAtPaymentSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_fnet_customers(request):
    customers = Customer.objects.all().order_by("-date_created")
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_referred_customers(request):
    customers = ReferCustomer.objects.all().order_by("-date_created")
    serializer = ReferCustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_add_to_customers_points(request):
    customers = AddToCustomerPoints.objects.all().order_by("-date_created")
    serializer = AddToCustomerPointsSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_add_to_customers_redeemed_points(request):
    customers = AddToCustomerRedeemPoints.objects.all().order_by("-date_created")
    serializer = AddToCustomerRedeemPointsSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_customers_accounts_registered(request):
    customers = CustomerAccounts.objects.all().order_by("-date_added")
    serializer = CustomerAccountsSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_expenses(request):
    today_year = timezone.now().year
  
    users = ExpensesRequest.objects.all().order_by("-date_requested")
    for user in users:
        if user.date_requested.year != today_year:
            user.delete()
    serializer = ExpenseRequestSerializer(users, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_bank_requests_deposits(request):
    today_year = timezone.now().year
  
    deposits = BankDeposit.objects.all().order_by("-date_requested")
    for deposit in deposits:
        if deposit.date_requested.year != today_year:
            deposit.delete()
    
    serializer = BankDepositSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_add_to_approved_requests_deposits(request):
    deposits = AddedToApprovedDeposits.objects.all().order_by("-date_approved")
    serializer = AddedToApprovedBankDepositsSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_mobile_money_deposit_requests_deposits(request):
    today_year = timezone.now().year
  
    deposits = MobileMoneyDeposit.objects.all().order_by("-date_deposited")
    for deposit in deposits:
        if deposit.date_deposited.year != today_year:
            deposit.delete()
    
    serializer = MobileMoneyDepositSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_mobile_money_withdrawal_requests_deposits(request):
    today_year = timezone.now().year
  
    deposits = MobileMoneyWithdraw.objects.all().order_by("-date_of_withdrawal")
    for deposit in deposits:
        if deposit.date_of_withdrawal.year != today_year:
            deposit.delete()
    
    serializer = MobileMoneyWithdrawalSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_mobile_money_accounts_started(request):
    today_year = timezone.now().year
  
    deposits = UserMobileMoneyAccountsStarted.objects.all().order_by("-date_posted")
    for deposit in deposits:
        if deposit.date_posted.year != today_year:
            deposit.delete()
    
    serializer = UserMobileMoneyAccountsStartedSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_mobile_money_accounts_closed(request):
    today_year = timezone.now().year
  
    deposits = UserMobileMoneyAccountsClosed.objects.all().order_by("-date_posted")
    for deposit in deposits:
        if deposit.date_posted.year != today_year:
            deposit.delete()
    
    serializer = UserMobileMoneyAccountsClosedSerializer(deposits, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_customers_withdrawals(request):
    withdrawals = CustomerWithdrawal.objects.all().order_by("-date_requested")
    serializer = CustomerWithdrawalSerializer(withdrawals, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_bank_payments(request):
    today_year = timezone.now().year
  
    payments = MyPayments.objects.all().order_by("-date_created")
    for deposit in payments:
        if deposit.date_created.year != today_year:
            deposit.delete()
    
    serializer = PaymentsSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_added_to_approved_payments(request):
    today_year = timezone.now().year
  
    payments = AddedToApprovedPayment.objects.all().order_by("-date_approved")
    for deposit in payments:
        if deposit.date_approved.year != today_year:
            deposit.delete()
    
    serializer = AddedToApprovedPaymentSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_admin_accounts_started_with(request):
    today_year = timezone.now().year
  
    accounts_started = AdminAccountsStartedWith.objects.all().order_by("-date_started")
    for deposit in accounts_started:
        if deposit.date_started.year != today_year:
            deposit.delete()
    
    serializer = AdminAccountsStartedSerializer(accounts_started, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_admin_accounts_with_with(request):
    today_year = timezone.now().year
  
    accounts_started = AdminAccountsCompletedWith.objects.all().order_by("-date_closed")
    for deposit in accounts_started:
        if deposit.date_closed.year != today_year:
            deposit.delete()
    
    serializer = AdminAccountsCompletedSerializer(accounts_started, many=True)
    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_fnet_notifications(request):
    today_year = timezone.now().year
  
    fnotifications = Notifications.objects.all().order_by("-date_created")
    for notification in fnotifications:
        if notification.date_created.year != today_year:
            notification.delete()
    serializer = NotificationSerializer(fnotifications, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_payment_at_bank(request):
    today_year = timezone.now().year
  
    payments = PaymentAtBank.objects.all().order_by("-date_added")
    for deposit in payments:
        if deposit.date_added.year != today_year:
            deposit.delete()
    
    serializer = PaymentAtBankSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_customers_payment_at_bank(request):
    payments = CustomerPaymentAtBank.objects.all().order_by("-date_added")
    serializer = CustomerPaymentAtBankSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_reports(request):
    today_year = timezone.now().year
    reports = Reports.objects.all().order_by("-date_reported")
    for deposit in reports:
        if deposit.date_reported.year != today_year:
            deposit.delete()
    serializer = ReportsSerializer(reports, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_fnet_messages(request):
    fnetmessages = FnetGroupMessage.objects.all().order_by("-timestamp")
    serializer = FnetGroupMessageSerializer(fnetmessages, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_fnet_messages_chat_id(request):
    chat_id = PrivateChatId.objects.all().order_by("-date_created")
    serializer = PrivateChatIdSerializer(chat_id, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_fnet_private_chat_messages(request):
    pmessages = FnetPrivateUserMessage.objects.all().order_by("-timestamp")
    serializer = FnetPrivateUserMessageSerializer(pmessages, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_blocked_lists(request):
    blockedlists = AddToBlockList.objects.all().order_by("-date_blocked")
    serializer = AddToBlockListSerializer(blockedlists, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_cash_request_deposits(request):
    cash_requests = CashRequest.objects.all().order_by("-date_requested")
    serializer = CashRequestSerializer(cash_requests, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_cash_payments(request):
    cash_payments = MyCashPayments.objects.all().order_by("-date_created")
    serializer = CashPaymentsSerializer(cash_payments, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_users_added_to_approved_cash_payments(request):
    cash_payments = AddedToApprovedCashPayment.objects.all().order_by("-date_approved")
    serializer = AddedToApprovedCashPaymentSerializer(cash_payments, many=True)
    return Response(serializer.data)


# deleting from database
# my_date = datetime.today()
# de_date = my_date.date()
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def delete_all_customer_requests_deposits(request):
    my_date = datetime.today()
    de_date = my_date.date()
    deposit = CustomerRequestDeposit.objects.exclude(date_requested=de_date).order_by("-date_requested")
    # request_deposits = CustomerRequestDeposit.objects.all().order_by("-date_requested")
    for i in deposit:
        i.delete()
    serializer = CustomerDepositRequestSerializer(deposit, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_withdraw_reference(request):
    serializer = WithdrawalReferenceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_customer_bank_withdrawal_summary(request):
    summary = CustomerWithdrawal.objects.filter(agent=request.user).order_by("-date_requested")
    serializer = CustomerWithdrawalSerializer(summary,many=True)
    return Response(serializer.data)

# unpaid cash deposits

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_agents_unpaid_cash_request_deposits(request):
    deposits = CashRequest.objects.filter(request_paid="Not Paid").order_by('-date_requested')
    serializer = CashRequestSerializer(deposits, many=True)
    return Response(serializer.data)