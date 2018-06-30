from django.contrib.auth.models import User, Group
from django.contrib import admin
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework import filters as rffilter
# refactor this
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters as filterr
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializer import *
from django.http import Http404
from .pagination import *

class DurationFilterBackend(filterr.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if "duration" in request.GET and request.GET['duration'] != '':
            return queryset.filter(duration__lte=request.GET["duration"])
        elif "start" in request.GET and request.GET['start'] != '':
            return queryset.filter(start__gte=request.GET["start"])
        else:
            return queryset

class InternshipFilterBackend(filterr.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if "internship" in request.GET and request.GET['internship'] != '':
            return queryset.filter(internship__id_code=request.GET["internship"])
        else:
            return queryset

class CodeIdFilterBackend(filterr.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'id' in request.GET:
            id = request.GET['id']
            code = id[-4:]
            id = id[:-4]
            queryset = queryset.filter(id = id,code=code)
            if len(list(queryset)) >0:
                return queryset
            else:
                return NotFound()
        return queryset

class UsernameFilterBackend(filterr.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if "username" in request.GET:
            return queryset.filter(user__user__username=request.GET["username"])
        else:
            return queryset

            
class InternList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Intern.objects.all()
    serializer_class = InternSerializer
    pagination_class = BasicPagination
    filter_backends = (UsernameFilterBackend,)

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
    filter_backends = (DjangoFilterBackend,filterr.SearchFilter,filterr.OrderingFilter,)
    filter_fields = ('id','email',)
    search_fields = ('name', 'email')
    ordering_fields = ('name', 'email')

class SiteAdminList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)
    queryset = SiteAdmin.objects.all()
    serializer_class = SiteAdminSerializer

class SkillList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class DegreeList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)

class JobList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)

class ProjectList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)


class InternshipReadList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Internship.objects.all()
    pagination_class = BasicPagination
    serializer_class = InternshipReadSerializer
    filter_backends = (DjangoFilterBackend,filterr.SearchFilter,filterr.OrderingFilter,DurationFilterBackend,CodeIdFilterBackend)
    filter_fields = ('category','location','company','approved','skills','PPO','free_snacks','letter_of_recommendation','free_snacks','flexible_work_hours','certificate','informal_dress_code')
    search_fields = ('category','stipend','location','responsibilities','skills__name')
    ordering_fields = ('start', 'duration')

class InternshipList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer

def update(request):
    for i in Internship.objects.all():
        i.id_code = str(i.id) + str(i.code)
        i.save()
    return Http404

class SubmissionList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern','status')

class SubmissionInternReadList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Submission.objects.all()
    serializer_class = SubmissionInternReadSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,InternshipFilterBackend,)
    filter_fields = ('intern',)

class SubmissionCompanyReadList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Submission.objects.all()
    serializer_class = SubmissionCompanyReadSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,InternshipFilterBackend,)

class QuestionList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = BasicPagination
    filter_backends = (InternshipFilterBackend,)
    '''
    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function 
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(QuestionSerializer, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        '''


class AnswerList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('question',)
    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function 
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(AnswerSerializer, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)