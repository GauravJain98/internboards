from .models import *
from rest_framework import permissions
from django.contrib.auth.models import User
from oauth.models import AuthToken
'''

class IsAuthenticated2(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'HTTP_ACCESSTOKEN' in request.META:

            return False
        else:
            return True
        return False

            
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
'''

class InternPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'HTTP_ACCESSTOKEN' in request.META:
            token = request.META['HTTP_ACCESSTOKEN']
            user = AuthToken.objects.select_related('user').get(token = token).user
            intern = Intern.objects.filter(user__user = user).exists()
            return intern
        return False

class Company_UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'HTTP_ACCESSTOKEN' in request.META:
            token = request.META['HTTP_ACCESSTOKEN']
            user = AuthToken.objects.select_related('user').get(token = token).user
            company_user = Company_User.objects.filter(user__user = user).exists()
            return company_user
        return False