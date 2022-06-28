from rest_framework import serializers
from rest_framework.response import Response
from .models import *
from user.serializers import *
import uuid

# class RecruiterSerializer(serializers.ModelSerializer):
#     class Meta:

# Method Name 'JobSerializer'
class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobDetail
        # fields = '__all__'
        exclude = ('Skills', 'recruiter_id')



# Method Name 'ApplicantSerializer'
class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantDetails
        # fields = '__all__'
        exclude = ('id',)
