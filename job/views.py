from django.shortcuts import render
from rest_framework import generics, authentication, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.settings import api_settings
from rest_framework.response import Response
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
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authtoken.models import Token
from django.db.models import Q
from .models import *
# from .forms import *
from .serializers import *
from django.core import serializers
from django.utils import timezone
import random
import uuid
import datetime
from django.core.exceptions import BadRequest
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.views.generic import DetailView, View
from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        return Response({"detail": "Invalid token."}, status=401)
    return exception_handler(exc, context)


class JobStatusView(APIView):
    model = ApplicantDetails
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    serializer_class = ApplicantSerializer

    def get_object(self, job_id):
        try:
            return ApplicantDetails.objects.get(pk=job_id)
        except ApplicantDetails.DoesNotExist:
            raise Http404

    def get(self, request, job_id, format=None):
        user = UserDetail.objects.get(email=request.user)
        if user.recruiter == False:
            return Response({'message': 'You need recruiter privileges to perform this action'}, status.HTTP_403_FORBIDDEN)
        else:
            job = JobDetail.objects.get(pk=job_id)
            if job.recruiter_id.id == request.user.id:
                applicant_detail = ApplicantDetails.objects.filter(job_id=job_id)
                serializer = ApplicantSerializer(applicant_detail, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message":"You do not have permission to perform this action"}, status.HTTP_403_FORBIDDEN)




# # Method to view seeker profile
# # className --->  ViewProfileView
class ViewProfileView(APIView):
    model = ApplicantDetails

    def get_object(self, request, pk):
        try:
            return ApplicantDetails.objects.get(pk=pk)
        except ApplicantDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            x = request.META['HTTP_AUTHORIZATION']
            if len(request.META['HTTP_AUTHORIZATION']) < 10:
                return Response({"detail": "Invalid token."}, status=401)
            else:
                user = UserDetail.objects.get(email=request.user)
                if user.recruiter == False:
                    return Response({'message': 'You need recruiter privileges to perform this action'}, status.HTTP_403_FORBIDDEN)
                else:
                    try:
                        # applicant = ApplicantDetails.objects.get(applicant_id=applicant_id)
                        user = UserDetail.objects.get(pk=pk)
                        serializer = UserSerialiser(user)
                        return Response(serializer.data)
                    except:
                        return Response({"detail": "nothing found"}, status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)
#
#
#
# # Method to update and delete a job
# # className --->  JobUpdateDeleteView
# # Create a permission to allow recruiters to edit only their own job post details
class JobUpdateDeleteView(generics.UpdateAPIView):
    model = JobDetail
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    serializer_class = JobSerializer

    def get_object(self, request, pk):
        try:
            # breakpoint()
            return JobDetail.objects.get(pk=pk)
        except JobDetail.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        try:
            x = request.META['HTTP_AUTHORIZATION']
            if len(request.META['HTTP_AUTHORIZATION']) == 0:
                return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)
            elif len(request.META['HTTP_AUTHORIZATION']) < 10:
                return Response({"detail": "Invalid token."}, status=401)
            else:
                if pk is None:
                    jobs = JobDetail.objects.all()
                    serializer = self.get_serializer(jobs, many=True)
                    return Response(serializer.data)
                else:
                    job = self.get_object(request, pk)
                    serializer = self.get_serializer(instance=job)
                    return Response(serializer.data)
                # recuiter = UserDetail.objects.get(email=request.user)
                # serializer = UserSerialiser(seeker)
                # return Response(serializer.data)
        except KeyError:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, pk, format=None):
        try:
            x = request.META['HTTP_AUTHORIZATION']
            if len(request.META['HTTP_AUTHORIZATION']) == 0:
                return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)
            elif len(request.META['HTTP_AUTHORIZATION']) < 10:
                return Response({"detail": "Invalid token."}, status=401)
            else:
                user = UserDetail.objects.get(email=request.user)
                if user.recruiter == False:
                    return Response({'message': 'You need recruiter privileges to perform this action'}, status.HTTP_403_FORBIDDEN)
                else:
                    try:
                        job = self.get_object(request, pk)
                        if UserDetail.objects.get(email=request.user).recruiter==True:
                            if job.recruiter_id.id == request.user.id:
                                serializer = JobSerializer(job, data=request.data, partial=True)
                                if serializer.is_valid():
                                    serializer.save()
                                    return Response({'message': 'job details have been updated successfully'}, status.HTTP_200_OK)
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response({"detail": "You do not have permission to perform this action."}, status.HTTP_403_FORBIDDEN)
                        else:
                            return Response({"detail": "You do not have permission to perform this action."}, status.HTTP_403_FORBIDDEN)
                    except:
                        return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)


    def delete(self, request, pk, format=None):
        try:
            x = request.META['HTTP_AUTHORIZATION']
            if len(request.META['HTTP_AUTHORIZATION']) < 10:
                return Response({"detail": "Invalid token."}, status=401)
            else:
                user = UserDetail.objects.get(email=request.user)
                if user.recruiter == False:
                    return Response({'detail': 'You do not have permission to perform this action.'}, status.HTTP_403_FORBIDDEN)
                else:
                    job = self.get_object(request, pk)
                    if job.recruiter_id.id == request.user.id:
                        job.delete()
                        return Response(status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response({'detail': 'You do not have permission to perform this action.'}, status.HTTP_403_FORBIDDEN)
        except KeyError:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)
    #
    # def post(self, request, format=None):
    #     seeker = self.get_object(request)
    #     # seeker = UserDetail.objects.get(email=request.user)
    #     serializer = UserSerialiser(seeker, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobApplyView(APIView):
    model = JobDetail
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    serializer_class = JobSerializer

    def get_object(self, request):
        try:
            user = UserDetail.objects.get(email=request.user)
            if user.recruiter == False:
                return user
            else:
                return None
        except UserDetail.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        try:
            x = request.META['HTTP_AUTHORIZATION']
            if len(request.META['HTTP_AUTHORIZATION']) < 10:
                if len(request.META['HTTP_AUTHORIZATION']) == 0:
                    return Response({"detail": "Authentication credentials were not provided."}, status=401)
                return Response({"detail": "Invalid token."}, status=401)
            else:
                seeker = self.get_object(request)
                if seeker == None:
                    return Response({'message': 'You need seeker privileges to perform this action'}, status.HTTP_403_FORBIDDEN)
                job_id = request.data.get("job_id")
                job = JobDetail.objects.get(pk=job_id)
                # try:
                applicant_detail, created = ApplicantDetails.objects.get_or_create(
                    job_id=job, job_title=job.job_title, company=job.company,
                    applicant_id=seeker, applicant_name=seeker.name, applicant_email=seeker.email
                )
                if created == False:
                    return Response({"message": "You have already applied for this job"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                job.no_of_applicants += 1
                job.save()
                return Response({"message": "You have successfully applied for this job"}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)


# Method to view seeker applied jobs
# className --->  JobAppliedView
class JobAppliedView(APIView):
    model = JobDetail
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    serializer_class = JobSerializer

    def get_object(self, request):
        try:
            user = UserDetail.objects.get(email=request.user)
            if user.recruiter == False:
                return user
            else:
                return None
        except UserDetail.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            x = request.META['HTTP_AUTHORIZATION']
            if len(request.META['HTTP_AUTHORIZATION']) < 10:
                if len(request.META['HTTP_AUTHORIZATION']) == 0:
                    return Response({"detail": "Authentication credentials were not provided."}, status=401)
                return Response({"detail": "Invalid token."}, status=401)
            else:
                seeker = self.get_object(request)
                if seeker == None:
                    return Response({'message': 'You need seeker privileges to perform this action'}, status.HTTP_403_FORBIDDEN)
                # job_id = request.data.get("job_id")
                # job = JobDetail.objects.get(pk=job_id)
                # # try:
                applicant_detail = ApplicantDetails.objects.filter(
                    applicant_id=seeker, applicant_name=seeker.name, applicant_email=seeker.email
                )
                serializer = ApplicantSerializer(applicant_detail, many=True)
                # if created == False:
                    # return Response({"message": "You have already applied for this job"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)



class JobFiltersView(APIView):
    model = JobDetail
    serializer_class = JobSerializer

    def get(self, request, format=None):
        # try:
        srh = request.GET.get('search')
        job = JobDetail.objects.filter(Q(job_title__icontains=srh) | Q(work_location__icontains=srh) | Q(description__icontains=srh) | Q(company__icontains=srh))
        serializer = JobSerializer(job, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class JobListView(APIView):
    model = JobDetail
    serializer_class = JobSerializer

    def get(self, request, format=None):
        try:
            job = JobDetail.objects.all()
            serializer = JobSerializer(job, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)


class JobPostView(APIView):
    model = JobDetail
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication,]
    serializer_class = JobSerializer

    def get_object(self, request):
        try:
            user = UserDetail.objects.get(email=request.user)
            if user.recruiter == True:
                return user
            else:
                return None
        except UserDetail.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        try:
            # breakpoint()
            x = request.META['HTTP_AUTHORIZATION']
            if len(request.META['HTTP_AUTHORIZATION']) < 10:
                if len(request.META['HTTP_AUTHORIZATION']) == 0:
                    return Response({"detail": "Authentication credentials were not provided."}, status=401)
                return Response({"detail": "Invalid token."}, status=401)
            else:
                recruiter = self.get_object(request)
                if recruiter == None:
                    return Response({'message': 'You need recruiter privileges to perform this action'}, status.HTTP_403_FORBIDDEN)
                new_dic = request.data
                recruiter = UserDetail.objects.get(id=request.user.id)
                new_dic['recruiter_id'] = recruiter
                new_dic['company'] = recruiter.company
                new_dic['about_company'] = recruiter.about_company
                new_dic['website'] = recruiter.website
                # try:
                job_detail = JobDetail.objects.create(**new_dic)
                return Response({"message": "job details have been posted successfully"}, status=status.HTTP_201_CREATED)
                # except Exception as e:
                #     return Response("None", status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)


class MyPostsView(APIView):
    model = JobDetail
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    serializer_class = JobSerializer

    def get_object(self, request):
        try:
            if request.user.recruiter == True:
                jobs = JobDetail.objects.filter(recruiter_id=request.user.id)
                return jobs
            else:
                return None
        except JobDetail.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            x = request.META['HTTP_AUTHORIZATION']
            if len(request.META['HTTP_AUTHORIZATION']) < 10:
                if len(request.META['HTTP_AUTHORIZATION']) == 0:
                    return Response({"detail": "Authentication credentials were not provided."}, status=401)
                return Response({"detail": "Invalid token."}, status=401)
            else:
                if request.user.recruiter == True:
                    jobs = self.get_object(request)
                    if len(jobs) < 1:
                        return Response({'message': 'You need recruiter privileges to perform this action'}, status.HTTP_403_FORBIDDEN)
                    serializer = JobSerializer(jobs, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'You need recruiter privileges to perform this action'}, status.HTTP_403_FORBIDDEN)
                # else:
                #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)
