from .models import *
from rest_framework import permissions
from django.contrib.auth.models import User
from oauth.models import AuthToken

class InternPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        token = request.data['token']
        user = AuthToken.objects.select_related('user').get(token = token).user
        intern = Intern.objects.filter(user__user = user).exists()
        return intern

class Company_UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = AuthToken.objects.select_related('user').get(token = token).user
        company_user = Company_User.objects.filter(user__user = user).exists()
        return company_user
