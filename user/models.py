from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomAccountManager(BaseUserManager):

    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError(gettext_lazy('You must enter an email'))
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        if len(other_fields) > 15:
            user.recruiter = False
        else:
            user.recruiter = True
        user.save()
        return user

    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Super User must have "is_staff=True"')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Super User must have "is_superuser=True"')
        return self.create_user(email, name, password, **other_fields)

    def create_admin(self, email, password, name, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Super User must have "is_staff=True"')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Super User must have "is_superuser=True"')
        return self.create_user(email, name, password, **other_fields)


class UserDetail(AbstractBaseUser, PermissionsMixin):
    gender_choices = (("Male", "Male"), ("Female", "Female"))

    email = models.EmailField(gettext_lazy('email_address'), unique=True)
    name = models.CharField(max_length=150, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100, choices=gender_choices, null=True, blank=True)
    mobile_number = models.IntegerField(null=True, blank=True, unique=True)
    address = models.TextField(null=True, blank=True)
    is_staff = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    course = models.CharField(max_length=150, null=True, blank=True)
    specialization = models.CharField(max_length=150, null=True, blank=True)
    course_type = models.CharField(max_length=150, null=True, blank=True)
    college = models.CharField(max_length=150, null=True, blank=True)
    percentage = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)
    year_of_passing = models.IntegerField(null=True, blank=True)
    skills = models.CharField(max_length=150, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    experience_level = models.CharField(max_length=150, null=True, blank=True)
    designation = models.CharField(max_length=150, null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=150, null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    worked_from = models.DateField(null=True, blank=True)
    to = models.DateField(null=True, blank=True)
    about_company = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    recruiter = models.BooleanField(default=False, null=True, blank=True)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    # forget_password_token = models.CharField(max_length=100, blank=True, null=True)


    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def __str__(self):
        return self.email
