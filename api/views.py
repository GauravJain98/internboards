from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view,permission_classes
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status, generics
from rest_framework import filters as rffilter
import json
from django.db.models import Count,Value
from django.views.decorators.cache import cache_page
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
from functools import WRAPPER_ASSIGNMENTS, update_wrapper, wraps

def cache_me(cache):
    def true_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            self = args[0]
            instance = args[1]
            cache_key = '%s.%s' % (instance.facility, instance.id)
            logger.debug('%s cache_key: %s' % (cache, cache_key))
            if not self.request.method == 'PATCH':
                try:
                    data = caches[cache].get(cache_key)
                    if data is not None:
                        return data
                except:
                    pass
            else:
                return caches[cache].pop(cache_key)
            logger.info('did not cache')
            data = f(*args, **kwargs)
            try:
                caches[cache].set(cache_key, data)
            except:
                pass
            return data
        return wrapper
    return true_decorator

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

class DeleteFilter(filterr.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(archived = False)

class InternshipFilterBackend(filterr.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if "internship" in request.GET and request.GET['internship'] != '':
            return queryset.filter(internship__id_code=request.GET["internship"])
        else:
            return queryset

class FullInternshipFilterBackend(filterr.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
#        subs = list(Submission.objects.select_related('internship').filter(status=1))
        queryset.filter(visibility__gt = now())
        for query in queryset:
            j=0
            for sub in query.submission.all():
                if sub.status == 1:
                    j= j+1
            if j > 100 or query.status == -1:
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
    http_method_names = ['get','post', 'options']

class Company_UserAddList(viewsets.ModelViewSet):
    queryset = Company_User.objects.all()
    serializer_class = Company_UserSerializer
    http_method_names = ['post', 'options']

class InternList(viewsets.ModelViewSet):
#    permission_classes  = (IsAuthenticated2,)
    queryset = Intern.objects.select_related('user').select_related('user__user').select_related('user__address').prefetch_related('skills').all()
    serializer_class = InternSerializer
    pagination_class = BasicPagination
    filter_backends = (UsernameFilterBackend,DeleteFilter)


def loaderio(request):
    return HttpResponse('loaderio-31e01252bfb60d0ec0fbabd93985c4ca')

class Company_UserList(viewsets.ModelViewSet):
    queryset = Company_User.objects.select_related('user').select_related('user__address').select_related('user__user').all()
    serializer_class = Company_UserSerializer
    pagination_class = BasicPagination
    filter_backends = (UsernameFilterBackend,DeleteFilter)

class CategoryList(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = BasicPagination

    @cache_me('catagory')
    def to_representation(self, instance):
       return super(CategorySerializer, self).to_representation(instance)

class GithubList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Github.objects.all()
    serializer_class = GithubSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,DeleteFilter)
    filter_fields = ('intern',)

class CompanyList(viewsets.ModelViewSet):
#   added permission to add
    queryset = Company.objects.prefetch_related('hiring').prefetch_related('address').all()
    serializer_class = CompanySerializer
    filter_backends = (DjangoFilterBackend,filterr.SearchFilter,filterr.OrderingFilter,DeleteFilter)
    filter_fields = ('id','email',)
    search_fields = ('name', 'email')
    ordering_fields = ('name', 'email')

class SiteAdminList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)#,permissions.IsAdminUser)
    queryset = SiteAdmin.objects.select_related('user').select_related('user__address').select_related('user__user').all()
    serializer_class = SiteAdminSerializer
    pagination_class = BasicPagination

class SkillList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class DegreeList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Degree.objects.select_related('intern').all()
    serializer_class = DegreeSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,DeleteFilter)
    filter_fields = ('intern',)

class JobList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Job.objects.all()
    pagination_class = BasicPagination
    serializer_class = JobSerializer
    filter_backends = (DjangoFilterBackend,DeleteFilter)
    filter_fields = ('intern',)

class ProjectList(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('intern').all()
    serializer_class = ProjectSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,DeleteFilter)
    filter_fields = ('intern',)

@api_view(['GET'])
@permission_classes((IsAuthenticated2,))
def submissionCompany(request):
    try:
        status = request.GET['status']
    except:
        if 'id' in request.GET:
            id = request.GET['id']
        else:
            status = 0
    if 'id' in request.GET:
        internship = Internship.objects.select_related('company').get(id_code = "906559")
        cuser = Company_User.objects.select_related('company').filter(user__user = AuthToken.objects.get(token = request.META['HTTP_ACCESSTOKEN']).user)
        if cuser.count() == 0:
            return Response({
                "error":"Invalid user"
            })
        if internship.company != cuser.first().company:
            return Response({
                'error':'Internship does not exist'
            })
        submissions = Submission.objects.select_related('intern').prefetch_related('intern__skills').prefetch_related('answer').prefetch_related('answer__question').select_related('intern__user').select_related('intern__user__address').select_related('intern__user__user').select_related('internship').prefetch_related('internship__skills').prefetch_related('intern__jobs').prefetch_related('intern__degrees').prefetch_related('intern__projects').filter(internship = internship)#request.GET['internship'])
    else:
        submissions = Submission.objects.select_related('intern').prefetch_related('intern__skills').prefetch_related('answer').prefetch_related('answer__question').select_related('intern__user').select_related('intern__user__address').select_related('intern__user__user').select_related('internship').prefetch_related('internship__skills').prefetch_related('intern__jobs').prefetch_related('intern__degrees').prefetch_related('intern__projects').filter(internship__company = Company_User.objects.get(user__user = AuthToken.objects.get(token = request.META['HTTP_ACCESSTOKEN']).user).company).filter(status=status).filter(internship__id_code = request.GET['internship'])
    if 'id' in request.GET:
        counts = Submission.objects.all().values('status').annotate(total = Count('status'))
    else:
        counts = Submission.objects.filter(internship__company =Company_User.objects.get(user__user = AuthToken.objects.get(token = request.META['HTTP_ACCESSTOKEN']).user).company).filter(internship__id_code = request.GET['internship']).values('status').annotate(total = Count('status'))
    hired = 0
    shortlisted = 0
    review_period = 0
    interviewee = 0
    rejected = 0
    nextl = False
    if 'id' in request.GET:
        for submission in submissions:
            if nextl:
                nextl = submission.id
                print(nextl)
                submission = submissions.filter(id=id)
                break
            nextl = (str(submission.id) == str(id))
    if nextl == True:
        nextl =False
    for count in counts:
        if count['status'] == 4:
            hired = count['total']
        if count['status'] == 3:
            interviewee = count['total']
        if count['status'] == 2:
            shortlisted = count['total']
        if count['status'] == 1:
            review_period = count['total']
        if count['status'] == 0:
            rejected = count['total']
    res = {
        'next':nextl,
        'hired':hired,
        'shortlisted':shortlisted,
        'review_period':review_period,
        'rejected':rejected,
        'interviewee':interviewee,
        'submissions':[],
    }

    for submission_data in submissions:
        submission = SubmissionCompanyReadSerializer(submission_data,many=False).data
        degree = DegreeSerializer(submission_data.intern.degrees,many=True).data
        job = JobSerializer(submission_data.intern.jobs,many=True).data
        project = ProjectSerializer(submission_data.intern.projects,many=True).data
        questions = AnswerReadSerializer(submission_data.answer,many=True).data
        res['submissions'].append({
            'submission':submission,
            'projects':project,
            'jobs':job,
            'degrees':degree,
            'questions':questions,
        })
    return Response(res)

@api_view(['PATCH'])
def updateInternship(request,id):
    validate_data = {}
    body = json.loads(request.body.decode('utf-8'))
    if 'status' in body:
        validate_data['status'] = body['status']
    if 'category' in body:
        validate_data['category'] = body['category']
    if 'fixed' in body:
        validate_data['fixed'] = body['fixed']
    if 'stipend_rate' in body:
        validate_data['stipend_rate'] = body['stipend_rate']
    if 'certificate' in body:
        validate_data['certificate'] = body['certificate']
    if 'negotiable' in body:
        validate_data['negotiable'] = body['negotiable']
    if 'flexible_work_hours' in body:
        validate_data['flexible_work_hours'] = body['flexible_work_hours']
    if 'letter_of_recommendation' in body:
        validate_data['letter_of_recommendation'] = body['letter_of_recommendation']
    if 'free_snacks' in body:
        validate_data['free_snacks'] = body['free_snacks']
    if 'informal_dress_code' in body:
        validate_data['informal_dress_code'] = body['informal_dress_code']
    if 'PPO' in body:
        validate_data['PPO'] = body['PPO']
    if 'performance_based' in body:
        validate_data['performance_based'] = body['performance_based']
    if 'visibility' in body:
        validate_data['visibility'] = body['visibility']
    if 'applications_end' in body:
        validate_data['applications_end'] = body['applications_end']
    if 'deadline' in body:
        validate_data['deadline'] = body['deadline']
    if 'duration' in body:
        validate_data['duration'] = body['duration']
    if 'responsibilities' in body:
        validate_data['responsibilities'] = body['responsibilities']
    if 'stipend' in body:
        validate_data['stipend'] = body['stipend']
    if 'location' in body:
        validate_data['location'] = body['location']
    internship = Internship.objects.filter(id_code=id)
    inter = internship.update(**validate_data)
    intern = InternshipReadSerializer(internship[0], many=False).data
    return Response(intern)

@api_view(['GET'])
def resume(request):
    ''''
    intern = Intern.objects.select_related('user').select_related('user__user').select_related('user__address').get(id=6)
    projects_data = Project.objects.filter(intern = intern)#.values_list('created_at','updated_at','name','description','location','start','end','description','intern').
    jobs_data = Job.objects.filter(intern = intern)#.values_list('created_at','updated_at','position','organiztion','location','start','end','description','intern').annotate(name=Value('xxx', output_field=models.CharField()))
    degrees_data = Degree.objects.filter(intern = intern)
    github_data = Github.objects.filter(intern = intern)
    if github_data.exists():
        github = GithubSerializer(github_data,many=False).data
    else:
        github = {}
    projects = ProjectSerializer(projects_data, many=True).data
    degrees = DegreeSerializer(degrees_data, many=True).data
    jobs = JobSerializer(jobs_data, many=True).data
    intern = InternSerializer(intern, many=False).data
    return Response({
        'projects':projects,
        'jobs':jobs,
        'intern':intern,
        'degrees':degrees,
        'github':github
    })
    '''
    if 'HTTP_ACCESSTOKEN' in request.META:
        token = request.META['HTTP_ACCESSTOKEN']
        user = AuthToken.objects.select_related('user').get(token = token).user
        intern = Intern.objects.filter(user__user = user)
        if intern.exists():
            intern = intern
        elif 'intern' in request.GET:
            company_user = Company_User.objects.filter(user__user = user)
            if company_user.exists():
                intern = Intern.objects.filter(id = request.GET['intern'])
                if intern.exists():
                    if not Submission.objects.filter(intern = intern[0],internship__company = company_user[0].company).exists():
                        return Response({'err':'intern has not applied'})
            else:
                return Response({'err':'invalid user'})
        else:
            return Response({'err':'invalid request'})
        if intern.exists():
            intern = list(intern)[0]
            projects_data = Project.objects.filter(intern = intern)
            jobs_data = Job.objects.filter(intern = intern)
            degrees_data = Degree.objects.filter(intern = intern)
            github_data = Github.objects.filter(intern = intern)
            if github_data.exists():
                github = GithubSerializer(github_data,many=False).data
            else:
                github = {}
            projects = ProjectSerializer(projects_data, many=True).data
            degrees = DegreeSerializer(degrees_data, many=True).data
            jobs = JobSerializer(jobs_data, many=True).data
            intern = InternSerializer(intern, many=False).data
            return Response({
                'projects':projects,
                'jobs':jobs,
                'intern':intern,
                'degrees':degrees,
                'github':github
            })
        else:
            return Response({'err':'invalid intern'})
    else:
        return Response({'err':'no token'})

class InternshipReadList(viewsets.ModelViewSet):
    pagination_class = BasicPagination
    serializer_class = InternshipReadSerializer
    filter_backends = (DjangoFilterBackend,filterr.SearchFilter,DeleteFilter,filterr.OrderingFilter,DurationFilterBackend,CodeIdFilterBackend,FullInternshipFilterBackend)
    filter_fields = ('category','location','company','approved','skills','PPO','free_snacks','letter_of_recommendation','free_snacks','flexible_work_hours','certificate','informal_dress_code')
    search_fields = ('category','stipend','location','responsibilities','skills__name')
    ordering_fields = ('deadline', 'duration')

    def get_queryset(self):
        intern = getIntern(self.request)
        queryset = Internship.objects.select_related('company').prefetch_related('submission').select_related('company_user').prefetch_related('skills').all()

        if not intern or 'id' in self.request.GET:
            return queryset
        submissions= Submission.objects.select_related('internship').filter(intern = intern)
        for submission in submissions:
            queryset = queryset.exclude(id = submission.internship.id)
        return queryset

class FullInternshipSubReadList(viewsets.ModelViewSet):
    pagination_class = BasicPagination
    serializer_class = FullInternshipReadSubSerializer
    filter_backends = (DjangoFilterBackend,filterr.SearchFilter,DeleteFilter,filterr.OrderingFilter,DurationFilterBackend,CodeIdFilterBackend)
    filter_fields = ('category','location','company','approved','skills','PPO','status','visibility','free_snacks','letter_of_recommendation','free_snacks','flexible_work_hours','certificate','informal_dress_code')
    search_fields = ('category','stipend','location','responsibilities','skills__name')
    ordering_fields = ('deadline', 'duration')
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = Internship.objects.select_related('company').select_related('company_user').prefetch_related('skills').all()
        return queryset

class InternshipSubReadList(viewsets.ModelViewSet):
    pagination_class = BasicPagination
    serializer_class = InternshipReadSubSerializer
    filter_backends = (DjangoFilterBackend,filterr.SearchFilter,DeleteFilter,filterr.OrderingFilter,DurationFilterBackend,CodeIdFilterBackend)
    filter_fields = ('category','location','company','approved','skills','PPO','status','visibility','free_snacks','letter_of_recommendation','free_snacks','flexible_work_hours','certificate','informal_dress_code')
    search_fields = ('category','stipend','location','responsibilities','skills__name')
    ordering_fields = ('deadline', 'duration')
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = Internship.objects.select_related('company').select_related('company_user').prefetch_related('skills').all()
        return queryset

class InternshipList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Internship.objects.select_related('company').select_related('company_user').prefetch_related('skills').all()
    serializer_class = InternshipSerializer

def update(request):
    for i in Internship.objects.all():
        i.id_code = str(i.id) + str(i.code)
        i.save()
    return Http404
'''
def send(request):
    pass
    from_email = "internsips@studentgiri.c.api-central.net"
    to_email = "crazcuber@gmail.com"
    sending_mail(subject, "email_template_name", context, from_email, to_email)
'''
class SubmissionList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Submission.objects.select_related('intern').select_related('internship').all()
    serializer_class = SubmissionSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,filterr.OrderingFilter,DeleteFilter)
    filter_fields = ('intern','status','internship__id_code')
    ordering = ('-created_at',)

class SubmissionInternReadList(viewsets.ModelViewSet):
    serializer_class = SubmissionInternReadSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,InternshipFilterBackend,filterr.OrderingFilter,DeleteFilter)
    filter_fields = ('intern','status','internship__id_code')
    ordering = ('-created_at',)
    queryset = Submission.objects.select_related('intern').prefetch_related('intern__skills').prefetch_related('internship__skills').select_related('intern__user').select_related('intern__user__user').select_related('intern__user__address').select_related('internship').select_related('internship__company').all()

class Submit(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmitSerializer

class SubmissionCompanyReadList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Submission.objects.all()
    serializer_class = SubmissionCompanyReadSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,DeleteFilter)
    filter_fields = ('intern','status','internship__id_code')
    ordering = ('-created_at',)

class QuestionList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Question.objects.select_related('internship').all()
    serializer_class = QuestionSerializer
    pagination_class = BasicPagination
    filter_backends = (InternshipFilterBackend,DeleteFilter)
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

class AnswerList(viewsets.ModelViewSet):
    permission_classes  = (IsAuthenticated2,)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,DeleteFilter)
    filter_fields = ('question',)

class AnswerReadList(viewsets.ModelViewSet):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Answer.objects.select_related('question').select_related('question__internship').all()
    serializer_class = AnswerReadSerializer
    pagination_class = BasicPagination
    filter_backends = (DjangoFilterBackend,DeleteFilter)
    filter_fields = ('submission',)
