from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import filters as filterr
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializer import *
from rest_framework.pagination import PageNumberPagination


class UserFilter(filters.FilterSet):

    class Meta:
        model = User
        fields = ['username']

class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 20
    def get_paginated_response(self, data):
         return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'results': data
        })

class InternList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Intern.objects.all()
    serializer_class = InternSerializer
    pagination_class = BasicPagination

class InternUsernameList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Intern.objects.all()
    serializer_class = InternSerializer
    pagination_class = BasicPagination
    def get_queryset(self):
        queryset = self.queryset.filter(user__user__username = self.request.GET['username'])
        return queryset

class Company_UserList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Company_User.objects.all()
    serializer_class = Company_UserSerializer
    pagination_class = BasicPagination

class CategoryList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = BasicPagination

class GithubList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Github.objects.all()
    serializer_class = GithubSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)

class CompanyList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer     
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,filterr.SearchFilter,filterr.OrderingFilter,)
    filter_fields = ('name','email',)
    search_fields = ('name', 'email')
    ordering_fields = ('name', 'email')

class SiteAdminList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)
    queryset = SiteAdmin.objects.all()
    serializer_class = SiteAdminSerializer     
    pagination_class = BasicPagination

class SkillList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer     
    pagination_class = BasicPagination

class DegreeList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer     
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)

class JobList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Job.objects.all()
    serializer_class = JobSerializer     
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)


class ProjectList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer     
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)

class InternshipReadList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Internship.objects.all()
    pagination_class = BasicPagination
    serializer_class = InternshipReadSerializer
    filter_backends = (DjangoFilterBackend,filterr.SearchFilter,filterr.OrderingFilter,)
    filter_fields = ('company','start','approved','skills','PPO','free_snacks','letter_of_recommendation','free_snacks','flexible_work_hours','certificate','informal_dress_code')
    search_fields = ('catagory', 'stipend','location','responsibilities','skills')
    ordering_fields = ('start', 'duration')

class InternshipList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Internship.objects.all()
    pagination_class = BasicPagination
    serializer_class = InternshipSerializer


class SubmissionList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    pagination_class = BasicPagination

class QuestionList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = BasicPagination

class AnswerList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    pagination_class = BasicPagination
