from rest_framework import permissions
from datetime import datetime, timezone
from .models import AuthToken
from django.core.cache import cache
#revoke auth check

class IsAuthenticated2(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'HTTP_ACCESSTOKEN' in request.META:
            token = AuthToken.objects.filter(token = request.META['HTTP_ACCESSTOKEN'],revoked = False)
            # if cache.get(str(token)) is None:
            if token.exists():
                token = list(token)[0]
                if (datetime.now(timezone.utc) - token.added).total_seconds() > token.expires :
                    token.revoked = True
                    token.save()
                    return False
                else:
                #        data = cache.set(str(token),True ,3600*24)
                    return True
            else:
                return False
            # else:
            #     return cache.get(str(token))
        return False

'''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
'''