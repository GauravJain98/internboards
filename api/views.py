from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status, generics
from rest_framework import filters as rffilter
# refactor this
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth.permissions import IsAuthenticated2
from django.utils.timezone import now
from rest_framework import filters as filterr
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializer import *
from django.http import Http404
from .pagination import *
from .permissions import *

def send(html, email):
    sg =sendgrid.SendGridAPIClient(apikey='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')
    from_email = Email("contact@internboards.com")
    to_email = Email(email)
    subject = "Sending with SendGrid is Fun"
    if html == 1:
        content = Content("text/html", "<html><p>Hello, world!</p><h1>h1</h1><h2>h2</h2></html>")
    if html == 2:
        content = Content("text/html", "<html><p>Hello, world!</p><h1>h1</h1><h2>h2</h2></html>")
    if html == 3:
        content = Content("text/html", "<html><p>Hello, world!</p><h1>h1</h1><h2>h2</h2></html>")
    if html == 4:
        content = Content("text/html", "<html><p>Hello, world!</p><h1>h1</h1><h2>h2</h2></html>")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

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

class FullInternshipFilterBackend(filterr.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        subs = Submission.objects.filter(status=1)
        queryset.filter(visibility__gt = now())
        for query in queryset:
            sub = subs.filter(internship = query)
            if len(sub) > 100:
                queryset.exclude(id = query.id)
            '''
            if datetime.now() > query.visibility:
                queryset.exclude(id = query.id)
            '''
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
                raise Http404
        return queryset

class UsernameFilterBackend(filterr.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if "username" in request.GET:
            return queryset.filter(user__user__username=request.GET["username"])
        else:
            return queryset

class InternAddList(viewsets.ModelViewSet):
    queryset = Intern.objects.all()
    serializer_class = InternAddSerializer
    http_method_names = ['post', 'options']

class Company_UserAddList(viewsets.ModelViewSet):
    queryset = Company_User.objects.all()
    serializer_class = Company_UserSerializer
    http_method_names = ['post', 'options']
        
class InternList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Intern.objects.all()
    serializer_class = InternSerializer
    pagination_class = BasicPagination
    filter_backends = (UsernameFilterBackend,)

class Company_UserList(viewsets.ModelViewSet):
    queryset = Company_User.objects.all()
    serializer_class = Company_UserSerializer
    pagination_class = BasicPagination
    filter_backends = (UsernameFilterBackend,)

class CategoryList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = BasicPagination


class GithubList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Github.objects.all()
    serializer_class = GithubSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)

class CompanyList(viewsets.ModelViewSet):
#   added permission to add
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (DjangoFilterBackend,filterr.SearchFilter,filterr.OrderingFilter,)
    filter_fields = ('id','email',)
    search_fields = ('name', 'email')
    ordering_fields = ('name', 'email')

class SiteAdminList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,permissions.IsAdminUser)
    queryset = SiteAdmin.objects.all()
    serializer_class = SiteAdminSerializer
    pagination_class = BasicPagination

class SkillList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,InternPermission)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class DegreeList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)

class JobList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Job.objects.all()
    pagination_class = BasicPagination
    serializer_class = JobSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)

class ProjectList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)

class InternshipReadList(viewsets.ModelViewSet):
    pagination_class = BasicPagination
    serializer_class = InternshipReadSerializer
    filter_backends = (DjangoFilterBackend,filterr.SearchFilter,filterr.OrderingFilter,DurationFilterBackend,CodeIdFilterBackend,FullInternshipFilterBackend)
    filter_fields = ('category','location','company','approved','skills','PPO','free_snacks','letter_of_recommendation','free_snacks','flexible_work_hours','certificate','informal_dress_code')
    search_fields = ('category','stipend','location','responsibilities','skills__name')
    ordering_fields = ('start', 'duration')

    def get_queryset(self):
        intern = getIntern(self.request)
        queryset = Internship.objects.all()
        
        if not intern or 'id' in self.request.GET:
            return queryset
        submissions= Submission.objects.select_related('internship').filter(intern = intern)
        for submission in submissions:
            queryset = queryset.exclude(id = submission.internship.id)
        return queryset

class InternshipSubReadList(viewsets.ModelViewSet):
    pagination_class = BasicPagination
    serializer_class = InternshipReadSubSerializer
    filter_backends = (DjangoFilterBackend,filterr.SearchFilter,filterr.OrderingFilter,DurationFilterBackend,CodeIdFilterBackend)
    filter_fields = ('category','location','company','approved','skills','PPO','status','visibility','free_snacks','letter_of_recommendation','free_snacks','flexible_work_hours','certificate','informal_dress_code')
    search_fields = ('category','stipend','location','responsibilities','skills__name')
    ordering_fields = ('start', 'duration')

    def get_queryset(self):
        queryset = Internship.objects.all()
        
        return queryset

class InternshipList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer

def update(request):
    for i in Internship.objects.all():
        i.id_code = str(i.id) + str(i.code)
        i.save()
    return Http404

class SubmissionList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern','status','internship')

class SubmissionInternReadList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Submission.objects.all()
    serializer_class = SubmissionInternReadSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,InternshipFilterBackend,)
    filter_fields = ('intern','status',)

class Submit(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmitSerializer

class Resume(ObjectMultipleModelAPIView):

    querylist = (
        {
            'queryset': Project.objects.all(), 
            'serializer_class': ProjectSerializer,
            'label':'project',
        },
        {
            'queryset': Job.objects.all(), 
            'serializer_class': JobSerializer,
            'label':'job',
        }
    )

class SubmissionCompanyReadList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Submission.objects.all()
    serializer_class = SubmissionCompanyReadSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('intern',)

class QuestionList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = BasicPagination
    filter_backends = (InternshipFilterBackend,)
    '''
    de' create(self, request, *args, **kwargs):
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
    permission_classes  = (IsAuthenticated2,)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('question',)

class AnswerReadList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Answer.objects.all()
    serializer_class = AnswerReadSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('submission',)
