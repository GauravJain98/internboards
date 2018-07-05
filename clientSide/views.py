from django.shortcuts import render
from django.http import HttpResponse
import requests
from urllib.parse import urlencode
from django.contrib.auth.models import User
from oauth.models import AuthToken
# Create your views here.

def studentGiriRedirect(request):
    try:
        code = request.GET['code']
        client_id = "1729786746660238"
        redirect_uri = "http://api.internboards/callback/studentgiri"
        client_secret = "GXpqf31Rs8ofodRiQZqZX79QgJiF2Dyw47sj3RH6"
        url = "https://accounts.studentgiri.com/token/"
        params = {
            "code":code,
            "client_id":client_id,
            "client_secret":client_secret,
            "redirect_uri":redirect_uri,
            "grant_type":"authorization_code"
        }
        data=requests.post(url, data = params)
        access_token = data.json()['access_token']
        url = "https://accounts.studentgiri.com/v1.0/me/?"
        params = {
            'access_token':access_token,
            'scope':'email'
        }
        data = requests.get(url +urlencode(params))
        email = data.json()['email']
        name = data.json()['name']
        if not User.objects.filter(email = email):
             user = User.objects.create_user(email = email,user=user)
             user.save
        user = User.objects.get(email = email)
        auth = AuthToken(user = user)
        auth.save()
        internurl = 'http://internboards.com'
        return redirect(internurl+ urlencode({'access_token':auth.token}))
    except:
        return redirect(internurl+ urlencode({'access_token':'error'}))
