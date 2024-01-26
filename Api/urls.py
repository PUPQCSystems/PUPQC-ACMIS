from django.urls import path
from Api import views_ris, views_esis
from .views import AccreditationRecords, CreateCategory, FacultyCertificateRecords, SeminarRecords
from .views_esis import *
from Api import views

urlpatterns = [
    path('accreditation-records/', AccreditationRecords.as_view(), name='item-list-create'),

    path('esis/extension/records/', views_esis.extension_info, name='extension-info'),
    path('ris/research/records/', views_ris.research_info, name='research-info'),

    path('faculty/certificate/records/', FacultyCertificateRecords.as_view(), name='faculty-certificate-info'),
    path('faculty/seminars-workshops-trainings/records/', SeminarRecords.as_view(), name='seminars-workshops-trainings'),
    path('faculty/category/records/', CreateCategory.as_view(), name='category'),
] 