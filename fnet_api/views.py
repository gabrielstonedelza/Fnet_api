from django.shortcuts import render, get_object_or_404
from .serializers import FNetAdminSerializer, CustomerSerializer, AgentDepositRequestSerializer, \
    CustomerWithdrawalSerializer, PaymentsSerializer

from .models import FNetAdmin, Customer, AgentDepositRequests, CustomerWithdrawal, Payments
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from users.models import User
from users.serializers import UsersSerializer


@api_view(['GET'])
def get_agent_requests(request):
    # guarantor = get_object_or_404(FNetAdmin, user=user)
    all_agents_requests = AgentDepositRequests.objects.all().order_by('-date_requested')
    serializer = AgentDepositRequestSerializer(all_agents_requests, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
def approve_request(request, id):
    agent_request = get_object_or_404(AgentDepositRequests, id=id)
    serializer = AgentDepositRequestSerializer(agent_request, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_customer(request, username):
    agent = get_object_or_404(User, username=username)
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=agent)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def agent_deposit_request(request, username):
    agent = get_object_or_404(User, username=username)
    serializer = AgentDepositRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=agent)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def customer_withdrawal(request, username):
    agent = get_object_or_404(User, username=username)
    serializer = CustomerWithdrawalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=agent)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_agents(request):
    users = User.objects.all().order_by('-date_joined')
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_customers(request):
    customers = Customer.objects.all().order_by('-date_created')
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def agent_customers_summary(request, username):
    user = get_object_or_404(User, username=username)
    customers = Customer.objects.filter(agent=user).order_by('-date_created')
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def deposit_request_summary(request, username):
    user = get_object_or_404(User, username=username)
    depo_requests = AgentDepositRequests.objects.filter(agent=user).order_by('-date_requested')
    serializer = AgentDepositRequestSerializer(depo_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def customer_withdrawal_summary(request, username):
    user = get_object_or_404(User, username=username)
    c_withdrawals = CustomerWithdrawal.objects.filter(agent=user).order_by('-date_requested')
    serializer = CustomerWithdrawalSerializer(c_withdrawals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_payments(request):
    payments = Payments.objects.all().order_by('-date_created')
    serializer = PaymentsSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def make_payments(request, username):
    agent = get_object_or_404(User, username=username)
    serializer = PaymentsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=agent)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def approve_payment(request, id):
    payment = get_object_or_404(Payments, id=id)
    serializer = PaymentsSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
