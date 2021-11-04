from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ProfileSerializer
from .models import Profile, User
from django.shortcuts import render,get_object_or_404
from .permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def profile(request):
    user = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)


def fnet_home(request):
    return render(request, "users/fnet_home.html")
