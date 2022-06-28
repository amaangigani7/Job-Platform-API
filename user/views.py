from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status, authentication, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from django.db.models import Q
from .models import *
from .utils import *
# from .forms import *
from .serializers import *
from django.core import serializers
from django.utils import timezone
import random
import uuid
import datetime
from django.contrib.auth.hashers import check_password
from django.views.generic import DetailView, View
from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # x = context['request'].META['HTTP_COOKIE'].find('sessionid')
    # print(context['request'].META['HTTP_COOKIE'][x+10:])
    # if context['request'].META['HTTP_COOKIE'][x+10:] == '""':
    # # print(context['request'].user, context['request'].META['HTTP_AUTHORIZATION'])
    # if context['request'].META['HTTP_AUTHORIZATION'] == '' or context['request'].META['HTTP_AUTHORIZATION'] is None:
    # #     print('entered')
    #     return Response({"detail": "Authentication credentials were not provided."}, status=401)
    if isinstance(exc, NotAuthenticated):
        return Response({"detail": "Invalid token."}, status=401)

    # else
    # default case
    return exception_handler(exc, context)

# recruiter and seeker should pass auth token in headers along with any request.
# Method to view, update and delete a recruiter profile
# Method to view, update and delete a seeker profile
class SeekerProfileView(APIView):
    model = UserDetail
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    serializer_class = UserSerialiser

    def get_object(self, request):
        try:
            return UserDetail.objects.get(email=request.user)
        except UserDetail.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            x = request.META['HTTP_AUTHORIZATION']
            if len(request.META['HTTP_AUTHORIZATION']) < 10:
                return Response({"detail": "Invalid token."}, status=401)
            else:
                seeker = self.get_object(request)
                # recuiter = UserDetail.objects.get(email=request.user)
                serializer = UserSerialiser(seeker)
                return Response(serializer.data)
        except KeyError:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, format=None):
        seeker = self.get_object(request)
        # seeker = UserDetail.objects.get(email=request.user)
        serializer = UserSerialiser(seeker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        snippet = self.get_object(request)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        seeker = self.get_object(request)
        # seeker = UserDetail.objects.get(email=request.user)
        serializer = UserSerialiser(seeker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, format=None):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response({"message": "You've been logged out successfully"})

class RecruiterProfileView(APIView):
    model = UserDetail
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RecruiterSerialiser

    def get_object(self, request):
        try:
            return UserDetail.objects.get(email=request.user)
        except UserDetail.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        recuiter = self.get_object(request)
        try:
            x = request.META['HTTP_AUTHORIZATION']
        # recuiter = UserDetail.objects.get(email=request.user)
            serializer = RecruiterSerialiser(recuiter)
            return Response(serializer.data)
        except KeyError:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, format=None):
        # recuiter = self.get_object(request)
        recuiter = UserDetail.objects.get(email=request.user)
        serializer = RecruiterSerialiser(recuiter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        snippet = self.get_object(request)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        recruiter = UserDetail.objects.get(email=request.user)
        serializer = RecruiterSerialiser(recruiter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        parameter = request.data['email']
        password = request.data['password']
        if parameter is None or password is None:
            return Response({"non_field_errors": 'Unable to authenticate with provided credentials'})
        user = UserDetail.objects.get(email=parameter)
        if check_password(password, user.password):
            login(request, user)
            old_token = Token.objects.filter(user=user)
            if len(old_token) > 0:
                old_token.delete()
            x = Token.objects.create(user=user).key
            return Response({"token": x})
        else:
            return Response({"non_field_errors": ["Unable to authenticate with provided credentials"]}, status.HTTP_400_BAD_REQUEST)
        return super(LoginAPI, self).post(request, format=None)


class SeekerSignupView(generics.GenericAPIView):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data['name']) < 4 or check_alpha(request.data['name']) == False:
            return Response({"name": ['Enter a valid name']}, status.HTTP_400_BAD_REQUEST)
        if "." not in request.data['email'] or "@" not in request.data['email'] or "@." in request.data['email']:
            return Response({"email": ["Enter a valid email"]}, status.HTTP_400_BAD_REQUEST)
        if len(str(request.data['mobile_number'])) != 10:
            return Response({"mobile_number": ['Enter a valid number']}, status.HTTP_400_BAD_REQUEST)
        if not check_pass(request.data['password']):
            return Response({"password": ['Enter a valid password']}, status.HTTP_400_BAD_REQUEST)
        if UserDetail.objects.filter(email=request.data['email']):
            return Response({"email": ['user details with this email already exists.']}, status.HTTP_400_BAD_REQUEST)
        if UserDetail.objects.filter(mobile_number=request.data['mobile_number']):
            return Response({"mobile_number": ['user details with this mobile number already exists.']}, status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.recruiter = False
            user.save()
            return Response({
            "message": 'Your account has been created successfully'
            }, status.HTTP_201_CREATED)
        return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"message": 'Your account has been created successfully'}, status=status.HTTP_201_CREATED)


class RecruiterSignupView(generics.GenericAPIView):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data['name']) < 4 or check_alpha(request.data['name']) == False:
            return Response({"name": ['Enter a valid name']}, status.HTTP_400_BAD_REQUEST)
        if "." not in request.data['email'] or "@" not in request.data['email'] or "@." in request.data['email']:
            return Response({"email": ["Enter a valid email"]}, status.HTTP_400_BAD_REQUEST)
        if len(str(request.data['mobile_number'])) != 10 or str(request.data['mobile_number'])[0] not in ['7','8','9']:
            return Response({"mobile_number": ['Enter a valid number']}, status.HTTP_400_BAD_REQUEST)
        if not check_pass(request.data['password']):
            return Response({"password": ['Enter a valid password']}, status.HTTP_400_BAD_REQUEST)
        if UserDetail.objects.filter(email=request.data['email']):
            return Response({"email": ['user details with this email already exists.']}, status.HTTP_400_BAD_REQUEST)
        if UserDetail.objects.filter(mobile_number=request.data['mobile_number']):
            return Response({"mobile_number": ['user details with this mobile number already exists.']}, status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            # serializer.save()
            user = serializer.save()
            user.recruiter = True
            user.save()
            # breakpoint()
            # send_email_after_registration(request.data['email'], token=Customer.objects.get(user_name=request.data['user_name']).verification_token)
            return Response({
            # "status_code": status.HTTP_201_CREATED,
            # "user": CustomerSerializer(customer, context=self.get_serializer_context()).data,
            "message": 'Your account has been created successfully'
            }, status.HTTP_201_CREATED)
        return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"Errors": "nothing"}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"message": 'Your account has been created successfully'}, status=status.HTTP_201_CREATED)
