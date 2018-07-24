from .models import *
from rest_framework import permissions, serializers
from django.contrib.auth.models import User
from django.http import JsonResponse
from .permissions import *
from oauth.models import AuthToken
from django.utils.timezone import now
from django.core.cache import cache

def getUser(request):
    if 'HTTP_ACCESSTOKEN' in request.META:
        token = request.META['HTTP_ACCESSTOKEN']
        if cache.get(str(token) + 'user') is None:
            data = AuthToken.objects.select_related('user').get(token = token).user
            cache.set(str(token) +'user',data ,3600*24)
        else:
            data = cache.get(str(token) + 'user')
        return data
    return False

def getIntern(request):
    if 'HTTP_ACCESSTOKEN' in request.META:
        token = request.META['HTTP_ACCESSTOKEN']
        if cache.get(str(token) + 'intern') is None:
            user = list(AuthToken.objects.select_related('user').filter(token = token))
            if len(user) > 0:
                user = user[0].user
                intern = list(Intern.objects.filter(user__user = user))
                if len(intern) > 0:
                    data = intern[0]
                    cache.set(str(token) + 'intern',data,3600*24)
                else:
                    return False
            else:
                return False
        else:
            data = cache.get(str(token) + 'intern')
        return data
    return False

def getCompanyUser(request):
    if 'HTTP_ACCESSTOKEN' in request.META:
        token = request.META['HTTP_ACCESSTOKEN']
        user = list(AuthToken.objects.select_related('user').filter(token = token))
        if cache.get(str(token) + 'companyuser') is None:
            if len(user) > 0:
                user = user[0].user
                company_user = list(Company_User.objects.filter(user__user = user))
                if len(company_user) > 0:
                    data = company_user[0]
                    cache.set(str(token) + 'companyuser',data,3600*24)
                else:
                    return False
            else:
                return False
        else:
            data = cache.get(str(token) + 'companyuser')
        return data
    else:
        return False

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('apartment','street','city','zip_code','country')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','password')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        if not User.objects.filter(username =email).exists():
            user, created = User.objects.get_or_create(username = email,email = email,**validated_data)
            user.set_password(password)
            user.save()
            return user
        raise serializers.ValidationError("Same Email")

class Custom_UserSerializer(serializers.ModelSerializer):
    """
    Custom User Serializer
    https://medium.freecodecamp.org/nested-relationships-in-serializers-for-onetoone-fields-in-django-rest-framework-bdb4720d81e6
    """

    user = UserSerializer(required=True)
    address = AddressSerializer(required = False)

    class Meta:
        model = Custom_User
        fields = ['id', 'user', 'address']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        '''
        address_data = validated_data.pop('address')
        address = AddressSerializer.create(AddressSerializer(), validated_data=address_data)
        '''
        custom_user, created = Custom_User.objects.update_or_create(user=user,**validated_data)
        return custom_user

class CompanySerializer(serializers.ModelSerializer):
    hiring = serializers.SlugRelatedField(
        many=True,
        slug_field='link',
        queryset=Sub.objects.all()
    )
    address = AddressSerializer(required = True,many=True)

    class Meta:
        model = Company
        fields = ('id','name','hiring','website','email','description','address','city')

    def create(self,validated_data):
        hiring_data = validated_data.pop('hiring')
        address_data = validated_data.pop('address')
        company , created = Company.objects.update_or_create(**validated_data)

        for address in address_data:
            address = AddressSerializer.create(AddressSerializer(),validated_data=address)
            company.address.add(address)

        for hiring in hiring_data:
            company.hiring.add(hiring)
        return company

class CompanyReadSerializer(serializers.ModelSerializer):
    hiring = serializers.SlugRelatedField(
        many=True,
        slug_field='link',
        queryset=Sub.objects.all()
    )
    class Meta:
        model = Company
        fields = ('id','name','hiring')

    def create(self,validated_data):
        pass

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name',)

class CollegeSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required = True)

    class Meta:
        model = College
        fields = ('name','address')

    def create(self,validated_data):
        address_data = validated_data.pop('address')
        address = AddressSerializer.create(AddressSerializer(),validated_data=address_data)
        college , created = College.objects.update_or_create(address=address,**validated_data)
        return college

class Company_UserSerializer(serializers.ModelSerializer):

    user = Custom_UserSerializer(required=True)
    added_user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all(),required=False )
    company = CompanyReadSerializer(read_only=True)
    class Meta:
        model = Company_User
        fields = ['id', 'user', 'company','is_active','is_HR','added_user','share']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        added_user_data = validated_data.pop('added_user')
        company_data = validated_data.pop('company')

        user = Custom_UserSerializer.create(Custom_UserSerializer(), validated_data=user_data)

        company_user ,created = Company_User.objects.update_or_create(user = user ,company=company_data ,added_user = added_user_data, **validated_data)
        return company_user

class Company_UserAddSerializer(serializers.ModelSerializer):

    user = Custom_UserSerializer(required=True)
    added_user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    company = serializers.PrimaryKeyRelatedField(many=False, queryset=Company.objects.all())
    token = serializers.SerializerMethodField()

    def get_token(self,obj):
        if self.context['request'].method == 'POST':
            token = AuthToken.objects.filter(user=obj.user.user,revoked=False)
            if len(token) >0:
                token = list(token)[0]
                return token.token
            token = AuthToken.objects.create(user=obj.user.user,revoked=False)
            return token.token
        return ""

    class Meta:
        model = Company_User
        fields = ['id', 'user', 'company','is_active','token','is_HR','added_user','share']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        added_user_data = validated_data.pop('added_user')

        user = Custom_UserSerializer.create(Custom_UserSerializer(), validated_data=user_data)

        company_user ,created = Company_User.objects.update_or_create(user = user ,added_user = added_user_data, **validated_data)
        return company_user

class SubSerializer(serializers.ModelSerializer):
#    college = CollegeSerializer(read_only=True)
    class Meta:
        model = Sub
        fields = ['id','link']#,'college']

class InternSerializer(serializers.ModelSerializer):

    user = Custom_UserSerializer(required=True)
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )
    sub = SubSerializer(required=True)
    class Meta:
        model = Intern
        fields = ['id', 'user', 'skills','sub']
        read_only_fields = ('hired',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        skills_data = validated_data.pop('skills')

        cuser = Custom_UserSerializer.create(Custom_UserSerializer(), validated_data=user_data)
        intern ,created = Intern.objects.update_or_create(user = cuser , **validated_data)

        for skill in skills_data:
            intern.skills.add(skill)

        return intern

class InternAddSerializer(serializers.ModelSerializer):

    user = Custom_UserSerializer(required=True)
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )
    token = serializers.SerializerMethodField()
    sub = serializers.SlugRelatedField(
        many=False,
        slug_field='link',
        queryset=Sub.objects.all()
    )
    class Meta:
        model = Intern
        fields = ['id', 'user', 'skills','sub','token']
        read_only_fields = ('hired',)

    def get_token(self,obj):
        if self.context['request'].method == 'POST':
            token = AuthToken.objects.filter(user=obj.user.user,revoked=False)
            if len(token) >0:
                token = list(token)[0]
                return token.token
            token = AuthToken.objects.create(user=obj.user.user,revoked=False)
            return token.token
        return ""
    def to_representation(self, instance):

        return {}

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        skills_data = validated_data.pop('skills')

        cuser = Custom_UserSerializer.create(Custom_UserSerializer(), validated_data=user_data)
        intern ,created = Intern.objects.update_or_create(user = cuser , **validated_data)

        for skill in skills_data:
            intern.skills.add(skill)

        return intern

class GithubSerializer(serializers.ModelSerializer):
    intern = serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())
    class Meta:
        model = Github
        fields = ('intern','collaborators','stars','followers','repositories','following')

class SiteAdminSerializer(serializers.ModelSerializer):

    user = Custom_UserSerializer(required=True)

    class Meta:
        model = SiteAdmin
        fields = ['id', 'user','college']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = Custom_UserSerializer.create(Custom_UserSerializer(), validated_data=user_data)
        sitadmin ,created = SiteAdmin.objects.update_or_create(user = user , **validated_data)

        return SiteAdmin

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['id','name']

class DegreeSerializer(serializers.ModelSerializer):

    intern = serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())

    class Meta:
        model = Degree
        fields = ['id', 'intern','college_name','start','end','performance','name','type_of_degree','specialise','stream']

    def validate(self, data):
        if data['start'] > data['end']:
            raise serializers.ValidationError("finish must occur after start")
        return data

    def create(self, validated_data):

        intern_data = validated_data.pop('intern')
        degree ,created = Degree.objects.update_or_create(intern = intern_data, **validated_data)

        return degree

class JobSerializer(serializers.ModelSerializer):

    intern = serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())

    class Meta:
        model = Job
        fields = ['id', 'intern','position','organization','location','start','end','description']

    def validate(self, data):
        if data['start'] > data['end']:
            raise serializers.ValidationError("finish must occur after start")
        return data

    def create(self, validated_data):

        intern_data = validated_data.pop('intern')
        job ,created = Job.objects.update_or_create(intern = intern_data, **validated_data)

        return job

class ProjectSerializer(serializers.ModelSerializer):

    intern = serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())

    class Meta:
        model = Project
        fields = ['id', 'intern','name','start','end','description']

    def validate(self, data):
        if data['start'] > data['end']:
            raise serializers.ValidationError("finish must occur after start")
        return data

    def create(self, validated_data):

        intern_data = validated_data.pop('intern')
        project ,created = Project.objects.update_or_create(intern = intern_data, **validated_data)

        return project
'''
class HiringSerializer(serializers.ModelSerializer):

    company =serializers.StringRelatedField(many=False)

    class Meta:
        model = Hiring
        fields = ['id', 'company','college']

    def create(self, validated_data):

        company_data = validated_data.pop('company')
        hiring ,created = Hiring.objects.update_or_create(company = company, **validated_data)

        return intern
'''
class QuestionReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id','question','placeholder']

class InternshipSerializer(serializers.ModelSerializer):

    company = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset = Company.objects.all()
    )
    company_user =  serializers.PrimaryKeyRelatedField(many=False, queryset=Company_User.objects.all())
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )
    available = serializers.SlugRelatedField(
        many=True,
        slug_field='link',
        queryset=Sub.objects.all()
    )
    questions = QuestionReadSerializer(many=True)
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=Category.objects.all()
    )
    class Meta:
        model =  Internship
        fields = ['id','category','company','available','skills','start','company_user','questions','certificate','flexible_work_hours','letter_of_recommendation','free_snacks','informal_dress_code','PPO','stipend','deadline','duration','responsibilities','stipend_rate','location']

    def create(self, validated_data):
        skills_data = validated_data.pop('skills')
        hiring_data = validated_data.pop('available')
        company_data = validated_data.pop('company')
        company_user_data = validated_data.pop('company_user')
        questions_data = validated_data.pop('questions')
        internship = Internship.objects.create(company_user = company_user_data ,company = company_data , **validated_data)
        for question_data in questions_data:
            questions = Question.objects.create(internship = internship,placeholder = question_data.placeholder,question=question_data.id)
        for skill in skills_data:
            internship.skills.add(skill)
        for hire in hiring_data:
            internship.available.add(hire)
        return internship
    def delete(self, validated_data):
        pass

class InternshipReadSerializer(serializers.ModelSerializer):

    company = CompanyReadSerializer(read_only=True)
    company_user =  serializers.PrimaryKeyRelatedField(many=False, queryset=Company_User.objects.all())
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )
    available = serializers.SlugRelatedField(
        many=True,
        slug_field='link',
        queryset=Sub.objects.all()
    )
    applied = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=Category.objects.all()
    )
    class Meta:
        model =  Internship
        fields = ['id','category','company','in_main','skills','available','company_user','applied','approved','certificate','flexible_work_hours','letter_of_recommendation','free_snacks','informal_dress_code','PPO','stipend','deadline','duration','responsibilities','stipend','location','stipend_rate','code']

    def get_applied(self, obj):
        if 'request' in self.context and self.context['request'].META['PATH_INFO'] == '/submission/intern/':
            return None
        return obj.submission.count() == 0

    def create(self, validated_data):
        return JsonResponse({"error":"Not allowed to create"})

    def to_representation(self, instance):
        try:
            instance.id = str(instance.id) + instance.code
            instance.code = None
        except:
            pass
        finally:
            ret = super().to_representation(instance)
            return ret

class FullInternshipReadSerializer(serializers.ModelSerializer):

    company = CompanyReadSerializer(read_only=True)
    company_user =  serializers.PrimaryKeyRelatedField(many=False, queryset=Company_User.objects.all())
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )
    applied = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=Category.objects.all()
    )
    class Meta:
        model =  Internship
        fields = ['id','category','company','in_main','skills','available','company_user','applied','approved','certificate','flexible_work_hours','letter_of_recommendation','free_snacks','informal_dress_code','PPO','stipend','deadline','duration','responsibilities','stipend','location','stipend_rate','code']

    def create(self, validated_data):
        return JsonResponse({"error":"Not allowed to create"})

    def to_representation(self, instance):
        try:
            instance.id = str(instance.id) + instance.code
            instance.code = None
        except:
            pass
        finally:
            ret = super().to_representation(instance)
            return ret

class InternshipReadSubSerializer(serializers.ModelSerializer):

    company = serializers.PrimaryKeyRelatedField(many=False, queryset=Company.objects.all())
    company_user =  serializers.PrimaryKeyRelatedField(many=False, queryset=Company_User.objects.all())
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=Category.objects.all()
    )
    visibility = serializers.SerializerMethodField()
    class Meta:
        model =  Internship
        '''
        1,2,5,6,7
        'certificate','flexible_work_hours','letter_of_recommendation','free_snacks','informal_dress_code','PPO','stipend',
        '''
        fields = ['id','category','skills','company_user','company','status','visibility','applications','approved','denied','allowed','deadline','duration','stipend','location','stipend_rate','code','created_at']

    def get_visibility(self, obj):
        return obj.visibility < now().date()

    def create(self, validated_data):
        return JsonResponse({"error":"Not allowed to create"})

    def to_representation(self, instance):
        try:
            instance.id = str(instance.id) + instance.code
            instance.code = None
        except:
            pass
        finally:
            ret = super().to_representation(instance)
            return ret

class FullInternshipReadSubSerializer(serializers.ModelSerializer):

    company = serializers.PrimaryKeyRelatedField(many=False, queryset=Company.objects.all())
    company_user =  serializers.PrimaryKeyRelatedField(many=False, queryset=Company_User.objects.all())
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=Category.objects.all()
    )
    visibility = serializers.SerializerMethodField()
    class Meta:
        model =  Internship
        '''
        1,2,5,6,7
        'certificate','flexible_work_hours','letter_of_recommendation','free_snacks','informal_dress_code','PPO','stipend',
        '''
        fields = ['id','category','company','status','skills','company_user','visibility','applications','approved','denied','allowed','deadline','duration','responsibilities','stipend','location','stipend_rate','code']

    def get_visibility(self, obj):
        return obj.visibility < now().date()

    def create(self, validated_data):
        return JsonResponse({"error":"Not allowed to create"})

    def to_representation(self, instance):
        try:
            instance.id = str(instance.id) + instance.code
            instance.code = None
        except:
            pass
        finally:
            ret = super().to_representation(instance)
            return ret
'''
class InternshipAvaliableSerializer(serializers.ModelSerializer):

    internship =  serializers.PrimaryKeyRelatedField(many=False, queryset=Internship.objects.all())

    class Meta:
        model =  InternshipAvailable
        fields = ['internship','college']
'''
class SubmissionSerializer(serializers.ModelSerializer):

    intern =serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())
    internship =serializers.SlugRelatedField(
        many=False,
        slug_field='id_code',
        queryset=Internship.objects.all()
    )

    class Meta:
        model = Submission
        fields = ['id', 'intern','sub','internship','status']

    def validate(self, data):
        if self.context['request'].method != 'PATCH':
            if Submission.objects.filter(intern = data['intern'] , internship = data['internship'],sub = data['sub']).exists():
                raise serializers.ValidationError("Already applied")
            return data
        return data


    def create(self, validated_data):
        submission = Submission.objects.create(**validated_data)
        return submission

class SubmissionInternReadSerializer(serializers.ModelSerializer):

    intern =serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())
    internship =InternshipReadSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'intern','sub','internship','status','selected','created_at']
        read_only_fields = ('status','created_at')

    def create(self, validated_data):
        return JsonResponse({"error":"Not allowed to create"})


class SubmissionCompanyReadSerializer(serializers.ModelSerializer):

    intern =InternSerializer(read_only=True)
    internship =serializers.SlugRelatedField(
        many=False,
        slug_field='id_code',
        queryset=Internship.objects.all()
    )

    class Meta:
        model = Submission
        fields = ['id', 'intern','sub','internship','status','selected','created_at']
        read_only_fields = ('status','created_at')

    def create(self, validated_data):
        return JsonResponse({"error":"Not allowed to create"})

class QuestionSerializer(serializers.ModelSerializer):

    internship =serializers.SlugRelatedField(
        many=False,
        slug_field='id_code',
        queryset=Internship.objects.all()
    )

    class Meta:
        model = Question
        fields = ['id', 'internship','question','placeholder']

'''
class AnswerSerializer(serializers.ModelSerializer):

    submission = SubmissionSerializer(required = True)
    question =serializers.PrimaryKeyRelatedField(many=False, queryset=Question.objects.all())
    class Meta:
        model = Answer
        validators = []
        fields = ['id', 'submission','question','answer_text']
    def create(self, validated_data):
        submission_data = validated_data.pop('submission')
        answers_data = validated_data.pop('answers')
        question = answers_data['question']
#        internship = Submission.objects.select_related('int')
        submission = SubmissionSerializer.create(SubmissionSerializer(), validated_data=submission_data)
#        answer = AnswerSerializer.create(AnswerSerializer(), validated_data=answer_data)
        for answer in answers_data:
            answer = Answer.objects.create(submission = submission , answer_text = answer['answer_text'],question = answer['question'])
            answer.save()
        return submission
'''

class AnswerSerializer(serializers.ModelSerializer):

    submission =serializers.PrimaryKeyRelatedField(many=False, queryset=Submission.objects.all(),required=False)
    question =serializers.PrimaryKeyRelatedField(many=False, queryset=Question.objects.all())
    class Meta:
        model = Answer
        fields = ['id', 'submission','question','answer_text']

class AnswerReadSerializer(serializers.ModelSerializer):

    submission =serializers.PrimaryKeyRelatedField(many=False, queryset=Submission.objects.all(),required=False)
    question =QuestionReadSerializer(many=False)
    class Meta:
        model = Answer
        validators = []
        fields = ['id', 'submission','question','answer_text']

class SubmitSerializer(serializers.Serializer):
    submission = SubmissionSerializer(required = True)
    answers = AnswerSerializer(many=True)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            question = Question.objects.filter(internship= data["submission"]["internship"])
            if len(data['answers']) != len(question):
                raise serializers.ValidationError("Incomplete submission")
            for answer in data['answers']:
                if answer['question'] not in question:
                    raise serializers.ValidationError("Invalid Question")
            return data
        raise serializers.ValidationError("Method Not allowed")

    def create(self, validated_data):
        submission_data = validated_data.pop('submission')
        answers_data = validated_data.pop('answers')
        final_answers = []
        submission = SubmissionSerializer.create(SubmissionSerializer(), validated_data=submission_data)
        for answer in answers_data:
            answer = Answer.objects.create(submission = submission , answer_text = answer['answer_text'],question = answer['question'])
            answer.save()
            final_answers.append(answer)
        return {'submission':submission,'answers':final_answers}

