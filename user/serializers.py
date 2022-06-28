from rest_framework import serializers
from rest_framework.response import Response
from .models import *
import uuid
# Method Name 'RecruiterSerialiser'
class RecruiterSerialiser(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, min_length=6)
    class Meta:
        model = UserDetail
        fields = ('name', 'designation', 'company', 'email','date_of_birth', 'gender', 'mobile_number', 'about_company', 'website')
        extra_kwargs = {'password': {'write_only': True}}


# Method Name 'UserSerialiser'
class UserSerialiser(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, min_length=6)
    class Meta:
        model = UserDetail
        fields = ('name', 'designation', 'email', 'gender', 'mobile_number', 'company', 'date_of_birth', 'address', 'password', 'course', 'specialization', 'course_type', 'college', 'percentage', 'year_of_passing', 'skills', 'summary','experience_level', 'responsibilities', 'location', 'worked_from', 'to')
        extra_kwargs = {'password': {'write_only': True}}


# Method Name 'AuthTokenSerializer'
class AuthTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, min_length=6)
    name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = UserDetail
        fields = ('id', 'name', 'designation', 'email', 'gender', 'mobile_number', 'company', 'date_of_birth', 'address', 'password', 'course', 'specialization', 'course_type', 'college', 'percentage', 'year_of_passing', 'skills', 'summary','experience_level', 'about_company', 'website', 'responsibilities', 'location', 'worked_from', 'to')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        while True:
            auth_token = str(uuid.uuid4())
            if not UserDetail.objects.filter(verification_token=auth_token).first():
                break
        # user = UserDetail.objects.create(name=validated_data['name'], email=validated_data['email'], verification_token=auth_token)
        user = UserDetail.objects.create(**self.data)
        user.set_password(validated_data['password'])
        user.save()
        return user
