from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
from rest_framework import viewsets
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializer import *
admin.autodiscover()

class UserList(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupList(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
