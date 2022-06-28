from django.urls import path
from . import views

urlpatterns = [
    path('postjob/', views.JobPostView.as_view(), name='postjob'),
    path('myposts/', views.MyPostsView.as_view(), name='myposts'),
    path('listjob/', views.JobListView.as_view(), name='listjob'),
    path('filterjob/', views.JobFiltersView.as_view(), name='filterjob'),
    path('applyjob/', views.JobApplyView.as_view(), name='applyjob'),
    path('appliedjobs/', views.JobAppliedView.as_view(), name='appliedjobs'),
    path('jobstatus/<int:job_id>', views.JobStatusView.as_view(), name='jobstatus'),
    path('viewprofile/<int:pk>', views.ViewProfileView.as_view(), name='viewprofile'),
    path('updatejob/<int:pk>', views.JobUpdateDeleteView.as_view(), name='updatejob'),
]
