from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import *
from django.contrib.auth import authenticate, login
from api.models import Intern,Company_User

def refresh(obj):
    token = sub('-','',str(uuid4()))
    while AuthToken.objects.filter(token = token).exists():
        token = sub('-','',str(uuid4()))
    obj.token = token
    refresh_token = sub('-','',str(uuid4()))
    while AuthToken.objects.filter(refresh_token = refresh_token).exists():
        token = sub('-','',str(uuid4()))
    obj.refresh_token = refresh_token
    obj.save()

@api_view(['POST'])
def token(request):
    data = request.data
    err = {}
    expire = 3600*720
    if 'clientid' not in data:
        err['clientid'] = 'required'
    if 'clientsecret' not in data:
        err['clientsecret'] = 'required'
    if 'granttype' not in data:
        err['granttype'] = 'required'
    if err:
        return Response({'error/s':err},status= status.HTTP_400_BAD_REQUEST)
    if data['granttype'] == 'password':
        if 'username' not in data:
            err['username'] = 'required'
        if 'password' not in data:
            err['password'] = 'required'
        if 'usertype' not in data:
            err['usertype'] = 'required'
        else:
            if data['usertype'] not in ('intern','company'):
                err['usertype'] = 'invalid user'
    elif data['granttype'] == 'refeshtoken':
        if 'refreshtoken' not in data:
            err['refreshtoken'] = 'required'
    else:
        return Response({'error':'unsupported grant type'})
    if err:
        return Response({'error/s':err},status= status.HTTP_400_BAD_REQUEST)
    else:
        client = Client.objects.filter(client_id = data['clientid'],client_secret = data['clientsecret'])
        if client.exists():
            if data['granttype'] == 'password':
                if data['usertype'] == 'intern':
                    user = Intern.objects.select_related('user__user').filter(user__user__username = data['username'])
                if data['usertype'] == 'company':
                    user = Company_User.objects.select_related('user__user').filter(user__user__username = data['username'])
                if not user.exists():
                    return Response({'error':'Invalid user'},status= status.HTTP_401_UNAUTHORIZED)
                else:
                    user = list(user)[0]
                auth = authenticate(username=data['username'], password=data['password'])
                if auth:
                    token = AuthToken(client = list(client)[0],user = user.user.user,expires = expire)
                    token.save()
                    return Response({
                        'token':token.token,
                        'refreshtoken':token.refresh_token,
                        'expires':token.expires,
                        'user':data['username']
                    })
                else:
                    return Response({'error':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
            elif data['granttype'] == 'refeshtoken':
                token = AuthToken.objects.select_related('user').filter(refresh_token = data['refreshtoken'])
                if token.exists() and not token.first().revoked:
                    if (datetime.now - token.added).total_seconds > token.expire :
                        return Response({'error':'time expired'},status= status.HTTP_401_UNAUTHORIZED)
                    token = list(token)[0]
                    refresh(token)
                    return Response({
                        'token':token.token,
                        'refreshtoken':token.refresh_token,
                        'expires':token.expires,
                        'user':token.user.username
                    })
                else:
                    err = 'invalid token'
            else:
                return Reponse({'error':'unsupported grant type'})
        else:
            err = 'invalid client'
    return Response({'error/s':err},status= status.HTTP_400_BAD_REQUEST)
 

@api_view(['POST'])
def revoke(request):
    data = request.data
    err = {}
    if 'client_id' not in data:
        err['client_id'] = 'required'
    if 'client_secret' not in data:
        err['client_secret'] = 'required'
    if 'token' not in data:
        err['token'] = 'required'
    if err:
        return Response({'error/s':err})
    else:
        client = Client.objects.filter(client_id = data['client_id'],client_secret = data['client_secret'])
        if client.exists():
            token = AuthToken.objects.filter(token = data['token'])
            if token.exists() and not token.first().revoked:
                token = list(token)[0]
                token.revoked = True
                token.save()
                return Response({'token':token.token,'revoked':True})
            else:
                err = 'already revoked'
        else:
            err = 'invalid client'
        return Response({'error/s':err})
