from .models import *
from rest_framework import permissions, serializers
from django.contrib.auth.models import User
from django.http import JsonResponse
from .permissions import *

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('apartment','street','city','zip_code','country')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','password')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        password = validated_data.pop('password')
        user, created = User.objects.get_or_create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class Custom_UserSerializer(serializers.ModelSerializer):
    """ 
    Custom User Serializer
    https://medium.freecodecamp.org/nested-relationships-in-serializers-for-onetoone-fields-in-django-rest-framework-bdb4720d81e6
    """

    user = UserSerializer(required=True)
    address = AddressSerializer(required = True)

    class Meta:
        model = Custom_User
        fields = ['id', 'user', 'address']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        address_data = validated_data.pop('address')

        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        address = AddressSerializer.create(AddressSerializer(), validated_data=address_data)

        custom_user, created = Custom_User.objects.update_or_create(user=user,address=address, **validated_data)
        return custom_user

class CompanySerializer(serializers.ModelSerializer):
    hiring = serializers.SlugRelatedField(
        many=True,
        slug_field='sub',
        queryset=College.objects.all()
    )
    address = AddressSerializer(required = True)

    class Meta:
        model = Company
        fields = ('name','hiring','website','email','description','address','city')

    def create(self,validated_data):
        hiring_data = validated_data.pop('hiring')
        address_data = validated_data.pop('address')
        address = AddressSerializer.create(AddressSerializer(),validated_data=address_data)

        company , created = Company.objects.update_or_create(address=address,**validated_data) 

        for hiring in hiring_data:
            company.hiring.add(hiring)
        return company

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class CollegeSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required = True)
    
    class Meta:
        model = College
        fields = ('name','sub','location','address')

    def create(self,validated_data):
        address_data = validated_data.pop('address')
        address = AddressSerializer.create(AddressSerializer(),validated_data=address_data)
        college , created = College.objects.update_or_create(address=address,**validated_data) 
        return college

class Company_UserSerializer(serializers.ModelSerializer):

    user = Custom_UserSerializer(required=True)
    added_user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())    
    company = serializers.PrimaryKeyRelatedField(many=False, queryset=Company.objects.all())    

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

class InternSerializer(serializers.ModelSerializer):

    user = Custom_UserSerializer(required=True)
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )

    class Meta:
        model = Intern
        fields = ['id', 'user', 'skills','college','hired']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        skills_data = validated_data.pop('skills')

        user = Custom_UserSerializer.create(Custom_UserSerializer(), validated_data=user_data)
        intern ,created = Intern.objects.update_or_create(user = user , **validated_data) 

        for skill in skills_data:
            intern.skills.add(skill)

        return intern

class GithubSerializer(serializers.ModelSerializer):
    intern = serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())    
    class Meta:
        model = Github
        fields = ('intern','commits','stars','followers','repositories','following')

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
        fields = ['name']

class DegreeSerializer(serializers.ModelSerializer):

    intern = serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())    

    class Meta:
        model = Degree
        fields = ['id', 'intern','college_name','start','end','performance','name','type_of_degree','specialise']

    def create(self, validated_data):

        intern_data = validated_data.pop('intern')
        degree ,created = Degree.objects.update_or_create(intern = intern_data, **validated_data) 

        return degree

class JobSerializer(serializers.ModelSerializer):

    intern = serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())    

    class Meta:
        model = Job
        fields = ['id', 'intern','position','organization','location','start','end','description']

    def create(self, validated_data):

        intern_data = validated_data.pop('intern')
        job ,created = Job.objects.update_or_create(intern = intern_data, **validated_data) 

        return job

class ProjectSerializer(serializers.ModelSerializer):

    intern = serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())    

    class Meta:
        model = Project
        fields = ['id', 'intern','name','start','end','description']

    def create(self, validated_data):

        intern_data = validated_data.pop('intern')
        project ,created = Project.objects.update_or_create(intern = intern, **validated_data) 

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

    class Meta:
        model =  Internship
        fields = ['id','company','skills','company_user','applications','selected','approved','denied','allowed','certificate','flexible_work_hours','letter_of_recommendation','free_snacks','informal_dress_code','PPO','stripend','start','duration','responsibilities','stripend_rate','location']
   
    def create(self, validated_data):
        skills_data = validated_data.pop('skills')
        company_data = validated_data.pop('company')
        company_user_data = validated_data.pop('company_user')
        internship ,created = Internship.objects.update_or_create(company_user = company_user_data ,company = company_data , **validated_data) 

        for skill in skills_data:
            internship.skills.add(skill)

        return internship
    def delete(self, validated_data):
        pass

class InternshipReadSerializer(serializers.ModelSerializer):

    company = CompanySerializer(read_only=True)
    company_user =  serializers.PrimaryKeyRelatedField(many=False, queryset=Company_User.objects.all()) 
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )

    class Meta:
        model =  Internship
        fields = ['id','company','skills','company_user','applications','selected','approved','denied','allowed','certificate','flexible_work_hours','letter_of_recommendation','free_snacks','informal_dress_code','PPO','stripend','start','duration','responsibilities','stripend','location','code','stripend_rate']
   
    def create(self, validated_data):
        return JsonResponse({"error":"Not allowed to create"})

'''
class InternshipAvaliableSerializer(serializers.ModelSerializer):

    internship =  serializers.PrimaryKeyRelatedField(many=False, queryset=Internship.objects.all()) 

    class Meta:
        model =  InternshipAvailable
        fields = ['internship','college']
'''
class SubmissionSerializer(serializers.ModelSerializer):

    intern =serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())    
    internship =serializers.PrimaryKeyRelatedField(many=False, queryset=Internship.objects.all())    

    class Meta:
        model = Submission
        fields = ['id', 'intern','college','internship','status','selected']

class QuestionSerializer(serializers.ModelSerializer):

    internship =serializers.PrimaryKeyRelatedField(many=False, queryset=Internship.objects.all())    

    class Meta:
        model = Question
        fields = ['id', 'internship','question']

class AnswerSerializer(serializers.ModelSerializer):

    submission =serializers.PrimaryKeyRelatedField(many=False, queryset=Submission.objects.all())    
    question =serializers.PrimaryKeyRelatedField(many=False, queryset=Question.objects.all())    

    class Meta:
        model = Answer
        fields = ['id', 'submission','question','answer_text']

