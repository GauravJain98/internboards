from .models import *
from rest_framework import generics, permissions, serializers
from django.contrib.auth.models import User, Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class Custom_UserSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(required =True)

    class Meta:
        model = Custom_User
        fields = ('user','address')
    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        custom_user, created = CustomUser.objects.update_or_create(user=user, **validated_data)

        return custom_user

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name','website','email','description','address','city')

class Catagory(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = ('name',)

class GithubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Github
        fields = ('commits','stars','followers','repositories','following')
        #addIntern

class Custom_UserSerializer(serializers.HyperlinkedModelSerializer):
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

class Company_UserSerializer(serializers.HyperlinkedModelSerializer):
    """ 
    Custom User Serializer
    https://medium.freecodecamp.org/nested-relationships-in-serializers-for-onetoone-fields-in-django-rest-framework-bdb4720d81e6
    """

    user = Custom_UserSerializer(required=True)
    added_user = serializers.PrimaryKeyRelatedField(many=False, queryset=Company_User.objects.all())    
    comapany = serializers.PrimaryKeyRelatedField(many=False, queryset=Company.objects.all())    

    class Meta:
        model = Company_User
        fields = ['id', 'user', 'address']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = UserSerializer.create(UserSerializer(), validated_data=user_data)

        custom_user, created = Custom_User.objects.update_or_create(user=user, **validated_data)
        return custom_user
