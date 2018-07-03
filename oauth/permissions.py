from rest_framework import permissions
from datetime import datetime

class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if ('access_token'  request.data):
            token = Auth.objects.filter(token = request.data['access_token'],revoked = False):
            if token.exists():
                if (datetime.now - token.added).total_seconds > token.expire :
                    token.revoked = True
                    token.save()
                    return False
                else:
                    return True
        return False

            
'''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
'''