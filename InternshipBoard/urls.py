"""InternshipBoard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
#change the router to sim
router.register(r'intern/add', views.InternAddList)
router.register(r'companyuser/add', views.Company_UserAddList)
router.register(r'intern', views.InternList)
router.register(r'companyuser', views.Company_UserList)
router.register(r'category', views.CategoryList)
router.register(r'company', views.CompanyList)
router.register(r'siteadmin', views.SiteAdminList)
router.register(r'skill', views.SkillList)
router.register(r'submit', views.Submit)
#router.register(r'resume', views.Resume , base_name='resume')
router.register(r'degree', views.DegreeList)
router.register(r'job', views.JobList)
router.register(r'github', views.GithubList)
router.register(r'project', views.ProjectList)
#router.register(r'hiring', views.HiringList)
router.register(r'internship/read/company', views.InternshipSubReadList, base_name="Internship")
router.register(r'internship/read', views.InternshipReadList, base_name="Internship")
router.register(r'internship', views.InternshipList)
#router.register(r'internshipavaliable', views.InternshipAvaliableList)

router.register(r'submission/intern', views.SubmissionInternReadList)
#router.register(r'submission/company', views.SubmissionCompanyReadList)
router.register(r'submission', views.SubmissionList)
router.register(r'question', views.QuestionList)
router.register(r'answer/read', views.AnswerReadList)
router.register(r'answer', views.AnswerList)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth.urls')),
    path('callback/', include('clientSide.urls')),
    path('update/', views.update),
    path('resume/', views.resume),
    path('submission/company', views.submissionCompany),
   url(r'^', include(router.urls))
]
