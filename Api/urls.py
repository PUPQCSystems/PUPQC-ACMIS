from django.urls import path
from Api import views_exhibits, views_ris, views_esis, views_student_award
from .views import AccreditationRecords, CreateCategory, FacultyCertificateRecords, ProgramAccreditation, SeminarRecords
from .views_esis import *
from Api import views

app_name = 'apis'

urlpatterns = [
    path('accreditation-records/', AccreditationRecords.as_view(), name='item-list-create'),
    path('program-accreditation-records/', ProgramAccreditation.as_view(), name='program-accreditaion'),

    path('exhibit/', views_exhibits.landing_page, name='exhibit-page'),
    path('student-awards/', views_student_award.landing_page, name='student-award-page'),

    path('esis/extension/records/', views_esis.extension_info, name='extension-info'),
    path('ris/research/infos/students/', views_ris.research_student, name='research-info-student'),
    path('ris/research/infos/faculties/', views_ris.research_faculty, name='research-info-faculty'),

    path('faculty/certificate/records/', FacultyCertificateRecords.as_view(), name='faculty-certificate-info'),
    path('faculty/seminars-workshops-trainings/records/', SeminarRecords.as_view(), name='seminars-workshops-trainings'),
    path('faculty/category/records/', CreateCategory.as_view(), name='category'),
] 