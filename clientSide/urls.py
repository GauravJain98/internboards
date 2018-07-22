from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import login,logout


urlpatterns = [
    path('github', views.githubRedirect,name='studentGiriRedirect'),
    path('tester', views.tester,name='studentGiriRedirect'),
    path('', views.studentGiriRedirect,name='studentGiriRedirect'),
]