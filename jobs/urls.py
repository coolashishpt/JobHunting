from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('create/', views.create_job, name='create_job'),
    path('dashboard/recruiter/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('dashboard/candidate/', views.candidate_dashboard, name='candidate_dashboard'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('<int:pk>/save/', views.save_job, name='save_job'),
    path('<int:job_pk>/applicants/', views.applicants_list, name='applicants_list'),
    path('<int:job_pk>/applicants/<int:app_pk>/', views.applicant_detail, name='applicant_detail'),
]
