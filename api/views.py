from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializer import *

class InternList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,InternIPermission)
    queryset = Intern.objects.all()
    serializer_class = InternSerializer

class Company_UserList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,Company_UserCPermission)
    queryset = Company_User.objects.all()
    serializer_class = Company_UserSerializer

class CategoryList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class GithubList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,InternIPermission)
    queryset = Github.objects.all()
    serializer_class = GithubSerializer

