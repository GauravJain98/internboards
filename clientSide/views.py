from django.shortcuts import redirect
from django.http import HttpResponse
import requests
from urllib.parse import urlencode
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from oauth.models import AuthToken
import json
from rest_framework.response import Response

@api_view(['GET'])
def studentGiriRedirect(request):
    try:
        code = request.GET['code']
        client_id = "1729786746660238"
        redirect_uri = "http://api.internboards.com/callback"
        client_secret = "GXpqf31Rs8ofodRiQZqZX79QgJiF2Dyw47sj3R67"
        url = "https://accounts.studentgiri.com/token/"
        params = {
            "code":code,
            "client_id":client_id,
            "client_secret":client_secret,
            "redirect_uri":redirect_uri,
            "grant_type":"authorization_code"
        }
        data=requests.post(url, data = params).json()
        access_token = data["access_token"]
        url = "https://accounts.studentgiri.com/v1.0/me/?"
        params = {
            'access_token':access_token,
            'scope':'email'
        }
        data = requests.get(url +urlencode(params))
        email = data.json()['email']
        name = data.json()['name']
        if not User.objects.filter(email = email):
            user = User.objects.create_user(username=email,email = email)
            user.save
        user = User.objects.get(email = email)
        auth_token, created = AuthToken.objects.get_or_create(client__client_id='id',user=user)
        if not created:
            auth_token.save()
        internurl = 'http://internboards.com/login/studentgiri?'
        return redirect(internurl+ urlencode({'access_token':auth_token.token,'username':user.username}))
    except:
        internurl = 'http://internboards.com/login/studentgiri?'
        return redirect(internurl+ urlencode({'access_token':'error'}))


def githubRedirect(request):
    try:
        code = request.GET['code']
        client_id = "5e3d27cb56a6852a0293"
        redirect_uri = "http://api.internboards/callback/github"
        client_secret = "5705eda5cdfc8eda5c2c07cb4b30b78ca826ff75"
        url = "https://github.com/login/oauth/access_token?"
        params = {
            "code":code,
            "client_id":client_id,
            "client_secret":client_secret,
            "redirect_uri":redirect_uri
        }
        data=requests.post(url, data = params)
        access_token = data.json()['access_token']
        url = "https://api.github.com/user?"
        params = {
            'access_token':access_token,
            'scope':'email'
        }
        data = requests.get(url +urlencode(params))
        return Response(data)
        email = data.json()['email']
        name = data.json()['name']
        if not User.objects.filter(email = email):
             user = User.objects.create_user(email = email,user=user)
             user.save
        user = User.objects.get(email = email)
        auth = AuthToken(user = user)
        auth.save()
        internurl = 'http://internboards.com/login/github'
        return redirect(internurl+ urlencode({'access_token':auth.token}))
    except:
        internurl = 'http://internboards.com/login/github'
        return redirect(internurl+ urlencode({'access_token':'error'}))
