from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ProfileSerializer
from .models import Profile, User
from django.shortcuts import render, get_object_or_404
from .permissions import IsOwnerOrReadOnly


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    user = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)


def fnet_home(request):
    return render(request, "users/fnet_home.html")


@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    my_profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(my_profile, data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
