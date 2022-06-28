from django.db import models
from user.models import *

# Create your models here.
class JobDetail(models.Model):
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    experience = models.CharField(max_length=100)
    work_location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    Skills = models.TextField(null=True, blank=True)
    about_company = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    openings = models.IntegerField()
    no_of_applicants = models.IntegerField(null=True, blank=True, default=0)
    application_deadline = models.DateField()
    recruiter_id = models.ForeignKey(UserDetail, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title

class ApplicantDetails(models.Model):
    job_id = models.ForeignKey(JobDetail, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    applicant_id = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=255)
    applicant_email = models.EmailField(max_length=255)

    def __str__(self):
        return self.job_id
