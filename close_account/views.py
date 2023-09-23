from django.shortcuts import render,get_object_or_404
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from .models import CloseAccount
from .serializers import CloseAccountSerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def close_accounts(request):
    serializer = CloseAccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_my_closed_accounts(request):
    my_accounts = CloseAccount.objects.filter(agent=request.user).order_by('-date_created')
    serializer = CloseAccountSerializer(my_accounts, many=True)
    return Response(serializer.data)

@api_view(['GET','PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_my_accounts_detail(request,pk):
    account = get_object_or_404(CloseAccount, pk=pk)
    serializer = CloseAccountSerializer(account,data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_account(request, id):
    try:
        closed_account = get_object_or_404(CloseAccount, id=id)
        closed_account.delete()
    except CloseAccount.DoesNotExist:
        return Http404
    return Response(status=status.HTTP_204_NO_CONTENT)
