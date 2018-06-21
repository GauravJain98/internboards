from .models import *
from rest_framework import generics, permissions, serializers
from django.contrib.auth.models import User, Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class Custom_UserSerializer(serializers.ModelSerializer):
    """ 
    Custom User Serializer
    https://medium.freecodecamp.org/nested-relationships-in-serializers-for-onetoone-fields-in-django-rest-framework-bdb4720d81e6
    """

    user = UserSerializer(required=True)
    
    class Meta:
        model = Custom_User
        fields = ['id', 'user', 'address']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = UserSerializer.create(UserSerializer(), validated_data=user_data)

        custom_user, created = Custom_User.objects.update_or_create(user=user, **validated_data)
        return custom_user

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name','website','email','description','address','city')

class CategorySeializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class Company_UserSerializer(serializers.ModelSerializer):

    user = Custom_UserSerializer(required=True)
    added_user = serializers.PrimaryKeyRelatedField(many=False, queryset=Company_User.objects.all())    
    company = serializers.PrimaryKeyRelatedField(many=False, queryset=Company.objects.all())    

    class Meta:
        model = Company_User
        fields = ['id', 'user', 'company','is_active','is_HR','added_user','share']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        added_user_data = validated_data.pop('added_user')
        company_data = validated_data.pop('company')

        user = UserSerializer.create(UserSerializer(), validated_data=user_data)

        company_user ,created = Company_User.objects.update_or_create(user = user ,company=company ,added_user = added_user, **validated_data) 
        return company_user

class InternSerializer(serializers.ModelSerializer):

    user = Custom_UserSerializer(required=True)
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )

    class Meta:
        model = Company_User
        fields = ['id', 'user', 'skills','college','location','hired']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        skills_data = validated_data.pop('skills')

        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        intern ,created = Intern.objects.update_or_create(user = user ,company=company ,added_user = added_user, **validated_data) 

        for skill in skills:
            intern.add(skill)

        return intern

class GithubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Github
        fields = ('intern','commits','stars','followers','repositories','following')

class SiteAdminSerializer(serializers.ModelSerializer):

    user = Custom_UserSerializer(required=True)

    class Meta:
        model = Company_User
        fields = ['id', 'user', 'email','sub']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        sitadmin ,created = SiteAdmin.objects.update_or_create(user = user , **validated_data) 

        for skill in skills:
            intern.add(skill)

        return intern

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

        return intern

class JobSerializer(serializers.ModelSerializer):

    intern = serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())    

    class Meta:
        model = Degree
        fields = ['id', 'intern','position','organization','location','start','end','description']

    def create(self, validated_data):

        intern_data = validated_data.pop('intern')
        job ,created = Job.objects.update_or_create(intern = intern_data, **validated_data) 

        return intern

class ProjectSerializer(serializers.ModelSerializer):

    intern = serializers.PrimaryKeyRelatedField(many=False, queryset=Intern.objects.all())    

    class Meta:
        model = Degree
        fields = ['id', 'intern','name','start','end','description']

    def create(self, validated_data):

        intern_data = validated_data.pop('intern')
        project ,created = Project.objects.update_or_create(intern = intern, **validated_data) 

        return intern

class HiringSerializer(serializers.ModelSerializer):

    company =serializers.StringRelatedField(many=False, queryset=Company.objects.all())    

    class Meta:
        model = Hiring
        fields = ['id', 'company','college']

    def create(self, validated_data):

        company_data = validated_data.pop('company')
        hiring ,created = Hiring.objects.update_or_create(company = company, **validated_data) 

        return intern

class InternshipSerializer(serializers.ModelSerializer):

    company = serializers.StringRelatedField(many=False, queryset=Company.objects.all())  
    company_user =  serializers.PrimaryKeyRelatedField(many=False, queryset=Company_User.objects.all()) 

    class Meta:
        model =  Internship
        fields = ['company','company_user','applications','selected','approved','denied','allowed','certificate','flexible_work_hours','letter_of_recommendation','free_snack','informal_dress_code','PPO','stripend','start','end','responsibilities','stripend','location','code']

class InternshipAvalibleSerializer(serializers.ModelSerializer):

    internship =  serializers.PrimaryKeyRelatedField(many=False, queryset=Internship.objects.all()) 

    class Meta:
        model =  InternshipAvalible
        fields = ['internship','college']

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

