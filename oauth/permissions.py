from rest_framework import permissions
from datetime import datetime, timezone
from .models import AuthToken

class IsAuthenticated2(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'HTTP_ACCESSTOKEN' in request.META:
            token = AuthToken.objects.filter(token = request.META['HTTP_ACCESSTOKEN'],revoked = False)
            if token.exists():
                token = list(token)[0]
                if ( datetime.now(timezone.utc) - token.added).total_seconds() > token.expires :
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