import requests
from rest_framework import generics, serializers
from Accreditation.models import  program_accreditation
from Users.models import category_training, faculty_certificates, seminar_workshop_training
from .serializers import CategorySerializer, FacultyCertificateSerializer, ProgramAccreditationSerializer, WorkshopsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class FacultyCertificateRecords(generics.ListCreateAPIView):
    queryset = faculty_certificates.objects.filter(is_deleted=False)
    serializer_class = FacultyCertificateSerializer


class SeminarRecords(generics.ListCreateAPIView):
    queryset = seminar_workshop_training.objects.filter(is_deleted=False)
    serializer_class = WorkshopsSerializer

class CreateCategory(generics.ListCreateAPIView):
    queryset = category_training.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer


class ProgramAccreditation(generics.ListCreateAPIView):
    queryset = program_accreditation.objects.select_related('program', 'instrument_level').filter(is_deleted=False)
    serializer_class = ProgramAccreditationSerializer