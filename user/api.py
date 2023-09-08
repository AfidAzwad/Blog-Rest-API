from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User

class RegisterApi(generics.GenericAPIView):
    return True