from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ProfileSerializer
from .models import Profile
from django.shortcuts import render


@api_view(['GET'])
def profile(request):
    user = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
def profile_update(request, id):
    user_profile = Profile.objects.get(id=id)
    serializer = ProfileSerializer(user_profile, data=request.data)
    user = request.user
    if user_profile.user != user:
        return Response({"User: you are not authorized to edit this profile"})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def fnet_home(request):
    return render(request, "users/fnet_home.html")
