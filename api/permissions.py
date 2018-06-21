from .models import *
from rest_framework import permissions
from django.contrib.auth.models import User
admin.autodiscover()

class InternPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        intern = Intern.objects.filter(user = request.user).exists()
        return intern

class Company_UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        company_user = Company_User.objects.filter(user = request.user).exists()
        return company_user
