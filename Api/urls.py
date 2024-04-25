from django.urls import path
from Api import views_exhibits, views_fis, views_ris, views_esis, views_student_award
from .views import CreateCategory, FacultyCertificateRecords, ProgramAccreditation, SeminarRecords
from .views_esis import *
from Api import views

app_name = 'apis'

urlpatterns = [
    path('program-accreditation-records/', ProgramAccreditation.as_view(), name='program-accreditaion'),

    path('exhibit/<str:program_accred_pk>/', views_exhibits.landing_page, name='exhibit-page'),
    path('student-awards/<str:program_accred_pk>/', views_student_award.landing_page, name='student-award-page'),

    path('esis/extension/records/', views_esis.extension_info, name='extension-info'),
    path('ris/research/infos/students/<str:program_accred_pk>/', views_ris.research_student, name='research-info-student'),
    path('ris/research/infos/faculties/<str:program_accred_pk>/', views_ris.research_faculty, name='research-info-faculty'),

    path('fis/awards/infos/<str:program_accred_pk>/', views_fis.faculty_awards_info, name='faculty-awards-info'),

    path('faculty/certificate/records/', FacultyCertificateRecords.as_view(), name='faculty-certificate-info'),
    path('faculty/seminars-workshops-trainings/records/', SeminarRecords.as_view(), name='seminars-workshops-trainings'),
    path('faculty/category/records/', CreateCategory.as_view(), name='category'),

    path('faculty-development/data/', views_fis.FacultyDevelopmentAPI.as_view(), name='api-faculty-development')


] 