from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializer import *

class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

