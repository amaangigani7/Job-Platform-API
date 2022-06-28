from django.urls import path
from . import views

urlpatterns = [
    path('recruiter/signup/', views.RecruiterSignupView.as_view(), name='re_signup'),
    path('seeker/signup/', views.SeekerSignupView.as_view(), name='se_signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('recruiterprofile/', views.RecruiterProfileView.as_view(), name='recruiterprofile'),
    # path('recruiterprofile/<int:pk>/', views.RecruiterProfileView.as_view(), name='recruiterprofile'),
    path('seekerprofile/', views.SeekerProfileView.as_view(), name='seekerprofile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

]
