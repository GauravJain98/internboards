from .models import *
from rest_framework import permissions
from django.contrib.auth.models import User
from oauth.models import AuthToken
from django.core.cache import cache
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
#            if cache.get(token) is None:
            user = AuthToken.objects.select_related('user').get(token = token).user
            intern = list(Intern.objects.filter(user__user = user))
                #if len(intern) > 0:
               #     cache.set(token ,{'user':intern[0],'type':'intern'} , 3600*24)
            return len(intern) > 0
            # else:
            #     data = cache.get(token)
            #     return data.type == 'intern'
        return False

class Company_UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'HTTP_ACCESSTOKEN' in request.META:
            token = request.META['HTTP_ACCESSTOKEN']
            # if cache.get(token) is None:
            user = AuthToken.objects.select_related('user').get(token = token).user
            companyuser = list(Company_User.objects.filter(user__user = user))
            #    if len(companyuser) > 0:
            #        cache.set(token ,{'user':companyuser[0],'type':'companyuser'} , 3600*24)
            return len(companyuser) > 0
            # else:
            #     data = cache.get(token)
            #     return data.type == 'companyuser'
        return False