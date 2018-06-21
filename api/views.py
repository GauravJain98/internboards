from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializer import *
admin.autodiscover()

class InternPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        intern = Intern.objects.filter(user = request.user).exists()
        return intern

class Company_UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        company_user = Company_User.objects.filter(user = request.user).exists()
        return company_user

class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

