from django.shortcuts import redirect
from django.http import HttpResponse
import requests
from urllib.parse import urlencode
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from oauth.models import AuthToken, Client
import json
from api.models import Intern,Custom_User
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
        if not User.objects.filter(email = email,username=email):
            user = User.objects.create_user(username=email,email = email)
            cuser = Custom_User(user = user)
            user.save()
            cuser.save()
            intern = Intern(user=cuser)
            intern.save()
        else:
            user = User.objects.get(username=email,email = email)
            cuser = Custom_User.objects.get(user = user)
        auth_token = AuthToken(client= Client.objects.get(client_id='id'),user=user,revoked = False)
        auth_token.save()
        internurl = 'http://internboards.com/login/studentgiri?'
        return redirect(internurl+ urlencode({'access_token':auth_token.token,'username':user.username}))
    except:
        internurl = 'http://internboards.com/login/studentgiri?'
        return redirect(internurl+ urlencode({'access_token':'error'}))

@api_view(['GET'])
def githubRedirect(request):
    try:
        token = 'error'
        code = request.GET['code']
        client_id = "5e3d27cb56a6852a0293"
        redirect_uri = "http://api.internboards.com/callback/github"
        client_secret = "5705eda5cdfc8eda5c2c07cb4b30b78ca826ff75"
        url = "https://github.com/login/oauth/access_token"
        params = {
            "code":code,
            "client_id":client_id,
            "client_secret":client_secret,
            "redirect_uri":redirect_uri
        }
        url = "https://github.com/login/oauth/access_token?"
        data=requests.post(url, data = params,headers = {'Accept': 'application/json'})
        access_token = data.json()['access_token']
        params = {
            'access_token':access_token,
            'scope':'email'
        }
        data = requests.get('https://api.github.com/user?access_token=' + access_token).json()
        email = data['email']
        following = data['following']
        follower = data['follower']
        handle = data['login']
        origanization = data['origanization']
        owned_private_repo = data
        name = data['name']
        if not User.objects.filter(email = email,username=email):
            user = User.objects.create_user(username=email,email = email)
            cuser = Custom_User(user = user)
            user.save()
            cuser.save()
            intern = Intern(user=cuser)
            intern.save()
        else:
            user = User.objects.get(username=email,email = email)
            cuser = Custom_User.objects.get(user = user)
        github = Github(follower=follower,following=following,handle=handle,intern=intern,owned_private_repo=owned_private_repo,stars = stars,repositories=repositories,origanization_url = origanization_url,owned_public_repo=owned_public_repo,collaborators = collaborators,url = url)
        github.save()
        auth = AuthToken(user = user,revoked = False)
        auth.save()
        token = auth.token
        internurl = 'http://internboards.com/login/github?'
        return redirect(internurl+'access_token'+token)
    except:
        internurl = 'http://internboards.com/login/studentgiri?'
        return redirect(internurl+ urlencode({'access_token':'error'}))
