from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, generics, status
from .models import PaymentAtBank
from .serializers import PaymentAtBankSerializer


# Create your views here.
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_at_bank(request):
    serializer = PaymentAtBankSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(agent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_data_at_bank(request):
    all_agents_bank_payment = PaymentAtBank.objects.all().order_by('-date_added')
    serializer = PaymentAtBankSerializer(all_agents_bank_payment, many=True)
    return Response(serializer.data)
